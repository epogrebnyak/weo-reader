from weo.dates import (
    Date,
    all_releases,
    current,
    download,
    first,
    get_season,
    make_url_countries,
    month_str,
    succ,
    validate,
)


def test_constructor():
    d1 = Date(2020, 1)
    d2 = Date(2020, 2)


def foo(a, b):
    pass


def test_download():
    assert download(year=2020, release=1, fetch=foo) == (
        "weo_2020_1.csv",
        "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/WEOApr2020all.xls",
    )


def test_get_season():
    assert get_season("September") == 2


def test_validate():
    validate(Date(2020, 1))


def test_url_countries():
    assert (
        make_url_countries(Date(2020, 1))
        == "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/WEOApr2020all.xls"
    )
    assert (
        make_url_countries(Date(2020, 2))
        == "https://www.imf.org/-/media/Files/Publications/WEO/WEO-Database/2020/02/WEOOct2020all.xls"
    )


def test_month_str():
    assert month_str(Date(2011, 2)) == "Sep"


def test_le():
    assert first() <= current()


def test_succ():
    assert succ(Date(2020, 2)) == Date(2021, 1)


def test_all_releases():
    assert all_releases()[0] == (2007, 2)
