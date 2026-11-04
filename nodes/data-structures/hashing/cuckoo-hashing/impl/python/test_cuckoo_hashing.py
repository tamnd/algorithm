# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cuckoo-hashing/. The authors are listed in prov/FHYWMC.jsonl.

import random

from cuckoo_hashing import CuckooHashing, random_pair


def example_then_random():
    calls = [0]

    def factory(r, rng):
        calls[0] += 1
        if calls[0] == 1:
            return (lambda k: k % r), (lambda k: (k // r) % r)
        return random_pair(r, rng)

    return factory


def test_page_example() -> None:
    t = CuckooHashing(11, factory=example_then_random(), rng=random.Random(1))
    assert t.max_loop == 76
    for k in [20, 50, 53, 75, 100, 67, 105, 3, 36, 39]:
        t.insert(k, -k)
        t.check_invariant()
    assert t.rehashes == 0 and t.r == 11 and len(t) == 10
    assert [c and c[0] for c in t.t1] == [None, 100, None, 36, None, None, 50, None, None, 75, None]
    assert [c and c[0] for c in t.t2] == [3, 20, None, 39, 53, None, 67, None, None, 105, None]
    assert t.search(67) == -67 and t.search(4) is None
    assert t.delete(67) and t.search(67) is None and not t.delete(67)
    t.check_invariant()


def test_cycle_forces_rehash() -> None:
    t = CuckooHashing(11, factory=example_then_random(), rng=random.Random(2))
    for k in [1, 122, 243]:
        t.insert(k, k)
        t.check_invariant()
    assert t.rehashes >= 1
    assert all(t.search(k) == k for k in [1, 122, 243])


def test_edges() -> None:
    t = CuckooHashing(1, rng=random.Random(3))
    assert t.search("x") is None and not t.delete("x") and len(t) == 0
    t.insert("x", 1)
    t.insert("x", 2)
    assert len(t) == 1 and t.search("x") == 2
    t.check_invariant()
    for k in [2**63 - 1, -(2**63), -1, 0, 2**64]:
        t.insert(k, k)
        t.check_invariant()
    assert all(t.search(k) == k for k in [2**63 - 1, -(2**63), -1, 0, 2**64])


def test_random_against_dict() -> None:
    rng = random.Random(777)
    for _ in range(600):
        t = CuckooHashing(rng.randint(1, 6), rng=random.Random(rng.random()))
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 60)):
            k = rng.randint(-30, 30)
            op = rng.random()
            if op < 0.5:
                v = rng.randint(0, 99)
                t.insert(k, v)
                model[k] = v
            elif op < 0.75:
                assert t.delete(k) == (k in model)
                model.pop(k, None)
            else:
                assert t.search(k) == model.get(k)
            t.check_invariant()
            assert len(t) == len(model)
        assert dict(t.items()) == model
