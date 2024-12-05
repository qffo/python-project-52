from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(_('Name'), max_length=255, blank=False, unique=True)
    description = models.TextField(_('Description'), blank=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.ForeignKey(
        Status, on_delete=models.PROTECT, verbose_name=_('Status'))
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='Executor', verbose_name=_(
            'Executor'))
    labels = models.ManyToManyField(Label, blank=True, verbose_name=_('Labels'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
