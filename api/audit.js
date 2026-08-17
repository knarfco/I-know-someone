// Future-Proof Audit V2 — mechanical, deterministic checker.
// Implements the 9 criteria exactly as written in the "Future-Proof Audit — V2" spec.
// No AI judgment is used anywhere in this file: every verdict is produced by
// parsing the raw HTML (and robots.txt) and applying the literal PASS/FAIL
// conditions from the spec. Where the spec's evidence cannot be confirmed
// from raw source, the verdict is NOT VERIFIABLE (never guessed).

const cheerio = require('cheerio');

const AI_AGENTS = ['GPTBot', 'ClaudeBot', 'PerplexityBot', 'Google-Extended', 'OAI-SearchBot'];
const FETCH_TIMEOUT_MS = 10000;

async function fetchWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    return await fetch(url, { ...options, signal: controller.signal, redirect: 'follow' });
  } finally {
    clearTimeout(timeout);
  }
}

function extractJsonLdBlocks($) {
  const blocks = [];
  $('script[type="application/ld+json"]').each((i, el) => {
    const raw = $(el).contents().text();
    let parsed = null;
    let error = null;
    try {
      parsed = JSON.parse(raw);
    } catch (e) {
      error = e.message;
    }
    blocks.push({ raw, parsed, error });
  });
  return blocks;
}

// Pulls every object carrying an @type out of a parsed JSON-LD tree,
// including objects nested inside an @graph array.
function flattenTyped(parsed) {
  const out = [];
  function walk(node) {
    if (!node || typeof node !== 'object') return;
    if (Array.isArray(node)) {
      node.forEach(walk);
      return;
    }
    if (node['@graph']) walk(node['@graph']);
    if (node['@type']) out.push(node);
  }
  walk(parsed);
  return out;
}

function checkH1($) {
  const h1s = $('h1');
  const count = h1s.length;
  if (count === 0) {
    return { verdict: 'FAIL', evidence: 'No <h1> tag found anywhere in the page source.' };
  }
  if (count > 1) {
    const texts = h1s.map((i, e) => $(e).text().trim() || '(empty)').get();
    return { verdict: 'FAIL', evidence: `${count} <h1> tags found: ${texts.join(' | ')}` };
  }
  const text = h1s.first().text().trim();
  if (!text) {
    return { verdict: 'FAIL', evidence: 'Exactly one <h1> tag found, but its content is empty.' };
  }
  return { verdict: 'PASS', evidence: `Exactly one <h1> tag found with content: "${text}"` };
}

function checkHeadingHierarchy($) {
  const headings = [];
  $('h1,h2,h3,h4,h5,h6').each((i, el) => {
    headings.push(parseInt(el.tagName.substring(1), 10));
  });
  if (headings.length <= 1) {
    return {
      verdict: 'FAIL',
      evidence: `Heading sequence: ${headings.map((h) => 'H' + h).join(' > ') || '(none found)'}. No heading structure exists below the H1.`,
    };
  }
  let maxSoFar = headings[0];
  for (let i = 1; i < headings.length; i++) {
    if (headings[i] > maxSoFar + 1) {
      return {
        verdict: 'FAIL',
        evidence: `Heading sequence: ${headings.map((h) => 'H' + h).join(' > ')}. Level skipped: H${maxSoFar} followed directly by H${headings[i]}.`,
      };
    }
    maxSoFar = Math.max(maxSoFar, headings[i]);
  }
  return {
    verdict: 'PASS',
    evidence: `Heading sequence: ${headings.map((h) => 'H' + h).join(' > ')}. No skipped levels going down the page.`,
  };
}

function checkCanonical($) {
  const link = $('head link[rel="canonical"]').first();
  if (link.length === 0) {
    return { verdict: 'FAIL', evidence: 'No <link rel="canonical"> found inside <head>.' };
  }
  const href = (link.attr('href') || '').trim();
  if (!href) {
    return { verdict: 'FAIL', evidence: '<link rel="canonical"> found but its href attribute is empty.' };
  }
  if (!/^https?:\/\//i.test(href)) {
    return {
      verdict: 'FAIL',
      evidence: `<link rel="canonical" href="${href}"> found but href is not a complete, absolute URL.`,
    };
  }
  return { verdict: 'PASS', evidence: `<link rel="canonical" href="${href}"> found in <head>.` };
}

