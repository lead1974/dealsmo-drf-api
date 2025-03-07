from django.urls import path
from .views import (
    GoogleLoginView, 
    GithubLoginView, 
    FacebookLoginView,
    GoogleAuthRedirectView,
    GoogleCallbackView
)

app_name = 'social_auth'

urlpatterns = [
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('google/auth/', GoogleAuthRedirectView.as_view(), name='google_auth'),
    path('google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('github/', GithubLoginView.as_view(), name='github_login'),
    path('facebook/', FacebookLoginView.as_view(), name='facebook_login'),
]