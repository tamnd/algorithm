# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/laplacian-surface-editing/. The authors are listed in prov/44KQTR.jsonl.

import math
import random
from fractions import Fraction

import pytest

from laplacian_surface_editing import energy, laplacian_edit, neighbours, similarity_rows
from mx1mesh import add, dot, mat_vec, norm, rotation_matrix, sub, to_float


def patch(m, amp=Fraction(1, 2)):
    """The grid of (m + 1)^2 points on [-1, 1]^2 with the bump z = amp (1 - x^2)(1 - y^2), cut into triangles."""
    p = []
    for a in range(m + 1):
        for b in range(m + 1):
            x, y = Fraction(2 * a, m) - 1, Fraction(2 * b, m) - 1
            p.append((x, y, amp * (1 - x * x) * (1 - y * y)))
    f = []
    for a in range(m):
        for b in range(m):
            i = a * (m + 1) + b
            f += [(i, i + m + 1, i + m + 2), (i, i + m + 2, i + 1)]
    return p, f


def border(m):
    return [a * (m + 1) + b for a in range(m + 1) for b in range(m + 1) if a in (0, m) or b in (0, m)]


@pytest.mark.parametrize("m, rotations", [(4, False), (3, True)])
def test_the_unconstrained_solve_returns_the_input(m, rotations) -> None:
    p, f = patch(m)
    corners = {k: p[k] for k in (0, m, (m + 1) * m)}  # handles left at their rest positions
    assert laplacian_edit(p, f, corners, rotations=rotations) == p  # exact, with Fraction
    p, f = patch(8)
    p = to_float(p)
    q = laplacian_edit(p, f, {k: p[k] for k in (0, 8, 72)}, rotations=rotations)  # the same in floating point
    assert max(norm(sub(a, b)) for a, b in zip(q, p)) < 1e-12


def test_without_a_handle_the_solution_is_not_unique() -> None:
    p, f = patch(3)
    with pytest.raises(ValueError):  # q and q + t give the same Laplacian coordinates
        laplacian_edit(p, f, {})


@pytest.mark.parametrize("rotations", [False, True])
def test_a_translation_of_the_handles_moves_the_whole_mesh(rotations) -> None:
    p, f = patch(3)
    t = (Fraction(3, 10), Fraction(-1, 5), Fraction(1))
    handles = {k: add(p[k], t) for k in (0, 3, 12)}
    assert laplacian_edit(p, f, handles, rotations=rotations) == [add(x, t) for x in p]


def test_the_similarity_of_the_rest_ring_is_the_identity() -> None:
    p, f = patch(3)
    nb = neighbours(len(p), f)
    for i in range(len(p)):
        S = similarity_rows(p, i, nb[i])
        for q, expect in ((p, (1, 0, 0, 0)), ([add(x, (5, -1, 2)) for x in p], (1, 0, 0, 0)),
                          ([tuple(2 * c for c in x) for x in p], (2, 0, 0, 0))):
            assert tuple(sum(g * q[j][c] for (j, c), g in row.items()) for row in S) == expect


@pytest.mark.parametrize("rotations", [False, True])
def test_the_solve_is_a_least_squares_minimum(rotations) -> None:
    rng = random.Random(7)
    p, f = patch(6)
    p = to_float(p)
    R = rotation_matrix((1, 0, 0), 0.5)
    handles = {k: tuple(mat_vec(R, p[k])) for k in border(6)}
    q = laplacian_edit(p, f, handles, rotations=rotations)
    e = energy(p, f, q, handles, rotations=rotations)
    for _ in range(10):
        q2 = [tuple(x + rng.gauss(0, 1e-3) for x in v) for v in q]
        assert energy(p, f, q2, handles, rotations=rotations) >= e - 1e-12


def test_rotations_keep_the_detail() -> None:
    m = 8
    p, f = patch(m)
    p = to_float(p)
    centre = (m // 2) * (m + 1) + m // 2
    errors = {}
    for th in (0.1, 0.5, math.pi / 2):
        R = rotation_matrix((1, 0, 0), th)
        handles = {k: tuple(mat_vec(R, p[k])) for k in border(m)}
        target = [tuple(mat_vec(R, x)) for x in p]
        for rotations in (False, True):
            q = laplacian_edit(p, f, handles, rotations=rotations)
            errors[th, rotations] = max(norm(sub(a, b)) for k, (a, b) in enumerate(zip(q, target)) if k not in handles)
            if th == math.pi / 2:  # height of the bump along the turned normal: 0.5 at rest
                h = dot(q[centre], mat_vec(R, (0, 0, 1)))
                assert (abs(h) < 1e-9) if not rotations else (abs(h - 0.5) < 1e-3)
    assert errors[0.1, True] < 0.002 < 0.04 < errors[0.1, False]
    assert errors[0.5, True] < 0.04 < 0.2 < errors[0.5, False]
    assert errors[math.pi / 2, True] < errors[math.pi / 2, False]
