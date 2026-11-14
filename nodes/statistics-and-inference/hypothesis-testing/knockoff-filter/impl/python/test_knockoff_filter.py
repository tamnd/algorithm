# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/knockoff-filter/. The authors are listed in prov/WNY22A.jsonl.

import itertools
import math
import random
import statistics
from fractions import Fraction

import pytest

from knockoff_filter import (
    jacobi_eigen,
    knockoff_select,
    knockoff_threshold,
    knockoffs,
    marginal_statistic,
    ols_statistic,
)

HAND_W = [9, 8, 7.5, 7, 6, 5.5, -5, 4, 3, -2.5, 2, -1, 0.5, -0.3]


def design(rng: random.Random, n: int, p: int, rho: float = 0.5) -> list[list[float]]:
    """Rows share a common factor, so the columns are positively correlated."""
    rows = []
    for _ in range(n):
        z = rng.gauss(0, 1)
        rows.append([rho * z + rng.gauss(0, 1) for _ in range(p)])
    return rows


def gram(a: list, b: list) -> list[list[float]]:
    return [[sum(a[i][j] * b[i][k] for i in range(len(a))) for k in range(len(b[0]))] for j in range(len(a[0]))]


def threshold_brute_force(w: list, q, plus: bool):
    """Smallest admissible t > 0 by the definition: the counts are constant on each interval between |W| values,
    so test every |W_j|, every midpoint and a point below the smallest; return the selected set there."""
    mags = sorted({abs(x) for x in w if x != 0})
    if not mags:
        return [False] * len(w)
    candidates = sorted(set(mags) | {(a + b) / 2 for a, b in zip(mags, mags[1:])} | {mags[0] / 2})
    offset = 1 if plus else 0
    for t in candidates:
        if Fraction(offset + sum(1 for x in w if x <= -t)) / max(sum(1 for x in w if x >= t), 1) <= q:
            return [x >= t for x in w]
    return [False] * len(w)


def test_hand_example() -> None:
    # knockoff+ at q = 0.2: at t = 5.5 there are 6 positives and no negatives at or beyond -5.5, so (1 + 0)/6 <= 0.2,
    # and every smaller t fails, for example t = 5 gives (1 + 1)/6.
    assert knockoff_threshold(HAND_W, Fraction(1, 5)) == 5.5
    assert sum(knockoff_select(HAND_W, Fraction(1, 5))) == 6
    # The plain knockoff stops at t = 3: 8 positives, 1 negative (-5), 1/8 <= 0.2; t = 2.5 gives 2/8.
    assert knockoff_threshold(HAND_W, Fraction(1, 5), plus=False) == 3
    assert sum(knockoff_select(HAND_W, Fraction(1, 5), plus=False)) == 8
    # One null feature with a positive statistic: the plain filter selects it, knockoff+ cannot.
    assert knockoff_select([2.0], Fraction(1, 10), plus=False) == [True]
    assert knockoff_select([2.0], Fraction(1, 10)) == [False]
    assert knockoff_select([0, 0], Fraction(1, 2)) == [False, False]


def test_threshold_matches_definition() -> None:
    rng = random.Random(2015)
    for _ in range(2000):
        p = rng.randint(1, 12)
        w = [rng.choice([-1, 1]) * rng.randint(0, 8) for _ in range(p)]
        q = Fraction(rng.randint(1, 10), 10)
        for plus in (True, False):
            assert knockoff_select(w, q, plus) == threshold_brute_force(w, q, plus)


def test_jacobi_eigen() -> None:
    rng = random.Random(1846)
    for _ in range(30):
        n = rng.randint(1, 7)
        b = [[rng.uniform(-1, 1) for _ in range(n)] for _ in range(n)]
        a = [[b[i][j] + b[j][i] for j in range(n)] for i in range(n)]
        w, v = jacobi_eigen(a)
        for i in range(n):
            for j in range(n):
                assert sum(v[i][k] * w[k] * v[j][k] for k in range(n)) == pytest.approx(a[i][j], abs=1e-10)
                assert sum(v[k][i] * v[k][j] for k in range(n)) == pytest.approx(1.0 if i == j else 0.0, abs=1e-10)


