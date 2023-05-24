from django.db import models

# Create your models here.
from django.contrib.postgres.fields import ArrayField

class Context(models.Model):
    srs_name = models.CharField(max_length=500,blank= True)
    entities = ArrayField(models.CharField(max_length=50), blank=True,default=[])

class UseCase(models.Model):
    actor = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    fields = ArrayField(models.CharField(max_length=50), blank=True,default=[])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.actor} {self.action} {self.fields}'