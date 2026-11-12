# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hirschberg-algorithm/. The authors are listed in prov/WVTXEZ.jsonl.

import random
from typing import Iterator

from hirschberg_algorithm import GAP, hirschberg_algorithm, match_mismatch, nw_last_row

TOY = match_mismatch(2, -1)


def all_alignments(x: str, y: str) -> Iterator[tuple[str, str]]:
    """Every global alignment of x and y, as (top, bottom) rows."""
    if not x and not y:
        yield "", ""
        return
    if x and y:
        for t, b in all_alignments(x[1:], y[1:]):
            yield x[0] + t, y[0] + b
    if x:
        for t, b in all_alignments(x[1:], y):
            yield x[0] + t, GAP + b
    if y:
        for t, b in all_alignments(x, y[1:]):
            yield GAP + t, y[0] + b


def score_of(top: str, bottom: str, s, d: int) -> int:
    return sum(-d if a == GAP or b == GAP else s(a, b) for a, b in zip(top, bottom))


def full_nw(x: str, y: str, s, d: int) -> int:
    """The full quadratic-space table, used as the reference for longer strings."""
    f = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(len(x) + 1):
        for j in range(len(y) + 1):
            if i == 0 or j == 0:
                f[i][j] = -(i + j) * d
            else:
                f[i][j] = max(f[i - 1][j - 1] + s(x[i - 1], y[j - 1]), f[i - 1][j] - d, f[i][j - 1] - d)
    return f[len(x)][len(y)]


def check(x: str, y: str, s, d: int, result: tuple[int, str, str]) -> None:
    score, top, bottom = result
    assert len(top) == len(bottom)
    assert top.replace(GAP, "") == x
    assert bottom.replace(GAP, "") == y
    assert all(not (a == GAP and b == GAP) for a, b in zip(top, bottom))
    assert score_of(top, bottom, s, d) == score


def test_worked_example() -> None:
    stats: dict = {}
    result = hirschberg_algorithm("AGTACGCA", "TATGC", TOY, 2, stats)
    assert result == (1, "AGTACGCA", "--TATGC-")
    assert stats["cells"] == 75
    # The same strings in the other order give the mirrored alignment.
    assert hirschberg_algorithm("TATGC", "AGTACGCA", TOY, 2) == (1, "--TATGC-", "AGTACGCA")


def test_last_rows() -> None:
    x, y = "AGTACGCA", "TATGC"
    assert nw_last_row(x, 0, 4, y, 0, 5, TOY, 2, False) == [-8, -4, 0, -2, -1, -3]
    assert nw_last_row(x, 4, 8, y, 0, 5, TOY, 2, True) == [-8, -4, 0, 1, -1, -3]


def test_edges() -> None:
    assert hirschberg_algorithm("", "", TOY, 2) == (0, "", "")
    assert hirschberg_algorithm("ACG", "", TOY, 2) == (-6, "ACG", "---")
    assert hirschberg_algorithm("", "AC", TOY, 2) == (-4, "--", "AC")
    assert hirschberg_algorithm("A", "C", TOY, 2) == (-1, "A", "C")
    assert hirschberg_algorithm("A", "C", match_mismatch(2, -5), 2)[0] == -4
    assert hirschberg_algorithm("A", "GGAGG", TOY, 2) == (-6, "--A--", "GGAGG")


def test_against_brute_force() -> None:
    rng = random.Random(1975)
    for _ in range(500):
        x = "".join(rng.choice("ACGT") for _ in range(rng.randrange(6)))
        y = "".join(rng.choice("ACGT") for _ in range(rng.randrange(6)))
        s = match_mismatch(rng.randrange(0, 4), rng.randrange(-4, 1))
        d = rng.randrange(0, 5)
        result = hirschberg_algorithm(x, y, s, d)
        assert result[0] == max(score_of(t, b, s, d) for t, b in all_alignments(x, y))
        check(x, y, s, d, result)


def test_asymmetric_matrix_and_long_strings() -> None:
    rng = random.Random(360825)
    alphabet = "ACDE"
    for _ in range(150):
        table = {(a, b): rng.randrange(-5, 6) for a in alphabet for b in alphabet}
        s = lambda a, b, t=table: t[a, b]
        x = "".join(rng.choice(alphabet) for _ in range(rng.randrange(40)))
        y = "".join(rng.choice(alphabet) for _ in range(rng.randrange(40)))
        d = rng.randrange(0, 6)
        stats: dict = {}
        result = hirschberg_algorithm(x, y, s, d, stats)
        assert result[0] == full_nw(x, y, s, d)
        check(x, y, s, d, result)
        m, n = max(len(x), len(y)), min(len(x), len(y))
        lg = (m - 1).bit_length() if m else 0
        assert stats["cells"] <= n * (2 * m + lg - 1) if m else stats["cells"] == 0
