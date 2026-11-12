# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generational-garbage-collection/. The authors are listed in prov/JNBZA2.jsonl.

import random
from typing import Optional

from generational_garbage_collection import GenHeap


class Oracle:
    """The same object graph by oid, with no collector at all."""

    def __init__(self) -> None:
        self.fields: dict[int, list[Optional[int]]] = {}
        self.roots: list[Optional[int]] = []

    def reachable(self) -> set[int]:
        seen: set[int] = set()
        stack = [r for r in self.roots if r is not None]
        while stack:
            o = stack.pop()
            if o in seen:
                continue
            seen.add(o)
            stack.extend(t for t in self.fields[o] if t is not None)
        return seen


def oid_of(h: GenHeap, a: Optional[int]) -> Optional[int]:
    return None if a is None else h.obj(a).oid


def check(h: GenHeap, m: Oracle) -> None:
    objs = h.all_objects()
    for o in objs.values():
        for t in o.fields:
            assert t is None or t in objs, "dangling pointer"
    assert h.old_to_young_slots() <= h.remset
    assert [oid_of(h, r) for r in h.roots] == m.roots
    by_oid = {o.oid: o for o in objs.values()}
    for oid in m.reachable():
        assert oid in by_oid, "a reachable object was freed"
        assert [oid_of(h, t) for t in by_oid[oid].fields] == m.fields[oid]


def run_trace(seed: int, steps: int, nursery: int, old: int, tenure: int) -> GenHeap:
    rng = random.Random(seed)
    h, m = GenHeap(nursery, old, tenure), Oracle()
    for _ in range(steps):
        live = [k for k, r in enumerate(m.roots) if r is not None]
        op = rng.random()
        if op < 0.35 or not live:
            nf = rng.randint(0, 3)
            k = h.alloc(nf)
            oid = h.obj(h.roots[k]).oid
            m.fields[oid] = [None] * nf
            m.roots.append(oid)
        elif op < 0.75:
            s = rng.choice(live)
            nf = len(m.fields[m.roots[s]])
            if nf:
                i = rng.randrange(nf)
                r = rng.choice(live + [None])
                h.write(s, i, r)
                m.fields[m.roots[s]][i] = None if r is None else m.roots[r]
        elif op < 0.9:
            s = rng.choice(live)
            nf = len(m.fields[m.roots[s]])
            if nf:
                i = rng.randrange(nf)
                d = rng.randrange(len(m.roots))
                h.load(s, i, d)
                m.roots[d] = m.fields[m.roots[s]][i]
        else:
            d = rng.choice(live)
            h.drop(d)
            m.roots[d] = None
        check(h, m)
    h.minor_collect()
    check(h, m)
    h.major_collect()
    check(h, m)
    assert {o.oid for o in h.all_objects().values()} == m.reachable()
    return h


def test_random_traces() -> None:
    total_minor = 0
    for seed in range(60):
        rng = random.Random(1000 + seed)
        h = run_trace(seed, 300, rng.randint(2, 8), rng.randint(4, 30), rng.randint(1, 3))
        total_minor += h.minor_count
    assert total_minor > 500


def test_old_to_young_pointer_keeps_child() -> None:
    h = GenHeap(nursery_size=2, old_size=100, tenure_age=1)
    p = h.alloc(1)
    h.minor_collect()  # p is promoted
    assert h.roots[p] in h.old
    c = h.alloc(0)
    h.write(p, 0, c)
    assert (h.roots[p], 0) in h.remset
    h.drop(c)  # c is now reachable only through the old object
    h.minor_collect()
    child = h.old[h.roots[p]].fields[0]
    assert child is not None and child in h.old
    assert h.remset == set()


class NoBarrier(GenHeap):
    """The pitfall: a store with no write barrier."""

    def write(self, src_root: int, i: int, ref_root: Optional[int]) -> None:
        src = self.roots[src_root]
        assert src is not None
        self.obj(src).fields[i] = None if ref_root is None else self.roots[ref_root]


def test_missing_barrier_frees_a_live_object() -> None:
    h = NoBarrier(nursery_size=2, old_size=100, tenure_age=1)
    p = h.alloc(1)
    h.minor_collect()
    c = h.alloc(0)
    h.write(p, 0, c)
    h.drop(c)
    h.minor_collect()
    child = h.old[h.roots[p]].fields[0]
    assert child is not None and child not in h.all_objects()  # dangling


def test_page_example() -> None:
    h = GenHeap(nursery_size=4, old_size=100, tenure_age=2)
    a = h.alloc(1)
    b = h.alloc(0)
    c = h.alloc(0)
    h.write(a, 0, b)
    h.drop(b)
    h.drop(c)
    d = h.alloc(0)
    h.alloc(0)  # the nursery is full: the first minor collection runs here
    assert h.minor_count == 1
    assert {o.oid for o in h.young.values()} == {0, 1, 3, 4}
    assert h.old == {}
    h.drop(d)
    h.alloc(0)  # second minor: a and b reach age 2 and are promoted
    assert h.minor_count == 2
    assert sorted(o.oid for o in h.old.values()) == [0, 1]
    assert sorted(o.oid for o in h.young.values()) == [4, 5]
    assert h.promoted == 2 and h.copied == 6


def test_no_collection_without_allocation() -> None:
    h = GenHeap(3, 10)
    k = h.alloc(2)
    h.write(k, 0, k)
    h.write(k, 1, None)
    assert h.minor_count == 0 and h.major_count == 0
