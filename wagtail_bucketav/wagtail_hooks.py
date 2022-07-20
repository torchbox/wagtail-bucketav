import logging

from wagtail.core import hooks

from .models import FileScanStatus

logger = logging.getLogger("wagtail_bucketav")


@hooks.register("after_bucketav_image_scan")
def log_scanned_image(image, file_scan_status):
    if file_scan_status == FileScanStatus.ERRORED:
        logger.error("Image scan failed id=%d", image.id)
    else:
        logger.info("Image scanned id=%d status=%s", image.id, file_scan_status)


@hooks.register("after_bucketav_document_scan")
def log_scanned_document(document, file_scan_status):
    if file_scan_status == FileScanStatus.ERRORED:
        logger.error("Document scan failed id=%d", document.id)
    else:
        logger.info("Document scanned id=%d status=%s", document.id, file_scan_status)
