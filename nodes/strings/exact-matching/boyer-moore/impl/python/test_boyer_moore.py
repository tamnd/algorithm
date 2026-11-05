# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boyer-moore/. The authors are listed in prov/GBSH7D.jsonl.

import random

from boyer_moore import boyer_moore, good_suffix, last_occurrence, suffixes


def oracle(t: str, p: str) -> list[int]:
    return [s for s in range(len(t) - len(p) + 1) if t.startswith(p, s)]


def gs_oracle(p: str) -> list[int]:
    m, out = len(p), []
    for j in range(m):
        d = 1
        while not (
            all(p[i - d] == p[i] for i in range(max(j + 1, d), m)) and (j - d < 0 or p[j - d] != p[j])
        ):
            d += 1
        out.append(d)
    return out


def period(p: str) -> int:
    return next(d for d in range(1, len(p) + 1) if all(p[i - d] == p[i] for i in range(d, len(p))))


def test_example() -> None:
    p = "gcagagag"
    assert suffixes(p) == [1, 0, 0, 2, 0, 4, 0, 8]
    assert good_suffix(p) == [7, 7, 7, 2, 7, 4, 7, 1]
    assert last_occurrence(p) == {"g": 7, "c": 1, "a": 6}
    assert boyer_moore("gcatcgcagagagtatacagtacg", p) == [5]


def test_edges() -> None:
    assert boyer_moore("abc", "") == [0, 1, 2, 3]
    assert boyer_moore("", "") == [0]
    assert boyer_moore("", "a") == []
    assert boyer_moore("ab", "abc") == []
    assert boyer_moore("a" * 10, "a" * 4) == list(range(7))
    assert boyer_moore("a" * 10, "baaa") == []


def test_tables_against_definition() -> None:
    rng = random.Random(77)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(400):
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(1, 10)))
            gs = good_suffix(p)
            assert gs == gs_oracle(p)
            assert gs[0] == period(p)


def test_random_against_oracle() -> None:
    rng = random.Random(1977)
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(700):
            t = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 40)))
            p = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 7)))
            assert boyer_moore(t, p) == oracle(t, p)
