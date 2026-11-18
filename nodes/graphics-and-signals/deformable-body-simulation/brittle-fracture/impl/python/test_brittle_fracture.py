# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/brittle-fracture/. The authors are listed in prov/PNJ37X.jsonl.
"""Tests of the O'Brien-Hodgins fracture method on 2D triangle meshes.

The stress split, the forces against central differences of the energy,
the separation tensor (zero at a node of one element, rotation covariant,
along the pull in a stretched strip), the cut of the mesh (valid, area and
energy conserved), and the pulled strip that breaks later for a larger
toughness.
"""

import math
import random

import anim
from brittle_fracture import (Mesh, components, element_forces, fracture_step, grid, separation_tensors,
                              split_node, split_stress, stvk_energy, stvk_stress, sym_eig2)

MU, LAM = 0.384615, 0.576923


def mat_close(a, b, tol):
    return all(abs(a[i][j] - b[i][j]) <= tol for i in range(2) for j in range(2))


def total_forces(mesh):
    f = [[0.0, 0.0] for _ in mesh.x]
    for t, (fe, _) in zip(mesh.tris, element_forces(mesh)):
        for k, a in enumerate(t):
            f[a][0] += fe[k][0]
            f[a][1] += fe[k][1]
    return f


def test_sym_eig2_against_definition():
    rng = random.Random(1)
    for _ in range(500):
        a, b, d = rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2)
        vals, vecs = sym_eig2([[a, b], [b, d]])
        assert vals[0] >= vals[1]
        for lam, n in zip(vals, vecs):
            r = (a * n[0] + b * n[1] - lam * n[0], b * n[0] + d * n[1] - lam * n[1])
            assert math.hypot(*r) < 1e-12
        assert abs(vecs[0][0] * vecs[1][0] + vecs[0][1] * vecs[1][1]) < 1e-15


def test_stress_split():
    rng = random.Random(2)
    for _ in range(500):
        a, b, d = rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2)
        s = [[a, b], [b, d]]
        sp, sm = split_stress(s)
        assert mat_close([[sp[i][j] + sm[i][j] for j in range(2)] for i in range(2)], s, 1e-14)
        assert min(sym_eig2(sp)[0]) >= -1e-12 and max(sym_eig2(sm)[0]) <= 1e-12
        assert mat_close(anim.mul(sp, sm), [[0, 0], [0, 0]], 1e-12)


