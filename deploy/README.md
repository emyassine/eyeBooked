# EyeBooked mobile deploy package

Upload the full `deploy/` directory to a PHP host that serves HTTPS. Open `index.php` on a phone and use the browser's install prompt, or choose **Add to Home Screen** in Safari. The service worker caches the app shell after its first successful visit.

The PHP page is a mobile-first copy of `index-14.html`. It uses local Tailwind, Font Awesome, and font files so the main interface can load from the service worker cache. `manifest.webmanifest` defines the installable app, `service-worker.js` handles offline reloads, and the PNG icons cover standard, maskable, and iOS home-screen use.

`og-image.png` is 1200 × 630. The page builds absolute Open Graph image URLs from the current host and app path.

This source is an interactive front-end prototype. Sign-in, appointments, checkout, rewards, AI face analysis, and other integrations still need production backends or service credentials before they represent live services. Most demo state stays in the browser's local storage. Geolocation and any hosted AI feature require a network connection.
