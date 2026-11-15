# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hidden-classes/. The authors are listed in prov/S7XDVF.jsonl.

import random

import pytest

from hidden_classes import (
    MEGAMORPHIC,
    MISSING,
    MONOMORPHIC,
    POLYMORPHIC,
    UNINITIALIZED,
    Runtime,
    example,
)


def test_example():
    assert example() == {
        "shapes": 6,
        "p_is_r": True,
        "p_is_q": False,
        "p_offsets": {"x": 0, "y": 1},
        "q_offsets": {"y": 0, "x": 1},
        "reads": [3, 6, 7, 3],
        "hits": 2,
        "misses": 2,
        "state": POLYMORPHIC,
        "norm": True,
    }


def ref_lookup(parent, methods, cls, key):
    while cls is not None:
        if key in methods[cls]:
            return methods[cls][key]
        cls = parent[cls]
    return MISSING


def random_run(seed):
    rng = random.Random(seed)
    rt = Runtime()
    parent = {}
    methods = {}
    cnames = ["C%d" % i for i in range(rng.randint(1, 4))]
    for i, c in enumerate(cnames):
        p = rng.choice(cnames[:i]) if i > 0 and rng.random() < 0.7 else None
        rt.define_class(c, p)
        parent[c] = p
        methods[c] = {}
    keys = ["a", "b", "c", "d", "e"]
    for _ in range(rng.randint(0, 4)):
        c, k = rng.choice(cnames), rng.choice(keys)
        methods[c][k] = rt.set_method(c, k)
    objs = []
    ref = []
    order = []
    deleted = []
    prefixes = set()
    for _ in range(rng.randint(4, 12)):
        c = rng.choice(cnames)
        objs.append(rt.new(c))
        ref.append({})
        order.append([])
        deleted.append(False)
    sites = [rt.site(rng.choice(keys), rng.randint(1, 4)) for _ in range(4)]
    reads = 0
    for _ in range(250):
        r = rng.random()
        i = rng.randrange(len(objs))
        o = objs[i]
        if r < 0.35:
            k = rng.choice(keys[: rng.randint(1, len(keys))])
            v = rng.randrange(1000)
            rt.set(o, k, v)
            if k not in ref[i]:
                order[i].append(k)
            ref[i][k] = v
        elif r < 0.38:
            k = rng.choice(keys)
            rt.delete(o, k)
            if k in ref[i]:
                deleted[i] = True
                del ref[i][k]
                order[i].remove(k)
        elif r < 0.42:
            c, k = rng.choice(cnames), rng.choice(keys)
            if rng.random() < 0.7:
                methods[c][k] = rt.set_method(c, k)
            else:
                rt.remove_method(c, k)
                methods[c].pop(k, None)
        else:
            site = rng.choice(sites)
            before = (site.megamorphic, len(site.entries))
            hits = site.hits
            got = site.load(o)
            want = ref[i][site.key] if site.key in ref[i] else ref_lookup(parent, methods, o.klass.name, site.key)
            assert got == want
            assert rt.get(o, site.key) == want
            reads += 1
            if before[0]:
                assert site.megamorphic
            elif site.hits > hits or o.shape is None:
                assert (site.megamorphic, len(site.entries)) == before
            elif before[1] < site.bound:
                assert len(site.entries) == before[1] + 1
            else:
                assert site.megamorphic and not site.entries
        for j, oj in enumerate(objs):
            assert rt.own(oj) == ref[j]
            for k in keys:
                want = ref[j][k] if k in ref[j] else ref_lookup(parent, methods, oj.klass.name, k)
                assert rt.get(oj, k) == want
            if deleted[j]:
                assert oj.shape is None
                continue
            s = oj.shape
            assert s is not None and s.klass is oj.klass
            assert s.names() == order[j]
            assert len(oj.slots) == len(s.offsets)
            for k, off in s.offsets.items():
                assert oj.slots[off] == ref[j][k]
            for n in range(len(order[j]) + 1):
                prefixes.add((oj.klass.name, tuple(order[j][:n])))
        for site in sites:
            shapes = [e[0] for e in site.entries]
            assert len(shapes) == len({id(s) for s in shapes}) <= site.bound
            for s, kind, data in site.entries:
                if kind == "field":
                    assert s.offsets[site.key] == data
                else:
                    assert site.key not in s.offsets
                    assert data == ref_lookup(parent, methods, s.klass.name, site.key)
    live = [j for j in range(len(objs)) if not deleted[j]]
    for a in live:
        for b in live:
            same = (objs[a].klass is objs[b].klass) and order[a] == order[b]
            assert (objs[a].shape is objs[b].shape) == same
    assert rt.shape_count == len(prefixes | {(c, ()) for c in cnames})
    return reads


