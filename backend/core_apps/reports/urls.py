from django.urls import path
from .views import (
    ReportCreateAPIView,
    ReportListAPIView,
    AdminReportListAPIView,
    ReportStatusUpdateAPIView,
)

urlpatterns = [
    path("create/", ReportCreateAPIView.as_view(), name="create-report"),
    path("me/", ReportListAPIView.as_view(), name="my-reports"),
    path("all/", AdminReportListAPIView.as_view(), name="all-reports"),
    path("<uuid:id>/status/", ReportStatusUpdateAPIView.as_view(), name="update-report-status"),
]