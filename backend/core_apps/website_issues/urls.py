from django.urls import path

from .views import (
    IssueListAPIView,
    IssueCreateAPIView,
    IssueDeleteAPIView,
    IssueUpdateAPIView,
    MyIssuesListAPIView,
    IssueDetailAPIView,
)


urlpatterns = [
    path("", IssueListAPIView.as_view(), name="issue-list"),
    path("me/", MyIssuesListAPIView.as_view(), name="my-issue-list"),
    path(
        "create/", IssueCreateAPIView.as_view(), name="create-issue"
    ),
    path("update/<uuid:id>/", IssueUpdateAPIView.as_view(), name="update-issue"),
    path("<uuid:id>/", IssueDetailAPIView.as_view(), name="issue-detail"),
    path("delete/<uuid:id>/", IssueDeleteAPIView.as_view(), name="delete-issue"),
]