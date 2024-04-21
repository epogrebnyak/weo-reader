from pytest import mark

@mark.skip
def test_version():
    from weo import __version__
    assert __version__ >= "0.5.0"
