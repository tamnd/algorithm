# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/polymorphic-inline-cache/. The authors are listed in prov/WAS1H3.jsonl.

import random

import pytest

from polymorphic_inline_cache import (
    MEGAMORPHIC,
    MONOMORPHIC,
    NOT_UNDERSTOOD,
    POLYMORPHIC,
    UNINITIALIZED,
    Runtime,
    example,
)


class Shadow:
    """An independent copy of the class table, used as the reference lookup."""

    def __init__(self) -> None:
        self.parent: dict[str, str | None] = {}
        self.methods: dict[str, dict[str, object]] = {}

    def lookup(self, name: str | None, selector: str) -> object:
        while name is not None:
            if selector in self.methods[name]:
                return self.methods[name][selector]
            name = self.parent[name]
        return NOT_UNDERSTOOD

    def ancestors(self, name: str | None) -> set[str]:
        out = set()
        while name is not None:
            out.add(name)
            name = self.parent[name]
        return out


def test_example_table():
    assert example() == [
        ("Point", "miss", "Point.print", MONOMORPHIC),
        ("Circle", "miss", "Circle.print", POLYMORPHIC),
        ("Point", "hit", "Point.print", POLYMORPHIC),
        ("ColorPoint", "miss", "Point.print", POLYMORPHIC),
        ("Circle", "hit", "Circle.print", POLYMORPHIC),
        ("Square", "miss", "Object.print", MEGAMORPHIC),
        ("Point", "miss", "Point.print", MEGAMORPHIC),
    ]


def test_example_invalidation():
    rt = Runtime()
    for name, parent in [("Object", None), ("Point", "Object"), ("ColorPoint", "Point"), ("Circle", "Object")]:
        rt.define_class(name, parent)
    rt.set_method("Object", "print")
    rt.set_method("Point", "print")
    circle_print = rt.set_method("Circle", "print")
    site = rt.site("print", bound=3)
    for name in ["Point", "Circle", "ColorPoint"]:
        site.send(rt.classes[name])
    assert site.types_seen() == ["Point", "Circle", "ColorPoint"]
    new = rt.set_method("ColorPoint", "print")
    assert site.types_seen() == ["Point", "Circle"]
    assert site.send(rt.classes["ColorPoint"]) == new
    assert site.state == POLYMORPHIC and len(site.entries) == 3
    rt.set_method("Point", "print")
    assert site.types_seen() == ["Circle"] and site.state == MONOMORPHIC
    assert site.send(rt.classes["Circle"]) == circle_print


@pytest.mark.parametrize("bound", [1, 2, 3, 4, 10])
def test_state_machine_without_changes(bound):
    rt = Runtime()
    rt.define_class("Object")
    rt.set_method("Object", "m")
    names = ["C%d" % i for i in range(bound + 3)]
    for n in names:
        rt.define_class(n, "Object")
    for j in range(1, bound + 3):
        site = rt.site("m", bound)
        for n in names[:j] * 3:
            site.send(rt.classes[n])
        if j <= bound:
            assert len(site.entries) == j
            assert site.state == (MONOMORPHIC if j == 1 else POLYMORPHIC)
            assert site.misses == j and site.hits == 2 * j
        else:
            assert site.state == MEGAMORPHIC and site.entries == []
        expected = [UNINITIALIZED, MONOMORPHIC, POLYMORPHIC, MEGAMORPHIC]
        if bound == 1:
            expected = [UNINITIALIZED, MONOMORPHIC, MEGAMORPHIC]
        assert site.history == expected[: len(site.history)]


def check_site(site, shadow):
    classes = [k.name for k, _ in site.entries]
    assert len(classes) == len(set(classes))
    assert len(classes) <= site.bound
    for k, m in site.entries:
        assert m == shadow.lookup(k.name, site.selector)
    if site.megamorphic:
        assert site.state == MEGAMORPHIC and not site.entries
    elif not classes:
        assert site.state == UNINITIALIZED
    elif len(classes) == 1:
        assert site.state == MONOMORPHIC
    else:
        assert site.state == POLYMORPHIC


