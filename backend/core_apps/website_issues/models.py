import logging

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL

from core_apps.common.models import TimeStampedModel


User = get_user_model()

logger = logging.getLogger(__name__)


class Issue(TimeStampedModel):
    class IssueStatus(models.TextChoices):
        REPORTED = ("reported", _("Reported"))
        RESOLVED = ("resolved", _("Resolved"))
        IN_PROGRESS = ("in_progress", _("In Progress"))

    class Priority(models.TextChoices):
        LOW = ("low", _("Low"))
        MEDIUM = ("medium", _("Medium"))
        HIGH = ("high", _("High"))

    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reported_by_issues",
        verbose_name=_("Reported by"),
    )

    title = models.CharField(verbose_name=_("Issue Title"), max_length=255)
    description = models.TextField(verbose_name=_("Issue Description"))
    status = models.CharField(
        max_length=20,
        choices=IssueStatus.choices,
        default=IssueStatus.REPORTED,
        verbose_name=_("Status"),
    )
    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.LOW,
        verbose_name=_("Priority"),
    )
    resolved_on = models.DateField(verbose_name=_("Resolved On"), null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        is_existing_instance = self.pk is not None

        if is_existing_instance:
            old_issue = Issue.objects.get(pk=self.pk)
        super().save(*args, **kwargs)