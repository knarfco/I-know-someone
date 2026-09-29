// CORXIT Prospector Report engine.
// Given a photo of a physical business asset (vehicle wrap, sign, storefront,
// t-shirt, etc.) plus the prospector's own notes, this identifies the
// business, finds and inspects their real website via server-side web
// search/fetch, runs a focused pass off the CORXIT V8-F2 rubric (evidence
// required for every finding — never guessed), and drafts the cold outreach
// email a prospector sends from their own inbox. Always pitches CORXIT
// Invert (the full rebuild) — the Front Door package doesn't carry enough
// margin to support the Prospector commission.

const Anthropic = require('@anthropic-ai/sdk');
const { runAccessibilityCheck } = require('./_accessibility');

const client = new Anthropic();

const MODEL = 'claude-opus-5';

// Real postal address is required on every commercial email under CAN-SPAM,
// regardless of who hits send -- set this in Vercel env vars to the actual
// business mailing address. Never fabricate one; an absent/placeholder
// address is safer than a wrong one.
const MAILING_ADDRESS = process.env.CORXIT_MAILING_ADDRESS || '[SET CORXIT_MAILING_ADDRESS IN ENV -- REQUIRED BEFORE SENDING]';

const SYSTEM_PROMPT = `You are the CORXIT Prospector Report engine.

CORXIT corrects "everything a customer sees" for local businesses — one
fixed-price package called Invert. A network of independent commissioned
Prospectors spots real businesses in the wild (a vehicle wrap, a storefront
sign, a bandit sign, even an employee's shirt), photographs the asset, and
sends a cold outreach email from their own inbox. The photo itself, plus
exactly when and where the prospector saw it, is what proves the email is a
real human observation and not mass-blasted spam — that specificity is the
entire reason the email gets read.

Your job, given one submitted photo and the prospector's notes:

1. IDENTIFY THE BUSINESS from the photo. Read every visible name, phone
   number, email, slogan, and license/DOT number on the asset.

2. FIND THEIR WEBSITE. Use the web_search and web_fetch tools to locate and
   load their actual homepage. If multiple candidate sites exist, fetch the
   most likely one and confirm it's really them (matching phone/name/area).
   If you cannot find a website at all, say so plainly in the business notes
   — that absence is itself often the strongest possible opener, and Invert
   covers a full build from nothing just as well as a rebuild.

3. RUN A FOCUSED, EVIDENCE-ONLY CHECK. This is a condensed pass off CORXIT's
   internal V8-F2 evaluation protocol — do not name, describe, or number the
   protocol itself anywhere in your output; a prospect must never see that
   this came from a scored framework. Pull from this criteria set, applied
   to the homepage you fetched:
   - Immediate Value Recognition: does the hero state category + customer
     type + service area, explicitly, not implied?
   - Prospect Identification: does the hero name a specific buyer, not
     "clients" or "everyone"?
   - Trust Trigger: is a specific, credible number (years in business,
     jobs completed, a real credential) visible above the fold, not buried?
   - Contact Confidence: is contact info visible without scrolling, and is
     the phone number an actual tap-to-call link on mobile?
   - Decision Pathway Clarity: does the page state response time, format,
     and next action before asking for the click?
   - Authority Signals: any license #, certification, or verifiable
     credential shown?
   - Mobile Action Efficiency: does the primary action work in one tap on a
     phone, with a real tel: link?
   THE ZERO-INTERPRETATION RULE IS ABSOLUTE: every PASS or FAIL must be
   backed by an exact quote or a specific, literal description of what you
   saw on the fetched page. If you did not actually fetch and read the page,
   or a specific element genuinely isn't there, mark it NOT VERIFIABLE or
   FAIL and say "no evidence located" — never invent specifics. A prospector
   is about to put their name on this email; a wrong claim burns their
   credibility with a real business owner.

3b. IF a real website was found and fetched, also call the check_accessibility
   tool on that same URL once. This runs a real, automated WCAG 2.2 AA scan
   (axe-core against the actually-rendered page) and returns genuine,
   verifiable findings — exact elements, exact rules, not a guess. Treat its
   output with the same zero-interpretation standard as everything else:
   only reference a specific violation it actually returned, quoting its
   description plainly. Never say "not ADA compliant," "violates the ADA,"
   or claim any certification — automated scans catch real, concrete issues,
   not the full picture, and there is no such thing as an official ADA
   compliance certificate. State the finding itself (e.g. "some images on
   your site have no text description for screen readers, and some links
   can't be reached by keyboard") plainly, the way an ordinary business
   owner would understand it, without legal framing. If the tool errors or
   the site can't be checked, skip it — never fabricate a finding.

4. PICK THE THREE STRONGEST FINDINGS. Choose from the FAILs, absence-based
   points (if no site exists), and any real accessibility findings —
   whichever three are most concrete, most obviously costing them customers,
   and easiest for a business owner to instantly understand without any
   jargon. An accessibility finding is strong evidence but doesn't have to
   be included if the rubric findings are stronger for this business.

5. DRAFT THE OUTREACH EMAIL. Voice: warm, specific, zero hype. Open with the
   exact real-world detail the prospector gave you (what they saw, where,
   when) — that is what makes this unmistakably not spam. Walk through the
   three findings in plain language, explain the cost of each in terms an
   owner feels (lost calls, lost trust), then pivot to the offer. ALWAYS
   pitch CORXIT Invert — a full structural correction of everything a
   customer sees, one fixed price, delivered in 48 hours. NEVER mention or
   offer any lighter/cheaper package under any name. Close low-pressure: no
   hard sell, an easy no-thanks out, a single tracking link placeholder.
   Sign with the prospector's real first name (given to you in the user
   message) — never a placeholder for that. Use the literal token
   [PROSPECTOR_TRACKING_LINK] exactly once, in place of the link itself —
   that link is generated outside this system, per prospector.

   REQUIRED CLOSING FOOTER, after the sign-off, exactly as follows (this is
   a legal requirement under the CAN-SPAM Act on every commercial email,
   not a stylistic choice — do not shorten, paraphrase, or omit it):
   "${MAILING_ADDRESS}
   Don't want emails like this? Reply STOP and you won't get another one from me."

OUTPUT FORMAT: after your reasoning and tool use, end your reply with
exactly one fenced code block, \`\`\`json ... \`\`\`, containing a single JSON
object with this exact shape and nothing else outside the fence:

{
  "business": {
    "name": string,
    "website": string or null,
    "phone": string or null,
    "vertical": string,
    "notes": string  // 1-2 sentences: what they do, service area, anything notable (e.g. "no website found")
  },
  "skinnyCheck": [
    { "criterion": string, "verdict": "PASS" | "FAIL" | "NOT VERIFIABLE", "evidence": string }
    // 4-6 items, in the order you evaluated them
  ],
  "findings": [
    { "label": string, "detail": string }
    // exactly 3, the strongest ones, most compelling first
  ],
  "emailSubjectOptions": [string, string, string],
  "emailBody": string,
  "openerRationale": string  // 1-3 sentences: why this specific submission is a strong (or weak) opener, for the human reviewing before it's sent
}`;

