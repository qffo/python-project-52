from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.users.views import User


class LabelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='Viktor', password='frgt66hy')
        cls.label = Label.objects.create(name="Test_Label")

    def test_label_list_authenticated(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('labels_list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.label.name)

    def test_label_list_unauthenticated(self):
        url = reverse('labels_list')
        response = self.client.get(url)

        self.assertRedirects(response, '/login/')

    def test_label_create(self):
        self.client.login(username='Viktor', password='frgt66hy')

        before_count = Label.objects.count()

        url = reverse('labels_create')
        data = {'name': 'New_Label'}
        response = self.client.post(url, data)

        after_count = Label.objects.count()
        self.assertEqual(after_count, before_count + 1)

        self.assertRedirects(response, reverse('labels_list'))
        self.assertTrue(Label.objects.filter(name='New_Label').exists())

    def test_label_create_unauthenticated(self):
        url = reverse('labels_create')
        response = self.client.get(url)

        self.assertRedirects(response, '/login/?next=/labels/create/')

    def test_label_update(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('labels_update', kwargs={'pk': self.label.pk})
        data = {'name': 'Updated Label'}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('labels_list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

    def test_label_update_unauthenticated(self):
        url = reverse('labels_update', kwargs={'pk': self.label.pk})
        response = self.client.get(url)

        self.assertRedirects(
            response, f'/login/?next=/labels/{self.label.pk}/update/')

    def test_label_delete(self):
        self.client.login(username='Viktor', password='frgt66hy')

        before_count = Label.objects.count()

        url = reverse('labels_delete', kwargs={'pk': self.label.pk})
        response = self.client.post(url)

        after_count = Label.objects.count()
        self.assertEqual(after_count, before_count - 1)

        self.assertRedirects(response, reverse('labels_list'))
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_unauthenticated(self):
        url = reverse('labels_delete', kwargs={'pk': self.label.pk})
        response = self.client.get(url)

        self.assertRedirects(
            response, f'/login/?next=/labels/{self.label.pk}/delete/')

    def test_label_create_page(self):
        self.client.login(username='Viktor', password='frgt66hy')

        url = reverse('labels_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Создать метку')
