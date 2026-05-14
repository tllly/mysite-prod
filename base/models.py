from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PublishingPanel,
    InlinePanel,
)
from wagtail.fields import RichTextField

import uuid
from wagtail.models import (
    Page,
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin,
    Locale,
)

class AboutPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]

    class Meta:
        verbose_name = "About Us Page"

from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

from wagtail.snippets.models import register_snippet

@register_setting
class NavigationSettings(BaseGenericSetting):
    whatsapp = models.CharField(max_length=255, help_text="WhatsApp number (e.g., 86138...)", blank=True)
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True)
    facebook_url = models.URLField(verbose_name="Facebook URL", blank=True)
    email = models.EmailField(blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("whatsapp"),
                FieldPanel("linkedin_url"),
                FieldPanel("facebook_url"),
                FieldPanel("email"),
            ],
            "Global Contact Settings",
        )
    ]

@register_setting
class TrackingSettings(BaseGenericSetting):
    ga_tracking_id = models.CharField(max_length=255, help_text="Google Analytics Tracking ID (e.g., G-XXXXX)", blank=True)
    gtm_container_id = models.CharField(max_length=255, help_text="Google Tag Manager Container ID (e.g., GTM-XXXXX)", blank=True)
    custom_head_scripts = models.TextField(help_text="Custom scripts to be added to the <head> section", blank=True)
    custom_body_scripts = models.TextField(help_text="Custom scripts to be added to the start of the <body> section", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("ga_tracking_id"),
                FieldPanel("gtm_container_id"),
                FieldPanel("custom_head_scripts"),
                FieldPanel("custom_body_scripts"),
            ],
            "Tracking & External Scripts",
        )
    ]

@register_snippet
class Testimonial(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True, help_text="e.g. CEO of Company X")
    quote = models.TextField()
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("quote"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name

@register_snippet
class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = RichTextField()

    panels = [
        FieldPanel("question"),
        FieldPanel("answer"),
    ]

    def __str__(self):
        return self.question

@register_snippet
class Certificate(TranslatableMixin, models.Model):
    translation_key = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    locale = models.ForeignKey(Locale, on_delete=models.PROTECT, related_name='+', null=True)
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name = "Certificate"

from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from modelcluster.fields import ParentalKey

class FormField(AbstractFormField):
    page = ParentalKey('InquiryPage', on_delete=models.CASCADE, related_name='form_fields')

class InquiryPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        product_name = self.request.GET.get('product')
        if product_name:
            # Try to pre-fill a field if it matches 'subject' or 'product'
            for field_name, field in form.fields.items():
                if field_name.lower() in ['subject', 'product', 'message']:
                    field.initial = f"Inquiry about: {product_name}"
                    # If it's a message field, maybe don't overwrite if not empty, 
                    # but initial is usually fine.
                    break
        return form

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('from_address'),
            FieldPanel('to_address'),
            FieldPanel('subject'),
        ], "Email Notification Config"),
    ]

@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model,
):

    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"

    def get_preview_template(self, request, mode_name):
        return "base.html"

    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"
