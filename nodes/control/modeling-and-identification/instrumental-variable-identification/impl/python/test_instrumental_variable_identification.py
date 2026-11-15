# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/instrumental-variable-identification/. The authors are listed in prov/YQN1Q7.jsonl.

import random
from fractions import Fraction

from instrumental_variable_identification import iv_arx, iv_solve, regressor

A_TRUE = [-1.5, 0.7]
B_TRUE = [1.0, 0.5]
C_TRUE = [-1.0, 0.2]


def _armax(a, b, c, u, e):
    y = []
    for t in range(len(u)):
        s = e[t]
        for i, ci in enumerate(c, start=1):
            if t - i >= 0:
                s += ci * e[t - i]
        for j, bj in enumerate(b):
            if t - 1 - j >= 0:
                s += bj * u[t - 1 - j]
        for i, ai in enumerate(a, start=1):
            if t - i >= 0:
                s -= ai * y[t - i]
        y.append(s)
    return y


def _data(n, seed):
    rng = random.Random(seed)
    u = [rng.choice((-1.0, 1.0)) for _ in range(n)]
    e = [rng.gauss(0.0, 1.0) for _ in range(n)]
    return _armax(A_TRUE, B_TRUE, C_TRUE, u, e), u


def test_worked_example():
    y, u = _data(2000, 1)
    want_delayed = [-1.5471, 0.7584, 1.0261, 0.4135]
    want_model = [-1.5210, 0.7207, 1.0311, 0.4428]
    got = iv_arx(y, u, 2, 2, 1)
    assert all(abs(p - q) < 1e-4 for p, q in zip(got, want_delayed))
    got = iv_arx(y, u, 2, 2, 1, "model")
    assert all(abs(p - q) < 1e-4 for p, q in zip(got, want_model))


def test_exact_without_noise():
    rng = random.Random(4)
    a = [Fraction(-3, 2), Fraction(7, 10)]
    b = [Fraction(1), Fraction(1, 2)]
    u = [rng.choice((-1, 1)) for _ in range(25)]
    y = _armax(a, b, [], u, [0] * 25)
    assert iv_arx(y, u, 2, 2, 1) == a + b
    assert iv_arx(y, u, 2, 2, 1, "model") == a + b


def test_random_phi_as_instrument_is_least_squares():
    # Oracle: with zeta = phi the estimate must satisfy the least squares
    # normal equations exactly: the residual is orthogonal to every column.
    rng = random.Random(99)
    done = 0
    while done < 500:
        na = rng.randint(0, 2)
        nb = rng.randint(1, 2)
        nk = rng.randint(0, 2)
        n = rng.randint(na + nb + 5, 12)
        u = [rng.randint(-3, 3) for _ in range(n)]
        y = [Fraction(rng.randint(-9, 9), rng.randint(1, 3)) for _ in range(n)]
        t0 = max(na, nk + nb - 1)

        def phi(t):
            return regressor(y, u, na, nb, nk, t)

        try:
            theta = iv_solve(y, phi, phi, t0)
        except ValueError:
            continue
        for i in range(na + nb):
            s = 0
            for t in range(t0, n):
                p = phi(t)
                s += p[i] * (y[t] - sum(x * th for x, th in zip(p, theta)))
            assert s == 0
        done += 1


def test_consistent_where_least_squares_is_biased():
    y, u = _data(20000, 2)
    iv = iv_arx(y, u, 2, 2, 1, "model")
    for est, true in zip(iv, A_TRUE + B_TRUE):
        assert abs(est - true) < 0.05

    def phi(t):
        return regressor(y, u, 2, 2, 1, t)

    ls = iv_solve(y, phi, phi, 2)
    assert abs(ls[0] - A_TRUE[0]) > 0.15


def test_constant_input_gives_singular_matrix():
    u = [1] * 20
    y = _armax([Fraction(-1, 2)], [1], [], u, [0] * 20)
    try:
        iv_arx(y, u, 1, 1, 1)
    except ValueError:
        pass
    else:
        raise AssertionError("expected a singular matrix")


def test_bad_arguments():
    for args, kwargs in ((([1.0] * 9, [1.0] * 9, 1, 0), {}), (([1.0] * 9, [1.0] * 8, 1, 1), {}),
                         (([1.0] * 9, [1.0] * 9, 1, 1), {"instruments": "other"}),
                         (([1.0] * 3, [1.0] * 3, 2, 2), {})):
        try:
            iv_arx(*args, **kwargs)
        except ValueError:
            continue
        raise AssertionError("expected ValueError")
