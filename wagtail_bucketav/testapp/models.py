from django.db import models


class Document(models.Model):
    file = models.FileField()


class Image(models.Model):
    file = models.ImageField()


class MyModel(models.Model):
    name = models.CharField(max_length=10)
