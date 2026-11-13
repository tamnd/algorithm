# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/richardson-lucy-deconvolution/. The authors are listed in prov/09YP53.jsonl.

import random
from fractions import Fraction as F

import pytest

from richardson_lucy_deconvolution import (
    blur,
    correlate,
    poisson_log_likelihood,
    richardson_lucy,
    richardson_lucy_step,
)


def random_psf(rng, exact=True):
    ph = rng.choice([1, 3])
    pw = rng.choice([1, 3, 5])
    raw = [[rng.randint(0, 4) for _ in range(pw)] for _ in range(ph)]
    raw[ph // 2][pw // 2] += 1  # keep the sum positive
    total = sum(map(sum, raw))
    if exact:
        return [[F(v, total) for v in row] for row in raw]
    return [[v / total for v in row] for row in raw]


def matrix_em_step(u, d, psf):
    """The EM update u_j <- u_j / c_j * sum_i A_ij d_i / b_i with an explicit matrix A."""
    h, w = len(u), len(u[0])
    n = w * h
    bh, bw = len(psf) // 2, len(psf[0]) // 2
    a = [[F(0)] * n for _ in range(n)]  # a[i][j]: weight of source pixel j in data pixel i
    for y in range(h):
        for x in range(w):
            j = y * w + x
            for jj, prow in enumerate(psf):
                for ii, p in enumerate(prow):
                    yy = (y + jj - bh) % h
                    xx = (x + ii - bw) % w
                    a[yy * w + xx][j] += p
    uf = [u[k // w][k % w] for k in range(n)]
    df = [d[k // w][k % w] for k in range(n)]
    b = [sum(a[i][j] * uf[j] for j in range(n)) for i in range(n)]
    col = [sum(a[i][j] for i in range(n)) for j in range(n)]
    new = []
    for j in range(n):
        s = sum(a[i][j] * df[i] / b[i] for i in range(n) if df[i] != 0)
        new.append(uf[j] * s / col[j])
    return [new[y * w:(y + 1) * w] for y in range(h)]


def test_page_example():
    psf = [[F(1, 4), F(1, 2), F(1, 4)]]
    d = blur([[0, 0, 8, 0, 0, 0]], psf)
    assert d == [[0, 2, 4, 2, 0, 0]]
    u1 = richardson_lucy(d, psf, 1)
    assert u1 == [[F(1, 2), 2, 3, 2, F(1, 2), 0]]
    u2 = richardson_lucy(d, psf, 2)
    assert u2 == [[F(2, 15), F(28, 15), 4, F(28, 15), F(2, 15), 0]]
    u3 = richardson_lucy(d, psf, 3)
    assert u3 == [[F(2, 59), F(1029, 649), F(3090, 649), F(1029, 649), F(2, 59), 0]]
    ls = [poisson_log_likelihood(d, blur(u, psf)) for u in ([[F(4, 3)] * 6], u1, u2, u3)]
    assert ls == sorted(ls)
    uf = richardson_lucy([[0.0, 2.0, 4.0, 2.0, 0.0, 0.0]], [[0.25, 0.5, 0.25]], 10)
    assert [round(v, 4) for v in uf[0]] == [0.0, 0.2863, 7.4274, 0.2863, 0.0, 0.0]


def test_adjoint():
    rng = random.Random(5)
    for _ in range(100):
        h, w = rng.randint(1, 4), rng.randint(1, 4)
        psf = random_psf(rng)
        u = [[F(rng.randint(0, 9)) for _ in range(w)] for _ in range(h)]
        r = [[F(rng.randint(0, 9)) for _ in range(w)] for _ in range(h)]
        lhs = sum(a * b for ra, rb in zip(blur(u, psf), r) for a, b in zip(ra, rb))
        rhs = sum(a * b for ra, rb in zip(u, correlate(r, psf)) for a, b in zip(ra, rb))
        assert lhs == rhs


def test_flux_and_nonnegativity_exact():
    rng = random.Random(11)
    for _ in range(500):
        h, w = rng.randint(1, 3), rng.randint(1, 4)
        psf = random_psf(rng)
        d = [[rng.choice([0, 0, 1, 2, 3, 5, 8]) for _ in range(w)] for _ in range(h)]
        total = sum(map(sum, d))
        if rng.random() < 0.5:
            u = [[F(rng.randint(1, 6), rng.randint(1, 3)) for _ in range(w)] for _ in range(h)]
        else:
            u = richardson_lucy(d, psf, 0)
        for _ in range(3):
            u = richardson_lucy_step(u, d, psf)
            assert all(v >= 0 for row in u for v in row)
            assert sum(map(sum, u)) == total


def test_matches_matrix_em():
    rng = random.Random(23)
    for _ in range(150):
        h, w = rng.randint(1, 3), rng.randint(1, 3)
        psf = random_psf(rng)
        d = [[rng.randint(0, 6) for _ in range(w)] for _ in range(h)]
        u = [[F(rng.randint(1, 5)) for _ in range(w)] for _ in range(h)]
        assert richardson_lucy_step(u, d, psf) == matrix_em_step(u, d, psf)


def test_likelihood_does_not_decrease():
    rng = random.Random(99)
    for _ in range(500):
        h, w = rng.randint(1, 4), rng.randint(1, 5)
        psf = random_psf(rng, exact=False)
        d = [[float(rng.randint(0, 12)) for _ in range(w)] for _ in range(h)]
        u = [[rng.uniform(0.1, 10.0) for _ in range(w)] for _ in range(h)]
        prev = poisson_log_likelihood(d, blur(u, psf))
        for _ in range(6):
            u = richardson_lucy_step(u, d, psf)
            cur = poisson_log_likelihood(d, blur(u, psf))
            assert cur >= prev - 1e-9 * (1 + abs(prev))
            prev = cur


def test_fixed_point_and_zero_pixel():
    rng = random.Random(4)
    for _ in range(100):
        h, w = rng.randint(1, 3), rng.randint(1, 4)
        psf = random_psf(rng)
        ut = [[F(rng.randint(0, 5)) for _ in range(w)] for _ in range(h)]
        d = blur(ut, psf)
        assert richardson_lucy(d, psf, 2, ut) == ut
    psf = [[F(1, 4), F(1, 2), F(1, 4)]]
    d = [[1, 4, 2, 3]]
    u = richardson_lucy(d, psf, 5, [[1, 0, 1, 1]])
    assert u[0][1] == 0
    assert sum(u[0]) == 10


def test_errors():
    psf = [[F(1, 2), F(1, 2)]]
    with pytest.raises(ValueError):
        richardson_lucy([[1, 2]], psf, 1)
    with pytest.raises(ValueError):
        richardson_lucy([[1, 2]], [[F(1, 2)]], 1)
    with pytest.raises(ValueError):
        richardson_lucy([[1, -2]], [[1]], 1)
    with pytest.raises(ValueError):
        richardson_lucy([[1, 2, 3]], [[0, 1, 0]], 1, [[0, 1, 1]])
    assert richardson_lucy([[0, 0]], [[1]], 3) == [[0, 0]]
    assert richardson_lucy([[3, 5]], [[1]], 1) == [[3, 5]]
