from rest_framework import generics
from rest_framework import serializers
from rest_framework.permissions import IsAdminUser
from .models import Report
from .serializers import ReportSerializer, ReportStatusUpdateSerializer
from ..common.renderers import GenericJSONRenderer


class ReportCreateAPIView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "report"

    def perform_create(self, serializer: serializers.Serializer) -> None:
        serializer.save(reported_by=self.request.user)


class ReportListAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer
    renderer_classes = [GenericJSONRenderer]
    object_label = "reports"

    def get_queryset(self) -> Report:
        user = self.request.user
        return Report.objects.filter(reported_by=user)


class AdminReportListAPIView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [IsAdminUser]
    object_label = "reports"


class ReportStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportStatusUpdateSerializer
    renderer_classes = [GenericJSONRenderer]
    permission_classes = [IsAdminUser]
    object_label = "report"
    http_method_names = ["patch"]
    lookup_field = "id"
    lookup_url_kwarg = "id"