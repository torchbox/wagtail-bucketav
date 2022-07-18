from django.urls import path

from .views import BucketAVWebhookView

app_name = "wagtail_bucketav"

urlpatterns = [path("sns-hook/", BucketAVWebhookView.as_view(), name="sns-hook")]
