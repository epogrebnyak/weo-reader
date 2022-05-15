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

import weo

weo.download(year=2020, release="Oct", filename="weo.csv")

import pathlib
import weo

# create folder 
pathlib.Path("weo_data").mkdir(parents=False, exist_ok=True)

# download all releases
for (year, release) in weo.all_releases():
  weo.download(year, release, directory="weo_data")

from weo import WEO

w = WEO("weo.csv")

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


w.get("General government gross debt", "Percent of GDP")
w.getc("NGDP_RPCH")
w.country("DEU")
w.fix_year(1994)

(w.gdp_usd(2024)
  .dropna()
  .sort_values()
  .tail(12)
  .plot
  .barh(title="GDP by country, USD billion (2024)")
)

w.gdp_pc_usd(start_year=2000, end_year=2020)

from dbnomics import fetch_series_by_api_link
ts1 = fetch_series_by_api_link("https://api.db.nomics.world/v22/"
                               "series/IMF/WEO:latest/DEU.PCPI"
                               "?observations=1")
