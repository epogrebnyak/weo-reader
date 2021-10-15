"""Access WEO data as dataframe

  from weo import WEO
  w = WEO('weo.csv')
  
"""
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from iso3166 import countries  # type: ignore


class WEO_ParsingError(ValueError):
    pass


def alpha3_to_2(alpha3: str):
    exceptions = dict(UVK="Kosovo", WBG="West Bank/Gaza Strip")
    try:
        return exceptions[alpha3]
    except KeyError:
        return countries.get(alpha3).alpha2


def convert(x):
    if isinstance(x, str) and "," in x:
        x = x.replace(",", "")
    try:
        return float(x)
    except ValueError:
        return np.nan


def read_csv(filename):  # October 2020 and later files use UTF-16 LE encoding
    df = pd.read_csv(filename, delimiter="\t", encoding="iso-8859-1")
    if df.isnull().iloc[0, 0]:
        df = pd.read_csv(filename, delimiter="\t", encoding="UTF-16 LE")
        df.dropna(how="all", axis=1, inplace=True)
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
    def inner(self, *arg, year=None, start_year=None, end_year=None):
        df = func(self)
        if arg:
            year = arg[0]
        elif start_year and end_year:
            year = [start_year + y for y in range(end_year - start_year + 1)]
        if year:
            if type(year) == list:
                year = [str(y) for y in year]
            else:
                year = str(year)

            ts = df.transpose()[year]
            return ts
        else:
            return df

    return inner


class WEO:
    """Wrapper for pandas dataframe that holds
    World Economic Outlook country dataset.

    Initialised by local filepath:

       w = WEO('weo.csv')

    Attributes:

     - .subjects
     - .codes
     - .core_codes
     - .years

    All-or-subsets inspection methods:

     - .variables()
     - .units()
     - .countries()

    Country finders:

     - .iso_code3(country_name)
     - .iso_code2(country_name)
     - .country_name(country_code)

    Single variable dataframe:

     - .get(subject, unit)
     - .getc(code)

    Multiple variable dataframe:

     - .country(country_code)
     - .fix_year(year)

    Variables:

      - .gdp_usd()
      - .current_account()
      - .libor_usd()
        and other
    """

    def __init__(self, filename, id_column="ISO"):
        self.df, _ = read_csv(filename)
        self.id_column = id_column

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
            raise WEO_ParsingError(
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
        return self.t(_df, self.id_column)

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
            raise WEO_ParsingError(iso_code)
        _df = self._extract(ix, "WEO Subject Code")
        if compact:
            _df = _df[self.core_codes]
        if year is None:
            return _df
        else:
            _df = _df.transpose()[str(year)]
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
    def gdp_pc_nc(self):
        return self.get(
            "Gross domestic product per capita, current prices", "National currency"
        )

    @accept_year
    def gdp_pc_usd(self):
        return self.get(
            "Gross domestic product per capita, current prices", "U.S. dollars"
        )

    @accept_year
    def gdp_ppp(self):
        return self.get(
            "Gross domestic product, current prices",
            "Purchasing power parity; international dollars",
        )

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
