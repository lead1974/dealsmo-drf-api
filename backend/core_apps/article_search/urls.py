from django.urls import path

from .views import ArticleElasticSearchView

urlpatterns = [
    path(
        "article-search/",
        ArticleElasticSearchView.as_view({"get": "list"}),
        name="article_search",
    )
]
