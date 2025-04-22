from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, ArticleViewCountView, ClapArticleView, ArticleCategoryViewSet

router = DefaultRouter()
router.register(r"article-categories", ArticleCategoryViewSet, basename="article-category")
router.register(r"", ArticleViewSet, basename="article")

urlpatterns = [
    path("categories/", ArticleCategoryViewSet.as_view({"get": "list"}), name="article-categories"),
    path("all/", ArticleViewSet.as_view({"get": "all"}), name="article-all"),
    path("published/", ArticleViewSet.as_view({"get": "published"}), name="article-published"),
    path("archived/", ArticleViewSet.as_view({"get": "archived"}), name="article-archived"),
    path("draft/", ArticleViewSet.as_view({"get": "draft"}), name="article-draft"),
    path("", include(router.urls)),
    path(
        "<slug:slug>/view-count/",
        ArticleViewCountView.as_view(),
        name="article-view-count",
    ),
    path(
        "<slug:slug>/clap/",
        ClapArticleView.as_view(),
        name="article-clap",
    ),
    path("responses/", include("core_apps.article_responses.urls")),
]
