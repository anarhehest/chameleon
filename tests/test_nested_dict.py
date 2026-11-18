import copy
import pytest

from chameleon import Chameleon


def test_init_wraps_nested_plain_dict():
    c = Chameleon({"a": {"b": 1}})
    assert isinstance(c["a"], Chameleon)
    assert c.a.b == 1


def test_init_deeply_nested():
    c = Chameleon({"a": {"b": {"c": 1}}})
    assert c.a.b.c == 1
    assert isinstance(c.a.b, Chameleon)


def test_setitem_wraps_plain_dict():
    c = Chameleon()
    c["a"] = {"b": 1}
    assert isinstance(c["a"], Chameleon)
    assert c.a.b == 1


def test_setattr_wraps_plain_dict():
    c = Chameleon()
    c.a = {"b": 1}
    assert isinstance(c.a, Chameleon)
    assert c.a.b == 1


def test_update_wraps_plain_dict():
    c = Chameleon()
    c.update({"a": {"b": 1}})
    assert isinstance(c["a"], Chameleon)
    assert c.a.b == 1


def test_setdefault_wraps_plain_dict():
    c = Chameleon()
    result = c.setdefault("a", {"b": 1})
    assert isinstance(result, Chameleon)
    assert result is c["a"]
    assert c.a.b == 1


def test_fromkeys_wraps_plain_dict():
    c = Chameleon.fromkeys(["a", "b"], {"x": 1})
    assert isinstance(c["a"], Chameleon)
    assert c.a.x == 1
    assert c["a"] is c["b"]  # shared, matches dict.fromkeys


def test_ior_wraps_plain_dict():
    c = Chameleon()
    c |= {"a": {"b": 1}}
    assert isinstance(c.a, Chameleon)
    assert c.a.b == 1


def test_chameleon_value_not_rewrapped():
    inner = Chameleon({"b": 1})
    c = Chameleon({"a": inner})
    assert c["a"] is inner


def test_strict_propagates_to_nested():
    c = Chameleon({"a": {"b": 1}}, strict=True)
    with pytest.raises(AttributeError):
        c.a.missing


def test_setitem_wraps_with_parent_strict():
    c = Chameleon(strict=True)
    c["a"] = {"b": 1}
    with pytest.raises(AttributeError):
        c.a.missing


def test_nested_dict_in_list_not_wrapped():
    # documented behavior: lists are opaque
    c = Chameleon({"items": [{"a": 1}]})
    assert isinstance(c["items"], list)
    assert type(c["items"][0]) is dict


def test_original_dict_not_mutated():
    src = {"a": {"b": 1}}
    inner = src["a"]
    c = Chameleon(src)
    assert src["a"] is inner
    assert c["a"] is not inner


def test_patch_wraps_plain_dict():
    c = Chameleon()
    with c.patch("a.b", {"x": 1}):
        assert isinstance(c.a.b, Chameleon)
        assert c.a.b.x == 1
    assert c == {}


def test_deepcopy_normalizes_legacy_plain_dict():
    # a legacy Chameleon with a plain dict child (pre-fix) gets fixed on deepcopy
    c = Chameleon()
    dict.__setitem__(c, "a", {"b": 1})  # bypass wrapper, simulate legacy
    d = copy.deepcopy(c)
    assert isinstance(d["a"], Chameleon)
    assert d.a.b == 1
