from django.apps import AppConfig


class WagtailBucketAVAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "wagtail_bucketav"

    def ready(self):
        from .signals import bucketav_scan
        from .utils import log_scanned_instance

        bucketav_scan.connect(log_scanned_instance)
