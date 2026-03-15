from django import template

from base.models import FooterText, InquiryPage, Certificate

register = template.Library()

@register.simple_tag
def get_inquiry_url():
    inquiry_page = InquiryPage.objects.live().first()
    return inquiry_page.url if inquiry_page else "#"

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