# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turbo-boyer-moore/. The authors are listed in prov/05ED1E.jsonl.

import itertools
import random

from turbo_boyer_moore import turbo_boyer_moore


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def test_example() -> None:
    stats: dict = {}
    assert turbo_boyer_moore("gcatcgcagagagtatacagtacg", "gcagagag", stats) == [5]
    assert stats["comparisons"] == 15


def test_edges() -> None:
    assert turbo_boyer_moore("abc", "") == [0, 1, 2, 3]
    assert turbo_boyer_moore("", "") == [0]
    assert turbo_boyer_moore("", "a") == []
    assert turbo_boyer_moore("ab", "abc") == []
    assert turbo_boyer_moore("a" * 10, "a" * 4) == list(range(7))
    assert turbo_boyer_moore("a" * 10, "baaa") == []


def test_periodic_input_is_linear() -> None:
    stats: dict = {}
    assert turbo_boyer_moore("a" * 1000, "a" * 10, stats) == list(range(991))
    assert stats["comparisons"] <= 2 * 1000


def test_exhaustive_binary() -> None:
    for m in range(1, 5):
        for p in itertools.product("ab", repeat=m):
            ps = "".join(p)
            for n in range(0, 9):
                for t in itertools.product("ab", repeat=n):
                    ts = "".join(t)
                    stats: dict = {}
                    assert turbo_boyer_moore(ts, ps, stats) == oracle(ts, ps)
                    assert stats["comparisons"] <= 2 * n


def test_random_against_oracle() -> None:
    rng = random.Random(1994)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            stats: dict = {}
            assert turbo_boyer_moore(t, p, stats) == oracle(t, p)
            assert stats["comparisons"] <= 2 * len(t)
