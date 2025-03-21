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
from core_apps.profiles.models import Profile
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
        scopes = [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid',
            'profile',
            'email'
        ]
        auth_url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={" ".join(scopes)}&access_type=offline'
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

class SocialAuthView(APIView):
    permission_classes = (AllowAny,)
    provider = None  # Will be set by child classes

    def get_user_info(self, auth_token):
        """Get user info from different social providers"""
        if self.provider == 'google':
            response = requests.get(
                'https://www.googleapis.com/oauth2/v3/userinfo',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            logger.info(f"Google API Response Status: {response.status_code}")
            logger.info(f"Google API Response Headers: {response.headers}")
            logger.info(f"Google API Response Text: {response.text}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    logger.info(f"Google user info response: {data}")
                    # Log each field individually to see what we're getting
                    logger.info(f"Email from Google: {data.get('email')}")
                    logger.info(f"Given name from Google: {data.get('given_name')}")
                    logger.info(f"Family name from Google: {data.get('family_name')}")
                    logger.info(f"Name from Google: {data.get('name')}")
                    
                    # Try to get name from the 'name' field if given_name and family_name are not available
                    full_name = data.get('name', '').split(' ', 1)
                    first_name = data.get('given_name', full_name[0] if full_name else '')
                    last_name = data.get('family_name', full_name[1] if len(full_name) > 1 else '')
                    
                    return {
                        'email': data.get('email'),
                        'first_name': first_name,
                        'last_name': last_name,
                    }
                except Exception as e:
                    logger.error(f"Error parsing Google response: {str(e)}")
                    return None
            else:
                logger.error(f"Google API error: {response.text}")
                return None
        
        elif self.provider == 'github':
            response = requests.get(
                'https://api.github.com/user',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            if response.status_code == 200:
                data = response.json()
                # GitHub provides name as a single field, we'll split it
                full_name = data.get('name', '').split(' ', 1)
                return {
                    'email': data.get('email'),
                    'first_name': full_name[0] if full_name else '',
                    'last_name': full_name[1] if len(full_name) > 1 else '',
                }
        
        elif self.provider == 'facebook':
            response = requests.get(
                'https://graph.facebook.com/me',
                params={
                    'fields': 'email,first_name,last_name',
                    'access_token': auth_token
                }
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'email': data.get('email'),
                    'first_name': data.get('first_name', ''),
                    'last_name': data.get('last_name', ''),
                }
        
        elif self.provider == 'microsoft':
            response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    'email': data.get('userPrincipalName'),
                    'first_name': data.get('givenName', ''),
                    'last_name': data.get('surname', ''),
                }

        elif self.provider == 'instagram':
            # Instagram Basic Display API
            response = requests.get(
                'https://graph.instagram.com/me',
                params={
                    'fields': 'id,username,account_type,media_count',
                    'access_token': auth_token
                }
            )
            if response.status_code == 200:
                data = response.json()
                # Instagram doesn't provide email by default, we'll use username@instagram.com
                return {
                    'email': f"{data.get('username')}@instagram.com",
                    'first_name': data.get('username', ''),  # Instagram doesn't provide real name
                    'last_name': '',  # Instagram doesn't provide last name
                }

        elif self.provider == 'tiktok':
            response = requests.get(
                'https://open-api.tiktok.com/oauth/userinfo/',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            if response.status_code == 200:
                data = response.json()
                # TikTok provides display name, we'll split it
                display_name = data.get('display_name', '').split(' ', 1)
                return {
                    'email': f"{data.get('open_id')}@tiktok.com",  # TikTok doesn't provide email
                    'first_name': display_name[0] if display_name else '',
                    'last_name': display_name[1] if len(display_name) > 1 else '',
                }
        
        return None

    def post(self, request, *args, **kwargs):
        auth_token = request.data.get('auth_token', None)
        if not auth_token:
            logger.error("No auth token provided in request")
            return Response({'error': 'No auth token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get user info from the appropriate provider
            user_info = self.get_user_info(auth_token)
            if not user_info:
                logger.error(f"Failed to get user info from {self.provider}")
                return Response({'error': f'Failed to get user info from {self.provider}'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            email = user_info.get('email')
            first_name = user_info.get('first_name', '')
            last_name = user_info.get('last_name', '')
            
            logger.info(f"User info from {self.provider}: email={email}, first_name={first_name}, last_name={last_name}")
            
            if not email:
                return Response({'error': f'Email not provided by {self.provider}'}, 
                              status=status.HTTP_400_BAD_REQUEST)

            # Try to get existing user or create a new one
            try:
                user = User.objects.get(email=email)
                logger.info(f"Found existing user: {user.email}")
                # Update profile if user exists
                profile = user.profile
                if first_name and not profile.first_name:  # Only update if empty
                    logger.info(f"Updating first name from {profile.first_name} to {first_name}")
                    profile.first_name = first_name
                if last_name and not profile.last_name:  # Only update if empty
                    logger.info(f"Updating last name from {profile.last_name} to {last_name}")
                    profile.last_name = last_name
                profile.save()
            except User.DoesNotExist:
                logger.info(f"Creating new user with email: {email}")
                # Create a new user with a random password
                random_password = str(uuid.uuid4())
                user = User.objects.create_user(
                    email=email,
                    password=random_password,  # This password will never be used for login
                )
                # The profile will be created by the signal
                # Get the profile after it's created by the signal
                profile = user.profile
                if first_name:
                    logger.info(f"Setting first name to: {first_name}")
                    profile.first_name = first_name
                if last_name:
                    logger.info(f"Setting last name to: {last_name}")
                    profile.last_name = last_name
                profile.save()

            # Make sure we fetch the latest profile data
            profile.refresh_from_db()
            logger.info(f"Final profile data: first_name={profile.first_name}, last_name={profile.last_name}")

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'email': user.email,
                    'first_name': profile.first_name or '',  # Ensure we don't return None
                    'last_name': profile.last_name or '',    # Ensure we don't return None
                }
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error during {self.provider} auth: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(SocialAuthView):
    provider = 'google'

class GithubLoginView(SocialAuthView):
    provider = 'github'

class FacebookLoginView(SocialAuthView):
    provider = 'facebook'

class MicrosoftLoginView(SocialAuthView):
    provider = 'microsoft'

class InstagramLoginView(SocialAuthView):
    provider = 'instagram'

class TikTokLoginView(SocialAuthView):
    provider = 'tiktok'