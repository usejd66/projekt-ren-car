/* Service worker (versioni {{ version }}).
   - Faqet: gjithmonë nga rrjeti (çmimet dhe datat e lira duhet të jenë të sakta);
     pa internet shfaqet /offline/.
   - Skedarët statikë dhe fotot: nga cache-i (emrat kanë hash, nuk ndryshojnë). */
const CACHE = "site-{{ version }}";
const PRECACHE = [{% for url in urls %}"{{ url|escapejs }}"{% if not forloop.last %}, {% endif %}{% endfor %}];

self.addEventListener("install", (event) => {
    event.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
    // fshi cache-t e versioneve të vjetra
    event.waitUntil(
        caches.keys()
            .then((keys) => Promise.all(keys.filter((k) => k.startsWith("site-") && k !== CACHE).map((k) => caches.delete(k))))
            .then(() => self.clients.claim())
    );
});

self.addEventListener("fetch", (event) => {
    const req = event.request;
    const url = new URL(req.url);
    if (req.method !== "GET" || url.origin !== self.location.origin || url.pathname.startsWith("/admin")) return;

    if (req.mode === "navigate") {
        event.respondWith(fetch(req).catch(() => caches.match("/offline/")));
        return;
    }

    if (url.pathname.startsWith("/static/") || url.pathname.startsWith("/media/")) {
        event.respondWith(
            caches.match(req).then((hit) => hit || fetch(req).then((res) => {
                if (res.ok) {
                    const copy = res.clone();
                    caches.open(CACHE).then((cache) => cache.put(req, copy));
                }
                return res;
            }))
        );
    }
});
