"""Python client to get IMF WEO datasetas pandas dataframe.

1. Download country data source file from IMF website (as weo.csv):

curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls

or

  from weo import download
  download('weo.csv', 2019, 2) # 1 or 2 are release numbers

2. Access data as WEO class instance

  from weo import WEO
  w = WEO('weo.csv')

"""

from dataclasses import dataclass
from pathlib import Path

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
from iso3166 import countries  # type: ignore


class WEO_Error(ValueError):
    pass


def check_range(year, period):
    if (year, period) < (2007, 2):
        raise WEO_Error(
            f"Cannot process year and period before (2007, 2).\n"
            f"Provided: {(year, period)}"
        )


def check_prefix(prefix: str):
    if prefix not in ["all", "alla"]:
        raise WEO_Error(prefix)


def alpha3_to_2(alpha3: str):
    if alpha3 == "UVK":
        return "Kosovo"
    else:
        return countries.get(alpha3).alpha2


def check_period(period):
    if not period in [1, 2]:
        raise WEO_Error(f"period should be 1 or 2, got {period}")


def to_month(year: int, period: int):
    check_period(period)
    month = {1: "Apr", 2: "Oct"}[period]
    # Second 2011 WEO issue was in September, not October
    if year == 2011 and period == 2:
        month = "Sep"
    return month


def make_url_countries(year: int, period: int):
    return make_url(year, period, prefix="all")
    # NOTE: can also use "alla" for commodities


def make_url(year, period, prefix):
    """
    URL for country data file starting Oct 2007.
    Data in other formats goes back to 2000.

    Landing page with URLs:
    https://www.imf.org/external/pubs/ft/weo/2011/02/weodata/download.aspx
    """
    check_prefix(prefix)
    month = to_month(year, period)
    period_marker = str(period).zfill(2)
    return (
        "https://www.imf.org/external/pubs/ft/weo/"
        f"{year}/{period_marker}"
        f"/weodata/WEO{month}{year}{prefix}.xls"
    )


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


# Using "forward reference" for WEO class: https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html#miscellaneous
def download(year: int, period: int, path: str, overwrite=False) -> "WEO":
    """Download WEO dataset to local file at *path*.
    *year* and *period* identify WEO dataset.
    *year: int* is 2017 and up. 
    *period: int* is 1 for April release and 2 for Sept/Oct release. 
    Set *overwrite* flag to True if you want to delete existign file at *path*
    (default value is False).
    """
    check_period(period)
    check_range(year, period)
    r = Release(year, period)
    r.download(path, overwrite)
    return WEO(path)


@dataclass
class Release(object):
    year: int
    period: int

    def download(self, path: str, overwrite: bool):
        if Path(path).exists() and not overwrite:
            raise FileExistsError(path)
        pure_download(self.year, self.period, path)


def pure_download(year: int, period: int, path: str):
    url = make_url_countries(year, period)
    curl(path, url)
    mb = size(path)
    print(f"Downloaded {year}-{to_month(year, period)} WEO dataset.")
    print("File:", path, f"({mb}Mb)")
    return WEO(path)


def convert(x):
    if isinstance(x, str) and "," in x:
        x = x.replace(",", "")
    try:
        return float(x)
    except ValueError:
        return np.nan


def read_csv(filename):
    df = pd.read_csv(filename, delimiter="\t", encoding="iso-8859-1")
    ix = df["Country"].isna()
    return df[~ix], df[ix]


def split_footnote(s):
    import re

    res = re.search(
        "International Monetary Fund, "
        "World Economic Outlook Database, "
        r"(\w*) (\d*)",
        s,
    )
    return int(res[2]), res[1]


def version(filename):
    _, tail = read_csv(filename)
    return split_footnote(tail.iloc[0, 0])


def accept_year(func):  # FIXME: make accept a country
    def inner(self, *arg, year=None):
        df = func(self)
        if arg:
            year = arg[0]
        if year:
            ts = df[str(year)].transpose().iloc[:, 0]
            return ts
        else:
            return df

    return inner


