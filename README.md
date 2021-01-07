# weo-reader

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/epogrebnyak/weo-reader)
![pytest](https://github.com/epogrebnyak/weo-reader/workflows/pytest/badge.svg)
[![Downloads](https://pepy.tech/badge/weo/week)](https://pepy.tech/project/weo/week)

This is a Python client to download [IMF World Economic Outlook Report][weo] dataset as [pandas](https://pandas.pydata.org/) dataframes by release dates. You can explore:
- single country macroeconomic data and forecast, 
- macro variables across countries for a given year,
- country-year panel for single macro variable. 

Dataset releases (vintages) are available back to 2007, the reported data goes back to 1980, forecast is three years ahead.

[weo]: https://www.imf.org/en/Publications/WEO


![изображение](https://user-images.githubusercontent.com/9265326/103473902-8c64da00-4dae-11eb-957c-4737f56abdce.png)


## Install

The program is tested to run under Python 3.8. It may work well with Python version 3.6 and above.

To install `weo`:

`pip install weo`

## Step 1. Download data
   
You need to save data as from IMF web site as local file. Specify year
and release: 

```python 
import weo


weo.download(year=2020, release="Oct", filename="weo.csv")
```

You can access WEO releases starting October 2007 with this client. WEO is normally released in April and October, one exception is September 2011. 

Release is referenced by number (`1` or `2`) or by month (`'Apr'` or  `'Oct'`, and `'Sep'` in in 2011).

Your can list all years and releases available for download  with  `weo.all_releases()`. Combine it to create local dataset of WEO vintages from 2007 to present:

```python

    from weo import all_releases

    for (year, release) in all_releases():
      weo.download(year, release, directory='weo_data') 
```

Note that folder 'weo_data' must exist for this script to run.

## Step 2. Inspect data

Use `WEO` class to view and extract data. `WEO` is a wrapper around a pandas dataframe that ensures proper data import and easier access and slicing of data. 


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

Plot a chart with the 12 largest economies in 2024 (current prices):

```python
(w.gdp_usd(2024)
  .dropna()
  .sort_values()
  .tail(12)
  .plot
  .barh(title="GDP by country, USD billion (2024)")
)
```

## Alternative data sources

1\. If you need the latest data as time series and not the vintages of WEO releases, and you know 
variables that you are looking for, *dbnomics* is a good choice: 
- <https://db.nomics.world/IMF/WEO>
- <https://db.nomics.world/IMF/WEOAGG>

Small example:

```python
from dbnomics import fetch_series_by_api_link
ts1 = fetch_series_by_api_link("https://api.db.nomics.world/v22/"
                               "series/IMF/WEO/DEU.NGDPRPC"
                               "?observations=1")
```

2\. Similar dataset, not updated since 2018, but with earlier years: https://github.com/datasets/imf-weo

## Development notes

- You can download the WEO file in command line with `curl` command:
```
curl -o weo.csv https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.xls
```
- `WEOOct2020all.xls` from the web site is really a CSV file, not an Excel file.
- There is an update of GDP figures in [June 2020](jun2020), but the file structure is incompatible with regular releases.
- Prior to 2020 the URL was similar to `https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls`

[jun2020]: https://www.imf.org/en/Publications/WEO/Issues/2020/06/24/WEOUpdateJune2020
