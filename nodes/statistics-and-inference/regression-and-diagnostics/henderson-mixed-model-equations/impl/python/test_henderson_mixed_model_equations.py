# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/henderson-mixed-model-equations/. The authors are listed in prov/3AX196.jsonl.

import random
from fractions import Fraction as Fr

import pytest

from henderson_mixed_model_equations import (
    matmul, mixed_model_equations, mme_inverse_blocks, one_way_design, transpose,
)


def inverse_gj(a):
    """Gauss-Jordan inverse in exact rational arithmetic (independent of the LDL^T code)."""
    n = len(a)
    m = [[Fr(v) for v in row] + [Fr(int(i == j)) for j in range(n)] for i, row in enumerate(a)]
    for c in range(n):
        piv = next(r for r in range(c, n) if m[r][c] != 0)
        m[c], m[piv] = m[piv], m[c]
        m[c] = [v / m[c][c] for v in m[c]]
        for r in range(n):
            if r != c and m[r][c] != 0:
                f = m[r][c]
                m[r] = [u - f * v for u, v in zip(m[r], m[c])]
    return [row[n:] for row in m]


def add(a, b):
    return [[u + v for u, v in zip(r, s)] for r, s in zip(a, b)]


def random_spd(rng, k):
    """A random symmetric positive definite rational matrix: M M^T + I."""
    m = [[Fr(rng.randint(-2, 2)) for _ in range(k)] for _ in range(k)]
    return add(matmul(m, transpose(m)), [[Fr(int(i == j)) for j in range(k)] for i in range(k)])


def gls_and_blup(x, z, g, r, y):
    """Reference: b = (X^T V^-1 X)^-1 X^T V^-1 y and u = G Z^T V^-1 (y - X b), with V = Z G Z^T + R."""
    v = add(matmul(matmul(z, g), transpose(z)), r)
    vi = inverse_gj(v)
    xt = transpose(x)
    a = matmul(matmul(xt, vi), x)
    ai = inverse_gj(a)
    col = [[v] for v in y]
    b = [row[0] for row in matmul(ai, matmul(matmul(xt, vi), col))]
    resid = [[y[i] - sum(x[i][j] * b[j] for j in range(len(b)))] for i in range(len(y))]
    u = [row[0] for row in matmul(matmul(matmul(g, transpose(z)), vi), resid)]
    return b, u, v, vi, ai


def test_henderson_equals_gls_and_blup_exactly():
    rng = random.Random(20261114)
    for _ in range(12):
        n, p, q = rng.randint(5, 9), rng.randint(1, 3), rng.randint(1, 4)
        x = [[Fr(1)] + [Fr(rng.randint(-3, 3)) for _ in range(p - 1)] for _ in range(n)]
        z = [[Fr(rng.randint(0, 1)) for _ in range(q)] for _ in range(n)]
        g = random_spd(rng, q)
        r = random_spd(rng, n) if rng.random() < 0.5 else [[Fr(rng.randint(1, 4)) if i == j else Fr(0) for j in range(n)] for i in range(n)]
        y = [Fr(rng.randint(-9, 9)) for _ in range(n)]
        try:
            want_b, want_u, v, vi, ai = gls_and_blup(x, z, g, r, y)
        except StopIteration:
            continue  # X^T V^-1 X singular: X has dependent columns
        fit = mixed_model_equations(x, z, g, r, y)
        assert fit.b == want_b
        assert fit.u == want_u
        cb, cu = mme_inverse_blocks(fit, p)
        assert cb == ai
        # C^22 = G - G Z^T P Z G with P = V^-1 - V^-1 X (X^T V^-1 X)^-1 X^T V^-1.
        vix = matmul(vi, x)
        proj = add(vi, [[-t for t in row] for row in matmul(matmul(vix, ai), transpose(vix))])
        gz = matmul(g, transpose(z))
        pev = add(g, [[-t for t in row] for row in matmul(matmul(gz, proj), transpose(gz))])
        assert cu == pev


def test_balanced_one_way_shrinkage():
    groups = [[10, 12, 14], [15, 16, 17], [18, 20, 22]]
    x, z, y = one_way_design([[Fr(v) for v in grp] for grp in groups])
    g = [[Fr(15) if i == j else Fr(0) for j in range(3)] for i in range(3)]
    r = [[Fr(3) if i == j else Fr(0) for j in range(9)] for i in range(9)]
    fit = mixed_model_equations(x, z, g, r, y)
    assert fit.b == [Fr(16)]
    assert fit.u == [Fr(-15, 4), Fr(0), Fr(15, 4)]  # shrinkage 15/16 of the group mean deviations -4, 0, 4


def test_unbalanced_one_way_closed_form():
    groups = [[Fr(v) for v in grp] for grp in ([10, 12, 14], [15, 17], [18, 20, 22, 24])]
    su, se = Fr(15), Fr(3)
    x, z, y = one_way_design(groups)
    g = [[su if i == j else Fr(0) for j in range(3)] for i in range(3)]
    r = [[se if i == j else Fr(0) for j in range(len(y))] for i in range(len(y))]
    fit = mixed_model_equations(x, z, g, r, y)
    w = [len(grp) / (se + len(grp) * su) for grp in groups]
    means = [sum(grp) / len(grp) for grp in groups]
    b = sum(wi * m for wi, m in zip(w, means)) / sum(w)
    assert fit.b == [b]
    assert fit.u == [len(grp) * su / (len(grp) * su + se) * (m - b) for grp, m in zip(groups, means)]


def test_float_input_agrees_with_exact():
    groups = [[10.0, 12.0, 14.0], [15.0, 17.0], [18.0, 20.0, 22.0, 24.0]]
    x, z, y = one_way_design(groups)
    g = [[15.0 if i == j else 0.0 for j in range(3)] for i in range(3)]
    r = [[3.0 if i == j else 0.0 for j in range(len(y))] for i in range(len(y))]
    fit = mixed_model_equations(x, z, g, r, y)
    xf, zf, yf = one_way_design([[Fr(int(v)) for v in grp] for grp in groups])
    exact = mixed_model_equations(xf, zf, [[Fr(int(v)) for v in row] for row in g], [[Fr(int(v)) for v in row] for row in r], yf)
    assert abs(fit.b[0] - float(exact.b[0])) < 1e-12
    assert all(abs(a - float(b)) < 1e-12 for a, b in zip(fit.u, exact.u))


def test_bad_input():
    x, z, y = one_way_design([[1.0, 2.0], [3.0]])
    with pytest.raises(ValueError):
        mixed_model_equations(x, z, [[1.0, 0.0], [0.0, 0.0]], [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)], y)
    with pytest.raises(ValueError):
        mixed_model_equations(x, z, [[1.0, 0.0], [0.0, 1.0]], [[0.0 if i == j else 0.0 for j in range(3)] for i in range(3)], y)
    with pytest.raises(ValueError):
        mixed_model_equations(x, z, [[1.0]], [[1.0 if i == j else 0.0 for j in range(3)] for i in range(3)], y)
