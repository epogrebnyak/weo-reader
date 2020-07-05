from weo import download, WEO

def test_example_readme_py():
    download("2019-Oct", "weo.csv", overwrite=True)

    w = WEO("weo.csv")

    # What is inside?
    w.variables()
    w.units()
    w.units("Gross domestic product, current prices")
    w.codes
    w.from_code("LUR")

    # Countries
    w.countries("United")
    w.iso_code3("Netherlands")

    # Get some data
    w.get("General government gross debt", "Percent of GDP")
    w.getc("NGDP_RPCH")
    w.gdp_usd(2024).head(20).sort_values().plot.barh(
        title="GDP by country, USD bln (2024)"
    )
    w.country("DEU", 2018)


def test_2020_April():
    download("2020-Apr", path="2020_April.csv", overwrite=True)
    w = WEO("2020_April.csv") 
    _ = [w.getc(x).head() for (s, u, x) in w.variables()]
