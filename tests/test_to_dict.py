from chameleon import Chameleon


def test_to_dict_plain():
    c = Chameleon({"a": 1, "b": "x"})
    d = c.to_dict()
    assert d == {"a": 1, "b": "x"}
    assert type(d) is dict


def test_to_dict_nested_chameleon():
    c = Chameleon({"a": Chameleon({"b": 1})})
    d = c.to_dict()
    assert d == {"a": {"b": 1}}
    assert type(d["a"]) is dict


def test_to_dict_in_list():
    c = Chameleon({"items": [Chameleon({"a": 1})]})
    assert c.to_dict() == {"items": [{"a": 1}]}


def test_to_dict_in_tuple():
    c = Chameleon({"items": (Chameleon({"a": 1}), 2)})
    d = c.to_dict()
    assert d == {"items": ({"a": 1}, 2)}
    assert isinstance(d["items"], tuple)


def test_to_dict_in_plain_dict():
    c = Chameleon({"a": {"b": Chameleon({"c": 1})}})
    assert c.to_dict() == {"a": {"b": {"c": 1}}}


def test_to_dict_deep_nesting():
    c = Chameleon({"a": [{"b": (Chameleon({"c": 1}),)}]})
    assert c.to_dict() == {"a": [{"b": ({"c": 1},)}]}
