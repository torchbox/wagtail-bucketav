# django-bucketav

Scan Django uploads using [BucketAV](https://bucketav.com/).

## Synopsis

#### Base setup

```sh
(.venv) $ pip install django-bucketav
# Or, with Poetry:
(.venv) $ poetry add django-bucketav
```

The `DJANGO_BUCKETAV_MODELS` Django setting is used to configure which FileFields of which Django models
this package should handle:
```python
# settings.py

DJANGO_BUCKETAV_MODELS = {
    "myapp.Document": ["file", "fallback_for_other_countries"],
    "myapp.Image": ["image"],
}
```

```python
# urls.py

from django.urls import include, path

urlpatterns = [
    path("bucketav/", include("django_bucketav.urls")),
]

```

With such an example setup, when BucketAV will ping the Django app on the
`/bucketav/sns-hook/` URL path with the result of an antivirus scan it will look
for the given file path in the `file` and `fallback_for_other_countries` fields
of the Document model, as well as the `image` field of the Image model.

If it finds such a reference, it will send a `scan_result_received` Django signal that your code is free to handle,
following [the usual Django signals machinery](https://docs.djangoproject.com/en/5.0/topics/signals/) :
```python
# myapp/signal_handlers.py

from django.utils import timezone
from django_bucketav.models import FileScanStatus

from .models import Document

def update_scan_status_for_instance(
    sender, instance: Document, file_scan_status: FileScanStatus, **kwargs
):
    instance.scan_status = file_scan_status
    instance.last_scanned_at = timezone.now()
    instance.save()
```

#### The (optional) BucketAVMixin class

A `BucketAVMixin` model mixin is provided for convenience, that makes it even easier: any Django model
that is referenced in the `DJANGO_BUCKETAV_MODELS` Django setting and that extends this class `bucketav_last_scanned_at` fields, and they
will get a `bucketav_scan_status` and a `bucketav_last_scanned_at` fields, and they
will automatically be updated every time a ping from BucketAV is received for a file
that is managed by such a model.

```python
# myapp/models.py

from django.db import models
from django_bucketav.models import BucketAVMixin


class Document(BucketAVMixin, models.Model):
    file = models.FileField()

# --> this Document class gets a `bucketav_scan_status` and a
# bucketav_last_scanned_at` fields, and they will automatically  be updated
# every time BucketAV pings us.
```
