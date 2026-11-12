# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/read-barrier/. The authors are listed in prov/CVZ3Q6.jsonl.

import random
from typing import Optional, Union

from read_barrier import BakerHeap, BrooksHeap, Obj

Heap = Union[BakerHeap, BrooksHeap]


class Oracle:
    def __init__(self) -> None:
        self.fields: dict[int, list[Optional[int]]] = {}
        self.roots: list[Optional[int]] = []

    def reachable(self) -> set[int]:
        seen: set[int] = set()
        stack = [r for r in self.roots if r is not None]
        while stack:
            o = stack.pop()
            if o not in seen:
                seen.add(o)
                stack.extend(t for t in self.fields[o] if t is not None)
        return seen


def oid(o: Optional[Obj]) -> Optional[int]:
    return None if o is None else o.fwd.oid


def check(h: Heap, m: Oracle) -> None:
    """The heap seen through the forwarding words equals the oracle."""
    assert [oid(r) for r in h.roots] == m.roots
    seen: set[int] = set()
    stack = [r.fwd for r in h.roots if r is not None]
    while stack:
        o = stack.pop()
        assert o.space != "freed", "a reachable object was freed"
        if o.oid in seen:
            continue
        seen.add(o.oid)
        assert [oid(t) for t in o.fields] == m.fields[o.oid]
        stack.extend(t.fwd for t in o.fields if t is not None)
    assert seen == m.reachable()


def mutate(h: Heap, m: Oracle, rng: random.Random) -> None:
    live = [k for k, r in enumerate(m.roots) if r is not None]
    op = rng.random()
    if op < 0.25 or not live:
        nf = rng.randint(0, 3)
        k = h.alloc(nf)
        r = h.roots[k]
        assert r is not None
        m.fields[r.oid] = [None] * nf
        m.roots.append(r.oid)
    elif op < 0.6:
        s = rng.choice(live)
        nf = len(m.fields[m.roots[s]])
        if nf:
            i, r = rng.randrange(nf), rng.choice(live + [None])
            h.write(s, i, r)
            m.fields[m.roots[s]][i] = None if r is None else m.roots[r]
    elif op < 0.9:
        s = rng.choice(live)
        nf = len(m.fields[m.roots[s]])
        if nf:
            i, d = rng.randrange(nf), rng.randrange(len(m.roots))
            h.load(s, i, d)
            m.roots[d] = m.fields[m.roots[s]][i]
    else:
        d = rng.choice(live)
        h.roots[d] = None
        m.roots[d] = None


def test_baker_to_space_invariant() -> None:
    moved = 0
    for seed in range(200):
        rng = random.Random(seed)
        h, m = BakerHeap(), Oracle()
        for _ in range(rng.randint(20, 60)):
            mutate(h, m, rng)
        for _ in range(3):
            h.flip()
            while h.collecting:
                if rng.random() < 0.5:
                    h.step()
                else:
                    mutate(h, m, rng)
                assert all(r is None or r.space == "to" for r in h.roots), "the mutator holds a from-space pointer"
                check(h, m)
            for o in h.objects:  # after the flip ends, nothing points into from-space
                assert all(t is None or t.space == "to" for t in o.fields)
            moved += len(h.objects)
    assert moved > 3000


def test_brooks_indirection() -> None:
    for seed in range(200):
        rng = random.Random(5000 + seed)
        h, m = BrooksHeap(), Oracle()
        for _ in range(rng.randint(20, 60)):
            mutate(h, m, rng)
        for _ in range(3):
            h.start(rng)
            while h.cset:
                if rng.random() < 0.5:
                    h.copy_step()
                else:
                    mutate(h, m, rng)
                check(h, m)
            h.update_refs()
            check(h, m)
            for o in h.objects:
                assert o.fwd is o and all(t is None or t.space != "freed" for t in o.fields)


class NoBrooks(BrooksHeap):
    """The pitfall: a store that skips the indirection."""

    @staticmethod
    def write_field(o: Obj, i: int, v: Optional[Obj]) -> None:
        o.fields[i] = v


def lost_write(cls: type) -> BrooksHeap:
    h = cls()
    a = h.alloc(1)
    b = h.alloc(0)
    h.start(random.Random(0), fraction=1.0)
    h.cset = [h.roots[a]]
    h.copy_step()  # a is copied; the mutator still holds the old pointer
    h.write(a, 0, b)
    h.update_refs()
    return h


def test_store_without_indirection_is_lost() -> None:
    h = lost_write(NoBrooks)
    assert h.roots[0].fields[0] is None  # the store went to the old copy
    h = lost_write(BrooksHeap)
    assert h.roots[0].fields[0] is h.roots[1]


def test_baker_heals_the_slot() -> None:
    h = BakerHeap()
    a = h.alloc(1)
    b = h.alloc(0)
    h.write(a, 0, b)
    h.roots[b] = None
    h.flip()
    pa = h.roots[a]
    assert pa.space == "to" and pa.fields[0].space == "from"
    h.load(a, 0, b)  # the barrier copies b and heals a.f[0]
    assert h.roots[b].space == "to" and pa.fields[0] is h.roots[b]
