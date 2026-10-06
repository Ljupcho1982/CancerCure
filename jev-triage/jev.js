// Jev: fast "System 1" classifier. Small model, strict JSON, confidence threshold.
import { readFile, writeFile } from 'node:fs/promises';

export const CATEGORIES = ['urgent', 'reply_today', 'routine', 'info', 'spam'];
export const ACTIONS = ['reply', 'delegate', 'archive', 'snooze', 'delete'];
export const THRESHOLD = Number(process.env.JEV_THRESHOLD ?? 80);
const MODEL = process.env.JEV_MODEL ?? 'claude-haiku-4-5-20251001';
const FEEDBACK_FILE = new URL('./feedback.json', import.meta.url);

const SYSTEM = `You are Jev, a fast email triage model. Decide from sender, subject and the first lines only.
Return ONLY JSON: {"category":"urgent|reply_today|routine|info|spam","action":"reply|delegate|archive|snooze|delete","confidence":0-100,"reason":"one short sentence"}.
Be honest about confidence: ambiguous, emotional, legal, financial or medical mails get LOW confidence.`;

export async function loadFeedback() {
  try { return JSON.parse(await readFile(FEEDBACK_FILE, 'utf8')); } catch { return []; }
}
export async function saveFeedback(item) {
  const all = await loadFeedback();
  all.push({ ...item, at: new Date().toISOString() });
  await writeFile(FEEDBACK_FILE, JSON.stringify(all.slice(-200), null, 2));
}

export function normalize(raw) {
  const category = CATEGORIES.includes(raw?.category) ? raw.category : 'routine';
  const action = ACTIONS.includes(raw?.action) ? raw.action : 'snooze';
  let confidence = Math.round(Number(raw?.confidence));
  if (!Number.isFinite(confidence)) confidence = 0;
  confidence = Math.max(0, Math.min(100, confidence));
  // Safety: never auto-delete; destructive actions always need a human.
  const needsHuman = confidence < THRESHOLD || action === 'delete';
  return { category, action, confidence, reason: String(raw?.reason ?? '').slice(0, 200), needsHuman };
}

async function callModel(email, examples) {
  const shots = examples.slice(-8).map(e =>
    `Subject: ${e.subject}\nFrom: ${e.from}\n=> ${JSON.stringify(e.correct)}`).join('\n\n');
  const user = `${shots ? `Past corrections by the user:\n${shots}\n\n` : ''}From: ${email.from}\nSubject: ${email.subject}\nBody: ${String(email.body ?? '').slice(0, 300)}`;
  const res = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'x-api-key': process.env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'content-type': 'application/json',
    },
    body: JSON.stringify({ model: MODEL, max_tokens: 150, system: SYSTEM, messages: [{ role: 'user', content: user }] }),
  });
  if (!res.ok) throw new Error(`Anthropic API ${res.status}`);
  const data = await res.json();
  const text = data.content?.[0]?.text ?? '';
  return JSON.parse(text.slice(text.indexOf('{'), text.lastIndexOf('}') + 1));
}

export async function triage(email) {
  if (!process.env.ANTHROPIC_API_KEY) throw new Error('ANTHROPIC_API_KEY is not set');
  const started = Date.now();
  const raw = await callModel(email, await loadFeedback());
  return { id: email.id, ...normalize(raw), engine: MODEL, ms: Date.now() - started };
}
