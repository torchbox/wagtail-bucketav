import json
import logging

from django_sns_view.views import SNSEndpoint

from .models import FileScanStatus
from .signals import bucketav_scan
from .utils import get_object_for_key

logger = logging.getLogger("wagtail_bucketav")


class BucketAVWebhookView(SNSEndpoint):
    def handle_message(self, message, payload):
        message = json.loads(message)  # Actually parse the JSON

        file_key = message["key"]

        file_scan_status = FileScanStatus(message["status"])

        logger.debug(
            "Received ping from BucketAV key=%s status=%s", file_key, file_scan_status
        )

        instance = get_object_for_key(file_key)

        if instance is None:
            logger.error("Received ping for unknown file key=%s", file_key)
            return

        bucketav_scan.send(
            sender=instance.__class__,
            instance=instance,
            file_scan_status=file_scan_status,
        )
