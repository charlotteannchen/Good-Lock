var staticCacheName = 'djangopwa-v1';

// Cache the PWA files during the service worker installation
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        // List all files you want to cache initially
        '/pwa_download',  // Cache the /pwa_download path
        // Add other assets as needed
      ]);
    })
  );
});

// Handle fetch events
self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);
  
  // Check if the request URL's origin matches the location origin
  if (requestUrl.origin === location.origin) {
    if (requestUrl.pathname === '/pwa_download') {
      // Respond with cached response for the /pwa_download path
      event.respondWith(caches.match('/pwa_download').then(function(response) {
        return response || fetch(event.request);
      }));
      return;
    }
  }

  // Default fetch handler for other requests
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
