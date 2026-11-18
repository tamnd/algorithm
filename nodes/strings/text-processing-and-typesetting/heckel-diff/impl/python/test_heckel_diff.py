# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heckel-diff/. The authors are listed in prov/T7BYC1.jsonl.
# This file also tests the shared helper txdiff.py, whose reference copy is in this folder.

import difflib
import itertools
import random
from collections import Counter

from heckel_diff import heckel_diff, heckel_links, increasing_pairs
from txdiff import (DELETE, INSERT, KEEP, Op, apply_script, is_matching, is_valid_script, lcs_matching,
                    matching_to_script, script_cost, script_matching, split_lines, unified_diff)


def lcs_brute(a, b):
    for r in range(min(len(a), len(b)), -1, -1):
        for ia in itertools.combinations(range(len(a)), r):
            sub = [a[i] for i in ia]
            for jb in itertools.combinations(range(len(b)), r):
                if sub == [b[j] for j in jb]:
                    return r
    return 0


def test_helper_split_and_apply() -> None:
    assert split_lines("") == []
    assert split_lines("x\n") == ["x"]
    assert split_lines("x\ny") == ["x", "y"]
    assert split_lines("\n\n") == ["", ""]
    assert unified_diff([], [], []) == []
    assert not is_valid_script("ab", "b", [Op(KEEP, 0, 0, "a"), Op(DELETE, 1, 1, "b")])
    assert apply_script("ab", [Op(DELETE, 0, 0, "a"), Op(KEEP, 1, 0, "b"), Op(INSERT, 2, 1, "c")]) == ["b", "c"]


def test_helper_against_brute_force_and_difflib() -> None:
    rng = random.Random(5)
    for _ in range(300):
        a = [rng.choice("abc") for _ in range(rng.randint(0, 6))]
        b = [rng.choice("abc") for _ in range(rng.randint(0, 6))]
        pairs = lcs_matching(a, b)
        assert is_matching(a, b, pairs)
        assert len(pairs) == lcs_brute(a, b)
        s = matching_to_script(a, b, pairs)
        assert is_valid_script(a, b, s)
        assert script_matching(s) == pairs
        assert script_cost(s) == len(a) + len(b) - 2 * len(pairs)
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        dp = [(blk.a + t, blk.b + t) for blk in sm.get_matching_blocks() for t in range(blk.size)]
        for n in (0, 1, 3):
            assert unified_diff(a, b, matching_to_script(a, b, dp), n) == list(
                difflib.unified_diff(a, b, "a", "b", lineterm="", n=n))


def test_check_value_is_not_minimal() -> None:
    a, b = list("uaaav"), list("aaauv")
    assert heckel_links(a, b) == [(0, 3), (4, 4)]
    script, moved = heckel_diff(a, b)
    assert is_valid_script(a, b, script)
    assert script_cost(script) == 6
    assert moved == []
    assert len(a) + len(b) - 2 * len(lcs_matching(a, b)) == 2


def test_moved_function() -> None:
    old = ["int f()", "{", "return 1;", "}", "int g()", "{", "return 2;", "}"]
    new = old[4:] + old[:4]
    assert heckel_links(old, new) == [(4, 0), (5, 1), (6, 2), (7, 3), (0, 4), (1, 5), (2, 6), (3, 7)]
    script, moved = heckel_diff(old, new)
    assert is_valid_script(old, new, script)
    assert moved == [(4, 0, 4)]
    assert script_cost(script) == 8


def test_passes_four_and_five_extend_runs() -> None:
    # The braces are not unique. Pass 4 links the first braces from the begin line, then
    # each closing brace from the unique line before it. The second opening braces stay unlinked.
    old = ["{", "x", "}", "{", "y", "}"]
    new = ["{", "y", "}", "{", "x", "}"]
    assert heckel_links(old, new) == [(0, 0), (4, 1), (5, 2), (1, 4), (2, 5)]
    script, moved = heckel_diff(old, new)
    assert script_cost(script) == 6 and moved == [(4, 1, 2)]
    # Equal first and last lines are linked from the begin and end lines.
    assert heckel_links(list("aab"), list("aac")) == [(0, 0), (1, 1)]
    assert heckel_links(list("baa"), list("caa")) == [(1, 1), (2, 2)]


def test_random_properties() -> None:
    rng = random.Random(7)
    for _ in range(400):
        alpha = "abcdefgh"[: rng.randint(1, 8)]
        a = [rng.choice(alpha) for _ in range(rng.randint(0, 9))]
        b = [rng.choice(alpha) for _ in range(rng.randint(0, 9))]
        links = heckel_links(a, b)
        assert all(a[i] == b[j] for i, j in links)
        assert len({i for i, _ in links}) == len(links) == len({j for _, j in links})
        ca, cb = Counter(a), Counter(b)
        for j, x in enumerate(b):
            if ca[x] == 1 and cb[x] == 1:
                assert (a.index(x), j) in links
        kept = increasing_pairs(links)
        assert is_matching(a, b, kept)
        script, _ = heckel_diff(a, b)
        assert is_valid_script(a, b, script)
        assert script_cost(script) >= len(a) + len(b) - 2 * len(lcs_matching(a, b))


def test_permutations_are_minimal() -> None:
    # When every line occurs once in each file, all lines are linked and the kept pairs are an LCS.
    rng = random.Random(11)
    for n in range(0, 9):
        for _ in range(20):
            a = list(range(n))
            b = a[:]
            rng.shuffle(b)
            script, _ = heckel_diff(a, b)
            assert script_cost(script) == 2 * n - 2 * len(lcs_matching(a, b))
