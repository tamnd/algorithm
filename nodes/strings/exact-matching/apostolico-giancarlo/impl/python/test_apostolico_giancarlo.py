# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/apostolico-giancarlo/. The authors are listed in prov/7XHZHF.jsonl.

import itertools
import random

from apostolico_giancarlo import apostolico_giancarlo, good_suffix, suffixes


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def test_example() -> None:
    stats: dict = {}
    assert apostolico_giancarlo("gcatcgcagagagtatacagtacg", "gcagagag", stats) == [5]
    assert stats["comparisons"] == 15


def test_tables() -> None:
    p = "gcagagag"
    suff = suffixes(p)
    assert suff == [1, 0, 0, 2, 0, 4, 0, 8]
    assert good_suffix(p, suff) == [7, 7, 7, 2, 7, 4, 7, 1]


def test_edges() -> None:
    assert apostolico_giancarlo("abc", "") == [0, 1, 2, 3]
    assert apostolico_giancarlo("", "") == [0]
    assert apostolico_giancarlo("", "a") == []
    assert apostolico_giancarlo("ab", "abc") == []
    assert apostolico_giancarlo("a" * 10, "a" * 4) == list(range(7))
    assert apostolico_giancarlo("a" * 10, "baaa") == []


def test_periodic_input_is_linear() -> None:
    stats: dict = {}
    assert apostolico_giancarlo("a" * 1000, "a" * 10, stats) == list(range(991))
    assert stats["comparisons"] <= 1000


def test_exhaustive_binary() -> None:
    for m in range(1, 5):
        for p in itertools.product("ab", repeat=m):
            ps = "".join(p)
            for n in range(0, 9):
                for t in itertools.product("ab", repeat=n):
                    ts = "".join(t)
                    stats: dict = {}
                    assert apostolico_giancarlo(ts, ps, stats) == oracle(ts, ps)
                    assert 2 * stats["comparisons"] <= 3 * n


def test_random_against_oracle() -> None:
    rng = random.Random(1986)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            stats: dict = {}
            assert apostolico_giancarlo(t, p, stats) == oracle(t, p)
            assert 2 * stats["comparisons"] <= 3 * len(t)
