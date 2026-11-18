import pytest

from chameleon import Chameleon, _RESERVED

RESERVED_NAMES = [
    "items",
    "keys",
    "values",
    "get",
    "update",
    "pop",
    "setdefault",
    "copy",
    "clear",
    "popitem",
    "fromkeys",
    "patch",
    "to_dict",
]


@pytest.mark.parametrize("name", RESERVED_NAMES)
def test_setattr_reserved_raises(name):
    c = Chameleon()
    with pytest.raises(AttributeError, match=name):
        setattr(c, name, 1)


@pytest.mark.parametrize("name", RESERVED_NAMES)
def test_delattr_reserved_raises(name):
    c = Chameleon()
    with pytest.raises(AttributeError):
        delattr(c, name)


@pytest.mark.parametrize("name", RESERVED_NAMES)
def test_getattr_reserved_returns_method_not_item(name):
    c = Chameleon()
    c[name] = "shadow"
    attr = getattr(c, name)
    assert attr != "shadow"
    assert callable(attr)
    assert c[name] == "shadow"


def test_item_access_to_reserved_name_works():
    c = Chameleon()
    c["items"] = 42
    assert c["items"] == 42
    assert c.items != 42


def test_reserved_covers_dict_and_class_methods():
    for name in ("items", "keys", "values", "get", "update", "pop", "patch", "to_dict"):
        assert name in _RESERVED
