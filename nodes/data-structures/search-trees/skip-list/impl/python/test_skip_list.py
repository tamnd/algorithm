# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/skip-list/. The authors are listed in prov/XYVYKG.jsonl.

import bisect
import random

from skip_list import SkipList


def test_basic() -> None:
    s = SkipList(seed=1)
    for k in [30, 10, 50, 20, 40]:
        assert s.insert(k, str(k))
        s.check_invariant()
    assert list(s.keys()) == [10, 20, 30, 40, 50]
    assert s.search(40) == "40" and s.search(35) is None
    assert not s.insert(40, "x") and s.search(40) == "x" and len(s) == 5
    assert s.floor(35) == 30 and s.ceiling(35) == 40
    assert s.floor(5) is None and s.ceiling(55) is None
    assert s.delete(30) and not s.delete(30)
    s.check_invariant()
    assert list(s.keys()) == [10, 20, 40, 50]


def test_empty() -> None:
    s = SkipList(seed=2)
    s.check_invariant()
    assert s.search(1) is None and not s.delete(1) and s.floor(1) is None
    assert list(s.keys()) == []


def test_level_sizes() -> None:
    s = SkipList(seed=3)
    for k in range(10000):
        s.insert(k)
    sizes = s.level_sizes()
    assert sizes[0] == 10000
    assert all(a >= b for a, b in zip(sizes, sizes[1:]))
    assert 4500 <= sizes[1] <= 5500 and 2000 <= sizes[2] <= 3000
    s.check_invariant()


def test_random_against_sorted_list() -> None:
    rng = random.Random(4242)
    for case in range(500):
        s = SkipList(p=rng.choice([0.25, 0.5]), max_level=rng.choice([4, 16, 32]), seed=case)
        ref: dict[int, int] = {}
        for _ in range(rng.randint(1, 60)):
            k = rng.randint(0, 40)
            op = rng.random()
            if op < 0.5:
                assert s.insert(k, k * 7) == (k not in ref)
                ref[k] = k * 7
            elif op < 0.8:
                assert s.delete(k) == (k in ref)
                ref.pop(k, None)
            else:
                assert s.search(k) == ref.get(k)
            keys = sorted(ref)
            i = bisect.bisect_right(keys, k)
            assert s.floor(k) == (keys[i - 1] if i else None)
            j = bisect.bisect_left(keys, k)
            assert s.ceiling(k) == (keys[j] if j < len(keys) else None)
        s.check_invariant()
        assert list(s.items()) == sorted(ref.items())
        assert len(s) == len(ref)
