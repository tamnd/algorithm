# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/balanced-incomplete-block-design/. The authors are listed in prov/JG5X5V.jsonl.

import random
from fractions import Fraction
from itertools import combinations

import pytest

from balanced_incomplete_block_design import (
    develop, efficiency_factor, fano, intrablock_estimates, kirkman_15, parameters,
)


def determinant(m: list[list[Fraction]]) -> Fraction:
    m = [row[:] for row in m]
    n, det = len(m), Fraction(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if m[r][c] != 0), None)
        if piv is None:
            return Fraction(0)
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            det = -det
        det *= m[c][c]
        for r in range(c + 1, n):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * z for x, z in zip(m[r], m[c])]
    return det


def check_identities(v: int, blocks) -> None:
    v, b, r, k, lam = parameters(v, blocks)
    assert b * k == v * r and lam * (v - 1) == r * (k - 1) and b >= v
    inc = [[Fraction(int(t in blk)) for blk in blocks] for t in range(v)]
    nnt = [[sum(a * c for a, c in zip(inc[i], inc[j])) for j in range(v)] for i in range(v)]
    assert all(nnt[i][j] == (r if i == j else lam) for i in range(v) for j in range(v))
    assert determinant(nnt) == (r - lam) ** (v - 1) * (r + (v - 1) * lam) != 0


def test_fano_plane() -> None:
    blocks = fano()
    assert blocks[:3] == [[0, 1, 3], [1, 2, 4], [2, 3, 5]]
    assert parameters(7, blocks) == (7, 7, 3, 3, 1)
    check_identities(7, blocks)
    # any two lines meet in exactly one point (a symmetric design)
    assert all(len(set(a) & set(b)) == 1 for a, b in combinations(blocks, 2))


def test_kirkman_schoolgirls() -> None:
    days = kirkman_15()
    assert len(days) == 7 and all(len(d) == 5 for d in days)
    for day in days:
        assert sorted(p for blk in day for p in blk) == list(range(15))  # each girl once a day
    blocks = [blk for day in days for blk in day]
    assert parameters(15, blocks) == (15, 35, 7, 3, 1)
    check_identities(15, blocks)


def test_other_designs() -> None:
    check_identities(4, [list(c) for c in combinations(range(4), 3)])          # (4, 4, 3, 3, 2)
    check_identities(6, [list(c) for c in combinations(range(6), 2)])          # (6, 15, 5, 2, 1)
    check_identities(13, develop([[0, 1, 3, 9]], 13))                          # projective plane of order 3
    check_identities(11, develop([[1, 3, 4, 5, 9]], 11))                       # quadratic residues mod 11
    assert parameters(9, [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8],
                          [0, 4, 8], [1, 5, 6], [2, 3, 7], [0, 5, 7], [1, 3, 8], [2, 4, 6]]) == (9, 12, 4, 3, 1)


def test_not_a_bibd() -> None:
    with pytest.raises(ValueError):
        parameters(7, develop([[0, 1, 2]], 7))  # differences 1, 1, 2: pairs at distance 3 never meet
    with pytest.raises(ValueError):
        parameters(4, [[0, 1], [2, 3]])


def least_squares_effects(v, blocks, y) -> list[Fraction]:
    """Treatment effects (sum zero) of the model y = mu + tau_t + beta_block + e, solved exactly."""
    obs = [(t, j, Fraction(val)) for j, (blk, ys) in enumerate(zip(blocks, y)) for t, val in zip(blk, ys)]
    b = len(blocks)
    cols = [[Fraction(1)] * len(obs)]
    cols += [[Fraction((t == i) - (t == v - 1)) for t, _, _ in obs] for i in range(v - 1)]
    cols += [[Fraction((j == i) - (j == b - 1)) for _, j, _ in obs] for i in range(b - 1)]
    k = len(cols)
    m = [[sum(a * c for a, c in zip(cols[i], cols[jj])) for jj in range(k)]
         + [sum(a * o[2] for a, o in zip(cols[i], obs))] for i in range(k)]
    for c in range(k):
        piv = next(r for r in range(c, k) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        for r in range(k):
            if r != c and m[r][c] != 0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * z for x, z in zip(m[r], m[c])]
    beta = [m[i][k] / m[i][i] for i in range(k)]
    tau = beta[1:v]
    return tau + [-sum(tau)]


def test_intrablock_estimates_are_least_squares() -> None:
    rng = random.Random(1)
    for v, blocks in ((7, fano()), (4, [list(c) for c in combinations(range(4), 3)])):
        y = [[rng.randint(0, 30) for _ in blk] for blk in blocks]
        got = intrablock_estimates(v, blocks, y)
        exact = least_squares_effects(v, blocks, y)
        assert all(abs(g - float(e)) < 1e-9 for g, e in zip(got, exact))


def test_example() -> None:
    blocks = [list(c) for c in combinations(range(4), 3)]
    y = [[71, 76, 70], [70, 77, 72], [75, 73, 70], [80, 77, 73]]
    v, b, r, k, lam = parameters(4, blocks)
    assert (v, b, r, k, lam) == (4, 4, 3, 3, 2)
    values = [Fraction(x) for ys in y for x in ys]
    grand = sum(values) / len(values)
    sst = sum((x - grand) ** 2 for x in values)
    ss_blocks = k * sum((Fraction(sum(ys), k) - grand) ** 2 for ys in y)
    totals = [sum(x for blk, ys in zip(blocks, y) for t, x in zip(blk, ys) if t == i) for i in range(v)]
    q = [totals[i] - sum(Fraction(sum(ys), k) for blk, ys in zip(blocks, y) if i in blk) for i in range(v)]
    ss_treat_adj = k * sum(qi * qi for qi in q) / (lam * v)
    sse = sst - ss_blocks - ss_treat_adj
    assert totals == [216, 233, 220, 215] and q == [-2, 11, Fraction(-5, 3), Fraction(-22, 3)]
    assert (sst, ss_blocks, ss_treat_adj, sse) == (Fraction(362, 3), Fraction(110, 3), Fraction(817, 12), Fraction(191, 12))
    assert (ss_treat_adj / 3) / (sse / 5) == Fraction(4085, 573)
    tau = [Fraction(-3, 4), Fraction(33, 8), Fraction(-5, 8), Fraction(-11, 4)]
    assert all(abs(g - float(e)) < 1e-12 for g, e in zip(intrablock_estimates(v, blocks, y), tau))
    assert least_squares_effects(v, blocks, y) == tau
    # the one-way analysis that ignores the blocks
    ss_treat_unadj = sum(r * (Fraction(t, r) - grand) ** 2 for t in totals)
    assert ss_treat_unadj == Fraction(206, 3)
    assert (ss_treat_unadj / 3) / ((sst - ss_treat_unadj) / 8) == Fraction(206, 9) / Fraction(13, 2)


def test_efficiency() -> None:
    assert efficiency_factor(7, 3, 1, 3) == 7 / 9
    assert abs(efficiency_factor(15, 3, 1, 7) - 5 / 7) < 1e-15
