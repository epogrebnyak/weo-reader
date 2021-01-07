from .dataframe import WEO
from .dates import all_releases, download

try:
    from importlib.metadata import version

    __version__ = version(__name__)
except:
    pass

import os
from typing import Optional


def get(year: int, release: int, path: Optional[str] = None) -> WEO:
    """Fast-track access to dataset - download if not present,
    read from file if already downloaded.
    """
    from .dates import accept

    _, path, _ = accept(year, release, path)
    if not os.path.exists(path):
        download(year, release, path)
    return WEO(path)