class WEO:
    """Wrapper for pandas dataframe that holds
       World Economic Outlook country dataset.

       Initialised by local filename, example: 
       
       w = WEO('weo.csv')

       
       Source data:
           .df

       Attributes:
           .subjects
           .codes                      
           .core_codes
           .years

       All-or-subsets inspection methods:           
           .variables()
           .units()
           .countries()

       Country finders:
           .iso_code3(country_name)
           .iso_code2(country_name)
           .country_name(country_code)

       Single variable dataframe:
           .get(subject, unit)
           .getc(code)

       Multiple variable dataframe:
           .country(country_code)
           .fix_year(year)

       Variables:
           .gdp_usd()
           .current_account()
           .libor_usd()
           and other
       """

    def __init__(self, filename):
        self.df, _ = read_csv(filename)

    @property
    def years(self):
        return [x for x in self.df.columns if x.isdigit()]

    @property
    def daterange(self):
        return pd.period_range(start=self.years[0], end=self.years[-1], freq="A")

    @property
    def core_codes(self):
        return [
            x
            for x in [
                # GDP
                "NGDP",
                "NGDP_RPCH",
                # Saving and investment
                "NGSD_NGDP",
                "NID_NGDP",
                # Inflation
                "PCPIEPCH",
                "PCPIPCH",
                "NGDP_D",
                # Labor
                "LP",
                "LUR",
                # Goverment - national currency
                "GGR",  # General government revenue
                "GGX",  # General government total expenditure
                # Government debt
                "GGXWDG",  # gross
                "GGXWDN",  # net
                # Net lending/borrowing
                "GGXONLB",
                "GGXCNL",
                # In USD
                "NGDPD",  # GDP
                "BCA",  # Current account
                "PPPEX",  # Implied PPP conversion rate
            ]
            if x in self.codes
        ]

    def core_codes_describe(self):
        return [(c, *self.from_code(c)) for c in self.core_codes]

    # subjects and codes

    def _unique(self, columns):
        return self.df[columns].drop_duplicates()

    def _allowed_values(self, column):
        return self.df[column].unique().tolist()

    @property
    def _subject_df(self):
        return self._unique(
            ["WEO Subject Code", "Subject Descriptor", "Units"]
        ).set_index("WEO Subject Code")

    @property
    def _countries_df(self):
        return self._unique(["WEO Country Code", "ISO", "Country"])

    @property
    def subjects(self):
        return self._allowed_values("Subject Descriptor")

    @property
    def codes(self):
        return self._allowed_values("WEO Subject Code")

    # subjects

    def variables(self, pattern=None):
        vs = [(v, u, self.to_code(v, u)) for v in self.subjects for u in self.units(v)]
        if pattern:
            return [(v, u, c) for (v, u, c) in vs if pattern.lower() in v.lower()]
        return vs

    def units(self, subject=None):
        ix = self.df["Subject Descriptor"] == subject
        return (self.df[ix] if subject else self.df)["Units"].unique().tolist()

    # codes

    def to_code(self, subject: str, unit: str):
        self.check_subject(subject)
        self.check_unit(subject, unit)
        return self._get_by_subject_and_unit(subject, unit)["WEO Subject Code"].iloc[0]

    def from_code(self, variable_code: str):
        self.check_code(variable_code)
        ix = self._subject_df.index == variable_code
        return tuple(self._subject_df[ix].transpose().iloc[:, 0].to_list())

    # countries

    def countries(self, name=None):
        """List all countries or find country names that
           include *name* as substring. The search is case-insensitive.
        """
        if name:
            c = name.lower()
            ix = self._countries_df["Country"].apply(lambda x: c in x.lower())
            return self._countries_df[ix]
        else:
            return self._countries_df

    def iso_code3(self, country_name: str):
        """Return three-letter ISO code for *country_name*."""
        return self.countries(country_name).ISO.iloc[0]

    def iso_code2(self, country_name: str):
        """Return two-letter ISO code for *country_name*."""
        return alpha3_to_2(self.iso_code3(country_name))

    def country_name(self, iso_code):
        """Return country name for ISO country *code*."""
        if len(iso_code) == 2:
            iso_code = countries.get(iso_code).alpha3
        return self.df[self.df.ISO == iso_code].Country.iloc[0]

    # checkers

    def _must_be_one_of(self, x, xs, name: str):
        if x not in xs:
            raise WEO_Error(
                f"{name.capitalize()} must be one of \n"
                + ", ".join(xs)
                + f"\nProvided {name}: {x}"
            )

    def check_subject(self, subject):
        self._must_be_one_of(subject, self.subjects, "subject")

    def check_unit(self, subject, unit):
        self._must_be_one_of(unit, self.units(subject), "unit")

    def check_code(self, code):
        self._must_be_one_of(code, self.codes, "code")

    def check_country(self, iso_code):
        self._must_be_one_of(iso_code, self.countries().ISO.to_list(), "country")

    # assessor by subject/unit or code

    def _get_by_subject_and_unit(self, subject: str, unit: str):
        ix = (self.df["Subject Descriptor"] == subject) & (self.df["Units"] == unit)
        return self.df[ix]

    def _get_by_code(self, variable_code):
        ix = self.df["WEO Subject Code"] == variable_code
        return self.df[ix]

    def t(self, df, column):
        """Extract columns with years from *df*, make *column* an index."""
        _df = df[self.years + [column]].set_index(column).transpose().applymap(convert)
        _df.columns.name = ""
        _df.index = self.daterange
        return _df

    def _extract(self, ix, column):
        """Extract columns with years from *df*, make *column* an index."""
        _df = (
            self.df[ix][self.years + [column]]
            .set_index(column)
            .transpose()
            .applymap(convert)
        )
        _df.columns.name = ""
        _df.index = self.daterange
        return _df

    def get(self, subject: str, unit: str):
        self.check_subject(subject)
        self.check_unit(subject, unit)
        _df = self._get_by_subject_and_unit(subject, unit)
        return self.t(_df, "ISO")

    def getc(self, code: str):
        self.check_code(code)
        return self.get(*self.from_code(code))

    # assessors in other dimensions (WIP)

    def fix_year(self, year):
        return (
            self.df[["ISO", "WEO Subject Code", str(year)]]
            .pivot(index="WEO Subject Code", columns="ISO", values=str(year))
            .applymap(convert)
        )

    def country(self, iso_code, year=None, compact=True):
        """
        Must add:
            - exchange rate
            - plottable information
        See notes for:
            - net debt            
        """
        if len(iso_code) == 3:
            ix = self.df.ISO == iso_code
        elif len(iso_code) == 2:
            ix = self.df.ISO.apply(alpha3_to_2) == iso_code
        else:
            raise WEO_Error(iso_code)
        _df = self._extract(ix, "WEO Subject Code")
        if compact:
            _df = _df[self.core_codes]
        if year is None:
            return _df
        else:
            _df = _df[str(year)].transpose()
            _df["Description"] = _df.index.map(lambda c: " - ".join(self.from_code(c)))
            return _df

    # individual variables

    @accept_year
    def gdp_nc(self):
        return self.get("Gross domestic product, current prices", "National currency")

    @accept_year
    def gdp_usd(self):
        return self.get("Gross domestic product, current prices", "U.S. dollars")

    def nlargest(self, n=10, year=2018):
        return self.gdp_usd(year).sort_values(ascending=False).head(n).index.tolist()

    def exchange_rate(self, year=None):
        return self.gdp_nc(year) / self.gdp_usd(year)

    @accept_year
    def population(self):
        return self.get("Population", "Persons")

    @accept_year
    def gdp_growth(self):
        return self.get("Gross domestic product, constant prices", "Percent change")

    @accept_year
    def current_account(self):
        return self.get("Current account balance", "U.S. dollars")

    @accept_year
    def inflation(self):
        return self.get("Inflation, end of period consumer prices", "Percent change")

    @accept_year
    def gov_net_lending_pgdp(self):
        return self.get("General government net lending/borrowing", "Percent of GDP")

    @accept_year
    def gov_gross_debt_pgdp(self):
        return self.get("General government gross debt", "Percent of GDP")

    def libor_usd(self):
        return self.get(
            "Six-month London interbank" " offered rate (LIBOR)", "Percent"
        )["USA"]
