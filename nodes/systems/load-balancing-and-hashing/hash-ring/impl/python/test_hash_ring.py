# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hash-ring/. The authors are listed in prov/XP6DXP.jsonl.

import random

import pytest

from hash_ring import HashRing


def naive_successor(points: dict[int, str], size: int, x: int) -> tuple[int, str]:
    p = min(points, key=lambda q: (q - x) % size)
    return p, points[p]


def test_page_example() -> None:
    r: HashRing[str] = HashRing(100)
    for p, s in [(12, "A"), (47, "B"), (80, "C")]:
        r.insert(p, s)
    assert r.successor(5) == (12, "A")
    assert r.successor(30) == (47, "B")
    assert r.successor(47) == (47, "B")
    assert r.successor(50) == (80, "C")
    assert r.successor(90) == (12, "A")
    assert r.shares() == {"A": 32, "B": 35, "C": 33}
    r.insert(40, "D")
    assert r.successor(30) == (40, "D")
    assert r.shares() == {"A": 32, "D": 28, "B": 7, "C": 33}
    assert r.arc(12) == (80, 12)
    assert r.remove(80) == "C"
    assert r.successor(50) == (12, "A")
    assert r.shares() == {"A": 65, "D": 28, "B": 7}


def test_single_point_owns_everything() -> None:
    r: HashRing[str] = HashRing(10)
    r.insert(3, "x")
    assert r.arc_length(3) == 10
    assert all(r.successor(x) == (3, "x") for x in range(10))


def test_errors() -> None:
    r: HashRing[str] = HashRing(10)
    with pytest.raises(LookupError):
        r.successor(0)
    r.insert(4, "a")
    with pytest.raises(KeyError):
        r.insert(4, "b")
    with pytest.raises(KeyError):
        r.remove(5)
    with pytest.raises(ValueError):
        r.insert(10, "c")


def test_random_operations_against_naive() -> None:
    rng = random.Random(11)
    size = 1000
    r: HashRing[str] = HashRing(size)
    ref: dict[int, str] = {}
    for step in range(3000):
        op = rng.random()
        if op < 0.45 or not ref:
            p = rng.randrange(size)
            if p in ref:
                with pytest.raises(KeyError):
                    r.insert(p, "dup")
            else:
                r.insert(p, f"s{step}")
                ref[p] = f"s{step}"
        elif op < 0.75:
            p = rng.choice(sorted(ref))
            assert r.remove(p) == ref.pop(p)
        else:
            x = rng.randrange(size)
            assert r.successor(x) == naive_successor(ref, size, x)
        assert r.pos == sorted(ref)
        if ref:
            assert sum(r.shares().values()) == size


def test_arcs_partition_the_ring() -> None:
    rng = random.Random(3)
    size = 500
    r: HashRing[int] = HashRing(size)
    for p in rng.sample(range(size), 40):
        r.insert(p, p)
    for x in range(size):
        p, _ = r.successor(x)
        a, b = r.arc(p)
        assert (x - a) % size != 0 and (x - a) % size <= (b - a) % size
