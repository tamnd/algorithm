# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nesterov-accelerated-gradient/. The authors are listed in prov/FR184S.jsonl.

import math
import random

import pytest

from nesterov_accelerated_gradient import nesterov_accelerated_gradient

TOL = 1e-9


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def matvec(a, v):
    return [dot(row, v) for row in a]


def householder(v):
    """The orthogonal matrix I - 2 v v^T / (v^T v)."""
    s = sum(t * t for t in v)
    n = len(v)
    return [[(1.0 if i == j else 0.0) - 2.0 * v[i] * v[j] / s for j in range(n)] for i in range(n)]


def t_sequence(k):
    """t_1 = 1, t_{j+1} = (1 + sqrt(1 + 4 t_j^2)) / 2; returns [None, t_1, ..., t_k]."""
    ts = [None, 1.0]
    for _ in range(k - 1):
        ts.append((1.0 + math.sqrt(1.0 + 4.0 * ts[-1] ** 2)) / 2.0)
    return ts


def quadratic(rng, n, lam):
    """f(x) = 1/2 (x - c)^T A (x - c), A = Q diag(lam) Q^T, f* = 0.
    Returns f, grad and the projection of a point onto the set of minimizers."""
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    a = [[sum(q[i][t] * lam[t] * q[j][t] for t in range(n)) for j in range(n)] for i in range(n)]
    c = [rng.uniform(-5, 5) for _ in range(n)]

    def f(x):
        e = [xi - ci for xi, ci in zip(x, c)]
        return 0.5 * dot(e, matvec(a, e))

    def grad(x):
        return matvec(a, [xi - ci for xi, ci in zip(x, c)])

    def project(x):
        e = [xi - ci for xi, ci in zip(x, c)]
        z = [sum(q[i][t] * e[i] for i in range(n)) for t in range(n)]
        z = [zt if l == 0 else 0.0 for zt, l in zip(z, lam)]
        return [ci + sum(q[i][t] * z[t] for t in range(n)) for i, ci in enumerate(c)]

    return f, grad, project


def smooth_abs(rng, n):
    """f(x) = sum_i w_i (sqrt(1 + (z_i - c_i)^2) - 1), z = Q x: convex, L-smooth with L = max w_i,
    not strongly convex, with f* = 0 at the unique minimizer Q^T c."""
    q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
    w = [rng.uniform(0.2, 5.0) for _ in range(n)]
    c = [rng.uniform(-3, 3) for _ in range(n)]

    def f(x):
        z = matvec(q, x)
        return sum(wi * (math.sqrt(1.0 + (zi - ci) ** 2) - 1.0) for wi, zi, ci in zip(w, z, c))

    def grad(x):
        z = matvec(q, x)
        t = [wi * (zi - ci) / math.sqrt(1.0 + (zi - ci) ** 2) for wi, zi, ci in zip(w, z, c)]
        return [sum(q[s][i] * t[s] for s in range(n)) for i in range(n)]

    xstar = [sum(q[s][i] * c[s] for s in range(n)) for i in range(n)]
    return f, grad, max(w), (lambda x: xstar)


def test_worked_example():
    f = lambda x: 0.5 * (x[0] ** 2 + 10.0 * x[1] ** 2)
    grad = lambda x: [x[0], 10.0 * x[1]]
    path = nesterov_accelerated_gradient(grad, [10.0, 1.0], 10.0, 1000)
    first = next(k for k, x in enumerate(path) if math.hypot(*grad(x)) <= 1e-6)
    assert first == 148
    assert path[1] == [9.0, 0.0] and path[2] == [8.1, 0.0]
    increases = [k for k in range(40) if f(path[k + 1]) > f(path[k])]
    assert increases[:4] == [11, 12, 13, 14]
    path = nesterov_accelerated_gradient(grad, [10.0, 1.0], 10.0, 1000, mu=1.0)
    first = next(k for k, x in enumerate(path) if math.hypot(*grad(x)) <= 1e-6)
    assert first == 50
    assert all(f(path[k + 1]) <= f(path[k]) for k in range(first))
    grad2 = lambda x: [x[0], 1000.0 * x[1]]
    for mu, expected in ((0.0, 6479), (1.0, 595)):
        path = nesterov_accelerated_gradient(grad2, [10.0, 1.0], 1000.0, 100000, mu=mu)
        assert next(k for k, x in enumerate(path) if math.hypot(*grad2(x)) <= 1e-6) == expected


def test_rejects_bad_input():
    with pytest.raises(ValueError):
        nesterov_accelerated_gradient(lambda x: x, [1.0], 0.0, 3)
    with pytest.raises(ValueError):
        nesterov_accelerated_gradient(lambda x: x, [1.0], 1.0, 3, mu=2.0)


def test_t_sequence_lower_bound():
    ts = t_sequence(1000)
    for k in range(1, 1001):
        assert ts[k] >= (k + 1) / 2.0
        if k > 1:
            assert math.isclose(ts[k] ** 2 - ts[k], ts[k - 1] ** 2, rel_tol=1e-12)


