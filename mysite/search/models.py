from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50, null=True)
    number = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null=True)
    publisher = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    