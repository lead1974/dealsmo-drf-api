from django.db import models
from django.contrib.auth import get_user_model
from core_apps.common.models import TimeStampedModel
from core_apps.articles.models import Article
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class ArticleResponse(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article_responses")
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="article_responses"
    )
    parent_response = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="article_replies"
    )

    content = models.TextField(verbose_name=_("article response content"))

    class Meta:
        verbose_name = "Article Response"
        verbose_name_plural = "Article Responses"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.profile.username} commented on {self.article.title}"