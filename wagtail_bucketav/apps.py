from django.apps import AppConfig


class WagtailBucketAVAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "wagtail_bucketav"

    def ready(self):
        from .signal_handlers import log_scanned_instance
        from .signals import scan_result_received

        scan_result_received.connect(log_scanned_instance)
