from django.db import models
from django.db.models.deletion import ProtectedError


class Label(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.task_set.exists():
            raise ProtectedError(
                'Cannot delete this label because it is being used',
                self.task_set.all()
            )
        return super().delete(*args, **kwargs)
