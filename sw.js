/* Vocab MASter EV service worker. Bump VERSION on every release so phones get the update.
   Only caches that start with PREFIX are cleaned up, so other MAS Studio apps on the same site keep theirs. */
const PREFIX = 'vocab-master-ev-';
const VERSION = PREFIX + 'v1.2.0';
const SHELL = ["./", "index.html", "manifest.webmanifest", "words-index.js", "logo-mark.png", "photon-banner.jpg", "favicon-64.png", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "author.jpg", "author-cover.jpg", "barlow-400.woff2", "barlow-500.woff2", "barlow-600.woff2", "barlow-700.woff2", "barlow-condensed-500.woff2", "barlow-condensed-600.woff2", "barlow-condensed-700.woff2", "newsreader-500.woff2", "newsreader-400-italic.woff2"];
const WORDS = ["words-01.js", "words-02.js", "words-03.js", "words-04.js", "words-05.js", "words-06.js", "words-07.js", "words-08.js", "words-09.js", "words-10.js", "words-11.js", "words-12.js", "words-13.js", "words-14.js", "words-15.js", "words-16.js", "words-17.js", "words-18.js", "words-19.js", "words-20.js", "words-21.js", "words-22.js", "words-23.js", "words-24.js", "words-25.js", "words-26.js", "words-27.js", "words-28.js", "words-29.js", "words-30.js", "words-31.js", "words-32.js", "words-33.js", "words-34.js", "words-35.js", "words-36.js", "words-37.js", "words-38.js", "words-39.js", "words-40.js", "words-41.js", "words-42.js", "words-43.js", "words-44.js", "words-45.js", "words-46.js", "words-47.js", "words-48.js", "words-49.js", "words-50.js", "words-51.js", "words-52.js", "words-53.js", "words-54.js", "words-55.js", "words-56.js", "words-57.js", "words-58.js", "words-59.js", "words-60.js", "words-index.js"];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k.startsWith(PREFIX) && k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
    .then(() => caches.open(VERSION)).then(c => Promise.all(WORDS.map(u => c.match(u).then(hit => hit || fetch(u).then(r => r.ok && c.put(u, r)).catch(() => {}))))));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;
  if (req.mode === 'navigate' || url.pathname.endsWith('/index.html')) {
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(VERSION).then(c => c.put('index.html', copy)); return r; })
      .catch(() => caches.match('index.html')));
    return;
  }
  e.respondWith(caches.match(req, {ignoreSearch: true}).then(hit => hit || fetch(req).then(r => {
    if (r.ok) { const copy = r.clone(); caches.open(VERSION).then(c => c.put(req, copy)); }
    return r;
  })));
});