function checkMetaDescription($) {
  const meta = $('head meta[name="description"]').first();
  if (meta.length === 0) {
    return { verdict: 'FAIL', evidence: 'No <meta name="description"> found inside <head>.' };
  }
  const content = (meta.attr('content') || '').trim();
  if (!content) {
    return { verdict: 'FAIL', evidence: '<meta name="description"> found but its content attribute is empty.' };
  }
  return { verdict: 'PASS', evidence: `<meta name="description" content="${content}"> found.` };
}

function checkSchema(blocks) {
  if (blocks.length === 0) {
    return { verdict: 'FAIL', evidence: 'No <script type="application/ld+json"> block found anywhere on the page.' };
  }
  for (const b of blocks) {
    if (b.parsed) {
      const typed = flattenTyped(b.parsed).find((o) => o['@type']);
      if (typed) {
        const t = Array.isArray(typed['@type']) ? typed['@type'].join(', ') : typed['@type'];
        return { verdict: 'PASS', evidence: `Valid JSON-LD block found with @type "${t}".` };
      }
    }
  }
  const errors = blocks.filter((b) => b.error);
  if (errors.length > 0) {
    return {
      verdict: 'FAIL',
      evidence: `${blocks.length} JSON-LD block(s) found; none contained a usable @type. Parse error(s): ${errors
        .map((b) => b.error)
        .join('; ')}`,
    };
  }
  return {
    verdict: 'FAIL',
    evidence: `${blocks.length} JSON-LD block(s) found and parsed as valid JSON, but none contain a recognizable @type value.`,
  };
}

function checkCrawlability($, httpStatus) {
  const meta = $('head meta[name="robots"]').first();
  const rawContent = meta.length ? meta.attr('content') || '' : '';
  const content = rawContent.toLowerCase();
  const blocked = content.includes('noindex') || content.includes('nofollow');
  const statusOk = httpStatus === 200;
  const metaEvidence = meta.length ? `<meta name="robots" content="${rawContent}">` : 'No <meta name="robots"> tag found.';
  const evidence = `${metaEvidence} HTTP status returned: ${httpStatus}.`;
  if (blocked || !statusOk) {
    return { verdict: 'FAIL', evidence };
  }
  return { verdict: 'PASS', evidence };
}

function parseRobotsTxt(text) {
  const groups = [];
  let current = null;
  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.split('#')[0].trim();
    if (!line) continue;
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    const field = line.slice(0, idx).trim().toLowerCase();
    const value = line.slice(idx + 1).trim();
    if (field === 'user-agent') {
      if (!current || current.rules.length > 0) {
        current = { agents: [], rules: [] };
        groups.push(current);
      }
      current.agents.push(value.toLowerCase());
    } else if ((field === 'disallow' || field === 'allow') && current) {
      current.rules.push({ type: field, path: value });
    }
  }
  return groups;
}

async function fetchRobotsTxt(pageUrl) {
  let origin;
  try {
    origin = new URL(pageUrl).origin;
  } catch {
    return { status: 'error', error: 'Could not derive site root from URL.' };
  }
  try {
    const res = await fetchWithTimeout(`${origin}/robots.txt`);
    if (res.status === 404) return { status: 'not_found' };
    if (!res.ok) return { status: 'error', error: `robots.txt request returned HTTP ${res.status}.` };
    const text = await res.text();
    return { status: 'ok', text };
  } catch (e) {
    return { status: 'error', error: e.message };
  }
}

