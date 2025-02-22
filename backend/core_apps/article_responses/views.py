from rest_framework import generics
from rest_framework.generics import get_object_or_404
from .models import Article, ArticleResponse
from .serializers import ArticleResponseSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions


class ArticleResponseListCreateView(generics.ListCreateAPIView):
    queryset = ArticleResponse.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ArticleResponseSerializer

    def get_queryset(self):
        article_id = self.kwargs.get("article_id")
        return ArticleResponse.objects.filter(article__id=article_id, parent_response=None)

    def perform_create(self, serializer):
        user = self.request.user
        article_id = self.kwargs.get("article_id")
        article = get_object_or_404(Article, id=article_id)
        serializer.save(user=user, article=article)


class ArticleResponseUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArticleResponse.objects.all()
    serializer_class = ArticleResponseSerializer
    lookup_field = "id"

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