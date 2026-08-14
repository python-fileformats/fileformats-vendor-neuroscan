def test_extras_pkg_import():

    import fileformats.extras.vendor.neuroscan

    assert (
        fileformats.extras.vendor.neuroscan.__name__
        == "fileformats.extras.vendor.neuroscan"
    )
