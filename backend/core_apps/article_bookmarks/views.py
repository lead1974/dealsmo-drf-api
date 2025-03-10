from uuid import UUID

from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound, ValidationError

from core_apps.articles.models import Article

from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkCreateView(generics.CreateAPIView):
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        article_slug = self.kwargs.get("slug")

        if article_slug:
            try:
                article = Article.objects.get(slug=article_slug)
            except Article.DoesNotExist:
                raise ValidationError("Invalid article slug provided")
        else:
            raise ValidationError("article slug is required")
        try:
            serializer.save(user=self.request.user, article=article)
        except IntegrityError:
            raise ValidationError("You have already bookmarked this article")


class BookmarkDestroyView(generics.DestroyAPIView):
    queryset = Bookmark.objects.all()
    lookup_field = "article__slug"
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        article_slug = self.kwargs.get("slug")

        try:
            bookmark = Bookmark.objects.get(user=user, article__slug=article_slug)
        except Bookmark.DoesNotExist:
            raise NotFound("Bookmark not found or it doesn't belong to you.")

        return bookmark

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user != user:
            raise ValidationError("You cannot delete a bookmark that is not yours")
        instance.delete()
