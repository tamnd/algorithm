# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/backward-dawg-matching/. The authors are listed in prov/YJ949P.jsonl.

import itertools
import random

from backward_dawg_matching import backward_dawg_matching, suffix_automaton


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def accepts(trans: list[dict], terminal: list[bool], w: str) -> tuple[bool, bool]:
    q = 0
    for c in w:
        if c not in trans[q]:
            return False, False
        q = trans[q][c]
    return True, terminal[q]


def test_automaton_against_definition() -> None:
    for m in range(0, 7):
        for p in itertools.product("ab", repeat=m):
            w = "".join(p)
            trans, terminal = suffix_automaton(w)
            assert len(trans) <= max(m + 1, 2 * m - 1)
            for k in range(0, m + 2):
                for x in itertools.product("ab", repeat=k):
                    xs = "".join(x)
                    assert accepts(trans, terminal, xs) == (xs in w, w.endswith(xs))


def test_example() -> None:
    stats: dict = {}
    assert backward_dawg_matching("gcatcgcagagagtatacagtacg", "gcagagag", stats) == [5]
    assert stats["inspections"] == 16


def test_edges() -> None:
    assert backward_dawg_matching("abc", "") == [0, 1, 2, 3]
    assert backward_dawg_matching("", "") == [0]
    assert backward_dawg_matching("", "a") == []
    assert backward_dawg_matching("ab", "abc") == []
    assert backward_dawg_matching("a" * 10, "a" * 4) == list(range(7))
    assert backward_dawg_matching("a" * 10, "baaa") == []


def test_skips_on_absent_characters() -> None:
    stats: dict = {}
    assert backward_dawg_matching("x" * 1000, "abcdefghij", stats) == []
    assert stats["inspections"] == 100


def test_random_against_oracle() -> None:
    rng = random.Random(1994)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert backward_dawg_matching(t, p) == oracle(t, p)
