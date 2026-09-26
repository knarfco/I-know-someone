// Starts a $1.99 Super Intelligence Readiness Check: validates the form and
// hands back a Stripe Checkout URL. The website, business name, and city ride
// along in the session's metadata, so the report endpoint can recover them
// from Stripe itself instead of trusting anything the browser sends later.

const {
  PRICE_CENTS,
  PRODUCT_NAME,
  siteUrl,
  applyCors,
  stripeConfigured,
  stripe,
  normalizeWebsite,
  cleanText,
  validEmail,
} = require('./_readiness');

function readBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') {
    try {
      return JSON.parse(req.body);
    } catch {
      return {};
    }
  }
  return {};
}

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Use POST.' });
    return;
  }
  if (!stripeConfigured()) {
    res.status(503).json({ error: 'not_configured' });
    return;
  }

  const body = readBody(req);
  const website = normalizeWebsite(body.website);
  const business = cleanText(body.business, 120);
  const city = cleanText(body.city, 80);
  const email = typeof body.email === 'string' ? body.email.trim() : '';

  if (!website) {
    res.status(400).json({ error: 'Please enter a valid public website address, like yourbusiness.com.' });
    return;
  }
  if (!business) {
    res.status(400).json({ error: 'Please enter your business name.' });
    return;
  }
  if (!city) {
    res.status(400).json({ error: 'Please enter the city you serve.' });
    return;
  }
  if (!validEmail(email)) {
    res.status(400).json({ error: 'Please enter a valid email address.' });
    return;
  }

  try {
    const page = `${siteUrl()}/readiness-check.html`;
    const session = await stripe('POST', '/checkout/sessions', {
      mode: 'payment',
      customer_email: email,
      line_items: {
        0: {
          quantity: 1,
          price_data: {
            currency: 'usd',
            unit_amount: PRICE_CENTS,
            product_data: {
              name: PRODUCT_NAME,
              description: `Website and video readiness report for ${business}`,
            },
          },
        },
      },
      metadata: { website, business, city },
      success_url: `${page}?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${page}?canceled=1`,
    });
    res.status(200).json({ checkoutUrl: session.url });
  } catch (e) {
    res.status(502).json({ error: `Could not start checkout: ${e.message}` });
  }
};
