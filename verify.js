// Vocab MASter EV data check. Run with Node.js from the repo folder:  node verify.js
// Confirms every full entry has a definition, part of speech, five example sentences,
// strongest synonyms, collocations and related words, checks the EV 1.2 usage labels,
// word-forms tables and every-form sentences, and reports thesaurus coverage.
const fs = require('fs');
let INDEX = null; const SHARDS = {};
global.VM = { index(d) { INDEX = d; }, put(n, o) { SHARDS[n] = o; } };
eval(fs.readFileSync(__dirname + '/words-index.js', 'utf8'));
const files = fs.readdirSync(__dirname).filter(f => /^words-\d+\.js$/.test(f)).sort();
for (const f of files) eval(fs.readFileSync(__dirname + '/' + f, 'utf8'));
const all = Object.assign({}, ...Object.values(SHARDS));
let fail = 0, ex = 0, fx = 0, lab = 0; const stat = { s5: 0, k5: 0, r5: 0, a1: 0, cl3: 0, fm: 0, exl: 0 };
const bad = (w, why) => { fail++; if (fail < 30) console.log('FAIL', w, '-', why); };
for (const c of INDEX.c) {
  const e = all[c[0].toLowerCase()];
  if (!e) { bad(c[0], 'missing from data files'); continue; }
  if (!e.d) bad(c[0], 'no definition');
  if (!e.pos) bad(c[0], 'no part of speech');
  if (!Array.isArray(e.ex) || e.ex.length < 5) bad(c[0], 'fewer than 5 example sentences');
  if (/[ঀ-৿]/.test(JSON.stringify(e))) bad(c[0], 'contains Bangla text (EV is English only)');
  ex += (e.ex || []).length;
  if (e.exl) { if (e.exl.length !== (e.ex || []).length) bad(c[0], 'usage labels do not match the sentences'); else { stat.exl++; lab += e.exl.length; } }
  for (const f of (e.fx || [])) { if (!Array.isArray(f) || f.length !== 2 || !f[0] || !f[1]) bad(c[0], 'malformed every-form sentence'); else { fx++; lab++; } }
  if (e.fm) { if (!e.fm.every(f => Array.isArray(f) && f[0] && f[1])) bad(c[0], 'malformed word-forms table'); else stat.fm++; }
  if ((e.s || []).length >= 5) stat.s5++;
  if ((e.k || []).length >= 5) stat.k5++;
  if ((e.r || []).length >= 5) stat.r5++;
  if ((e.a || []).length + (e.aw || []).length >= 1) stat.a1++;
  if ((e.cl || []).length >= 3) stat.cl3++;
}
INDEX.b.forEach((w, i) => { const s = SHARDS[i + 1]; if (!s || Object.keys(s)[0] !== w) bad(w, 'shard boundary ' + (i + 1) + ' is out of order'); });
const n = INDEX.c.length, pct = x => (100 * x / n).toFixed(1) + '%';
const bits = b => INDEX.c.filter(c => c[3] & b).length;
console.log(`Full entries: ${n}  ·  thesaurus entries: ${INDEX.lw.split('|').length}  ·  example sentences: ${ex + fx} (${fx} every-form)  ·  labelled: ${lab}`);
console.log(`Entries with usage labels: ${pct(stat.exl)}  ·  with a word-forms table: ${pct(stat.fm)}`);
console.log(`5+ strongest synonyms: ${pct(stat.s5)}  ·  5+ weak synonyms: ${pct(stat.k5)}  ·  5+ related words: ${pct(stat.r5)}  ·  3+ collocations: ${pct(stat.cl3)}  ·  has antonyms: ${pct(stat.a1)}`);
console.log(`IBA: ${bits(64)}  Barron's 333: ${bits(1)}  GRE 500 Essential: ${bits(2)}  GRE 500 Advanced: ${bits(4)}  GRE Hit Parade: ${bits(8)}`);
console.log(`Word Smart I: ${bits(16)}  Word Smart II: ${bits(32)}  TOEFL AWL: ${bits(128)}  Oxford 3000: ${bits(256)}  Starter Set: ${bits(512)}`);
console.log(fail ? `${fail} problems found` : 'All checks passed.');
process.exit(fail ? 1 : 0);
