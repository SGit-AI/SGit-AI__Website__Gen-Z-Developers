#!/usr/bin/env node
// gen-z-developers.sgit.ai pre-release gate. Run from anywhere: node admin/build/validate.js
// The same shape as the gates of graphs.sgit.ai and pki.sgit.ai, reduced to what this site has. Checks, in order:
//   1. version agreement — admin/build/version.txt vs the badge on every page, the newest row of
//      admin/content/versions.json, and llms.txt
//   2. internal links — every relative href/src in every .html file resolves to a file in the tree
//      (fragments stripped; external, mailto and data links skipped)
//   3. canonical host — every <link rel="canonical"> and og:url points at the host in CNAME, and every page has one
//   4. key-leak tripwire — nothing in the tree may carry a PRIVATE sgit key: the rule is sgit's own scanner rule,
//      sgit_private_\S+, which covers every private credential kind, present and future. The public read key
//      (sgit_public_read_…) is public by design and passes. Also the legacy shape: a long passphrase joined by a
//      colon to an eight-character vault id.
//   5. div balance — every page opens and closes the same number of <div>s
//   6. the book is a projection of its markdown — v1/book/manifest.json records the hash of each chapter's
//      markdown and of the <main> it rendered; a markdown file edited without the build rerunning, or a page
//      hand-edited behind the markdown, fails here. v1/ is frozen, so this is also the freeze check.
//   7. the frozen version exists — v1/versions/v1.0.0.md is there and admin/content/book/versions.json names it
//   8. the map covers the book — every file under v1/content/ has a row in admin/content/map.json, and no row
//      names a file that is not there
//   9. the sitemap and the tree agree in both directions (404.html excepted)
// Any failure exits 1: no tag, no publish.
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = process.argv[2] ? path.resolve(process.argv[2]) : path.resolve(__dirname, '..', '..');
const errors = [];
const rel = f => path.relative(ROOT, f).split(path.sep).join('/');

function walk(dir, out = []) {
  for (const name of fs.readdirSync(dir)) {
    if (name === '.git' || name === '.github' || name === 'node_modules' || name === '.sg_vault') continue;
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, out); else out.push(p);
  }
  return out;
}
const files = walk(ROOT);
const htmlFiles = files.filter(f => f.endsWith('.html'));
const read = f => fs.readFileSync(f, 'utf8');
const sha = s => crypto.createHash('sha256').update(s, 'utf8').digest('hex');
let manifestChapters = 0;

// --- 1. version agreement ---------------------------------------------------
const VERSION = read(path.join(ROOT, 'admin/build/version.txt')).trim();
if (!/^v\d+\.\d+\.\d+$/.test(VERSION)) errors.push(`version.txt does not carry a vX.Y.Z version: "${VERSION}"`);
for (const f of htmlFiles) {
  const t = read(f);
  const m = t.match(/<span class="ver">site <a [^>]*>(v[\d.]+)<\/a><\/span>/);
  if (!m) errors.push(`${rel(f)}: no version badge`);
  else if (m[1] !== VERSION) errors.push(`${rel(f)}: badge says ${m[1]}, version.txt says ${VERSION}`);
}
const releases = JSON.parse(read(path.join(ROOT, 'admin/content/versions.json'))).releases;
if (releases[releases.length - 1].version !== VERSION) errors.push(`admin/content/versions.json: newest row is ${releases[releases.length - 1].version}, version.txt says ${VERSION}`);
if (!read(path.join(ROOT, 'llms.txt')).includes(`Site ${VERSION}.`)) errors.push(`llms.txt does not carry ${VERSION}`);

// --- 2. internal links ------------------------------------------------------
const HOST = read(path.join(ROOT, 'CNAME')).trim();
for (const f of htmlFiles) {
  const t = read(f);
  const re = /(?:href|src)="([^"#]*)(?:#[^"]*)?"/g;
  let m;
  while ((m = re.exec(t))) {
    const url = m[1];
    if (!url || /^(https?:|mailto:|data:|\/\/)/.test(url)) continue;
    const target = url.startsWith('/') ? path.join(ROOT, url) : path.resolve(path.dirname(f), url);
    const ok = fs.existsSync(target) && (fs.statSync(target).isFile() || fs.existsSync(path.join(target, 'index.html')));
    if (!ok) errors.push(`${rel(f)}: link to "${url}" does not resolve`);
  }
}

// --- 3. canonical host ------------------------------------------------------
for (const f of htmlFiles) {
  const t = read(f);
  const c = t.match(/<link rel="canonical" href="([^"]+)">/);
  if (!c) { errors.push(`${rel(f)}: no canonical`); continue; }
  if (!c[1].startsWith(`https://${HOST}/`)) errors.push(`${rel(f)}: canonical "${c[1]}" is not on ${HOST}`);
  const og = t.match(/<meta property="og:url" content="([^"]+)">/);
  if (og && og[1] !== c[1]) errors.push(`${rel(f)}: og:url disagrees with canonical`);
}

// --- 4. key-leak tripwire ---------------------------------------------------
const PRIVATE = /sgit_private_\S+/;
const LEGACY = /\b[A-Za-z0-9]{20,}:[a-z0-9]{8}\b/;
for (const f of files) {
  if (/\.(png|jpg|jpeg|webp|gif|pdf|ico|woff2?)$/i.test(f)) continue;
  const t = read(f);
  if (PRIVATE.test(t) && rel(f) !== 'admin/build/validate.js') errors.push(`${rel(f)}: carries a private sgit key (sgit_private_*)`);
  if (LEGACY.test(t) && !/sgit_public_read_/.test(t.match(LEGACY)[0]) && rel(f) !== 'admin/build/validate.js') {
    // the public read key is {64-hex}:{id} and is allowed; anything else of that shape is suspect
    const hit = t.match(LEGACY)[0];
    const pub = t.includes('sgit_public_read_' + hit);
    if (!pub) errors.push(`${rel(f)}: "${hit.slice(0, 12)}…" looks like a vault key`);
  }
}

