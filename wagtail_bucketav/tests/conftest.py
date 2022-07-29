import json
from unittest.mock import Mock

import pytest
from django.urls import reverse

from wagtail_bucketav.signals import bucketav_scan


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
def bucketav_scan_receiver():
    hook = Mock()
    bucketav_scan.connect(hook)
    yield hook
    bucketav_scan.disconnect(hook)
