# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kth-balanced-bracket-sequence/. The authors are listed in prov/4XTB6R.jsonl.

import itertools
import math
import random

import pytest

from kth_balanced_bracket_sequence import completion_table, kth_balanced


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


def rank(w: str) -> int:
    """Independent rank: count the smaller words through the closed form."""
    m = len(w)
    h = 0
    r = 0
    for i, c in enumerate(w):
        if c == ")":
            rest, j = m - 1 - i, h + 1
            if (rest - j) % 2 == 0 and j <= rest:
                u = (rest - j) // 2
                r += math.comb(rest, u) - (math.comb(rest, u - 1) if u >= 1 else 0)
            h -= 1
        else:
            h += 1
    return r


def test_example() -> None:
    assert kth_balanced(4, 7) == "(())(())"
    assert kth_balanced(4, 11) == "()(())()"
    assert kth_balanced(5, 17) == "(()(()))()"


def test_edges() -> None:
    assert kth_balanced(0, 0) == ""
    assert kth_balanced(1, 0) == "()"
    for n in range(1, 30):
        assert kth_balanced(n, 0) == "(" * n + ")" * n
        assert kth_balanced(n, catalan(n) - 1) == "()" * n
    for n, k in [(0, 1), (3, 5), (3, -1), (4, 14)]:
        with pytest.raises(ValueError):
            kth_balanced(n, k)


def test_full_lists() -> None:
    for n in range(0, 9):
        words = brute_force(n)
        d = completion_table(2 * n)
        assert [kth_balanced(n, k, d) for k in range(len(words))] == words
        assert len(words) == catalan(n)


def test_random_large_ranks() -> None:
    rng = random.Random(3)
    for _ in range(600):
        n = rng.randint(1, 40)
        k = rng.randrange(catalan(n))
        w = kth_balanced(n, k)
        assert len(w) == 2 * n and is_balanced(w)
        assert rank(w) == k
