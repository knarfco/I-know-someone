// Shared helpers for the MediaIn360 Super Intelligence Readiness Check —
// the paid ($6.97) version of the Future-Proof Audit. The underscore prefix
// keeps Vercel from exposing this file as its own endpoint.
//
// Everything here switches on by environment variables, so the code can sit
// deployed before the accounts exist:
//   STRIPE_SECRET_KEY       required for checkout + report (sk_live_... / sk_test_...)
//   READINESS_SITE_URL      where the check page lives (default https://mediain360.com)
//   YOUTUBE_API_KEY         enables the YouTube video-presence check
//   SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS / REPORT_FROM_EMAIL
//                           enable emailing the report (Zoho: smtp.zoho.com, 465)
//   REPORT_BCC_EMAIL        optional copy of every report (e.g. info@mediain360.com)
//   TURNSTILE_SITE_KEY / TURNSTILE_SECRET_KEY
//                           enable Cloudflare Turnstile on checkout (get both
//                           from a free Cloudflare account -- see README).
//                           Until both are set, checkout runs with no bot
//                           check at all rather than silently blocking every
//                           submission.

const PRICE_CENTS = 697;
const PRODUCT_NAME = 'Super Intelligence Readiness Check';
const STRIPE_API = 'https://api.stripe.com/v1';
const TURNSTILE_VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify';

function siteUrl() {
  return (process.env.READINESS_SITE_URL || 'https://mediain360.com').replace(/\/+$/, '');
}

// The check page is served from mediain360.com, so its browser calls here are
// cross-origin.
function applyCors(req, res) {
  const allowed = [siteUrl(), siteUrl().replace('://', '://www.')];
  const origin = req.headers && req.headers.origin;
  if (origin && allowed.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function stripeConfigured() {
  return Boolean(process.env.STRIPE_SECRET_KEY);
}

// Stripe's API takes form-encoded bodies with bracketed keys; nested objects
// are flattened into that shape here so no SDK dependency is needed.
function toForm(obj, prefix, out = new URLSearchParams()) {
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined || v === null) continue;
    const key = prefix ? `${prefix}[${k}]` : k;
    if (typeof v === 'object') toForm(v, key, out);
    else out.append(key, String(v));
  }
  return out;
}

