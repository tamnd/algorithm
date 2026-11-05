# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/suffix-automaton/. The authors are listed in prov/XE8A8C.jsonl.

import itertools
import random

from suffix_automaton import SuffixAutomaton


def endpos_classes(s: str) -> int:
    """The number of distinct end-position sets of substrings, the empty one included."""
    sets = set()
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            x = s[i:j]
            sets.add(frozenset(k + len(x) - 1 for k in range(len(s) - len(x) + 1) if s[k:k + len(x)] == x))
    return len(sets) + 1


def naive_count(s: str, p: str) -> int:
    return sum(1 for i in range(len(s) - len(p) + 1) if s[i:i + len(p)] == p)


def test_example() -> None:
    a = SuffixAutomaton("abbb")
    a.check_invariant()
    assert a.state_count() == 7
    assert a.count("b") == 3 and a.count("bb") == 2 and a.count("abb") == 1
    assert a.is_suffix("bbb") and not a.is_suffix("ab")
    a = SuffixAutomaton("banana")
    a.check_invariant()
    assert a.distinct_substrings() == 15
    assert a.count("ana") == 2 and a.first_occurrence("ana") == 1
    assert a.first_occurrence("na") == 2 and a.first_occurrence("nab") == -1


def test_edges() -> None:
    a = SuffixAutomaton("")
    assert a.state_count() == 1 and a.contains("") and not a.contains("a")
    assert a.count("") == 0 and a.distinct_substrings() == 0
    for n in (1, 2, 10, 1000):
        a = SuffixAutomaton("a" * n)
        a.check_invariant()
        assert a.state_count() == n + 1 and a.distinct_substrings() == n
        k = max(1, n // 2)
        assert a.count("a" * k) == n - k + 1
    for n in (3, 4, 7, 12):
        assert SuffixAutomaton("a" + "b" * (n - 1)).state_count() == 2 * n - 1
        assert SuffixAutomaton("a" + "b" * (n - 2) + "c").transition_count() == 3 * n - 4
    a = SuffixAutomaton([1, 2, 1, 2, 3])
    assert a.count([1, 2]) == 2 and a.is_suffix([2, 3])


def test_random_against_naive() -> None:
    rng = random.Random(1985)
    for trial in range(600):
        sigma = "abcd"[: rng.choice([1, 2, 4])]
        n = rng.randint(0, 14)
        s = "".join(rng.choice(sigma) for _ in range(n))
        if trial % 30 == 0:
            s = rng.choice(["a" * n, "ab" * (n // 2), ""])
        a = SuffixAutomaton(s)
        a.check_invariant()
        assert a.state_count() == endpos_classes(s)
        subs = {s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
        assert a.distinct_substrings() == len(subs)
        for k in range(0, min(len(s), 5) + 2):
            for t in itertools.product(sigma + "e" if k < 3 else sigma, repeat=k):
                p = "".join(t)
                assert a.contains(p) == (p in s)
                assert a.is_suffix(p) == s.endswith(p)
                assert a.count(p) == (naive_count(s, p) if p else len(s))
                assert a.first_occurrence(p) == s.find(p)
