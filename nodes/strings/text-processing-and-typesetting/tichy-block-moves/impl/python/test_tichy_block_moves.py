# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tichy-block-moves/. The authors are listed in prov/ZJTFAN.jsonl.

import itertools
import random

from tichy_block_moves import apply_moves, block_moves, block_moves_linear


def fewest_moves(s, t):
    """The least number of copies and adds that build t, by a dynamic program over the positions of t."""
    subs = {tuple(s[i:j]) for i in range(len(s)) for j in range(i + 1, len(s) + 1)}
    best = [0] * (len(t) + 1)
    for q in range(len(t) - 1, -1, -1):
        best[q] = 1 + best[q + 1]
        for r in range(q + 1, len(t) + 1):
            if tuple(t[q:r]) in subs:
                best[q] = min(best[q], 1 + best[r])
    return best[0]


def test_page_example() -> None:
    s, t = "abcde", "cdeabxe"
    moves = block_moves(s, t)
    assert moves == [("copy", 2, 3), ("copy", 0, 2), ("add", "x"), ("copy", 4, 1)]
    assert "".join(apply_moves(s, moves)) == t
    assert block_moves_linear(s, t) == moves


def test_copies_may_repeat_and_overlap() -> None:
    assert block_moves("ab", "ababab") == [("copy", 0, 2)] * 3
    assert block_moves("aaa", "aaaaa") == [("copy", 0, 3), ("copy", 0, 2)]
    assert block_moves("", "xy") == [("add", "x"), ("add", "y")]
    assert block_moves("abc", "") == []


def test_greedy_is_optimal_on_all_small_inputs() -> None:
    words = [w for n in range(8) for w in itertools.product("ab", repeat=n)]
    for s in words:
        for t in words:
            moves = block_moves(s, t)
            assert tuple(apply_moves(s, moves)) == t
            assert len(moves) == fewest_moves(s, t)


def test_random_inputs() -> None:
    rng = random.Random(17)
    for _ in range(300):
        alpha = "abcdxyz"[: rng.randint(1, 7)]
        s = [rng.choice(alpha[:4]) for _ in range(rng.randint(0, 15))]
        t = [rng.choice(alpha) for _ in range(rng.randint(0, 15))]
        moves = block_moves(s, t)
        assert apply_moves(s, moves) == t
        assert block_moves_linear(s, t) == moves
        assert len(moves) == fewest_moves(s, t)
        # An add is used only for a symbol that does not occur in s.
        assert all(m[1] not in s for m in moves if m[0] == "add")
