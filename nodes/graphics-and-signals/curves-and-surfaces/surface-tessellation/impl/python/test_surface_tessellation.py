# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/surface-tessellation/. The authors are listed in prov/FWMAHV.jsonl.

import math
import random
from fractions import Fraction

from surface_tessellation import (boundary_edges, chordal_bound, consistent_steps,
                                  euler_characteristic, max_deviation, patch_point,
                                  second_derivative_bounds, steps_for_tolerance, tessellate)

G = [Fraction(-1), Fraction(-1, 3), Fraction(1, 3), Fraction(1)]


def push(q, c=Fraction(1, 4), face_c=None):
    """Scale a control point of the cube out by 1 + c per coordinate strictly inside (-1, 1)."""
    k = sum(1 for x in q if abs(x) < 1)
    if k == 2 and face_c is not None:
        return tuple(x * (1 + face_c * 2) for x in q)
    return tuple(x * (1 + c * k) for x in q)


def rounded_cube(bulge_top=None):
    """Six bicubic patches that close up into a rounded cube.

    The face on the axis k with sign sg uses the axes a, b with e_a x e_b = sg e_k,
    so every S_u x S_v points outward. Shared edges have the same control points.
    """
    nets = []
    for k in range(3):
        for sg in (1, -1):
            a, b = (k + 1) % 3, (k + 2) % 3
            if sg < 0:
                a, b = b, a
            net = []
            for i in range(4):
                row = []
                for j in range(4):
                    q = [None] * 3
                    q[k], q[a], q[b] = Fraction(sg), G[i], G[j]
                    top = bulge_top if (k == 2 and sg == 1) else None
                    row.append(push(tuple(q), face_c=top))
                net.append(row)
            nets.append(net)
    return nets


def test_shared_edges_have_equal_control_points():
    nets = rounded_cube()
    keys = {}
    for net in nets:
        m = 3
        for side in ([net[i][0] for i in range(4)], [net[i][m] for i in range(4)],
                     [net[0][j] for j in range(4)], [net[m][j] for j in range(4)]):
            k = min(tuple(side), tuple(reversed(side)))
            keys[k] = keys.get(k, 0) + 1
    assert len(keys) == 12 and set(keys.values()) == {2}     # 12 cube edges, each on 2 patches


def test_uniform_cube_is_watertight():
    nets = rounded_cube()
    for s in (1, 2, 3):
        verts, tris = tessellate(nets, [(s, s)] * 6)
        assert boundary_edges(tris) == []
        assert len(verts) == 6 * s * s + 2 and len(tris) == 12 * s * s
        assert euler_characteristic(verts, tris) == 2


def test_naive_steps_crack_and_consistent_steps_do_not():
    nets = rounded_cube(bulge_top=Fraction(1, 2))
    wanted = [steps_for_tolerance(net, 0.02) for net in nets]
    assert len(set(wanted)) > 1                              # the bulged top wants more steps
    verts, tris = tessellate(nets, wanted)
    assert boundary_edges(tris) != []                        # T-junctions: the mesh has cracks
    fixed = consistent_steps(nets, wanted)
    assert all(f[0] >= w[0] and f[1] >= w[1] for f, w in zip(fixed, wanted))
    verts, tris = tessellate(nets, fixed)
    assert boundary_edges(tris) == []
    assert euler_characteristic(verts, tris) == 2


def test_edge_classes_are_the_three_belts():
    nets = rounded_cube()
    rng = random.Random(301)
    wanted = [(rng.randint(1, 5), rng.randint(1, 5)) for _ in nets]
    fixed = consistent_steps(nets, wanted)
    # every class is a set of 4 parallel cube edges; each axis gets one count
    by_axis = {}
    for p, (su, sv) in enumerate(fixed):
        k = p // 2
        a, b = (k + 1) % 3, (k + 2) % 3
        if p % 2:
            a, b = b, a
        by_axis.setdefault(a, set()).add(su)
        by_axis.setdefault(b, set()).add(sv)
    assert all(len(s) == 1 for s in by_axis.values()) and len(by_axis) == 3
    verts, tris = tessellate(nets, fixed)
    assert boundary_edges(tris) == [] and euler_characteristic(verts, tris) == 2


def random_net(rng, m, n):
    return [[tuple(rng.uniform(-1, 1) + (i if c == 0 else j if c == 1 else 0) for c in range(3))
             for j in range(n + 1)] for i in range(m + 1)]


def test_chordal_bound_holds_against_dense_sampling():
    rng = random.Random(302)
    for _ in range(12):
        net = random_net(rng, rng.randint(1, 4), rng.randint(1, 4))
        su, sv = rng.randint(1, 5), rng.randint(1, 5)
        assert max_deviation(net, su, sv) <= chordal_bound(net, su, sv) + 1e-12


def test_steps_for_tolerance():
    rng = random.Random(303)
    for tol in (0.5, 0.1, 0.03):
        net = random_net(rng, 3, 3)
        su, sv = steps_for_tolerance(net, tol)
        assert chordal_bound(net, su, sv) <= tol
        assert max_deviation(net, su, sv, dense=4) <= tol


def test_bilinear_patch_has_mixed_term_only():
    net = [[(0, 0, 0), (0, 1, 0)], [(1, 0, 0), (1, 1, 1)]]      # z = uv
    assert second_derivative_bounds(net) == (0.0, 1.0, 0.0)
    assert chordal_bound(net, 1, 1) == 0.25
    # on the diagonal u = v of the cell, T = u and S = u^2, so the bound 1/4 is reached at u = 1/2
    assert max_deviation(net, 1, 1, dense=16) == 0.25


def test_exact_vertices_on_a_shared_edge():
    nets = rounded_cube()
    a, b = nets[0], nets[2]                    # the +x face and the +y face share the edge x = y = 1
    pa = {patch_point(a, Fraction(i, 7), Fraction(j, 7)) for i in range(8) for j in range(8)}
    pb = {patch_point(b, Fraction(i, 7), Fraction(j, 7)) for i in range(8) for j in range(8)}
    shared = pa & pb
    assert len(shared) == 8 and all(p[0] == p[1] for p in shared)
