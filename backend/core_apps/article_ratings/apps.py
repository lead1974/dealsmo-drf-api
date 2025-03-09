from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ArticleRatingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.article_ratings"
    verbose_name = _("Article Ratings")
