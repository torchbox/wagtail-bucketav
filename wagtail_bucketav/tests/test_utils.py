import pytest
import wagtail_factories

from wagtail_bucketav import utils


@pytest.mark.django_db
def test_get_image_with_key():
    image = wagtail_factories.ImageFactory()
    file_key = str(image.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object == image


@pytest.mark.django_db
def test_get_document_with_key():
    document = wagtail_factories.DocumentFactory()
    file_key = str(document.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object == document


@pytest.mark.django_db
def test_get_unknown_file_key():
    discovered_object = utils.get_object_for_key("not-a-file")
    assert discovered_object is None
