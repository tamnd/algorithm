# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/discrete-cosine-transform/. The authors are listed in prov/C2X14P.jsonl.

import cmath
import math
import random

import pytest

from discrete_cosine_transform import (
    AAN_SCALE, aan_dct8, dct, dct_2d, dct_matrix, fast_dct, fast_idct, idct, idct_2d,
)

TOL = 1e-9


def close(a, b, tol=TOL):
    return max((abs(p - q) for p, q in zip(a, b)), default=0.0) < tol and len(a) == len(b)


def test_worked_example():
    # The example of the page: a smooth row of 8 samples.
    x = [10.0, 11.0, 12.0, 14.0, 15.0, 15.0, 14.0, 12.0]
    c = dct(x)
    want = [36.415999, -3.15889, -3.616262, 1.210129, -0.353553, 0.207237, -0.415512, -0.118547]
    assert close(c, want, 1e-6)
    assert abs(sum(v * v for v in x) - 1351.0) < TOL
    assert abs(sum(v * v for v in c) - 1351.0) < TOL
    # Keeping the first 3 coefficients leaves an error of the energy of the others.
    kept = c[:3] + [0.0] * 5
    approx = idct(kept)
    assert close(approx, [9.655, 10.870, 12.689, 14.237, 14.854, 14.444, 13.496, 12.754], 1e-3)
    err = sum((p - q) ** 2 for p, q in zip(approx, x))
    assert abs(err - sum(v * v for v in c[3:])) < TOL
    assert abs(err - 1.819063) < 1e-6


def test_dc_of_constant_block():
    assert close(dct([5.0] * 8), [5.0 * math.sqrt(8)] + [0.0] * 7)
    assert close(dct([7.0]), [7.0])
    assert dct([]) == [] and idct([]) == []


def test_orthonormal_matrix():
    for n in [1, 2, 3, 5, 8, 16]:
        c = dct_matrix(n)
        for i in range(n):
            for j in range(n):
                s = sum(c[i][k] * c[j][k] for k in range(n))
                assert abs(s - (1.0 if i == j else 0.0)) < 1e-12


def test_inverse_and_fast_against_definition():
    rng = random.Random(9)
    for _ in range(500):
        n = 1 << rng.randint(0, 5)
        x = [rng.uniform(-255, 255) for _ in range(n)]
        c = dct(x)
        assert close(idct(c), x, 1e-9)
        assert close(fast_dct(x), c, 1e-9)
        assert close(fast_idct(c), x, 1e-9)
    for n in [3, 5, 6, 7]:
        x = [rng.uniform(-1, 1) for _ in range(n)]
        assert close(idct(dct(x)), x)
        with pytest.raises(ValueError):
            fast_dct(x)


def test_fast_large():
    rng = random.Random(10)
    x = [rng.uniform(-1, 1) for _ in range(256)]
    assert close(fast_dct(x), dct(x), 1e-10)
    y = [rng.uniform(-1, 1) for _ in range(1024)]
    assert close(fast_idct(fast_dct(y)), y, 1e-10)


def test_dct_from_dft_of_symmetric_extension():
    # X[k] = a_k Re(exp(-i pi k / (2N)) * DFT_2N(x, reversed x)[k]) / 2.
    rng = random.Random(12)
    for n in [1, 4, 6, 8]:
        x = [rng.uniform(-1, 1) for _ in range(n)]
        ext = x + x[::-1]
        dft = [sum(ext[j] * cmath.exp(-2j * math.pi * j * k / (2 * n)) for j in range(2 * n)) for k in range(n)]
        want = [(math.sqrt(1 / n) if k == 0 else math.sqrt(2 / n)) * (cmath.exp(-1j * math.pi * k / (2 * n)) * dft[k]).real / 2 for k in range(n)]
        assert close(dct(x), want)


def test_aan_against_definition():
    rng = random.Random(13)
    for _ in range(500):
        x = [rng.uniform(-128, 127) for _ in range(8)]
        y = aan_dct8(x)
        raw = [sum(x[i] * math.cos((2 * i + 1) * k * math.pi / 16) for i in range(8)) for k in range(8)]
        assert close(y, [AAN_SCALE[k] * raw[k] for k in range(8)], 1e-9)
        # Dividing by the scale gives the orthonormal DCT.
        c = dct(x)
        assert close([y[k] / AAN_SCALE[k] * (math.sqrt(1 / 8) if k == 0 else 0.5) for k in range(8)], c, 1e-9)


def test_jpeg_fdct_formula():
    # ITU-T T.81 A.3.3: S_vu = 1/4 C_u C_v sum_x sum_y s_yx cos((2x+1) u pi/16) cos((2y+1) v pi/16).
    rng = random.Random(14)
    s = [[rng.randint(0, 255) - 128 for _ in range(8)] for _ in range(8)]
    out = dct_2d(s)

    def cc(u):
        return 1 / math.sqrt(2) if u == 0 else 1.0

    for v in range(8):
        for u in range(8):
            want = 0.25 * cc(u) * cc(v) * sum(
                s[y][x] * math.cos((2 * x + 1) * u * math.pi / 16) * math.cos((2 * y + 1) * v * math.pi / 16)
                for x in range(8) for y in range(8))
            assert abs(out[v][u] - want) < 1e-9
    back = idct_2d(out)
    assert all(abs(back[i][j] - s[i][j]) < 1e-9 for i in range(8) for j in range(8))


def jacobi_eigenvectors(a):
    # An independent classical Jacobi solver, used here only as an oracle.
    n = len(a)
    a = [row[:] for row in a]
    v = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for _ in range(2000):
        p, q = max(((i, j) for i in range(n) for j in range(i + 1, n)), key=lambda ij: abs(a[ij[0]][ij[1]]))
        if abs(a[p][q]) < 1e-15:
            break
        th = (a[q][q] - a[p][p]) / (2 * a[p][q])
        t = (1.0 if th >= 0 else -1.0) / (abs(th) + math.sqrt(th * th + 1))
        c = 1 / math.sqrt(t * t + 1)
        s = t * c
        for k in range(n):
            a[k][p], a[k][q] = c * a[k][p] - s * a[k][q], s * a[k][p] + c * a[k][q]
        for k in range(n):
            a[p][k], a[q][k] = c * a[p][k] - s * a[q][k], s * a[p][k] + c * a[q][k]
        for k in range(n):
            v[k][p], v[k][q] = c * v[k][p] - s * v[k][q], s * v[k][p] + c * v[k][q]
    order = sorted(range(n), key=lambda k: -a[k][k])
    return [[v[i][k] for i in range(n)] for k in order]


def test_dct_approaches_klt_of_ar1():
    # Max over k of 1 - |<c_k, v_k>| between the DCT and KLT basis vectors, n = 8.
    c = dct_matrix(8)
    bounds = {0.5: 0.04, 0.9: 0.002, 0.95: 5e-4, 0.99: 2e-5, 0.999: 2e-7}
    last = 1.0
    for rho, bound in bounds.items():
        r = [[rho ** abs(i - j) for j in range(8)] for i in range(8)]
        vecs = jacobi_eigenvectors(r)
        gap = max(1 - abs(sum(vecs[k][i] * c[k][i] for i in range(8))) for k in range(8))
        assert gap < bound
        assert gap < last
        last = gap
