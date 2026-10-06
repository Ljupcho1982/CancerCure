import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { triage, saveFeedback, normalize, THRESHOLD } from './jev.js';
import { fetchUnread } from './gmail.js';

const PORT = process.env.PORT ?? 3000;
const json = (res, code, obj) => { res.writeHead(code, { 'content-type': 'application/json' }); res.end(JSON.stringify(obj)); };
const body = req => new Promise((ok, no) => { let s = ''; req.on('data', c => { s += c; if (s.length > 1e6) req.destroy(); }); req.on('end', () => { try { ok(JSON.parse(s || '{}')); } catch (e) { no(e); } }); });

createServer(async (req, res) => {
  try {
    if (req.method === 'GET' && req.url === '/') {
      res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' });
      return res.end(await readFile(new URL('./public/index.html', import.meta.url)));
    }
    if (req.method === 'GET' && req.url === '/api/config')
      return json(res, 200, { threshold: THRESHOLD, ai: !!process.env.ANTHROPIC_API_KEY, gmail: !!process.env.GMAIL_ACCESS_TOKEN });
    if (req.method === 'GET' && req.url === '/api/gmail') return json(res, 200, await fetchUnread());
    if (req.method === 'POST' && req.url === '/api/triage') {
      const { emails = [] } = await body(req);
      return json(res, 200, await Promise.all(emails.slice(0, 50).map(triage)));
    }
    if (req.method === 'POST' && req.url === '/api/feedback') {
      const { from, subject, correct } = await body(req);
      const c = normalize({ ...correct, confidence: 100 });
      await saveFeedback({ from, subject, correct: { category: c.category, action: c.action, confidence: 100, reason: 'user-corrected' } });
      return json(res, 200, { ok: true });
    }
    json(res, 404, { error: 'not found' });
  } catch (e) { json(res, 500, { error: e.message }); }
}).listen(PORT, () => console.log(`Jev triage on http://localhost:${PORT}`));
