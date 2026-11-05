# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-superstring-merge/. The authors are listed in prov/HBAFAC.jsonl.

import itertools
import random
from typing import List, Sequence

from greedy_superstring_merge import (
    greedy_merge_order,
    greedy_superstring,
    overlap,
    reduce_strings,
)


def ov(x: str, y: str) -> int:
    for k in range(min(len(x), len(y)), -1, -1):
        if x[len(x) - k :] == y[:k]:
            return k
    return 0


def naive_merge(strings: Sequence[str]) -> str:
    # The string form: merge two current strings with the largest overlap,
    # ties by the smaller tail index, then the smaller head index.
    s = reduce_strings(strings)
    chains: List[List[int]] = [[i] for i in range(len(s))]
    text = list(s)
    while len(chains) > 1:
        best = None
        for a in range(len(chains)):
            for b in range(len(chains)):
                if a != b:
                    w = ov(text[a], text[b])
                    key = (-w, chains[a][-1], chains[b][0])
                    if best is None or key < best[0]:
                        best = (key, a, b, w)
        assert best is not None
        _, a, b, w = best
        new_text = text[a] + text[b][w:]
        new_chain = chains[a] + chains[b]
        for x in sorted((a, b), reverse=True):
            del chains[x]
            del text[x]
        chains.append(new_chain)
        text.append(new_text)
    return text[0] if text else ""


def optimum(strings: Sequence[str]) -> int:
    s = reduce_strings(strings)
    if not s:
        return 0
    best = None
    for p in itertools.permutations(range(len(s))):
        length = len(s[p[0]])
        for a, b in zip(p, p[1:]):
            length += len(s[b]) - ov(s[a], s[b])
        best = length if best is None else min(best, length)
    assert best is not None
    return best


def check(strings: List[str]) -> None:
    g = greedy_superstring(strings)
    assert g == naive_merge(strings), (strings, g)
    for x in strings:
        assert x in g
    opt = optimum(strings)
    assert opt <= len(g) <= 4 * opt or (opt == 0 and g == "")
    kept = reduce_strings(strings)
    total = sum(map(len, kept))
    assert 2 * (total - len(g)) >= total - opt
    _, merges = greedy_merge_order(strings)
    assert len(g) == total - sum(w for _, _, w in merges)


def test_example() -> None:
    s, merges = greedy_merge_order(["abb", "bba", "bbb"])
    assert s == ["abb", "bba", "bbb"]
    assert merges == [(0, 1, 2), (1, 2, 0)]
    assert greedy_superstring(["abb", "bba", "bbb"]) == "abbabbb"
    assert greedy_superstring(["abb", "bbb", "bba"]) == "abbba"
    assert optimum(["abb", "bba", "bbb"]) == 5


def test_overlap() -> None:
    assert overlap("abb", "bba") == 2
    assert overlap("bba", "abb") == 1
    assert overlap("bba", "bbb") == 0
    assert overlap("", "a") == 0
    assert overlap("aaa", "aa") == 2


def test_edge_cases() -> None:
    assert greedy_superstring([]) == ""
    assert greedy_superstring([""]) == ""
    assert greedy_superstring(["", ""]) == ""
    assert greedy_superstring(["a"]) == "a"
    assert greedy_superstring(["a", "a"]) == "a"
    assert greedy_superstring(["ab", "b"]) == "ab"
    assert greedy_superstring(["aaa", "aa", "a"]) == "aaa"
    assert greedy_superstring(["ab", "ba"]) == "aba"
    assert reduce_strings(["b", "ab", "b", "abc"]) == ["abc"]


def test_lower_bound_family() -> None:
    for k in range(1, 8):
        bad = ["a" + "b" * k, "b" * k + "a", "b" * (k + 1)]
        good = [bad[0], bad[2], bad[1]]
        assert len(greedy_superstring(bad)) == 2 * k + 3
        assert len(greedy_superstring(good)) == k + 3
        assert optimum(bad) == k + 3


def test_exhaustive_small() -> None:
    for k in (1, 2, 3):
        alphabet = "abc"[:k]
        words = [
            "".join(w) for n in range(0, 4) for w in itertools.product(alphabet, repeat=n)
        ]
        limit = 3 if k < 3 else 2
        for m in range(1, limit + 1):
            for strings in itertools.product(words, repeat=m):
                check(list(strings))


def test_random() -> None:
    rng = random.Random(2026)
    for _ in range(600):
        k = rng.choice((1, 2, 3))
        alphabet = "abc"[:k]
        m = rng.randint(0, 6)
        strings = [
            "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 6))) for _ in range(m)
        ]
        check(strings)


if __name__ == "__main__":
    test_example()
    test_overlap()
    test_edge_cases()
    test_lower_bound_family()
    test_exhaustive_small()
    test_random()
    print("ok")
