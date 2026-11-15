# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-positively-invariant-set/. The authors are listed in prov/MVMQPG.jsonl.

import itertools
import random
from fractions import Fraction as Fr

import pytest

from ctlmat import mat_power, matvec, mul
from maximal_positively_invariant_set import Infeasible, Unbounded, lp_max, mpi_set, remove_redundant

BOX_F = [[1, 0], [-1, 0], [0, 1], [0, -1]]
BOX_G = [1, 1, 1, 1]
EYE = [[1, 0], [0, 1]]


def rotation(s):
    """s times the rotation with cos = 3/5 and sin = 4/5."""
    return [[s * Fr(3, 5), -s * Fr(4, 5)], [s * Fr(4, 5), s * Fr(3, 5)]]


def inside(rows, b, x, tol=0):
    return all(sum(a * v for a, v in zip(r, x)) <= bi + tol for r, bi in zip(rows, b))


def vertices(rows, b, tol=0):
    out = []
    for i, j in itertools.combinations(range(len(rows)), 2):
        a1, a2 = rows[i], rows[j]
        d = a1[0] * a2[1] - a1[1] * a2[0]
        if d == 0 or abs(d) < 1e-12:
            continue
        x = [(b[i] * a2[1] - b[j] * a1[1]) / d, (a1[0] * b[j] - a2[0] * b[i]) / d]
        if inside(rows, b, x, tol) and x not in out:
            out.append(x)
    return out


def test_lp_against_vertex_enumeration():
    rng = random.Random(7)
    for _ in range(80):
        rows = [[1.0, 0.0], [-1.0, 0.0], [0.0, 1.0], [0.0, -1.0]]
        b = [rng.uniform(0.5, 3.0) for _ in range(4)]
        for _ in range(rng.randint(0, 5)):
            rows.append([rng.uniform(-1, 1), rng.uniform(-1, 1)])
            b.append(rng.uniform(-0.3, 1.5))
        c = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        verts = vertices(rows, b, 1e-9)
        if not verts:
            with pytest.raises(Infeasible):
                lp_max(c, rows, b)
            continue
        want = max(c[0] * v[0] + c[1] * v[1] for v in verts)
        got, x = lp_max(c, rows, b)
        assert abs(got - want) < 1e-7
        assert inside(rows, b, x, 1e-7)


def test_lp_exact_and_unbounded():
    v, x = lp_max([1, 1], [[1, 2], [3, 1], [-1, 0], [0, -1]], [4, 6, 0, 0])
    assert v == Fr(14, 5) and x == [Fr(8, 5), Fr(6, 5)]
    with pytest.raises(Unbounded):
        lp_max([1, 0], [[0, 1]], [1])
    with pytest.raises(Infeasible):
        lp_max([1, 0], [[1, 0], [-1, 0]], [-1, -1])


def test_exact_octagon_for_s_nine_tenths():
    A = rotation(Fr(9, 10))
    rows, b, t = mpi_set(A, EYE, BOX_F, BOX_G)
    assert t == 1
    r2, b2 = remove_redundant(rows, b)
    assert len(r2) == 8
    verts = vertices(r2, b2)
    want = [(-1, Fr(-14, 27)), (Fr(-23, 36), -1), (Fr(14, 27), -1), (1, Fr(-23, 36)),
            (1, Fr(14, 27)), (Fr(23, 36), 1), (Fr(-14, 27), 1), (-1, Fr(23, 36))]
    assert sorted(tuple(v) for v in verts) == sorted(want)
    for v in verts:  # invariance: A v stays in the set, exactly
        assert inside(r2, b2, matvec(A, v))


@pytest.mark.parametrize("s, t_star, facets", [(Fr(19, 20), 2, 12), (Fr(99, 100), 4, 20)])
def test_determinedness_index(s, t_star, facets):
    rows, b, t = mpi_set(rotation(s), EYE, BOX_F, BOX_G)
    assert t == t_star
    r2, _ = remove_redundant(rows, b)
    assert len(r2) == facets


def test_sampling_invariance_and_maximality():
    rng = random.Random(11)
    A = rotation(Fr(19, 20))
    rows, b, t = mpi_set(A, EYE, BOX_F, BOX_G)
    Af = [[float(v) for v in r] for r in A]
    rf = [[float(v) for v in r] for r in rows]
    bf = [float(v) for v in b]
    inner = outer = 0
    for _ in range(400):
        x = [rng.uniform(-1, 1), rng.uniform(-1, 1)]
        if inside(rf, bf, x):
            inner += 1
            y = x
            for _ in range(60):  # stays in the box for all k
                y = matvec(Af, y)
                assert max(abs(v) for v in y) <= 1 + 1e-12
                assert inside(rf, bf, y, 1e-12)
        else:
            outer += 1
            y, left = x, False
            for _ in range(t + 1):  # leaves the box within t* + 1 steps
                y = matvec(Af, y)
                left = left or max(abs(v) for v in y) > 1
            assert left
    assert inner > 50 and outer > 50


def test_lqr_terminal_set_double_integrator():
    K = [0.4344832432759559, 1.0284659329503845]
    AK = [[1.0 - 0.5 * K[0], 1.0 - 0.5 * K[1]], [-K[0], 1.0 - K[1]]]
    C = [[1.0, 0.0], [0.0, 1.0], [-K[0], -K[1]]]
    F = [[1.0, 0, 0], [-1.0, 0, 0], [0, 1.0, 0], [0, -1.0, 0], [0, 0, 1.0], [0, 0, -1.0]]
    rows, b, t = mpi_set(AK, C, F, [5.0] * 4 + [1.0] * 2)
    assert t == 1 and len(rows) == 8
    r2, b2 = remove_redundant(rows, b)
    assert len(r2) == 6
    FCA = mul(mul(F, C), mat_power(AK, 1))
    assert any(max(abs(u - v) for u, v in zip(r, FCA[4])) < 1e-12 for r in r2)
    for v in vertices(r2, b2, 1e-9):
        w = matvec(AK, v)
        assert inside(r2, b2, w, 1e-9)


def test_single_output_with_unbounded_first_set():
    # O_0 = {|x_1| <= 1} is an unbounded strip; observability makes O_1 bounded.
    A = [[Fr(1, 2), 1], [0, Fr(1, 2)]]
    rows, b, t = mpi_set(A, [[1, 0]], [[1], [-1]], [1, 1])
    assert t == 2
    r2, b2 = remove_redundant(rows, b)
    assert len(r2) == 6
    verts = vertices(r2, b2)
    want = [(-1, Fr(-1, 2)), (0, -1), (1, Fr(-5, 4)), (1, Fr(1, 2)), (0, 1), (-1, Fr(5, 4))]
    assert sorted(tuple(v) for v in verts) == sorted(want)
    for v in verts:
        assert inside(r2, b2, matvec(A, v))


def test_not_finitely_determined_without_schur():
    with pytest.raises(RuntimeError):
        mpi_set(rotation(1.0), EYE, [[float(a) for a in r] for r in BOX_F], [1.0] * 4, kmax=15)
