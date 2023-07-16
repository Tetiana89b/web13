

from django.contrib.auth.models import AbstractUser
from django.db import models
from djongo import models


class User(AbstractUser):
    
    def __str__(self):
        return self.username


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=200, unique=False)
    born_date = models.DateField(null=True, blank=True)
    born_location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Quote(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    quote = models.TextField()
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.quote



