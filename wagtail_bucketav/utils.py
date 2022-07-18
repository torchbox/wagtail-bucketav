from wagtail.documents import get_document_model
from wagtail.images import get_image_model


def get_object_for_key(file_key):
    image_for_file = get_image_model().objects.filter(file=file_key).first()

    if image_for_file:
        return image_for_file

    return get_document_model().objects.filter(file=file_key()).first()
