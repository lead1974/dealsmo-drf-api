from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    def is_email_verified(self, obj):
        try:
            email_address = EmailAddress.objects.get(user=obj)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return False
    is_email_verified.boolean = True
    is_email_verified.short_description = "Email Verified"

    list_display = [
        "pkid",
        "id",
        "email",
        "is_email_verified",
        "is_staff",
        "is_active",
    ]

    list_display_links = ["pkid", "id", "email"]

    list_filter = ["email", "is_staff", "is_active"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ["email"]


admin.site.register(User, UserAdmin)
