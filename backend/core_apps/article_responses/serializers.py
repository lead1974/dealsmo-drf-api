from rest_framework import serializers

from .models import ArticleResponse


class ArticleResponseSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.profile.username", read_only=True)
    article_title = serializers.CharField(source="article.title", read_only=True)

    class Meta:
        model = ArticleResponse
        fields = [
            "id",
            "username",
            "article_title",
            "parent_response",
            "content",
            "created_at",
        ]
