# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patience-diff/. The authors are listed in prov/3MB06K.jsonl.

import random
from collections import Counter

from patience_diff import longest_increasing, patience_diff, patience_matching, unique_common
from txdiff import is_matching, is_valid_script, lcs_matching, matching_to_script, script_cost, unified_diff

OLD = ["void func1() {", "    x += 1", "}", "", "void func2() {", "    x += 2", "}"]
NEW = ["void func1() {", "    x += 1", "}", "", "void functhreehalves() {", "    x += 1.5", "}", "",
       "void func2() {", "    x += 2", "}"]


def test_inserted_function() -> None:
    pairs = patience_matching(OLD, NEW)
    assert pairs == [(0, 0), (1, 1), (2, 2), (3, 3), (4, 8), (5, 9), (6, 10)]
    diff = unified_diff(OLD, NEW, matching_to_script(OLD, NEW, pairs))
    assert diff[6:10] == ["+void functhreehalves() {", "+    x += 1.5", "+}", "+"]
    # A shifted matching of the same length keeps the closing brace and blank line of func1
    # with those of the new function. It is just as short, so a minimum diff may print it.
    shifted = [(0, 0), (1, 1), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10)]
    assert is_matching(OLD, NEW, shifted) and len(shifted) == len(lcs_matching(OLD, NEW))


def test_check_value() -> None:
    a, b = list("uaaav"), list("aaauv")
    for fallback in (None, "lcs"):
        assert patience_matching(a, b, fallback) == [(0, 3), (4, 4)]
        assert script_cost(patience_diff(a, b, fallback)) == 6
    assert len(a) + len(b) - 2 * len(lcs_matching(a, b)) == 2


def test_counts_are_taken_again_in_each_gap() -> None:
    # Only U is unique in the whole files, but a and b are unique inside each gap.
    a, b = list("abUba"), list("baUab")
    assert unique_common(a, b, 0, 5, 0, 5) == [(2, 2)]
    assert patience_matching(a, b) == [(1, 0), (2, 2), (4, 3)]


def test_fallback() -> None:
    a, b = list("abab"), list("baba")
    assert patience_matching(a, b) == []
    assert patience_matching(a, b, "lcs") == [(1, 0), (2, 1), (3, 2)]


def test_longest_increasing() -> None:
    assert longest_increasing([]) == []
    assert longest_increasing([(0, 3), (1, 1), (2, 2), (3, 0), (4, 4)]) == [(1, 1), (2, 2), (4, 4)]


def test_unique_lines_give_a_longest_matching() -> None:
    rng = random.Random(3)
    for n in range(0, 12):
        for _ in range(20):
            a = list(range(n))
            b = [x for x in a if rng.random() < 0.8] + [100 + t for t in range(rng.randint(0, 3))]
            rng.shuffle(b)
            pairs = patience_matching(a, b)
            assert len(pairs) == len(lcs_matching(a, b))


def test_random_properties() -> None:
    rng = random.Random(9)
    for _ in range(500):
        alpha = "abcdefg"[: rng.randint(1, 7)]
        a = [rng.choice(alpha) for _ in range(rng.randint(0, 10))]
        b = [rng.choice(alpha) for _ in range(rng.randint(0, 10))]
        best = len(lcs_matching(a, b))
        plain = patience_matching(a, b)
        full = patience_matching(a, b, "lcs")
        for pairs in (plain, full):
            assert is_matching(a, b, pairs)
            assert len(pairs) <= best
            assert is_valid_script(a, b, matching_to_script(a, b, pairs))
        # The fallback only adds pairs in ranges that have no unique common line.
        assert set(plain) <= set(full)
        ca, cb = Counter(a), Counter(b)
        if a and b and all(ca[x] == 1 for x in a) and all(cb[x] == 1 for x in b):
            assert len(plain) == best
