from weo import dates, all_dates


def test_dates():
    assert dates(2007) == ["2007-Oct"]
    assert dates(2011) == ["2011-Apr", "2011-Sep"]
    assert dates(2020) == ["2020-Apr"]


def test_all_dates():
    assert all_dates()[0] == "2007-Oct"
