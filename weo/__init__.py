from .dataframe import WEO
from .dates import all_releases, download

from importlib.metadata import version

try:
    __version__ = version(__name__)
except:
    pass


def get(year: int, release: int, path: str) -> WEO:
    import os
    if not os.path.exists(path):
        download(year, release, path)
    return WEO(path)
