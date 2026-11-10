# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/independence-sampler/. The authors are listed in prov/AW5Q0G.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from independence_sampler import independence_sampler, transition_matrix


def ess(xs):
    """Effective sample size by Geyer's initial positive sequence."""
    n = len(xs)
    m = sum(xs) / n
    c = [x - m for x in xs]
    var = sum(v * v for v in c) / n
    if var == 0:
        return 1.0

    def rho(k):
        return sum(c[i] * c[i + k] for i in range(n - k)) / (n * var)

    tau, k = -1.0, 0
    while k + 1 < n:
        g = rho(k) + rho(k + 1)
        if g <= 0:
            break
        tau += 2 * g
        k += 2
    return n / max(tau, 1e-9)


def check_mean(xs, mu, sd):
    assert abs(sum(xs) / len(xs) - mu) < 5 * sd / math.sqrt(ess(xs))


def step(mu, p):
    n = len(mu)
    return [sum(mu[a] * p[a][b] for a in range(n)) for b in range(n)]


def tv(mu, nu):
    return sum(abs(a - b) for a, b in zip(mu, nu)) / 2


def test_example_matrix_and_distances() -> None:
    pi = [F(1, 6), F(1, 3), F(1, 2)]
    q = [F(1, 2), F(1, 4), F(1, 4)]
    p = transition_matrix(pi, q)
    assert p == [
        [F(1, 2), F(1, 4), F(1, 4)],
        [F(1, 8), F(5, 8), F(1, 4)],
        [F(1, 12), F(1, 6), F(3, 4)],
    ]
    assert step(pi, p) == pi
    mu = [F(1), F(0), F(0)]
    got = []
    for _ in range(5):
        mu = step(mu, p)
        got.append(tv(mu, pi))
    assert got == [F(1, 3), F(13, 96), F(1, 16), F(1, 32), F(1, 64)]
    # 1/2 is an eigenvalue: det(P - I/2) = 0
    a = [[p[i][j] - F(int(i == j), 2) for j in range(3)] for i in range(3)]
    det = (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
           - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
           + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))
    assert det == 0


def test_bound_on_random_tables() -> None:
    rng = random.Random(7)
    for _ in range(20):
        n = rng.randint(2, 6)
        t = [F(rng.randint(1, 9)) for _ in range(n)]
        q = [F(rng.randint(1, 9)) for _ in range(n)]
        p = transition_matrix(t, q)
        pi = [v / sum(t) for v in t]
        qn = [v / sum(q) for v in q]
        m = max(a / b for a, b in zip(pi, qn))
        assert all(pi[x] * p[x][y] == pi[y] * p[y][x] for x in range(n) for y in range(n))
        for x in range(n):
            assert all(p[x][y] >= pi[y] / m for y in range(n))
            mu = [F(int(i == x)) for i in range(n)]
            for s in range(1, 6):
                mu = step(mu, p)
                assert tv(mu, pi) <= (1 - 1 / m) ** s


def gauss_logpdf(x, mu, sd):
    return -0.5 * ((x - mu) / sd) ** 2 - math.log(sd)


def test_gaussian_target_with_wide_proposal() -> None:
    # target N(1, 1), proposal N(0, 2^2): the weight is bounded
    chain, acc = independence_sampler(
        lambda x: gauss_logpdf(x, 1.0, 1.0),
        lambda r: r.gauss(0.0, 2.0),
        lambda y: gauss_logpdf(y, 0.0, 2.0),
        0.0,
        60_000,
        random.Random(8),
    )
    assert 0.3 < acc / len(chain) < 0.8
    check_mean(chain, 1.0, 1.0)
    check_mean([(x - 1.0) ** 2 for x in chain], 1.0, math.sqrt(2.0))


def test_light_tailed_proposal_gets_stuck() -> None:
    # target N(0, 4), proposal N(0, 1): w(6) is about 3.6e5, so the chain stays at 6
    chain, acc = independence_sampler(
        lambda x: gauss_logpdf(x, 0.0, 2.0),
        lambda r: r.gauss(0.0, 1.0),
        lambda y: gauss_logpdf(y, 0.0, 1.0),
        6.0,
        2000,
        random.Random(9),
    )
    assert acc == 0 and set(chain) == {6.0}


def test_bad_start() -> None:
    with pytest.raises(ValueError):
        independence_sampler(lambda x: -math.inf, lambda r: 0.0, lambda y: 0.0, 1.0, 3, random.Random(1))
