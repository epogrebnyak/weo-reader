"""Download dataset from IMF WEO website.

  from weo import download
  download("2019-Oct', 'weo.csv')       
           
Equivalent to:

  curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls

"""

from pathlib import Path

import requests  # type: ignore

from dataclasses import dataclass
from datetime import datetime, date


class WEO_DateError(ValueError):
    pass


def validate(year: int, month: int):
    text = date(year, month, 1).strftime("%Y-%b")
    exceptions = [(2011, 9)]
    if (year, month) < (2007, 4):
        raise WEO_DateError(f"Cannot work with date earlier than 2007-Apr, got {text}")
    t = datetime.today()
    if (year, month) > (t.year, t.month):
        raise WEO_DateError(f"The date is in the future, got {text}")
    if month not in [4, 10] and (year, month) not in exceptions:
        raise WEO_DateError(f"Usual accepted months are Apr and Oct, got {text}")


def validate_month(month: int):
    if month not in [4, 9, 10]:
        raise WEO_DateError(month)


@dataclass
class Release:
    year: int
    month: int

    def __post_init__(self):
        validate_month(self.month)

    def __iter__(self):
        yield self.year
        yield self.month

    def month_string(self) -> str:
        return {4: "Apr", 9: "Sep", 10: "Oct"}[self.month]

    def period_string(self) -> str:
        return {4: "01", 9: "02", 10: "02"}[self.month]


def parse(s: str):
    for fmt in "%Y-%b", "%Y-%m", "%Y-%B":
        try:
            dt = datetime.strptime(s, fmt)
            return dt.year, dt.month
        except ValueError:
            pass
    raise ValueError(s)


def from_date(s: str) -> Release:
    return Release(*parse(s))




def make_url_countries(r: Release):
    return make_url(r, prefix="all")


def make_url_commodities(r: Release):
    return make_url(r, prefix="alla")


def make_url(r, prefix):
    """
    URL for country data file starting Oct 2007.
    Data in other formats goes back to 2000.

    Landing page with URLs:
    https://www.imf.org/external/pubs/ft/weo/2011/02/weodata/download.aspx
    """
    year = r.year
    month = r.month_string()
    period_marker = r.period_string()
    return (
        "https://www.imf.org/external/pubs/ft/weo/"
        f"{year}/{period_marker}"
        f"/weodata/WEO{month}{year}{prefix}.xls"
    )


def download(date_str: str, path: str, overwrite=False):
    """Download WEO dataset to local file at *path*.
    
    date_str is "2020-04", "2019-Oct" or similar.
    path is where to write downloaded file.
    Set *overwrite* flag to True if you want to delete existing file at *path*
    (default value is False).
    """
    r = from_date(date_str)
    validate(*r)
    if Path(path).exists() and not overwrite:
        raise FileExistsError(path)
    url = make_url_countries(r)
    curl(path, url)
    print(f"Downloaded {date_str} WEO dataset.")
    print("File:", path, f"({size(path)}Mb)")


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


def size(path: str):
    return to_mb(Path(path).stat().st_size)
