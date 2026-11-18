from chameleon import Chameleon


def test_missing_attribute_auto_vivifies():
    c = Chameleon()
    child = c.missing
    assert isinstance(child, Chameleon)
    assert c["missing"] is child


def test_nested_auto_vivification():
    c = Chameleon()
    c.a.b.c = 1
    assert c["a"]["b"]["c"] == 1
    assert isinstance(c.a, Chameleon)
    assert isinstance(c.a.b, Chameleon)


def test_auto_vivification_persists():
    c = Chameleon()
    c.a
    assert "a" in c
