from django.db import models

from ..models import BucketAVMixin


class Document(models.Model):
    file = models.FileField()


class DocumentWithBucketAVMixin(BucketAVMixin, models.Model):
    file = models.FileField()


class Image(models.Model):
    file = models.ImageField()


class MyModel(models.Model):
    name = models.CharField(max_length=10)
