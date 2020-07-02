# weo-reader

This is a third-party Python client to download [IMF World Economic Outlook Report][weo] dataset and use it as [pandas](https://pandas.pydata.org/) dataframe. 

You can download WEO releases by year and month and explore the dataset.

[weo]: https://www.imf.org/en/Publications/WEO

## Install

The program uses Python 3.6. To install `weo` as a python package use:

`pip install weo`
   
## Start using   

### Download 
   
You need the data saved as a local file.  Download latest WEO country data file from IMF web site as shown below:

```python 
from weo import download


download("2019-Oct", path='weo.csv', overwrite=True)
```

### Read and try

Use `WEO` class to view and extract data. `WEO` is a wrapper around a by-country pandas dataframe that ensures proper data import and easier access to data.

Somehting to try:

```python
from weo import WEO

w = WEO("weo.csv")

# What is inside?
# - variable listing
w.variables()
# - units
w.units()
w.units("Gross domestic product, current prices")
# - variable codes
w.codes
w.from_code("LUR")
# - countries
w.countries("United")      # Dataframe with United Arab Emirates, United Kingdom
                           # and United States
w.iso_code3("Netherlands") # 'NLD'

# Get some data
w.get("General government gross debt", "Percent of GDP")
w.getc("NGDP_RPCH")
w.gdp_usd(2024).head(20).sort_values().plot.barh(title="GDP by country, USD bln (2024)")
w.country("DEU", 2018)
```

## Alternatives

1. If you need the latest data and not the vintages of WEO releases, and you know 
variables that you are looking for, *dbnomics* is a good choice: 
- <https://db.nomics.world/IMF/WEO>
- <https://db.nomics.world/IMF/WEOAGG>

Small example:

```
from dbnomics import fetch_series_by_api_link
ts1 = fetch_series_by_api_link("https://api.db.nomics.world/v22/series/IMF/WEO/DEU.NGDPRPC?observations=1")
```

2. Similar dataset, but not updated since 2018 (has earlier years): https://github.com/datasets/imf-weo

## Development notes

- You can download the WEO file in command line with `curl` command:
```
curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls
```
- `WEOOct2019all.xls` from the web site is really a CSV file, not an Excel file.
