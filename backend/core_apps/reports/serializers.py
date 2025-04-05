from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Report

User = get_user_model()


class ReportSerializer(serializers.ModelSerializer):
    reported_user_email = serializers.EmailField(write_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Report
        fields = ["id", "title", "description", "reported_user_email", "status", "created_at"]

    def validate_reported_user_email(self, value: str) -> str:
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("The provided email does not exist")
        return value

    def create(self, validated_data: dict) -> Report:
        reported_user_email = validated_data.pop("reported_user_email")

        try:
            reported_user = User.objects.get(email=reported_user_email)
        except User.DoesNotExist as e:
            raise serializers.ValidationError(
                "The user with that email does not exist."
            ) from e

        return Report.objects.create(
            reported_user=reported_user,
            status=Report.Status.OPEN,
            **validated_data
        )


class ReportStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["status"]

    def validate_status(self, value: str) -> str:
        if value not in Report.Status.values:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {', '.join(Report.Status.values)}"
            )
        return value