async function stripe(method, path, params) {
  const res = await fetch(`${STRIPE_API}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${process.env.STRIPE_SECRET_KEY}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: method === 'GET' ? undefined : toForm(params || {}),
  });
  const data = await res.json();
  if (!res.ok) {
    const msg = (data && data.error && data.error.message) || `Stripe returned HTTP ${res.status}`;
    throw new Error(msg);
  }
  return data;
}

// The audit fetches whatever URL a customer types, server-side. Refuse
// obvious internal addresses so it can't be pointed at private networks.
function isPublicHostname(hostname) {
  const h = hostname.toLowerCase();
  if (h === 'localhost' || h.endsWith('.localhost') || h.endsWith('.local') || h.endsWith('.internal')) return false;
  if (/^(127\.|10\.|0\.|169\.254\.|192\.168\.)/.test(h)) return false;
  if (/^172\.(1[6-9]|2\d|3[01])\./.test(h)) return false;
  if (h.startsWith('[') || h.includes(':')) return false; // IPv6 literals
  return h.includes('.');
}

// Accepts "example.com" as well as full URLs, since business owners rarely
// type the https:// part.
function normalizeWebsite(raw) {
  if (!raw || typeof raw !== 'string') return null;
  let s = raw.trim();
  if (!/^https?:\/\//i.test(s)) s = `https://${s}`;
  try {
    const u = new URL(s);
    if (!/^https?:$/.test(u.protocol) || !isPublicHostname(u.hostname)) return null;
    return u.toString();
  } catch {
    return null;
  }
}

function cleanText(raw, max) {
  if (typeof raw !== 'string') return '';
  return raw.replace(/\s+/g, ' ').trim().slice(0, max);
}

function validEmail(raw) {
  return typeof raw === 'string' && raw.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(raw.trim());
}

function turnstileConfigured() {
  return Boolean(process.env.TURNSTILE_SITE_KEY && process.env.TURNSTILE_SECRET_KEY);
}

// Verifies a Turnstile token with Cloudflare. A verified token, once used,
// can't be replayed -- pair this with checking `payload.success` and nothing
// else. Returns true if Turnstile isn't configured yet, so checkout keeps
// working (with no bot check) until both keys are set.
async function verifyTurnstile(token, remoteIp) {
  if (!turnstileConfigured()) return true;
  if (!token || typeof token !== 'string') return false;
  try {
    const body = new URLSearchParams({ secret: process.env.TURNSTILE_SECRET_KEY, response: token });
    if (remoteIp) body.append('remoteip', remoteIp);
    const res = await fetch(TURNSTILE_VERIFY_URL, { method: 'POST', body });
    if (!res.ok) return false;
    const data = await res.json();
    return Boolean(data.success);
  } catch {
    return false;
  }
}

// Video presence: does anything on YouTube mention this business by name for
// its city? Mechanical like the rest of the audit — PASS only when a result's
// title, channel, or description actually contains the business name.
async function checkYouTubePresence(business, city) {
  const name = 'YouTube Presence';
  if (!process.env.YOUTUBE_API_KEY) {
    return { name, verdict: 'NOT VERIFIABLE', evidence: 'The YouTube check is not switched on yet.' };
  }
  const query = `${business} ${city}`.trim();
  const params = new URLSearchParams({
    part: 'snippet',
    q: query,
    type: 'video',
    maxResults: '10',
    key: process.env.YOUTUBE_API_KEY,
  });
  try {
    const res = await fetch(`https://www.googleapis.com/youtube/v3/search?${params}`);
    if (!res.ok) {
      return { name, verdict: 'NOT VERIFIABLE', evidence: `YouTube search returned HTTP ${res.status}.` };
    }
    const data = await res.json();
    const needle = business.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
    const norm = (s) => (s || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ');
    const hit = (data.items || []).find((it) => {
      const sn = it.snippet || {};
      return [sn.title, sn.channelTitle, sn.description].some((t) => norm(t).includes(needle));
    });
    if (hit) {
      return {
        name,
        verdict: 'PASS',
        evidence: `Searching YouTube for "${query}" found a video mentioning your business: "${hit.snippet.title}".`,
      };
    }
    return {
      name,
      verdict: 'FAIL',
      evidence: `Searching YouTube for "${query}" returned no video that mentions your business by name.`,
    };
  } catch (e) {
    return { name, verdict: 'NOT VERIFIABLE', evidence: `YouTube search could not be completed: ${e.message}` };
  }
}

function emailConfigured() {
  return Boolean(process.env.SMTP_HOST && process.env.SMTP_USER && process.env.SMTP_PASS && process.env.REPORT_FROM_EMAIL);
}

async function sendReportEmail(to, subject, text) {
  const nodemailer = require('nodemailer');
  const port = Number(process.env.SMTP_PORT || 465);
  const transport = nodemailer.createTransport({
    host: process.env.SMTP_HOST,
    port,
    secure: port === 465,
    auth: { user: process.env.SMTP_USER, pass: process.env.SMTP_PASS },
  });
  await transport.sendMail({
    from: `MediaIn360 <${process.env.REPORT_FROM_EMAIL}>`,
    to,
    bcc: process.env.REPORT_BCC_EMAIL || undefined,
    subject,
    text,
  });
}

module.exports = {
  PRICE_CENTS,
  PRODUCT_NAME,
  siteUrl,
  applyCors,
  stripeConfigured,
  stripe,
  normalizeWebsite,
  cleanText,
  validEmail,
  turnstileConfigured,
  verifyTurnstile,
  checkYouTubePresence,
  emailConfigured,
  sendReportEmail,
};