def test_convex_potential_and_rate_every_iterate():
    """For convex L-smooth f: t_k^2 (f(x_k) - f*) + L/2 ||t_k x_k - (t_k - 1) x_{k-1} - x*||^2 <= L/2 R^2,
    hence f(x_k) - f* <= L R^2 / (2 t_k^2) <= 2 L R^2 / (k + 1)^2, for every k >= 1."""
    rng = random.Random(8401)
    for trial in range(200):
        n = rng.randint(1, 6)
        if trial % 2 == 0:
            lam = [rng.uniform(0.0, 10.0) for _ in range(n)]
            if n > 1 and rng.random() < 0.5:
                lam[rng.randrange(n)] = 0.0
            if max(lam) == 0.0:
                lam[0] = 1.0
            f, grad, project = quadratic(rng, n, lam)
            big_l = max(lam) * rng.choice([1.0, 1.0, 2.0])
        else:
            f, grad, big_l, project = smooth_abs(rng, n)
        x0 = [rng.uniform(-10, 10) for _ in range(n)]
        xstar = project(x0)
        r2 = math.dist(x0, xstar) ** 2
        k_max = 200
        path = nesterov_accelerated_gradient(grad, x0, big_l, k_max)
        ts = t_sequence(k_max)
        scale = 1.0 + big_l * r2
        for k in range(1, len(path)):
            gap = f(path[k])
            u = [ts[k] * a - (ts[k] - 1.0) * b - s for a, b, s in zip(path[k], path[k - 1], xstar)]
            potential = ts[k] ** 2 * gap + 0.5 * big_l * dot(u, u)
            assert potential <= 0.5 * big_l * r2 + TOL * scale * ts[k] ** 2
            assert gap <= 2.0 * big_l * r2 / (k + 1) ** 2 + TOL * scale


def test_strongly_convex_potential_every_iterate():
    """For mu-strongly convex L-smooth f with the constant momentum and s = sqrt(mu / L):
    phi_k = f(x_k) - f* + mu/2 ||z_k - x*||^2 with z_k = x_k + (sqrt(kappa) - 1)(x_k - x_{k-1})
    satisfies phi_{k+1} <= (1 - s) phi_k for every k >= 0 (x_{-1} = x_0)."""
    rng = random.Random(8402)
    for trial in range(200):
        n = rng.randint(1, 6)
        if trial % 2 == 0:
            lam = [rng.uniform(0.1, rng.choice([1.0, 10.0, 1000.0])) for _ in range(n)]
            f, grad, project = quadratic(rng, n, lam)
            mu, big_l = min(lam), max(lam)
            xstar = project([0.0] * n)
        else:
            q = householder([rng.uniform(-1, 1) + (0.1 if i == 0 else 0.0) for i in range(n)])
            av = [rng.uniform(0.5, 3.0) for _ in range(n)]
            bv = [rng.uniform(0.0, 5.0) for _ in range(n)]
            mu, big_l = min(av), max(a + b for a, b in zip(av, bv))

            def f(x, q=q, av=av, bv=bv):
                z = matvec(q, x)
                return sum(a * zi * zi / 2 + b * math.log1p(2.0 * math.sinh(zi / 2) ** 2) for a, b, zi in zip(av, bv, z))

            def grad(x, q=q, av=av, bv=bv, n=n):
                z = matvec(q, x)
                w = [a * zi + b * math.tanh(zi) for a, b, zi in zip(av, bv, z)]
                return [sum(q[t][i] * w[t] for t in range(n)) for i in range(n)]

            xstar = [0.0] * n
        s = math.sqrt(mu / big_l)
        x0 = [rng.uniform(-5, 5) for _ in range(n)]
        path = nesterov_accelerated_gradient(grad, x0, big_l, 300, mu=mu)

        def phi(k):
            prev = path[k - 1] if k > 0 else path[0]
            z = [a + (1.0 / s - 1.0) * (a - b) for a, b in zip(path[k], prev)]
            return f(path[k]) + 0.5 * mu * math.dist(z, xstar) ** 2

        phi0 = phi(0)
        for k in range(len(path) - 1):
            assert phi(k + 1) <= (1.0 - s) * phi(k) + 1e-13 * (1 + phi0)
            assert f(path[k + 1]) <= (1.0 - s) ** (k + 1) * phi0 + 1e-13 * (1 + phi0)


def test_against_lower_bound_function():
    """On Nesterov's worst function in R^(2k+1) from x_0 = 0, the gap after k steps lies between
    the lower bound 3 L R^2 / (32 (k + 1)^2) and the upper bound 2 L R^2 / (k + 1)^2."""
    big_l = 1.0
    for k in (1, 2, 5, 10, 25, 50):
        p = 2 * k + 1

        def f(x):
            s = x[0] ** 2 + sum((x[i] - x[i + 1]) ** 2 for i in range(p - 1)) + x[p - 1] ** 2
            return big_l / 4.0 * (0.5 * s - x[0])

        def grad(x):
            r = []
            for i in range(p):
                a = 2.0 * x[i] - (x[i - 1] if i > 0 else 0.0) - (x[i + 1] if i < p - 1 else 0.0)
                r.append(big_l / 4.0 * a)
            r[0] -= big_l / 4.0
            return r

        xstar = [1.0 - (i + 1) / (p + 1) for i in range(p)]
        fstar = big_l / 8.0 * (-1.0 + 1.0 / (p + 1))
        r2 = dot(xstar, xstar)
        path = nesterov_accelerated_gradient(grad, [0.0] * p, big_l, k)
        gap = f(path[k]) - fstar
        assert 3.0 * big_l * r2 / (32.0 * (k + 1) ** 2) <= gap + TOL
        assert gap <= 2.0 * big_l * r2 / (k + 1) ** 2 + TOL
