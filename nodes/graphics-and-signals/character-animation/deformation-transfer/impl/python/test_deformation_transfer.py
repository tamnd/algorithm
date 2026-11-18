# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deformation-transfer/. The authors are listed in prov/CM6PX4.jsonl.
"""Tests of deformation transfer.

The identity deformation gives the target rest mesh. A similarity motion of
the source moves the target by the same similarity. Transfer onto the source
itself gives the deformed source. The solution has a zero gradient of the
energy and beats random perturbations. The fourth vertex moves exactly under
a similarity. The check value of the page holds.
"""

import math
import random

import anim
from deformation_transfer import (
    apply_affine,
    energy,
    fourth_vertex,
    source_deformations,
    transfer,
)


def grid(f):
    verts = [(float(x), float(y), f(x, y)) for y in range(3) for x in range(3)]
    tris = []
    for y in range(2):
        for x in range(2):
            a = 3 * y + x
            tris.append((a, a + 1, a + 4))
            tris.append((a, a + 4, a + 3))
    return verts, tris


SRC, TRIS = grid(lambda x, y: 0.2 * x * y)
TGT, _ = grid(lambda x, y: 0.3 * math.sin(x) - 0.1 * y * y)
TGT = [(1.5 * x, 0.8 * y, z) for x, y, z in TGT]
PAIRS = [(t, t) for t in range(len(TRIS))]


def bend(verts):
    out = []
    c, s = math.cos(0.6), math.sin(0.6)
    for x, y, z in verts:
        if x > 1.0:
            dx = x - 1.0
            out.append((1.0 + c * dx - s * z, y, s * dx + c * z))
        else:
            out.append((x, y, z))
    return out


def rot(rng):
    q = anim.q_normalize([rng.gauss(0, 1) for _ in range(4)])
    return anim.q_to_mat3(q)


def close(a, b, tol):
    return all(abs(x - y) <= tol for p, q in zip(a, b) for x, y in zip(p, q))


def test_identity_gives_the_target_rest_mesh():
    s = source_deformations(SRC, SRC, TRIS)
    out, _ = transfer(TGT, TRIS, PAIRS, s, (0, TGT[0]))
    assert close(out, TGT, 1e-9)


def test_similarity_transfers_exactly():
    rng = random.Random(1)
    r = rot(rng)
    m = [[1.7 * x for x in row] for row in r]
    t = (0.3, -1.0, 2.0)
    s = source_deformations(SRC, [apply_affine(m, t, p) for p in SRC], TRIS)
    out, _ = transfer(TGT, TRIS, PAIRS, s, (4, apply_affine(m, t, TGT[4])))
    assert close(out, [apply_affine(m, t, p) for p in TGT], 1e-9)


def test_fourth_vertex_follows_a_similarity():
    rng = random.Random(2)
    r = rot(rng)
    m = [[0.6 * x for x in row] for row in r]
    t = (1.0, 2.0, 3.0)
    a, b, c = SRC[0], SRC[1], SRC[4]
    moved = fourth_vertex(apply_affine(m, t, a), apply_affine(m, t, b), apply_affine(m, t, c))
    assert close([moved], [apply_affine(m, t, fourth_vertex(a, b, c))], 1e-12)


def test_self_transfer_gives_the_deformed_source():
    d = bend(SRC)
    s = source_deformations(SRC, d, TRIS)
    out, _ = transfer(SRC, TRIS, PAIRS, s, (0, d[0]))
    assert close(out, d, 1e-9)


def test_solution_is_a_minimum():
    d = bend(SRC)
    s = source_deformations(SRC, d, TRIS)
    out, fourth = transfer(TGT, TRIS, PAIRS, s, (0, TGT[0]))
    e0 = energy(TGT, TRIS, PAIRS, s, out, fourth)
    flat = [c for p in out[1:] + fourth for c in p]

    def f(x):
        vs = [out[0]] + [tuple(x[3 * i : 3 * i + 3]) for i in range(len(out) - 1)]
        k = 3 * (len(out) - 1)
        fo = [tuple(x[k + 3 * i : k + 3 * i + 3]) for i in range(len(fourth))]
        return energy(TGT, TRIS, PAIRS, s, vs, fo)

    g = anim.num_grad(f, flat)
    assert max(abs(x) for x in g) < 1e-6
    rng = random.Random(3)
    for _ in range(30):
        assert f([x + rng.gauss(0, 0.01) for x in flat]) >= e0


def test_many_to_many_duplicates_do_not_change_the_result():
    d = bend(SRC)
    s = source_deformations(SRC, d, TRIS)
    a, _ = transfer(TGT, TRIS, PAIRS, s, (0, TGT[0]))
    b, _ = transfer(TGT, TRIS, PAIRS + PAIRS, s, (0, TGT[0]))
    assert close(a, b, 1e-9)


def test_check_value_of_the_page():
    src = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    dst = [(0.0, 0.0, 0.0), (1.0, 0.0, 0.0), (0.5, 1.0, 0.0)]
    s = source_deformations(src, dst, [(0, 1, 2)])
    want = [[1.0, 0.5, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    assert all(abs(s[0][i][j] - want[i][j]) < 1e-12 for i in range(3) for j in range(3))
    tgt = [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    v4 = fourth_vertex(*tgt)
    assert abs(v4[2] - math.sqrt(2.0)) < 1e-12
    out, fourth = transfer(tgt, [(0, 1, 2)], [(0, 0)], s, (0, tgt[0]))
    assert close(out, [(0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.5, 1.0, 0.0)], 1e-12)
    assert close(fourth, [(0.0, 0.0, math.sqrt(2.0))], 1e-12)
