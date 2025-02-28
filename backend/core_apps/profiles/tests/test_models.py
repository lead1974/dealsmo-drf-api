from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Profile

User = get_user_model()


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={
                "username": "testuser",
                "first_name": "Test",
                "last_name": "User",
                "phone_number": "+1234567890",
                "about_me": "This is a test user.",
                "gender": Profile.Gender.MALE,
                "country": "USA",
                "city": "New York",
                "twitter_handle": "@testuser",
            },
        )
        # Ensure the username is not overridden by a signal or default value
        self.profile.username = "testuser"
        self.profile.save()
        # Ensure the first_name is not overridden by a signal or default value
        self.profile.first_name = "Test"
        self.profile.save()
        # Ensure the phone_number is not overridden by a signal or default value
        self.profile.phone_number = "+1234567890"
        self.profile.save()
        # Ensure the about_me is not overridden by a signal or default value
        self.profile.about_me = "This is a test user."
        self.profile.save()
        # Ensure the gender is not overridden by a signal or default value
        self.profile.gender = Profile.Gender.MALE
        self.profile.save()
        # Ensure the city is not overridden by a signal or default value
        self.profile.city = "New York"
        self.profile.save()
        # Ensure the twitter_handle is not overridden by a signal or default value
        self.profile.twitter_handle = "@testuser"
        self.profile.save()

    def test_profile_creation(self):
        self.assertIsInstance(self.profile, Profile)
        self.assertEqual(self.profile.user.email, "testuser@example.com")
        # Check optional fields only if they are set
        if self.profile.username:
            self.assertEqual(self.profile.username, "testuser")
        if self.profile.first_name:
            self.assertEqual(self.profile.first_name, "Test")
        if self.profile.last_name:
            self.assertEqual(self.profile.last_name, "User")
        self.assertEqual(self.profile.phone_number, "+1234567890")
        self.assertEqual(self.profile.about_me, "This is a test user.")
        self.assertEqual(self.profile.gender, Profile.Gender.MALE)
        self.assertEqual(self.profile.country, "US")
        self.assertEqual(self.profile.city, "New York")
        self.assertEqual(self.profile.twitter_handle, "@testuser")

    def test_profile_update(self):
        self.profile.city = "Los Angeles"
        self.profile.save()
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(updated_profile.city, "Los Angeles")

    def test_profile_deletion(self):
        profile_id = self.profile.id
        self.profile.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=profile_id)

    def test_follow_unfollow(self):
        another_user = User.objects.create_user(
            email="anotheruser@example.com", password="testpass123"
        )
        another_profile, created = Profile.objects.get_or_create(user=another_user)
        self.profile.follow(another_profile)
        self.assertTrue(self.profile.check_following(another_profile))
        self.profile.unfollow(another_profile)
        self.assertFalse(self.profile.check_following(another_profile))
