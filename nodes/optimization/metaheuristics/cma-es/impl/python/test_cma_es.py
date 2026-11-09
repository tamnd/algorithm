# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cma-es/. The authors are listed in prov/BASB19.jsonl.

import math
import random

from cma_es import CMAES, cholesky_ok, cma_es, ellipsoid, jacobi_eigen, rosenbrock, sphere


def test_default_parameters() -> None:
    for n in range(1, 41):
        es = CMAES([0.0] * n, 1.0)
        assert math.isclose(sum(es.w), 1.0)
        assert all(a > b > 0 for a, b in zip(es.w, es.w[1:]))
        assert 1 <= es.mueff <= es.mu
        # c1 + cmu < 1 keeps a positive weight on the old C, which the SPD proof uses.
        assert 0 < es.c1 and 0 < es.cmu and es.c1 + es.cmu < 1
        assert 0 < es.cs < 1 and 0 < es.cc <= 1 and es.ds > 1


def test_jacobi_eigen() -> None:
    a = [[4.0, 1.0, 0.5], [1.0, 3.0, 0.2], [0.5, 0.2, 1.0]]
    vals, b = jacobi_eigen(a)
    for k in range(3):
        v = [b[i][k] for i in range(3)]
        av = [sum(a[i][j] * v[j] for j in range(3)) for i in range(3)]
        assert all(math.isclose(av[i], vals[k] * v[i], abs_tol=1e-12) for i in range(3))
    assert math.isclose(sum(vals), 8.0)


def test_covariance_stays_symmetric_positive_definite() -> None:
    for f, n, seed in ((ellipsoid, 5, 0), (rosenbrock, 4, 1), (sphere, 3, 2)):
        trace = []
        cma_es(f, [0.5] * n, 0.8, 1500, random.Random(seed), trace=trace)
        assert len(trace) > 50
        for _, _, sigma, c in trace:
            assert sigma > 0
            assert all(c[i][j] == c[j][i] for i in range(n) for j in range(n))
            assert cholesky_ok(c)
            assert min(jacobi_eigen(c)[0]) > 0


def test_invariant_under_increasing_transformation() -> None:
    m0 = [0.7, -0.4, 0.3]
    a, b, c = [], [], []
    cma_es(ellipsoid, m0, 0.5, 400, random.Random(5), trace=a)
    cma_es(lambda x: 3 * ellipsoid(x) + 7, m0, 0.5, 400, random.Random(5), trace=b)
    cma_es(lambda x: ellipsoid(x) ** 3, m0, 0.5, 400, random.Random(5), trace=c)
    for ta, tb, tc in zip(a, b, c):
        assert ta[2] == tb[2] == tc[2] and ta[3] == tb[3] == tc[3]


def test_invariant_under_translation() -> None:
    shift = [3.0, -1.0, 2.0]
    g = lambda x: ellipsoid([xi - si for xi, si in zip(x, shift)])
    xa, fa, _ = cma_es(ellipsoid, [0.7, -0.4, 0.3], 0.5, 600, random.Random(6))
    xb, fb, _ = cma_es(g, [3.7, -1.4, 2.3], 0.5, 600, random.Random(6))
    assert all(math.isclose(p + s, q, abs_tol=1e-9) for p, s, q in zip(xa, shift, xb))


def test_fixed_seed_reaches_optimum_and_learns_the_shape() -> None:
    x, fx, evals = cma_es(ellipsoid, [1.0] * 5, 1.0, 20000, random.Random(0), target=1e-10)
    assert fx < 1e-10
    # A rotated ellipse with Hessian eigenvalues 1 along (1, 1) and 100 along (1, -1).
    f = lambda x: (x[0] + x[1]) ** 2 / 2 + 100 * (x[0] - x[1]) ** 2 / 2
    trace = []
    x, fx, evals = cma_es(f, [1.0, 1.0], 0.5, 100000, random.Random(0), target=1e-20, trace=trace)
    assert fx < 1e-20
    vals, b = jacobi_eigen(trace[-1][3])
    k = max(range(2), key=lambda i: vals[i])
    assert max(vals) / min(vals) > 20
    assert abs(abs(b[0][k] + b[1][k]) / math.sqrt(2) - 1) < 0.01  # main axis along (1, 1)
