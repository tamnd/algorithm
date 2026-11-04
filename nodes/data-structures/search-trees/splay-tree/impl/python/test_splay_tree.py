# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/splay-tree/. The authors are listed in prov/MX6QFK.jsonl.

import bisect
import math
import random

from splay_tree import SplayTree


def test_example() -> None:
    t = SplayTree()
    for k in [1, 2, 3, 4, 5, 6, 7]:
        t.insert(k)
    t.check_invariant()
    assert t.height() == 6 and t.root.key == 7
    assert t.search(1) is None and t.root.key == 1
    assert t.height() == 4
    assert t.insert(3, "c") is False and t.root.key == 3 and t.search(3) == "c"
    assert t.delete(3) and 3 not in t and len(t) == 6
    t.check_invariant()
    assert list(t.keys()) == [1, 2, 4, 5, 6, 7]


def test_split_join() -> None:
    t = SplayTree()
    for k in range(0, 100, 3):
        t.insert(k)
    u = t.split(50)
    t.check_invariant()
    u.check_invariant()
    assert list(t.keys()) == list(range(0, 51, 3)) and list(u.keys()) == list(range(51, 100, 3))
    t.join(u)
    t.check_invariant()
    assert list(t.keys()) == list(range(0, 100, 3)) and len(u) == 0


def test_sequential_access_is_linear() -> None:
    n = 2000
    t = SplayTree()
    keys = list(range(n))
    random.Random(5).shuffle(keys)
    for k in keys:
        t.insert(k)
    t.rotations = 0
    for k in range(n):
        assert t.search(k) is None
    assert t.rotations <= 5 * n


def test_amortized_bound_on_chain_accesses() -> None:
    n = 1024
    t = SplayTree()
    for k in range(n):
        t.insert(k)
    t.rotations = 0
    m = 4000
    rng = random.Random(8)
    for _ in range(m):
        t.access(rng.randrange(n))
    assert t.rotations <= m * (3 * math.log2(n) + 1) + n * math.log2(n)


def test_random_against_sorted_dict() -> None:
    rng = random.Random(2718)
    for _ in range(500):
        t = SplayTree()
        ref: dict[int, int] = {}
        for _ in range(rng.randint(1, 60)):
            k = rng.randint(0, 40)
            op = rng.random()
            if op < 0.45:
                assert t.insert(k, -k) == (k not in ref)
                ref[k] = -k
                assert t.root.key == k
            elif op < 0.75:
                assert t.delete(k) == (k in ref)
                ref.pop(k, None)
            elif op < 0.9:
                assert t.search(k) == ref.get(k)
            else:
                ks = sorted(ref)
                i = bisect.bisect_right(ks, k)
                assert t.floor(k) == (ks[i - 1] if i else None)
        t.check_invariant()
        assert list(t.items()) == sorted(ref.items())
        if ref and rng.random() < 0.5:
            cut = rng.randint(-1, 41)
            u = t.split(cut)
            t.check_invariant()
            u.check_invariant()
            assert list(t.keys()) == [k for k in sorted(ref) if k <= cut]
            assert list(u.keys()) == [k for k in sorted(ref) if k > cut]
            t.join(u)
            t.check_invariant()
            assert t.minimum() == min(ref)
