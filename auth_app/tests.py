from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile

class ProfileViewTest(TestCase):
    def setUp(self):
        # Create a test user and associated profile
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile = Profile.objects.get(user=self.user)

        # Log in the test user
        self.client.login(username='testuser', password='password123')

    def test_profile_view_get(self):
        """
        Test that the profile view loads correctly with GET request.
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        self.assertContains(response, 'Profile')

    def test_profile_update_valid_data(self):
        """
        Test updating the profile with valid data.
        """
        response = self.client.post(reverse('profile'), {
            'birth_date': '1990-01-01',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful update
        self.profile.refresh_from_db()
        self.assertEqual(str(self.profile.birth_date), '1990-01-01')

    def test_profile_update_invalid_data(self):
        """
        Test updating the profile with invalid data.
        """
        response = self.client.post(reverse('profile'), {
            'birth_date': 'invalid-date',
        })
        self.assertEqual(response.status_code, 200)  # Should reload the form with errors
        self.assertFormError(response, 'profile_form', 'birth_date', 'Enter a valid date.')

    def test_profile_creation_signal(self):
        """
        Test that a profile is created automatically when a new user is created.
        """
        new_user = User.objects.create_user(username='newuser', password='password456')
        self.assertTrue(Profile.objects.filter(user=new_user).exists())
