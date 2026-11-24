"""
BRANDING – i vetmi skedar që ndryshon për çdo klient.

Emri, logoja, ngjyra, qyteti, kontaktet dhe vendet e marrjes përdoren automatikisht
në të gjitha faqet, në email-e, te manifesti i aplikacionit (PWA) dhe te Google (SEO).

Për një klient të ri:
  1. Ndrysho vlerat më poshtë.
  2. (opsionale) Vendos logon te car_app/static/image/ dhe shkruaj emrin e skedarit te "logo_image".
  3. Zëvendëso foton e hero-s: car_app/static/image/hero1.webp (desktop) dhe hero1-mobile.webp (telefon).
  4. python manage.py collectstatic
"""

BRAND = {
    # --- Emri dhe logoja -------------------------------------------------------------
    "name": "DriveOn",                 # emri i plotë (titujt e faqeve, email-et, Google)
    "logo_first": "DRIVE",             # logoja si tekst: pjesa e parë (e zezë / e bardhë)
    "logo_second": "ON",               # pjesa e dytë, me ngjyrën e markës
    "logo_image": "",                  # p.sh. "image/logo.svg" – nëse vendoset, del në vend të tekstit

    # --- Ngjyrat ---------------------------------------------------------------------
    "color": "#e9002b",                # ngjyra kryesore (butonat, theksimet)
    "color_hover": "#bb0022",          # e njëjta, pak më e errët (kur kalon miun mbi butona)

    # --- Vendndodhja -----------------------------------------------------------------
    "city": "Tirana",
    "country": "Albania",
    "address": "Tirana, Albania",
    "map_query": "Tirana, Albania",    # çfarë kërkohet në hartën te faqja Contact
    "locations": ("Tirana", "Durrës", "Tirana Airport"),  # vendet e marrjes (rezervimi, filtrat, footer)

    # --- Kontaktet -------------------------------------------------------------------
    "phone": "+355 69 000 0000",       # si shfaqet
    "email": "info@driveon.al",
    "hours": "Every day, 08:00 – 20:00",
    "instagram": "https://www.instagram.com/driveon",
    "facebook": "https://www.facebook.com/driveon",
}


# ---- Vlerat që llogariten automatikisht (nuk ka nevojë të ndryshohen) -------------------

def _hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def _lighten(color, amount=0.12):
    r, g, b = _hex_to_rgb(color)
    return "#{:02x}{:02x}{:02x}".format(*(round(c + (255 - c) * amount) for c in (r, g, b)))


def _join_or(items):
    items = list(items)
    return items[0] if len(items) == 1 else f"{', '.join(items[:-1])} or {items[-1]}"


def site():
    """Të dhënat që marrin template-t si {{ site.* }}."""
    phone_digits = "".join(ch for ch in BRAND["phone"] if ch.isdigit())
    return {
        **BRAND,
        "phone_link": f"+{phone_digits}",                 # për tel:
        "whatsapp": phone_digits,                          # për wa.me/
        "color_rgb": ", ".join(map(str, _hex_to_rgb(BRAND["color"]))),   # "233, 0, 43"
        "color_light": _lighten(BRAND["color"]),
        "locations_text": _join_or(BRAND["locations"]),    # "Tirana, Durrës or Tirana Airport"
    }


LOCATIONS = BRAND["locations"]
