from django.db import models

from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
    description = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='Executor')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
