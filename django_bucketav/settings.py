from typing import TYPE_CHECKING

from django.conf import settings

if TYPE_CHECKING:
    from typing_extensions import Dict, List, TypeAlias

    DjangoModelString: TypeAlias = str
    BucketAVModelDefinition: TypeAlias = Dict[DjangoModelString, List[str]]
else:
    BucketAVModelDefinition = dict


def bucketav_models() -> "BucketAVModelDefinition":
    return getattr(settings, "BUCKETAV_MODELS", {})
