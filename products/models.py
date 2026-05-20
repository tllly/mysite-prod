from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

import uuid
from wagtail.models import Page, Orderable, TranslatableMixin, Locale
from wagtail.fields import RichTextField
from wagtail.admin.panels import MultiFieldPanel, FieldPanel, InlinePanel
from wagtail.snippets.models import register_snippet


class ProductIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        productpages = self.get_children().live().order_by('-first_published_at')
        context['productpages'] = productpages
        return context

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

class ProductPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'ProductPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class ProductCategory(TranslatableMixin, models.Model):
    translation_key = models.UUIDField(default=uuid.uuid4, editable=False, null=True)
    locale = models.ForeignKey(Locale, on_delete=models.PROTECT, related_name='+', null=True)
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("icon"),
    ]

    def __str__(self):
        return self.name

    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = 'Product Categories'

class ProductPage(Page):
    sku = models.CharField(max_length=50, blank=True, verbose_name="SKU / Item No.")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Price")
    moq = models.CharField(max_length=100, blank=True, verbose_name="MOQ (Minimum Order Quantity)")
    lead_time = models.CharField(max_length=100, blank=True, verbose_name="Lead Time")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    specifications = RichTextField(blank=True, verbose_name="Specifications")
    packaging_details = RichTextField(blank=True, verbose_name="Packaging Details")
    video_file = models.ForeignKey(
        'wagtailmedia.Media',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Local Video File"
    )
    video_url = models.URLField(blank=True, verbose_name="External Video URL (YouTube/Vimeo)")
    is_featured = models.BooleanField(default=False, verbose_name="Is Featured")

    categories = ParentalManyToManyField('products.ProductCategory', blank=True)
    tags = ClusterTaggableManager(through=ProductPageTag, blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_context(self, request):
        context = super().get_context(request)
        # Find related products by tags
        tag_ids = self.tags.values_list('id', flat=True)
        related_products = ProductPage.objects.live().filter(tags__in=tag_ids).exclude(id=self.id).distinct()[:3]
        context['related_products'] = related_products
        return context

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("sku"),
            FieldPanel("price"),
            FieldPanel("moq"),
            FieldPanel("lead_time"),
            FieldPanel("is_featured"),
            FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            FieldPanel("tags"),
        ], heading="Product information"),
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("specifications"),
        FieldPanel("packaging_details"),
        InlinePanel("product_variants", label="Available Specifications / Variants"),
        FieldPanel("video_file"),
        FieldPanel("video_url"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]

class ProductVariant(Orderable):
    page = ParentalKey(ProductPage, on_delete=models.CASCADE, related_name='product_variants')
    name = models.CharField(max_length=255, help_text="e.g. 1 Round Liner (.25mm Long Taper)")
    stock_status = models.CharField(
        max_length=100, 
        default="In Stock", 
        help_text="e.g. In Stock, Lead time 2 weeks, etc."
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("stock_status"),
    ]

class ProductPageGalleryImage(Orderable):
    page = ParentalKey(ProductPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]

class ProductTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get('tag')
        productpages = ProductPage.objects.filter(tags__name=tag)
        context = super().get_context(request)
        context['productpages'] = productpages
        return context
