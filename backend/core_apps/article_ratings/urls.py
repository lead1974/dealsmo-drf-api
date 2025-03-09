from django.urls import path

from .views import RatingCreateView

urlpatterns = [
    path(
        "create/<uuid:article_id>/",
        RatingCreateView.as_view(),
        name="create_article_rating",
    )
]
