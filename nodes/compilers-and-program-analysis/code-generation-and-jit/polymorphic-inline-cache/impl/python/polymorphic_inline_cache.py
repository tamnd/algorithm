# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polymorphic-inline-cache/. The authors are listed in prov/WAS1H3.jsonl.

"""A small class-based object model with polymorphic inline caches.

Classes have a method table and an optional parent. A full lookup walks the
chain of parents. Each send site has a polymorphic inline cache (PIC) with the
states uninitialized, monomorphic, polymorphic and megamorphic. The runtime
keeps a list of all sites and empties the stale entries when a method table or
a parent link changes.
"""

from __future__ import annotations

from dataclasses import dataclass, field

UNINITIALIZED = "uninitialized"
MONOMORPHIC = "monomorphic"
POLYMORPHIC = "polymorphic"
MEGAMORPHIC = "megamorphic"

NOT_UNDERSTOOD = ("not understood",)


@dataclass(frozen=True)
class Method:
    """A method body. The id makes two definitions with the same name differ."""

    owner: str
    selector: str
    ident: int


@dataclass(eq=False)
class Klass:
    name: str
    parent: Klass | None = None
    methods: dict[str, Method] = field(default_factory=dict)

    def chain(self) -> list[Klass]:
        out: list[Klass] = []
        k: Klass | None = self
        while k is not None:
            out.append(k)
            k = k.parent
        return out


class Runtime:
    """Classes, the send sites, and the global lookup cache used by megamorphic sites."""

    def __init__(self) -> None:
        self.classes: dict[str, Klass] = {}
        self.sites: list[PIC] = []
        self.global_cache: dict[tuple[int, str], Method | tuple[str]] = {}
        self.full_lookups = 0
        self._next_ident = 0

    def define_class(self, name: str, parent: str | None = None) -> Klass:
        if name in self.classes:
            raise ValueError("class already defined: " + name)
        k = Klass(name, self.classes[parent] if parent is not None else None)
        self.classes[name] = k
        return k

    def lookup(self, k: Klass, selector: str) -> Method | tuple[str]:
        """The full lookup: the first class in the chain of k that defines selector."""
        self.full_lookups += 1
        for d in k.chain():
            m = d.methods.get(selector)
            if m is not None:
                return m
        return NOT_UNDERSTOOD

    def global_lookup(self, k: Klass, selector: str) -> Method | tuple[str]:
        key = (id(k), selector)
        m = self.global_cache.get(key)
        if m is None:
            m = self.lookup(k, selector)
            self.global_cache[key] = m
        return m

    def _changed(self, d: Klass) -> None:
        """Called before a change of d. Empties every entry whose class has d in its chain."""
        self.global_cache.clear()
        for site in self.sites:
            site.invalidate(d)

    def set_method(self, cls: str, selector: str) -> Method:
        d = self.classes[cls]
        self._changed(d)
        self._next_ident += 1
        m = Method(cls, selector, self._next_ident)
        d.methods[selector] = m
        return m

    def remove_method(self, cls: str, selector: str) -> None:
        d = self.classes[cls]
        if selector in d.methods:
            self._changed(d)
            del d.methods[selector]

    def set_parent(self, cls: str, parent: str | None) -> None:
        d = self.classes[cls]
        p = self.classes[parent] if parent is not None else None
        if p is not None and d in p.chain():
            raise ValueError("the new parent link would make a cycle")
        self._changed(d)
        d.parent = p

    def site(self, selector: str, bound: int = 4) -> PIC:
        s = PIC(self, selector, bound)
        self.sites.append(s)
        return s


class PIC:
    """A polymorphic inline cache for one send site.

    entries is a list of (class, method) pairs with distinct classes, in the
    order in which they were added, of length at most bound. A megamorphic
    site has no entries and uses the global lookup cache.
    """

    def __init__(self, rt: Runtime, selector: str, bound: int = 4) -> None:
        if bound < 1:
            raise ValueError("bound must be at least 1")
        self.rt = rt
        self.selector = selector
        self.bound = bound
        self.entries: list[tuple[Klass, Method | tuple[str]]] = []
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
        if len(self.entries) == 1:
            return MONOMORPHIC
        return POLYMORPHIC

    def _record(self) -> None:
        if self.history[-1] != self.state:
            self.history.append(self.state)

    def send(self, k: Klass) -> Method | tuple[str]:
        """The method that a send of the selector to a receiver of class k runs."""
        if self.megamorphic:
            self.misses += 1
            return self.rt.global_lookup(k, self.selector)
        for ck, m in self.entries:
            if ck is k:
                self.hits += 1
                return m
        self.misses += 1
        m = self.rt.lookup(k, self.selector)
        if len(self.entries) < self.bound:
            self.entries.append((k, m))
        else:
            self.entries = []
            self.megamorphic = True
        self._record()
        return m

    def invalidate(self, d: Klass) -> None:
        kept = [(k, m) for k, m in self.entries if d not in k.chain()]
        if len(kept) != len(self.entries):
            self.entries = kept
            self._record()

    def types_seen(self) -> list[str]:
        """The receiver classes in the cache, the data that type feedback reads."""
        return [k.name for k, _ in self.entries]


def example() -> list[tuple[str, str, str, str]]:
    """The worked example of the page: one print site with bound 3."""
    rt = Runtime()
    for name, parent in [("Object", None), ("Point", "Object"), ("ColorPoint", "Point"), ("Circle", "Object"), ("Square", "Object")]:
        rt.define_class(name, parent)
    rt.set_method("Object", "print")
    rt.set_method("Object", "hash")
    rt.set_method("Point", "x")
    rt.set_method("Point", "print")
    rt.set_method("ColorPoint", "color")
    rt.set_method("Circle", "print")
    rt.set_method("Circle", "area")
    rt.set_method("Square", "area")
    site = rt.site("print", bound=3)
    rows = []
    for name in ["Point", "Circle", "Point", "ColorPoint", "Circle", "Square", "Point"]:
        hits = site.hits
        m = site.send(rt.classes[name])
        assert isinstance(m, Method)
        rows.append((name, "hit" if site.hits > hits else "miss", m.owner + "." + m.selector, site.state))
    return rows


if __name__ == "__main__":
    for row in example():
        print(*row)
