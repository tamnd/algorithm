# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bird-baker/. The authors are listed in prov/WZE4CC.jsonl.
import random

import pytest

from bird_baker import bird_baker


def naive(text, patterns):
    n1 = len(text)
    n2 = len(text[0]) if n1 else 0
    out = []
    for j, p in enumerate(patterns):
        m1 = len(p)
        m2 = len(p[0]) if m1 else 0
        for r in range(n1 - m1 + 1):
            for c in range(n2 - m2 + 1):
                if all(text[r + i][c:c + m2] == p[i] for i in range(m1)):
                    out.append((r, c, j))
    return sorted(out)


def test_example() -> None:
    text = ["ababa", "babab", "ababa", "bbaab"]
    patterns = [["ab", "ba"], ["ba", "ab", "ba"]]
    labels: list[list[int]] = []
    got = bird_baker(text, patterns, labels)
    assert got == [(0, 0, 0), (0, 1, 1), (0, 2, 0), (0, 3, 1), (1, 1, 0), (1, 3, 0)]
    # Row ids: ab = 0, ba = 1; -1 means that no pattern row ends there.
    assert labels == [[-1, 0, 1, 0, 1], [-1, 1, 0, 1, 0], [-1, 0, 1, 0, 1], [-1, -1, 1, -1, 0]]


def test_empty_and_degenerate() -> None:
    assert bird_baker([], []) == []
    assert bird_baker([], [[]]) == [(0, 0, 0)]
    assert bird_baker(["ab"], [[]]) == [(0, 0, 0), (0, 1, 0), (0, 2, 0), (1, 0, 0), (1, 1, 0), (1, 2, 0)]
    # One row of width 0: every row start, every column 0..n2.
    assert bird_baker(["ab", "ba"], [[""]]) == naive(["ab", "ba"], [[""]])
    assert bird_baker(["ab"], [["abc"]]) == []
    assert bird_baker(["ab"], [["a"], ["a"]]) == [(0, 0, 0), (0, 0, 1)]
    with pytest.raises(ValueError):
        bird_baker(["ab", "a"], [["a"]])
    with pytest.raises(ValueError):
        bird_baker(["ab"], [["ab", "a"]])


def test_tuples_as_symbols() -> None:
    text = [(1, 2, 1, 2), (2, 1, 2, 1)]
    assert bird_baker(text, [[(1, 2), (2, 1)]]) == [(0, 0, 0), (0, 2, 0)]


def test_periodic_text() -> None:
    text = ["ab" * 6] * 7
    patterns = [["ab", "ab"], ["ba"] * 3, ["aba"], ["a"], ["abab"] * 7]
    assert bird_baker(text, patterns) == naive(text, patterns)


def random_grid(rng: random.Random, alphabet: str, rows: int, cols: int) -> list[str]:
    return ["".join(rng.choice(alphabet) for _ in range(cols)) for _ in range(rows)]


def test_random_against_naive() -> None:
    rng = random.Random(20261106)
    cases = 0
    for alphabet in ("a", "ab", "abcd"):
        for _ in range(400):
            n1 = rng.randint(0, 7)
            n2 = rng.randint(1, 8) if n1 else 0
            text = random_grid(rng, alphabet, n1, n2)
            if rng.random() < 0.25 and n1:
                tile = random_grid(rng, alphabet, rng.randint(1, 2), rng.randint(1, 2))
                text = [(tile[i % len(tile)] * n2)[:n2] for i in range(n1)]
            patterns = []
            for _ in range(rng.randint(0, 5)):
                kind = rng.random()
                if kind < 0.4 and n1 and n2:
                    # A sub-rectangle of the text.
                    r = rng.randrange(n1)
                    c = rng.randrange(n2)
                    h = rng.randint(1, n1 - r)
                    w = rng.randint(1, n2 - c)
                    patterns.append([row[c:c + w] for row in text[r:r + h]])
                elif kind < 0.6 and patterns and patterns[-1] and patterns[-1][0]:
                    # Top or bottom part of the previous pattern, or a copy of it.
                    prev = patterns[-1]
                    cut = rng.randint(1, len(prev))
                    patterns.append(list(prev[:cut]) if rng.random() < 0.5 else list(prev[-cut:]))
                elif kind < 0.65:
                    patterns.append([] if rng.random() < 0.5 else [""] * rng.randint(1, 3))
                else:
                    patterns.append(random_grid(rng, alphabet, rng.randint(1, 3), rng.randint(1, 3)))
            assert bird_baker(text, patterns) == naive(text, patterns), (text, patterns)
            cases += 1
    assert cases >= 1200
