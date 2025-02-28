from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from ..models import Profile

User = get_user_model()

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        # Ensure only one profile per user
        self.profile, created = Profile.objects.get_or_create(
            user=self.user,
            defaults={
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User',
                'phone_number': '+1234567890',
                'about_me': 'This is a test user.',
                'gender': Profile.Gender.MALE,
                'country': 'USA',
                'city': 'New York',
                'twitter_handle': '@testuser'
            }
        )

    def test_get_profiles(self):
        response = self.client.get(reverse('all-profiles'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to test response data

    def test_get_profile_detail(self):
        response = self.client.get(reverse('my-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to test response data

    def test_update_profile(self):
        response = self.client.patch(reverse('update-profile'), {
            'city': 'Los Angeles'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.city, 'Los Angeles')

    def test_follow_user(self):
        another_user = User.objects.create_user(
            email='anotheruser@example.com',
            password='testpass123'
        )
        another_profile, created = Profile.objects.get_or_create(user=another_user)
        self.profile.follow(another_profile)
        self.assertTrue(self.profile.check_following(another_profile))

    def test_unfollow_user(self):
        another_user = User.objects.create_user(
            email='anotheruser@example.com',
            password='testpass123'
        )
        another_profile, created = Profile.objects.get_or_create(user=another_user)
        self.profile.follow(another_profile)
        self.profile.unfollow(another_profile)
        self.assertFalse(self.profile.check_following(another_profile))

    def test_create_profile(self):
        # Check if the endpoint supports profile creation
        response = self.client.post(reverse('all-profiles'), {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'phone_number': '+1234567890',
            'gender': 'M',
            'country': 'USA',
            'city': 'Los Angeles',
            'twitter_handle': '@newuser',
            'about_me': 'This is a new user.'
        })
        # If the endpoint does not support creation, adjust the expected status code
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_405_METHOD_NOT_ALLOWED])
        # Add more assertions to test response data if creation is supported

    def test_delete_profile(self):
        # Test deleting a profile
        pass 