function checkAiCrawlerAccess(robotsResult, pageUrl) {
  if (robotsResult.status === 'not_found') {
    return { verdict: 'PASS', evidence: 'No robots.txt found at the site root; no rules exist to block AI crawlers.' };
  }
  if (robotsResult.status === 'error') {
    return {
      verdict: 'NOT VERIFIABLE',
      evidence: `robots.txt could not be retrieved (${robotsResult.error}).`,
    };
  }
  const groups = parseRobotsTxt(robotsResult.text);
  let path;
  try {
    path = new URL(pageUrl).pathname || '/';
  } catch {
    path = '/';
  }
  const blockedAgents = [];
  for (const agent of AI_AGENTS) {
    const matchingGroups = groups.filter((g) => g.agents.includes(agent.toLowerCase()));
    for (const g of matchingGroups) {
      for (const rule of g.rules) {
        if (rule.type === 'disallow' && rule.path !== '' && path.startsWith(rule.path)) {
          blockedAgents.push(`${agent} (Disallow: ${rule.path})`);
        }
      }
    }
  }
  if (blockedAgents.length > 0) {
    return { verdict: 'FAIL', evidence: `robots.txt blocks: ${blockedAgents.join(', ')} for path "${path}".` };
  }
  return {
    verdict: 'PASS',
    evidence: `robots.txt retrieved; no Disallow rule blocks ${AI_AGENTS.join(', ')} from path "${path}".`,
  };
}

function findOrgCandidates(blocks) {
  const candidates = [];
  for (const b of blocks) {
    if (!b.parsed) continue;
    for (const obj of flattenTyped(b.parsed)) {
      const types = Array.isArray(obj['@type']) ? obj['@type'] : [obj['@type']];
      if (types.includes('Organization') || types.includes('LocalBusiness')) {
        candidates.push(obj);
      }
    }
  }
  return candidates;
}

function checkOrgSchemaCompleteness(blocks) {
  const candidates = findOrgCandidates(blocks);
  if (candidates.length === 0) {
    return { verdict: 'FAIL', evidence: 'No JSON-LD block with @type Organization or LocalBusiness found.' };
  }
  let bestMissing = null;
  for (const obj of candidates) {
    const hasName = !!(obj.name && String(obj.name).trim());
    const addr = obj.address || obj.location;
    const hasAddress = !!addr && (typeof addr === 'string' ? addr.trim() !== '' : Object.keys(addr).length > 0);
    const hasPhone = !!(obj.telephone && String(obj.telephone).trim());
    const sameAs = obj.sameAs;
    const hasSameAs = Array.isArray(sameAs) ? sameAs.length > 0 : !!(sameAs && String(sameAs).trim());
    if (hasName && hasAddress && hasPhone && hasSameAs) {
      return {
        verdict: 'PASS',
        evidence: `Organization/LocalBusiness JSON-LD block found with non-empty name, address, telephone, and sameAs.`,
      };
    }
    const missing = [];
    if (!hasName) missing.push('name');
    if (!hasAddress) missing.push('address');
    if (!hasPhone) missing.push('telephone');
    if (!hasSameAs) missing.push('sameAs');
    if (!bestMissing) bestMissing = missing;
  }
  return {
    verdict: 'FAIL',
    evidence: `Organization/LocalBusiness JSON-LD block found but missing: ${bestMissing.join(', ')}.`,
  };
}

function detectFaqContent($) {
  const faqHeadings = [];
  $('h1,h2,h3,h4,h5,h6').each((i, el) => {
    const text = $(el).text().trim();
    if (text.endsWith('?')) {
      const next = $(el).next();
      if (next.length && next.text().trim()) {
        faqHeadings.push(text);
      }
    }
  });
  return faqHeadings;
}

function checkFaqSchema($, blocks) {
  const faqHeadings = detectFaqContent($);
  if (faqHeadings.length === 0) {
    return {
      verdict: 'SKIPPED',
      evidence: 'No FAQ-style content (a heading ending in "?" immediately followed by an answer) was detected on the page.',
    };
  }
  for (const b of blocks) {
    if (!b.parsed) continue;
    for (const obj of flattenTyped(b.parsed)) {
      const types = Array.isArray(obj['@type']) ? obj['@type'] : [obj['@type']];
      if (types.includes('FAQPage')) {
        return {
          verdict: 'PASS',
          evidence: `FAQ-style content detected (e.g. "${faqHeadings[0]}") and a matching FAQPage JSON-LD block was found.`,
        };
      }
    }
  }
  return {
    verdict: 'FAIL',
    evidence: `FAQ-style content detected (e.g. "${faqHeadings[0]}") but no matching FAQPage JSON-LD block was found.`,
  };
}

