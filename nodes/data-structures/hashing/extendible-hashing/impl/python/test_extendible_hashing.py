# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extendible-hashing/. The authors are listed in prov/X591T6.jsonl.

import random

from extendible_hashing import ExtendibleHashing


def layout(t: ExtendibleHashing) -> tuple[int, list[int], list[tuple[int, list[int]]]]:
    bs = t.buckets()
    return t.d, [next(j for j, s in enumerate(bs) if s is x) for x in t.dir], [
        (x.depth, [k for k, _ in x.pairs]) for x in bs
    ]


def test_page_example() -> None:
    t = ExtendibleHashing(b=2, h=lambda k: k)
    for k in [4, 12, 7, 9, 2, 16, 6]:
        t.insert(k, str(k))
        t.check_invariant()
    d, dirs, bs = layout(t)
    assert d == 3
    # buckets in order of first entry: A, B, C, D
    assert dirs == [0, 1, 2, 1, 3, 1, 2, 1]
    assert bs == [(3, [16]), (1, [7, 9]), (2, [2, 6]), (3, [4, 12])]
    assert t.search(12) == "12" and t.search(5) is None
    assert t.delete(9) and not t.delete(9) and len(t) == 6
    t.check_invariant()


def test_split_with_empty_side() -> None:
    t = ExtendibleHashing(b=2, h=lambda k: k)
    for k in [0, 8, 16]:  # equal in the low 3 bits: needs 4 splits on one insert
        t.insert(k, k)
        t.check_invariant()
    assert t.d == 4 and all(t.search(k) == k for k in [0, 8, 16])


def test_equal_hash_values_overflow() -> None:
    u = ExtendibleHashing(b=1, w=5)
    u.insert(-1, 1)
    u.insert(-2, 2)  # same built-in hash value
    u.check_invariant()
    assert u.d == 5 and u.search(-1) == 1 and u.search(-2) == 2
    t = ExtendibleHashing(b=1, h=lambda k: 5, w=3)
    for k in range(4):
        t.insert(k, k)
        t.check_invariant()
    assert all(t.search(k) == k for k in range(4)) and len(t) == 4
    assert t.d == 3 and len(t.dir) == 8


def test_edges() -> None:
    t = ExtendibleHashing(b=1, w=16)
    assert t.search("a") is None and not t.delete("a") and len(t) == 0
    t.insert("a", 1)
    t.insert("a", 2)
    assert t.search("a") == 2 and len(t) == 1
    for k in [2**63 - 1, -(2**63), -1, 0, 2**64 + 3]:
        t.insert(k, k)
        t.check_invariant()
    assert all(t.search(k) == k for k in [2**63 - 1, -(2**63), -1, 0, 2**64 + 3])


def test_random_against_dict() -> None:
    rng = random.Random(1979)
    for _ in range(600):
        t = ExtendibleHashing(b=rng.randint(1, 4), w=12)  # hash(-1) == hash(-2) in Python
        model: dict[int, int] = {}
        for _ in range(rng.randint(0, 60)):
            k = rng.randint(-40, 40)
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
