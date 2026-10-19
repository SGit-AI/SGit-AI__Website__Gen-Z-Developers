/* graph/view.html: the book as a graph, drawn from graph/graph.json. Columns by kind (2018 files, sources, ideas,
 * chapters); click a node to light its neighbours and read it in the side panel; filters by idea state and
 * destination. No library, nothing stored, nothing sent. */
(function () {
  'use strict';
  const root = document.getElementById('gv'); if (!root) return;
  const NS = 'http://www.w3.org/2000/svg';
  const svgEl = (t, a) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); return e; };
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const up = root.dataset.up || '';
  const COLS = [
    { key: 'book', label: 'The 2018 book', test: (n) => n.kind === 'source' && n.source_kind === 'book-2018' && n.book_kind !== 'apparatus' },
    { key: 'src', label: 'Sources: articles, decisions', test: (n) => n.kind === 'source' && n.source_kind !== 'book-2018' && n.source_kind !== 'storyboard' && (n.source_kind !== 'newsroom' || n.state === 'processed' || n.state === 'mined') },
    { key: 'idea', label: 'Ideas', test: (n) => n.kind === 'idea' },
    { key: 'chapter', label: 'Chapters, proposed', test: (n) => n.kind === 'chapter' || n.kind === 'part' },
  ];
  const COLOUR = { 'book-2018': '#e8b64a', newsroom: '#3b9fb0', article: 'var(--solid)', 'agent-article': '#475569', decision: '#b45309', survey: '#94a3b8', memo: '#94a3b8', idea: '#0f766e', chapter: '#7c3aed', part: '#4c1d95' };
  const STATE = { candidate: '#fb923c', accepted: '#0f766e', drafting: '#2563eb', 'signed-off': '#15803d', declined: '#b91c1c', deferred: '#6b21a8' };
  let G, filter = { state: 'all', dest: 'all' }, focus = null;
  const side = document.getElementById('gv-side'), canvas = document.getElementById('gv-canvas'), filters = document.getElementById('gv-filters');

  function render() {
    canvas.innerHTML = '';
    const nodes = Object.values(G.nodes);
    const ideas = nodes.filter((n) => n.kind === 'idea' && (filter.state === 'all' || n.state === filter.state) && (filter.dest === 'all' || n.destination === filter.dest));
    const ideaIds = new Set(ideas.map((n) => n.id));
    const linked = new Set();
    for (const e of G.edges) { if (ideaIds.has(e.from)) linked.add(e.to); if (ideaIds.has(e.to)) linked.add(e.from); }
    const cols = COLS.map((c) => ({ ...c, items: nodes.filter((n) => c.test(n) && (c.key === 'idea' ? ideaIds.has(n.id) : linked.has(n.id) || (c.key === 'chapter' && n.kind === 'part'))) }));
    for (const c of cols) if (c.key === 'chapter') c.items = c.items.filter((n) => n.kind === 'chapter' ? linked.has(n.id) : true);
    const rowH = 16, top = 40, W = 1180, colW = W / cols.length;
    const H = top + Math.max(...cols.map((c) => c.items.length)) * rowH + 30;
    const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-label': 'The book as a graph: the 2018 files, the sources, the ideas and the proposed chapters, with the edges between them' });
    const pos = {};
    cols.forEach((c, ci) => {
      const x = ci * colW + 20;
      const t = svgEl('text', { x, y: 20, class: 'gv-col' }); t.textContent = `${c.label} (${c.items.length})`; svg.appendChild(t);
      c.items.sort((a, b) => (a.kind === 'part' ? -1 : 0) || String(a.title).localeCompare(String(b.title)));
      // keep chapters under their part
      if (c.key === 'chapter') { const parts = c.items.filter((n) => n.kind === 'part'); const chs = c.items.filter((n) => n.kind === 'chapter'); c.items = []; for (const p of parts) { c.items.push(p); for (const ch of chs) if (ch.part === p.id.slice(5)) c.items.push(ch); } }
      c.items.forEach((n, i) => { pos[n.id] = { x: x + 6, y: top + i * rowH + 8 }; });
    });
    const edgeEls = [];
    for (const e of G.edges) {
      if (!pos[e.from] || !pos[e.to]) continue;
      const a = pos[e.from], b = pos[e.to];
      const left = a.x < b.x ? a : b, right = a.x < b.x ? b : a;
      const path = svgEl('path', { d: `M${left.x + 4},${left.y} C${left.x + colW * 0.45},${left.y} ${right.x - colW * 0.45},${right.y} ${right.x - 4},${right.y}`, class: 'gv-edge' });
      path.dataset.from = e.from; path.dataset.to = e.to;
      svg.appendChild(path); edgeEls.push(path);
    }
    const nodeEls = {};
    cols.forEach((c, ci) => c.items.forEach((n) => {
      const p = pos[n.id];
      const g = svgEl('g', { class: 'gv-node' + (n.id === focus ? ' focus' : '') });
      const fill = n.kind === 'idea' ? STATE[n.state] || '#0f766e' : COLOUR[n.source_kind || n.kind] || '#999';
      g.appendChild(svgEl('circle', { cx: p.x, cy: p.y, r: n.kind === 'part' ? 5 : 4, style: `fill:${fill}` })); // style, not fill=: a theme token needs var()
      const t = svgEl('text', { x: p.x + 9, y: p.y + 3.5 }); t.textContent = (n.kind === 'part' ? '▸ ' : '') + String(n.title).slice(0, ci === 2 ? 44 : 38); g.appendChild(t);
      const title = svgEl('title'); title.textContent = n.full_title || n.title; g.appendChild(title);
      g.onclick = () => { focus = focus === n.id ? null : n.id; light(); show(n); };
      svg.appendChild(g); nodeEls[n.id] = g;
    }));
    canvas.appendChild(svg);
    function light() {
      const nb = new Set();
      if (focus) for (const e of G.edges) { if (e.from === focus) nb.add(e.to); if (e.to === focus) nb.add(e.from); }
      for (const id in nodeEls) nodeEls[id].classList.toggle('dim', !!focus && id !== focus && !nb.has(id)), nodeEls[id].classList.toggle('focus', id === focus);
      for (const p of edgeEls) { const on = focus && (p.dataset.from === focus || p.dataset.to === focus); p.classList.toggle('lit', !!on); p.classList.toggle('dim', !!focus && !on); }
    }
    light();
  }
  function show(n) {
    const nb = [];
    for (const e of G.edges) { if (e.from === n.id && G.nodes[e.to]) nb.push({ n: G.nodes[e.to], kind: e.kind, label: e.label, dir: 'to' }); if (e.to === n.id && G.nodes[e.from]) nb.push({ n: G.nodes[e.from], kind: e.kind, label: e.label, dir: 'from' }); }
    const link = (x) => x.url ? `<a href="${esc(x.url.startsWith('http') ? x.url : up + x.url)}">${esc(x.title)}</a>` : esc(x.title);
    side.innerHTML = `<h3>${link(n)}</h3><p class="dim small">${esc(n.kind)}${n.source_kind ? ' · ' + esc(n.source_kind) : ''}${n.state ? ' · <span class="st ' + esc(n.state) + '">' + esc(n.state) + '</span>' : ''}${n.destination ? ' · ' + esc(n.destination) : ''}</p>` +
      (n.statement ? `<p>${esc(n.statement)}</p>` : n.punchline ? `<p>${esc(n.punchline)}</p>` : n.why ? `<p class="small">${esc(n.why)}</p>` : n.said ? `<p class="small">“${esc(n.said)}”</p>` : '') +
      (n.decided_by ? `<p class="small dim">Decided by: ${esc(n.decided_by)}</p>` : '') +
      `<h3>${nb.length} connection${nb.length === 1 ? '' : 's'}</h3><ul>` + nb.slice(0, 40).map((x) => `<li>${link(x.n)} <span class="dim small">${esc(x.kind.replace(/-/g, ' '))}${x.label ? ': ' + esc(x.label) : ''}</span></li>`).join('') + (nb.length > 40 ? `<li class="dim">and ${nb.length - 40} more</li>` : '') + '</ul>';
  }
  function renderFilters() {
    const states = ['all', 'candidate', 'accepted', 'drafting', 'signed-off', 'declined', 'deferred'];
    const dests = ['all', 'this-edition', 'next-version', 'another-book', 'the-process', 'undecided'];
    filters.innerHTML = '<span class="dim">Ideas by state</span> ' + states.map((s) => `<button type="button" class="chip" data-k="state" data-v="${s}" aria-pressed="${filter.state === s}">${s}</button>`).join('') +
      ' <span class="dim">destination</span> ' + dests.map((s) => `<button type="button" class="chip" data-k="dest" data-v="${s}" aria-pressed="${filter.dest === s}">${s}</button>`).join('');
    filters.querySelectorAll('.chip').forEach((b) => b.onclick = () => { filter[b.dataset.k] = b.dataset.v; renderFilters(); render(); });
  }
  fetch(root.dataset.graph, { cache: 'no-store' }).then((r) => r.json()).then((g) => {
    G = g; renderFilters(); render();
    const h = location.hash.slice(1); if (h && G.nodes[h]) { focus = h; render(); show(G.nodes[h]); }
    else side.innerHTML = `<h3>${G.counts.nodes} nodes, ${G.counts.edges} edges</h3><p class="small dim">Click a node. Ideas are coloured by state (orange candidate, teal accepted, blue drafting, green signed off, red declined, purple deferred); sources by kind (yellow the 2018 book, teal a newsroom article, navy a co-written article, brown a decision); chapters purple. Only the sources and chapters an idea links to are drawn; the full lists are on the other pages.</p>`;
  }).catch((e) => { canvas.innerHTML = `<p class="note warn">The graph could not be loaded (${esc(e.message || e)}).</p>`; });
})();
