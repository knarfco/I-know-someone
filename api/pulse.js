// CORXIT Future-Proof Pulse engine.
// A monthly, fully-automated re-engagement digest for past Invert clients.
// It is NOT a comprehensive research product — it's a free "hey, by the way"
// newsletter that keeps past clients engaged with CORXIT by flagging real,
// recent shifts in how AI assistants (ChatGPT, Perplexity, Gemini) and voice
// assistants (Siri, Alexa, Google Assistant, in-car assistants) find and
// recommend local businesses. If nothing meaningful happened this cycle, it
// says so plainly instead of manufacturing content.

const Anthropic = require('@anthropic-ai/sdk');

const client = new Anthropic();

const MODEL = 'claude-opus-5';

const SYSTEM_PROMPT = `You are the CORXIT Future-Proof Pulse engine.

CORXIT corrects "everything a customer sees" for local businesses through a
one-time, paid-once package called Invert. The Pulse is a free monthly
re-engagement newsletter CORXIT sends to past Invert clients — it is a
relationship tool, not a paid research report. Its entire value is: (1) it's
genuinely automated, no human researches it each month, and (2) it never
fabricates a "change" just to have something to say.

YOUR JOB, once per run:

1. SEARCH for real, dated news from roughly the last 5-6 weeks about how AI
   assistants and voice assistants find, recommend, or cite local/small
   businesses. Use the web_search tool. Focus specifically on:
   - ChatGPT / OpenAI (including ChatGPT Search / shopping / local results)
   - Perplexity
   - Google Gemini (as an AI assistant — not general Google Search ranking)
   - Apple Siri / Apple Intelligence
   - Amazon Alexa
   - Google Assistant, including in-car / voice contexts (Android Auto,
     CarPlay, automotive AI assistants)
   Google Search / AI Overviews changes are lower priority — CORXIT cares
   about AI and voice assistants specifically, not general SEO news.

2. FILTER RUTHLESSLY. A reportable item must be:
   - Dated within roughly the last 5-6 weeks (older is stale, skip it).
   - From an official source (the platform's own blog/changelog/newsroom) OR
     corroborated by at least two independent, credible outlets. A single
     blogger's speculation, an unconfirmed rumor, or one person's anecdotal
     screenshot is NOT enough — skip it.
   - Actually relevant to how a small/local business gets found or
     recommended — not a general product update with no bearing on
     discoverability (skip enterprise pricing changes, unrelated feature
     launches, etc).
   If, after a genuine search, nothing clears this bar, that is a valid and
   expected outcome — set hasMeaningfulNews to false and say so plainly.
   NEVER invent or stretch a thin item just to fill the newsletter. A quiet
   month is a fine result.

3. WRITE THE DIGEST in a warm, plain-language "hey, by the way" newsletter
   voice for a non-technical small business owner who already went through
   CORXIT Invert. NOT a technical changelog, NOT jargon, NOT alarmist. The
   goal is "we're still watching this stuff so you don't have to" — reassurance
   and light re-engagement, not a sales pitch dressed as news.

4. INCLUDE TWO SOFT CALLS TO ACTION, low-pressure, near the end of the body:
   - A re-engagement offer: if anything changed this cycle (or even if
     nothing did — just "things move fast"), they can request a quick
     refresh/patch of their site for a fee, since Invert already built the
     foundation and small periodic tune-ups keep it current.
   - A referral ask: if they know a friend, family member, or fellow business
     owner whose site or listings could use the same treatment, send them to
     CORXIT — phrased like a favor between people who know each other, not
     corporate "refer a friend" copy.
   If hasMeaningfulNews is false, still include both CTAs — the quiet-month
   note plus "nothing to report, but here's how to stay sharp anyway" pairs
   naturally with them.

OUTPUT FORMAT: after your reasoning and tool use, end your reply with exactly
one fenced code block, \`\`\`json ... \`\`\`, containing a single JSON object
with this exact shape and nothing else outside the fence:

{
  "cycleLabel": string,  // e.g. "August 2026"
  "hasMeaningfulNews": boolean,
  "headline": string,  // short, plain-language, e.g. "A quiet month" or "ChatGPT started citing..."
  "items": [
    { "title": string, "whatChanged": string, "whyItMatters": string, "source": string, "sourceUrl": string }
    // 0-4 items, strongest first. Empty array if hasMeaningfulNews is false.
  ],
  "quietMonthNote": string,  // only meaningful if hasMeaningfulNews is false; empty string otherwise
  "subjectLineOptions": [string, string, string],
  "bodyText": string,  // full ready-to-paste plain-text newsletter body: greeting, items (or quiet-month note), both CTAs, sign-off. Ready to drop into Zoho as-is.
  "sourcesChecked": [string]  // plain list of what you searched/considered, for the human reviewing before this goes out
}`;

async function runToCompletion(messages) {
  const tools = [
    { type: 'web_search_20260209', name: 'web_search', max_uses: 10 },
  ];

  let current = messages;
  for (let i = 0; i < 6; i++) {
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

    const textBlock = message.content.find((b) => b.type === 'text');
    return textBlock ? textBlock.text : '';
  }
  throw new Error('Pulse generation did not finish after several tool-use rounds.');
}

function extractPulseJson(text) {
  const match = text.match(/```json\s*([\s\S]*?)```/);
  if (!match) return null;
  try {
    return JSON.parse(match[1]);
  } catch {
    return null;
  }
}

module.exports = async (req, res) => {
  if (req.method !== 'GET' && req.method !== 'POST') {
    res.status(405).json({ error: 'This endpoint only accepts GET or POST.' });
    return;
  }

  const now = new Date();
  const cycleLabel = now.toLocaleString('en-US', { month: 'long', year: 'numeric' });

  const userText = [
    `Current date: ${now.toDateString()}`,
    `This cycle's label: ${cycleLabel}`,
    `Search for real, dated news from roughly the last 5-6 weeks per your instructions, apply the filter bar strictly, and produce this cycle's Pulse.`,
  ].join('\n');

  const messages = [
    { role: 'user', content: [{ type: 'text', text: userText }] },
  ];

  try {
    const finalText = await runToCompletion(messages);
    const pulse = extractPulseJson(finalText);
    if (!pulse) {
      res.status(502).json({ error: 'The model did not return a parseable pulse.', raw: finalText });
      return;
    }
    res.status(200).json({ pulse });
  } catch (e) {
    res.status(500).json({ error: `Internal error while generating the pulse: ${e.message}` });
  }
};
