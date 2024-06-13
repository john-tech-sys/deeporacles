from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class UsersListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_users_list_authenticated(self):
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'your_template.html')

    def test_users_list_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('users_list'))
        self.assertRedirects(response, '/login/?next=/path/to/users_list/')
