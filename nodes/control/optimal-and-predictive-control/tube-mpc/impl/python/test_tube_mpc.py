# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tube-mpc/. The authors are listed in prov/ZNT0ZQ.jsonl.

import itertools
import random
from fractions import Fraction as Fr

import pytest

from tube_mpc import closed_loop, lp_min, rpi_outer, support, tighten, tube_mpc, zonotope_rows

# The example of the page: a double integrator with a deadbeat ancillary gain.
A = [[1, 1], [0, 1]]
B = [[Fr(1, 2)], [1]]
K = [[-1, Fr(-3, 2)]]
W = [[Fr(1, 10), 0], [0, Fr(1, 10)]]
X = [([1, 0], 5), ([-1, 0], 5), ([0, 1], 1), ([0, -1], 1)]
U = [([1], 1), ([-1], 1)]
Q = [[1, 0], [0, 1]]
R = [[1]]


def closed(Kg):
    return [[A[i][j] + B[i][0] * Kg[0][j] for j in range(2)] for i in range(2)]


def inside(rows, p, tol=0):
    return all(sum(ci * pi for ci, pi in zip(c, p)) <= b + tol for c, b in rows)


def test_lp_small_cases():
    val, z = lp_min([1, 1], [[-1, -1]], [-1], [[1, -1]], [Fr(1, 3)], tol=0)
    assert val == 1 and z == [Fr(2, 3), Fr(1, 3)]
    assert lp_min([1], [[1], [-1]], [-1, -1], tol=0) is None
    with pytest.raises(ValueError):
        lp_min([1], [[1]], [1], tol=0)


def test_zonotope_rows_and_support():
    rng = random.Random(3)
    for n in (2, 3):
        for _ in range(4):
            gens = [[Fr(rng.randint(-5, 5), 4) for _ in range(n)] for _ in range(n + 1)]
            rows = zonotope_rows(gens, n)
            verts = [[sum(s * g[i] for s, g in zip(signs, gens)) for i in range(n)]
                     for signs in itertools.product((-1, 1), repeat=len(gens))]
            a = [rng.randint(-3, 3) for _ in range(n)]
            assert support(gens, a) == max(sum(ai * vi for ai, vi in zip(a, v)) for v in verts)
            for _ in range(15):
                p = [Fr(rng.randint(-12, 12), 4) for _ in range(n)]
                # p is in the zonotope iff gens xi = p for some |xi| <= 1.
                k = len(gens)
                Gb = [[1 if j == i else 0 for j in range(k)] for i in range(k)]
                Gb += [[-1 if j == i else 0 for j in range(k)] for i in range(k)]
                Eq = [[g[i] for g in gens] for i in range(n)]
                lp = lp_min([0] * k, Gb, [1] * (2 * k), Eq, p, tol=0)
                assert inside(rows, p) == (lp is not None)


def test_example_sets_are_exact():
    s, alpha, Z = rpi_outer(closed(K), W)
    assert (s, alpha) == (2, 0)
    # A_K is nilpotent, so Z = W + A_K W is the minimal robust positively invariant set.
    assert support(Z, [1, 0]) == Fr(7, 40) and support(Z, [0, 1]) == Fr(1, 4)
    assert [b for _, b in tighten(X, Z)] == [Fr(193, 40)] * 2 + [Fr(3, 4)] * 2
    assert [b for _, b in tighten(U, Z, K)] == [Fr(3, 5)] * 2
    Zrows = zonotope_rows(Z, 2)
    val, z0, vs, zs = tube_mpc(A, B, Z, Zrows, [-3, 0], 6, Q, R, tighten(X, Z), tighten(U, Z, K), tol=0)
    assert val == Fr(51, 4) and z0 == [Fr(-117, 40), Fr(3, 20)] and zs[-1] == [0, 0]
    assert tube_mpc(A, B, Z, Zrows, [-3, 0], 4, Q, R, tighten(X, Z), tighten(U, Z, K), tol=0) is None


def test_rpi_outer_bound_is_invariant():
    rng = random.Random(8)
    for _ in range(5):
        while True:
            M = [[Fr(rng.randint(-8, 8), 10) for _ in range(2)] for _ in range(2)]
            tr, det = M[0][0] + M[1][1], M[0][0] * M[1][1] - M[0][1] * M[1][0]
            if abs(det) < 1 and abs(tr) < 1 + det - Fr(1, 10):  # Jury test: Schur with a margin
                break
        s, alpha, Z = rpi_outer(M, W, Fr(1, 5))
        rows = zonotope_rows(Z, 2)
        # A_K Z + W is inside Z: compare support functions on the facet normals of Z.
        AZ = [[sum(M[i][j] * g[j] for j in range(2)) for i in range(2)] for g in Z]
        assert all(support(AZ + W, c) <= b for c, b in rows)
        # Z contains every partial sum W + A_K W + ... of the minimal invariant set.
        P, Fs = [[1, 0], [0, 1]], []
        for _ in range(25):
            Fs += [[sum(P[i][j] * g[j] for j in range(2)) for i in range(2)] for g in W]
            P = [[sum(M[i][k] * P[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
        assert all(support(Fs, c) <= b for c, b in rows)


def run_case(Kg, alpha_max, seed, steps):
    s, alpha, Z = rpi_outer(closed(Kg), W, alpha_max)
    Zrows = zonotope_rows(Z, 2)
    Xb, Ub = tighten(X, Z), tighten(U, Z, Kg)
    rng = random.Random(seed)
    ws = [[rng.choice([-0.1, 0.1]), rng.choice([-0.1, 0.1])] for _ in range(steps)]
    xs, us, z0s, vals = closed_loop(A, B, Kg, Z, Zrows, [-3.0, 0.0], 8, Q, R, Xb, Ub, ws)
    return Zrows, xs, us, z0s, vals


@pytest.mark.parametrize("Kg, seed", [(K, 1), ([[Fr(-1, 2), -1]], 2)])
def test_constraints_hold_for_vertex_disturbances(Kg, seed):
    Zrows, xs, us, z0s, vals = run_case(Kg, Fr(1, 10), seed, 18)
    for k, (x, u, z0) in enumerate(zip(xs, us, z0s)):
        assert abs(x[0]) <= 5 + 1e-9 and abs(x[1]) <= 1 + 1e-9 and abs(u[0]) <= 1 + 1e-9
        assert inside(Zrows, [x[0] - z0[0], x[1] - z0[1]], 1e-9)
    # The value drops by at least the first stage cost of the nominal plan.
    for k in range(len(vals) - 1):
        z0 = z0s[k]
        v0 = us[k][0] - sum(Kg[0][i] * (xs[k][i] - z0[i]) for i in range(2))
        assert vals[k + 1] <= vals[k] - (abs(z0[0]) + abs(z0[1]) + abs(v0)) + 1e-7
    assert vals[-1] < 1e-9


def test_no_disturbance_reaches_the_origin():
    s, alpha, Z = rpi_outer(closed(K), W)
    Zrows = zonotope_rows(Z, 2)
    xs, us, z0s, vals = closed_loop(A, B, K, Z, Zrows, [-3.0, 0.0], 6, Q, R, tighten(X, Z), tighten(U, Z, K), [[0.0, 0.0]] * 7)
    expect = [51 / 4, 69 / 8, 81 / 16, 19 / 8, 5 / 16, 0, 0]
    assert all(abs(v - e) < 1e-9 for v, e in zip(vals, expect))
    assert all(abs(c) < 1e-9 for x in xs[5:] for c in x)
