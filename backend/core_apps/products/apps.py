from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticlesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.products"
    verbose_name = _("Products")

    def ready(self):
        import core_apps.products.signals  # noqa