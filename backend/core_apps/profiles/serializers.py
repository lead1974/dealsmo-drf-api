from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile.user.field.related_model
        fields = ["id", "email", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(source="user.email")
    full_name = serializers.SerializerMethodField(read_only=True)
    avatar = serializers.SerializerMethodField()
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "avatar",
            "phone_number",
            "gender",
            "country",
            "city",
            "twitter_handle",
            "about_me",
        ]

    def get_full_name(self, obj):
        first_name = obj.first_name.title() if obj.first_name else ""
        last_name = obj.last_name.title() if obj.last_name else ""
        return f"{first_name} {last_name}".strip()

    def get_avatar(self, obj):
        return obj.avatar.url if obj.avatar else None


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "about_me",
            "gender",
            "country",
            "city",
            "twitter_handle",
        ]


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "avatar",
            "about_me",
            "twitter_handle",
        ]
