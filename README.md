# weo-reader

![Python 3.7](https://github.com/epogrebnyak/weo-reader/workflows/Python%203.7/badge.svg)

This is a third-party Python client to download [IMF World Economic Outlook Report][weo] dataset and use it as [pandas](https://pandas.pydata.org/) dataframe. 

You can download [WEO releases][weo] by year and month and explore the dataset. 

[weo]: https://www.imf.org/en/Publications/WEO

## Install

The program uses Python 3.7. To install `weo` as a python package use:

`pip install weo`
   
## Start using   

### Download 
   
You need to save data as a local file before use.
 Download latest WEO country data file from IMF web site as shown below:

```python 
from weo import download

download("2019-Oct", path='weo.csv', overwrite=True)
```

## Available dates

You can access WEO releases starting `2007-Oct` with this client. WEO is normally released in April and October, one exception is `2011-Sep`. 

There is an update of GDP figures in [June 2020](jun2020), but the file structure is incompatible with regular releases.

`2020-04`, `2020-Apr`,  `2020-April`,  `2019-10`, `2019-Oct`, `2019-October` are all valid date formats. 

See the progress of https://github.com/epogrebnyak/weo-reader/issues/9 for complete date listing.


### Play with data

Use `WEO` class to view and extract data. `WEO` is a wrapper around a pandas dataframe that ensures proper data import and easier access/slicing of data.

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

See some data:

```python

w.get("General government gross debt", "Percent of GDP")
w.getc("NGDP_RPCH")
w.country("DEU", 2018)
```

Plot a chart:

```python
w.gdp_usd(2024).head(20).sort_values().plot.barh(title="GDP by country, USD bln (2024)")
```

## Alternatives

1. If you need the latest data and not the vintages of WEO releases, and you know 
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

2. Similar dataset, not updated since 2018, but has earlier years: https://github.com/datasets/imf-weo

## Development notes

- You can download the WEO file in command line with `curl` command:
```
curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls
```
- `WEOOct2019all.xls` from the web site is really a CSV file, not an Excel file.
- You cannot get [June 2020 GDP update][jun2020] with this client as the update has a different table structure.

[jun2020]: https://www.imf.org/en/Publications/WEO/Issues/2020/06/24/WEOUpdateJune2020
