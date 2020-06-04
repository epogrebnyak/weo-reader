from weo import download, WEO

download(year=2019, period=2, path="weo_2019_2.csv", overwrite=True)

w = WEO("weo_2019_2.csv")

# What is inside?
w.variables() # [('Gross domestic product, constant prices', 'National currency', 'NGDP_R'), 
# ... ('Current account balance', 'Percent of GDP', 'BCA_NGDPD')]
w.units()
w.units("Gross domestic product, current prices")
w.codes
w.from_code("LUR")

# Countries
w.countries("United")  # Dataframe with United Arab Emirates, United Kingdom
# and United States
w.iso_code3("Netherlands")  # 'NLD'

# Get some data
w.get("General government gross debt", "Percent of GDP")
w.getc("NGDP_RPCH")
w.gdp_usd(2024).head(20).sort_values().plot.barh(title="GDP by country, USD bln (2024)")
w.country("DEU", 2018)
