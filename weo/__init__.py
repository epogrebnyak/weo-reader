from .dataframe import WEO
from .dates import all_releases, download

from importlib.metadata import version
try:
    __version__ = version(__name__)
except:
    pass


from typing import Optional
import os

def get(year: int, release: int, path: Optional[str]=None) -> WEO:
    from .dates import accept
    _, path, _ = accept(year, release, path)
    if not os.path.exists(path):
        download(year, release, path)
    return WEO(path)

 
