import copy
import pickle
import string

import pytest
from hypothesis import given, strategies as st

from chameleon import Chameleon, _RESERVED


def test_attribute_read_returns_item():
    c = Chameleon({"a": 1, "b": "two"})
    assert c.a == 1
    assert c.b == "two"


def test_attribute_write_writes_item():
    c = Chameleon()
    c.x = 42
    assert c["x"] == 42
    assert c.x == 42


def test_attribute_delete_deletes_item():
    c = Chameleon({"x": 1})
    del c.x
    assert "x" not in c


def test_attribute_delete_missing_raises():
    c = Chameleon()
    with pytest.raises(AttributeError):
        del c.nope


def test_item_access_still_works():
    c = Chameleon()
    c["k"] = 1
    assert c["k"] == 1
    assert c.k == 1


# ------------------------------------------- property-based invariants

_lower = string.ascii_lowercase
_safe_key = st.text(min_size=1, max_size=8, alphabet=_lower)
_safe_path = st.lists(_safe_key, min_size=1, max_size=4, unique=True)


@given(keys=_safe_path, value=st.integers())
def test_patch_leaves_mapping_unchanged(keys, value):
    c = Chameleon()
    path = ".".join(keys)
    before = c.to_dict()
    with c.patch(path, value):
        pass
    assert c.to_dict() == before


@given(keys=_safe_path, value=st.integers())
def test_patch_exposes_value_inside_block(keys, value):
    c = Chameleon()
    path = ".".join(keys)
    with c.patch(path, value):
        node = c
        for k in keys[:-1]:
            node = node[k]
        assert node[keys[-1]] == value


@given(
    data=st.dictionaries(
        keys=st.text(min_size=1, alphabet=_lower),
        values=st.integers(),
        max_size=5,
    )
)
def test_to_dict_roundtrip(data):
    assert Chameleon(data).to_dict() == data
