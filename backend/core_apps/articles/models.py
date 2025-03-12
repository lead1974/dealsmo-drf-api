from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.utils import timezone
from datetime import timedelta

from core_apps.common.models import TimeStampedModel

from .read_time_engine import ArticleReadTimeEngine

User = get_user_model()


def get_default_end_date():
    return timezone.now() + timedelta(days=365*50)


class ArticleCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", always_update=True, unique=True)
    description = models.TextField(blank=True)
    sequence = models.IntegerField(default=0, help_text=_("Order in which the category appears"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("Parent Category"),
    )

    class Meta:
        verbose_name = _("Article Category")
        verbose_name_plural = _("Article Categories")
        ordering = ["sequence", "name"]

    def __str__(self):
        return self.name


class Clap(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "article"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.profile.username} clapped {self.article.title}"


class Article(TimeStampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")
        ARCHIVED = "archived", _("Archived")

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)
    description = models.CharField(verbose_name=_("description"), max_length=255)
    body = models.TextField(verbose_name=_("article content"))
    banner_image = models.ImageField(
        verbose_name=_("banner image"), default="/profile_default.png"
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("Article Category"),
    )
    tags = TaggableManager()
    claps = models.ManyToManyField(User, through=Clap, related_name="clapped_articles")
    
    # New fields
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_("Status")
    )
    start_date = models.DateTimeField(
        verbose_name=_("Start Date"),
        default=timezone.now,
        help_text=_("Date when the article becomes visible")
    )
    end_date = models.DateTimeField(
        verbose_name=_("End Date"),
        default=get_default_end_date,
        help_text=_("Date when the article will be archived")
    )

    def __str__(self):
        return f"{self.author.email} - {self.title}"

    @property
    def estimated_reading_time(self):
        return ArticleReadTimeEngine.estimate_reading_time(self)

    def view_count(self):
        return self.article_views.count()

    def average_rating(self):
        ratings = self.ratings.all()

        if ratings.count() > 0:
            total_rating = sum(rating.rating for rating in ratings)
            average_rating = total_rating / ratings.count()
            return round(average_rating, 2)
        return None

    @property
    def is_published(self):
        now = timezone.now()
        return (
            self.status == self.Status.PUBLISHED
            and self.start_date <= now
            and self.end_date > now
        )


class ArticleView(TimeStampedModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_views"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user_views"
    )
    viewer_ip = models.GenericIPAddressField(
        verbose_name=_("viewer IP"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Article View")
        verbose_name_plural = _("Article Views")
        unique_together = ("article", "user", "viewer_ip")

    def __str__(self):
        return f"{self.article.title} viewed by {self.user.profile.username if self.user else 'Anonymous'} from IP {self.viewer_ip}"

    @classmethod
    def record_view(cls, article, user, viewer_ip):
        view, _ = cls.objects.get_or_create(
            article=article, user=user, viewer_ip=viewer_ip
        )
        view.save()
