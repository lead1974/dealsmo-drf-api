from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticleBookmarksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.product_ratings"
    verbose_name = _("Product Ratings")
