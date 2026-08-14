def test_pkg_import():

    import fileformats.vendor.neuroscan

    assert fileformats.vendor.neuroscan.__name__ == "fileformats.vendor.neuroscan"
