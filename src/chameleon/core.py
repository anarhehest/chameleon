from __future__ import annotations

import contextlib
from copy import deepcopy as _deepcopy


class Chameleon(dict):
    _strict = False

    def __init__(self, *args, strict=False, **kwargs):
        object.__setattr__(self, "_strict", strict)
        self.update(*args, **kwargs)

    def _wrap_value(self, value):
        if isinstance(value, Chameleon):
            return value
        if isinstance(value, dict):
            return Chameleon(value, strict=self._strict)
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, self._wrap_value(value))

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def setdefault(self, key, default=None):
        if key in self:
            return self[key]
        self[key] = default
        return self[key]

    def __ior__(self, other):
        self.update(other)
        return self

    @classmethod
    def fromkeys(cls, iterable, value=None):
        result = cls()
        wrapped = result._wrap_value(value)
        for k in iterable:
            result[k] = wrapped
        return result

    def __getattr__(self, name):
        if (name.startswith("__") and name.endswith("__")) or name in _RESERVED:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        try:
            return self[name]
        except KeyError:
            if self._strict:
                raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
            child = Chameleon(strict=False)
            self[name] = child
            return child

    def __setattr__(self, name, value):
        if (name.startswith("__") and name.endswith("__")) or name in _RESERVED:
            raise AttributeError(f"{name!r} is reserved; use c[{name!r}] = ... instead")
        self[name] = value

    def __delattr__(self, name):
        if (name.startswith("__") and name.endswith("__")) or name in _RESERVED:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    @contextlib.contextmanager
    def patch(self, path, value):
        keys = path.split(".")
        if not all(keys):
            raise ValueError(f"invalid path: {path!r}")

        created = []
        node = self

        try:
            for key in keys[:-1]:
                if key in node:
                    child = node[key]
                    if not isinstance(child, dict):
                        raise TypeError(
                            f"path {path!r} crosses non-mapping at {key!r} ({type(child).__name__})"
                        )
                    node = child
                    continue
                child = Chameleon(strict=self._strict)
                node[key] = child
                created.append((node, key))
                node = child

            last = keys[-1]
            had_key = last in node
            old_value = node[last] if had_key else None
            node[last] = value
            try:
                yield
            finally:
                if had_key:
                    node[last] = old_value
                else:
                    node.pop(last, None)
        finally:
            for parent, key in reversed(created):
                child = parent.get(key)
                if isinstance(child, Chameleon) and not child:
                    del parent[key]

    def to_dict(self):
        def convert(v):
            if isinstance(v, dict):
                return {k: convert(x) for k, x in v.items()}
            if isinstance(v, list):
                return [convert(x) for x in v]
            if isinstance(v, tuple):
                return tuple(convert(x) for x in v)
            return v

        return convert(self)

    def copy(self):
        return type(self)(self, strict=self._strict)

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        cls = type(self)
        new = cls(strict=self._strict)
        memo[id(self)] = new
        for k, v in self.items():
            new[_deepcopy(k, memo)] = _deepcopy(v, memo)
        return new

    def __repr__(self):
        return f"Chameleon({dict.__repr__(self)})"


_RESERVED = frozenset(dir(dict)) | frozenset(dir(Chameleon))
