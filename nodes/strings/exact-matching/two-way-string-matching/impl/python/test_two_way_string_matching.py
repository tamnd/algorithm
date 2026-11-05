# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/two-way-string-matching/. The authors are listed in prov/5X5RDM.jsonl.

import itertools
import random

from two_way_string_matching import critical_factorization, two_way_string_matching


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def period(w: str) -> int:
    return next(d for d in range(1, len(w) + 1) if all(w[i] == w[i + d] for i in range(len(w) - d)))


def local_period(w: str, cut: int) -> int:
    for r in range(1, len(w) + 1):
        if all(w[i] == w[i + r] for i in range(max(0, cut - r), cut) if i + r < len(w)):
            return r
    return len(w)


def test_critical_factorization() -> None:
    for m in range(1, 8):
        for p in itertools.product("abc", repeat=m):
            w = "".join(p)
            ell, per = critical_factorization(w)
            assert local_period(w, ell + 1) == period(w)
            assert ell + 1 < period(w)
            if w[: ell + 1] == w[per : per + ell + 1]:
                assert per == period(w)
            else:
                assert period(w) > max(ell + 1, m - ell - 1)


def test_example() -> None:
    assert critical_factorization("gcagagag") == (1, 2)
    stats: dict = {}
    assert two_way_string_matching("gcatcgcagagagtatacagtacg", "gcagagag", stats) == [5]
    assert stats["comparisons"] == 20
    stats = {}
    assert two_way_string_matching("abaabaabaabaab", "aabaab", stats) == [2, 5, 8]
    assert stats["comparisons"] == 14


def test_edges() -> None:
    assert two_way_string_matching("abc", "") == [0, 1, 2, 3]
    assert two_way_string_matching("", "") == [0]
    assert two_way_string_matching("", "a") == []
    assert two_way_string_matching("ab", "abc") == []
    assert two_way_string_matching("a" * 10, "a" * 4) == list(range(7))
    assert two_way_string_matching("a" * 10, "baaa") == []
    assert two_way_string_matching([3, 1, 3, 1, 3], [3, 1, 3]) == [0, 2]


def test_comparison_bound() -> None:
    for m in range(1, 6):
        for p in itertools.product("ab", repeat=m):
            ps = "".join(p)
            for n in range(m, 11):
                for t in itertools.product("ab", repeat=n):
                    ts = "".join(t)
                    stats: dict = {}
                    assert two_way_string_matching(ts, ps, stats) == oracle(ts, ps)
                    assert stats["comparisons"] <= 2 * n - m


def test_random_against_oracle() -> None:
    rng = random.Random(1991)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert two_way_string_matching(t, p) == oracle(t, p)
