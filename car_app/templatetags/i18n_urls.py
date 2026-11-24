from django import template
from django.conf import settings
from django.urls import translate_url

register = template.Library()


@register.simple_tag(takes_context=True)
def lang_url(context, code):
    """E njëjta faqe në gjuhën tjetër (p.sh. /cars/ -> /en/cars/), bashkë me parametrat."""
    request = context["request"]
    return translate_url(request.get_full_path(), code)


@register.simple_tag
def languages():
    return settings.LANGUAGES
