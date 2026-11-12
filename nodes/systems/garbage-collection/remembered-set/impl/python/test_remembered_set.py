# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/remembered-set/. The authors are listed in prov/ASEXAM.jsonl.

import random
from typing import Optional

from remembered_set import RememberedSet


class TwoGen:
    """A heap of objects with pointer fields, each object old or young."""

    def __init__(self, rs: RememberedSet) -> None:
        self.fields: dict[int, list[Optional[int]]] = {}
        self.old: set[int] = set()
        self.rs = rs
        self.n = 0

    def new(self, k: int, old: bool = False) -> int:
        self.n += 1
        self.fields[self.n] = [None] * k
        if old:
            self.old.add(self.n)
        return self.n

    def young(self, x: object) -> bool:
        return x is not None and x in self.fields and x not in self.old

    def write(self, src: int, i: int, ref: Optional[int]) -> None:
        self.fields[src][i] = ref
        if src in self.old and self.young(ref):  # the write barrier
            self.rs.record(src, i)

    def old_to_young(self) -> set[tuple[int, int]]:
        return {(o, i) for o in self.old for i, t in enumerate(self.fields[o]) if self.young(t)}

    def minor(self, promote: set[int]) -> list[tuple[int, int]]:
        seen = list(self.rs.roots(lambda o: self.fields[o], self.young))
        self.old |= promote
        for p in promote:
            for i, t in enumerate(self.fields[p]):
                if self.young(t):
                    self.rs.record(p, i)
        if self.rs.precision == "slot":
            self.rs.retain(lambda e: self.young(self.fields[e[0]][e[1]]))
        else:
            self.rs.retain(lambda o: any(self.young(t) for t in self.fields[o]))
        return seen

    def free_unreferenced_old(self, rng: random.Random) -> None:
        pointed = {t for f in self.fields.values() for t in f if t is not None}
        dead = {o for o in self.old if o not in pointed and rng.random() < 0.5}
        for o in dead:
            del self.fields[o]
        self.old -= dead
        self.rs.forget_objects(dead)


def check(h: TwoGen) -> None:
    for (o, i) in h.old_to_young():
        assert h.rs.covers(o, i)


def run(seed: int, precision: str) -> None:
    rng = random.Random(seed)
    h = TwoGen(RememberedSet(rng.randint(1, 6), precision))
    for _ in range(4):
        h.new(rng.randint(1, 3), old=True)
    for _ in range(250):
        ids = list(h.fields)
        op = rng.random()
        if op < 0.25 or not ids:
            h.new(rng.randint(0, 3), old=rng.random() < 0.2)
        elif op < 0.8:
            src = rng.choice(ids)
            if h.fields[src]:
                h.write(src, rng.randrange(len(h.fields[src])), rng.choice(ids + [None]))
        elif op < 0.93:
            want = h.old_to_young()
            seen = h.minor({y for y in h.fields if y not in h.old and rng.random() < 0.6})
            assert len(seen) == len(set(seen))
            assert set(seen) == want
        else:
            h.free_unreferenced_old(rng)
        check(h)


def test_random_slot_precision() -> None:
    for seed in range(150):
        run(seed, "slot")


def test_random_object_precision() -> None:
    for seed in range(150):
        run(500 + seed, "object")


def test_page_example() -> None:
    rs = RememberedSet(3)
    h = TwoGen(rs)
    a, b = h.new(2, old=True), h.new(2, old=True)
    x, y = h.new(0), h.new(0)
    h.write(a, 0, x)
    h.write(b, 1, y)
    assert rs.buffer == [(a, 0), (b, 1)] and rs.table == set()
    h.write(a, 0, y)
    assert rs.buffer == [] and rs.table == {(a, 0), (b, 1)}
    h.write(b, 1, None)
    h.write(a, 1, x)
    assert rs.buffer == [(a, 1)]
    seen = h.minor({x, y})
    assert sorted(seen) == [(a, 0), (a, 1)]
    assert len(rs) == 0


def test_object_precision_deduplicates() -> None:
    rs = RememberedSet(10, "object")
    h = TwoGen(rs)
    a = h.new(3, old=True)
    y = h.new(0)
    for i in range(3):
        h.write(a, i, y)
    assert rs.buffer == [a] and rs.appends == 1


def test_capacity_one_drains_each_time() -> None:
    rs = RememberedSet(1)
    rs.record("o", 0)
    rs.record("o", 0)
    assert rs.drains == 2 and rs.table == {("o", 0)} and rs.buffer == []
