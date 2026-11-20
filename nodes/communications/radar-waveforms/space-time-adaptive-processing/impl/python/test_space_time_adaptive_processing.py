# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/space-time-adaptive-processing/. The authors are listed in prov/STKZ5N.jsonl.

import random

import pytest

from cbb import cholesky, cn, solve
from space_time_adaptive_processing import (
    brennan_rank,
    cholesky_solve,
    clutter_covariance,
    rmb_mean_loss,
    sample_covariance,
    sinr,
    smi_stap,
    steering,
)


def dot(a, b):
    return sum(x.conjugate() * y for x, y in zip(a, b))


def numeric_rank(a, rel=1e-9):
    """Rank by Gaussian elimination with complete pivoting and a relative tolerance."""
    m = [[complex(v) for v in row] for row in a]
    rows, cols = len(m), len(m[0])
    top = max(abs(v) for row in m for v in row)
    rank = 0
    for c in range(min(rows, cols)):
        best, bi, bk = 0.0, -1, -1
        for i in range(c, rows):
            for k in range(c, cols):
                if abs(m[i][k]) > best:
                    best, bi, bk = abs(m[i][k]), i, k
        if best <= rel * top:
            break
        m[c], m[bi] = m[bi], m[c]
        for row in m:
            row[c], row[bk] = row[bk], row[c]
        for i in range(c + 1, rows):
            f = m[i][c] / m[c][c]
            for k in range(c, cols):
                m[i][k] -= f * m[c][k]
        rank += 1
    return rank


def random_hpd(rng, d):
    t = d + rng.randint(1, 4)
    r = sample_covariance([[cn(rng, 1.0) for _ in range(d)] for _ in range(t)])
    return r


def draw(rng, g):
    z = [cn(rng, 1.0) for _ in range(len(g))]
    return [sum(g[i][k] * z[k] for k in range(i + 1)) for i in range(len(g))]


def test_worked_example():
    # Two elements, one pulse. Training [3, 3] (a jammer at broadside) and [1, -1]
    # give R = [[5, 4], [4, 5]]. The target is at f_s = 0.25, so v = [1, j].
    training = [[3, 3], [1, -1]]
    assert sample_covariance(training) == [[5, 4], [4, 5]]
    v = [1, 1j]
    w, y, amf = smi_stap(training, v, v)
    assert all(abs(a - b) < 1e-12 for a, b in zip(w, [(5 - 4j) / 9, (-4 + 5j) / 9]))
    assert y == pytest.approx(10 / 9) and amf == pytest.approx(10 / 9)
    assert abs(dot(w, [1, 1])) ** 2 == pytest.approx(2 / 81)
    r = [[5, 4], [4, 5]]
    assert sinr(w, v, r) == pytest.approx(10 / 9)
    assert sinr(v, v, r) == pytest.approx(0.4)


def test_cholesky_solve_matches_gaussian_elimination():
    rng = random.Random(8101)
    for _ in range(500):
        d = rng.randint(1, 6)
        r = random_hpd(rng, d)
        v = [cn(rng, 1.0) for _ in range(d)]
        got = cholesky_solve(cholesky(r), v)
        want = solve(r, v)
        assert all(abs(a - b) < 1e-8 * (1 + abs(b)) for a, b in zip(got, want))


def test_loading_is_added_to_the_diagonal():
    rng = random.Random(8104)
    for _ in range(100):
        d = rng.randint(2, 6)
        t = rng.randint(1, d - 1)
        training = [[cn(rng, 1.0) for _ in range(d)] for _ in range(t)]
        v = [cn(rng, 1.0) for _ in range(d)]
        delta = rng.uniform(0.1, 3.0)
        w, _, _ = smi_stap(training, v, v, delta)
        r = sample_covariance(training)
        for i in range(d):
            r[i][i] += delta
        assert all(abs(a - b) < 1e-8 * (1 + abs(b)) for a, b in zip(w, solve(r, v)))
    with pytest.raises(ValueError):
        smi_stap([[1, 1]], [1, 1], [1, 1])  # T < D without loading: R is singular


def test_optimum_weight_beats_random_weights():
    rng = random.Random(8102)
    for _ in range(300):
        d = rng.randint(1, 6)
        r = random_hpd(rng, d)
        v = [cn(rng, 1.0) for _ in range(d)]
        w = solve(r, v)
        best = dot(v, w).real
        assert sinr(w, v, r) == pytest.approx(best, rel=1e-8)
        u = [cn(rng, 1.0) for _ in range(d)]
        assert sinr(u, v, r) <= best * (1 + 1e-9)


@pytest.mark.parametrize("m,p,beta,want", [(4, 4, 1, 7), (4, 4, 2, 10), (3, 4, 1, 6), (4, 3, 2, 8)])
def test_brennan_rule_for_integer_beta(m, p, beta, want):
    assert brennan_rank(m, p, beta) == want
    r = clutter_covariance(m, p, beta, 3 * m * p, 1.0)
    rc = [[v - (1 if i == k else 0) for k, v in enumerate(row)] for i, row in enumerate(r)]
    assert numeric_rank(rc) == want


def test_clutter_ridge_is_nulled():
    m, p, beta = 4, 4, 1.0
    d = m * p
    r = clutter_covariance(m, p, beta, 64, 10 ** 4)  # CNR 40 dB, noise power 1
    off = steering(m, p, 0.0, 0.5)
    on = steering(m, p, 0.125, 0.125)
    opt_off = sinr(solve(r, off), off, r)
    opt_on = sinr(solve(r, on), on, r)
    assert opt_off > 0.8 * d  # within 1 dB of the noise-only value D
    assert opt_on < 1e-3 * d  # a target on the clutter ridge is lost
    # The non-adaptive filter v lets the clutter in through its sidelobes: more than 20 dB worse.
    assert sinr(off, off, r) < 0.01 * opt_off


@pytest.mark.parametrize("t_count", [5, 8])
def test_rmb_mean_loss(t_count):
    # D = 4 (M = 2, P = 2), 600 trials, seed 8103; E rho = (T + 2 - D) / (T + 1).
    m, p = 2, 2
    d = m * p
    r = clutter_covariance(m, p, 1.0, 8, 100.0)
    g = cholesky(r)
    v = steering(m, p, 0.1, -0.3)
    best = dot(v, solve(r, v)).real
    rng = random.Random(8103 + t_count)
    total, trials = 0.0, 600
    for _ in range(trials):
        training = [draw(rng, g) for _ in range(t_count)]
        w, _, _ = smi_stap(training, v, v)
        total += sinr(w, v, r) / best
    assert total / trials == pytest.approx(rmb_mean_loss(d, t_count), abs=0.03)


def test_rmb_closed_form_values():
    assert rmb_mean_loss(4, 5) == pytest.approx(0.5)
    assert rmb_mean_loss(16, 29) == pytest.approx(0.5)
    assert rmb_mean_loss(4, 8) == pytest.approx(2 / 3)


def test_steering_is_a_kronecker_product():
    rng = random.Random(8105)
    for _ in range(100):
        m, p = rng.randint(1, 5), rng.randint(1, 5)
        fs, ft = rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)
        a = steering(m, 1, fs, 0.0)
        b = steering(1, p, 0.0, ft)
        v = steering(m, p, fs, ft)
        assert all(abs(v[q * m + k] - b[q] * a[k]) < 1e-12 for q in range(p) for k in range(m))
