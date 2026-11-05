# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shiloach-vishkin-merge/. The authors are listed in prov/T0XRJS.jsonl.

import itertools
import math
import random

import pytest

from shiloach_vishkin_merge import shiloach_vishkin_merge


def stable_merge(a, b):
    return sorted([(x, 0, i) for i, x in enumerate(a)] + [(x, 1, i) for i, x in enumerate(b)])


def test_example() -> None:
    out, s = shiloach_vishkin_merge([1, 4, 6, 9], [2, 3, 7, 8, 10], 3)
    assert out == [1, 2, 3, 4, 6, 7, 8, 9, 10]
    assert s == [(0, 0), (2, 2), (3, 2), (4, 4), (4, 5)]


def test_edges() -> None:
    assert shiloach_vishkin_merge([], [], 4)[0] == []
    assert shiloach_vishkin_merge([1, 2], [], 3)[0] == [1, 2]
    assert shiloach_vishkin_merge([], [1, 2], 3)[0] == [1, 2]
    with pytest.raises(ValueError):
        shiloach_vishkin_merge([1], [2], 0)


def test_small_exhaustive() -> None:
    for m in range(5):
        for n in range(5):
            for a in itertools.product(range(3), repeat=m):
                for b in itertools.product(range(3), repeat=n):
                    a2, b2 = sorted(a), sorted(b)
                    for p in (1, 2, 3, 5):
                        tagged_a = [(x, 0, i) for i, x in enumerate(a2)]
                        tagged_b = [(x, 1, i) for i, x in enumerate(b2)]
                        out, _ = shiloach_vishkin_merge(tagged_a, tagged_b, p)
                        assert out == stable_merge(a2, b2)


def test_piece_sizes() -> None:
    rng = random.Random(7)
    for _ in range(200):
        m, n, p = rng.randrange(60), rng.randrange(60), rng.randrange(1, 12)
        a = sorted(rng.randrange(20) for _ in range(m))
        b = sorted(rng.randrange(20) for _ in range(n))
        out, s = shiloach_vishkin_merge(a, b, p)
        assert out == sorted(a + b)
        assert len(s) - 1 <= 2 * p - 1
        for (i, j), (i2, j2) in zip(s, s[1:]):
            assert i <= i2 and j <= j2
            assert i2 - i <= max(1, math.ceil(m / p)) and j2 - j <= max(1, math.ceil(n / p))


def test_stable_with_custom_keys() -> None:
    class K:
        def __init__(self, k: int, tag: str) -> None:
            self.k, self.tag = k, tag

        def __lt__(self, other: "K") -> bool:
            return self.k < other.k

    a = [K(1, "a0"), K(2, "a1"), K(2, "a2")]
    b = [K(2, "b0"), K(3, "b1")]
    out, _ = shiloach_vishkin_merge(a, b, 2)
    assert [x.tag for x in out] == ["a0", "a1", "a2", "b0", "b1"]
