import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User

@pytest.mark.django_db
class TestUserAuthAPI:
    def setup_method(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'username': 'teststaff',
            'password': 'strongpassword123',
            'email': 'test@example.com'
        }

    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data)
        assert response.status_code == 201
        assert response.data['username'] == self.user_data['username']
        assert 'password' not in response.data

        # Verify user is staff
        user = User.objects.get(username=self.user_data['username'])
        assert user.is_staff is True

    def test_user_login(self):
        # Create user
        User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'],
            is_staff=True
        )

        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data)
        
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
