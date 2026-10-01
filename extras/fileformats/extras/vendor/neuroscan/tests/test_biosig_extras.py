def test_extras_pkg_import():

    import fileformats.extras.vendor.neuroscan

    pkg_name = fileformats.extras.vendor.neuroscan.__name__
    assert pkg_name == "fileformats.extras.vendor.neuroscan"


def test_neuroscan_deidentify_takes_no_recipe():
    """Implementations that don't take a recipe annotate it with `None`"""
    import typing as ty

    from fileformats.biosig import Biosig
    from fileformats.core import LoadedMarker, find_extra_implementation
    from fileformats.vendor.neuroscan import Neuroscan

    impl = find_extra_implementation(Biosig.deidentify, Neuroscan)
    hint = ty.get_type_hints(impl, include_extras=True)["recipe"]
    assert hint is type(None)
    assert LoadedMarker.from_hint(hint) is None
