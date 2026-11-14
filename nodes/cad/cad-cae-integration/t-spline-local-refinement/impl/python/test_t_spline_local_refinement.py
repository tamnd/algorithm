# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/t-spline-local-refinement/. The authors are listed in prov/WVHYV3.jsonl.

import random
from fractions import Fraction as F

from t_spline_local_refinement import (
    TMesh,
    blend,
    coupled_weight,
    evaluate,
    face_extensions_and_junctions,
    is_analysis_suitable,
    new_control_points,
    refine,
    refine_vector,
)

HALF = [F(0)] * 4 + [F(k, 2) for k in range(1, 8)] + [F(4)] * 4  # lines 0..14
QUARTER = [F(0)] * 4 + [F(k, 4) for k in range(1, 16)] + [F(4)] * 4  # lines 0..22


def coarse(vals, step):
    """The tensor mesh on the integer knot values; the other lines are not in the mesh."""
    mesh = TMesh(vals, vals)
    m = len(vals) - 1
    lines = [0, 1, 2] + list(range(3, m - 2, step)) + [m - 2, m - 1, m]
    mesh.add_lines(lines, lines)
    return mesh


def global_coefficients(mesh, idx):
    """Reference: the coefficients of a blending function in the tensor B-splines on all lines."""
    s, t = idx
    ds = refine_vector(s, set(range(s[0], s[-1] + 1)) - set(s), mesh.sv)
    dt = refine_vector(t, set(range(t[0], t[-1] + 1)) - set(t), mesh.tv)
    return {(a, b): ca * cb for a, ca in ds.items() for b, cb in dt.items()}


def rank(cols):
    keys = sorted({k for c in cols for k in c})
    A = [[c.get(k, F(0)) for c in cols] for k in keys]
    r = 0
    for c in range(len(cols)):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        for i in range(r + 1, len(A)):
            if A[i][c] != 0:
                f = A[i][c] / A[r][c]
                A[i] = [x - f * y for x, y in zip(A[i], A[r])]
        r += 1
    return r


def face_cross(mesh, i, j):
    """Request to split the face that contains the unit cell (i, j) into four, or None."""
    left = max(k for k in range(0, i + 1) if (k, j) in mesh.v)
    right = min(k for k in range(i + 1, mesh.m + 1) if (k, j) in mesh.v)
    bottom = max(k for k in range(0, j + 1) if (i, k) in mesh.h)
    top = min(k for k in range(j + 1, mesh.n + 1) if (i, k) in mesh.h)
    if right - left < 2 or top - bottom < 2:
        return None
    mi, mj = (left + right) // 2, (bottom + top) // 2
    return [("v", mi, bottom, top), ("h", left, right, mj)]


def check_nested(T1, T2, M):
    old, new = T1.functions(), T2.functions()
    for A, idx in old.items():
        lhs = global_coefficients(T1, idx)
        rhs = {}
        for B, c in M[A].items():
            for k, v in global_coefficients(T2, new[B]).items():
                rhs[k] = rhs.get(k, F(0)) + c * v
        assert {k: v for k, v in rhs.items() if v} == lhs


def random_points(rng, k):
    return [(F(rng.randint(0, 400), 100), F(rng.randint(0, 400), 100)) for _ in range(k)]


def test_one_split_face_needs_two_insertion_edges():
    T1 = coarse(HALF, 2)
    assert is_analysis_suitable(T1) and len(T1.anchors()) == 49
    request = [("v", 6, 5, 7), ("h", 5, 7, 6)]
    T = T1.copy()
    T.add_v(6, 5, 7)
    T.add_h(5, 7, 6)
    assert not is_analysis_suitable(T)  # the extensions meet at the centre (6, 6)
    T2, M, added = refine(T1, request)
    assert added == [((5, 6), (3, 6), "L"), ((7, 6), (9, 6), "R")]
    assert is_analysis_suitable(T2) and len(T2.anchors()) == 56
    assert T1.h <= T2.h and T1.v <= T2.v and T.h <= T2.h and T.v <= T2.v
    check_nested(T1, T2, M)
    row = {B: c for B, c in M[(5, 5)].items()}
    assert row == {(5, 5): F(9, 16), (6, 5): F(3, 8), (5, 6): F(3, 8), (6, 6): F(1, 4)}
    assert sum(1 for A in M if M[A] != {A: 1}) == 16


def test_an_l_junction_is_not_analysis_suitable():
    T = coarse(HALF, 2)
    T.add_v(6, 5, 6)  # from the bottom of the face to its centre
    T.add_h(6, 7, 6)  # from the centre to the right side of the face
    ext = face_extensions_and_junctions(T)
    assert any(J == (6, 6) and d == "U" for J, d, _, _ in ext)
    assert any(J == (6, 6) and d == "L" for J, d, _, _ in ext)
    assert not is_analysis_suitable(T)


def test_analysis_suitable_is_not_enough_for_nesting():
    T1, _, _ = refine(coarse(HALF, 2), [("v", 6, 5, 7), ("h", 5, 7, 6)])
    T2 = T1.copy()
    T2.add_h(0, T2.m, 4)  # a full line through the face extension of (6, 5)
    assert is_analysis_suitable(T2)
    w, _ = coupled_weight(face_extensions_and_junctions(T1), T2)
    assert w > 0  # a loop edge
    new = [global_coefficients(T2, idx) for idx in T2.functions().values()]
    old = global_coefficients(T1, T1.functions()[(6, 5)])
    assert rank(new + [old]) == rank(new) + 1  # the old function is not in the new space
    T3, M, _ = refine(T1, [("h", 0, T1.m, 4)])
    assert is_analysis_suitable(T3)
    check_nested(T1, T3, M)


def test_random_refinements_stay_analysis_suitable_and_nested():
    rng = random.Random(5)
    T = coarse(QUARTER, 4)
    for _ in range(4):
        req = None
        while req is None:
            req = face_cross(T, rng.randint(3, 18), rng.randint(3, 18))
        T2, M, _ = refine(T, req)
        assert is_analysis_suitable(T2)
        assert T.h <= T2.h and T.v <= T2.v
        check_nested(T, T2, M)
        T = T2


def test_refined_surface_is_unchanged_and_basis_sums_to_one():
    rng = random.Random(6)
    T = coarse(QUARTER, 4)
    Q = {A: (F(rng.randint(-20, 20)), F(rng.randint(-20, 20)), F(rng.randint(-20, 20)), F(rng.randint(1, 4))) for A in T.anchors()}
    Q = {A: (x * w, y * w, z * w, w) for A, (x, y, z, w) in Q.items()}  # homogeneous
    pts = random_points(rng, 6) + [(F(1), F(1)), (F(3, 2), F(5, 4)), (F(4), F(4))]
    before = [evaluate(T, Q, s, t) for s, t in pts]
    for _ in range(3):
        req = None
        while req is None:
            req = face_cross(T, rng.randint(3, 18), rng.randint(3, 18))
        T2, M, _ = refine(T, req)
        Q = new_control_points(M, Q)
        assert set(Q) == set(T2.anchors())
        assert [evaluate(T2, Q, s, t) for s, t in pts] == before
        funcs = T2.functions()
        for s, t in pts:
            assert sum(blend(T2, idx, s, t) for idx in funcs.values()) == 1
        T = T2
