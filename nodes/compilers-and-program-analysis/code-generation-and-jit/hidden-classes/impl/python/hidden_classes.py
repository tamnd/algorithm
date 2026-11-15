# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-classes/. The authors are listed in prov/S7XDVF.jsonl.

"""Hidden classes (shapes) for a small dynamic object model.

An object has a class, for methods, and its own properties, which can be
added at any time. The layout of the own properties is described by a shape.
Shapes form a tree: each class has a root shape with no properties, and adding
a property follows, or creates, a transition to a child shape. Objects that
got the same properties in the same order share one shape and store their
values at the same offsets. Deleting a property moves the object to
dictionary mode, where it has no shape.

A load inline cache keyed by shapes caches, per site, either the offset of an
own property or the method found through the class chain.
"""

from __future__ import annotations

from dataclasses import dataclass, field

UNINITIALIZED = "uninitialized"
MONOMORPHIC = "monomorphic"
POLYMORPHIC = "polymorphic"
MEGAMORPHIC = "megamorphic"

MISSING = ("missing",)


@dataclass(frozen=True)
class Method:
    owner: str
    name: str
    ident: int


@dataclass(eq=False)
class Klass:
    name: str
    parent: Klass | None = None
    methods: dict[str, Method] = field(default_factory=dict)
    root: Shape | None = None

    def chain(self) -> list[Klass]:
        out: list[Klass] = []
        k: Klass | None = self
        while k is not None:
            out.append(k)
            k = k.parent
        return out


class Shape:
    """An immutable layout: the class, and the own property names with their offsets."""

    __slots__ = ("klass", "parent", "key", "offsets", "transitions", "ident")

    def __init__(self, klass: Klass, parent: Shape | None, key: str | None, ident: int) -> None:
        self.klass = klass
        self.parent = parent
        self.key = key
        self.ident = ident
        self.offsets: dict[str, int] = dict(parent.offsets) if parent is not None else {}
        if key is not None:
            self.offsets[key] = len(self.offsets)
        self.transitions: dict[str, Shape] = {}

    def names(self) -> list[str]:
        """The property names in the order in which they were added."""
        out: list[str] = []
        s: Shape | None = self
        while s is not None and s.key is not None:
            out.append(s.key)
            s = s.parent
        return out[::-1]


class Obj:
    __slots__ = ("klass", "shape", "slots", "dictionary")

    def __init__(self, klass: Klass) -> None:
        self.klass = klass
        self.shape: Shape | None = klass.root
        self.slots: list[object] = []
        self.dictionary: dict[str, object] | None = None


class Runtime:
    def __init__(self) -> None:
        self.classes: dict[str, Klass] = {}
        self.sites: list[LoadIC] = []
        self.shape_count = 0
        self._next = 0

    def _new_shape(self, klass: Klass, parent: Shape | None, key: str | None) -> Shape:
        self.shape_count += 1
        return Shape(klass, parent, key, self.shape_count)

    def define_class(self, name: str, parent: str | None = None) -> Klass:
        if name in self.classes:
            raise ValueError("class already defined: " + name)
        k = Klass(name, self.classes[parent] if parent is not None else None)
        k.root = self._new_shape(k, None, None)
        self.classes[name] = k
        return k

    def _changed(self, d: Klass) -> None:
        for site in self.sites:
            site.invalidate(d)

    def set_method(self, cls: str, name: str) -> Method:
        d = self.classes[cls]
        self._changed(d)
        self._next += 1
        m = Method(cls, name, self._next)
        d.methods[name] = m
        return m

    def remove_method(self, cls: str, name: str) -> None:
        d = self.classes[cls]
        if name in d.methods:
            self._changed(d)
            del d.methods[name]

    def new(self, cls: str) -> Obj:
        return Obj(self.classes[cls])

    def transition(self, shape: Shape, key: str) -> Shape:
        child = shape.transitions.get(key)
        if child is None:
            child = self._new_shape(shape.klass, shape, key)
            shape.transitions[key] = child
        return child

    def set(self, o: Obj, key: str, value: object) -> None:
        if o.dictionary is not None:
            o.dictionary[key] = value
            return
        assert o.shape is not None
        i = o.shape.offsets.get(key)
        if i is not None:
            o.slots[i] = value
        else:
            o.shape = self.transition(o.shape, key)
            o.slots.append(value)

    def delete(self, o: Obj, key: str) -> None:
        """Remove an own property. The object leaves the shape tree for dictionary mode."""
        if o.dictionary is None:
            assert o.shape is not None
            if key not in o.shape.offsets:
                return
            o.dictionary = {k: o.slots[i] for k, i in o.shape.offsets.items()}
            o.shape = None
            o.slots = []
        o.dictionary.pop(key, None)

    def own(self, o: Obj) -> dict[str, object]:
        if o.dictionary is not None:
            return dict(o.dictionary)
        assert o.shape is not None
        return {k: o.slots[i] for k, i in o.shape.offsets.items()}

    def lookup_method(self, k: Klass, name: str) -> Method | tuple[str]:
        for d in k.chain():
            m = d.methods.get(name)
            if m is not None:
                return m
        return MISSING

    def get(self, o: Obj, key: str) -> object:
        """The full lookup: an own property first, then a method of the class chain."""
        if o.dictionary is not None:
            if key in o.dictionary:
                return o.dictionary[key]
        else:
            assert o.shape is not None
            i = o.shape.offsets.get(key)
            if i is not None:
                return o.slots[i]
        return self.lookup_method(o.klass, key)

    def site(self, key: str, bound: int = 4) -> LoadIC:
        s = LoadIC(self, key, bound)
        self.sites.append(s)
        return s


