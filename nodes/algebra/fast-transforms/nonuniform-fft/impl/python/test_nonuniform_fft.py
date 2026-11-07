# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/nonuniform-fft/. The authors are listed in prov/KGXG3C.jsonl.

import cmath
import math
import random

import pytest

from nonuniform_fft import fft, nufft1, nufft2, parameters

U = 2.0**-53


def e(t):
    return cmath.exp(-2j * math.pi * t)


def direct1(t, c, n, sign=-1):
    return [sum(cj * e(-sign * k * tj) for tj, cj in zip(t, c)) for k in range(n)]


def direct2(t, f, sign=-1):
    return [sum(fk * e(-sign * k * tj) for k, fk in enumerate(f)) for tj in t]


def tol(n, eps, v):
    N = parameters(n, eps)[1]
    return (eps + 256 * (N.bit_length() + 1) * U) * max(sum(abs(z) for z in v), 1e-300)


def err(a, b):
    return max((abs(x - y) for x, y in zip(a, b)), default=0.0)


def rand_c(rng, m):
    return [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(m)]


@pytest.mark.parametrize("eps", [1e-2, 1e-5, 1e-9, 1e-12, 1e-14])
def test_type1_against_direct(eps):
    rng = random.Random(int(-math.log10(eps)))
    for n in (1, 2, 3, 8, 37, 128):
        for m in (1, 5, 60):
            t = [rng.uniform(-2, 2) for _ in range(m)]
            c = rand_c(rng, m)
            assert err(nufft1(t, c, n, eps), direct1(t, c, n)) <= tol(n, eps, c)


@pytest.mark.parametrize("eps", [1e-2, 1e-5, 1e-9, 1e-12, 1e-14])
def test_type2_against_direct(eps):
    rng = random.Random(100 + int(-math.log10(eps)))
    for n in (1, 2, 3, 8, 37, 128):
        for m in (1, 5, 60):
            t = [rng.random() for _ in range(m)]
            f = rand_c(rng, n)
            assert err(nufft2(t, f, eps), direct2(t, f)) <= tol(n, eps, f)


def test_sign_plus():
    rng = random.Random(5)
    t = [rng.random() for _ in range(30)]
    c = rand_c(rng, 30)
    assert err(nufft1(t, c, 20, 1e-10, sign=1), direct1(t, c, 20, sign=1)) <= tol(20, 1e-10, c)
    f = rand_c(rng, 20)
    assert err(nufft2(t, f, 1e-10, sign=1), direct2(t, f, sign=1)) <= tol(20, 1e-10, f)


def test_transpose_identity():
    # sum_k X_k f_k = sum_j c_j y_j, since type 2 is the transpose of type 1
    rng = random.Random(9)
    for n, m in ((16, 40), (33, 7), (1, 3)):
        t = [rng.random() for _ in range(m)]
        c, f = rand_c(rng, m), rand_c(rng, n)
        X, y = nufft1(t, c, n, 1e-12), nufft2(t, f, 1e-12)
        lhs = sum(a * b for a, b in zip(X, f))
        rhs = sum(a * b for a, b in zip(c, y))
        scale = sum(map(abs, c)) * sum(map(abs, f))
        assert abs(lhs - rhs) <= 1e-11 * scale


def test_grid_points_give_dft_and_inverse():
    rng = random.Random(4)
    for n in (1, 2, 4, 6, 16, 50):
        t = [j / n for j in range(n)]
        x = rand_c(rng, n)
        X = nufft1(t, x, n, 1e-12)
        D = [sum(x[j] * e(j * k / n) for j in range(n)) for k in range(n)]
        assert err(X, D) <= tol(n, 1e-12, x)
        back = [v / n for v in nufft2(t, X, 1e-12, sign=1)]
        assert err(back, x) <= tol(n, 1e-12, X) / n + 1e-12


def test_edge_cases():
    assert nufft1([], [], 5) == [0j] * 5
    assert nufft2([], [1, 2, 3]) == []
    # an impulse at a single point
    X = nufft1([0.3], [1.0], 9, 1e-12)
    assert err(X, [e(0.3 * k) for k in range(9)]) <= 2e-12
    # zeros
    assert err(nufft2([0.1, 0.7], [0, 0, 0]), [0, 0]) == 0.0
    # a constant series is constant at every point
    y = nufft2([0.0, 0.123, 0.999, 0.5], [2.5], 1e-12)
    assert err(y, [2.5] * 4) <= 1e-11
    # periodicity of the points
    rng = random.Random(1)
    c = rand_c(rng, 4)
    t = [rng.random() for _ in range(4)]
    assert err(nufft1(t, c, 10), nufft1([v + 3 for v in t], c, 10)) <= 1e-11
    with pytest.raises(ValueError):
        nufft1([0.1], [1.0], 0)
    with pytest.raises(ValueError):
        parameters(4, 0.0)


def test_inner_fft():
    rng = random.Random(2)
    for N in (1, 2, 4, 8, 64):
        a = rand_c(rng, N)
        D = [sum(a[l] * e(l * r / N) for l in range(N)) for r in range(N)]
        assert err(fft(a), D) <= 64 * (N.bit_length() + 1) * U * math.sqrt(N) * sum(map(abs, a))


def test_larger_case():
    rng = random.Random(77)
    n, m = 512, 400
    t = [rng.random() for _ in range(m)]
    c = rand_c(rng, m)
    X = nufft1(t, c, n, 1e-9)
    for k in rng.sample(range(n), 20):
        assert abs(X[k] - sum(cj * e(k * tj) for tj, cj in zip(t, c))) <= tol(n, 1e-9, c)
