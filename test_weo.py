from weo import convert, WEO

def test_convert():    
    assert convert("9,902.554") == 9902.554
    
    
def test_iso_code():        
    w = WEO('weo.csv') # not guaranteed 
    w.iso_code('Neth') == 'NLD'    