import pytest
import copy

from chameleon import Chameleon


def test_copy_returns_chameleon():
    c = Chameleon({"a": 1})
    c1 = c.copy()
    assert isinstance(c1, Chameleon)
    assert c1 == c
    assert c1 is not c


def test_copy_is_shallow():
    c = Chameleon({"nested": Chameleon({"x": 1})})
    c1 = c.copy()
    assert c1["nested"] is c["nested"]


def test_copy_preserves_strict():
    c = Chameleon(strict=True)
    assert isinstance(c.copy(), Chameleon)
    with pytest.raises(AttributeError):
        c.copy().missing


def test_copy_copy_returns_chameleon():
    c = Chameleon({"a": 1})
    assert isinstance(copy.copy(c), Chameleon)


def test_copy_deepcopy_returns_chameleon():
    c = Chameleon({"a": 1})
    assert isinstance(copy.deepcopy(c), Chameleon)


def test_deepcopy_is_deep():
    c = Chameleon({"nested": Chameleon({"x": 1})})
    d = copy.deepcopy(c)
    assert d["nested"] is not c["nested"]
    assert d["nested"] == c["nested"]


def test_deepcopy_preserves_strict_on_children():
    c = Chameleon(strict=True)
    d = copy.deepcopy(c)
    with pytest.raises(AttributeError):
        d.typo


def test_deepcopy_handles_cycle():
    c = Chameleon()
    c.x = c
    d = copy.deepcopy(c)
    assert d.x is d
