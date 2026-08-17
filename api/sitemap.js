// Discovers every page URL for a site by reading its sitemap.xml, so
// bulk mode can run the same single-page audit against each one in turn.
// Purely a discovery step — it does not run any of the 9 criteria itself.

const cheerio = require('cheerio');

const FETCH_TIMEOUT_MS = 10000;
const MAX_PAGES = 150;
const MAX_SITEMAP_FILES = 20;

async function fetchWithTimeout(url, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
  try {
    return await fetch(url, { ...options, signal: controller.signal, redirect: 'follow' });
  } finally {
    clearTimeout(timeout);
  }
}

async function fetchSitemapLocs(sitemapUrl) {
  const res = await fetchWithTimeout(sitemapUrl, {
    headers: { 'User-Agent': 'FutureProofAuditBot/2.0 (+mechanical audit tool)' },
  });
  if (!res.ok) return { ok: false, status: res.status };
  const xml = await res.text();
  const $ = cheerio.load(xml, { xmlMode: true });
  const locs = $('loc')
    .map((i, el) => $(el).text().trim())
    .get()
    .filter(Boolean);
  return { ok: true, locs };
}

async function discoverPages(rootUrl) {
  const origin = new URL(rootUrl).origin;
  const candidateSitemaps = [`${origin}/sitemap.xml`];
  const pages = [];
  const seenSitemaps = new Set();
  let sitemapsFetched = 0;

  while (candidateSitemaps.length > 0 && sitemapsFetched < MAX_SITEMAP_FILES && pages.length < MAX_PAGES) {
    const next = candidateSitemaps.shift();
    if (seenSitemaps.has(next)) continue;
    seenSitemaps.add(next);
    sitemapsFetched++;

    let result;
    try {
      result = await fetchSitemapLocs(next);
    } catch (e) {
      continue;
    }
    if (!result.ok) continue;

    for (const loc of result.locs) {
      if (/\.xml$/i.test(loc)) {
        candidateSitemaps.push(loc);
      } else {
        pages.push(loc);
      }
      if (pages.length >= MAX_PAGES) break;
    }
  }

  return { pages: pages.slice(0, MAX_PAGES), sitemapsFetched, truncated: pages.length > MAX_PAGES };
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
    const { pages, sitemapsFetched, truncated } = await discoverPages(targetUrl);
    if (sitemapsFetched === 0 || pages.length === 0) {
      res.status(200).json({
        pages: [],
        error: `No sitemap.xml could be found or read at ${new URL(targetUrl).origin}/sitemap.xml. Bulk mode needs a sitemap to discover pages — try checking pages individually instead.`,
      });
      return;
    }
    res.status(200).json({ pages, truncated, maxPages: MAX_PAGES });
  } catch (e) {
    res.status(500).json({ error: `Internal error while reading the sitemap: ${e.message}` });
  }
};
