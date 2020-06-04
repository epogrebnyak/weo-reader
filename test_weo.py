import os
import random
import pytest  # type: ignore

from weo import WEO_Error, download, convert, make_url, WEO

# persist file for testing
path = "weo_2019_2.csv"
if not os.path.exists(path):
    download(2019, 2, path)


@pytest.fixture
def w():
    yield WEO(path)


def test_url_special_case_september():
    assert (
        make_url(2011, 2, "all")
        == "https://www.imf.org/external/pubs/ft/weo/2011/02/weodata/WEOSep2011all.xls"
    )


def test_donaload_raises_on_wrong_year():
    with pytest.raises(WEO_Error):
        download(1999, 1, "a.txt")


def test_download_raises_on_wrong_period():
    with pytest.raises(WEO_Error):
        download(2019, 3, "a.txt")


def test_convert():
    assert convert("9,902.554") == 9902.554


def test_variables(w):
    assert w.variables("current account") == [
        ("Current account balance", "U.S. dollars", "BCA"),
        ("Current account balance", "Percent of GDP", "BCA_NGDPD"),
    ]


def test_countries(w):
    assert len(w.countries()) == 194


def test_country(w):
    assert w.country("DE").equals(w.country("DEU"))


def test_country_name(w):
    assert w.country_name("DZA") == "Algeria"


def test_country_name_alpha2(w):
    assert w.country_name("LT") == "Lithuania"


def test_iso_code(w):
    assert w.iso_code3("Neth") == "NLD"
    assert w.iso_code2("Neth") == "NL"


def test_code(w):
    assert w.from_code("LUR") == ("Unemployment rate", "Percent of total labor force")
    assert w.from_code("LP") == ("Population", "Persons")


def test_number_of_variables(w):
    assert len(w.variables()) == len(w.codes)


def test_getc(w):
    c = random.choice(w.codes)
    df = w.getc(c)
    assert df.shape == (45, 194)


def test_get(w):
    s, u, _ = random.choice(w.variables())
    df = w.get(s, u)
    assert df.shape == (45, 194)


def test_units(w):
    assert w.units(random.choice(w.subjects))


def test_nlargest(w):
    assert w.nlargest(n=10, year=2018) == [
        "USA",
        "CHN",
        "JPN",
        "DEU",
        "GBR",
        "FRA",
        "IND",
        "ITA",
        "BRA",
        "KOR",
    ]


def test_example_readme_py():
    from weo import download, WEO

    download(year=2019, period=2, path="weo_2019_2.csv", overwrite=True)

    w = WEO("weo_2019_2.csv")

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
    w = download(year=2020, period=1, path="2020_April.csv", overwrite=True)
    _ = [w.getc(x).head() for (s, u, x) in w.variables()]