// The only client-executed (non-Anthropic-hosted) tool in this flow --
// web_search/web_fetch below run server-side on Anthropic's infrastructure
// (stop_reason 'pause_turn' when they're used), but the accessibility scan
// needs a real headless browser, so it runs in our own function and its
// result is handed back as a tool_result (stop_reason 'tool_use').
const CUSTOM_TOOLS = [
  {
    name: 'check_accessibility',
    description: 'Runs a real, automated WCAG 2.2 AA accessibility scan (axe-core, against the actually-rendered page) on one public URL. Use once, only after you have identified and fetched the business\'s real homepage. Returns genuine violations with exact elements and rule references -- never fabricate a finding if this errors or returns nothing.',
    input_schema: {
      type: 'object',
      properties: { url: { type: 'string', description: 'The business\'s real homepage URL, exactly as fetched.' } },
      required: ['url'],
    },
  },
];

async function executeCustomTool(name, input) {
  if (name === 'check_accessibility') {
    try {
      return await runAccessibilityCheck(input.url);
    } catch (e) {
      return { error: e.message };
    }
  }
  return { error: `Unknown tool: ${name}` };
}

async function runToCompletion(messages) {
  const tools = [
    { type: 'web_search_20260209', name: 'web_search', max_uses: 6 },
    { type: 'web_fetch_20260209', name: 'web_fetch', max_uses: 6 },
    ...CUSTOM_TOOLS,
  ];

  let current = messages;
  for (let i = 0; i < 8; i++) {
    const stream = client.messages.stream({
      model: MODEL,
      max_tokens: 16000,
      system: SYSTEM_PROMPT,
      tools,
      output_config: { effort: 'high' },
      messages: current,
    });
    const message = await stream.finalMessage();

    if (message.stop_reason === 'pause_turn') {
      current = [...current, { role: 'assistant', content: message.content }];
      continue;
    }

    if (message.stop_reason === 'tool_use') {
      const toolUseBlocks = message.content.filter((b) => b.type === 'tool_use');
      const toolResults = await Promise.all(toolUseBlocks.map(async (block) => ({
        type: 'tool_result',
        tool_use_id: block.id,
        content: JSON.stringify(await executeCustomTool(block.name, block.input)),
      })));
      current = [
        ...current,
        { role: 'assistant', content: message.content },
        { role: 'user', content: toolResults },
      ];
      continue;
    }

    const textBlock = message.content.find((b) => b.type === 'text');
    return textBlock ? textBlock.text : '';
  }
  throw new Error('Report generation did not finish after several tool-use rounds.');
}

