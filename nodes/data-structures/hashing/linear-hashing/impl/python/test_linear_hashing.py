# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/linear-hashing/. The authors are listed in prov/EA0KDC.jsonl.

import random

import pytest

from linear_hashing import LinearHashing


def layout(t: LinearHashing) -> list[list[int]]:
    return [sorted(k for k, _ in b) for b in t.buckets]


def test_example() -> None:
    t: LinearHashing[int, str] = LinearHashing(2, 1.0, 0.5)
    states = []
    for k in [5, 12, 7, 20, 3, 18, 9]:
        t.insert(k, str(k))
        t.check_invariant()
        states.append((t.level, t.p, layout(t)))
    assert states[2] == (0, 1, [[12], [5, 7], []])
    assert states[3] == (1, 0, [[12, 20], [5], [], [7]])
    assert states[4] == (1, 1, [[], [5], [], [3, 7], [12, 20]])
    assert states[6] == (1, 3, [[], [9], [18], [3, 7], [12, 20], [5], []])
    assert t.address(20) == 4 and t.address(5) == 5 and t.address(7) == 3
    for k in [12, 20, 9]:
        assert t.delete(k)
        t.check_invariant()
    assert (t.level, t.p, len(t.buckets)) == (1, 3, 7)
    assert t.delete(5)
    t.check_invariant()
    assert (t.level, t.p, layout(t)) == (1, 2, [[], [], [18], [3, 7], [], []])
    assert t.search(18) == "18" and t.search(5) is None


def test_edges() -> None:
    t: LinearHashing[int, int] = LinearHashing()
    assert len(t) == 0 and t.search(1) is None and not t.delete(1)
    t.insert(1, 10)
    t.insert(1, 11)  # replace, not a second pair
    assert len(t) == 1 and t.search(1) == 11
    assert t.delete(1) and len(t) == 0 and not t.delete(1)
    t.check_invariant()
    # negative keys, large keys and keys that are not integers
    for k in [-1, -2, -(2**63), 2**63 - 1, 2**64 + 7]:
        t.insert(k, k)
    t.insert("abc", 1)
    t.insert((1, 2), 2)
    t.check_invariant()
    assert t.search(-(2**63)) == -(2**63) and t.search("abc") == 1 and t.search((1, 2)) == 2
    # all keys in one bucket: the structure stays correct
    u: LinearHashing[int, int] = LinearHashing(1, 2.0)
    for i in range(200):
        u.insert(i * 2**20, i)
        u.check_invariant()
    assert all(u.search(i * 2**20) == i for i in range(200))
    # one initial bucket and a load factor below 1, which needs several splits per insert
    w: LinearHashing[int, int] = LinearHashing(1, 0.3, 0.1)
    for i in range(100):
        w.insert(i, i)
        w.check_invariant()
    assert len(w.buckets) >= 100 / 0.3
    for i in range(100):
        assert w.delete(i)
        w.check_invariant()
    assert len(w.buckets) == 1 and w.level == 0 and w.p == 0


def test_bad_parameters() -> None:
    with pytest.raises(ValueError):
        LinearHashing(0)
    with pytest.raises(ValueError):
        LinearHashing(2, 0.0)
    with pytest.raises(ValueError):
        LinearHashing(2, 1.0, 0.6)


def test_random_against_dict() -> None:
    rng = random.Random(1980)
    for _ in range(500):
        n0 = rng.randint(1, 5)
        hi = rng.choice([0.5, 1.0, 2.0, 3.0])
        t: LinearHashing[int, int] = LinearHashing(n0, hi, hi * rng.choice([0.0, 0.25, 0.5]))
        model: dict[int, int] = {}
        span = rng.choice([5, 30, 200])
        for _ in range(rng.randint(0, 80)):
            k = rng.randint(-span, span)
            op = rng.random()
            if op < 0.5:
                v = rng.randint(0, 9)
                t.insert(k, v)
                model[k] = v
            elif op < 0.8:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.search(k) == model.get(k)
            t.check_invariant()
        assert len(t) == len(model)
        assert sorted(t.items()) == sorted(model.items())
