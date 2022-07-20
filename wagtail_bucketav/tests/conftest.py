import json
from unittest.mock import Mock

import pytest
from django.urls import reverse
from wagtail.core import hooks


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
def after_bucketav_image_scan():
    hook = Mock()
    with hooks.register_temporarily("after_bucketav_image_scan", hook):
        yield hook


@pytest.fixture
def after_bucketav_document_scan():
    hook = Mock()
    with hooks.register_temporarily("after_bucketav_document_scan", hook):
        yield hook