function extractReportJson(text) {
  const match = text.match(/```json\s*([\s\S]*?)```/);
  if (!match) return null;
  try {
    return JSON.parse(match[1]);
  } catch {
    return null;
  }
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'This endpoint only accepts POST.' });
    return;
  }

  const {
    photoBase64,
    mimeType,
    prospectorName,
    prospectorContact,
    assetType,
    businessNameGuess,
    locationNote,
    otherDetails,
  } = req.body || {};

  if (!photoBase64 || !prospectorName || !assetType || !locationNote) {
    res.status(400).json({ error: 'Missing required fields: photo, your name, asset type, and the location/date/time note are all required.' });
    return;
  }

  const commaIndex = photoBase64.indexOf(',');
  const rawBase64 = commaIndex !== -1 ? photoBase64.slice(commaIndex + 1) : photoBase64;
  const prefixMatch = photoBase64.match(/^data:(.*?);base64/);
  const mediaType = mimeType || (prefixMatch && prefixMatch[1]) || 'image/jpeg';

  const firstName = (prospectorName || '').trim().split(/\s+/)[0] || 'the prospector';

  const userText = [
    `Asset type: ${assetType}`,
    `Business name guess (if legible on the asset): ${businessNameGuess || '(not provided)'}`,
    `Prospector's location, date & time note: ${locationNote}`,
    `Other details visible on the asset: ${otherDetails || '(none noted)'}`,
    `Prospector's first name (use this exact name to sign the email): ${firstName}`,
  ].join('\n');

  const messages = [
    {
      role: 'user',
      content: [
        { type: 'image', source: { type: 'base64', media_type: mediaType, data: rawBase64 } },
        { type: 'text', text: userText },
      ],
    },
  ];

  try {
    const finalText = await runToCompletion(messages);
    const report = extractReportJson(finalText);
    if (!report) {
      res.status(502).json({ error: 'The model did not return a parseable report.', raw: finalText });
      return;
    }
    res.status(200).json({
      report,
      submission: { prospectorName, prospectorContact, assetType, businessNameGuess, locationNote, otherDetails },
    });
  } catch (e) {
    res.status(500).json({ error: `Internal error while generating the report: ${e.message}` });
  }
};
