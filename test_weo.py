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


def test_varibale_list_length(w):
    assert len(w.variables()) == len(w.codes())


def test_country_name(w):
    assert w.country_name('DZA') == 'Algeria'


def test_iso_code(w):
    w.iso_code('Neth') == 'NLD'


def test_code(w):
    return w.code('LUR') == \
        ('Unemployment rate', 'Percent of total labor force')
