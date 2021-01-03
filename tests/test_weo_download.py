import pytest
from weo.download import from_date, make_url_countries, Release, download
from weo.dates import WEO_DateError


def test_from_date():
    assert from_date("2020-04") == Release(year=2020, month=4)
    assert from_date("2019-Oct") == Release(year=2019, month=10)


def test_from_date_fails():
    with pytest.raises(WEO_DateError):
        from_date("2020-01")


def test_make_countries_url():
    assert (
        make_url_countries(from_date("2020-04"))
        == "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/WEOApr2020all.xls"
    )


def test_url_september():
    assert (
        make_url_countries(from_date("2011-Sep"))
        == "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2011/WEOSep2011all.xls"
    )


def test_download_raises_on_wrong_year():
    with pytest.raises(WEO_DateError):
        download("1999-Apr", "_.txt")


def test_download_raises_on_wrong_period():
    with pytest.raises(WEO_DateError):
        download("2019-Feb", "_.txt")
