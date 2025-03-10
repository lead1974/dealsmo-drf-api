from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404

from .models import Article, ArticleResponse
from .serializers import ArticleResponseSerializer


class ArticleResponseListCreateView(generics.ListCreateAPIView):
    queryset = ArticleResponse.objects.all()
    serializer_class = ArticleResponseSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        article_slug = self.kwargs.get("slug")
        return ArticleResponse.objects.filter(
            article__slug=article_slug, parent_response=None
        )

    def perform_create(self, serializer):
        user = self.request.user
        article_slug = self.kwargs.get("slug")
        article = get_object_or_404(Article, slug=article_slug)
        serializer.save(user=user, article=article)


class ArticleResponseUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleResponse.objects.all()
    serializer_class = ArticleResponseSerializer
    lookup_field = "id"

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        user = self.request.user
        response = self.get_object()
        if user != response.user:
            raise PermissionDenied("You do not have permission to edit this response.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        response = self.get_object()
        if user != response.user:
            raise PermissionDenied(
                "You do not have permission to delete this response."
            )
        instance.delete()
