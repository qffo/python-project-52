from django.test import TestCase
from django.urls import reverse

from .views import User


class UserRegistrationTestCase(TestCase):
    fixtures = ['task_manager/fixtures/users.json']

    def setUp(self):
        self.url = reverse('user_create')
        self.user = User.objects.create_user(
            username='Viktor',
            password='gthn56FeWQ',
        )

    def test_user_create(self):
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'testuserti',
            'password1': 'tipitipi',
            'password2': 'tipitipi',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.filter(username='testuserti').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_user_update(self):
        self.client.login(username='Viktor', password='gthn56FeWQ')
        response = self.client.post(
            reverse('user_update', kwargs={'pk': self.user.pk}), {
                'first_name': 'UpdatedFirstName',
                'last_name': 'UpdatedLastName',
                'username': 'updateViktor',
                'password1': 'tipitipi',
                'password2': 'tipitipi',
            })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedFirstName')
        self.assertEqual(self.user.last_name, 'UpdatedLastName')
        self.assertEqual(self.user.username, 'updateViktor')

    def test_user_delet(self):
        self.client.login(username='Viktor', password='gthn56FeWQ')
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(
            username='Viktor').exists())
