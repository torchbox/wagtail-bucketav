import json
from unittest.mock import Mock

import pytest
from django.urls import reverse

from wagtail_bucketav.signals import scan_result_received


@pytest.fixture
def sns_request(db, client, settings):
    settings.SNS_VERIFY_CERTIFICATE = False

    def _do_request(message):
        return client.post(
            reverse("wagtail_bucketav:sns-hook"),
            {
                "SigningCertURL": "https://sns.123.amazonaws.com",
                "Message": json.dumps(message),
            },
            content_type="application/json",
            HTTP_X_AMZ_SNS_MESSAGE_TYPE="Notification",
        )

    return _do_request


@pytest.fixture
def scan_result_received_receiver():
    hook = Mock()
    scan_result_received.connect(hook)
    yield hook
    scan_result_received.disconnect(hook)
