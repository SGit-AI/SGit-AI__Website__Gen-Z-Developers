/* read/: the reader and the editor's desk for Generation Z Developers.
 *
 * Everything the reader does stays in this browser (localStorage, key genz.reader.v1): the reading meter's balance
 * and charges, the state of each chapter (unread, reading, read, to review, continue, signed off), the comments on
 * paragraphs, which chapters are folded. Nothing is sent anywhere; the export writes a file the reader can put in the
 * vault's reviews/ folder. The meter's rules are the newsroom's (sg-meter v1.5.0): charge by the share read, never
 * less than a tenth once opened, credit allowed below zero, nothing blocked.
 *
 * The book comes from v1/book/book.json (build.py): chapters as blocks, the newsroom articles that answer each, and
 * the chapters that share terms. No library, no network beyond that one file.
 */
(function () {
  'use strict';
  const rootEl = document.getElementById('reader');
  const KEY = (rootEl && rootEl.dataset.store) || 'genz.reader.v1';
  const STATES = [['unread', 'Unread'], ['reading', 'Reading'], ['read', 'Read'], ['review', 'To review'], ['continue', 'Continue'], ['signed', 'Signed off']];
  const root = document.getElementById('reader');
  if (!root) return;
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const NS = 'http://www.w3.org/2000/svg';
  const svgEl = (tag, attrs) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); return e; };

  // ---------------------------------------------------------------- state
  let book = null, S = null, chapters = [], bySlug = {}, current = null, graphTab = 'chapter', storageOk = true;
  function fresh() { return { v: 1, balance: null, topups: 0, charged: {}, states: {}, comments: [], folds: {}, readBlocks: {}, mode: 'read', filter: 'all', hideOthers: false, opened: {}, pricePerWords: null }; }
  function load() {
    try { const raw = localStorage.getItem(KEY); S = raw ? Object.assign(fresh(), JSON.parse(raw)) : fresh(); }
    catch (e) { S = fresh(); storageOk = false; }
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { storageOk = false; } }

  // ---------------------------------------------------------------- the meter
  const pence = (n) => (book.meter.symbol || '£') + (n / 100).toFixed(2);
  function priceOf(ch) { return Math.max(1, Math.round(ch.words / (S.pricePerWords || book.meter.pence_per_words))); }
  function chargeOf(slug) { const c = S.charged[slug]; return c ? c.pence : 0; }
  function spent() { return Object.values(S.charged).reduce((a, c) => a + c.pence, 0); }
  function balance() { return book.meter.start + S.topups - spent(); }
  function settle(slug) {
    const ch = bySlug[slug]; if (!ch) return;
    const rb = S.readBlocks[slug] || {};
    const readWords = ch.blocks.reduce((a, b) => a + (rb[b.id] ? b.words : 0), 0);
    let share = ch.words ? readWords / ch.words : 0;
    share = Math.round(share * 20) / 20; // steps of 5%, as the newsroom's meter does
    if (!S.opened[slug]) return;
    share = Math.max(share, book.meter.min_share);
    const p = Math.max(1, Math.round(priceOf(ch) * share));
    const before = S.charged[slug];
    if (!before || before.pence !== p || before.share !== share) {
      S.charged[slug] = { share, pence: p, at: new Date().toISOString() };
      if (share >= 0.9 && (S.states[slug] === 'reading' || !S.states[slug])) S.states[slug] = 'read';
      save(); paintStrip(); paintChapterFoot(slug); paintTocItem(slug);
    }
  }
  function paintStrip() {
    const b = balance();
    const m = $('rd-meter');
    m.className = 'rd-meter' + (b < 0 ? ' neg' : '');
    const cur = current ? `this chapter ${pence(chargeOf(current))} of ${pence(priceOf(bySlug[current]))}` : '';
    m.innerHTML = `balance <b>${pence(b)}</b> &middot; spent ${pence(spent())}${cur ? ' &middot; ' + cur : ''}` +
      (storageOk ? '' : ' &middot; <span title="localStorage is not available; the balance will not be kept">not kept</span>') +
      ` <button class="rd-btn" id="rd-topup" type="button" title="Add £5 of credit (simulated; the newsroom's door is a Stripe link)">+£5</button>`;
    m.querySelector('#rd-topup').onclick = () => { S.topups += 500; save(); paintStrip(); };
    const pub = chapters.filter((c) => c.published);
    const read = pub.filter((c) => ['read', 'signed', 'review', 'continue'].includes(S.states[c.slug])).length;
    const signed = pub.filter((c) => S.states[c.slug] === 'signed').length;
    $('rd-progress').innerHTML = `<b>${read}</b> of ${pub.length} read` + (S.mode === 'review' ? ` &middot; <b>${signed}</b> signed off &middot; ${S.comments.length} comment${S.comments.length === 1 ? '' : 's'}` : '');
  }

  // ---------------------------------------------------------------- render
  function stateOf(slug) { return S.states[slug] || 'unread'; }
  function visibleByFilter(ch) {
    const f = S.filter;
    if (f === 'all') return true;
    if (f === 'published') return ch.published;
    if (f === 'drafts') return !ch.published;
    if (f === 'commented') return S.comments.some((c) => c.slug === ch.slug);
    return stateOf(ch.slug) === f;
  }
  function isFolded(ch) {
    if (S.folds[ch.slug] != null) return S.folds[ch.slug];
    return !ch.published; // drafts start folded
  }
  function renderToc() {
    const toc = $('rd-toc'); toc.innerHTML = '';
    const groups = [];
    for (const p of book.parts) {
      const pc = chapters.filter((c) => c.part === p.slug && c.published);
      if (pc.length) groups.push({ title: p.title, items: pc });
    }
    const front = { slug: book.front.slug || 'github-issues', title: book.front.title, number: 0, published: true, front: true };
    groups.unshift({ title: 'Front matter', items: [front] });
    const drafts = chapters.filter((c) => !c.published);
    const dgroups = [];
    for (const p of book.parts) {
      const dc = drafts.filter((c) => c.part === p.slug);
      if (dc.length) dgroups.push({ title: p.title + ' (drafts)', items: dc });
    }
    const addGroup = (g) => {
      toc.appendChild(el('h4', null, esc(g.title)));
      for (const c of g.items) {
        const a = el('a', null, `<span class="n">${c.number != null ? (c.number || '') : (c.kind === 'outline' ? '○' : '◌')}</span><span class="t">${esc(c.title)}</span><span class="st st-${stateOf(c.slug)}"></span>`);
        a.href = '#' + c.slug; a.dataset.slug = c.slug;
        if (!visibleByFilter(c) && !c.front) a.classList.add('folded');
        toc.appendChild(a);
      }
    };
    groups.forEach(addGroup);
    toc.appendChild(el('h4', null, 'The drafts, not in the book'));
    dgroups.forEach(addGroup);
  }
  function paintTocItem(slug) {
    const a = $('rd-toc').querySelector(`a[data-slug="${slug}"]`); if (!a) return;
    const st = a.querySelector('.st'); st.className = 'st st-' + stateOf(slug);
    const ch = bySlug[slug]; if (ch) a.classList.toggle('folded', !visibleByFilter(ch));
  }
  function chapterCard(ch) {
    const card = el('article', 'rd-ch' + (isFolded(ch) ? ' folded' : ''));
    card.id = ch.slug; card.dataset.slug = ch.slug;
    const where = book.candidate ? (ch.front ? 'front matter' : `chapter ${ch.number} of ${chapters.length}`) : ch.front ? `front matter, p. ${ch.print_page}` : ch.published ? `chapter ${ch.number} of the published book &middot; p. ${ch.print_page}` : (ch.kind === 'outline' ? 'an outline, never published' : 'a draft, never published');
    const badge = book.candidate ? `<span class="badge draft">${esc(book.candidate)}</span>` : ch.front || ch.published ? '<span class="badge written">published</span>' : (ch.kind === 'outline' ? '<span class="badge outline">outline</span>' : '<span class="badge draft">draft</span>');
    const head = el('div', 'rd-chhead', `<h2>${esc(ch.title)}</h2><span>${where}</span> ${badge} <span>${ch.words.toLocaleString()} words</span>` +
      (ch.url ? ` <a href="../${ch.url}">its page</a>` : '') +
      `<span class="rd-state" data-slug="${ch.slug}"></span><button type="button" class="fold" aria-expanded="${!isFolded(ch)}">${isFolded(ch) ? 'Open' : 'Fold'}</button>`);
    card.appendChild(head);
    const body = el('div', 'rd-body');
    for (const b of ch.blocks) {
      const blk = el('div', 'blk', b.html);
      blk.dataset.block = b.id; blk.dataset.words = b.words;
      const btn = el('button', 'cbtn', '+'); btn.type = 'button'; btn.title = 'Comment on this paragraph'; btn.setAttribute('aria-label', 'Comment on this paragraph');
      blk.appendChild(btn);
      blk.appendChild(el('div', 'rd-comments'));
      body.appendChild(blk);
    }
    card.appendChild(body);
    const foot = el('div', 'rd-chfoot');
    card.appendChild(foot);
    return card;
  }
  function renderContent() {
    const c = $('rd-content'); c.innerHTML = '';
    const front = Object.assign({}, book.front, { front: true, published: true, kind: 'published', blocks: book.front.blocks, part: null });
    bySlug[front.slug] = front;
    c.appendChild(el('div', 'rd-partnote', 'Front matter'));
    c.appendChild(chapterCard(front));
    for (const p of book.parts) {
      const pc = chapters.filter((x) => x.part === p.slug && x.published);
      if (!pc.length) continue;
      c.appendChild(el('div', 'rd-partnote', esc(p.title) + (p.print_page ? ' &middot; from p. ' + p.print_page : '')));
      if (p.intro_html) { const i = el('div', 'rd-ch rd-intro'); i.innerHTML = `<div class="rd-body">${p.intro_html}</div>`; c.appendChild(i); }
      for (const ch of pc) c.appendChild(chapterCard(ch));
    }
    c.appendChild(el('div', 'rd-partnote', 'The drafts and outlines: in the 2018 repository, never in the published book'));
    for (const p of book.parts) {
      const dc = chapters.filter((x) => x.part === p.slug && !x.published);
      if (!dc.length) continue;
      c.appendChild(el('div', 'rd-partnote', esc(p.title) + ' &middot; drafts'));
      for (const ch of dc) c.appendChild(chapterCard(ch));
    }
    for (const ch of [front].concat(chapters)) { paintStateButtons(ch.slug); paintComments(ch.slug); paintChapterFoot(ch.slug); }
    applyFilter();
  }
  function paintStateButtons(slug) {
    const box = $('rd-content').querySelector(`.rd-state[data-slug="${slug}"]`); if (!box) return;
    if (S.mode !== 'review') { box.innerHTML = ''; return; }
    box.innerHTML = STATES.map(([k, l]) => `<button type="button" data-s="${k}" aria-pressed="${stateOf(slug) === k}">${l}</button>`).join('');
  }
  function paintChapterFoot(slug) {
    const card = document.getElementById(slug); if (!card) return;
    const ch = bySlug[slug]; const foot = card.querySelector('.rd-chfoot'); if (!foot) return;
    const c = S.charged[slug];
    const arts = ch.articles && ch.articles.length ? `<span>Answered since: ${ch.articles.map((a) => `<a href="${esc(a.url)}">${esc(a.title)}</a>`).join(', ')}</span>` : '';
    foot.innerHTML = `<span class="cost">${c ? `read ${Math.round(c.share * 100)}%, charged ${pence(c.pence)}` : `not opened yet, ${pence(priceOf(ch))} to read it all`}</span>` +
      `<span>state: <b>${STATES.find((s) => s[0] === stateOf(slug))[1]}</b></span>${arts}`;
  }
  function paintComments(slug) {
    const card = document.getElementById(slug); if (!card) return;
    for (const blk of card.querySelectorAll('.blk')) {
      const id = blk.dataset.block;
      const mine = S.comments.filter((c) => c.block === id);
      blk.classList.toggle('has', mine.length > 0);
      blk.classList.toggle('readblk', !!(S.readBlocks[slug] || {})[id] && S.mode === 'review');
      const box = blk.querySelector('.rd-comments');
      const open = box.dataset.open === '1';
      box.innerHTML = mine.map((c) => `<div class="c" data-id="${c.id}">${esc(c.text)}<span class="when">${c.at.slice(0, 16).replace('T', ' ')}</span><button type="button" class="del" title="Delete this comment" aria-label="Delete this comment">&times;</button></div>`).join('') +
        (open ? `<form><textarea placeholder="A comment on this paragraph: a finding, a question, a change to make" aria-label="Comment"></textarea><button type="submit">Keep</button></form>` : '');
      box.hidden = !(mine.length || open);
      blk.querySelector('.cbtn').textContent = mine.length ? String(mine.length) : '+';
    }
  }
  function applyFilter() {
    for (const card of $('rd-content').querySelectorAll('.rd-ch[data-slug]')) {
      const ch = bySlug[card.dataset.slug];
      const show = ch.front || visibleByFilter(ch);
      card.hidden = S.mode === 'review' && S.hideOthers && !show;
      const folded = S.mode === 'review' && !show ? true : isFolded(ch);
      card.classList.toggle('folded', folded);
      const b = card.querySelector('.fold'); if (b) { b.textContent = folded ? 'Open' : 'Fold'; b.setAttribute('aria-expanded', String(!folded)); }
    }
    for (const a of $('rd-toc').querySelectorAll('a[data-slug]')) { const ch = bySlug[a.dataset.slug]; if (ch && !ch.front) a.classList.toggle('folded', !visibleByFilter(ch)); }
    for (const note of $('rd-content').querySelectorAll('.rd-partnote')) {
      let n = note.nextElementSibling, any = false;
      while (n && !n.classList.contains('rd-partnote')) { if (!n.hidden) any = true; n = n.nextElementSibling; }
      note.hidden = !any;
    }
  }
  function renderFilters() {
    const f = $('rd-filters');
    f.hidden = S.mode !== 'review';
    if (f.hidden) return;
    const chips = [['all', 'All'], ['published', 'Published'], ['drafts', 'Drafts'], ['unread', 'Unread'], ['reading', 'Reading'], ['read', 'Read'], ['review', 'To review'], ['continue', 'Continue'], ['signed', 'Signed off'], ['commented', 'Commented']];
    f.innerHTML = '<span class="dim">Show</span> ' + chips.map(([k, l]) => `<button type="button" class="chip" data-f="${k}" aria-pressed="${S.filter === k}">${l}</button>`).join('') +
      `<span class="sep">|</span><button type="button" class="chip" id="rd-hide" aria-pressed="${S.hideOthers}">Hide the rest</button>` +
      `<button type="button" class="chip" id="rd-foldall">Fold all</button><button type="button" class="chip" id="rd-openall">Open all</button>` +
      `<span class="sep">|</span><button type="button" class="chip" id="rd-exportbtn">Export / import the review</button>`;
    f.querySelectorAll('[data-f]').forEach((b) => b.onclick = () => { S.filter = b.dataset.f; save(); renderFilters(); applyFilter(); });
    $('rd-hide').onclick = () => { S.hideOthers = !S.hideOthers; save(); renderFilters(); applyFilter(); };
    $('rd-foldall').onclick = () => { for (const c of chapters) S.folds[c.slug] = true; save(); applyFilter(); };
    $('rd-openall').onclick = () => { for (const c of chapters) S.folds[c.slug] = false; save(); applyFilter(); };
    $('rd-exportbtn').onclick = () => { const x = $('rd-export'); x.hidden = !x.hidden; if (!x.hidden) renderExport(); x.scrollIntoView({ block: 'nearest' }); };
  }

  // ---------------------------------------------------------------- the graph
  const chapterOf = (slug) => chapters.find((c) => c.slug === slug);
  function renderGraph() {
    const g = $('rd-graph'); g.innerHTML = '';
    const tabs = el('div', 'gtabs', `<button type="button" data-t="chapter" aria-pressed="${graphTab === 'chapter'}">This chapter</button><button type="button" data-t="book" aria-pressed="${graphTab === 'book'}">The book</button>`);
    tabs.querySelectorAll('button').forEach((b) => b.onclick = () => { graphTab = b.dataset.t; renderGraph(); });
    g.appendChild(tabs);
    if (graphTab === 'book') return bookGraph(g);
    const ch = current ? bySlug[current] : null;
    if (!ch) { g.appendChild(el('p', 'dim small', 'Open a chapter to see its graph.')); return; }
    g.appendChild(el('h3', null, esc(ch.title)));
    const W = 360, H = 400, cx = W / 2, cy = 190;
    const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': `The graph of ${ch.title}: its part, neighbours, related chapters and the articles that answer it` });
    const nodes = [], edges = [];
    const add = (n) => { nodes.push(n); return n; };
    const center = add({ x: cx, y: cy, label: ch.title, cls: 'center', r: 9 });
    const part = book.parts.find((p) => p.slug === ch.part);
    if (part) { const n = add({ x: cx, y: 36, label: part.title, cls: 'part', r: 7, href: '#' + part.slug + '-part' }); edges.push({ a: center, b: n, cls: 'seq', label: 'part' }); }
    const seq = ch.published ? chapters.filter((c) => c.published) : chapters.filter((c) => !c.published);
    const i = seq.indexOf(ch);
    if (i > 0) { const n = add({ x: 46, y: cy, label: seq[i - 1].title, cls: 'seq', r: 6, slug: seq[i - 1].slug }); edges.push({ a: center, b: n, cls: 'seq', label: 'before' }); }
    if (i >= 0 && i + 1 < seq.length) { const n = add({ x: W - 46, y: cy, label: seq[i + 1].title, cls: 'seq', r: 6, slug: seq[i + 1].slug }); edges.push({ a: center, b: n, cls: 'seq', label: 'after' }); }
    const rel = (ch.related || []).slice(0, 5);
    rel.forEach((r, k) => {
      const ang = Math.PI * (0.62 + 0.76 * (k / Math.max(1, rel.length - 1 || 1)) * (rel.length > 1 ? 1 : 0.5));
      const n = add({ x: cx + 130 * Math.cos(ang), y: cy + 120 * Math.sin(ang) + 10, label: (chapterOf(r.slug) || {}).title || r.slug, cls: 'rel', r: 6, slug: r.slug });
      edges.push({ a: center, b: n, cls: 'rel', label: r.shared.slice(0, 2).join(', ') });
    });
    (ch.articles || []).slice(0, 4).forEach((a, k) => {
      const n = add({ x: cx + 150 * Math.cos(-Math.PI * (0.18 + 0.16 * k)), y: cy + 120 * Math.sin(-Math.PI * (0.18 + 0.16 * k)), label: a.title, cls: 'art', r: 6, url: a.url });
      edges.push({ a: center, b: n, cls: 'art', label: 'answered by' });
    });
    for (const e of edges) {
      svg.appendChild(svgEl('line', { x1: e.a.x, y1: e.a.y, x2: e.b.x, y2: e.b.y, class: 'rd-edge ' + e.cls }));
      const t = svgEl('text', { x: (e.a.x + e.b.x) / 2, y: (e.a.y + e.b.y) / 2 - 3, class: 'rd-elabel', 'text-anchor': 'middle' }); t.textContent = e.label; svg.appendChild(t);
    }
    const fill = { center: 'var(--solid)', part: '#e8b64a', seq: '#94a3b8', rel: '#3b9fb0', art: '#0f766e' };
    for (const n of nodes) {
      const gnode = svgEl('g', { class: 'rd-node ' + n.cls });
      gnode.appendChild(svgEl('circle', { cx: n.x, cy: n.y, r: n.r, style: `fill:${fill[n.cls] || '#999'}` })); // style: a theme token needs var()
      const t = svgEl('text', { x: n.x, y: n.y + n.r + 12, 'text-anchor': 'middle' });
      const words = n.label.split(' '); let line = '', lines = [];
      for (const w of words) { if ((line + ' ' + w).trim().length > 20) { lines.push(line.trim()); line = w; } else line += ' ' + w; }
      lines.push(line.trim());
      lines.slice(0, 2).forEach((l, k) => { const ts = svgEl('tspan', { x: n.x, dy: k ? 12 : 0 }); ts.textContent = l + (k === 1 && lines.length > 2 ? '…' : ''); t.appendChild(ts); });
      gnode.appendChild(t);
      if (n.slug) gnode.onclick = () => go(n.slug);
      else if (n.url) gnode.onclick = () => window.open(n.url, '_blank', 'noopener');
      else if (n.href) gnode.onclick = () => { graphTab = 'book'; renderGraph(); };
      svg.appendChild(gnode);
    }
    // the paragraphs, one bar each
    const bx = 12, bw = Math.max(2, Math.min(14, (W - 24) / Math.max(1, ch.blocks.length) - 2));
    const rb = S.readBlocks[ch.slug] || {};
    ch.blocks.forEach((b, k) => {
      const has = S.comments.some((c) => c.block === b.id);
      const h = Math.max(6, Math.min(40, 6 + b.words / 6));
      const r = svgEl('rect', { x: bx + k * (bw + 2), y: H - 12 - h, width: bw, height: h, rx: 2, class: 'rd-bar', style: `fill:${has ? '#b45309' : (rb[b.id] ? '#94a3b8' : 'var(--line)')}` });
      const title = svgEl('title'); title.textContent = `Paragraph ${k + 1}, ${b.words} words${rb[b.id] ? ', read' : ''}${has ? ', commented' : ''}`; r.appendChild(title);
      r.onclick = () => { const e = document.querySelector(`[data-block="${b.id}"]`); if (e) e.scrollIntoView({ block: 'center', behavior: 'smooth' }); };
      svg.appendChild(r);
    });
    const lab = svgEl('text', { x: bx, y: H - 54, class: 'rd-elabel' }); lab.textContent = `${ch.blocks.length} paragraphs: grey read, orange commented`; svg.appendChild(lab);
    g.appendChild(svg);
    g.appendChild(el('div', 'glegend', '<span><i style="background:var(--solid)"></i>this chapter</span><span><i style="background:#e8b64a"></i>part</span><span><i style="background:#94a3b8"></i>before / after</span><span><i style="background:#3b9fb0"></i>shares terms</span><span><i style="background:#0f766e"></i>newsroom article</span>'));
    if (rel.length) g.appendChild(el('ul', 'gedges', rel.map((r) => `<li><b>${esc((chapterOf(r.slug) || {}).title || r.slug)}</b>: ${r.shared.map(esc).join(', ')}</li>`).join('')));
    if (ch.terms && ch.terms.length) g.appendChild(el('p', 'small dim', 'Terms: ' + ch.terms.map(esc).join(', ')));
    if (ch.ideas && ch.ideas.length) g.appendChild(el('p', 'small', 'Written from: ' + ch.ideas.map((i) => `<a href="${esc(i.url)}">${esc(i.title)}</a> <span class="dim">(${esc(i.state)})</span>`).join('; ')));
    if (ch.gap && ch.gap !== 'none' && ch.gap !== '') g.appendChild(el('p', 'small dim', 'The map says: ' + esc(ch.gap)));
  }
  function bookGraph(g) {
    g.appendChild(el('h3', null, 'The whole book'));
    const cols = book.parts.map((p) => ({ p, pub: chapters.filter((c) => c.part === p.slug && c.published), dr: chapters.filter((c) => c.part === p.slug && !c.published) }));
    const W = 360, rowH = 14, pad = 10;
    let y = 16; const items = [];
    for (const col of cols) {
      items.push({ y, label: col.p.title, head: true });
      y += rowH;
      for (const c of col.pub.concat(col.dr)) { items.push({ y, c }); y += rowH; }
      y += 6;
    }
    const H = y + pad;
    const svg = svgEl('svg', { viewBox: `0 0 ${W} ${H}`, role: 'img', 'aria-label': 'Every chapter by part: a filled dot is published, a hollow one a draft; colour is your reading state' });
    const col = { unread: '#e5e1d5', reading: '#60a5fa', read: '#94a3b8', review: '#fb923c', continue: '#818cf8', signed: '#4ade80' };
    for (const it of items) {
      if (it.head) { const t = svgEl('text', { x: 8, y: it.y, class: 'rd-elabel', 'font-weight': '700' }); t.textContent = it.label; svg.appendChild(t); continue; }
      const c = it.c, st = stateOf(c.slug);
      const gnode = svgEl('g', { class: 'rd-node' + (c.slug === current ? ' center' : '') });
      gnode.appendChild(svgEl('circle', { cx: 16, cy: it.y - 4, r: 4.5, style: `fill:${c.published ? col[st] : 'var(--panel)'};stroke:${c.published ? 'var(--solid)' : col[st] === '#e5e1d5' ? '#b45309' : col[st]}`, 'stroke-width': c.published ? 0.5 : 1.5 }));
      const t = svgEl('text', { x: 28, y: it.y }); t.textContent = (c.number ? c.number + '. ' : '') + c.title.slice(0, 40); gnode.appendChild(t);
      const n = S.comments.filter((x) => x.slug === c.slug).length;
      if (n) { const tc = svgEl('text', { x: W - 10, y: it.y, 'text-anchor': 'end', class: 'rd-elabel' }); tc.textContent = n + ' comment' + (n > 1 ? 's' : ''); gnode.appendChild(tc); }
      gnode.onclick = () => go(c.slug);
      svg.appendChild(gnode);
    }
    g.appendChild(svg);
    g.appendChild(el('div', 'glegend', Object.entries(col).map(([k, v]) => `<span><i style="background:${v}"></i>${STATES.find((s) => s[0] === k)[1]}</span>`).join('') + '<span>○ draft or outline</span>'));
  }

  // ---------------------------------------------------------------- export / import
  function reviewMarkdown() {
    const lines = [`# Review of Generation Z Developers, book v1.0.0`, '', `*From the reader at gen-z-developers.sgit.ai/read/, exported ${new Date().toISOString().slice(0, 16).replace('T', ' ')}. Balance ${pence(balance())}, spent ${pence(spent())}. For the vault's reviews/ folder; every finding is a comment on a paragraph, and the state is the reader's.*`, ''];
    const all = [book.front].concat(chapters);
    for (const ch of all) {
      const st = stateOf(ch.slug), cs = S.comments.filter((c) => c.slug === ch.slug), ch_ = S.charged[ch.slug];
      if (st === 'unread' && !cs.length) continue;
      lines.push(`## ${ch.title}`, '', `**File.** ${ch.file || '_manuscript/github-issues.md'}  **Version.** book v1.0.0  **State.** ${STATES.find((s) => s[0] === st)[1]}${ch_ ? `  **Read.** ${Math.round(ch_.share * 100)}%` : ''}`, '');
      cs.forEach((c, k) => {
        const b = ch.blocks.find((x) => x.id === c.block);
        const quote = b ? b.html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().slice(0, 160) : '';
        lines.push(`${k + 1}. ${c.text.replace(/\n/g, ' ')}`, `   > "${quote}${quote.length === 160 ? '…' : ''}" (${c.block}, ${c.at.slice(0, 10)})`, '');
      });
    }
    return lines.join('\n');
  }
  function download(name, text, type) {
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], { type })); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  function renderExport() {
    const x = $('rd-export');
    x.innerHTML = `<b>The review, as a file.</b> <span class="dim">Nothing leaves this browser unless you take it: the markdown goes in the vault's <code>reviews/</code> folder, the JSON restores this desk on another device.</span>
<div class="row"><button type="button" id="rd-dl-md">Download review.md</button><button type="button" id="rd-dl-json">Download review.json</button><button type="button" id="rd-copy">Copy the markdown</button><label class="btn">Import review.json <input type="file" id="rd-import" accept="application/json"></label><button type="button" id="rd-reset" title="Forget everything kept in this browser: balance, states, comments">Reset the desk</button></div>
<textarea readonly aria-label="The review as markdown">${esc(reviewMarkdown())}</textarea>`;
    $('rd-dl-md').onclick = () => download('review.md', reviewMarkdown(), 'text/markdown');
    $('rd-dl-json').onclick = () => download('review.json', JSON.stringify(Object.assign({ exported: new Date().toISOString(), book: 'v1.0.0' }, S), null, 1), 'application/json');
    $('rd-copy').onclick = async () => { try { await navigator.clipboard.writeText(reviewMarkdown()); $('rd-copy').textContent = 'Copied'; } catch (e) { $('rd-copy').textContent = 'Select and copy the text below'; } };
    $('rd-import').onchange = (ev) => {
      const f = ev.target.files[0]; if (!f) return;
      f.text().then((t) => { try { const d = JSON.parse(t); if (!d || !d.states) throw 0; S = Object.assign(fresh(), d); save(); renderAll(); } catch (e) { alert('That is not a review.json from this desk.'); } });
    };
    $('rd-reset').onclick = () => { if (confirm('Forget the balance, every state and every comment kept in this browser?')) { S = fresh(); save(); renderAll(); } };
  }

  // ---------------------------------------------------------------- navigation and observers
  function go(slug, instant) {
    const card = document.getElementById(slug); if (!card) return;
    if (S.folds[slug]) { S.folds[slug] = false; save(); applyFilter(); }
    card.hidden = false;
    history.replaceState(null, '', '#' + slug);
    card.scrollIntoView({ block: 'start', behavior: instant ? 'auto' : 'smooth' });
    setCurrent(slug);
  }
  function setCurrent(slug) {
    if (current === slug) return;
    current = slug;
    if (!S.opened[slug]) { S.opened[slug] = new Date().toISOString(); if (!S.states[slug]) S.states[slug] = 'reading'; save(); paintStateButtons(slug); paintTocItem(slug); settle(slug); }
    document.querySelectorAll('.rd-ch.current').forEach((e) => e.classList.remove('current'));
    const card = document.getElementById(slug); if (card) card.classList.add('current');
    document.querySelectorAll('.rd-toc a.here').forEach((e) => e.classList.remove('here'));
    const a = $('rd-toc').querySelector(`a[data-slug="${slug}"]`); if (a) { a.classList.add('here'); a.scrollIntoView({ block: 'nearest' }); }
    paintStrip(); renderGraph();
  }
  let chapterIO, blockIO;
  function observe() {
    if (blockIO) blockIO.disconnect();
    // the current chapter is the last one whose top has passed the reading line (just under the strip)
    const cards = [...document.querySelectorAll('.rd-ch[data-slug]')].filter((c) => !c.hidden);
    let ticking = false;
    const pick = () => {
      ticking = false;
      const line = 170; let best = null;
      for (const c of cards) { const r = c.getBoundingClientRect(); if (r.top <= line) best = c; else break; }
      if (!best && cards.length) best = cards[0];
      if (best) setCurrent(best.dataset.slug);
    };
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(pick); } };
    if (chapterIO) window.removeEventListener('scroll', chapterIO);
    chapterIO = onScroll; window.addEventListener('scroll', onScroll, { passive: true }); pick();
    const timers = new Map();
    blockIO = new IntersectionObserver((es) => {
      for (const e of es) {
        const id = e.target.dataset.block, slug = e.target.closest('.rd-ch').dataset.slug;
        if (e.isIntersecting) {
          if (!timers.has(id)) timers.set(id, setTimeout(() => {
            timers.delete(id);
            const rb = S.readBlocks[slug] || (S.readBlocks[slug] = {});
            if (!rb[id]) { rb[id] = 1; save(); settle(slug); if (S.mode === 'review') e.target.classList.add('readblk'); if (slug === current) renderGraph(); }
          }, Math.min(4000, 600 + Number(e.target.dataset.words) * 150)));
        } else if (timers.has(id)) { clearTimeout(timers.get(id)); timers.delete(id); }
      }
    }, { rootMargin: '-80px 0px -20% 0px', threshold: 0.6 });
    document.querySelectorAll('.rd-ch:not(.folded) .blk').forEach((b) => blockIO.observe(b));
  }

  // ---------------------------------------------------------------- events
  function wire() {
    $('rd-content').addEventListener('click', (ev) => {
      const t = ev.target;
      if (t.classList.contains('fold')) { const card = t.closest('.rd-ch'); const slug = card.dataset.slug; S.folds[slug] = !card.classList.contains('folded'); save(); applyFilter(); observe(); return; }
      if (t.classList.contains('cbtn')) {
        if (S.mode !== 'review') { S.mode = 'review'; save(); setMode(); }
        const box = t.parentElement.querySelector('.rd-comments'); box.dataset.open = box.dataset.open === '1' ? '0' : '1';
        paintComments(t.closest('.rd-ch').dataset.slug); const ta = box.querySelector('textarea'); if (ta) ta.focus(); return;
      }
      if (t.classList.contains('del')) { const id = t.parentElement.dataset.id; S.comments = S.comments.filter((c) => c.id !== id); save(); paintComments(t.closest('.rd-ch').dataset.slug); paintStrip(); renderGraph(); return; }
      if (t.closest('.rd-state') && t.dataset.s) { const slug = t.closest('.rd-state').dataset.slug; S.states[slug] = t.dataset.s; save(); paintStateButtons(slug); paintChapterFoot(slug); paintTocItem(slug); paintStrip(); renderGraph(); applyFilter(); return; }
    });
    $('rd-content').addEventListener('submit', (ev) => {
      const f = ev.target; if (!f.closest('.rd-comments')) return;
      ev.preventDefault();
      const ta = f.querySelector('textarea'); const text = ta.value.trim(); if (!text) return;
      const blk = f.closest('.blk'), slug = f.closest('.rd-ch').dataset.slug;
      S.comments.push({ id: 'c' + Date.now().toString(36), slug, block: blk.dataset.block, text, at: new Date().toISOString() });
      if (!S.states[slug] || S.states[slug] === 'reading' || S.states[slug] === 'read') S.states[slug] = 'review';
      save(); blk.querySelector('.rd-comments').dataset.open = '0'; paintComments(slug); paintStateButtons(slug); paintChapterFoot(slug); paintTocItem(slug); paintStrip(); renderGraph();
    });
    $('rd-toc').addEventListener('click', (ev) => { const a = ev.target.closest('a[data-slug]'); if (!a) return; ev.preventDefault(); go(a.dataset.slug); });
    $('rd-mode').onclick = () => { S.mode = S.mode === 'review' ? 'read' : 'review'; save(); setMode(); };
    $('rd-help').onclick = () => { const h = $('rd-helpbox'); h.hidden = !h.hidden; $('rd-help').setAttribute('aria-expanded', String(!h.hidden)); };
    document.addEventListener('keydown', (ev) => {
      if (ev.target.matches('input, textarea') || ev.metaKey || ev.ctrlKey || ev.altKey) return;
      const seq = [book.front.slug].concat(chapters.filter((c) => c.published).map((c) => c.slug), chapters.filter((c) => !c.published).map((c) => c.slug));
      const i = seq.indexOf(current);
      if (ev.key === 'j' && i + 1 < seq.length) go(seq[i + 1]);
      else if (ev.key === 'k' && i > 0) go(seq[i - 1]);
      else if (ev.key === 'g') { $('rd-graph').scrollIntoView({ block: 'nearest' }); }
      else if (ev.key === 'f' && current) { for (const c of chapters) S.folds[c.slug] = c.slug !== current; save(); applyFilter(); observe(); go(current); }
    });
    window.addEventListener('hashchange', () => { const s = location.hash.slice(1); if (s && bySlug[s]) go(s); });
    // images load after the first jump and move the page: keep the opened chapter pinned until the reader moves
    let pinned = null, userMoved = false;
    ['wheel', 'touchstart', 'keydown'].forEach((ev) => window.addEventListener(ev, () => { userMoved = true; }, { passive: true }));
    window.repin = (slug) => { pinned = slug; userMoved = false; };
    $('rd-content').addEventListener('load', (ev) => { if (ev.target.tagName === 'IMG' && pinned && !userMoved) { const c = document.getElementById(pinned); if (c) c.scrollIntoView({ block: 'start', behavior: 'auto' }); } }, true);
  }
  function setMode() {
    $('rd-mode').setAttribute('aria-pressed', String(S.mode === 'review'));
    $('rd-mode').textContent = S.mode === 'review' ? 'Review mode: on' : 'Review mode';
    renderFilters(); for (const ch of [book.front].concat(chapters)) { paintStateButtons(ch.slug); paintComments(ch.slug); } applyFilter(); paintStrip(); $('rd-export').hidden = S.mode !== 'review' || $('rd-export').hidden; observe();
  }
  function renderAll() {
    renderToc(); renderContent(); setMode(); renderGraph(); observe();
    const s = location.hash.slice(1);
    if (s && bySlug[s]) { go(s, true); window.repin(s); } else setCurrent(book.front.slug);
  }

  load();
  fetch(root.dataset.book, { cache: 'no-store' }).then((r) => r.json()).then((b) => {
    book = b; chapters = b.chapters; for (const c of chapters) bySlug[c.slug] = c;
    if (S.balance == null) S.balance = b.meter.start;
    wire(); renderAll();
  }).catch((e) => { root.insertAdjacentHTML('afterbegin', `<p class="note warn">The book could not be loaded (${esc(e.message || e)}). <a href="../v1/book/index.html">The table of contents</a> works without the reader.</p>`); });
})();
