# weo-reader

1. The program uses Python 3.6. To install `weo` as a python package use:

`pip install weo`
   
   
2. You need the data saved as a local file.  Download latest WEO country data file from IMF web site (for example as `weo.csv`). 

You can do it manually in a command line with `curl` command:

```
curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls
```

Please note `WEOOct2019all.xls` is in fact a tab-delimited CSV file. 

Alternatively, can use `weo.download()` function:

```python 
from weo import download

download('weo.csv', 2019, 2)
```

2. Use `WEO` class from `weo` package or `weo.py` to view and extract data. `WEO` is a wrapper around a by-country pandas dataframe that ensures proper data import and easier access to it.

3. Things to try in a REPL, by line:

```python
from weo import WEO

w = WEO('weo.csv') 

# What is inside?
w.variables()
w.units()    
w.units('Gross domestic product, current prices')
w.find_countries('United')
w.iso_code('Netherlands')

# Get some data
w.get('General government gross debt', 'Percent of GDP')
w.gdp_usd(2024).head(20).sort_values().plot.barh(title="GDP by country, USD bln (2024)")
```

## Dev notes

-  `WEOOct2019all.xls` file from the web site is really a CSV file.
