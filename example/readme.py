import weo
from weo import WEO

weo.download(year=2020, release="Oct", filename="weo.csv")

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
w.getc("NGDP_RPCH")
w.country("DEU")
w.fix_year(1994)

# Plot a chart
w.gdp_usd(2024).dropna().sort_values().tail(12).plot.barh(
    title="GDP by country, USD billion (2024)"
)

# Get data from year range
w.gdp_pc_usd(start_year=2000, end_year=2020)
