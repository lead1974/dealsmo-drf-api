from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, ArticleViewCountView, ClapArticleView, ArticleCategoryViewSet

router = DefaultRouter()
router.register(r"", ArticleViewSet, basename="article")
router.register(r"article-categories", ArticleCategoryViewSet, basename="article-category")

urlpatterns = [
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
