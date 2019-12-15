import pytest
from weo import WEO_Period_Error, download, convert, WEO


def test_download():
    with pytest.raises(WEO_Period_Error):
       download('a.txt', 2030, 3)

def test_convert():    
    assert convert("9,902.554") == 9902.554
    
    
def test_iso_code():        
    w = WEO('weo.csv') # weo.csv location not guaranteed
    w.iso_code('Neth') == 'NLD'    