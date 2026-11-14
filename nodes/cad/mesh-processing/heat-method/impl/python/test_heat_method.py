# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heat-method/. The authors are listed in prov/MWDDTN.jsonl.

import heapq
import random
from math import acos

from heat_method import divergence, face_gradients, heat_method, solve_pinned
from mp2mesh import dot, edges, grid_mesh, icosphere, mat_vec, norm, stiffness_matrix, sub


def mean_error(d, exact):
    return sum(abs(a - b) for a, b in zip(d, exact)) / len(d)


def great_circle(points, s):
    return [acos(max(-1.0, min(1.0, dot(q, points[s])))) for q in points]


# ---- reference: Dijkstra on the edge graph, an upper bound on the true distance ----


def edge_dijkstra(points, faces, s):
    adj = {i: [] for i in range(len(points))}
    for i, j in edges(faces):
        w = norm(sub(points[i], points[j]))
        adj[i].append((j, w))
        adj[j].append((i, w))
    dist = [float("inf")] * len(points)
    dist[s] = 0.0
    pq = [(0.0, s)]
    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue
        for w, c in adj[v]:
            if d + c < dist[w]:
                dist[w] = d + c
                heapq.heappush(pq, (d + c, w))
    return dist


def test_poisson_step_recovers_a_piecewise_linear_function() -> None:
    rng = random.Random(1)
    for p, f in (icosphere(1), grid_mesh(4, 3, 0.5)):
        phi0 = [rng.uniform(-1, 1) for _ in p]
        X = face_gradients(p, f, phi0)
        div = divergence(p, f, X)
        Cphi = mat_vec(stiffness_matrix(p, f), phi0)
        assert max(abs(d + c) for d, c in zip(div, Cphi)) < 1e-12      # div of grad phi0 is -C phi0
        phi = solve_pinned(stiffness_matrix(p, f), [-d for d in div], 0, "cg")
        assert max(abs(a - (b - phi0[0])) for a, b in zip(phi, phi0)) < 1e-8


def test_flat_grid_against_euclidean_distance() -> None:
    prev = None
    for m in (4, 8, 16):
        g, gf = grid_mesh(m, m, 1.0 / m)
        d = heat_method(g, gf, [0])
        assert d[0] == 0.0
        err = mean_error(d, [norm(q) for q in g])
        assert prev is None or err < prev                              # measured: 0.033, 0.021, 0.014
        prev = err
    assert prev < 0.02


def test_symmetry_of_the_grid() -> None:
    m = 8
    g, gf = grid_mesh(m, m, 1.0 / m)
    d = heat_method(g, gf, [0])
    for i in range(m + 1):
        for j in range(m + 1):
            assert abs(d[j * (m + 1) + i] - d[i * (m + 1) + j]) < 1e-9


def test_better_than_edge_dijkstra_on_a_grid() -> None:
    m = 8
    g, gf = grid_mesh(m, m, 1.0 / m)
    exact = [norm(q) for q in g]
    heat = mean_error(heat_method(g, gf, [0]), exact)
    graph = edge_dijkstra(g, gf, 0)
    assert all(a >= b - 1e-12 for a, b in zip(graph, exact))         # graph paths are never shorter
    assert heat < mean_error(graph, exact)


def test_sphere_against_great_circle_distance() -> None:
    prev = None
    for level in (1, 2, 3):
        s, sf = icosphere(level)
        err = mean_error(heat_method(s, sf, [0]), great_circle(s, 0))
        assert prev is None or err < prev                              # measured: 0.096, 0.045, 0.023
        prev = err
    assert prev < 0.03


def test_two_sources() -> None:
    m = 8
    g, gf = grid_mesh(m, m, 1.0 / m)
    a, b = 0, (m + 1) * (m + 1) - 1
    d = heat_method(g, gf, [a, b])
    exact = [min(norm(sub(q, g[a])), norm(sub(q, g[b]))) for q in g]
    assert min(d[a], d[b]) == 0.0
    assert mean_error(d, exact) < 0.03


def test_cg_against_dense_solver() -> None:
    s, sf = icosphere(1)
    for src in ([0], [0, 5], [3, 17, 30]):
        a = heat_method(s, sf, src)
        b = heat_method(s, sf, src, solver="dense")
        assert max(abs(x - y) for x, y in zip(a, b)) < 1e-9
