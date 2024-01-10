import pytest

from wagtail_bucketav.models import FileScanStatus

from ..testapp.models import Document


def test_successful_image_ping(
    sns_request, scan_result_received_receiver, document_model
):
    response = sns_request({"key": str(document_model.file), "status": "clean"})
    assert response.status_code == 200
    assert scan_result_received_receiver.call_count == 1
    assert scan_result_received_receiver.call_args[1]["sender"] == Document
    assert scan_result_received_receiver.call_args[1]["instance"] == document_model
    assert (
        scan_result_received_receiver.call_args[1]["file_scan_status"]
        == FileScanStatus.CLEAN
    )


def test_successful_document_ping(
    sns_request, scan_result_received_receiver, document_model
):
    response = sns_request({"key": str(document_model.file), "status": "clean"})
    assert response.status_code == 200
    assert scan_result_received_receiver.call_count == 1
    assert scan_result_received_receiver.call_args[1]["sender"] == Document
    assert scan_result_received_receiver.call_args[1]["instance"] == document_model
    assert (
        scan_result_received_receiver.call_args[1]["file_scan_status"]
        == FileScanStatus.CLEAN
    )


def test_ping_unknown_file(sns_request, scan_result_received_receiver, document_model):
    response = sns_request({"key": "not-a-file", "status": "clean"})
    assert response.status_code == 200
    assert scan_result_received_receiver.call_count == 0


def test_ping_unknown_status(
    sns_request, scan_result_received_receiver, document_model
):
    with pytest.raises(ValueError):
        sns_request({"key": str(document_model.file), "status": "nonsense"})

    assert scan_result_received_receiver.call_count == 0
