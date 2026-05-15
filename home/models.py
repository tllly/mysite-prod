from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )
    hero_text = models.CharField(
        blank=True,
        max_length=255, help_text="Write an introduction for the site"
    )
    hero_cta = models.CharField(
        blank=True,
        verbose_name="Hero CTA",
        max_length=255,
        help_text="Text to display on Call to Action",
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Hero CTA link",
        help_text="Choose a page to link to for the Call to Action",
    )

    body = RichTextField(blank=True)

    # New dynamic fields for previously hardcoded sections
    trust_section_title = models.CharField(
        max_length=255,
        default="Why Choose Us",
        verbose_name="Trust Section Title"
    )
    
    cta_section_title = models.CharField(
        max_length=255,
        default="Ready to Start Your Project?",
        verbose_name="CTA Section Title"
    )
    cta_section_text = models.CharField(
        max_length=500,
        default="Contact our expert team today for a free consultation and quote.",
        verbose_name="CTA Section Text"
    )
    cta_inquiry_button = models.CharField(
        max_length=100,
        default="Send Inquiry",
        verbose_name="Inquiry Button Text"
    )
    cta_whatsapp_button = models.CharField(
        max_length=100,
        default="WhatsApp Chat",
        verbose_name="WhatsApp Button Text"
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Hero section",
        ),
        FieldPanel('body'),
        MultiFieldPanel(
            [
                FieldPanel("trust_section_title"),
            ],
            heading="Trust Section (Certificates & Testimonials)",
        ),
        MultiFieldPanel(
            [
                FieldPanel("cta_section_title"),
                FieldPanel("cta_section_text"),
                FieldPanel("cta_inquiry_button"),
                FieldPanel("cta_whatsapp_button"),
            ],
            heading="Global Contact CTA Section",
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        from products.models import ProductPage, ProductIndexPage
        # Get up to 3 featured products, or the latest 3 if none are featured
        featured_products = ProductPage.objects.live().filter(is_featured=True).order_by('-first_published_at')[:3]
        if not featured_products.exists():
            featured_products = ProductPage.objects.live().order_by('-first_published_at')[:3]
        context['featured_products'] = featured_products
        context['product_index_page'] = ProductIndexPage.objects.live().first()
        return context
