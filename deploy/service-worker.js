const CACHE_NAME = "eyebooked-shell-v1";
const APP_SHELL = [
  "./index.php",
  "./manifest.webmanifest",
  "./favicon.png",
  "./apple-touch-icon.png",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./og-image.png",
  "./assets/fonts.css",
  "./assets/js/tailwind-3.4.17.js",
  "./assets/js/fontawesome-6.5.1.js",
  "./assets/fonts/PlusJakartaSans-Variable.ttf",
  "./assets/fonts/NotoSansArabic-400.ttf",
  "./assets/fonts/NotoSansArabic-600.ttf",
  "./assets/fonts/NotoSansArabic-700.ttf"
];

self.addEventListener("install", event => {
  event.waitUntil(caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener("activate", event => {
  event.waitUntil(caches.keys().then(keys => Promise.all(
    keys.filter(key => key.startsWith("eyebooked-") && key !== CACHE_NAME).map(key => caches.delete(key))
  )));
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;

  if (request.mode === "navigate") {
    event.respondWith(fetch(request).then(response => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put("./index.php", copy));
      return response;
    }).catch(() => caches.match("./index.php")));
    return;
  }

  event.respondWith(caches.match(request).then(cached => cached || fetch(request).then(response => {
    if (response.ok) {
      const copy = response.clone();
      caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
    }
    return response;
  })));
});
