from django.db import models

# Create your models here.
from django.contrib.postgres.fields import ArrayField

class Context(models.Model):
    srs_name = models.CharField(max_length=500,blank= True)
    entities = ArrayField(models.CharField(max_length=255), default=list)

class UseCase(models.Model):
    actor = models.CharField(max_length=50)
    action = models.CharField(max_length=50)
    fields = ArrayField(models.CharField(max_length=255), default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def add_fields(self, *new_fields):
        for index, field in enumerate(new_fields):
            self.fields.insert(index, field)

    def __str__(self):
        return f'{self.actor} {self.action} {self.fields}'
    
from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='diagrams')

class PDFReport(models.Model):
    objective = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    overview = models.TextField()
    context_diagrams = models.ManyToManyField(UploadedImage, related_name='related_context_reports')
    use_case_diagrams = models.ManyToManyField(UploadedImage, related_name='related_use_case_reports')

    def __str__(self):
        return self.objective
