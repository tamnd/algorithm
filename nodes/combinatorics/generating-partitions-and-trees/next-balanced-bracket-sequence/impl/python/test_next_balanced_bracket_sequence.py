# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/next-balanced-bracket-sequence/. The authors are listed in prov/BRK0H7.jsonl.

import itertools
import math
import random

from next_balanced_bracket_sequence import balanced_sequences, next_balanced


def is_balanced(w: str) -> bool:
    h = 0
    for c in w:
        h += 1 if c == "(" else -1
        if h < 0:
            return False
    return h == 0


def brute_force(n: int) -> list[str]:
    words = ("".join(t) for t in itertools.product("()", repeat=2 * n))
    return sorted(w for w in words if is_balanced(w))


def catalan(n: int) -> int:
    return math.comb(2 * n, n) // (n + 1)


def test_example() -> None:
    s = list("(()(()))()")
    assert next_balanced(s)
    assert "".join(s) == "(()()(()))"


def test_edges() -> None:
    s: list[str] = []
    assert not next_balanced(s) and s == []
    assert list(balanced_sequences(0)) == [""]
    s = list("()")
    assert not next_balanced(s) and s == list("()")
    s = list("()()()")
    assert not next_balanced(s) and "".join(s) == "()()()"
    s = list("(())")
    assert next_balanced(s) and "".join(s) == "()()"


def test_full_lists_match_brute_force() -> None:
    for n in range(0, 9):
        got = list(balanced_sequences(n))
        assert got == brute_force(n)
        assert len(got) == catalan(n)


def test_counts_for_larger_n() -> None:
    for n in range(9, 12):
        count = 0
        prev = ""
        for w in balanced_sequences(n):
            assert w > prev
            prev = w
            count += 1
        assert count == catalan(n)


def test_random_words_against_sorted_list() -> None:
    rng = random.Random(1)
    tables = {n: brute_force(n) for n in range(1, 8)}
    for _ in range(600):
        n = rng.randint(1, 7)
        words = tables[n]
        k = rng.randrange(len(words))
        s = list(words[k])
        ok = next_balanced(s)
        if k + 1 < len(words):
            assert ok and "".join(s) == words[k + 1]
        else:
            assert not ok and "".join(s) == words[k]
