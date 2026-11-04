# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/radix-select/. The authors are listed in prov/ZPSQHH.jsonl.

import random

import pytest

from radix_select import radix_select


def test_example() -> None:
    a = [31, 41, 59, 26, 53, 58, 97, 93, 23, 84]
    assert radix_select(a, 5, r=4, w=7) == 53
    assert [radix_select(a, k) for k in range(1, 11)] == sorted(a)


def test_edges() -> None:
    assert radix_select([0], 1) == 0
    assert radix_select([0, 0, 0], 2) == 0
    assert radix_select([7, 7, 3, 7], 1, r=1) == 3
    assert radix_select([2**64 - 1, 0, 2**63], 2, r=16) == 2**63
    with pytest.raises(ValueError):
        radix_select([1, 2], 3)
    with pytest.raises(ValueError):
        radix_select([1, -2], 1)


def test_random_against_sorted() -> None:
    rng = random.Random(4096)
    for _ in range(1500):
        n = rng.randint(1, 80)
        bits = rng.choice([1, 3, 8, 20, 40])
        a = [rng.randrange(1 << bits) for _ in range(n)]
        k = rng.randint(1, n)
        r = rng.choice([1, 2, 3, 4, 8])
        assert radix_select(a, k, r=r) == sorted(a)[k - 1]
