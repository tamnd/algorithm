# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lms-algorithm/. The authors are listed in prov/7A11YC.jsonl.

import itertools
import math
import random
from fractions import Fraction as F

import pytest

from lms_algorithm import lms, lms_update, nlms_update


def matvec(a, v):
    return [sum(x * y for x, y in zip(row, v)) for row in a]


def moments(support):
    """R = E[u u^T] for u uniform on the support, in Fraction."""
    k = len(support[0])
    return [[sum(F(u[i] * u[j]) for u in support) / len(support) for j in range(k)] for i in range(k)]


def lambda_max_2x2(r):
    """Largest eigenvalue of a symmetric 2x2 matrix: (t + sqrt(t^2 - 4 det)) / 2."""
    t, det = r[0][0] + r[1][1], r[0][0] * r[1][1] - r[0][1] * r[1][0]
    disc = t * t - 4 * det
    num, den = math.isqrt(disc.numerator), math.isqrt(disc.denominator)
    if num * num == disc.numerator and den * den == disc.denominator:
        return (t + F(num, den)) / 2  # exact when the discriminant is a square
    return (float(t) + math.sqrt(disc)) / 2


def mean_by_enumeration(support, h, mu, n):
    """E[w_n] over all |support|^n input sequences, with d = h^T u and w_0 = 0."""
    total = [F(0)] * len(h)
    for seq in itertools.product(support, repeat=n):
        w = [F(0)] * len(h)
        for u in seq:
            w, _, _ = lms_update(w, u, sum(a * b for a, b in zip(h, u)), mu)
        total = [t + x for t, x in zip(total, w)]
    return [t / len(support) ** n for t in total]


def mean_closed_form(r, h, mu, n, w0=None):
    """E[w_n] = h + (I - mu R)^n (w_0 - h), from the recursion v <- (I - mu R) v on v = E[w] - h."""
    v = [-x for x in h] if w0 is None else [a - b for a, b in zip(w0, h)]
    for _ in range(n):
        v = [vi - mu * ri for vi, ri in zip(v, matvec(r, v))]
    return [hi + vi for hi, vi in zip(h, v)]


def test_trace_on_the_page() -> None:
    x = [F(1), F(-1), F(2), F(0), F(1), F(-2)]
    d = [F(1), F(-1, 2), F(3, 2), F(1), F(1), F(-3, 2)]  # d = x[n] + x[n-1]/2
    w, ys, es = lms(x, d, 2, F(1, 4))
    assert es == [1, F(-1, 4), F(13, 16), F(49, 32), F(9, 32), F(-27, 64)]
    assert w == [1, F(101, 256)]
    assert all(dn - yn == en for dn, yn, en in zip(d, ys, es))


def test_exact_mean_matches_independence_recursion() -> None:
    support = [(1, 1), (1, 0), (0, 1)]
    r = moments(support)
    assert r == [[F(2, 3), F(1, 3)], [F(1, 3), F(2, 3)]]
    assert lambda_max_2x2(r) == 1
    h = [F(1), F(-1, 2)]
    for mu in (F(1, 2), F(19, 10), F(2), F(5, 2)):
        for n in range(1, 7):
            assert mean_by_enumeration(support, h, mu, n) == mean_closed_form(r, h, mu, n)


def test_convergence_in_the_mean_exactly_inside_the_bound() -> None:
    support = [(1, 1), (1, 0), (0, 1)]
    r, h = moments(support), [F(1), F(-1, 2)]
    lam = lambda_max_2x2(r)
    dist = lambda mu, n: max(abs(a - b) for a, b in zip(mean_closed_form(r, h, mu, n), h))
    start = dist(F(0), 0)
    assert dist(F(1, 2), 400) < start * F(1, 10**20)
    assert dist(F(19, 10), 400) < start * F(1, 10**15)  # just inside 2 / lam = 2
    # on the bound: the component along the top eigenvector (1, 1) keeps its size 1/4
    for n in (400, 401):
        assert abs(dist(2 / lam, n) - F(1, 4)) < F(1, 10**150)
    assert dist(F(5, 2), 100) > start * 10**15  # outside: divergence


