# from django.db import models

# from task_manager.statuses.models import Status


# class Task(models.Model):
#     name = models.CharField(max_length=255,
#                             blank=False,
#                             unique=True)
#     description = models.TextField(blank=False)


#     author = models.ForeignKey(User, on_delete=models.PROTECT)
#     status = models.ForeignKey(Status, on_delete=models.PROTECT)
#     executor = models.ForeignKey(User, on_delete=models.PROTECT,
#                                  verbose_name=_('Executor'),
#                                  related_name='Executor')
#     labels = models.ManyToManyField(Label, blank=True,
#                                     verbose_name=_('Labels'))
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