def test_random_programs():
    total = 0
    for seed in range(120):
        total += random_run(seed)
    assert total > 15000


def test_same_order_shares_shape_different_order_does_not():
    rng = random.Random(7)
    rt = Runtime()
    rt.define_class("A")
    names = ["p%d" % i for i in range(6)]
    by_order = {}
    for _ in range(300):
        seq = rng.sample(names, rng.randint(0, 6))
        o = rt.new("A")
        for k in seq:
            rt.set(o, k, k.upper())
        by_order.setdefault(tuple(seq), set()).add(id(o.shape))
        assert {k: o.slots[i] for k, i in o.shape.offsets.items()} == {k: k.upper() for k in seq}
    assert all(len(v) == 1 for v in by_order.values())
    all_shapes = [next(iter(v)) for v in by_order.values()]
    assert len(set(all_shapes)) == len(all_shapes)


@pytest.mark.parametrize("bound", [1, 2, 4])
def test_load_ic_state_machine(bound):
    rt = Runtime()
    rt.define_class("A")
    objs = []
    for j in range(bound + 2):
        o = rt.new("A")
        for i in range(j):
            rt.set(o, "pad%d" % i, i)
        rt.set(o, "x", j)
        objs.append(o)
    for j in range(1, bound + 3):
        site = rt.site("x", bound)
        for o in objs[:j] * 2:
            assert site.load(o) == objs.index(o)
        if j <= bound:
            assert len(site.entries) == j and site.hits == j
            assert site.state == (MONOMORPHIC if j == 1 else POLYMORPHIC)
        else:
            assert site.state == MEGAMORPHIC
        full = [UNINITIALIZED, MONOMORPHIC, POLYMORPHIC, MEGAMORPHIC]
        if bound == 1:
            full = [UNINITIALIZED, MONOMORPHIC, MEGAMORPHIC]
        assert site.history == full[: len(site.history)]


def test_class_entries_invalidated_field_entries_kept():
    rt = Runtime()
    rt.define_class("Base")
    rt.define_class("A", "Base")
    m1 = rt.set_method("Base", "f")
    a1 = rt.new("A")
    a2 = rt.new("A")
    rt.set(a2, "f", 99)
    site = rt.site("f", bound=4)
    assert site.load(a1) == m1
    assert site.load(a2) == 99
    assert [e[1] for e in site.entries] == ["class", "field"]
    m2 = rt.set_method("A", "f")
    assert [e[1] for e in site.entries] == ["field"]
    assert site.load(a1) == m2
    assert site.load(a2) == 99


def test_dictionary_mode_is_not_cached():
    rt = Runtime()
    rt.define_class("A")
    o = rt.new("A")
    rt.set(o, "x", 1)
    rt.set(o, "y", 2)
    rt.delete(o, "x")
    assert o.shape is None and rt.own(o) == {"y": 2}
    site = rt.site("y")
    assert site.load(o) == 2 and site.load(o) == 2
    assert site.state == UNINITIALIZED and site.misses == 2
    assert site.load(o) == 2
    rt.set(o, "x", 5)
    assert rt.get(o, "x") == 5
