import logging

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework import serializers

from core_apps.common.models import ContentView
from .emails import send_resolution_email
from .models import Issue

logger = logging.getLogger(__name__)


class IssueSerializer(serializers.ModelSerializer):
    reported_by = serializers.ReadOnlyField(source="reported_by.email")
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = [
            "id",
            "reported_by",
            "title",
            "description",
            "status",
            "priority",
            "view_count",
        ]

    def get_view_count(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()


class IssueStatusUpdateSerializer(serializers.ModelSerializer):
    reported_by = serializers.ReadOnlyField(source="reported_by.email")

    class Meta:
        model = Issue
        fields = [
            "title",
            "description",
            "reported_by",
            "status",
            "resolved_on",
        ]

    def update(self, instance: Issue, validated_data: dict) -> Issue:
        if (
            validated_data.get("status") == Issue.IssueStatus.RESOLVED
            and instance.status != Issue.IssueStatus.RESOLVED
        ):
            instance.resolved_on = timezone.now().date()
            instance.save()
            send_resolution_email(instance)
        return super().update(instance, validated_data)