// --- 5. div balance ---------------------------------------------------------
for (const f of htmlFiles) {
  const t = read(f);
  const open = (t.match(/<div\b/g) || []).length, close = (t.match(/<\/div>/g) || []).length;
  if (open !== close) errors.push(`${rel(f)}: ${open} <div> but ${close} </div>`);
}

// --- 6. the book is a projection of its markdown ----------------------------
// v1 (frozen: the markdown may not change at all) and, when it exists, v2 (the release candidate: its pages must match
// its markdown, and the candidate's frozen text is checked in 7).
for (const ed of [{ dir: 'v1', frozen: true }, { dir: 'v2', frozen: false }]) {
  const mf = path.join(ROOT, ed.dir, 'book/manifest.json');
  if (!fs.existsSync(mf)) { if (ed.frozen) errors.push(`${ed.dir}/book/manifest.json is missing`); continue; }
  const manifest = JSON.parse(read(mf));
  if (manifest.site !== VERSION) errors.push(`${ed.dir}/book/manifest.json was generated at ${manifest.site}, not ${VERSION}: rerun build.py`);
  for (const ch of manifest.chapters) {
    const mdPath = ed.frozen ? path.join(ROOT, 'v1/content', ch.file) : path.join(ROOT, ch.file);
    if (!fs.existsSync(mdPath)) { errors.push(`${ed.dir} manifest names ${ch.file}, which does not exist`); continue; }
    if (sha(read(mdPath)) !== ch.markdown_sha256) errors.push(ed.frozen ? `v1/content/${ch.file} changed since its page was built (v1 is frozen; a change needs a new version)` : `${ch.file} changed since its page was built: rerun build.py`);
    const pg = path.join(ROOT, ch.page);
    if (!fs.existsSync(pg)) { errors.push(`${ed.dir} manifest names ${ch.page}, which does not exist`); continue; }
    const main = read(pg).match(/<article class="chapter( v2)?">[\s\S]*?<\/article>/);
    if (!main) errors.push(`${ch.page}: no <article class="chapter">`);
    else if (sha(main[0]) !== ch.main_sha256) errors.push(`${ch.page}: hand-edited behind its markdown (hash differs from the manifest)`);
  }
  manifestChapters += manifest.chapters.length;
}

// --- 7. the frozen version exists -------------------------------------------
const bookDoc = JSON.parse(read(path.join(ROOT, 'admin/content/book/versions.json')));
for (const v of bookDoc.versions) {
  if (!fs.existsSync(path.join(ROOT, 'v1/versions', v.version + '.md'))) errors.push(`v1/versions/${v.version}.md is missing`);
  if (!v.text_sha256) errors.push(`admin/content/book/versions.json: ${v.version} has no text_sha256`);
}
for (const c of (bookDoc.candidates || [])) {
  // a candidate is frozen once; its text is checked by build.py against text_sha256, the gate checks the file is there and matches
  const fz = path.join(ROOT, c.frozen || ('v2/versions/' + c.version + '.md'));
  if (!c.text_sha256) errors.push(`admin/content/book/versions.json: candidate ${c.version} has no text_sha256 (run build.py)`);
  else if (!fs.existsSync(fz)) errors.push(`${c.frozen}: the frozen candidate is missing`);
  else if (sha(read(fz)) !== c.text_sha256) errors.push(`${c.frozen}: the frozen candidate no longer matches its recorded hash`);
  if (/^v\d+\.\d+\.\d+$/.test(c.version)) errors.push(`candidate ${c.version} is named like a version; a candidate carries a suffix (-rc1)`);
}

// --- 8. the map covers the book --------------------------------------------
const map = JSON.parse(read(path.join(ROOT, 'admin/content/map.json')));
const onDisk = new Set(files.filter(f => rel(f).startsWith('v1/content/') && f.endsWith('.md')).map(f => rel(f).slice('v1/content/'.length)));
const inMap = new Set(map.rows.map(r => r.file));
for (const f of onDisk) if (!inMap.has(f)) errors.push(`map.json has no row for v1/content/${f}`);
for (const f of inMap) if (!onDisk.has(f)) errors.push(`map.json names ${f}, which is not in v1/content`);

// --- 9. sitemap -------------------------------------------------------------
const sitemap = read(path.join(ROOT, 'sitemap.xml'));
const locs = new Set([...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1].replace(`https://${HOST}/`, '') || 'index.html'));
for (const f of htmlFiles) {
  const r = rel(f);
  if (r === '404.html') continue;
  if (!locs.has(r)) errors.push(`sitemap.xml does not list ${r}`);
}
for (const l of locs) if (!fs.existsSync(path.join(ROOT, l))) errors.push(`sitemap.xml lists ${l}, which does not exist`);

if (errors.length) {
  console.error(`validate: ${errors.length} problem(s)`);
  for (const e of errors) console.error('  - ' + e);
  process.exit(1);
}
console.log(`validate: ok — ${VERSION}, ${htmlFiles.length} pages, ${manifestChapters} chapters checked against their markdown, no private key in the tree`);
