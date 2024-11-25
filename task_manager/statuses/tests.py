from django.urls import reverse
from ..users.views import User
from django.test import TestCase
from task_manager.statuses.models import Status


class StatusTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='Viktor', password='frgt66hy')
        cls.status = Status.objects.create(name="Test_Status")

    def test_status_list_authenticated(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('status_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.status.name)

    def test_status_list_unauthenticated(self):
        url = reverse('status_list')
        response = self.client.get(url)

        self.assertRedirects(response, '/login/')

    def test_status_create(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('status_create')
        data = {'name': 'New_Status'}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('status_list'))
        self.assertTrue(Status.objects.filter(name='New_Status').exists())

    def test_status_create_unauthenticated(self):
        url = reverse('status_create')
        response = self.client.get(url)

        self.assertRedirects(response, '/login/?next=/statuses/create/')

    def test_status_update(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('status_update', kwargs={'pk': self.status.pk})
        data = {'name': 'Updated Status'}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('status_list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_status_update_unauthenticated(self):
        url = reverse('status_update', kwargs={'pk': self.status.pk})
        response = self.client.get(url)

        self.assertRedirects(
            response, f'/login/?next=/statuses/{self.status.pk}/update/')

    def test_status_delete(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('status_delete', kwargs={'pk': self.status.pk})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('status_list'))
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_status_delete_unauthenticated(self):
        url = reverse('status_delete', kwargs={'pk': self.status.pk})
        response = self.client.get(url)

        self.assertRedirects(
            response, f'/login/?next=/statuses/{self.status.pk}/delete/')

    def test_status_create_page(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('status_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Создать статус')
