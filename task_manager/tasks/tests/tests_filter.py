from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilterTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='Viktor1', password='Gtgt67HNnnm')
        self.user2 = User.objects.create_user(
            username='Viktor2', password='cdVFWe55HJKl')

        self.status1 = Status.objects.create(name='Ожидает')
        self.status2 = Status.objects.create(name='В процессе')

        self.label1 = Label.objects.create(name='Срочная')
        self.label2 = Label.objects.create(name='Важная')

        self.task1 = Task.objects.create(
            name='Задача 1',
            description='Описание задачи 1',
            author=self.user1,
            status=self.status1,
            executor=self.user2
        )
        self.task2 = Task.objects.create(
            name='Задача 2',
            description='Описание задачи 2',
            author=self.user1,
            status=self.status2,
            executor=self.user2
        )
        self.task3 = Task.objects.create(
            name='Задача 3',
            description='Описание задачи 3',
            author=self.user2,
            status=self.status1,
            executor=self.user1
        )
        self.task4 = Task.objects.create(
            name='Задача 4',
            description='Описание задачи 4',
            author=self.user1,
            status=self.status1,
            executor=self.user1
        )

        self.task1.labels.add(self.label1)
        self.task2.labels.add(self.label2)

    def test_filter_by_status(self):
        self.client.login(username='Viktor1', password='Gtgt67HNnnm')
        response = self.client.get(
            reverse('tasks_list') + '?status=' + str(self.status1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 4')
        self.assertContains(response, 'Задача 3')
        self.assertNotContains(response, 'Задача 2')

    def test_filter_by_executor(self):
        self.client.login(username='Viktor1', password='Gtgt67HNnnm')
        response = self.client.get(
            reverse('tasks_list') + '?executor=' + str(self.user2.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 2')
        self.assertNotContains(response, 'Задача 3')
        self.assertNotContains(response, 'Задача 4')

    def test_filter_by_label(self):
        self.client.login(username='Viktor1', password='Gtgt67HNnnm')
        response = self.client.get(
            reverse('tasks_list') + '?labels=' + str(self.label1.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertNotContains(response, 'Задача 2')
        self.assertNotContains(response, 'Задача 3')
        self.assertNotContains(response, 'Задача 4')

    def test_filter_by_author(self):
        self.client.login(username='Viktor1', password='Gtgt67HNnnm')
        # Используем фильтр only_own_tasks
        response = self.client.get(
            reverse('tasks_list') + '?only_own_tasks=True')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 2')
        self.assertNotContains(response, 'Задача 3')
        self.assertContains(response, 'Задача 4')

    def test_no_filter(self):
        self.client.login(username='Viktor1', password='Gtgt67HNnnm')
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задача 1')
        self.assertContains(response, 'Задача 2')
        self.assertContains(response, 'Задача 3')
        self.assertContains(response, 'Задача 4')
