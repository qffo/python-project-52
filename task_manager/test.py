from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserRegistrationTestCase(TestCase):
    fixtures = ['task_manager/fixtures/users.json']

    def setUp(self):
        self.url = reverse('user_create')
        self.user = User.objects.create_user(
            username='ConniePerignon', password='Conpir444', email='Conpirlol@example.com')

    def test_user_create(self):
        data = {
            'username': 'testuserti',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuserti@example.com',
            'password1': 'tipitipi',
            'password2': 'tipitipi',
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        user = User.objects.filter(username='testuserti').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testuserti@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')

    def test_user_update(self):
        self.client.login(username='ConniePerignon', password='Conpir444')
        response = self.client.post(reverse('user_update', kwargs={'pk': self.user.pk}), {
            'username': 'updateConniePerignon',
            'email': 'updateduser@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateConniePerignon')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_user_delet(self):
        self.client.login(username='ConniePerignon', password='Conpir444')
        response = self.client.post(
            reverse('user_delete', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(
            username='ConniePerignon').exists())
