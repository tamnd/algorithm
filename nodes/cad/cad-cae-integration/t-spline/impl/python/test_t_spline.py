# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-spline/. The authors are listed in prov/80ZTCE.jsonl.

import random
from fractions import Fraction as F

from t_spline import TMesh, blend, evaluate, rank, tensor_basis, to_nurbs_matrix

SV = [F(x) for x in (0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4)]
TV = [F(x) for x in (0, 0, 0, 0, 1, 2, 3, 3, 3, 3)]


def example_mesh():
    """The full grid without the line s = 2, except for the edge t in [1, 2]."""
    mesh = TMesh.full_grid(SV, TV)
    mesh.v -= {(5, j) for j in range(2, 7)}
    mesh.add_v(5, 4, 5)
    return mesh


def all_basis(knots, p, x):
    """Reference: all B-splines of degree p on a clamped knot vector at x."""
    n = len(knots) - p - 1
    if x == knots[-1]:
        return [F(int(i == n - 1)) for i in range(n)]
    N = [F(int(knots[i] <= x < knots[i + 1])) for i in range(len(knots) - 1)]
    for d in range(1, p + 1):
        M = []
        for i in range(len(N) - 1):
            v = F(0)
            if knots[i + d] > knots[i]:
                v += (x - knots[i]) / (knots[i + d] - knots[i]) * N[i]
            if knots[i + d + 1] > knots[i + 1]:
                v += (knots[i + d + 1] - x) / (knots[i + d + 1] - knots[i + 1]) * N[i + 1]
            M.append(v)
        N = M
    return N


def points(rng, k):
    return [(F(rng.randint(0, 400), 100), F(rng.randint(0, 300), 100)) for _ in range(k)]


def test_full_grid_blending_functions_are_the_tensor_b_splines():
    mesh = TMesh.full_grid(SV, TV)
    anchors = mesh.anchors()
    assert len(anchors) == (mesh.m - 3) * (mesh.n - 3) == 42
    for i, j in anchors:
        assert mesh.local_index_vectors(i, j) == (list(range(i - 2, i + 3)), list(range(j - 2, j + 3)))
    rng = random.Random(1)
    for s, t in points(rng, 25):
        Bs, Bt = all_basis(SV, 3, s), all_basis(TV, 3, t)
        for i, j in anchors:
            assert blend(mesh, (i, j), s, t) == Bs[i - 2] * Bt[j - 2]


def test_full_grid_surface_is_the_nurbs_surface():
    mesh = TMesh.full_grid(SV, TV)
    rng = random.Random(2)
    P = {A: (F(rng.randint(-9, 9)), F(rng.randint(-9, 9)), F(rng.randint(-9, 9))) for A in mesh.anchors()}
    w = {A: F(rng.randint(1, 5), rng.randint(1, 3)) for A in mesh.anchors()}
    for s, t in points(rng, 15):
        Bs, Bt = all_basis(SV, 3, s), all_basis(TV, 3, t)
        num = [F(0)] * 3
        den = F(0)
        for i, j in mesh.anchors():
            b = w[i, j] * Bs[i - 2] * Bt[j - 2]
            den += b
            num = [x + b * y for x, y in zip(num, P[i, j])]
        assert evaluate(mesh, P, w, s, t) == tuple(x / den for x in num)
    anchors, M = to_nurbs_matrix(mesh)
    nt = mesh.n - 3
    for c, (i, j) in enumerate(anchors):
        assert [M[r][c] for r in range(42)] == [F(r == (i - 2) * nt + (j - 2)) for r in range(42)]


def test_local_knot_vectors_by_ray_casting():
    mesh = example_mesh()
    assert len(mesh.anchors()) == 40 and (5, 3) not in mesh.anchors() and (5, 6) not in mesh.anchors()
    expect = {
        (4, 4): ([0, 0, 1, 2, 3], [0, 0, 1, 2, 3]),  # the ray at t = 1 meets s = 2
        (4, 3): ([0, 0, 1, 3, 4], [0, 0, 0, 1, 2]),  # the ray at t = 0 does not
        (6, 6): ([0, 1, 3, 4, 4], [1, 2, 3, 3, 3]),
        (5, 4): ([0, 1, 2, 3, 4], [0, 0, 1, 2, 3]),
    }
    for A, (s, t) in expect.items():
        assert mesh.local_knots(*A) == ([F(x) for x in s], [F(x) for x in t])


def test_blending_functions_equal_their_tensor_expansion():
    mesh = example_mesh()
    anchors, M = to_nurbs_matrix(mesh)
    nt = mesh.n - 3
    rng = random.Random(3)
    for s, t in points(rng, 12):
        N = [tensor_basis(mesh, r // nt, r % nt, s, t) for r in range(len(M))]
        for c, A in enumerate(anchors):
            assert blend(mesh, A, s, t) == sum(M[r][c] * N[r] for r in range(len(M)))
    assert rank(M) == len(anchors)  # linearly independent


def test_partition_of_unity_and_linear_precision_on_the_example():
    mesh = example_mesh()
    anchors = mesh.anchors()
    centre = {A: [sum(k[1:4]) / 3 for k in mesh.local_knots(*A)] for A in anchors}
    rng = random.Random(4)
    for s, t in points(rng, 20) + [(F(2), F(3, 2)), (F(4), F(3))]:
        T = {A: blend(mesh, A, s, t) for A in anchors}
        assert sum(T.values()) == 1
        assert sum(centre[A][0] * T[A] for A in anchors) == s
        assert sum(centre[A][1] * T[A] for A in anchors) == t
        assert all(x >= 0 for x in T.values())


def test_each_blending_function_is_nonzero_only_inside_its_local_box():
    mesh = example_mesh()
    rng = random.Random(5)
    for A in mesh.anchors():
        sk, tk = mesh.local_knots(*A)
        for s, t in points(rng, 6):
            if not (sk[0] <= s <= sk[-1] and tk[0] <= t <= tk[-1]):
                assert blend(mesh, A, s, t) == 0
