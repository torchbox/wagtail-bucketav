import operator
from functools import reduce

from django.apps import apps
from django.db.models import Q

from .settings import bucketav_models


def get_object_for_key(file_key):
    for model_string, fields in bucketav_models().items():
        model = apps.get_model(model_string)

        filters = reduce(operator.or_, [Q(**{field: file_key}) for field in fields])
        if instance := model.objects.filter(filters).first():
            return instance
