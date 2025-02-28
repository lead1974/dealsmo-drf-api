from django.contrib.auth import get_user_model
from django.test import TestCase
from ..serializers import ProfileSerializer
from ..models import Profile
from rest_framework import serializers
from ..models import User

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name"]

    def get_username(self, obj):
        return obj.profile.username if hasattr(obj, "profile") else None

    def get_first_name(self, obj):
        return obj.profile.first_name if hasattr(obj, "profile") else None

    def get_last_name(self, obj):
        return obj.profile.last_name if hasattr(obj, "profile") else None


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
        self.serializer_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "phone_number": "+17142573835",
            "gender": "M",
            "country": "US",
            "city": "New York",
            "twitter_handle": "@testuser",
            "about_me": "This is a test user.",
        }
        self.profile, created = Profile.objects.get_or_create(
            user=self.user, defaults=self.profile_attributes
        )
        self.serializer = ProfileSerializer(instance=self.profile)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        expected_fields = set(self.serializer_data.keys()).union(
            {"profile_photo", "full_name", "id"}
        )
        self.assertEqual(set(data.keys()), expected_fields)

    def test_profile_serialization(self):
        data = self.serializer.data
        self.assertEqual(data["username"], self.profile.username)
        self.assertEqual(data["first_name"], self.profile.first_name)
        self.assertEqual(data["last_name"], self.profile.last_name)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["phone_number"], self.profile.phone_number)
        self.assertEqual(data["gender"], self.profile.gender)
        self.assertEqual(data["country"], self.profile.country.name)
        self.assertEqual(data["city"], self.profile.city)
        self.assertEqual(data["twitter_handle"], self.profile.twitter_handle)
        self.assertEqual(data["about_me"], self.profile.about_me)

    def test_profile_deserialization(self):
        # Ensure serializer data includes all required fields
        serializer_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "phone_number": "+17142573835",  # Ensure this format is valid
            "gender": "M",
            "country": "US",
            "city": "New York",
            "twitter_handle": "@testuser",
            "about_me": "This is a test user.",
        }
        serializer = ProfileSerializer(data=serializer_data)
        if not serializer.is_valid():
            print(serializer.errors)
        self.assertTrue(serializer.is_valid())
        # Check optional fields only if they are set
        if "username" in serializer_data:
            self.assertEqual(
                serializer.validated_data["username"], serializer_data["username"]
            )
        if "first_name" in serializer_data:
            self.assertEqual(
                serializer.validated_data["first_name"], serializer_data["first_name"]
            )
        if "last_name" in serializer_data:
            self.assertEqual(
                serializer.validated_data["last_name"], serializer_data["last_name"]
            )
        self.assertEqual(
            serializer.validated_data["phone_number"], serializer_data["phone_number"]
        )
        self.assertEqual(serializer.validated_data["gender"], serializer_data["gender"])
        self.assertEqual(
            serializer.validated_data["country"], serializer_data["country"]
        )
        self.assertEqual(serializer.validated_data["city"], serializer_data["city"])
        self.assertEqual(
            serializer.validated_data["twitter_handle"],
            serializer_data["twitter_handle"],
        )
        self.assertEqual(
            serializer.validated_data["about_me"], serializer_data["about_me"]
        )

    def test_user_serializer(self):
        # Ensure the user has a profile
        Profile.objects.get_or_create(user=self.user, defaults={"username": "testuser"})

        serializer = UserSerializer(self.user)
        assert "id" in serializer.data
        assert "email" in serializer.data
        assert "username" in serializer.data
        assert "first_name" in serializer.data
        assert "last_name" in serializer.data
