from django.urls import path

from .views import RatingCreateView

urlpatterns = [
    path(
        "create/<slug:slug>/",
        RatingCreateView.as_view(),
        name="create_article_rating",
    )
]
