from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.views import User


class TaskCRUDTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='Viktor', password='ghcv67Er')
        self.executor = User.objects.create_user(
            username='Viktor_ex', password='ghcv67Erex')
        self.status = Status.objects.create(name="New")
        self.client.login(username='Viktor', password='ghcv67Er')
        self.label = Label.objects.create(name="Urgent")

    def test_create_task(self):
        url = reverse('task_create')
        data = {
            'name': 'Test Task',
            'description': 'Task Description',
            'status': self.status.id,
            'executor': self.executor.id,
        }

        before_count = Task.objects.count()

        response = self.client.post(url, data)

        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count + 1)

        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.first()

        self.assertEqual(task.name, data['name'])
        self.assertEqual(task.description, data['description'])
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.executor, self.executor)

        task.labels.set([self.label.id])

        self.assertTrue(task.labels.filter(id=self.label.id).exists())

    def test_task_info(self):
        task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            author=self.user,
            status=self.status,
            executor=self.executor
        )
        url = reverse('task_info', args=[task.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.name)
        self.assertContains(response, task.description)

    def test_update_task(self):
        task = Task.objects.create(
            name="Old Task",
            description="Old Description",
            author=self.user,
            status=self.status,
            executor=self.executor
        )
        url = reverse('task_update', args=[task.pk])
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.executor.id,
            'labels': [self.label.id],
        }

        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('tasks_list'))

        task.refresh_from_db()
        self.assertEqual(task.name, data['name'])
        self.assertEqual(task.description, data['description'])

        self.assertIn(self.label, task.labels.all())

    def test_delete_task(self):
        task = Task.objects.create(
            name="Task to Delete",
            description="Task to Delete Description",
            author=self.user,
            status=self.status,
            executor=self.executor
        )

        before_count = Task.objects.count()

        url = reverse('task_delete', args=[task.pk])

        response = self.client.post(url)

        after_count = Task.objects.count()
        self.assertEqual(after_count, before_count - 1)

        self.assertRedirects(response, reverse('tasks_list'))

        with self.assertRaises(Task.DoesNotExist):
            task.refresh_from_db()

    def test_delete_task_permission(self):
        another_user = User.objects.create_user(
            username='user2', password='debg55juk')
        task = Task.objects.create(
            name="Task to Delete",
            description="Task to Delete Description",
            author=self.user,
            status=self.status,
            executor=self.executor
        )
        self.assertTrue(another_user.is_authenticated)
        self.client.login(username='user2', password='debg55juk')
        url = reverse('task_delete', args=[task.pk])
        response = self.client.post(url)
        self.assertRedirects(response, reverse('tasks_list'))
        self.assertEqual(len(Task.objects.all()), 1)
