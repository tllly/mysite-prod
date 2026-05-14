from django import template
from django.conf import settings
from django.utils import translation
from wagtail.models import Locale
from base.models import FooterText, InquiryPage, Certificate, Testimonial, FAQ

register = template.Library()

@register.inclusion_tag("base/includes/language_switcher.html", takes_context=True)
def language_switcher(context):
    request = context.get('request')
    page = context.get('page')
    
    current_language_code = translation.get_language()
    
    translations = {}
    if page and hasattr(page, 'get_translations'):
        for page_translation in page.get_translations().live():
            translations[page_translation.locale_id] = page_translation.url

    # Only show locales that have a valid published translation for this page,
    # OR the locale is the currently active one (so the user knows what they are looking at)
    locales = Locale.objects.all()
    available_locales = []
    for locale in locales:
        if locale.language_code == current_language_code or locale.id in translations:
            available_locales.append(locale)

    return {
        'request': request,
        'current_language_code': current_language_code,
        'locales': available_locales,
        'translations': translations,
        'page': page,
    }

@register.simple_tag
def get_inquiry_url():
    inquiry_page = InquiryPage.objects.live().first()
    return inquiry_page.url if inquiry_page else "#"

@register.inclusion_tag("base/includes/testimonials.html", takes_context=True)
def get_testimonials(context):
    return {
        'testimonials': Testimonial.objects.all(),
    }

@register.inclusion_tag("base/includes/faqs.html", takes_context=True)
def get_faqs(context):
    return {
        'faqs': FAQ.objects.all(),
    }

@register.inclusion_tag("base/includes/certificates.html", takes_context=True)
def get_certificates(context):
    return {
        'certificates': Certificate.objects.all(),
    }

@register.inclusion_tag("base/includes/footer_text.html", takes_context=True)
def get_footer_text(context):
    footer_text = context.get("footer_text", "")

    if not footer_text:
        instance = FooterText.objects.filter(live=True).first()
        footer_text = instance.body if instance else ""

    return {
        "footer_text": footer_text,
    }

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
