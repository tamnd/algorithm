# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-bracket-sequence-ranking/. The authors are listed in prov/6BDKZQ.jsonl.

import itertools
import math
import random

import pytest

from balanced_bracket_sequence_ranking import completion_table, rank_balanced


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
    assert rank_balanced("()(())()") == 11
    assert rank_balanced("(()(()))()") == 17


def test_table_values() -> None:
    d = completion_table(8)
    assert d[8][:9] == [14, 0, 28, 0, 20, 0, 7, 0, 1]
    assert d[6][:7] == [5, 0, 9, 0, 5, 0, 1]
    for i in range(0, 9):
        for j in range(0, 9):
            if (i - j) % 2 == 0 and j <= i:
                u = (i - j) // 2
                want = math.comb(i, u) - (math.comb(i, u - 1) if u >= 1 else 0)
            else:
                want = 0
            assert d[i][j] == want


def test_edges() -> None:
    assert rank_balanced("") == 0
    assert rank_balanced("()") == 0
    for n in range(1, 30):
        assert rank_balanced("(" * n + ")" * n) == 0
        assert rank_balanced("()" * n) == catalan(n) - 1
    for bad in [")(", "(()", "())(", "(a)"]:
        with pytest.raises(ValueError):
            rank_balanced(bad)


def test_full_lists() -> None:
    for n in range(0, 9):
        words = brute_force(n)
        d = completion_table(2 * n)
        assert [rank_balanced(w, d) for w in words] == list(range(len(words)))
        assert len(words) == catalan(n)


def test_random_pairs_keep_the_order() -> None:
    rng = random.Random(2)
    for _ in range(600):
        n = rng.randint(1, 14)
        words = []
        for _ in range(2):
            h, w, opens = 0, [], 0
            for _ in range(2 * n):
                can_open = opens < n
                can_close = h > 0
                if can_open and (not can_close or rng.random() < 0.5):
                    w.append("(")
                    h += 1
                    opens += 1
                else:
                    w.append(")")
                    h -= 1
            assert is_balanced("".join(w))
            words.append("".join(w))
        a, b = words
        ra, rb = rank_balanced(a), rank_balanced(b)
        assert 0 <= ra < catalan(n) and 0 <= rb < catalan(n)
        assert (a < b) == (ra < rb) and (a == b) == (ra == rb)
