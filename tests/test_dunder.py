import pytest

from chameleon import Chameleon


def test_dunder_getattr_raises():
    c = Chameleon()
    with pytest.raises(AttributeError):
        c.__nonexistent__


def test_dunder_getattr_does_not_create():
    c = Chameleon()
    with pytest.raises(AttributeError):
        c.__nonexistent__
    assert "__nonexistent__" not in c


@pytest.mark.parametrize("name", ["__class__", "__init__", "__dict__", "__getattr__"])
def test_dunder_setattr_raises(name):
    c = Chameleon()
    with pytest.raises(AttributeError):
        setattr(c, name, 1)


def test_non_dunder_with_trailing_underscores_is_allowed():
    # name ending with '__' but not starting with '__' is a valid key
    c = Chameleon()
    c.foo__ = 1
    assert c["foo__"] == 1
