import pytest

from chameleon import Chameleon


def test_patch_sets_and_restores_existing():
    c = Chameleon({"a": 1})
    with c.patch("a", 2):
        assert c.a == 2
    assert c.a == 1


def test_patch_removes_new_top_level_key():
    c = Chameleon()
    with c.patch("a", 1):
        assert c.a == 1
    assert "a" not in c


def test_patch_removes_new_intermediate_nodes():
    c = Chameleon()
    with c.patch("a.b.c", 1):
        assert c["a"]["b"]["c"] == 1
    assert c == {}


def test_patch_keeps_existing_intermediate_nodes():
    c = Chameleon({"a": {"x": 1}})
    with c.patch("a.b", 2):
        assert c["a"] == {"x": 1, "b": 2}
    assert c == {"a": {"x": 1}}


def test_patch_keeps_sibling_created_by_user():
    c = Chameleon()
    with c.patch("a.b", 1):
        c["a"]["extra"] = 2
    assert c == {"a": {"extra": 2}}


def test_patch_restores_old_value_after_user_overwrite():
    c = Chameleon({"a": 1})
    with c.patch("a", 2):
        c.a = 99
    assert c.a == 1


def test_patch_restores_after_user_delete():
    c = Chameleon({"a": 1})
    with c.patch("a", 2):
        del c.a
    assert c.a == 1


def test_patch_restores_on_exception():
    c = Chameleon({"a": 1})
    with pytest.raises(RuntimeError):
        with c.patch("a", 2):
            raise RuntimeError("boom")
    assert c.a == 1


def test_patch_through_non_mapping_raises():
    c = Chameleon({"a": 5})
    with pytest.raises(TypeError, match="crosses non-mapping at 'a'"):
        with c.patch("a.b", 1):
            pass


def test_patch_through_non_mapping_does_not_create():
    c = Chameleon({"a": 5})
    with pytest.raises(TypeError):
        with c.patch("a.b.c", 1):
            pass
    assert c == {"a": 5}


def test_patch_through_plain_dict():
    c = Chameleon({"a": {"b": 1}})
    with c.patch("a.c", 2):
        assert c["a"] == {"b": 1, "c": 2}
    assert c["a"] == {"b": 1}


def test_patch_arbitrary_value():
    c = Chameleon()
    marker = object()
    with c.patch("a", marker):
        assert c.a is marker
    assert "a" not in c


@pytest.mark.parametrize("path", ["", "a..b", ".a", "a.", ".."])
def test_patch_invalid_path_raises(path):
    c = Chameleon()
    with pytest.raises(ValueError):
        with c.patch(path, 1):
            pass


def test_patch_invalid_path_does_not_mutate():
    c = Chameleon()
    with pytest.raises(ValueError):
        with c.patch("", 1):
            pass
    assert c == {}


def test_patch_tolerates_deleted_intermediate():
    c = Chameleon()
    with c.patch("a.b", 1):
        assert c.a.b == 1
        del c.a
    assert c == {}
