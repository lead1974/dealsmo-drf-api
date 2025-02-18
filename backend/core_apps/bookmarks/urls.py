from django.urls import path
from .views import BookmarkCreateView, BookmarkDestroyView

urlpatterns = [
    path(
        "bookmark_article/<uuid:article_id>/",
        BookmarkCreateView.as_view(),
        name="bookmark_article",
    ),
    path(
        "unbookmark_article/<uuid:article_id>/",
        BookmarkDestroyView.as_view(),
        name="unbookmark_article",
    ),
]