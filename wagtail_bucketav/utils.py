import logging

from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from .models import FileScanStatus

logger = logging.getLogger("wagtail_bucketav")


def get_object_for_key(file_key):
    image_for_file = get_image_model().objects.filter(file=file_key).first()

    if image_for_file:
        return image_for_file

    return get_document_model().objects.filter(file=file_key).first()


def log_scanned_instance(sender, instance, file_scan_status, **kwargs):
    if file_scan_status == FileScanStatus.ERRORED:
        logger.error("BucketAV scan failed type=%s id=%d", sender.__name__, instance.id)
    else:
        logger.info(
            "BucketAV scanned type=%s id=%d status=%s",
            sender.__name__,
            instance.id,
            file_scan_status,
        )
