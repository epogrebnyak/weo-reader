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


class WEO_Error(ValueError):
    pass


def to_month(period: int):
    try:
        return {1: 'Apr', 2: 'Oct'}[period]
    except KeyError:
        raise WEO_Error(f'period should be 1 or 2, got {period}')


def _url(year, period, prefix):
    """
    URL for country data file starting Oct 2007.
    Data in other formats goes back to 2000.

    Landing page with URLs:
    https://www.imf.org/external/pubs/ft/weo/2011/02/weodata/download.aspx
    """
    if prefix not in ['all', 'alla']:
        raise WEO_Error(prefix)
    if (year, period) < (2007, 2):
        raise WEO_Error(
            f'Valid year and period starts after (2007, 2), '
            f'provided: {(year, period)}')
    period_marker = str(period).zfill(2)
    month = to_month(period)
    if year == 2011 and period == 2:  # Second 2011 WEO issue was in September, not October
        month = 'Sep'
    return ('https://www.imf.org/external/pubs/ft/weo/'
            f'{year}/{period_marker}'
            f'/weodata/WEO{month}{year}{prefix}.xls')


def url(year, period):
    return _url(year, period, prefix='all')  # alla for commodities


def curl(path: str, url: str):
    r = requests.get(url, stream=True)
    iterable = r.iter_content(chunk_size=1024)
    with open(path, 'wb') as f:
        for chunk in iterable:
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return path


def to_mb(bytes):
    """Express bytes in Mb"""
    return round(bytes / 2 ** (10 * 2), 1)


def download(path, year, period, force=False):
    curl(path, url(year, period))
    p = Path(path)
    size = to_mb(p.stat().st_size)
    print(f'Downloaded {year}-{to_month(period)} WEO dataset.')
    print('File:', p, f'({size}Mb)')
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


