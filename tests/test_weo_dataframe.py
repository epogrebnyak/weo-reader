import os
import random

import pytest  # type: ignore

from weo import WEO, download
from weo.dataframe import WEO_ParsingError, convert, alpha3_to_2

# persist file for testing
path = "weo_2019_2.csv"
if not os.path.exists(path):
    download(year=2019, release="October", filename=path)


@pytest.fixture
def w():
    yield WEO(path)


def test_wbg():
    assert alpha3_to_2("WBG") # does not fail

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
