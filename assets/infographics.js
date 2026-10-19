/* infographics/plan.html: the review of the infographics plan, and its filters.
 *
 * Everything stays in this browser (localStorage, key genz.infographics.v1): the reviewer's name and a verdict per
 * proposal (accept, change, decline, later) with a note. Nothing is sent anywhere. The export, markdown or JSON, is how
 * a review reaches the vault's reviews/ folder or the agent, which records each verdict in plan.json with decided_by.
 */
(function () {
  'use strict';
  const bar = document.getElementById('ig-bar');
  if (!bar) return;
  const KEY = bar.dataset.store || 'genz.infographics.v1';
  const VERDICTS = [['accept', 'Accept'], ['change', 'Change'], ['decline', 'Decline'], ['later', 'Later']];
  const cards = Array.from(document.querySelectorAll('.ig-card'));
  const fresh = () => ({ reviewer: '', verdicts: {} });
  let S = fresh(), kept = true;
  try { const raw = localStorage.getItem(KEY); if (raw) S = Object.assign(fresh(), JSON.parse(raw)); } catch (e) { kept = false; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { kept = false; } tally(); };
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

  // ---- the controls on each card
  for (const card of cards) {
    const id = card.dataset.id, box = card.querySelector('.ig-review');
    box.innerHTML = '<div class="vb">' + VERDICTS.map(([v, l]) => `<button type="button" class="${v}" data-v="${v}">${l}</button>`).join('') +
      '</div><textarea placeholder="A line for the agent: what to change, why not, or anything else (optional)"></textarea>';
    const ta = box.querySelector('textarea');
    const paint = () => {
      const r = S.verdicts[id];
      box.querySelectorAll('button').forEach(b => b.classList.toggle('on', !!r && r.v === b.dataset.v));
      VERDICTS.forEach(([v]) => card.classList.toggle('v-' + v, !!r && r.v === v));
      ta.value = (r && r.note) || '';
    };
    box.querySelectorAll('button').forEach(b => b.onclick = () => {
      const r = S.verdicts[id];
      if (r && r.v === b.dataset.v) { if (r.note) r.v = ''; else delete S.verdicts[id]; }
      else S.verdicts[id] = { v: b.dataset.v, note: (r && r.note) || ta.value || '', at: new Date().toISOString() };
      save(); paint(); apply();
    });
    ta.oninput = () => {
      const r = S.verdicts[id] || (S.verdicts[id] = { v: '', note: '' });
      r.note = ta.value; r.at = new Date().toISOString();
      if (!r.v && !r.note) delete S.verdicts[id];
      save();
    };
    paint();
  }

  // ---- the bar: who, the tally, export and import
  bar.innerHTML = '<span class="tally" id="ig-tally"></span>' +
    '<label class="small">Reviewer <input type="text" id="ig-who" placeholder="your name"></label>' +
    '<span class="acts"><button type="button" class="btn" id="ig-md">Export markdown</button><button type="button" class="btn" id="ig-json">Export JSON</button>' +
    '<label class="btn" style="cursor:pointer">Import<input type="file" id="ig-in" accept="application/json" hidden></label>' +
    '<button type="button" class="btn" id="ig-reset">Clear</button></span>';
  const who = document.getElementById('ig-who');
  who.value = S.reviewer || '';
  who.oninput = () => { S.reviewer = who.value; save(); };
  function tally() {
    const c = { accept: 0, change: 0, decline: 0, later: 0 };
    for (const r of Object.values(S.verdicts)) if (c[r.v] !== undefined) c[r.v]++;
    const done = Object.values(c).reduce((a, b) => a + b, 0);
    document.getElementById('ig-tally').innerHTML = `<span><b>${done}</b> of ${cards.length} reviewed</span>` +
      VERDICTS.map(([v, l]) => `<span>${l.toLowerCase()} <b>${c[v]}</b></span>`).join('') +
      (kept ? '' : '<span class="warn" title="localStorage is not available here">not kept in this browser: export before you leave</span>');
  }
  const titleOf = id => { const c = document.getElementById(id); return c ? c.querySelector('h3').textContent : id; };
  const targetOf = id => { const c = document.getElementById(id), a = c && (c.querySelector('.ig-target a') || c.querySelector('.ig-target code')); return a ? a.textContent.trim() : ''; };
  function markdown() {
    const now = new Date().toISOString().slice(0, 10);
    let out = `# Infographics review, ${now}\n\nReviewer: ${S.reviewer || '(not named)'} · site ${bar.dataset.site} · candidate ${bar.dataset.candidate} · ` +
      `${Object.keys(S.verdicts).length} of ${cards.length} proposals\n\nExported from https://gen-z-developers.sgit.ai/infographics/plan.html. ` +
      `For the agent: record each verdict in admin/content/infographics/plan.json (accept: accepted; change: changes; decline: declined; later: deferred), with decided_by naming the reviewer and this file.\n`;
    for (const [v, l] of VERDICTS.concat([['', 'Notes without a verdict']])) {
      const rows = cards.filter(c => (S.verdicts[c.dataset.id] || {}).v === v && S.verdicts[c.dataset.id]);
      if (!rows.length) continue;
      out += `\n## ${l} (${rows.length})\n\n`;
      for (const c of rows) {
        const r = S.verdicts[c.dataset.id];
        out += `- **${titleOf(c.dataset.id)}** (\`${c.dataset.id}\`, ${targetOf(c.dataset.id)})${r.note ? ': ' + r.note.replace(/\s+/g, ' ').trim() : ''}\n`;
      }
    }
    return out;
  }
  function download(name, text, type) {
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name;
    document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  const stamp = () => new Date().toISOString().slice(0, 10);
  document.getElementById('ig-md').onclick = () => download(`infographics-review-${stamp()}.md`, markdown(), 'text/markdown');
  document.getElementById('ig-json').onclick = () => download(`infographics-review-${stamp()}.json`,
    JSON.stringify(Object.assign({ exported: new Date().toISOString(), site: bar.dataset.site, candidate: bar.dataset.candidate }, S), null, 1), 'application/json');
  document.getElementById('ig-in').onchange = e => {
    const f = e.target.files[0]; if (!f) return;
    f.text().then(t => {
      const d = JSON.parse(t);
      if (!d || typeof d.verdicts !== 'object') throw new Error('not an infographics review');
      S.verdicts = Object.assign(S.verdicts, d.verdicts); if (d.reviewer && !S.reviewer) S.reviewer = d.reviewer;
      save(); location.reload();
    }).catch(err => alert('Could not import: ' + err.message));
  };
  document.getElementById('ig-reset').onclick = () => { if (confirm('Clear every verdict and note in this browser? Export first if you want to keep them.')) { S = fresh(); save(); location.reload(); } };

  // ---- the filters
  const sels = Array.from(document.querySelectorAll('[data-filter]'));
  let only = null; // a chapter or part picked on the coverage grid
  const shown = document.getElementById('ig-shown');
  function apply() {
    const f = {}; sels.forEach(s => { if (s.value) f[s.dataset.filter] = s.value; });
    let n = 0;
    for (const c of cards) {
      const r = S.verdicts[c.dataset.id];
      let ok = true;
      for (const [k, v] of Object.entries(f)) {
        if (k === 'verdict') ok = ok && (v === 'none' ? !(r && r.v) : !!r && r.v === v);
        else ok = ok && c.dataset[k] === v;
      }
      if (only) ok = ok && (only.kind === 'target' ? c.dataset.target === only.v : c.dataset.part === only.v);
      c.hidden = !ok; if (ok) n++;
    }
    shown.textContent = n === cards.length ? `all ${n} shown` : `${n} of ${cards.length} shown`;
    document.querySelectorAll('[data-filter-target],[data-filter-part]').forEach(b =>
      b.classList.toggle('on', !!only && (b.dataset.filterTarget || b.dataset.filterPart) === only.v));
  }
  sels.forEach(s => s.onchange = apply);
  document.querySelectorAll('[data-filter-target]').forEach(b => b.onclick = () => { only = only && only.v === b.dataset.filterTarget ? null : { kind: 'target', v: b.dataset.filterTarget }; apply(); document.getElementById('proposals').scrollIntoView({ behavior: 'smooth' }); });
  document.querySelectorAll('[data-filter-part]').forEach(b => b.onclick = () => { only = only && only.v === b.dataset.filterPart ? null : { kind: 'part', v: b.dataset.filterPart }; apply(); document.getElementById('proposals').scrollIntoView({ behavior: 'smooth' }); });
  document.getElementById('ig-clear').onclick = () => { sels.forEach(s => s.value = ''); only = null; apply(); };
  tally(); apply();
})();
