// Minimal Gmail REST reader. Needs GMAIL_ACCESS_TOKEN (scope gmail.readonly). Never modifies mail.
const API = 'https://gmail.googleapis.com/gmail/v1/users/me';
const h = () => ({ authorization: `Bearer ${process.env.GMAIL_ACCESS_TOKEN}` });

export async function fetchUnread(max = 15) {
  if (!process.env.GMAIL_ACCESS_TOKEN) throw new Error('GMAIL_ACCESS_TOKEN is not set');
  const list = await (await fetch(`${API}/messages?q=is:unread&maxResults=${max}`, { headers: h() })).json();
  if (list.error) throw new Error(list.error.message);
  return Promise.all((list.messages ?? []).map(async ({ id }) => {
    const m = await (await fetch(`${API}/messages/${id}?format=metadata&metadataHeaders=From&metadataHeaders=Subject`, { headers: h() })).json();
    const hd = n => m.payload?.headers?.find(x => x.name === n)?.value ?? '';
    return { id, from: hd('From'), subject: hd('Subject'), body: m.snippet ?? '' };
  }));
}
