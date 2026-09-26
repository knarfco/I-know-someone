// Runs the paid Super Intelligence Readiness Check. Only works for a Stripe
// Checkout session that is actually paid; the website, business, and city
// come from that session's metadata, never from the query string. The same
// session can be reloaded (it's the customer's report), but the email copy
// goes out only once, tracked on the PaymentIntent's metadata.

const { runAudit, CRITERIA_META } = require('./audit');
const {
  PRODUCT_NAME,
  siteUrl,
  applyCors,
  stripeConfigured,
  stripe,
  checkYouTubePresence,
  emailConfigured,
  sendReportEmail,
} = require('./_readiness');

// Plain-English names and "why it matters" lines for business owners; the
// verdicts themselves still come straight from the mechanical audit.
const FRIENDLY = {
  h1: ['Clear main headline', 'AI and search engines use your main headline to understand what the page is about.'],
  heading_hierarchy: ['Organized page structure', 'Well-ordered headings help machines read your page like an outline.'],
  canonical: ['Official page address', 'Tells search engines which address is the real version of this page.'],
  meta_description: ['Search result description', 'The summary Google and AI tools can show about your page.'],
  schema: ['Machine-readable business data', 'Structured data lets AI read facts about you instead of guessing.'],
  crawlability: ['Search engines can read the page', 'If search engines are blocked, nothing else matters.'],
  ai_crawler_access: ['AI assistants are allowed in', 'Your site must let AI crawlers like GPTBot and ClaudeBot read it.'],
  org_schema_completeness: ['Complete business details for AI', 'Name, address, phone and more, in a form AI can read directly.'],
  faq_schema: ['FAQ readable by AI', 'Marked-up FAQs are easy for AI answers to quote.'],
};

function summarize(checks) {
  const counted = checks.filter((c) => c.verdict !== 'SKIPPED');
  const passed = counted.filter((c) => c.verdict === 'PASS').length;
  return { passed, total: counted.length };
}

function reportText(r) {
  const lines = [
    `${PRODUCT_NAME} for ${r.business} (${r.city})`,
    `Website checked: ${r.website}`,
    `Checked: ${new Date(r.dateChecked).toUTCString()}`,
    '',
    `WEBSITE READINESS: ${r.websiteScore.passed}/${r.websiteScore.total}`,
    ...r.websiteChecks.map((c) => `- ${c.verdict}: ${c.name} — ${c.evidence}`),
    '',
    `VIDEO PRESENCE: ${r.videoScore.passed}/${r.videoScore.total}`,
    ...r.videoChecks.map((c) => `- ${c.verdict}: ${c.name} — ${c.evidence}`),
    '',
    r.ready
      ? 'Your business passed every check. You are in great shape for AI search today.'
      : 'Your business is not future-proof yet. MediaIn360 fixes what is missing:',
    `${siteUrl()}/self-shoot.html#get-started`,
    '',
    'This report checks the one page you entered, mechanically. It does not guarantee what any AI will recommend.',
  ];
  return lines.join('\n');
}

module.exports = async (req, res) => {
  applyCors(req, res);
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  if (!stripeConfigured()) {
    res.status(503).json({ error: 'not_configured' });
    return;
  }

  const sessionId = req.query && req.query.session_id;
  if (typeof sessionId !== 'string' || !/^cs_[A-Za-z0-9_]+$/.test(sessionId)) {
    res.status(400).json({ error: 'Missing or invalid checkout session.' });
    return;
  }

  let session;
  try {
    session = await stripe('GET', `/checkout/sessions/${sessionId}?expand[]=payment_intent`);
  } catch (e) {
    res.status(404).json({ error: 'We could not find that checkout. If you were charged, email info@mediain360.com.' });
    return;
  }
  if (session.payment_status !== 'paid') {
    res.status(402).json({ error: 'This check has not been paid for yet.' });
    return;
  }

  const { website, business, city } = session.metadata || {};
  if (!website || !business) {
    res.status(500).json({ error: 'This checkout is missing its details. Email info@mediain360.com and we will run it for you.' });
    return;
  }

  try {
    const [audit, youtube] = await Promise.all([runAudit(website), checkYouTubePresence(business, city || '')]);
    const websiteChecks = CRITERIA_META.map((c) => {
      const r = audit.results[c.id] || { verdict: 'NOT VERIFIABLE', evidence: 'No result.' };
      const [name, why] = FRIENDLY[c.id] || [c.name, ''];
      return { id: c.id, name, why, verdict: r.verdict, evidence: r.evidence };
    });
    const videoChecks = [
      { id: 'youtube', why: 'Google\'s AI answers cite YouTube more than any other website.', ...youtube },
    ];
    const websiteScore = summarize(websiteChecks);
    const videoScore = summarize(videoChecks);
    const report = {
      business,
      city: city || '',
      website,
      dateChecked: audit.dateChecked,
      websiteChecks,
      videoChecks,
      websiteScore,
      videoScore,
      ready: websiteScore.passed === websiteScore.total && videoScore.passed === videoScore.total,
      emailed: false,
    };

    const pi = session.payment_intent && typeof session.payment_intent === 'object' ? session.payment_intent : null;
    const alreadyEmailed = pi && pi.metadata && pi.metadata.report_emailed === 'yes';
    if (emailConfigured() && pi && !alreadyEmailed && session.customer_details && session.customer_details.email) {
      try {
        await sendReportEmail(
          session.customer_details.email,
          `Your ${PRODUCT_NAME}: ${business}`,
          reportText(report),
        );
        await stripe('POST', `/payment_intents/${pi.id}`, { metadata: { report_emailed: 'yes' } });
        report.emailed = true;
      } catch (e) {
        // The on-screen report still works; the email just didn't go out.
        report.emailError = true;
      }
    } else if (alreadyEmailed) {
      report.emailed = true;
    }

    res.status(200).json(report);
  } catch (e) {
    res.status(500).json({ error: `Something went wrong running your check: ${e.message}` });
  }
};
