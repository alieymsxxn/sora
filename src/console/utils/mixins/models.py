from django.db import models

class TimeAuditMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class PriorityMixin(models.Model):
    order = models.IntegerField(default=-1)
    featured = models.BooleanField(default=False)

    class Meta:
        abstract = True