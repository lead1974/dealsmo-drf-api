import pytest
from django.contrib.auth import get_user_model
from rest_framework import serializers
from core_apps.profiles.models import Profile

User = get_user_model()


@pytest.mark.django_db
def test_create_normal_user(normal_user):
    assert normal_user.email is not None
    assert normal_user.password is not None
    assert normal_user.pkid is not None
    assert not normal_user.is_staff
    assert not normal_user.is_superuser
    assert normal_user.is_active


@pytest.mark.django_db
def test_create_superuser(super_user):
    assert super_user.email is not None
    assert super_user.password is not None
    assert super_user.pkid is not None
    assert super_user.is_staff
    assert super_user.is_superuser
    assert super_user.is_active


@pytest.mark.django_db
def test_delete_user(normal_user):
    user_pk = normal_user.pk
    normal_user.delete()

    with pytest.raises(User.DoesNotExist):
        User.objects.get(pk=user_pk)


@pytest.mark.django_db
def test_normal_user_email_is_normalized(normal_user):
    email = normal_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_super_user_email_is_normalized(super_user):
    email = super_user.email
    assert email == email.lower()


@pytest.mark.django_db
def test_user_email_incorrect(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email="realestate.com")


@pytest.mark.django_db
def test_create_user_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "Users must have an email address."


@pytest.mark.django_db
def test_create_superuser_with_no_email(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superuser must have an email address."


@pytest.mark.django_db
def test_create_superuser_with_no_password(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(password=None, is_superuser=True, is_staff=True)
    assert str(err.value) == "Superuser must have a password."


@pytest.mark.django_db
def test_super_user_is_not_staff(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=True, is_staff=False)
    assert str(err.value) == "Superuser must have is_staff=True."


@pytest.mark.django_db
def test_super_user_is_not_superuser(user_factory):
    with pytest.raises(ValueError) as err:
        user_factory.create(is_superuser=False, is_staff=True)
    assert str(err.value) == "Superuser must have is_superuser=True."


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
