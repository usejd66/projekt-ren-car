from django import template
from django.templatetags.static import static
from django.utils.html import format_html

from ..images import variant_urls

register = template.Library()

FALLBACK = "image/hero.webp"


def _img(image, alt, sizes, css_class, loading, width, fetchpriority=""):
    extra = format_html(' fetchpriority="{}"', fetchpriority) if fetchpriority else ""
    if not image:
        return format_html('<img src="{}" alt="{}" class="{}" loading="{}" decoding="async"{}>',
                           static(FALLBACK), alt, css_class, loading, extra)
    urls = variant_urls(image.name)
    if not urls:  # versionet ende s'janë krijuar: përdor origjinalin
        return format_html('<img src="{}" alt="{}" class="{}" loading="{}" decoding="async"{}>',
                           image.url, alt, css_class, loading, extra)
    srcset = ", ".join(f"{url} {w}w" for w, url in urls.items())
    src = urls.get(width) or next(iter(urls.values()))
    return format_html(
        '<img src="{}" srcset="{}" sizes="{}" alt="{}" class="{}" loading="{}" decoding="async"{}>',
        src, srcset, sizes, alt, css_class, loading, extra,
    )


@register.simple_tag
def car_img(car, sizes="100vw", css_class="", loading="lazy", width=960, fetchpriority=""):
    """<img> me srcset për foton kryesore të makinës (ose foton rezervë).

    {% car_img car sizes="(min-width: 1200px) 300px, 100vw" css_class="..." %}
    """
    return _img(car.image, str(car), sizes, css_class, loading, width, fetchpriority)


@register.simple_tag
def photo_img(image, alt, sizes="100vw", css_class="", loading="lazy", width=960, fetchpriority=""):
    """<img> me srcset për çdo ImageField (p.sh. fotot e galerisë)."""
    return _img(image, alt, sizes, css_class, loading, width, fetchpriority)


@register.simple_tag
def car_img_url(car, width=480):
    """Vetëm URL-ja e një versioni (p.sh. për data-image te rezervimi)."""
    return img_url(car.image, width)


@register.simple_tag
def img_url(image, width=480):
    if not image:
        return static(FALLBACK)
    return variant_urls(image.name).get(width) or image.url
