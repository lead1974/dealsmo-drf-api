from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from social_core.backends.google import GoogleOAuth2
from social_core.backends.github import GithubOAuth2
from social_core.backends.facebook import FacebookOAuth2
from social_django.utils import load_strategy, load_backend
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
import requests
import logging
import uuid

logger = logging.getLogger(__name__)
User = get_user_model()

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoogleAuthRedirectView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        redirect_uri = settings.GOOGLE_OAUTH_CALLBACK_URL
        auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile&access_type=offline'
        logger.info(f"Redirecting to Google with redirect_uri: {redirect_uri}")
        return Response({'authorization_url': auth_url})

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GoogleCallbackView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        code = request.GET.get('code')
        if not code:
            logger.error("No code provided in callback")
            return Response({'error': 'No code provided'}, status=status.HTTP_400_BAD_REQUEST)

        redirect_uri = settings.GOOGLE_OAUTH_CALLBACK_URL
        logger.info(f"Exchanging code for token with redirect_uri: {redirect_uri}")

        # Exchange code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        data = {
            'code': code,
            'client_id': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            'client_secret': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, data=data)
        if response.status_code != 200:
            logger.error(f"Failed to get access token. Status: {response.status_code}, Response: {response.text}")
            return Response({
                'error': 'Failed to get access token',
                'details': response.text
            }, status=status.HTTP_400_BAD_REQUEST)

        tokens = response.json()
        return Response({
            'access_token': tokens.get('access_token'),
            'id_token': tokens.get('id_token'),
            'expires_in': tokens.get('expires_in')
        })

@method_decorator(ensure_csrf_cookie, name='dispatch')
class SocialAuthView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        auth_token = request.data.get('auth_token', None)
        if not auth_token:
            logger.error("No auth token provided in request")
            return Response({'error': 'No auth token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get user info from Google
            user_info_response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            
            if user_info_response.status_code != 200:
                logger.error(f"Failed to get user info from Google. Status: {user_info_response.status_code}")
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

            user_info = user_info_response.json()
            email = user_info.get('email')
            
            if not email:
                return Response({'error': 'Email not provided by Google'}, status=status.HTTP_400_BAD_REQUEST)

            # Try to get existing user or create a new one
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user with a random password
                random_password = str(uuid.uuid4())
                user = User.objects.create_user(
                    email=email,
                    password=random_password,  # This password will never be used for login
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error during social auth: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(SocialAuthView):
    backend_class = GoogleOAuth2

class GithubLoginView(SocialAuthView):
    backend_class = GithubOAuth2

class FacebookLoginView(SocialAuthView):
    backend_class = FacebookOAuth2