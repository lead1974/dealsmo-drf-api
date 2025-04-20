from django.urls import path

from .views import ArticleElasticSearchView, DirectArticleSearchView

urlpatterns = [
    path(
        "article-search/",
        DirectArticleSearchView.as_view(),
        name="article_search",
    ),
    path(
        "legacy-article-search/",
        ArticleElasticSearchView.as_view({"get": "list"}),
        name="legacy_article_search",
    ),
]