def test_knockoff_gram_identities() -> None:
    rng = random.Random(7)
    for n, p in ((8, 3), (20, 6), (30, 10)):
        x = design(rng, n, p)
        xn, xk, s = knockoffs(x, rng=random.Random(1))
        sigma = gram(xn, xn)
        lam_min = min(jacobi_eigen(sigma)[0])
        assert s == pytest.approx(min(2 * lam_min, 1.0))
        kk, xkx = gram(xk, xk), gram(xn, xk)
        for i in range(p):
            assert sigma[i][i] == pytest.approx(1.0)
            for j in range(p):
                assert kk[i][j] == pytest.approx(sigma[i][j], abs=1e-9)
                assert xkx[i][j] == pytest.approx(sigma[i][j] - (s if i == j else 0.0), abs=1e-9)


def test_swap_leaves_gram_and_flips_statistics() -> None:
    """Swapping X_j and Xk_j for j in S keeps the Gram matrix of [X Xk] and flips the sign of W_j for j in S."""
    rng = random.Random(11)
    n, p = 24, 5
    x = design(rng, n, p)
    xn, xk, s = knockoffs(x, s=None)
    _, _, s_small = knockoffs(x)
    xn2, xk2, _ = knockoffs(x, s=0.9 * s_small)
    y = [rng.gauss(0, 1) for _ in range(n)]
    for subset in [(0,), (1, 3), (0, 2, 4)]:
        xs = [[xk[i][j] if j in subset else xn[i][j] for j in range(p)] for i in range(n)]
        xks = [[xn[i][j] if j in subset else xk[i][j] for j in range(p)] for i in range(n)]
        aug, aug_s = [a + b for a, b in zip(xn, xk)], [a + b for a, b in zip(xs, xks)]
        g, g_s = gram(aug, aug), gram(aug_s, aug_s)
        assert all(g[i][j] == pytest.approx(g_s[i][j], abs=1e-9) for i in range(2 * p) for j in range(2 * p))
        w, w_s = marginal_statistic(xn, xk)(y), marginal_statistic(xs, xks)(y)
        assert all(w_s[j] == pytest.approx(-w[j] if j in subset else w[j], abs=1e-9) for j in range(p))
        xs2 = [[xk2[i][j] if j in subset else xn2[i][j] for j in range(p)] for i in range(n)]
        xks2 = [[xn2[i][j] if j in subset else xk2[i][j] for j in range(p)] for i in range(n)]
        w, w_s = ols_statistic(xn2, xk2)(y), ols_statistic(xs2, xks2)(y)
        assert all(w_s[j] == pytest.approx(-w[j] if j in subset else w[j], abs=1e-7) for j in range(p))


