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