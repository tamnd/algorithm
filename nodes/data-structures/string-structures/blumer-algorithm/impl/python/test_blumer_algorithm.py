# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/blumer-algorithm/. The authors are listed in prov/EMPS9K.jsonl.

import random

from blumer_algorithm import SuffixAutomaton


def endpos_classes(s: str) -> int:
    """The number of states of the minimal suffix automaton: distinct end-position sets, plus the initial state."""
    sets = set()
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            w = s[i:j]
            sets.add(frozenset(k + len(w) for k in range(len(s) - len(w) + 1) if s.startswith(w, k)))
    return len(sets) + 1


def test_example() -> None:
    a = SuffixAutomaton()
    sizes = []
    for c in "abbb":
        a.extend(c)
        a.check_invariant()
        sizes.append(a.num_states())
    assert sizes == [2, 3, 5, 7]
    assert a.length == [0, 1, 2, 3, 1, 4, 2]
    assert a.link == [-1, 0, 4, 6, 0, 6, 4]
    assert a.nxt == [{"a": 1, "b": 4}, {"b": 2}, {"b": 3}, {"b": 5}, {"b": 6}, {}, {"b": 5}]
    assert a.count_distinct_substrings() == 7
    assert a.contains("abb") and not a.contains("ba")
    assert a.is_suffix("bb") and not a.is_suffix("ab")


def test_edges() -> None:
    a = SuffixAutomaton("")
    a.check_invariant()
    assert a.num_states() == 1 and a.contains("") and a.is_suffix("")
    a = SuffixAutomaton("aaaa")
    a.check_invariant()
    assert a.num_states() == 5 and a.count_distinct_substrings() == 4
    # the worst case for states: a b^(n-1) has 2n - 1 states
    n = 9
    assert SuffixAutomaton("a" + "b" * (n - 1)).num_states() == 2 * n - 1
    # the worst case for transitions: a b^(n-2) c has 3n - 4 transitions
    assert SuffixAutomaton("a" + "b" * (n - 2) + "c").num_transitions() == 3 * n - 4


def test_random_against_naive() -> None:
    rng = random.Random(1985)
    for case in range(600):
        s = "".join(rng.choice("ab" if case % 2 else "abc") for _ in range(rng.randint(0, 14)))
        a = SuffixAutomaton(s)
        a.check_invariant()
        subs = {s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
        assert a.count_distinct_substrings() == len(subs)
        assert a.num_states() == endpos_classes(s)
        for _ in range(5):
            w = "".join(rng.choice("abc") for _ in range(rng.randint(0, 4)))
            assert a.contains(w) == (w in subs or w == "")
            assert a.is_suffix(w) == s.endswith(w)
