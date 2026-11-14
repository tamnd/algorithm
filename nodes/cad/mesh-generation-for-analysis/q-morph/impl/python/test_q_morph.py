# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/q-morph/. The authors are listed in prov/D6Y61V.jsonl.

import random
from fractions import Fraction as F

from mg3geom import boundary_edges, is_valid_planar_mesh, orient2d, segments_cross
from q_morph import flip, qmorph_step, recover_edge, undirected_edges


def grid_mesh(rng, W, H, scramble):
    """A triangle mesh of a jittered W x H grid, with the boundary nodes on the
    rectangle, then `scramble` random flips of convex interior edges."""
    P = []
    for j in range(H + 1):
        for i in range(W + 1):
            x, y = F(i), F(j)
            if 0 < i < W:
                x += F(rng.randint(-25, 25), 100)
            if 0 < j < H:
                y += F(rng.randint(-25, 25), 100)
            P.append((x, y))
    v = lambda i, j: j * (W + 1) + i
    tris = []
    for j in range(H):
        for i in range(W):
            a, b, c, d = v(i, j), v(i + 1, j), v(i + 1, j + 1), v(i, j + 1)
            if rng.random() < 0.5:
                tris += [(a, b, c), (a, c, d)]
            else:
                tris += [(a, b, d), (b, c, d)]
    assert is_valid_planar_mesh(P, tris)
    for _ in range(scramble):
        u, w = rng.choice(sorted(undirected_edges(tris)))
        new = flip(P, tris, u, w)
        if new is not None:
            tris = new
    assert is_valid_planar_mesh(P, tris)
    return P, tris


def area(P, cells):
    return sum(sum(orient2d(P[c[0]], P[c[s]], P[c[s + 1]]) for s in range(1, len(c) - 1)) for c in cells)


def inside_quad(P, q, x):
    return all(orient2d(P[q[s]], P[q[(s + 1) % 4]], x) > 0 for s in range(4))


def check_step(P, tris, a, b):
    quad, rest, flips = qmorph_step(P, tris, a, b)
    if quad is None:
        return None
    assert quad[0] == a and quad[1] == b
    c, d = quad[3], quad[2]
    # the top edge is present after recovery, and recovery is deterministic
    recovered, flips2 = recover_edge(P, list(tris), c, d)
    assert flips2 == flips and (min(c, d), max(c, d)) in undirected_edges(recovered)
    # the merged triangles are exactly those whose centroid is inside the quad (brute force)
    merged = sorted(set(recovered) - set(rest))
    brute = sorted(t for t in recovered
                   if inside_quad(P, quad, tuple(sum(P[k][i] for k in t) / 3 for i in range(2))))
    assert merged == brute and len(merged) + len(rest) == len(recovered)
    # exact area: the quad has the area of the merged triangles, and the total is kept
    assert area(P, [quad]) == area(P, merged) > 0
    assert area(P, rest + [quad]) == area(P, tris)
    # conformity: convex cells, no directed edge twice, the same domain boundary
    assert is_valid_planar_mesh(P, rest + [quad])
    assert set(boundary_edges(rest + [quad])) == set(boundary_edges(tris))
    return flips


def test_step_on_jittered_grids():
    rng = random.Random(1)
    done = 0
    for _ in range(6):
        W, H = rng.randint(3, 6), rng.randint(3, 6)
        P, tris = grid_mesh(rng, W, H, 0)
        for i in range(W):
            if check_step(P, tris, i, i + 1) is not None:
                done += 1
    assert done >= 15


def test_step_on_scrambled_meshes_needs_and_does_recovery():
    rng = random.Random(2)
    done = with_flips = 0
    for _ in range(10):
        W, H = rng.randint(4, 6), rng.randint(4, 6)
        P, tris = grid_mesh(rng, W, H, 300)
        for i in range(W):
            flips = check_step(P, tris, i, i + 1)
            if flips is not None:
                done += 1
                with_flips += flips > 0
    assert done >= 20 and with_flips >= 6


def test_edge_recovery_by_flips():
    rng = random.Random(3)
    recovered_count = 0
    for _ in range(20):
        P, tris = grid_mesh(rng, 5, 5, 200)
        c, d = rng.sample(range(len(P)), 2)
        crossing0 = sum(segments_cross(P[c], P[d], P[u], P[w]) for u, w in undirected_edges(tris))
        out, flips = recover_edge(P, list(tris), c, d)
        if out is None:
            assert flips == "a vertex lies on the top edge"
            continue
        recovered_count += 1
        assert (min(c, d), max(c, d)) in undirected_edges(out)
        assert not any(segments_cross(P[c], P[d], P[u], P[w]) for u, w in undirected_edges(out))
        # a flip removes at most one crossing edge, so at least crossing0 flips are needed
        assert flips >= crossing0
        assert is_valid_planar_mesh(P, out) and area(P, out) == area(P, tris)
        assert set(boundary_edges(out)) == set(boundary_edges(tris))
    assert recovered_count >= 10


def test_failures_are_reported():
    P = [(F(0), F(0)), (F(2), F(0)), (F(1), F(2))]
    quad, why, _ = qmorph_step(P, [(0, 1, 2)], 0, 1)
    assert quad is None and "same vertex" in why
    quad, why, _ = qmorph_step(P, [(0, 1, 2)], 1, 0)
    assert quad is None and "not an edge" in why
    # two triangles that already form a convex quad: no flip, the quad is the union
    P = [(F(0), F(0)), (F(2), F(0)), (F(3), F(1)), (F(-1), F(1))]
    quad, rest, flips = qmorph_step(P, [(0, 1, 3), (1, 2, 3)], 0, 1)
    assert quad == (0, 1, 2, 3) and rest == [] and flips == 0
    # the side edge at b leans over the side edge at a: the quad is not convex
    P = [(F(0), F(0)), (F(2), F(0)), (F(1), F(1)), (F(5, 2), F(3))]
    quad, why, _ = qmorph_step(P, [(0, 1, 2), (1, 3, 2)], 0, 1)
    assert quad is None and "not strictly convex" in why
