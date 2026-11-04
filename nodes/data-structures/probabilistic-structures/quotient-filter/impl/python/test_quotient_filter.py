# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quotient-filter/. The authors are listed in prov/44MVA2.jsonl.

import random
from collections import Counter

import pytest

from quotient_filter import Key, QuotientFilter

FPS: dict[Key, tuple[int, int]] = {
    "a": (1, 5), "b": (1, 2), "c": (2, 7), "d": (4, 3), "e": (3, 1), "f": (7, 6), "g": (7, 4), "x": (2, 1),
}


class FixedQF(QuotientFilter):
    def _fp(self, key: Key) -> tuple[int, int]:
        return FPS[key]


def bits(f: QuotientFilter) -> list[str]:
    return [
        "".join("1" if v else "0" for v in (f.occupied[p], f.continuation[p], f.shifted[p])) for p in range(f.m)
    ]


def test_example() -> None:
    f = FixedQF(3, 3)
    for k in "abcde":
        assert f.insert(k)
    assert f.remainder[1:6] == [2, 5, 7, 1, 3]
    assert bits(f)[:6] == ["000", "100", "111", "101", "101", "001"]
    for k in "fg":
        f.insert(k)
    assert f.remainder[7] == 4 and f.remainder[0] == 6
    assert bits(f)[7] == "100" and bits(f)[0] == "011"
    assert all(f.query(k) for k in "abcdefg")
    assert not f.query("x")
    assert f.delete("b")
    assert f.remainder[1:5] == [5, 7, 1, 3] and bits(f)[:6] == ["011", "100", "100", "100", "100", "000"]
    assert all(f.query(k) for k in "acdefg") and not f.query("b")


def test_edges() -> None:
    with pytest.raises(ValueError):
        QuotientFilter(0, 4)
    f = QuotientFilter(1, 1)
    assert f.insert("a") and not f.insert("b")  # capacity 2^q - 1
    assert f.query("a") and f.delete("a") and not f.query("a")


def check_layout(f: QuotientFilter) -> Counter[tuple[int, int]]:
    """Check the invariant of the page directly, and return the stored multiset."""
    m = f.m
    e = next(p for p in range(m) if f._is_empty(p))
    order = [(e + t) % m for t in range(1, m)] + [e]  # no cluster crosses the empty slot e
    found: Counter[tuple[int, int]] = Counter()
    t = 0
    while t < m:
        p = order[t]
        if f._is_empty(p):
            assert f.remainder[p] == 0
            t += 1
            continue
        slots = []
        while not f._is_empty(order[t]):
            slots.append(order[t])
            t += 1
        c = slots[0]  # cluster start: the slot before it is empty
        qs = [j for j in slots if f.occupied[j]]
        k, prev = -1, -1
        for i, s in enumerate(slots):
            if not f.continuation[s]:
                k += 1
                if k == 0:
                    assert qs[0] == c
                else:
                    assert (qs[k] - c) % m <= i
                prev = -1
            Q = qs[k]
            assert f.shifted[s] == (s != Q)
            assert prev <= f.remainder[s]
            prev = f.remainder[s]
            found[(Q, f.remainder[s])] += 1
        assert k == len(qs) - 1
    return found


def test_random_against_multiset() -> None:
    rng = random.Random(2012)
    for _ in range(500):
        q, r = rng.randint(1, 4), rng.randint(1, 3)
        f = QuotientFilter(q, r, seed=rng.randrange(1000))
        live: Counter[int] = Counter()
        fps: Counter[tuple[int, int]] = Counter()
        for _ in range(rng.randint(0, 50)):
            x = rng.randrange(25)
            if rng.random() < 0.6:
                if f.insert(x):
                    live[x] += 1
                    fps[f._fp(x)] += 1
            elif live[x] > 0:
                assert f.delete(x)
                live[x] -= 1
                fps[f._fp(x)] -= 1
            assert +check_layout(f) == +fps
            for fq in range(f.m):
                for fr in range(1 << r):
                    assert f._contains(fq, fr) == (fps[(fq, fr)] > 0)


def test_rate() -> None:
    f = QuotientFilter(10, 8, seed=1)
    for i in range(900):
        assert f.insert(("k", i))
    assert all(f.query(("k", i)) for i in range(900))
    hits = sum(f.query(("z", i)) for i in range(20000))
    assert hits / 20000 < 900 / 1024 / 256 + 0.002
