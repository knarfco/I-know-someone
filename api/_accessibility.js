// Shared accessibility-scan core (WCAG 2.2 A/AA via axe-core against the
// real rendered page). Used two ways: api/accessibility.js exposes it as a
// plain internal HTTP endpoint; api/prospector.js calls runAccessibilityCheck
// directly as a Claude tool implementation, once it has identified and
// fetched a business's real homepage.
//
// Never issues a pass/fail "compliance" verdict -- automated tools only
// catch a fraction of real WCAG issues, so this reports concrete, verifiable
// findings (exact elements, exact rules) and says plainly that manual review
// is still required. See conclusion field.

const dns = require('node:dns').promises;
const net = require('node:net');
const { chromium: browserType } = require('playwright-core');
const chromium = require('@sparticuz/chromium').default;
const axe = require('axe-core');

const TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const MAX_NODES = 12;

function publicIP(ip) {
  if (net.isIP(ip) === 4) {
    const [a, b] = ip.split('.').map(Number);
    return !(a === 0 || a === 10 || a === 127 || a >= 224 ||
      (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) ||
      (a === 192 && b === 168) || (a === 100 && b >= 64 && b <= 127) ||
      (a === 192 && b === 0) || (a === 198 && (b === 18 || b === 19)));
  }
  if (net.isIP(ip) === 6) {
    const s = ip.toLowerCase();
    if (s.startsWith('::ffff:')) return publicIP(s.slice(7));
    return !(s === '::' || s === '::1' || s.startsWith('fc') || s.startsWith('fd') ||
      s.startsWith('fe8') || s.startsWith('fe9') || s.startsWith('fea') || s.startsWith('feb') ||
      s.startsWith('2001:db8:'));
  }
  return false;
}

async function validate(input) {
  if (typeof input !== 'string' || input.length > 2048) throw Error('Enter one public website URL.');
  const url = new URL(/^https?:\/\//i.test(input) ? input : 'https://' + input);
  if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password ||
      !['', '80', '443'].includes(url.port)) throw Error('Only public HTTP(S) websites on standard ports can be checked.');
  const host = url.hostname.replace(/\.$/, '').toLowerCase();
  if (!host.includes('.') || host.endsWith('.local') || host.endsWith('.internal') || net.isIP(host))
    throw Error('Enter a public domain name.');
  const addresses = await dns.lookup(host, { all: true, verbatim: true });
  if (!addresses.length || addresses.some(a => !publicIP(a.address))) throw Error('This address is not a public website.');
  return url.toString();
}

async function runAccessibilityCheck(inputUrl) {
  const url = await validate(inputUrl);
  let browser;
  try {
    browser = await browserType.launch({
      args: chromium.args,
      executablePath: await chromium.executablePath(),
      headless: true,
    });
    const context = await browser.newContext({ viewport: { width: 1365, height: 900 }, serviceWorkers: 'block' });
    const page = await context.newPage();
    await page.route('**/*', async route => {
      try {
        const requestUrl = route.request().url();
        if (!/^https?:/i.test(requestUrl)) return route.abort();
        await validate(requestUrl);
        return route.continue();
      } catch { return route.abort(); }
    });
    const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 18000 });
    await page.waitForTimeout(800);
    await page.addScriptTag({ content: axe.source });
    const result = await page.evaluate(tags => window.axe.run(document, {
      runOnly: { type: 'tag', values: tags },
      resultTypes: ['violations', 'incomplete', 'passes'],
    }), TAGS);
    const compact = list => list.map(v => ({
      id: v.id, impact: v.impact, description: v.help, helpUrl: v.helpUrl,
      wcag: v.tags.filter(t => /^wcag\d/.test(t)), count: v.nodes.length,
      nodes: v.nodes.slice(0, MAX_NODES).map(n => ({ target: n.target, summary: n.failureSummary || n.any.map(x => x.message).join('; '), html: n.html.slice(0, 500) })),
    }));
    return {
      requestedUrl: url, finalUrl: page.url(), checkedAt: new Date().toISOString(),
      httpStatus: response?.status() ?? null, title: await page.title(),
      standard: 'WCAG 2.2 Level AA automated rules (axe-core)',
      violations: compact(result.violations), needsReview: compact(result.incomplete),
      passingRules: result.passes.length,
      conclusion: result.violations.length ? 'Automated accessibility issues found' : 'No automated issues found in tested rules; manual review still required',
    };
  } finally {
    if (browser) await browser.close().catch(() => {});
  }
}

module.exports = { runAccessibilityCheck, validate, publicIP };