def test_invalid_input() -> None:
    with pytest.raises(ValueError):
        knockoffs([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # n < 2p
    with pytest.raises(ValueError):
        knockoffs([[1.0, 2.0], [2.0, 4.0], [3.0, 6.0], [1.0, 2.0]])  # collinear columns
    rng = random.Random(3)
    x = design(rng, 10, 3)
    with pytest.raises(ValueError):
        ols_statistic(*knockoffs(x)[:2])  # s = 2 lambda_min makes [X Xk] singular, unless s was capped at 1
    assert knockoff_threshold([], Fraction(1, 10)) == math.inf


def test_exact_fdr_under_coin_flips() -> None:
    """Condition on |W| and the non-null signs; flip the null signs as fair coins, as the sign-flip lemma gives.
    Enumerating all 2^m0 patterns gives the exact FDR. knockoff+ stays <= q and the plain filter's
    E[V / (R + 1/q)] stays <= q (these are the two theorems of Barber and Candes); the plain filter's
    FDR can exceed q."""
    rng = random.Random(4)
    q = Fraction(1, 5)
    worst_plain = Fraction(0)
    for _ in range(150):
        p = rng.randint(1, 9)
        m0 = rng.randint(1, p)
        mags = [Fraction(rng.randint(1, 30)) for _ in range(p)]
        alt_signs = [rng.choice([1, 1, 1, -1]) for _ in range(p - m0)]
        fdr_plus = fdr_plain = mfdr_plain = Fraction(0)
        for signs in itertools.product([1, -1], repeat=m0):
            w = [s * a for s, a in zip(list(signs) + alt_signs, mags)]
            for plus in (True, False):
                sel = knockoff_select(w, q, plus)
                r, v = sum(sel), sum(sel[:m0])
                if plus:
                    fdr_plus += Fraction(v, max(r, 1))
                else:
                    fdr_plain += Fraction(v, max(r, 1))
                    mfdr_plain += v / (r + 1 / q)
        total = 2**m0
        assert fdr_plus / total <= q
        assert mfdr_plain / total <= q
        worst_plain = max(worst_plain, fdr_plain / total)
    assert worst_plain > q


def test_monte_carlo_fdr_on_a_fixed_design() -> None:
    rng = random.Random(2018)
    n, p, k, amp, sigma_noise = 40, 10, 5, 4.0, 1.0
    q, reps = 0.2, 1000
    x = design(rng, n, p)
    xn, xk, s = knockoffs(x, rng=random.Random(5))
    stat = marginal_statistic(xn, xk)
    xn2, xk2, _ = knockoffs(x, s=0.9 * s, rng=random.Random(6))
    stat_ols = ols_statistic(xn2, xk2)
    beta = [amp] * k + [0.0] * (p - k)
    # BH on two-sided z-tests of the OLS coefficients, with the noise level known, for comparison.
    ev, evec = jacobi_eigen(gram(xn, xn))
    sinv = [[sum(evec[i][m] * evec[j][m] / ev[m] for m in range(p)) for j in range(p)] for i in range(p)]
    nd = statistics.NormalDist()
    results = {"plus": [0.0, 0.0], "plain": [0.0, 0.0], "ols_plus": [0.0, 0.0], "bh": [0.0, 0.0]}
    signs_null = 0
    for _ in range(reps):
        y = [sum(xn[i][j] * beta[j] for j in range(p)) + sigma_noise * rng.gauss(0, 1) for i in range(n)]
        y2 = [sum(xn2[i][j] * beta[j] for j in range(p)) + sigma_noise * rng.gauss(0, 1) for i in range(n)]
        w, w2 = stat(y), stat_ols(y2)
        signs_null += sum(1 for v in w[k:] if v > 0)
        xty = [sum(xn[i][j] * y[i] for i in range(n)) for j in range(p)]
        z = [sum(sinv[j][m] * xty[m] for m in range(p)) / math.sqrt(sinv[j][j]) for j in range(p)]
        pv = sorted((2 * (1 - nd.cdf(abs(z[j]))), j) for j in range(p))
        r_bh = max([i + 1 for i in range(p) if pv[i][0] <= (i + 1) * q / p] or [0])
        sel_bh = [False] * p
        for _, j in pv[:r_bh]:
            sel_bh[j] = True
        rules = {
            "plus": knockoff_select(w, q),
            "plain": knockoff_select(w, q, plus=False),
            "ols_plus": knockoff_select(w2, q),
            "bh": sel_bh,
        }
        for name, sel in rules.items():
            r = sum(sel)
            results[name][0] += sum(sel[k:]) / max(r, 1)
            results[name][1] += sum(sel[:k]) / k
    fdr = {name: v[0] / reps for name, v in results.items()}
    power = {name: v[1] / reps for name, v in results.items()}
    # Null statistics are positive half the time: 5000 signs, standard error 0.007.
    assert abs(signs_null / ((p - k) * reps) - 0.5) < 0.03
    # knockoff+ has FDR <= q = 0.2 by the theorem; 1000 runs give a standard error near 0.005.
    # With this seed: knockoff+ 0.12 (marginal W) and 0.11 (OLS W); the plain knockoff 0.23, above q.
    assert fdr["plus"] <= q + 0.02 and fdr["ols_plus"] <= q + 0.02
    assert fdr["plain"] > q
    # With p = 10, knockoff+ needs at least 1/q = 5 selections; BH on exact z-tests is more powerful here.
    assert 0.3 < power["plus"] < power["plain"] and power["ols_plus"] > 0.3
    assert power["bh"] > power["plus"]
    assert fdr["bh"] <= q
