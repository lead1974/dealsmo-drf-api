import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from core_apps.users.serializers import UserSerializer, CustomRegisterSerializer
from core_apps.profiles.models import Profile
from django.test import TestCase

User = get_user_model()


@pytest.mark.django_db
def test_user_serializer(normal_user):
    # Ensure the user has a profile
    Profile.objects.get_or_create(
        user=normal_user,
        defaults={
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+17142573835",
            "about_me": "This is a test user.",
            "gender": Profile.Gender.MALE,
            "country": "USA",
            "city": "New York",
            "twitter_handle": "@testuser",
        },
    )

    serializer = UserSerializer(normal_user)
    assert "id" in serializer.data
    assert "email" in serializer.data
    # assert "username" in serializer.data
    # assert "gender" in serializer.data
    # assert "phone_number" in serializer.data
    # assert "profile_photo" in serializer.data
    # assert "country" in serializer.data
    # assert "city" in serializer.data


@pytest.mark.django_db
def test_to_representation_normal_user(normal_user):
    serializer = UserSerializer(normal_user)
    serialized_data = serializer.data
    assert "admin" not in serialized_data


@pytest.mark.django_db
def test_to_representation_super_user(super_user):
    serializer = UserSerializer(super_user)
    serialized_data = serializer.data
    assert "admin" in serialized_data
    assert serialized_data["admin"] is True


@pytest.mark.django_db
def test_custom_register_serializer(mock_request):
    valid_data = {
        "email": "test@example.com",
        "password1": "test_password",
        "password2": "test_password",
    }
    serializer = CustomRegisterSerializer(data=valid_data)
    assert serializer.is_valid()

    user = serializer.save(mock_request)
    assert user.email == valid_data["email"]

    invalid_data = {
        "email": "test@example.com",
        "password1": "test_password",
        "password2": "wrong_password",
    }

    serializer = CustomRegisterSerializer(data=invalid_data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


class ProfileSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        self.profile_attributes = {
            "user": self.user,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+17142573835",
            "about_me": "This is a test user.",
            "gender": Profile.Gender.MALE,
            "country": "USA",
            "city": "New York",
            "twitter_handle": "@testuser",
        }
        self.profile, created = Profile.objects.get_or_create(
            user=self.user, defaults=self.profile_attributes
        )

    def test_user_serializer(self):
        # Ensure the user has a profile
        Profile.objects.get_or_create(user=self.user, defaults={"username": "testuser"})

        serializer = UserSerializer(self.user)
        assert "id" in serializer.data
        assert "email" in serializer.data
        # assert "username" in serializer.data
        # assert "first_name" in serializer.data
        # assert "last_name" in serializer.data
