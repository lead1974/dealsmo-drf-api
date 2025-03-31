from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class IssuesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.website_issues"
    verbose_name = _("Website Issues")
