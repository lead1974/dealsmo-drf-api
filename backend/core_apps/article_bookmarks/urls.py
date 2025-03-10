from django.urls import path

from .views import BookmarkCreateView, BookmarkDestroyView

urlpatterns = [
    path(
        "create/<slug:slug>/",
        BookmarkCreateView.as_view(),
        name="create_article_bookmark",
    ),
    path(
        "delete/<slug:slug>/",
        BookmarkDestroyView.as_view(),
        name="delete_article_bookmark",
    ),
]
