from . import logger
from .models import BucketAVMixin, FileScanStatus


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


def update_scan_status_for_instance(sender, instance, file_scan_status, **kwargs):
    if isinstance(instance, BucketAVMixin):
        instance.update_bucketav_scan_status(file_scan_status)