def random_run(seed):
    rng = random.Random(seed)
    rt = Runtime()
    shadow = Shadow()
    nclasses = rng.randint(3, 9)
    names = ["K%d" % i for i in range(nclasses)]
    for i, n in enumerate(names):
        p = rng.choice(names[:i]) if i > 0 and rng.random() < 0.85 else None
        rt.define_class(n, p)
        shadow.parent[n] = p
        shadow.methods[n] = {}
    selectors = ["a", "b", "c", "d"]
    for _ in range(rng.randint(2, 12)):
        n, s = rng.choice(names), rng.choice(selectors)
        shadow.methods[n][s] = rt.set_method(n, s)
    sites = [rt.site(rng.choice(selectors), rng.randint(1, 5)) for _ in range(6)]
    weights = {id(s): [rng.random() ** 3 for _ in names] for s in sites}
    sends = 0
    for _ in range(300):
        before = [(s.megamorphic, len(s.entries)) for s in sites]
        r = rng.random()
        if r < 0.88:
            i = rng.randrange(len(sites))
            site = sites[i]
            name = rng.choices(names, weights[id(site)])[0]
            hits = site.hits
            got = site.send(rt.classes[name])
            sends += 1
            assert got == shadow.lookup(name, site.selector)
            mega, n = before[i]
            if mega:
                assert site.megamorphic
            elif site.hits > hits:
                assert (site.megamorphic, len(site.entries)) == (mega, n)
            elif n < site.bound:
                assert not site.megamorphic and len(site.entries) == n + 1
            else:
                assert site.megamorphic and not site.entries
        else:
            n = rng.choice(names)
            kind = rng.randrange(3)
            if kind == 0:
                s = rng.choice(selectors)
                shadow.methods[n][s] = rt.set_method(n, s)
            elif kind == 1:
                s = rng.choice(selectors)
                rt.remove_method(n, s)
                shadow.methods[n].pop(s, None)
            else:
                p = rng.choice(names + [None])
                if p is not None and n in shadow.ancestors(p):
                    with pytest.raises(ValueError):
                        rt.set_parent(n, p)
                else:
                    rt.set_parent(n, p)
                    shadow.parent[n] = p
            for site, (mega, cnt) in zip(sites, before):
                assert site.megamorphic == mega
                assert len(site.entries) <= cnt
        for site in sites:
            check_site(site, shadow)
    return sends


def test_random_programs_match_full_lookup():
    total = 0
    for seed in range(150):
        total += random_run(seed)
    assert total > 30000


def test_invalidation_keeps_unrelated_entries():
    rt = Runtime()
    rt.define_class("A")
    rt.define_class("B", "A")
    rt.define_class("C", "A")
    rt.set_method("A", "f")
    site = rt.site("f", bound=4)
    for n in "ABC":
        site.send(rt.classes[n])
    rt.set_method("B", "g")
    assert site.types_seen() == ["A", "C"]
    rt.set_method("A", "g")
    assert site.types_seen() == []
    assert site.state == UNINITIALIZED


def test_parent_cycle_rejected():
    rt = Runtime()
    rt.define_class("A")
    rt.define_class("B", "A")
    with pytest.raises(ValueError):
        rt.set_parent("A", "B")
    with pytest.raises(ValueError):
        rt.set_parent("A", "A")


def test_not_understood_is_cached_and_invalidated():
    rt = Runtime()
    rt.define_class("A")
    site = rt.site("f", bound=2)
    assert site.send(rt.classes["A"]) == NOT_UNDERSTOOD
    assert site.send(rt.classes["A"]) == NOT_UNDERSTOOD and site.hits == 1
    m = rt.set_method("A", "f")
    assert site.send(rt.classes["A"]) == m
