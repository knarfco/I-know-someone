// Internal-only accessibility-check endpoint. Deliberately has no linked
// public page and is not referenced from index.html -- callable directly
// (GET /api/accessibility?url=...) for in-house use, or via
// api/prospector.js's own accessibility tool. Not meant for prospects or
// the public to self-serve.

const { runAccessibilityCheck } = require('./_accessibility');

module.exports = async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'GET') return res.status(405).json({ error: 'GET required.' });
  try {
    const report = await runAccessibilityCheck(req.query.url);
    return res.status(200).json(report);
  } catch (e) {
    return res.status(400).json({ error: e.message });
  }
};
