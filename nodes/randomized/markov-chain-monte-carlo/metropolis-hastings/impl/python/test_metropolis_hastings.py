# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/metropolis-hastings/. The authors are listed in prov/F19R05.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from metropolis_hastings import metropolis_hastings, transition_matrix


def stationary_check(p, w):
    n = len(w)
    pi = [v / sum(w) for v in w]
    for y in range(n):
        assert sum(pi[x] * p[x][y] for x in range(n)) == pi[y]
    for x in range(n):
        assert sum(p[x]) == 1
        assert all(v >= 0 for v in p[x])
        for y in range(n):
            assert pi[x] * p[x][y] == pi[y] * p[y][x]
    return pi


def solve(a, b):
    n = len(a)
    m = [list(a[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        r = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[r] = m[r], m[c]
        m[c] = [v / m[c][c] for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] for i in range(n)]


def asymptotic_variance(p, pi, f):
    """Exact sigma^2 = lim T Var(mean of f) via the fundamental matrix."""
    n = len(p)
    mu = sum(a * b for a, b in zip(pi, f))
    g = [v - mu for v in f]
    a = [[F(int(i == j)) - p[i][j] + pi[j] for j in range(n)] for i in range(n)]
    h = solve(a, g)
    return sum(pi[i] * g[i] * (2 * h[i] - g[i]) for i in range(n))


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / tau


def test_example_matrix() -> None:
    w = [F(1), F(2), F(3)]
    q = [[F(0), F(1, 2), F(1, 2)], [F(1, 2), F(0), F(1, 2)], [F(1, 2), F(1, 2), F(0)]]
    p = transition_matrix(w, q)
    assert p == [
        [F(0), F(1, 2), F(1, 2)],
        [F(1, 4), F(1, 4), F(1, 2)],
        [F(1, 6), F(1, 3), F(1, 2)],
    ]
    stationary_check(p, w)


def cycle_proposal(n, up=F(2, 3)):
    q = [[F(0)] * n for _ in range(n)]
    for x in range(n):
        q[x][(x + 1) % n] += up
        q[x][(x - 1) % n] += 1 - up
    return q


def test_hastings_correction_on_cycle() -> None:
    p = transition_matrix([F(1)] * 4, cycle_proposal(4))
    for x in range(4):
        assert p[x][(x + 1) % 4] == F(1, 3)
        assert p[x][(x - 1) % 4] == F(1, 3)
        assert p[x][x] == F(1, 3)


def test_asymmetric_proposal_exact() -> None:
    w = [F(1), F(3), F(2), F(5), F(4)]
    q = cycle_proposal(5)
    pi = stationary_check(transition_matrix(w, q), w)
    # without the Hastings factor the target is not stationary
    n = len(w)
    bad = [[F(0)] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if y != x and q[x][y] > 0:
                bad[x][y] = q[x][y] * min(F(1), w[y] / w[x])
        bad[x][x] = 1 - sum(bad[x])
    assert any(sum(pi[x] * bad[x][y] for x in range(n)) != pi[y] for y in range(n))


def test_long_run_matches_exact() -> None:
    w = [F(1), F(3), F(2), F(5), F(4)]
    q = cycle_proposal(5)
    p = transition_matrix(w, q)
    pi = [v / sum(w) for v in w]
    rng = random.Random(20251)
    n_steps = 200_000

    def prop(x, r):
        return (x + 1) % 5 if r.random() < 2 / 3 else (x - 1) % 5

    def logq(x, y):
        return math.log(2 / 3) if y == (x + 1) % 5 else math.log(1 / 3)

    chain, acc = metropolis_hastings(lambda x: math.log(w[x]), prop, logq, 0, n_steps, rng)
    assert len(chain) == n_steps and 0 < acc < n_steps
    for s in range(5):
        f = [F(int(x == s)) for x in range(5)]
        sd = math.sqrt(float(asymptotic_variance(p, pi, f)) / n_steps)
        freq = chain.count(s) / n_steps
        assert abs(freq - float(pi[s])) < 5 * sd


def exp_target(x):
    return -x if x > 0 else -math.inf


def lognormal_prop(x, r):
    return x * math.exp(0.8 * r.gauss(0.0, 1.0))


def lognormal_logq(x, y):
    # log density of y given x, up to a constant that cancels: -log y - (log y - log x)^2 / (2 s^2)
    return -math.log(y) - (math.log(y) - math.log(x)) ** 2 / (2 * 0.64)


def test_continuous_exponential_target() -> None:
    rng = random.Random(7)
    chain, _ = metropolis_hastings(exp_target, lognormal_prop, lognormal_logq, 1.0, 41_000, rng)
    xs = chain[1000:]
    n = len(xs)
    m = sum(xs) / n
    v = sum((x - m) ** 2 for x in xs) / n
    assert abs(m - 1.0) < 5 * math.sqrt(v / ess(xs))
    sq = [(x - m) ** 2 for x in xs]
    sv = math.sqrt(sum((s - v) ** 2 for s in sq) / n)
    assert abs(v - 1.0) < 5 * sv / math.sqrt(ess(sq))


def test_missing_correction_is_wrong() -> None:
    rng = random.Random(7)
    chain, _ = metropolis_hastings(exp_target, lognormal_prop, lambda x, y: 0.0, 1.0, 20_000, rng)
    assert sum(chain[1000:]) / 19_000 < 0.5


def test_start_outside_support() -> None:
    with pytest.raises(ValueError):
        metropolis_hastings(exp_target, lognormal_prop, lognormal_logq, -1.0, 10, random.Random(1))


def test_zero_steps() -> None:
    assert metropolis_hastings(exp_target, lognormal_prop, lognormal_logq, 1.0, 0, random.Random(1)) == ([], 0)
