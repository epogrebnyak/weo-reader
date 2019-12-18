import random
import pytest
from weo import (WEO_Error,
                 download, convert, url,
                 WEO)


@pytest.fixture
def w():
    yield WEO('weo.csv')  # FIXME: weo.csv location not guaranteed


def test_url_special_case_september():
    assert url(
        2011,
        2) == 'https://www.imf.org/external/pubs/ft/weo/2011/02/weodata/WEOSep2011all.xls'


def test_url_wrong_year():
    with pytest.raises(WEO_Error):
        url(2000, 1)


def test_download():
    with pytest.raises(WEO_Error):
        download('a.txt', 2019, 3)


def test_convert():
    assert convert("9,902.554") == 9902.554


def test_countries(w):
    assert len(w.countries()) == 194


def test_country_name(w):
    assert w.country_name('DZA') == 'Algeria'


def test_iso_code(w):
    w.iso_code('Neth') == 'NLD'


def test_code(w):
    assert w.from_code('LUR') == \
        ('Unemployment rate', 'Percent of total labor force')
    assert w.from_code('LP') == \
        ('Population', 'Persons')


def test_number_of_variables(w):
    assert len(w.variables) == len(w.codes)


def test_getc(w):
    c = random.choice(w.codes)
    df = w.getc(c)
    assert df.shape == (45, 194)


def test_getc(w):
    s, u, _ = random.choice(w.variables)
    df = w.get(s, u)
    assert df.shape == (45, 194)


def test_units(w):
    assert w.units(random.choice(w.subjects))
