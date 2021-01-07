from weo import WEO, download

download("2020-Oct", path="weo.csv", overwrite=True)

w = WEO("weo.csv")

# What is inside?
w.variables()  # [('Gross domestic product, constant prices', 'National currency', 'NGDP_R'),
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
w.getc("NGDPDPC")
w.country("DEU", 2018)

# Plot a chart
w.gdp_usd(2020).dropna().sort_values().tail(12).plot.barh(title="GDP by country, USD billion (2020)")
