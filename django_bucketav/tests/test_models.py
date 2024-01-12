import datetime as dt

import pytest

from ..models import FileScanStatus
from ..signals import scan_result_received
from ..testapp.models import DocumentWithBucketAVMixin


@pytest.mark.parametrize(
    ("signal_status_input", "expected_scan_status"),
    (
        ("clean", FileScanStatus.CLEAN),
        ("infected", FileScanStatus.INFECTED),
        ("no", FileScanStatus.ERRORED),
    ),
)
@pytest.mark.django_db
def test_successful_document_with_av_mixin_is_updated_on_scan_result_received_signal(
    # Test dependencies:
    settings,
    time_machine,
    sns_request,
    scan_result_received_receiver,
    document_with_av_mixin_model,
    # Test params:
    signal_status_input: str,
    expected_scan_status: FileScanStatus,
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
    time_machine.move_to(dt.datetime(2024, 1, 10, 2, 3, 4), tick=False)

    # Right, let's trigger a signal...
    scan_result_received.send(
        DocumentWithBucketAVMixin,
        instance=document_with_av_mixin_model,
        file_scan_status=signal_status_input,
    )

    # ...and check that things went according to plan!
    document_with_av_mixin_model.refresh_from_db()
    assert document_with_av_mixin_model.bucketav_scan_status == expected_scan_status
    bucketav_last_scanned_at = document_with_av_mixin_model.bucketav_last_scanned_at
    assert bucketav_last_scanned_at is not None and str(
        bucketav_last_scanned_at
    ).startswith("2024-01-10 02:03:04")
