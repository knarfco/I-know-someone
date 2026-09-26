// Public config for the static readiness-check.html page. A Turnstile site
// key is meant to be public (it's embedded in the page's own HTML by design,
// unlike the matching secret key), so handing it out here is normal and
// safe. Lets the static page pick up Turnstile the moment it's configured,
// with no redeploy of the site itself.

const { applyCors } = require('./_readiness');

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  res.setHeader('Cache-Control', 'public, max-age=300');
  res.status(200).json({
    turnstileSiteKey: process.env.TURNSTILE_SITE_KEY || null,
  });
};
