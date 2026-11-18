# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/histogram-diff/. The authors are listed in prov/BNZ7EN.jsonl.

import random

from histogram_diff import best_region, histogram_diff, histogram_matching
from txdiff import is_matching, is_valid_script, lcs_matching, matching_to_script, script_cost


def test_page_example() -> None:
    a = ["}", "}", "x", "}", "}", "y"]
    b = ["y", "}", "}", "x", "w"]
    # y is found first, with count 1. The braces have count 4 and are skipped as starting
    # points. The match of x grows backward over two braces and wins, since it is longer.
    assert best_region(a, b, 0, 6, 0, 5) == (0, 3, 1, 4)
    assert histogram_matching(a, b) == [(0, 1), (1, 2), (2, 3)]
    assert script_cost(histogram_diff(a, b)) == 5


def test_lower_count_wins_over_a_longer_run() -> None:
    a = ["z", "s", "k", "s", "k", "u"]
    b = ["s", "k", "v", "u", "w"]
    assert best_region(a, b, 0, 6, 0, 5) == (5, 6, 3, 4)
    assert histogram_matching(a, b) == [(1, 0), (2, 1), (5, 3)]


def test_check_value() -> None:
    a, b = list("uaaav"), list("aaauv")
    assert histogram_matching(a, b) == [(0, 3), (4, 4)]
    assert script_cost(histogram_diff(a, b)) == 6
    assert len(a) + len(b) - 2 * len(lcs_matching(a, b)) == 2


def test_unique_lines_are_not_enough_for_a_minimum() -> None:
    # Every line is unique, but the longest run 6, 7 is taken before the longer subsequence 1, 3, 5.
    a, b = [1, 2, 3, 4, 5, 6, 7], [6, 7, 1, 3, 5]
    assert histogram_matching(a, b) == [(5, 0), (6, 1)]
    assert len(lcs_matching(a, b)) == 3


def test_no_common_line_and_the_fallback() -> None:
    assert best_region(list("ab"), list("cd"), 0, 2, 0, 2) == (0, 0, 0, 0)
    assert histogram_matching(list("ab"), list("cd")) == []
    a, b = list("abab"), list("baba")
    assert histogram_matching(a, b) == [(1, 0), (2, 1), (3, 2)]
    # With max_chain 1, every common line occurs too often, so the range goes to the fallback.
    assert best_region(a, b, 0, 4, 0, 4, max_chain=1) is None
    assert histogram_matching(a, b, max_chain=1) == lcs_matching(a, b)
    assert histogram_matching(a, b, max_chain=1, fallback=None) == []


def test_common_start_and_end() -> None:
    a = list("pqXYZrs")
    b = list("pqZYXrs")
    pairs = histogram_matching(a, b)
    assert pairs[:2] == [(0, 0), (1, 1)] and pairs[-2:] == [(5, 5), (6, 6)]


def test_random_properties() -> None:
    rng = random.Random(13)
    for _ in range(500):
        alpha = "abcdef"[: rng.randint(1, 6)]
        a = [rng.choice(alpha) for _ in range(rng.randint(0, 12))]
        b = [rng.choice(alpha) for _ in range(rng.randint(0, 12))]
        best = len(lcs_matching(a, b))
        for max_chain in (1, 2, 64):
            full = histogram_matching(a, b, max_chain)
            plain = histogram_matching(a, b, max_chain, None)
            for pairs in (full, plain):
                assert is_matching(a, b, pairs) and len(pairs) <= best
                assert is_valid_script(a, b, matching_to_script(a, b, pairs))
            assert set(plain) <= set(full)
        assert len(histogram_matching(a, a)) == len(a)
