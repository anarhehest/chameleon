import pytest

from chameleon import Chameleon


def test_strict_missing_attribute_raises():
    c = Chameleon(strict=True)
    with pytest.raises(AttributeError, match="missing"):
        c.missing


def test_strict_existing_attribute_works():
    c = Chameleon({"a": 1}, strict=True)
    assert c.a == 1


def test_strict_does_not_auto_vivify():
    c = Chameleon(strict=True)
    with pytest.raises(AttributeError):
        c.a
    assert "a" not in c


def test_strict_not_inherited_by_children():
    c = Chameleon()
    c["x"] = Chameleon(strict=True)
    with pytest.raises(AttributeError):
        c.x.typo


def test_strict_flag_stored_out_of_band():
    c = Chameleon(strict=True)
    assert "_strict" not in c
    assert c == {}


def test_strict_default_false():
    c = Chameleon()
    assert c.__dict__.get("_strict") is False
