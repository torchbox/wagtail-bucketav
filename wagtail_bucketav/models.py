from django.db import models
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
    )

    class Meta:
        abstract = True