def test_random_distributions_against_the_bound() -> None:
    rng = random.Random(5301)
    done = 0
    while done < 500:
        support = [(rng.randint(-2, 2), rng.randint(-2, 2)) for _ in range(rng.randint(2, 4))]
        r = moments(support)
        if r[0][0] * r[1][1] - r[0][1] ** 2 == 0:
            continue  # R must be positive definite
        h = [F(rng.randint(-3, 3)), F(rng.randint(-3, 3), 2)]
        if h == [0, 0]:
            continue
        bound = 2 / float(lambda_max_2x2(r))
        mu = F(rng.randint(1, 109), 100) * F(bound).limit_denominator(10**6)
        assert mean_by_enumeration(support, h, mu, 3) == mean_closed_form(r, h, mu, 3)
        rf = [[float(v) for v in row] for row in r]
        # E[w_n] - h = (I - mu R)^n (w_0 - h); the columns of the power are the
        # errors from the starts w_0 = h + e_1 and w_0 = h + e_2
        inside = transition_power(rf, 0.9 * bound, 20)  # n = 2^20 steps
        outside = transition_power(rf, 1.1 * bound, 10)  # n = 2^10 steps
        assert max(abs(v) for row in inside for v in row) < 1e-6
        assert max(abs(v) for row in outside for v in row) > 1e6
        done += 1


def transition_power(r, mu, squarings):
    a = [[(1.0 if i == j else 0.0) - mu * r[i][j] for j in range(2)] for i in range(2)]
    for _ in range(squarings):
        a = [[sum(a[i][k] * a[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    return a


def test_transition_power_matches_the_recursion() -> None:
    rng = random.Random(5305)
    for _ in range(50):
        r = [[rng.uniform(0.5, 2), 0.0], [0.0, rng.uniform(0.5, 2)]]
        r[0][1] = r[1][0] = rng.uniform(-0.4, 0.4)
        mu = rng.uniform(0.1, 0.9)
        p = transition_power(r, mu, 3)
        col = mean_closed_form(r, [0.0, 0.0], mu, 8, [1.0, 0.0])
        assert abs(p[0][0] - col[0]) < 1e-12 and abs(p[1][0] - col[1]) < 1e-12


def second_moment(support, h, mu, n):
    """E[|w_n - h|^2] by enumeration, noiseless data."""
    total = F(0)
    for seq in itertools.product(support, repeat=n):
        w = [F(0)] * len(h)
        for u in seq:
            w, _, _ = lms_update(w, u, sum(a * b for a, b in zip(h, u)), mu)
        total += sum((a - b) ** 2 for a, b in zip(w, h))
    return total / len(support) ** n


def test_mean_square_needs_a_smaller_step() -> None:
    support, h = [(1, 1), (1, 0), (0, 1)], [F(1), F(-1, 2)]
    start = sum(v * v for v in h)
    # mu = 19/10 converges in the mean but the second moment grows
    assert second_moment(support, h, F(19, 10), 7) > 10 * start
    assert second_moment(support, h, F(1), 7) < start / 10
    # the exact mean-square limit of this example is 3 - sqrt(3), about 1.268
    assert second_moment(support, h, F(126, 100), 7) < second_moment(support, h, F(126, 100), 6)


def test_monte_carlo_system_identification() -> None:
    rng = random.Random(5302)
    h = [0.8, -0.4, 0.2]
    x = [rng.gauss(0, 1) for _ in range(4000)]
    d = [sum(h[k] * x[n - k] for k in range(3) if n - k >= 0) for n in range(len(x))]
    w, _, _ = lms(x, d, 3, 0.05)  # white input of variance 1: lambda_max = 1
    assert max(abs(a - b) for a, b in zip(w, h)) < 1e-6
    w, _, _ = lms(x[:300], d[:300], 3, 2.5)
    assert max(abs(a) for a in w) > 1e10


def test_monte_carlo_average_of_independent_runs() -> None:
    rng = random.Random(5303)
    support, h = [(1, 1), (1, 0), (0, 1)], [1.0, -0.5]
    r = moments(support)
    for mu, n in ((0.5, 30), (1.0, 30)):  # inside the mean-square limit, so the average settles
        runs, avg = 10000, [0.0, 0.0]
        for _ in range(runs):
            w = [0.0, 0.0]
            for _ in range(n):
                u = rng.choice(support)
                w, _, _ = lms_update(w, u, h[0] * u[0] + h[1] * u[1], mu)
            avg = [a + b / runs for a, b in zip(avg, w)]
        want = mean_closed_form([[float(v) for v in row] for row in r], h, mu, n)
        assert max(abs(a - b) for a, b in zip(avg, want)) < 0.05


def test_nlms_a_posteriori_error_is_zero() -> None:
    rng = random.Random(5304)
    for _ in range(500):
        m = rng.randint(1, 4)
        w = [F(rng.randint(-5, 5)) for _ in range(m)]
        u = [F(rng.randint(-5, 5)) for _ in range(m)]
        if all(v == 0 for v in u):
            continue
        d = F(rng.randint(-9, 9))
        w2, _, _ = nlms_update(w, u, d, F(1), F(0))
        assert d - sum(a * b for a, b in zip(w2, u)) == 0


def test_errors() -> None:
    with pytest.raises(ValueError):
        lms([1, 2], [1], 2, 0.1)
    with pytest.raises(ValueError):
        lms([1, 2], [1, 2], 0, 0.1)
