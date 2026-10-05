const KEY = 'carecompanion.v1';
const empty = () => ({ symptoms: [], meds: [], appts: [], tasks: [], taken: {} });
let db;
try { db = Object.assign(empty(), JSON.parse(localStorage.getItem(KEY))); } catch { db = empty(); }
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(db)); } catch {} render(); };
let lang = (navigator.language || '').startsWith('mk') ? 'mk' : 'en';
try { lang = localStorage.getItem('carecompanion.lang') || lang; } catch {}
const t = k => (I18N[lang] && I18N[lang][k]) || I18N.en[k] || k;
function translate() {
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(e => { e.textContent = t(e.dataset.i18n); });
  document.querySelectorAll('[data-i18n-ph]').forEach(e => { e.placeholder = t(e.dataset.i18nPh); });
  document.title = 'CareCompanion';
}
const $ = s => document.querySelector(s);
const today = () => new Date().toISOString().slice(0, 10);
const uid = () => Math.random().toString(36).slice(2, 10);

function li(html, onDelete, cls = '') {
  const el = document.createElement('li');
  el.className = cls;
  el.innerHTML = html;
  if (onDelete) {
    const b = document.createElement('button');
    b.className = 'x'; b.textContent = '✕'; b.title = t('del'); b.onclick = onDelete;
    el.append(b);
  }
  return el;
}
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const remove = (list, id) => { db[list] = db[list].filter(x => x.id !== id); save(); };

function render() {
  const fill = (sel, items, make) => { const ul = $(sel); ul.replaceChildren(...items.map(make)); };
  fill('#symptom-list', [...db.symptoms].sort((a, b) => b.date.localeCompare(a.date)), s =>
    li(`<span><strong>${esc(s.symptom)}</strong> ${s.severity}/10 <small>${esc(s.date)} ${esc(s.notes)}</small></span>`, () => remove('symptoms', s.id)));
  fill('#med-list', db.meds, m => {
    const times = m.times.split(',').map(t => t.trim()).filter(Boolean);
    const checks = times.map(t => {
      const k = `${today()}|${m.id}|${t}`;
      return `<label><input type="checkbox" data-k="${esc(k)}" ${db.taken[k] ? 'checked' : ''}> ${esc(t)}</label>`;
    }).join(' ');
    return li(`<span><strong>${esc(m.name)}</strong> ${esc(m.dose)}<small>${checks}</small></span>`, () => remove('meds', m.id));
  });
  fill('#appt-list', [...db.appts].sort((a, b) => a.when.localeCompare(b.when)), a =>
    li(`<span><strong>${esc(a.who)}</strong> <small>${esc(a.when.replace('T', ' '))}</small>${
      a.questions ? '<small>' + esc(t('ask')) + a.questions.split(';').map(q => esc(q.trim())).filter(Boolean).join(' • ') + '</small>' : ''}</span>`,
      () => remove('appts', a.id)));
  fill('#task-list', db.tasks, t => {
    const el = li(`<span><label><input type="checkbox" ${t.done ? 'checked' : ''}> ${esc(t.task)}</label><small>${esc(t.date)}</small></span>`,
      () => remove('tasks', t.id), t.done ? 'done' : '');
    el.querySelector('input').onchange = e => { t.done = e.target.checked; save(); };
    return el;
  });
}

function bindForm(sel, list, build) {
  const f = $(sel);
  f.onsubmit = e => {
    e.preventDefault();
    db[list].push({ id: uid(), ...build(Object.fromEntries(new FormData(f))) });
    f.reset(); if (f.date) f.date.value = today();
    save();
  };
}
bindForm('#symptom-form', 'symptoms', d => ({ ...d, severity: +d.severity }));
bindForm('#med-form', 'meds', d => d);
bindForm('#appt-form', 'appts', d => d);
bindForm('#task-form', 'tasks', d => ({ ...d, done: false }));
$('#symptom-form').date.value = today();

$('#med-list').addEventListener('change', e => {
  const k = e.target.dataset.k;
  if (k) { db.taken[k] = e.target.checked; save(); }
});

$('#tabs').onclick = e => {
  const t = e.target.dataset.tab; if (!t) return;
  document.querySelectorAll('nav button, .panel').forEach(x => x.classList.remove('active'));
  e.target.classList.add('active'); $('#' + t).classList.add('active');
};

$('#export').onclick = () => {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(db, null, 2)], { type: 'application/json' }));
  a.download = `carecompanion-${today()}.json`; a.click();
};
$('#import').onchange = async e => {
  try { db = Object.assign(empty(), JSON.parse(await e.target.files[0].text())); save(); }
  catch { alert(t('bad_file')); }
};
$('#print').onclick = () => {
  document.querySelectorAll('.panel').forEach(p => p.classList.add('active'));
  window.print();
  document.querySelectorAll('.panel').forEach(p => p.classList.toggle('active', p.id === 'data'));
};
$('#wipe').onclick = () => { if (confirm(t('confirm_wipe'))) { db = empty(); save(); } };

$('#lang').value = lang;
$('#lang').onchange = e => {
  lang = e.target.value;
  try { localStorage.setItem('carecompanion.lang', lang); } catch {}
  translate(); render();
};
translate();
render();
