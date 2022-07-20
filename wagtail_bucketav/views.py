import json
import logging

from django_sns_view.views import SNSEndpoint
from wagtail.core import hooks
from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from .models import FileScanStatus
from .utils import get_object_for_key

logger = logging.getLogger("wagtail_bucketav")


class BucketAVWebhookView(SNSEndpoint):
    @staticmethod
    def get_hook_name(instance):
        if isinstance(instance, get_image_model()):
            return "after_bucketav_image_scan"
        elif isinstance(instance, get_document_model()):
            return "after_bucketav_document_scan"
        return None

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

        hook_name = self.get_hook_name(instance)

        if hook_name is None:
            logger.error(
                "Received ping for unknown model type=%s", instance.__class__.__name__
            )
            return

        for fn in hooks.get_hooks(hook_name):
            fn(instance, file_scan_status)
