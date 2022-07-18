from django.urls import include, path

urlpatterns = [
    path("admin/", include("wagtail.admin.urls")),
    path("bucketav/", include("wagtail_bucketav.urls")),
    path("", include("wagtail.core.urls")),
]
