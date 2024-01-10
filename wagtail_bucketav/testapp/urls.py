from django.urls import include, path

urlpatterns = [
    path("bucketav/", include("wagtail_bucketav.urls")),
]
