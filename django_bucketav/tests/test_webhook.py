import datetime as dt

import pytest

from ..models import FileScanStatus
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


@pytest.mark.django_db
def test_successful_document_with_av_mixin_ping(
    settings,
    time_machine,
    sns_request,
    scan_result_received_receiver,
    document_with_av_mixin_model,
):
    # Check our initial state:
    assert (
        document_with_av_mixin_model.bucketav_scan_status == FileScanStatus.NOT_SCANNED
    )
    assert document_with_av_mixin_model.bucketav_last_scanned_at is None

    # Test setup:
    settings.BUCKETAV_MODELS = {
        "testapp.DocumentWithBucketAVMixin": ["file"],
    }
    time_machine.move_to(dt.datetime(2024, 1, 10))

    # Right, let's simulate a BucketAV webhook...
    response = sns_request(
        {"key": str(document_with_av_mixin_model.file), "status": "clean"}
    )
    assert response.status_code == 200

    # ...and check that things went according to plan!
    document_with_av_mixin_model.refresh_from_db()
    assert document_with_av_mixin_model.bucketav_scan_status == FileScanStatus.CLEAN
    bucketav_last_scanned_at = document_with_av_mixin_model.bucketav_last_scanned_at
    assert bucketav_last_scanned_at is not None and str(
        bucketav_last_scanned_at
    ).startswith("2024-01-10 00:00")
