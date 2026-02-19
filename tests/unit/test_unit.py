from server import clean_name


def test_clean_name():
    res = clean_name(" test ")

    assert res == "test"