def test_force_is_minus_gradient_of_stvk_energy():
    rng = random.Random(3)
    rest, tris = grid(2, 2, 1.0, 1.0)
    mesh = Mesh(rest, tris, MU, LAM)
    for _ in range(10):
        mesh.x = [[p[0] + rng.uniform(-0.15, 0.15), p[1] + rng.uniform(-0.15, 0.15)] for p in rest]
        f = total_forces(mesh)
        g = anim.num_grad(lambda z: stvk_energy(mesh, [z[2 * i:2 * i + 2] for i in range(len(z) // 2)]),
                          [c for p in mesh.x for c in p])
        s = max(map(abs, g))
        for a, b in zip([c for p in f for c in p], g):
            assert abs(a + b) <= 1e-6 * s


def test_tensile_force_equals_force_under_pure_tension():
    mesh = Mesh([(0, 0), (1, 0), (0, 1)], [(0, 1, 2)], MU, LAM)
    mesh.x = [[0, 0], [1.2, 0.1], [0.05, 1.1]]
    (f, fp), = element_forces(mesh)
    s = stvk_stress(anim.mul([[1.2, 0.05], [0.1, 1.1]], [[1, 0], [0, 1]]), MU, LAM)
    assert min(sym_eig2(s)[0]) > 0
    for a, b in zip(f, fp):
        assert math.hypot(a[0] - b[0], a[1] - b[1]) < 1e-14


def test_separation_tensor_is_zero_at_a_node_of_one_element():
    rng = random.Random(4)
    mesh = Mesh([(0, 0), (1, 0), (0, 1)], [(0, 1, 2)], MU, LAM)
    for _ in range(50):
        mesh.x = [[p[0] + rng.uniform(-0.3, 0.3), p[1] + rng.uniform(-0.3, 0.3)] for p in mesh.rest]
        for st in separation_tensors(mesh):
            assert mat_close(st, [[0, 0], [0, 0]], 1e-14)


def test_separation_tensor_is_rotation_covariant():
    rng = random.Random(5)
    rest, tris = grid(3, 2, 1.5, 1.0)
    mesh = Mesh(rest, tris, MU, LAM)
    mesh.x = [[p[0] * 1.1 + rng.uniform(-0.05, 0.05), p[1] + rng.uniform(-0.05, 0.05)] for p in rest]
    before = separation_tensors(mesh)
    q = anim.rot2(0.7)
    mesh.x = [list(anim.add(anim.matvec(q, p), (2.0, -1.0))) for p in mesh.x]
    after = separation_tensors(mesh)
    for a, b in zip(before, after):
        assert mat_close(anim.mul(anim.mul(q, a), anim.transpose(q)), b, 1e-12)


def test_stretched_strip_cracks_across_the_pull():
    rest, tris = grid(6, 2, 3.0, 1.0)
    mesh = Mesh(rest, tris, MU, LAM)
    mesh.x = [[1.1 * p[0], p[1]] for p in rest]
    sep = separation_tensors(mesh)
    for a, p in enumerate(rest):
        if 0.0 < p[0] < 3.0:
            vals, vecs = sym_eig2(sep[a])
            assert vals[0] > 0.0 and abs(vecs[0][0]) > 1.0 - 1e-12


def test_uniform_compression_never_breaks_an_interior_node():
    rng = random.Random(7)
    rest, tris = grid(2, 2, 2.0, 2.0)
    mesh = Mesh(rest, tris, MU, LAM)
    for sign in (-1, 1):
        for _ in range(20):
            a, b = 1 + sign * rng.uniform(0.02, 0.2), 1 + sign * rng.uniform(0.02, 0.2)
            q = anim.mul(anim.rot2(rng.uniform(0, 6.3)), anim.mul([[a, 0], [0, b]], anim.rot2(rng.uniform(0, 6.3))))
            mesh.x = [list(anim.matvec(q, p)) for p in rest]
            vals = sym_eig2(stvk_stress(q, MU, LAM))[0]
            sv = sym_eig2(separation_tensors(mesh)[4])[0]
            if sign < 0:
                assert vals[0] < 0 and sv[0] <= 1e-12
            else:
                assert vals[1] > 0 and sv[1] >= -1e-12


def check_valid(mesh, area):
    assert all(v > 0.0 for v in mesh.v0)
    assert abs(sum(mesh.v0) - area) < 1e-12
    count = {}
    for t in mesh.tris:
        for k in range(3):
            e = frozenset((t[k], t[(k + 1) % 3]))
            count[e] = count.get(e, 0) + 1
    assert max(count.values()) <= 2


def test_cut_through_an_interior_node_keeps_the_mesh_valid():
    rng = random.Random(6)
    for trial in range(20):
        rest, tris = grid(2, 2, 1.0, 1.0)
        mesh = Mesh(rest, tris, MU, LAM)
        mesh.x = [[p[0] * 1.05 + rng.uniform(-0.02, 0.02), p[1] + rng.uniform(-0.02, 0.02)] for p in rest]
        mesh.v = [[rng.uniform(-1, 1), rng.uniform(-1, 1)] for _ in rest]
        e0 = stvk_energy(mesh, mesh.x)
        p0 = [sum(m * v[k] for m, v in zip(mesh.mass, mesh.v)) for k in range(2)]
        n0, m0 = len(mesh.x), len(mesh.tris)
        ang = rng.uniform(0.0, math.pi)
        new = split_node(mesh, 4, (math.cos(ang), math.sin(ang)))
        assert new is not None
        check_valid(mesh, 1.0)
        assert abs(stvk_energy(mesh, mesh.x) - e0) < 1e-12
        assert abs(sum(mesh.mass) - 1.0) < 1e-12
        p1 = [sum(m * v[k] for m, v in zip(mesh.mass, mesh.v)) for k in range(2)]
        assert math.hypot(p1[0] - p0[0], p1[1] - p0[1]) < 1e-12
        added = len(mesh.x) - n0
        assert added in (1, 2, 3)
        # each cut edge adds one triangle on each side that has a triangle
        assert added - 1 <= len(mesh.tris) - m0 <= 2 * (added - 1)
        assert any(new in t for t in mesh.tris) and any(4 in t for t in mesh.tris)
        assert not any(new in t and 4 in t for t in mesh.tris)


def test_no_split_when_all_elements_are_on_one_side():
    mesh = Mesh([(0, 0), (1, 0), (0, 1)], [(0, 1, 2)], MU, LAM)
    assert split_node(mesh, 0, (1.0, 1.0)) is None
    assert len(mesh.x) == 3 and len(mesh.tris) == 1


def pulled_strip(tau, steps, stop_at_first=False):
    rest, tris = grid(6, 2, 3.0, 1.0)
    mesh = Mesh(rest, tris, MU, LAM)
    pres = {i: ((-0.05 if p[0] == 0.0 else 0.05), 0.0) for i, p in enumerate(rest) if p[0] in (0.0, 3.0)}
    first = None
    for it in range(steps):
        new = fracture_step(mesh, 0.02, tau, prescribed=pres, damping=0.5)
        if new is not None and first is None:
            first = it
            if stop_at_first:
                return first, None, mesh
        if components(mesh) > 1:
            return first, it, mesh
    return first, None, mesh


def test_pulled_strip_breaks_in_two():
    first, done, mesh = pulled_strip(0.02, 150)
    assert done is not None and first <= done
    check_valid(mesh, 3.0)
    xs = [p[0] for p in mesh.x]
    assert min(xs) < 0.0 and max(xs) > 3.0


def test_larger_toughness_breaks_later():
    times = [pulled_strip(tau, 150, stop_at_first=True)[0] for tau in (0.02, 0.035, 0.05)]
    assert all(t is not None for t in times)
    assert times == sorted(times) and times[0] < times[-1]
    assert pulled_strip(1e6, 150, stop_at_first=True)[0] is None
