# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/least-squares-arx-identification/. The authors are listed in prov/HXP9D6.jsonl.

import random
from fractions import Fraction

from least_squares_arx_identification import arx_loss, arx_ls, arx_regressor, arx_simulate, first_sample


def test_worked_example():
    u = [1, 1, -1, 1, -1, -1]
    y = [Fraction(0), Fraction(1), Fraction(7, 5), Fraction(-1, 5), Fraction(9, 10), Fraction(-3, 5)]
    theta = arx_ls(y, u, 1, 1, 1)
    assert theta == [Fraction(-163, 336), Fraction(5407, 5600)]
    assert arx_loss(theta, y, u, 1, 1, 1) == Fraction(2899, 168000)


def test_exact_recovery_without_noise():
    rng = random.Random(11)
    a = [Fraction(-3, 2), Fraction(7, 10)]
    b = [Fraction(1), Fraction(1, 2)]
    u = [rng.choice((-1, 1)) for _ in range(30)]
    y = arx_simulate(a, b, 1, u)
    assert arx_ls(y, u, 2, 2, 1) == a + b


def _normal_residual(theta, y, u, na, nb, nk):
    d = na + nb
    g = [Fraction(0)] * d
    for t in range(first_sample(na, nb, nk), len(y)):
        phi = arx_regressor(y, u, na, nb, nk, t)
        e = y[t] - sum(p * th for p, th in zip(phi, theta))
        for i in range(d):
            g[i] += phi[i] * e
    return g


def test_random_normal_equations_and_minimum():
    # Oracle: the least squares minimizer is the unique theta whose residual is
    # orthogonal to every regressor column; also no perturbation lowers the loss.
    rng = random.Random(2024)
    done = 0
    while done < 500:
        na = rng.randint(0, 2)
        nb = rng.randint(1, 2)
        nk = rng.randint(0, 2)
        n = rng.randint(na + nb + 4, 12)
        u = [rng.randint(-3, 3) for _ in range(n)]
        y = [Fraction(rng.randint(-9, 9), rng.randint(1, 4)) for _ in range(n)]
        try:
            theta = arx_ls(y, u, na, nb, nk)
        except ValueError:
            continue
        assert all(v == 0 for v in _normal_residual(theta, y, u, na, nb, nk))
        v0 = arx_loss(theta, y, u, na, nb, nk)
        for _ in range(2):
            pert = [th + Fraction(rng.randint(-3, 3), 7) for th in theta]
            assert arx_loss(pert, y, u, na, nb, nk) >= v0
        done += 1


def test_consistent_with_white_noise():
    rng = random.Random(1)
    n = 4000
    u = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    e = [rng.gauss(0.0, 1.0) for _ in range(n)]
    y = arx_simulate([-1.5, 0.7], [1.0, 0.5], 1, u, e)
    theta = arx_ls(y, u, 2, 2, 1)
    for est, true in zip(theta, [-1.5, 0.7, 1.0, 0.5]):
        assert abs(est - true) < 0.06


def test_biased_with_colored_noise():
    rng = random.Random(1)
    n = 4000
    u = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    e = [rng.gauss(0.0, 1.0) for _ in range(n)]
    y = arx_simulate([-1.5, 0.7], [1.0, 0.5], 1, u, e, c=[-1.0, 0.2])
    theta = arx_ls(y, u, 2, 2, 1)
    assert abs(theta[0] - (-1.5)) > 0.15
    assert abs(theta[1] - 0.7) > 0.15


def test_constant_input_is_not_informative():
    u = [1] * 20
    y = arx_simulate([Fraction(-1, 2)], [1, 1], 1, u)
    try:
        arx_ls(y, u, 1, 2, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected a singular matrix")


def test_fir_and_direct_term():
    rng = random.Random(5)
    u = [rng.randint(-2, 2) for _ in range(15)]
    y = [3 * u[t] - (2 * u[t - 1] if t >= 1 else 0) for t in range(15)]
    assert arx_ls(y, u, 0, 2, 0) == [3, -2]


def test_bad_arguments():
    for args in (([1, 2, 3], [1, 2, 3], -1, 1, 1), ([1, 2, 3], [1, 2, 3], 1, 0, 1),
                 ([1, 2, 3], [1, 2], 1, 1, 1), ([1, 2], [1, 2], 2, 2, 1)):
        try:
            arx_ls(*args)
        except ValueError:
            continue
        raise AssertionError("expected ValueError for %r" % (args,))