def accept_year(func): #FIXME: make accept a country
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

       Initialised by local filename, for example 'weo.csv'.

       Source data:
           .df

       Attributes:
           .variables
           .codes                      
           .core_codes

       All-or-subset inspection methods:           
           .units()
           .countries()


       Country finders:
           .iso_code()
           .country_name()

       Single-variable dataframe:
           .get(subject, unit)
           .getc(code)

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
        return pd.period_range(start=self.years[0],
                               end=self.years[-1],
                               freq='A')

    @property
    def core_codes(self):
        return ['NGDP',
                'NGDP_RPCH',
                # Inflation
                'PCPIEPCH',
                'PCPIPCH',
                # Labor
                'LP',
                'LUR',
                # Goverment - national currentcy
                'GGR',  # ('General government revenue', 'National currency')
                'GGX',
                # ('General government total expenditure', 'National currency')
                'GGXWDG',
                # ('General government gross debt', 'National currency')
                'GGXWDN',
                'GGXONLB',
                # ('General government primary net lending/borrowing', 'National currency')
                'GGXCNL',
                # In USD
                'NGDPD',  # GDP
                'BCA',  # Current account
                ]

    # subjects and codes

    def _unique(self, columns):
        return self.df[columns].drop_duplicates()

    def _allowed_values(self, column):
        return self.df[column].unique().tolist()

    @property
    def _subject_df(self):
        return self._unique(['WEO Subject Code',
                             'Subject Descriptor',
                             'Units']) .set_index('WEO Subject Code')

    @property
    def _countries_df(self):
        return self._unique(['WEO Country Code', 'ISO', 'Country'])

    @property
    def subjects(self):
        return self._allowed_values('Subject Descriptor')

    @property
    def codes(self):
        return self._allowed_values('WEO Subject Code')

    # subjects and codes

    @property
    def variables(self):
        return [(v, u, self.to_code(v, u))
                for v in self.subjects
                for u in self.units(v)]

    def units(self, subject=None):
        ix = self.df['Subject Descriptor'] == subject
        return (self.df[ix] if subject else self.df)['Units'].unique().tolist()

    def to_code(self, subject: str, unit: str):
        self.check_subject(subject)
        self.check_unit(subject, unit)
        return self._get_by_subject_and_unit(
            subject, unit)['WEO Subject Code'].iloc[0]

    def from_code(self, variable_code):
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
            ix = self._countries_df['Country'].apply(lambda x: c in x.lower())
            return self._countries_df[ix]
        else:
            return self._countries_df

    def iso_code(self, country_name: str):
        """Return ISO code for *country_name*."""
        return self.countries(country_name).ISO.iloc[0]

    def country_name(self, iso_code):
        """Return country name for ISO country *code*."""
        return self.df[self.df.ISO == iso_code].Country.iloc[0]

    # checkers

    def _must_be_one_of(self, x, xs, name: str):
        if x not in xs:
            raise WEO_Error(f"{name.capitalize()} must be one of \n"
                            + ", ".join(xs)
                            + f"\nProvided {name}: {x}")

    def check_subject(self, subject):
        self._must_be_one_of(subject, self.subjects, 'subject')

    def check_unit(self, subject, unit):
        self._must_be_one_of(unit, self.units(subject), 'unit')

    def check_code(self, code):
        self._must_be_one_of(code, self.codes, 'code')

    def check_country(self, iso_code):
        self._must_be_one_of(iso_code, w.countries().ISO.to_list(), 'country')

    # assessor by subject/unit or code

    def _get_by_subject_and_unit(self, subject: str, unit: str):
        ix = (self.df['Subject Descriptor'] == subject) & \
             (self.df['Units'] == unit)
        return self.df[ix]

    def _get_by_code(self, variable_code):
        ix = self.df['WEO Subject Code'] == variable_code
        return self.df[ix]

    def t(self, df, column):
        """Extract columns with years from *df*, make *column* an index."""
        _df = df[self.years + [column]] \
            .set_index(column) \
            .transpose() \
            .applymap(convert)
        _df.columns.name = ''
        _df.index = self.daterange
        return _df

    def get(self, subject: str, unit: str):
        self.check_subject(subject)
        self.check_unit(subject, unit)
        _df = self._get_by_subject_and_unit(subject, unit)
        return self.t(_df, 'ISO')

    def getc(self, code: str):
        self.check_code(code)
        return self.get(*self.from_code(code))

    # assessors in other dimensions (WIP)

    def fix_year(self, year):
        year_col = str(year)
        return self.df[['ISO', 'WEO Subject Code', year_col]] \
                   .pivot(index='WEO Subject Code',
                          columns='ISO',
                          values=year_col)

    def country(self, iso_code, year=None, full=False):
        ix = self.df.ISO == iso_code
        _df = self.t(self.df[ix], 'WEO Subject Code')
        if not full:
            _df = _df[self.core_codes]
        if year is None:
            return _df
        else:
            _df = _df[str(year)].transpose()
            _df['Description'] = \
                _df.index.map(lambda c: ' - '.join(self.from_code(c)))
            return _df

    # convenience functions

    @accept_year
    def gdp_nc(self):
        return self.get('Gross domestic product, current prices',
                        'National currency')

    @accept_year
    def gdp_usd(self):
        return self.get('Gross domestic product, current prices',
                        'U.S. dollars')

    def exchange_rate(self):
        return self.gdp_nc() / self.gdp_usd()

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
    def gov_gross_debt_pgdp(self):
        return self.get('General government gross debt',
                        'Percent of GDP')

    def libor_usd(self):
        return self.get('Six-month London interbank'
                        ' offered rate (LIBOR)', 'Percent')['USA']


if __name__ == '__main__':
    w = WEO('weo.csv')
    
    import missingno as msno
    msno.matrix(w.df.sort_values(['ISO', 'WEO Subject Code']))
    for label in w.core_codes:
        print(label, *w.from_code(label)) 
        msno.matrix(w.getc(label))
        
    z = w.fix_year(2018)
    z[~z.isna()] = 1
    z.sum().sort_values().head()
    z.sum().sort_values().head(20).index.map(lambda x: w.country_name(x))
