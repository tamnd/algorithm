# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-suffix-automaton/. The authors are listed in prov/NCDQ46.jsonl.

import random

from generalized_suffix_automaton import GeneralizedSuffixAutomaton


def substrings(strings: list[str]) -> set[str]:
    return {s[i:j] for s in strings for i in range(len(s)) for j in range(i + 1, len(s) + 1)}


def end_sets(strings: list[str]) -> set[frozenset]:
    """The distinct sets of end positions (k, e) of the nonempty substrings, plus the root."""
    classes = {frozenset((k, e) for k, s in enumerate(strings) for e in range(len(s)) for _ in [0] if s[:e + 1].endswith(u)) for u in substrings(strings)}
    return classes | {frozenset(["root"])}


def check(strings: list[str]) -> None:
    sam = GeneralizedSuffixAutomaton(strings)
    subs = substrings(strings)
    assert sam.distinct_substrings() == len(subs)
    assert sam.state_count() == len(end_sets(strings))
    total = sum(len(s) for s in strings)
    assert sam.state_count() <= max(1, 2 * total)
    for u in subs:
        assert sam.contains(u)
        assert sam.strings_containing(u) == [k for k, s in enumerate(strings) if u in s]
    for u in ("x", "ax", "ba" * 3):
        if u not in subs:
            assert not sam.contains(u)
    for need in range(1, len(strings) + 1):
        best = max((len(u) for u in subs if sum(u in s for s in strings) >= need), default=0)
        assert sam.longest_common_substring(need) == best
    reach, stack = {0}, [0]
    while stack:
        for w in sam.next[stack.pop()].values():
            if w not in reach:
                reach.add(w)
                stack.append(w)
    assert len(reach) == sam.state_count()


def test_example() -> None:
    sam = GeneralizedSuffixAutomaton(["ab", "cb"])
    assert sam.state_count() == 6
    assert sam.length == [0, 1, 2, 1, 2, 1]
    assert sam.link == [-1, 0, 5, 0, 5, 0]
    assert sam.strings_containing("b") == [0, 1]
    check(["ab", "cb"])
    check(["abab", "baba", "aab"])


def test_special() -> None:
    check([])
    check([""])
    check(["", "a"])
    for n in range(1, 9):
        check(["a" * n])
        check(["ab" * n, "ba" * n])
        check(["a" * n, "a" * (n + 2), "b"])


def test_random() -> None:
    rng = random.Random(11)
    for trial in range(600):
        sigma = (1, 2, 4)[trial % 3]
        count = rng.randrange(1, 5)
        strings = ["".join(rng.choice("acgt"[:sigma]) for _ in range(rng.randrange(0, 9))) for _ in range(count)]
        check(strings)
