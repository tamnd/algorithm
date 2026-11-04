# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/robin-hood-hashing/. The authors are listed in prov/CR9J17.jsonl.

import random

import pytest

from robin_hood_hashing import RobinHoodTable


def ident(k: int) -> int:
    return k


def linear_probing_distances(keys: list[int], m: int) -> list[int]:
    """Plain first-come linear probing, as an independent oracle for the sum of distances."""
    slot: list[int | None] = [None] * m
    for k in keys:
        j = k % m
        while slot[j] is not None:
            j = (j + 1) % m
        slot[j] = k
    return [(j - k % m) % m for j, k in enumerate(slot) if k is not None]


def test_example() -> None:
    t: RobinHoodTable[int, int] = RobinHoodTable(capacity=8, max_load=0.875, hash_fn=ident)
    for k in (8, 1, 16, 2, 24, 9):
        t.put(k, 10 * k)
        t.check_invariant()
    assert t._keys == [8, 16, 24, 1, 9, 2, None, None]
    assert t._dist == [0, 1, 2, 2, 3, 3, -1, -1]
    assert t.search(9) == 4
    assert t.search(17) is None and t.search(32) is None
    assert t.delete(16)
    assert t._keys == [8, 24, 1, 9, 2, None, None, None]
    assert t._dist == [0, 1, 1, 2, 2, -1, -1, -1]
    assert t.get(9) == 90 and t.get(2) == 20
    t.check_invariant()


def test_same_total_less_spread_than_linear_probing() -> None:
    keys = [8, 1, 16, 2, 24, 9]
    plain = linear_probing_distances(keys, 8)
    t: RobinHoodTable[int, int] = RobinHoodTable(capacity=8, max_load=0.875, hash_fn=ident)
    for k in keys:
        t.put(k, k)
    rh = t.distances()
    assert sum(plain) == sum(rh) == 11
    assert sum(d * d for d in plain) == 37 and sum(d * d for d in rh) == 27
    assert max(plain) == 4 and max(rh) == 3


def test_edges() -> None:
    t: RobinHoodTable[int, str] = RobinHoodTable(capacity=2)
    assert len(t) == 0 and t.get(1) is None and not t.delete(1)
    t.put(1, "a")
    t.put(1, "b")
    assert len(t) == 1 and t.get(1) == "b"
    assert t.delete(1) and len(t) == 0 and 1 not in t
    t.check_invariant()
    with pytest.raises(ValueError):
        RobinHoodTable(capacity=1)


def test_wrap_around_and_one_home() -> None:
    t: RobinHoodTable[int, int] = RobinHoodTable(capacity=8, max_load=0.875, hash_fn=lambda k: 6)
    for k in range(5):
        t.put(k, k)
        t.check_invariant()
    assert t.distances() == [2, 3, 4, 0, 1]  # slots 0, 1, 2 wrap around after 6, 7
    t.delete(0)
    t.check_invariant()
    assert sorted(k for k, _ in t.items()) == [1, 2, 3, 4]


def test_random_against_dict() -> None:
    rng = random.Random(1985)
    for trial in range(500):
        m = rng.choice([2, 4, 8, 16])
        hash_fn = (lambda k: k % 5) if trial % 4 == 0 else hash
        t: RobinHoodTable[int, int] = RobinHoodTable(capacity=m, max_load=rng.choice([0.5, 0.75, 0.9]), hash_fn=hash_fn)
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(-30, 30)
            op = rng.random()
            if op < 0.55:
                v = rng.randint(0, 99)
                t.put(k, v)
                model[k] = v
            elif op < 0.8:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.get(k) == model.get(k)
            t.check_invariant()
            assert len(t) == len(model)
        assert sorted(t.items()) == sorted(model.items())


def test_random_sum_and_squares_against_linear_probing() -> None:
    rng = random.Random(2004)
    for _ in range(500):
        m = rng.choice([4, 8, 16, 32])
        keys = rng.sample(range(200), rng.randint(0, m - 2))
        t: RobinHoodTable[int, int] = RobinHoodTable(capacity=m, max_load=0.99, hash_fn=ident)
        for k in keys:
            t.put(k, k)
        assert t.capacity == m
        plain = linear_probing_distances(keys, m)
        rh = t.distances()
        assert sum(rh) == sum(plain)
        assert sum(d * d for d in rh) <= sum(d * d for d in plain)
