from django.conf import settings
from wagtail.documents import get_document_model_string
from wagtail.images import get_image_model_string

_DEFAULT_WAGTAIL_BUCKETAV_MODELS = {
    get_image_model_string(): ["file"],
    get_document_model_string(): ["file"],
}


def bucketav_models():
    return getattr(
        settings, "WAGTAIL_BUCKETAV_MODELS", _DEFAULT_WAGTAIL_BUCKETAV_MODELS
    )
