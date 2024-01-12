from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class FileScanStatus(models.TextChoices):
    NOT_SCANNED = "not_scanned", _("Not scanned")
    CLEAN = "clean", _("Clean")
    INFECTED = "infected", _("Infected")
    ERRORED = "no", _("Errored")


class BucketAVMixin(models.Model):
    bucketav_scan_status = models.CharField(
        max_length=max(len(label) for label in FileScanStatus.labels),
        choices=FileScanStatus.choices,
        default=FileScanStatus.NOT_SCANNED,
        verbose_name=_("bucketAV scan status"),
    )
    bucketav_last_scanned_at = models.DateTimeField(null=True)

    def update_bucketav_scan_status(self, scan_status: FileScanStatus) -> None:
        self.bucketav_scan_status = scan_status
        self.bucketav_last_scanned_at = timezone.now()
        self.save(update_fields=("bucketav_scan_status", "bucketav_last_scanned_at"))

    class Meta:
        abstract = True
