# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gotoh-algorithm/. The authors are listed in prov/GKC398.jsonl.

import random

import pytest

from gotoh_algorithm import NEG, affine_score, gotoh_algorithm


def dna(match: int, mismatch: int):
    return lambda a, b: match if a == b else mismatch


def all_alignments(x: str, y: str):
    """Yield every global alignment of x and y as a pair of rows (explicit stack)."""
    stack = [(0, 0, "", "")]
    while stack:
        i, j, r1, r2 = stack.pop()
        if i == len(x) and j == len(y):
            yield r1, r2
            continue
        if i < len(x) and j < len(y):
            stack.append((i + 1, j + 1, r1 + x[i], r2 + y[j]))
        if i < len(x):
            stack.append((i + 1, j, r1 + x[i], r2 + "-"))
        if j < len(y):
            stack.append((i, j + 1, r1 + "-", r2 + y[j]))


def brute(x, y, s, d, e):
    return max(affine_score(r1, r2, s, d, e) for r1, r2 in all_alignments(x, y))


def check_rows(x, y, r1, r2):
    assert len(r1) == len(r2)
    assert r1.replace("-", "") == x and r2.replace("-", "") == y
    assert all(not (a == "-" and b == "-") for a, b in zip(r1, r2))


def test_page_example():
    s = dna(2, -1)
    score, r1, r2 = gotoh_algorithm("ACGTTA", "ACTA", s, 3, 1)
    assert score == 4
    assert affine_score(r1, r2, s, 3, 1) == 4
    check_rows("ACGTTA", "ACTA", r1, r2)


def test_edges():
    s = dna(1, -1)
    assert gotoh_algorithm("", "", s, 3, 1) == (0, "", "")
    assert gotoh_algorithm("ACG", "", s, 3, 1) == (-5, "ACG", "---")
    assert gotoh_algorithm("", "AC", s, 3, 1) == (-4, "--", "AC")
    assert gotoh_algorithm("A", "A", s, 3, 1) == (1, "A", "A")
    with pytest.raises(ValueError):
        gotoh_algorithm("A", "C", s, 1, 2)


def test_against_brute_force():
    rng = random.Random(7)
    for _ in range(250):
        m, n = rng.randint(0, 5), rng.randint(0, 5)
        x = "".join(rng.choice("ACGT") for _ in range(m))
        y = "".join(rng.choice("ACGT") for _ in range(n))
        e = rng.randint(0, 3)
        d = e + rng.randint(0, 4)
        s = dna(rng.randint(1, 3), -rng.randint(0, 3))
        score, r1, r2 = gotoh_algorithm(x, y, s, d, e)
        check_rows(x, y, r1, r2)
        assert affine_score(r1, r2, s, d, e) == score
        assert score == brute(x, y, s, d, e)


def test_linear_case_is_edit_distance():
    # With d = e = 1, match 0 and mismatch -1, the score is minus the Levenshtein distance.
    s = dna(0, -1)
    assert gotoh_algorithm("kitten", "sitting", s, 1, 1)[0] == -3
    assert gotoh_algorithm("GATTACA", "GCATGCU", s, 1, 1)[0] == -4


def wrong_border(x, y, s, d, e):
    """Fill the tables with X[0][j] = H[0][j] and Y[i][0] = H[i][0] at the borders.

    This is the boundary mistake that Flouri et al. (2015) report: a gap in one row
    and a gap in the other row then share one opening charge.
    """
    m, n = len(x), len(y)
    M = [[NEG] * (n + 1) for _ in range(m + 1)]
    X = [[NEG] * (n + 1) for _ in range(m + 1)]
    Y = [[NEG] * (n + 1) for _ in range(m + 1)]
    H = [[NEG] * (n + 1) for _ in range(m + 1)]
    M[0][0] = H[0][0] = 0
    for i in range(1, m + 1):
        H[i][0] = X[i][0] = Y[i][0] = -(d + (i - 1) * e)
    for j in range(1, n + 1):
        H[0][j] = Y[0][j] = X[0][j] = -(d + (j - 1) * e)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            M[i][j] = H[i - 1][j - 1] + s(x[i - 1], y[j - 1])
            X[i][j] = max(H[i - 1][j] - d, X[i - 1][j] - e)
            Y[i][j] = max(H[i][j - 1] - d, Y[i][j - 1] - e)
            H[i][j] = max(M[i][j], X[i][j], Y[i][j])
    return H[m][n]


def test_border_mistake():
    # Flouri et al.: mismatch cost 5, gap open 2 and extension 1 in the o + L e form,
    # that is d = 3 and e = 1 here.
    s = dna(0, -5)
    assert gotoh_algorithm("A", "C", s, 3, 1)[0] == -5
    assert brute("A", "C", s, 3, 1) == -5
    assert wrong_border("A", "C", s, 3, 1) == -4


def test_traceback_keeps_state():
    rng = random.Random(11)
    for _ in range(200):
        x = "".join(rng.choice("AC") for _ in range(rng.randint(1, 7)))
        y = "".join(rng.choice("AC") for _ in range(rng.randint(1, 7)))
        s = dna(1, -2)
        score, r1, r2 = gotoh_algorithm(x, y, s, 4, 1)
        assert affine_score(r1, r2, s, 4, 1) == score
