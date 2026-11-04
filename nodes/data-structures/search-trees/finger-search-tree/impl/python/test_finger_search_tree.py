# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/finger-search-tree/. The authors are listed in prov/X7SV6M.jsonl.

import bisect
import math
import random

from finger_search_tree import FingerSearchTree


def bottoms(t):
    v = t.root
    while not v.bottom:
        v = v.children[0]
    out = []
    while v is not None:
        out.append(v)
        v = v.next
    return out


def test_basic() -> None:
    t = FingerSearchTree()
    t.check_invariant()
    assert not t.search(5) and t.delete(5) is not None
    for k in [50, 20, 80, 10, 30, 60, 90, 40, 70, 15]:
        t.insert(k)
        t.check_invariant()
    assert t.keys() == sorted([50, 20, 80, 10, 30, 60, 90, 40, 70, 15])
    f = t.finger(10)
    assert t.search(90, f) and not t.search(85, f)
    t.delete(50, f)
    t.check_invariant()
    assert not t.search(50) and len(t) == 9


def test_sequential_build_uses_fingers() -> None:
    t = FingerSearchTree()
    f = None
    for k in range(5000):
        f = t.insert(k, f)
        assert t.last_climb <= 1 or k == 0
    t.check_invariant()
    assert t.keys() == list(range(5000))
    assert 6 <= t.height() <= 13


def test_random_against_oracle() -> None:
    rng = random.Random(20251104)
    for case in range(600):
        t = FingerSearchTree()
        ref = []
        f = None
        for _ in range(rng.randrange(1, 120)):
            k = rng.randrange(200)
            op = rng.random()
            if op < 0.55:
                f = t.insert(k, f if rng.random() < 0.7 else None)
                if k not in ref:
                    bisect.insort(ref, k)
                assert k in f.keys
            elif op < 0.85:
                f = t.delete(k, f if rng.random() < 0.7 else None)
                if k in ref:
                    ref.remove(k)
            else:
                g = rng.choice(bottoms(t))
                b, found = t.finger_search(g, k)
                assert found == (k in ref)
                assert (b.lo is None or b.lo < k) and (b.hi is None or k <= b.hi)
                f = b
        t.check_invariant()
        assert t.keys() == ref and len(t) == len(ref)


def test_climb_is_logarithmic_in_distance() -> None:
    rng = random.Random(7)
    t = FingerSearchTree()
    keys = rng.sample(range(10 ** 6), 4000)
    for k in keys:
        t.insert(k)
    ref = sorted(keys)
    nodes = bottoms(t)
    for _ in range(3000):
        g = rng.choice(nodes)
        k = rng.randrange(-10, 10 ** 6 + 10)
        b, found = t.finger_search(g, k)
        i = bisect.bisect_left(ref, k)
        assert found == (i < len(ref) and ref[i] == k)
        if g.hi is not None and k > g.hi:
            d = bisect.bisect_left(ref, k) - bisect.bisect_right(ref, g.hi)
        elif g.lo is not None and k <= g.lo:
            d = bisect.bisect_right(ref, g.lo) - bisect.bisect_right(ref, k)
        else:
            d = 0
        if d == 0:
            assert t.last_climb == 0
        else:
            assert t.last_climb <= math.log2(d) + 1
