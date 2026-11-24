"""Mban mend nga erdhi vizitori herën e parë (Google, Instagram, Facebook, direkt...).

Burimi ruhet në session dhe i bashkëngjitet çdo rezervimi / klikimi (modeli Lead),
që raporti të tregojë cili kanal sjell klientë.
"""
from urllib.parse import urlparse

KNOWN = {
    "google": "google", "bing": "bing", "yahoo": "yahoo", "duckduckgo": "duckduckgo",
    "instagram": "instagram", "facebook": "facebook", "fb": "facebook", "tiktok": "tiktok",
    "t.co": "twitter", "twitter": "twitter", "x.com": "twitter", "linkedin": "linkedin",
    "whatsapp": "whatsapp", "booking": "booking.com", "tripadvisor": "tripadvisor",
}
SKIP_PREFIXES = ("/static/", "/media/", "/admin", "/t/", "/sw.js", "/manifest")


def detect_source(request):
    get = request.GET
    if get.get("utm_source"):
        return get["utm_source"].lower()[:40]
    if "gclid" in get:
        return "google ads"
    if "fbclid" in get:
        return "facebook"
    referrer = urlparse(request.META.get("HTTP_REFERER", "")).netloc.lower()
    if not referrer or referrer == request.get_host().lower():
        return "direct"
    for key, name in KNOWN.items():
        if key in referrer:
            return name
    return referrer.removeprefix("www.")[:40]


class TrafficSourceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.method == "GET" and "src" not in request.session
                and not request.path.startswith(SKIP_PREFIXES)):
            request.session["src"] = detect_source(request)
        return self.get_response(request)
