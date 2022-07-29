import pytest
import wagtail_factories
from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from wagtail_bucketav.models import FileScanStatus


def test_successful_image_ping(sns_request, bucketav_scan_receiver):
    image = wagtail_factories.ImageFactory()
    response = sns_request({"key": str(image.file), "status": "clean"})
    assert response.status_code == 200
    assert bucketav_scan_receiver.call_count == 1
    assert bucketav_scan_receiver.call_args[1]["sender"] == get_image_model()
    assert bucketav_scan_receiver.call_args[1]["instance"] == image
    assert (
        bucketav_scan_receiver.call_args[1]["file_scan_status"] == FileScanStatus.CLEAN
    )


def test_successful_document_ping(sns_request, bucketav_scan_receiver):
    document = wagtail_factories.DocumentFactory()
    response = sns_request({"key": str(document.file), "status": "clean"})
    assert response.status_code == 200
    assert bucketav_scan_receiver.call_count == 1
    assert bucketav_scan_receiver.call_args[1]["sender"] == get_document_model()
    assert bucketav_scan_receiver.call_args[1]["instance"] == document
    assert (
        bucketav_scan_receiver.call_args[1]["file_scan_status"] == FileScanStatus.CLEAN
    )


def test_ping_unknown_file(sns_request, bucketav_scan_receiver):
    response = sns_request({"key": "not-a-file", "status": "clean"})
    assert response.status_code == 200
    assert bucketav_scan_receiver.call_count == 0


def test_ping_unknown_status(sns_request, bucketav_scan_receiver):
    image = wagtail_factories.ImageFactory()

    with pytest.raises(ValueError):
        sns_request({"key": str(image.file), "status": "nonsense"})

    assert bucketav_scan_receiver.call_count == 0
