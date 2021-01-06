# weo-reader

![Python 3.7](https://github.com/epogrebnyak/weo-reader/workflows/Python%203.7/badge.svg)
[![Downloads](https://pepy.tech/badge/weo/week)](https://pepy.tech/project/weo/week)

This is a Python client to download [IMF World Economic Outlook Report][weo] dataset as [pandas](https://pandas.pydata.org/) dataframes be release dates. You can explore country data, macro variables across countries 
or cross-section by year. Dataset vintages are available back to 2007. 

[weo]: https://www.imf.org/en/Publications/WEO


![изображение](https://user-images.githubusercontent.com/9265326/103473902-8c64da00-4dae-11eb-957c-4737f56abdce.png)


## Install

The program uses Python 3.7. To install `weo` use:

`pip install weo`

## Step 1. Download data
   
You need to save data as a local file before use. Download WEO country data from IMF web site as shown below:

```python 
import weo

weo.download(2019, "Oct", filename="weo.csv")
```

You can access WEO releases starting October 2007 with this client. WEO is normally released in April and October, one exception is September 2011. The
release is referenced by number (`1` or `2`) or month `'Apr'`,  `'Oct'` and in 2011 - `'Sep'`.


Your can list all years and releases available for download  with  `weo.all_releases()`. Combine it to create local dataset of WEO vintages from 2007 to present:

```python

    from weo import all_releases

    for (year, release) in all_releases():
      download(year, release, directory='weo_data') 
```

Note that folder 'weo_data' must exist for this script to run.

## Step 2. Inspect data

Use `WEO` class to view and extract data. `WEO` is a wrapper around a pandas dataframe that ensures proper data import and easier access and slicing of data. 

The dataset is year-variable-country-value cube, you can fix any dimension to get a table.

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

# variable codesß
w.codes
w.from_code("LUR")

# countries
w.countries("United")      # Dataframe with United Arab Emirates, United Kingdom
                           # and United States
w.iso_code3("Netherlands") # 'NLD'
```

See some data:

```python

w.get("General government gross debt", "Percent of GDP")
w.getc("NGDP_RPCH")
w.country("DEU", 2018)
```

Plot a chart with largest economies in 2024 (current prices):

```python
(w.gdp_usd(2024)
  .dropna()
  .sort_values()
  .tail(12)
  .plot
  .barh(title="GDP by country, USD bln (2024)")
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
curl -o weo.csv https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.x
```
- `WEOOct2019all.xls` from the web site is really a CSV file, not an Excel file.
- There is an update of GDP figures in [June 2020](jun2020), but the file structure is incompatible with regular releases.
- Prior to 2020 the URL was similar to `https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls`


[jun2020]: https://www.imf.org/en/Publications/WEO/Issues/2020/06/24/WEOUpdateJune2020
