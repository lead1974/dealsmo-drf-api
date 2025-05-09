from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from core_apps.common.admin import ContentViewInline
from core_apps.common.models import ContentView
from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "reported_by",
        "title",
        "status",
        "priority",
        "get_total_views",
    ]

    list_display_links = ["id", "reported_by"]
    list_filter = ["status", "priority"]
    search_fields = ["reported_by__email", "title", "description"]
    ordering = ["-created_at"]
    autocomplete_fields = ["reported_by"]
    inlines = [ContentViewInline]

    def get_total_views(self, obj):
        content_type = ContentType.objects.get_for_model(obj)
        return ContentView.objects.filter(
            content_type=content_type, object_id=obj.pkid
        ).count()

    get_total_views.short_description = "Total Views"