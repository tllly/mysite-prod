from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import ProductPage, ProductCategory

@register_snippet
class ProductCategoryViewSet(SnippetViewSet):
    model = ProductCategory
    icon = "tag"
    menu_label = "Product Categories"
    menu_order = 300
    add_to_admin_menu = False
    list_display = ("name",)

# For ProductPage, we will rely on the default Pages menu for now to avoid compatibility issues with PageViewSet
