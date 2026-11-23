from django import template
from django.templatetags.static import static
from django.utils.html import format_html

from ..images import variant_urls

register = template.Library()

FALLBACK = "image/hero.webp"


@register.simple_tag
def car_img(car, sizes="100vw", css_class="", loading="lazy", width=960):
    """<img> me srcset për foton e makinës (ose foton rezervë nëse nuk ka).

    Përdorimi: {% car_img car sizes="(min-width: 1200px) 300px, 100vw" css_class="..." %}
    """
    alt = str(car)
    if not car.image:
        return format_html(
            '<img src="{}" alt="{}" class="{}" loading="{}" decoding="async">',
            static(FALLBACK), alt, css_class, loading,
        )
    urls = variant_urls(car.image.name)
    if not urls:  # versionet ende s'janë krijuar: përdor origjinalin
        return format_html(
            '<img src="{}" alt="{}" class="{}" loading="{}" decoding="async">',
            car.image.url, alt, css_class, loading,
        )
    srcset = ", ".join(f"{url} {w}w" for w, url in urls.items())
    src = urls.get(width) or next(iter(urls.values()))
    return format_html(
        '<img src="{}" srcset="{}" sizes="{}" alt="{}" class="{}" loading="{}" decoding="async">',
        src, srcset, sizes, alt, css_class, loading,
    )


@register.simple_tag
def car_img_url(car, width=480):
    """Vetëm URL-ja e një versioni (p.sh. për data-image te rezervimi)."""
    if not car.image:
        return static(FALLBACK)
    urls = variant_urls(car.image.name)
    return urls.get(width) or car.image.url
