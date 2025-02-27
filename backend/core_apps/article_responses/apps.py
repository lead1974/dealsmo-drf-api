from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ResponsesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.article_responses"
    verbose_name = _("Article Responses")
