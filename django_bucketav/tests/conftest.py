import json
from unittest.mock import Mock

import pytest
from django.core.files.base import ContentFile
from django.urls import reverse

from ..signals import scan_result_received
from ..testapp.models import Document, DocumentWithBucketAVMixin


@pytest.fixture
def sns_request(db, client, settings):
    settings.SNS_VERIFY_CERTIFICATE = False

    def _do_request(message):
        return client.post(
            reverse("django_bucketav:sns-hook"),
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


@pytest.fixture
def django_file() -> ContentFile:
    file = ContentFile(
        # N.B. This GIF content is a copy-paste from:
        # https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.post
        b"GIF89a\x01\x00\x01\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00"
        b"\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x01\x00\x00",
        name="myimage.gif",
    )
    return file


@pytest.fixture
def document_model(django_file) -> Document:
    return Document.objects.create(file=django_file)


@pytest.fixture
def document_with_av_mixin_model(django_file) -> DocumentWithBucketAVMixin:
    return DocumentWithBucketAVMixin.objects.create(file=django_file)
