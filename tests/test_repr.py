from chameleon import Chameleon


def test_repr_empty():
    assert repr(Chameleon()) == "Chameleon({})"


def test_repr_plain():
    assert repr(Chameleon({"a": 1})) == "Chameleon({'a': 1})"


def test_repr_nested():
    assert repr(Chameleon({"a": Chameleon({"b": 1})})) == "Chameleon({'a': Chameleon({'b': 1})})"
