from weo import get


def test_example_readme_py():
    w = get(2019, "Oct", "weo_2019_1.csv")

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
    w = get(2020, "Apr", "weo_2020_1.csv")
    _ = [w.getc(x).head() for (s, u, x) in w.variables()]
