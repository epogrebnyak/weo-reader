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

from pathlib import Path
import pandas as pd
import numpy as np
import requests

LATEST_YEAR = 2024


class WEO_Period_Error(ValueError):
    pass


def url(year, period):
    period_marker = str(period).zfill(2)
    month = {1: 'Apr', 2: 'Oct'}[period]
    return ('https://www.imf.org/external/pubs/ft/weo/'
            f'{year}/{period_marker}'
            f'/weodata/WEO{month}{year}all.xls')


def curl(path: str, url: str):
    r = requests.get(url, stream=True)
    iterable = r.iter_content(chunk_size=1024)
    with open(path, 'wb') as f:
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return path


def to_mb(x):
    return round(x / 2 ** (10 * 2), 1)


def download(path, year, period):
    if period not in [1, 2]:
        raise WEO_Period_Error(f'period should be 1 or 2, got {period}')
    curl(path, url(year, period))
    p = Path(path)
    print('Downloaded', to_mb(p.stat().st_size), 'Mb')
    return p


def convert(x):
    if isinstance(x, str) and "," in x:
        x = x.replace(",", "")
    try:
        return float(x)
    except ValueError:
        return np.nan


def read_csv(filename):
    df = pd.read_csv(filename, delimiter="\t", encoding="iso-8859-1")
    ix = df['Country'].isna()
    return df[~ix], df[ix]


def split_footnote(s):
    import re
    res = re.search("International Monetary Fund, "
                    "World Economic Outlook Database, "
                    r"(\w*) (\d*)", s)
    return int(res[2]), res[1]


def version(filename):
    _, tail = read_csv(filename)
    return split_footnote(tail.iloc[0, 0])


def accept_year(func):
    def inner(self, *arg, year=None):
        df = func(self)
        if arg:
            year = arg[0]
        if year:
            ts = df[str(year)] \
                .transpose() \
                .iloc[:, 0]
            return ts
        else:
            return df
    return inner


class WEO:
    """Wrapper for pandas dataframe that holds
       World Economic Outlook country dataset.

       Source data:
           .df

       Inspection methods:
           .variables()
           .units()
           .find_countries()
           .iso_code()
           .subject_code()

       Single-variable dataframe:
           .get(subject, unit)
           .get_by_code(variable_code)

       Variables:
           .gdp_usd()
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
        return pd.period_range(start=self.years[0],
                               end=self.years[-1],
                               freq='A')

    # subjects and codes

    def subjects(self):
        return self.df['Subject Descriptor'].unique().tolist()

    def variables(self):
        return [(v, u, self.subject_code(v, u))
                for v in self.subjects()
                for u in self.units(v)]

    def subject_code(self, subject: str, unit: str):
        return self._get(subject, unit)['WEO Subject Code'].iloc[0]

    def units(self, subject=None):
        ix = self.df['Subject Descriptor'] == subject        
        return (self.df[ix] if subject else self.df) \
               ['Units'].unique().tolist()

    # countries

    @property
    def countries_df(self):
        country_cols = ['WEO Country Code', 'ISO', 'Country']
        return self.df[country_cols].drop_duplicates()

    def find_countries(self, name: str):
        """Find country names that include *name* as substring.
           Search is case-insensitive."""
        c = name.lower()
        ix = self.countries_df['Country'].apply(lambda x: c in x.lower())
        return self.countries_df[ix]

    def iso_code(self, country: str):
        """Return ISO code for *country* name."""
        return self.find_countries(country).ISO.iloc[0]

    def country_name(self, iso_code):
        return self.df[self.df.ISO == iso_code]

    # checkers

    def check_subject(self, subject):
        ss = self.subjects()
        if subject not in ss:
            raise ValueError("Subject must be one of \n"
                             + "%s" % ("\n  ".join(ss))
                             + f"\nProvided: {subject}")

    def check_units(self, subject, unit):
        units = self.units(subject)
        if unit not in units:
            raise ValueError(f"Unit must be one of {units}\n"
                             f"Provided: {unit}")

    # assessors

    def _get(self, subject: str, unit: str):
        ix = (self.df['Subject Descriptor'] == subject) & \
             (self.df['Units'] == unit)
        return self.df[ix]

    def get_by_code(self, variable_code):
        ix = self.df['WEO Subject Code'] == variable_code
        return self.df[ix]

    def t(self, df, column):
        _df = df[self.years + [column]] \
            .set_index(column) \
            .transpose() \
            .applymap(convert)
        _df.columns.name = ''
        _df.index = self.daterange
        return _df

    def get(self, subject: str, unit: str):
        self.check_subject(subject)
        self.check_units(subject, unit)
        _df = self._get(subject, unit)
        return self.t(_df, 'ISO')

    def fix_year(self, year):
        pass

    # convenience functions

    @accept_year
    def gdp_nc(self):
        return self.get('Gross domestic product, current prices',
                        'National currency')

    @accept_year
    def gdp_usd(self):
        return self.get('Gross domestic product, current prices',
                        'U.S. dollars')

    @accept_year
    def gdp_growth(self):
        return self.get('Gross domestic product, constant prices',
                        'Percent change')

    @accept_year
    def current_account(self):
        return self.get('Current account balance', 'U.S. dollars')

    @accept_year
    def inflation(self):
        return self.get('Inflation, end of period consumer prices',
                        'Percent change')

    @accept_year
    def gov_net_lending_pgdp(self):
        return self.get('General government net lending/borrowing',
                        'Percent of GDP')

    @accept_year
    def gov_debt_pgdp(self):
        return self.get('General government gross debt',
                        'Percent of GDP')

    def libor_usd(self):
        return self.get('Six-month London interbank'
                        ' offered rate (LIBOR)', 'Percent')['USA']


if __name__ == '__main__':
    from matplotlib.pyplot import figure

    w = WEO('weo.csv')

    # What are the largest economies?
    w.gdp_usd(2018).dropna().sort_values(ascending=True).tail(15).plot.barh()

    # Is everyone growing fast?
    figure()
    g = ((w.gdp_growth().loc['2018':, ] / 100 + 1).prod() ** (1 / 7) - 1) * 100
    g.hist(bins=50)

    figure()
    w.gdp_growth()['RUS'].plot.bar()  # change time axis

    # So why is everyone centering around 2% inflation?
    figure()
    w.inflation(2024).where(lambda x: x < 15).dropna().hist(bins=40)

    # Care to look at current accounts?
    ca = w.current_account()

    # Net exporters
    figure()
    ca.loc[:, ca.max() > 200].plot()

    # Net importers
    figure()
    ca.loc[:, ca.min() < -100].plot()

    # Who has most debt? Who is running a deficit?
    brics = ['BRA', 'IND', 'CHN', 'RUS']
    cri = ['ARG', 'GRC', 'RUS', ]  # can also include 'ECU', 'MEX'
    oil = ['NOR', 'SAU', 'RUS', 'IRN']
    dev = ['FRA', 'DEU', 'ITA', 'GBR', 'USA']  # 'ESP', 'KOR'

    for subset in [brics, cri, oil, dev]:
        w.gov_debt_pgdp()[subset].plot(title="Государственный долг, % ВВП")
        w.gov_net_lending_pgdp()[subset] .plot(
            title="Чистое кредитование/заимствование госсектора, % ВВП") .axhline(
            y=0, ls='-', lw=0.5, color='darkgrey')
