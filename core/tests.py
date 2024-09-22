from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_account_url = reverse('create')
        self.login_url = reverse('main')
        self.home_url = reverse('home')
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'gender': 'Male',
            'mobile_number': '1234567890',
            'date_of_birth': '2000-01-01',
        }

    def test_create_view(self):
        response = self.client.post(self.create_account_url, self.user_data, format='text/html')
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(User.objects.filter(username='testuser').exists())  
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())  

    def test_main_view(self):
        User.objects.create_user(**self.user_data)

        response = self.client.post(self.login_url, {'username': 'testuser', 'password': 'testpassword'}, format='text/html')
        self.assertEqual(response.status_code, 302)  
