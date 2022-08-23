from django.db import models

from wagtail.documents.models import Document, AbstractDocument
from wagtail.images.models import Image, AbstractImage, AbstractRendition

from wagtail_bucketav.models import BucketAVMixin


class CustomImage(AbstractImage, BucketAVMixin):
    admin_form_fields = Image.admin_form_fields


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class CustomDocument(AbstractDocument, BucketAVMixin):
    admin_form_fields = Document.admin_form_fields
