from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class Content(models.Model):
    title =  models.CharField(max_length=100)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=120)
    created_at = models.DateTimeField('Date published ', auto_now_add=True)
    def __str__(self):
        return self.title
    
    