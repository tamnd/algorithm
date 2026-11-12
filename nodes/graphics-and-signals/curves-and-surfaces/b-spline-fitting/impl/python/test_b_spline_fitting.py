# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/b-spline-fitting/. The authors are listed in prov/JDHTCP.jsonl.

import random
from fractions import Fraction as F

import pytest

from b_spline_fitting import averaged_knots, basis_funs, chord_length_parameters, evaluate, find_span, fit


def cox_de_boor(i, p, U, t, n):
    """Reference: the B-spline N_{i,p}(t) from the recursive definition, right-continuous,
    with the last nonempty span closed at the right end U[n+1]."""
    if p == 0:
        if U[i] <= t < U[i + 1]:
            return F(1)
        if t == U[n + 1] and U[i] < U[i + 1] == U[n + 1]:
            return F(1)
        return F(0)
    out = F(0)
    if U[i + p] != U[i]:
        out += (t - U[i]) / (U[i + p] - U[i]) * cox_de_boor(i, p - 1, U, t, n)
    if U[i + p + 1] != U[i + 1]:
        out += (U[i + p + 1] - t) / (U[i + p + 1] - U[i + 1]) * cox_de_boor(i + 1, p - 1, U, t, n)
    return out


def gauss(a, b):
    """Reference: dense Gaussian elimination in exact arithmetic; None when singular."""
    n = len(a)
    m = [row[:] + list(r) for row, r in zip(a, b)]
    w = len(m[0])
    for col in range(n):
        piv = next((r for r in range(col, n) if m[r][col] != 0), None)
        if piv is None:
            return None
        m[col], m[piv] = m[piv], m[col]
        for r in range(n):
            if r != col and m[r][col] != 0:
                f = m[r][col] / m[col][col]
                m[r] = [x - f * y for x, y in zip(m[r], m[col])]
    return [tuple(m[r][c] / m[r][r] for c in range(n, w)) for r in range(n)]


def reference_fit(Q, t, U, p):
    n = len(U) - p - 2
    N = [[cox_de_boor(i, p, U, tk, n) for i in range(n + 1)] for tk in t]
    A = [[sum(N[k][i] * N[k][j] for k in range(len(t))) for j in range(n + 1)] for i in range(n + 1)]
    d = len(Q[0])
    R = [[sum(N[k][i] * Q[k][c] for k in range(len(t))) for c in range(d)] for i in range(n + 1)]
    return gauss(A, R), N


def random_case(rng):
    p = rng.randint(1, 3)
    n = rng.randint(p, p + 4)
    inner = sorted(F(rng.randint(1, 11), 12) for _ in range(n - p))
    # keep multiplicities at most p so the basis stays continuous
    for k in range(len(inner)):
        if inner.count(inner[k]) > p:
            inner[k] = F(rng.randint(1, 11), 12)
    inner.sort()
    U = [F(0)] * (p + 1) + inner + [F(1)] * (p + 1)
    m = rng.randint(n, n + 5)
    t = sorted(F(rng.randint(0, 24), 24) for _ in range(m + 1))
    d = rng.choice([2, 3])
    Q = [tuple(F(rng.randint(-20, 20), rng.randint(1, 3)) for _ in range(d)) for _ in range(m + 1)]
    return Q, t, U, p


def test_basis_matches_recursive_definition():
    rng = random.Random(1)
    for _ in range(500):
        _, t, U, p = random_case(rng)
        n = len(U) - p - 2
        tk = rng.choice(t)
        s = find_span(U, p, n, tk)
        B = basis_funs(s, tk, p, U)
        full = [cox_de_boor(i, p, U, tk, n) for i in range(n + 1)]
        assert sum(full) == 1
        assert [full[s - p + a] for a in range(p + 1)] == B
        assert all(full[i] == 0 for i in range(n + 1) if not s - p <= i <= s)


def test_matches_dense_normal_equations():
    rng = random.Random(2)
    solved = singular = 0
    for _ in range(200):
        Q, t, U, p = random_case(rng)
        want, N = reference_fit(Q, t, U, p)
        if want is None:
            with pytest.raises(ValueError):
                fit(Q, t, U, p)
            singular += 1
            continue
        got = fit(Q, t, U, p)
        assert got == want
        # optimality: the residual is orthogonal to every basis column
        res = [tuple(q - c for q, c in zip(Q[k], evaluate(got, U, p, t[k]))) for k in range(len(t))]
        for i in range(len(got)):
            assert all(sum(N[k][i] * res[k][c] for k in range(len(t))) == 0 for c in range(len(Q[0])))
        solved += 1
    assert solved > 100 and singular > 0


def test_recovers_a_spline_exactly():
    rng = random.Random(3)
    for _ in range(300):
        _, t, U, p = random_case(rng)
        n = len(U) - p - 2
        P = [tuple(F(rng.randint(-9, 9)) for _ in range(2)) for _ in range(n + 1)]
        Q = [evaluate(P, U, p, tk) for tk in t]
        try:
            got = fit(Q, t, U, p)
        except ValueError:
            continue
        assert got == P


def test_float_pipeline():
    pts = [(float(x), float((x - 5) ** 2) / 5) for x in range(11)]
    t = chord_length_parameters(pts)
    U = averaged_knots(t, 4, 3)
    assert len(U) == 4 + 3 + 2 and U[:4] == [0.0] * 4 and U[-4:] == [1.0] * 4
    P = fit(pts, t, U, 3)
    err = max(max(abs(a - b) for a, b in zip(q, evaluate(P, U, 3, tk))) for q, tk in zip(pts, t))
    assert err < 0.2


def test_worked_example():
    # Degree 1, knots 0, 0, 1/2, 1, 1: three hat functions; five sites.
    U = [F(0), F(0), F(1, 2), F(1), F(1)]
    t = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    Q = [(F(0), F(0)), (F(1), F(2)), (F(2), F(2)), (F(3), F(1)), (F(4), F(0))]
    P = fit(Q, t, U, 1)
    assert P == [(F(0), F(12, 35)), (F(2), F(16, 7)), (F(4), F(-2, 35))]
