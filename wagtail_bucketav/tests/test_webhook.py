import pytest
import wagtail_factories


def test_successful_image_ping(sns_request, after_bucketav_image_scan):
    image = wagtail_factories.ImageFactory()
    response = sns_request({"key": str(image.file), "status": "clean"})
    assert response.status_code == 200
    assert after_bucketav_image_scan.call_count == 1


def test_successful_document_ping(sns_request, after_bucketav_document_scan):
    document = wagtail_factories.DocumentFactory()
    response = sns_request({"key": str(document.file), "status": "clean"})
    assert response.status_code == 200
    assert after_bucketav_document_scan.call_count == 1


def test_ping_unknown_file(
    sns_request, after_bucketav_image_scan, after_bucketav_document_scan
):
    response = sns_request({"key": "not-a-file", "status": "clean"})
    assert response.status_code == 200
    assert after_bucketav_document_scan.call_count == 0
    assert after_bucketav_image_scan.call_count == 0


def test_ping_unknown_status(sns_request, after_bucketav_image_scan):
    image = wagtail_factories.ImageFactory()

    with pytest.raises(ValueError):
        sns_request({"key": str(image.file), "status": "nonsense"})

    assert after_bucketav_image_scan.call_count == 0