class LoadIC:
    """A polymorphic inline cache for the read o.key, keyed by shape.

    An entry (shape, "field", offset) says that objects of this shape hold key
    at that offset. An entry (shape, "class", answer) says that they have no
    own key and that the class chain gives answer. Shapes never change, so
    only "class" entries need invalidation, when a class in the chain changes.
    Objects in dictionary mode are not cached.
    """

    def __init__(self, rt: Runtime, key: str, bound: int = 4) -> None:
        if bound < 1:
            raise ValueError("bound must be at least 1")
        self.rt = rt
        self.key = key
        self.bound = bound
        self.entries: list[tuple[Shape, str, object]] = []
        self.megamorphic = False
        self.hits = 0
        self.misses = 0
        self.history: list[str] = [UNINITIALIZED]

    @property
    def state(self) -> str:
        if self.megamorphic:
            return MEGAMORPHIC
        if not self.entries:
            return UNINITIALIZED
        return MONOMORPHIC if len(self.entries) == 1 else POLYMORPHIC

    def _record(self) -> None:
        if self.history[-1] != self.state:
            self.history.append(self.state)

    def load(self, o: Obj) -> object:
        if self.megamorphic or o.shape is None:
            self.misses += 1
            return self.rt.get(o, self.key)
        for s, kind, data in self.entries:
            if s is o.shape:
                self.hits += 1
                if kind == "field":
                    assert isinstance(data, int)
                    return o.slots[data]
                return data
        self.misses += 1
        i = o.shape.offsets.get(self.key)
        if i is not None:
            entry: tuple[Shape, str, object] = (o.shape, "field", i)
            result = o.slots[i]
        else:
            result = self.rt.lookup_method(o.klass, self.key)
            entry = (o.shape, "class", result)
        if len(self.entries) < self.bound:
            self.entries.append(entry)
        else:
            self.entries = []
            self.megamorphic = True
        self._record()
        return result

    def invalidate(self, d: Klass) -> None:
        kept = [e for e in self.entries if e[1] == "field" or d not in e[0].klass.chain()]
        if len(kept) != len(self.entries):
            self.entries = kept
            self._record()


def example() -> dict[str, object]:
    """The worked example of the page."""
    rt = Runtime()
    rt.define_class("Object")
    rt.define_class("Point", "Object")
    norm = rt.set_method("Point", "norm")
    p, q, r = rt.new("Point"), rt.new("Point"), rt.new("Point")
    rt.set(p, "x", 3)
    rt.set(p, "y", 4)
    rt.set(q, "y", 5)
    rt.set(q, "x", 6)
    rt.set(r, "x", 7)
    rt.set(r, "y", 8)
    site = rt.site("x", bound=2)
    reads = [site.load(o) for o in (p, q, r, p)]
    nsite = rt.site("norm", bound=2)
    nreads = [nsite.load(o) for o in (p, q)]
    return {
        "shapes": rt.shape_count,
        "p_is_r": p.shape is r.shape,
        "p_is_q": p.shape is q.shape,
        "p_offsets": dict(p.shape.offsets) if p.shape else None,
        "q_offsets": dict(q.shape.offsets) if q.shape else None,
        "reads": reads,
        "hits": site.hits,
        "misses": site.misses,
        "state": site.state,
        "norm": all(m == norm for m in nreads),
    }


if __name__ == "__main__":
    for k, v in example().items():
        print(k, v)