const CRITERIA_META = [
  { id: 'h1', name: 'H1 Present & Unique' },
  { id: 'heading_hierarchy', name: 'Heading Hierarchy Logical' },
  { id: 'canonical', name: 'Canonical Tag Present' },
  { id: 'meta_description', name: 'Meta Description Present' },
  { id: 'schema', name: 'Structured Data (Schema) Present & Valid' },
  { id: 'crawlability', name: 'Crawlability Baseline' },
  { id: 'ai_crawler_access', name: 'AI Crawler Access' },
  { id: 'org_schema_completeness', name: 'Organization/LocalBusiness Schema Completeness' },
  { id: 'faq_schema', name: 'FAQPage Schema (Conditional)' },
];

function notVerifiableAll(reason) {
  const results = {};
  for (const c of CRITERIA_META) {
    results[c.id] = { verdict: 'NOT VERIFIABLE', evidence: reason };
  }
  return results;
}

async function runAudit(targetUrl) {
  let pageRes;
  let html;
  let httpStatus = null;
  try {
    pageRes = await fetchWithTimeout(targetUrl, {
      headers: { 'User-Agent': 'FutureProofAuditBot/2.0 (+mechanical audit tool)' },
    });
    httpStatus = pageRes.status;
    html = await pageRes.text();
  } catch (e) {
    return {
      url: targetUrl,
      accessMethod: 'Raw HTML source (fetched via tool)',
      dateChecked: new Date().toISOString(),
      httpStatus: null,
      fetchError: e.message,
      results: notVerifiableAll(`Could not fetch the URL: ${e.message}`),
    };
  }

  const $ = cheerio.load(html);
  const jsonLdBlocks = extractJsonLdBlocks($);
  const robotsResult = await fetchRobotsTxt(targetUrl);

  const results = {
    h1: checkH1($),
    heading_hierarchy: checkHeadingHierarchy($),
    canonical: checkCanonical($),
    meta_description: checkMetaDescription($),
    schema: checkSchema(jsonLdBlocks),
    crawlability: checkCrawlability($, httpStatus),
    ai_crawler_access: checkAiCrawlerAccess(robotsResult, targetUrl),
    org_schema_completeness: checkOrgSchemaCompleteness(jsonLdBlocks),
    faq_schema: checkFaqSchema($, jsonLdBlocks),
  };

  return {
    url: targetUrl,
    accessMethod: 'Raw HTML source (fetched via tool)',
    dateChecked: new Date().toISOString(),
    httpStatus,
    results,
  };
}

module.exports = async (req, res) => {
  const rawUrl = req.query && req.query.url;
  if (!rawUrl || typeof rawUrl !== 'string') {
    res.status(400).json({ error: 'Missing required "url" query parameter.' });
    return;
  }
  let targetUrl;
  try {
    targetUrl = new URL(rawUrl).toString();
    if (!/^https?:$/.test(new URL(targetUrl).protocol)) throw new Error('not http(s)');
  } catch {
    res.status(400).json({ error: 'The URL provided is not a valid, complete http:// or https:// URL.' });
    return;
  }

  try {
    const report = await runAudit(targetUrl);
    const meta = CRITERIA_META;
    res.status(200).json({ ...report, criteriaOrder: meta });
  } catch (e) {
    res.status(500).json({ error: `Internal error while auditing: ${e.message}` });
  }
};

module.exports.CRITERIA_META = CRITERIA_META;
module.exports.runAudit = runAudit;
module.exports.checks = {
  checkH1,
  checkHeadingHierarchy,
  checkCanonical,
  checkMetaDescription,
  checkSchema,
  checkCrawlability,
  checkAiCrawlerAccess,
  checkOrgSchemaCompleteness,
  checkFaqSchema,
  extractJsonLdBlocks,
  parseRobotsTxt,
};
