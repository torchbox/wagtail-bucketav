import json
import logging

from django_sns_view.views import SNSEndpoint

from .models import FileScanStatus
from .signals import scan_result_received
from .utils import get_object_for_key

logger = logging.getLogger("django_bucketav")


class BucketAVWebhookView(SNSEndpoint):
    def handle_message(self, message: str, payload) -> None:
        message_dict = json.loads(message)  # Actually parse the JSON

        file_key: str = message_dict["key"]

        file_scan_status = FileScanStatus(message_dict["status"])

        logger.debug(
            "Received ping from BucketAV key=%s status=%s", file_key, file_scan_status
        )

        instance = get_object_for_key(file_key)

        if instance is None:
            logger.error("Received ping for unknown file key=%s", file_key)
            return

        scan_result_received.send(
            sender=instance.__class__,
            instance=instance,
            file_scan_status=file_scan_status,
        )
