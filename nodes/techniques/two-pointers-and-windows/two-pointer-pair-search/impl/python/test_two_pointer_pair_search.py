# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-pointer-pair-search/. The authors are listed in prov/XYYCS4.jsonl.

import random

from two_pointer_pair_search import count_pairs_with_sum, two_pointer_pair_search


def test_example() -> None:
    a = [1, 3, 4, 6, 8, 11, 14, 17]
    assert two_pointer_pair_search(a, 22) == (4, 6)
    assert two_pointer_pair_search(a, 24) is None


def test_edges() -> None:
    assert two_pointer_pair_search([], 0) is None
    assert two_pointer_pair_search([5], 10) is None
    assert two_pointer_pair_search([5, 5], 10) == (0, 1)
    assert two_pointer_pair_search([1, 3, 5], 10) is None
    assert two_pointer_pair_search([1, 4, 6, 9], 5) == (0, 1)
    assert two_pointer_pair_search([1, 2, 3, 4], 5) == (0, 3)
    assert two_pointer_pair_search([-5, -1, 0, 2, 7], -6) == (0, 1)
    big = 2**62
    assert two_pointer_pair_search([-big, 0, big], 0) == (0, 2)


def test_against_brute_force() -> None:
    rng = random.Random(20261104)
    for _ in range(2000):
        n = rng.randrange(0, 12)
        a = sorted(rng.randrange(-10, 11) for _ in range(n))
        t = rng.randrange(-22, 23)
        sols = {(i, j) for i in range(n) for j in range(i + 1, n) if a[i] + a[j] == t}
        got = two_pointer_pair_search(a, t)
        if sols:
            assert got is not None
            i, j = got
            assert 0 <= i < j < n and a[i] + a[j] == t
        else:
            assert got is None
        assert count_pairs_with_sum(a, t) == len(sols)
