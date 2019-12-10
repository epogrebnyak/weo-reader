# weo-reader


1. Manyally Download latest WEO data file from IMF web site as `weo.csv`, example:

```
curl -o weo.csv https://www.imf.org/external/pubs/ft/weo/2019/02/weodata/WEOOct2019all.xls
```

Caveat: `.xls` from the web site is really a CSV file.

2. Use `WEO` class from `weo.py` to view and extract data. `WEO` is a wrapper around a by-country pandas dataframe that ensures proper import and easier access to data.
