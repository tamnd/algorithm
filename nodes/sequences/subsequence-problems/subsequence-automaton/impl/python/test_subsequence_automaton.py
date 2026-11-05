# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/subsequence-automaton/. The authors are listed in prov/BAZPF7.jsonl.

import itertools
import random

from subsequence_automaton import CompactSubsequenceIndex, SubsequenceAutomaton


def is_subsequence(p: str, t: str) -> bool:
    it = iter(t)
    return all(c in it for c in p)


def test_banana() -> None:
    a = SubsequenceAutomaton("banana")
    assert [a.step(0, c) for c in "abn"] == [2, 1, 3]
    assert a.step(3, "a") == 4 and a.step(3, "n") == 5 and a.step(3, "b") is None
    assert a.contains("bnn") and a.contains("aaa") and a.contains("")
    assert not a.contains("nb") and not a.contains("aaaa") and not a.contains("x")
    assert a.count_distinct_subsequences() == 40


def test_counts() -> None:
    assert SubsequenceAutomaton("").count_distinct_subsequences() == 1
    assert SubsequenceAutomaton("aaa").count_distinct_subsequences() == 4
    assert SubsequenceAutomaton("abc").count_distinct_subsequences() == 8
    assert SubsequenceAutomaton("ABCBDAB").count_distinct_subsequences() == 102


def test_random_against_brute_force() -> None:
    rng = random.Random(1991)
    for _ in range(200):
        t = "".join(rng.choice("abc") for _ in range(rng.randrange(10)))
        a = SubsequenceAutomaton(t)
        c = CompactSubsequenceIndex(t)
        subs = {"".join(s) for k in range(len(t) + 1) for s in itertools.combinations(t, k)}
        assert a.count_distinct_subsequences() == len(subs)
        for _ in range(30):
            p = "".join(rng.choice("abcd") for _ in range(rng.randrange(6)))
            assert a.contains(p) == c.contains(p) == is_subsequence(p, t)
