from rest_framework import serializers

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    article_title = serializers.CharField(source="article.title", read_only=True)
    username = serializers.CharField(source="user.profile.username", read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "username", "article_title", "created_at"]
        read_only_fields = ["user"]
