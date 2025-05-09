from django.db import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from core_apps.articles.models import Article
from core_apps.article_ratings.exceptions import YouhaveAlreadyRated

from .models import Rating
from .serializers import RatingSerializer


@extend_schema(tags=['ratings'])
class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
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
            raise YouhaveAlreadyRated
