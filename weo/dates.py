import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple, Union

import requests

__all__ = [
    "download",
    "all_releases",
    "make_url_countries",
    "make_url_commodities",
    "Date",
]


def cur_year() -> int:
    return datetime.today().year


def cur_month() -> int:
    return datetime.today().month


class Release(Enum):
    Spring = 1
    Fall = 2


@dataclass
class Date:
    year: int
    release: Release

    def __gt__(self, x):
        return not (self <= x)

    def __lt__(self, x):
        return (self.year, self.release) < (x.year, x.release)

    def __le__(self, x):
        return (self < x) | (self == x)


def succ(d: Date) -> Date:
    year, rel = d.year, d.release
    if d.release == 2:
        year += 1
        rel = 1
    else:
        rel = 2
    return Date(year, rel)


def first() -> Date:
    return Date(2007, 2)


def current() -> Date:
    y = cur_year()
    m = cur_month()
    if m >= 10:
        return Date(y, 2)
    elif 4 <= m < 10:
        return Date(y, 1)
    else:
        return Date(y - 1, 2)


def month(d: Date) -> int:
    if d == Date(2011, 2):
        return 9
    elif d.release == 2:
        return 10
    else:
        return 4


def month_str(d: Date) -> str:
    return {4: "Apr", 9: "Sep", 10: "Oct"}[month(d)]


def name(d: Date) -> str:
    return f"{d.year}-{month_str(d)} WEO dataset"


def period_str(d: Date) -> str:
    return str(d.release).zfill(2)


base_url = "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database"


def filename(year, month, prefix):
    return f"WEO{month}{year}{prefix}.xls"


def url_after_2020(base_url, year, month, period_marker, prefix):
    fn = filename(year, month, prefix)
    return f"{base_url}/{year}/{period_marker}/{fn}"


def url_before_2020(base_url, year, month, period_marker, prefix):
    fn = filename(year, month, prefix)
    return f"{base_url}/{year}/{fn}"


def make_url(d: Date, prefix: str, base_url: str = base_url):
    year = d.year
    month = month_str(d)
    period_marker = period_str(d)
    args = base_url, year, month, period_marker, prefix
    if d >= Date(2020, 2):
        return url_after_2020(*args)
    else:
        return url_before_2020(*args)


def make_url_countries(d: Date):
    return make_url(d, prefix="all")


def make_url_commodities(d: Date):
    return make_url(d, prefix="alla")


def yield_dates():
    d = first()
    last = current()
    while d <= last:
        yield d
        d = succ(d)


def all_releases() -> List[Tuple[int, int]]:
    """Provide all (year, release) pairs to use in bulk download."""
    return [(d.year, d.release) for d in yield_dates()]


def is_future(d: Date):
    return d > current()


def is_ancient(d: Date):
    return d < first()


class DateError(ValueError):
    pass


def validate(d: Date):
    if is_ancient(d):
        raise DateError(f"Cannot work with date earlier than October 2007, got {d}")
    if is_future(d):
        raise DateError(f"The date is in the future: {d}")


def get_season(tag: Union[int, str]) -> int:
    if isinstance(tag, str):
        tag = tag.lower()[:3]
    if tag in [1, 2]:
        return tag
    elif tag in ["apr", 4]:
        return 1
    elif tag in ["oct", "sep", 9, 10]:
        return 2
    else:
        raise DateError(tag)


def default_filename(d: Date):
    return f"weo_{d.year}_{d.release}.csv"


def locate(d, filename: Optional[str] = None, directory: Optional[str] = None):
    if filename is None:
        filename = default_filename(d)
    if directory is None:
        return filename
    else:
        return os.path.normpath(os.path.join(directory, filename))


def get_date(year: int, release: Union[int, str]):
    release = get_season(release)
    d = Date(year, release)
    validate(d)
    return d


def curl(path: str, url: str):
    r = requests.get(url, stream=True)
    iterable = r.iter_content(chunk_size=1024)
    with open(path, "wb") as f:
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    print(path, size_str(path))
    return path


def download(
    year: int,
    release: int,
    filename: Optional[str] = None,
    directory: str = ".",
    fetch=curl,
):
    """Download dataset from IMF WEO website by release.

      from weo import download
      download(2020, 'Oct', 'weo.csv')

    Equivalent to:

       curl -o weo.csv https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.xls

    To download all releases (folder 'weo_data' must exist):

      from weo import all_releases

      for (year, release) in all_releases():
        download(year, release, directory='weo_data')



    Parameters
    ----------
    year : int
        Year of WEO release.
    release : int or str
        For spring WEO release use 1 or 'Apr'
        For fall WEO release use 2, 'Oct' or (in 2011) - 'Sep'.
    filename : str
        Filename where to save file.
    directory:
        Directory where to write file.
    fetch: callable, optional
        Used for testing.

    Returns
    -------
    path, url

    """
    d = get_date(year, release)
    path = locate(d, filename, directory)
    url = make_url_countries(d)
    if os.path.exists(path):
        print("Already downloaded", name(d), "at", path)
    else:
        fetch(path, url)
        print("Downloaded", name(d))
    return path, url


def mb(bytes: int):
    """Express bytes in Mb"""
    x = bytes / (2 ** (10 * 2))
    return round(x, 1)


def size(path: str) -> int:
    return Path(path).stat().st_size


def size_str(path: str) -> str:
    x = mb(size(path))
    return f"{x}Mb"
