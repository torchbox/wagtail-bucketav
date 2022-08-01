import logging

__version__ = "0.0.1"

logger = logging.getLogger("__name__")


def get_version():
    return __version__
