# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/turnbull-estimator/. The authors are listed in prov/0DBRMH.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from turnbull_estimator import Region, contains, innermost_intervals, survival, turnbull

INF = math.inf


def loglik(cells_of_obs, p):
    total = 0.0
    for cells in cells_of_obs:
        x = sum(p[c] for c in cells)
        if x <= 0:
            return -INF
        total += math.log(x)
    return total


def compositions(total, parts):
    """All tuples of `parts` non-negative integers that sum to `total`."""
    for bars in itertools.combinations(range(total + parts - 1), parts - 1):
        prev, out = -1, []
        for b in bars:
            out.append(b - prev - 1)
            prev = b
        out.append(total + parts - 2 - prev)
        yield out


def random_interval_data(rng, n):
    left, right = [], []
    for _ in range(n):
        a = rng.randint(0, 4)
        b = rng.choice([x for x in range(a + 1, 5)] + [INF])
        left.append(a)
        right.append(b)
    return left, right


def test_hand_example() -> None:
    # Sets (0,2], (1,3], (2,4], (3,inf): innermost intervals (1,2], (2,3], (3,4]. The
    # log-likelihood is log s1 + log(s1 + s2) + log(s2 + s3) + log s3, maximal at (1/2, 0, 1/2)
    # with value 4 log(1/2). The KKT condition holds with equality at the zero mass, g_2 = 1,
    # and there EM converges only sublinearly: s_2 is about 1/k after k iterations.
    fit = turnbull([0, 1, 2, 3], [2, 3, 4, INF], tol=1e-8)
    assert fit.regions == [Region(1, 2, True), Region(2, 3, True), Region(3, 4, True)]
    assert abs(fit.mass[0] - 0.5) < 1e-3 and abs(fit.mass[2] - 0.5) < 1e-3 and fit.mass[1] < 1e-3
    assert 4 * math.log(0.5) - 4 * fit.kkt_gap <= fit.loglik <= 4 * math.log(0.5)
    assert 1000 < fit.iterations
    lo, hi = survival(fit, 1)
    assert math.isclose(lo, 1.0) and math.isclose(hi, 1.0)
    lo, hi = survival(fit, 1.5)
    assert math.isclose(lo, 1 - fit.mass[0]) and math.isclose(hi, 1.0)


def test_against_brute_force_npmle_on_a_grid() -> None:
    # Endpoints in {0,...,4} or inf. The cells (0,1], ..., (3,4], (4,inf) carry the mass of any
    # distribution as far as the likelihood is concerned. The brute force tries every mass vector
    # on the simplex with step 1/16, 3876 vectors, without using the innermost intervals.
    rng = random.Random(1976)
    cells = [(k, k + 1) for k in range(4)] + [(4, INF)]
    for _ in range(6):
        left, right = random_interval_data(rng, rng.randint(4, 9))
        n = len(left)
        cells_of_obs = [[c for c, (u, v) in enumerate(cells) if a <= u and v <= b] for a, b in zip(left, right)]
        best = max(loglik(cells_of_obs, [k / 16 for k in comp]) for comp in compositions(16, 5))
        fit = turnbull(left, right, tol=1e-11)
        assert fit.loglik >= best - 1e-9  # the EM limit is at least as good as every grid point
        assert fit.loglik - best < 0.1  # and the grid comes close to it
        # The certified bound: no distribution beats the fit by more than n * kkt_gap.
        assert fit.kkt_gap <= 1e-11
        for _ in range(200):
            w = [rng.random() for _ in cells]
            tot = sum(w)
            assert loglik(cells_of_obs, [x / tot for x in w]) <= fit.loglik + n * fit.kkt_gap + 1e-12


def test_innermost_intervals_carry_every_signature() -> None:
    # Each point of the line has a signature, the set of observations that contain it.
    # Every signature is contained in the signature of some innermost interval, so moving
    # mass into the innermost intervals never lowers the likelihood.
    rng = random.Random(1955)
    for _ in range(100):
        n = rng.randint(1, 8)
        left, right = [], []
        for _ in range(n):
            a = rng.randint(0, 6)
            if rng.random() < 0.25:
                left.append(a)
                right.append(a)  # an exact time
            else:
                left.append(a)
                right.append(rng.choice([x for x in range(a + 1, 8)] + [INF]))
        regions = innermost_intervals(left, right)
        sig = [frozenset(i for i in range(n) if contains(q, left[i], right[i])) for q in regions]
        for i in range(n):
            assert any(i in s for s in sig)  # every observation contains an innermost interval
        points = [x / 2 for x in range(0, 20)]
        for x in points:
            s = frozenset(i for i in range(n) if (left[i] < x <= right[i]) or (left[i] == right[i] == x))
            assert any(s <= t for t in sig)
        for a, b in itertools.combinations(range(len(regions)), 2):
            assert not (sig[a] < sig[b] or sig[b] < sig[a])  # no region is dominated by another


