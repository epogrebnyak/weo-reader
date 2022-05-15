# weo-reader

[![PyPI](https://img.shields.io/pypi/v/weo)](https://pypi.org/project/weo/)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/epogrebnyak/weo-reader)
[![pytest](https://github.com/epogrebnyak/weo-reader/workflows/pytest/badge.svg)](https://github.com/epogrebnyak/weo-reader/actions)
[![Downloads](https://pepy.tech/badge/weo/week)](https://pepy.tech/project/weo/week)

This is a Python client to download [IMF World Economic Outlook Report][weo] dataset as [pandas](https://pandas.pydata.org/) dataframes by release dates. You can explore:

- single country macroeconomic data and forecast,
- macro variables across countries for a given year,
- country-year panel for single macro variable.

## Dataset releases (vintages)

Dataset releases (vintages) are available back to 2007, the reported data goes back to 1980, forecast is three years ahead.

| Release          | Date         |
| :--------------- | :-----------:|
| Latest confirmed | April 2022   |
| First            | October 2007 |

Confirmed release is tested to be processed with `weo`.
Usually, if something breaks in a new release users raise an [issue here](https://github.com/epogrebnyak/weo-reader/issues).

[weo]: https://www.imf.org/en/Publications/WEO

![изображение](https://user-images.githubusercontent.com/9265326/103473902-8c64da00-4dae-11eb-957c-4737f56abdce.png)

## Install

The program is tested to run with Python 3.8.5 and higher.

To install `weo`:

`pip install weo`

## First glance

```python
from weo import download, WEO

path, url = download(2022, 1) # first (April) semiannual release
w = WEO(path)
df_cpi = w.inflation()
print(df_cpi.USA.tail(8))

# weo_2022_1.csv 18.8Mb
# Downloaded 2022-Apr WEO dataset
#         USA
# 2020  1.549
# 2021  7.426
# 2022  5.329
# 2023  2.337
# 2024  2.096
# 2025  1.970
# 2026  1.983
# 2027  2.017
```

## Step 1. Download data

Save data from IMF web site as local file. Specify year
and release:

```python
import weo

weo.download(year=2020, release="Oct", filename="weo.csv")
```

- You can access WEO releases starting October 2007 with this client.
- WEO is normally released in April and October, one exception is September 2011.
- Release is referenced by:
  - number `1` or `2`;
  - month `'Apr'` or `'Oct'`, and `'Sep'` in 2011.

Your can list all years and releases available for download with `weo.all_releases()`.
Combine to create local dataset of WEO vintages from 2007 to present:

```python
import pathlib
import weo

# create folder
pathlib.Path("weo_data").mkdir(parents=False, exist_ok=True)

# download all releases
for (year, release) in weo.all_releases():
  weo.download(year, release, directory="weo_data")
```

## Step 2. Inspect data

Use `WEO` class to view and extract data. `WEO` is a wrapper around a pandas dataframe that ensures proper data import and easier access and slicing of data across time-country-variable dimensions.

Try code below:

```python
from weo import WEO

w = WEO("weo.csv")
```

What variables and measurements are inside?

```python
# variable listing
w.variables()

# units
w.units()
w.units("Gross domestic product, current prices")

# variable codes
w.codes
w.from_code("LUR")

# countries
w.countries("United")      # Dataframe with United Arab Emirates, United Kingdom
                           # and United States
w.iso_code3("Netherlands") # 'NLD'
```

The dataset is year-country-variable-value cube, you can fix any dimension to get a table.

```python

w.get("General government gross debt", "Percent of GDP")
w.getc("NGDP_RPCH")
w.country("DEU")
w.fix_year(1994)
```

Plot a chart with the projected 12 largest economies in 2024 (current prices):

```python
(w.gdp_usd(2024)
  .dropna()
  .sort_values()
  .tail(12)
  .plot
  .barh(title="GDP by country, USD billion (2024)")
)
```

Get GDP per capita data from 2000 to 2020:

```python
w.gdp_pc_usd(start_year=2000, end_year=2020)
```

## Code documentation

`weo` package documentation is [here](https://epogrebnyak.github.io/weo-reader/).

## Alternative data sources

1\. If you need the latest data as time series and not the vintages of WEO releases, and you know variables that you are looking for, DBnomics is a good choice:

- <https://db.nomics.world/IMF/WEO>
- <https://db.nomics.world/IMF/WEOAGG>

Example:

```python
from dbnomics import fetch_series_by_api_link
ts1 = fetch_series_by_api_link("https://api.db.nomics.world/v22/"
                               "series/IMF/WEO:latest/DEU.PCPI"
                               "?observations=1")
```

[![dbnomics](https://user-images.githubusercontent.com/9265326/168478113-00fb4d3f-11c3-43ad-9c19-28e2204f89c1.png)](https://db.nomics.world/IMF/WEO:2021-10/DEU.PCPI.idx)

More on DBnomics:

- [DBnomics Web API](https://db.nomics.world/docs/web-api/)
- [Introduction to DBnomics in Python](https://notes.quantecon.org/submission/5bd32515f966080015bafbcd)

2\. Similar dataset, not updated since 2018, but with earlier years than `weo-reader`:
https://github.com/datasets/imf-weo

## Development notes

- You can download the WEO file in command line with `curl` command:

```
curl -o weo.csv https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.xls
```

- `WEOOct2020all.xls` from the web site is really a CSV file, not an Excel file.
- There is an update of GDP figures in [June 2020](jun2020), but the file structure is incompatible with regular releases.
- Prior to 2020 the URL structure was similar to `https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls`

[jun2020]: https://www.imf.org/en/Publications/WEO/Issues/2020/06/24/WEOUpdateJune2020
