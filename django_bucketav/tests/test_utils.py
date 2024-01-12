import pytest

from .. import utils


@pytest.mark.django_db
def test_get_document_with_key(document_model):
    file_key = str(document_model.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object == document_model


@pytest.mark.django_db
def test_get_unknown_file_key():
    discovered_object = utils.get_object_for_key("not-a-file")
    assert discovered_object is None


@pytest.mark.django_db
def test_no_models(settings, document_model):
    settings.BUCKETAV_MODELS = {}
    file_key = str(document_model.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object is None


@pytest.mark.django_db
def test_model_not_covered_by_settings(settings, document_model):
    settings.BUCKETAV_MODELS = {
        "testapp.Image": ["file"],
    }
    file_key = str(document_model.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object is None


@pytest.mark.django_db
def test_unrelated_model(settings, document_model):
    settings.BUCKETAV_MODELS = {
        "testapp.MyModel": ["name"],
    }
    file_key = str(document_model.file)
    discovered_object = utils.get_object_for_key(file_key)
    assert discovered_object is None