def pav(values, weights):
    """Weighted isotonic (nondecreasing) regression by pool adjacent violators, in Fractions."""
    blocks = []  # [value, weight, count]
    for v, w in zip(values, weights):
        blocks.append([Fraction(v), Fraction(w), 1])
        while len(blocks) > 1 and blocks[-2][0] > blocks[-1][0]:
            v2, w2, c2 = blocks.pop()
            v1, w1, c1 = blocks.pop()
            blocks.append([(v1 * w1 + v2 * w2) / (w1 + w2), w1 + w2, c1 + c2])
    out = []
    for v, _, c in blocks:
        out.extend([v] * c)
    return out


def test_current_status_is_isotonic_regression() -> None:
    # Current status data: at time c_i only delta_i = 1{T_i <= c_i} is seen, so the set is
    # (0, c_i] or (c_i, inf). The NPMLE of F at the distinct c is the isotonic regression of
    # the delta, the mean of the delta at each c weighted by the count (Ayer et al. 1955).
    rng = random.Random(1955)
    for _ in range(10):
        n = rng.randint(5, 30)
        c = [rng.randint(1, 10) for _ in range(n)]
        t = [rng.expovariate(0.2) for _ in range(n)]
        delta = [1 if ti <= ci else 0 for ti, ci in zip(t, c)]
        left = [0 if d else ci for ci, d in zip(c, delta)]
        right = [ci if d else INF for ci, d in zip(c, delta)]
        xs = sorted(set(c))
        means = [Fraction(sum(d for ci, d in zip(c, delta) if ci == x), c.count(x)) for x in xs]
        f_hat = pav(means, [c.count(x) for x in xs])
        ll_pav = sum(math.log(f_hat[xs.index(ci)] if d else 1 - f_hat[xs.index(ci)]) for ci, d in zip(c, delta))
        fit = turnbull(left, right, tol=1e-9)
        assert ll_pav - n * fit.kkt_gap - 1e-12 <= fit.loglik <= ll_pav + 1e-12
        for x, f in zip(xs, f_hat):
            lo, hi = survival(fit, x)
            assert lo == hi  # S is determined at the observation times
            assert abs((1 - lo) - float(f)) < 1e-3


def kaplan_meier_exact(times, events):
    """S at each distinct time, by the product limit in Fractions."""
    s, out = Fraction(1), {}
    for t in sorted(set(times)):
        n = sum(1 for y in times if y >= t)
        d = sum(1 for y, e in zip(times, events) if y == t and e)
        s *= 1 - Fraction(d, n)
        out[t] = s
    return out


def test_exact_and_right_censored_data_give_kaplan_meier() -> None:
    rng = random.Random(1958)
    for _ in range(25):
        n = rng.randint(2, 25)
        times = [rng.randint(1, 12) for _ in range(n)]
        events = [1 if rng.random() < 0.6 else 0 for _ in range(n)]
        events[0] = 1
        left = list(times)
        right = [y if e else INF for y, e in zip(times, events)]
        fit = turnbull(left, right, tol=1e-12)
        km = kaplan_meier_exact(times, events)
        for t, s in km.items():
            lo, hi = survival(fit, t)
            assert math.isclose(lo, hi, abs_tol=1e-12)
            assert abs(lo - float(s)) < 1e-6


def test_exact_times_give_the_empirical_distribution() -> None:
    # Only exact times: the innermost intervals are the distinct times, the iteration stops
    # at once, and the masses are the empirical frequencies.
    rng = random.Random(1933)
    for _ in range(25):
        n = rng.randint(1, 30)
        times = [rng.randint(0, 9) for _ in range(n)]
        fit = turnbull(times, times, tol=1e-14)
        assert [q.left for q in fit.regions] == sorted(set(times))
        assert all(not q.left_open and q.left == q.right for q in fit.regions)
        for q, w in zip(fit.regions, fit.mass):
            assert math.isclose(w, float(Fraction(times.count(q.left), n)), rel_tol=1e-12)
        for t in range(-1, 11):
            lo, hi = survival(fit, t)
            assert lo == hi and math.isclose(lo, sum(1 for y in times if y > t) / n, abs_tol=1e-12)


def test_self_consistency_at_the_limit() -> None:
    # Turnbull's equation: s_j = (1/n) sum_i alpha_ij s_j / sum_l alpha_il s_l.
    rng = random.Random(7)
    left, right = random_interval_data(rng, 40)
    fit = turnbull(left, right, tol=1e-13)
    cover = [[j for j, q in enumerate(fit.regions) if contains(q, a, b)] for a, b in zip(left, right)]
    dens = [sum(fit.mass[j] for j in cov) for cov in cover]
    for j, s in enumerate(fit.mass):
        rhs = sum(s / dens[i] for i in range(len(left)) if j in cover[i]) / len(left)
        assert math.isclose(s, rhs, abs_tol=1e-12)
    assert math.isclose(math.fsum(fit.mass), 1.0, rel_tol=1e-14)


def test_rejects_bad_input() -> None:
    with pytest.raises(ValueError):
        turnbull([], [])
    with pytest.raises(ValueError):
        turnbull([2], [1])
    with pytest.raises(ValueError):
        turnbull([INF], [INF])
    with pytest.raises(ValueError):
        turnbull([1, 2], [3])
