from django.urls import path

from .views import BookmarkCreateView, BookmarkDestroyView

urlpatterns = [
    path(
        "create/<uuid:article_id>/",
        BookmarkCreateView.as_view(),
        name="create_article_bookmark",
    ),
    path(
        "delete/<uuid:article_id>/",
        BookmarkDestroyView.as_view(),
        name="delete_article_bookmark",
    ),
]
