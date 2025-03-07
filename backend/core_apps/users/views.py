from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from dj_rest_auth.views import UserDetailsView

from .serializers import UserSerializer, CustomRegisterSerializer

User = get_user_model()

class CustomUserDetailsView(UserDetailsView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_data = {
            'user': UserSerializer(user).data,
            'message': 'User registered successfully'
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
