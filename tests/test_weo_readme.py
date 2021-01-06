import pytest

from weo import get

w1 = get(2019, "Oct")
w2 = get(2020, "Apr")


def test_example_readme_py():
    w = w1

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
    w.country("DEU", 2018)


def test_plot():
    w = w1
    w.gdp_usd(2024).head(20).sort_values().plot.barh(
        title="GDP by country, USD bln (2024)"
    )


@pytest.mark.parametrize("w", [w1, w2])
def test_getc_in_2020_April(w):
    for (s, u, x) in w.variables():
        w.getc(x).head()
