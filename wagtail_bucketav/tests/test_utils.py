import pytest
import wagtail_factories
from wagtail.documents import get_document_model_string

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


@pytest.mark.django_db
def test_no_models(settings):
    settings.WAGTAIL_BUCKETAV_MODELS = {}
    image = wagtail_factories.ImageFactory()
    file_key = str(image.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object is None


@pytest.mark.django_db
def test_unknown_model(settings):
    settings.WAGTAIL_BUCKETAV_MODELS = {
        get_document_model_string(): ["file"],
    }
    image = wagtail_factories.ImageFactory()
    file_key = str(image.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object is None


@pytest.mark.django_db
def test_specific_model(settings):
    settings.WAGTAIL_BUCKETAV_MODELS = {
        get_document_model_string(): ["file"],
    }
    document = wagtail_factories.DocumentFactory()
    file_key = str(document.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object == document
