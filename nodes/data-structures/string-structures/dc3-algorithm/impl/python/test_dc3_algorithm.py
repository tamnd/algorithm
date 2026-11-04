# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dc3-algorithm/. The authors are listed in prov/13MGBB.jsonl.

import itertools
import random

import pytest

from dc3_algorithm import COVERS, is_difference_cover, naive_suffix_array, suffix_array


def test_example() -> None:
    s = "abracadabra"
    assert suffix_array(s) == [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
    assert suffix_array(s, 7) == naive_suffix_array(s)


def test_covers() -> None:
    for v, d in COVERS.items():
        assert is_difference_cover(d, v)
        # no smaller cover exists
        for r in range(1, len(d)):
            assert not any(is_difference_cover(c, v) for c in itertools.combinations(range(v), r))


def test_edges() -> None:
    for s in ["", "a", "aa", "ab", "ba", "aaaaaaaaaaaaaaaaaaaaaaa", "abababababababababab", "zyxwvutsrqponmlkjihgfedcba"]:
        for v in COVERS:
            assert suffix_array(s, v) == naive_suffix_array(s)
    with pytest.raises(ValueError):
        suffix_array("abc", 5)


def test_random_against_naive() -> None:
    rng = random.Random(3003)
    for case in range(600):
        n = rng.randint(0, 80)
        alpha = "ab" if case % 3 == 0 else "abcd"
        s = "".join(rng.choice(alpha) for _ in range(n))
        v = (3, 7, 13)[case % 3]
        assert suffix_array(s, v) == naive_suffix_array(s)
