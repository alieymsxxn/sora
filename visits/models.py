from django.db import models

# Create your models here.
class PageVisits(models.Model):
    path = models.fields.TextField(blank=True, null=True)
    timestamp = models.fields.DateTimeField(auto_now_add=True)
    