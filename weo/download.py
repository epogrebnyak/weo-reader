"""Download dataset from IMF WEO website.

  from weo import download
  download("2020-Oct', 'weo.csv')       
           
Equivalent to:

  curl -o weo.csv https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.xls

"""

from pathlib import Path

import requests  # type: ignore

from dataclasses import dataclass
from .dates import parse_and_validate


@dataclass
class Release:
    year: int
    month: int

    def month_string(self) -> str:
        return {4: "Apr", 9: "Sep", 10: "Oct"}[self.month]

    def period_string(self) -> str:
        return {4: "01", 9: "02", 10: "02"}[self.month]


def from_date(s: str) -> Release:
    year, month = parse_and_validate(s)
    return Release(year, month)


def make_url_countries(r: Release):
    return make_url(r, prefix="all")


def make_url_commodities(r: Release):
    return make_url(r, prefix="alla")


def make_url(r, prefix):
    """
    URL for country data file starting Oct 2007.
    Data in other formats goes back to 2000.

    Landing page with URLs:
    https://www.imf.org/en/Publications/SPROLLs/world-economic-outlook-databases
    """

    base_url = "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database"

    year = r.year
    month = r.month_string()
    period_marker = r.period_string()

    if year > 2020 or (year == 2020 and month == "Oct"):  # New URL format
        return (
            f"{base_url}/{year}/{period_marker}"
            f"/WEO{month}{year}{prefix}.xls"
        )
    return (  # Old URL format
        f"{base_url}/{year}"
        f"/WEO{month}{year}{prefix}.xls"
    )


def download(date_str: str, path: str, overwrite=False):
    """Download WEO dataset to local file at *path*.
    
    date_str is "2020-04", "2019-Oct" or similar.
    path is where to write downloaded file.
    Set *overwrite* flag to True if you want to delete existing file at *path*
    (default value is False).
    """
    r = from_date(date_str)
    if Path(path).exists() and not overwrite:
        raise FileExistsError(path)
    url = make_url_countries(r)
    curl(path, url)
    print(f"Downloaded {date_str} WEO dataset.")
    print("File:", path, size_str(path))


def curl(path: str, url: str):
    r = requests.get(url, stream=True)
    iterable = r.iter_content(chunk_size=1024)
    with open(path, "wb") as f:
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return path


def to_mb(bytes: int):
    """Express bytes in Mb"""
    return round(bytes / 2 ** (10 * 2), 1)


def size(path: str) -> int:
    return Path(path).stat().st_size


def size_str(path: str) -> str:
    return f"{to_mb(size(path))}Mb"
