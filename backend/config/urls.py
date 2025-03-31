from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import permissions

from core_apps.users.views import CustomUserDetailsView, CustomRegisterView

schema_view = get_schema_view(
    openapi.Info(
        title="DealsMo.com API",
        default_version="v1",
        description="API endpoints for DealsMo.com API",
        contact=openapi.Contact(email="email2lead@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/user/", CustomUserDetailsView.as_view(), name="user_details"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/register/", CustomRegisterView.as_view(), name="rest_register"),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path('api/v1/auth/social/', include('core_apps.social_auth.urls')),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    path("api/v1/website-issues/", include("core_apps.website_issues.urls")),
    path("api/v1/articles/", include("core_apps.articles.urls")),
    path("api/v1/article-ratings/", include("core_apps.article_ratings.urls")),
    path("api/v1/article-bookmarks/", include("core_apps.article_bookmarks.urls")),
    path("api/v1/elastic/", include("core_apps.article_search.urls")),
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

admin.site.site_header = "DealsMo.com API Admin"
admin.site.site_title = "DealsMo.com API Admin Portal"
admin.site.index_title = "Welcome to DealsMo.com API Portal"
