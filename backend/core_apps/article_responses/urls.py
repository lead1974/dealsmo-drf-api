from django.urls import path

from .views import ArticleResponseListCreateView, ArticleResponseUpdateDeleteView

urlpatterns = [
    path(
        "article/<slug:slug>/",
        ArticleResponseListCreateView.as_view(),
        name="responses",
    ),
    path(
        "<uuid:id>/", ArticleResponseUpdateDeleteView.as_view(), name="response_detail"
    ),
]
