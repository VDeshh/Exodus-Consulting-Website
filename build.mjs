// Exodus Consulting - build dist/ for Vercel.
// Node port of the copy step in deploy.ps1, because Vercel runs the build on
// Linux and cannot run PowerShell. Same rules: every site page plus css, js
// and assets, never the internal reference docs or the raw app captures.
import { cpSync, mkdirSync, readdirSync, rmSync, statSync } from 'node:fs';
import { join } from 'node:path';

const src = new URL('.', import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1');
const dist = join(src, 'dist');

rmSync(dist, { recursive: true, force: true });
mkdirSync(dist);

// every site page
const notAPage = /^(Exodus-|oc-email|exodus-standalone|train-animation)/;
let pages = 0;
for (const f of readdirSync(src)) {
  if (f.endsWith('.html') && !notAPage.test(f)) {
    cpSync(join(src, f), join(dist, f));
    pages++;
  }
}

for (const d of ['css', 'js', 'assets']) cpSync(join(src, d), join(dist, d), { recursive: true });

// never publish these
for (const p of [
  'assets/product/raw',
  'assets/product/prep.py',
  'assets/product/index.jpg',
  'assets/product/contact-sheet.jpg',
  'css/PARTIALS.html',
]) rmSync(join(dist, p), { recursive: true, force: true });
for (const f of readdirSync(join(dist, 'css'))) {
  if (f.endsWith('.md')) rmSync(join(dist, 'css', f));
}

const size = (p) => {
  const s = statSync(p);
  return s.isDirectory() ? readdirSync(p).reduce((n, f) => n + size(join(p, f)), 0) : s.size;
};
console.log(`dist built: ${pages} pages, ${(size(dist) / 1048576).toFixed(1)} MB`);
