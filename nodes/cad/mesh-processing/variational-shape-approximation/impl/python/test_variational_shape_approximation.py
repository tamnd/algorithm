# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/variational-shape-approximation/. The authors are listed in prov/J5DY1Y.jsonl.

import math
import random
from fractions import Fraction

from mx1mesh import box_mesh, dot, exact, face_adjacency, icosphere, norm, scale, to_float, unit
from variational_shape_approximation import coarse_mesh, energy, face_data, fit, flood, vsa


def noisy_sphere(seed, level=2):
    rng = random.Random(seed)
    p, f = icosphere(level)
    return [scale(1 + 0.3 * rng.random(), q) for q in p], f


def test_the_fit_step_gives_the_best_normal() -> None:
    rng = random.Random(7)
    p, f = noisy_sphere(1)
    areas, normals = face_data(p, f)
    label = [0 if normals[t][2] > 0.3 else 1 for t in range(len(f))]
    N = fit(areas, normals, label, [(1.0, 0.0, 0.0), (1.0, 0.0, 0.0)])
    best = energy(areas, normals, label, N)
    for i in (0, 1):  # the closed form 2A - 2|m| of each region
        A = sum(areas[t] for t in range(len(f)) if label[t] == i)
        m = [sum(areas[t] * normals[t][c] for t in range(len(f)) if label[t] == i) for c in range(3)]
        e = sum(areas[t] * norm(tuple(a - b for a, b in zip(normals[t], N[i]))) ** 2 for t in range(len(f)) if label[t] == i)
        assert abs(e - (2 * A - 2 * norm(m))) < 1e-9
    for _ in range(200):
        Q = [unit((rng.gauss(0, 1), rng.gauss(0, 1), rng.gauss(0, 1))) for _ in range(2)]
        assert energy(areas, normals, label, Q) >= best - 1e-12


def test_the_energy_never_increases() -> None:
    for seed in range(4):
        p, f = noisy_sphere(seed)
        _, _, _, h = vsa(p, f, 10)
        assert all(b <= a + 1e-12 for a, b in zip(h, h[1:]))
        assert h[-1] < h[0]


def test_the_guard_is_needed() -> None:
    # without the guard, growing the regions from random seeds can raise the energy
    raised = 0
    for seed in range(3):
        rng = random.Random(seed)
        p, f = noisy_sphere(seed)
        areas, normals = face_data(p, f)
        adj = face_adjacency(f)
        k = 8
        seeds = rng.sample(range(len(f)), k)
        N = [normals[t] for t in seeds]
        label = [max(range(k), key=lambda i: dot(normals[t], N[i])) for t in range(len(f))]
        for i, t in enumerate(seeds):
            label[t] = i
        for _ in range(15):
            N = fit(areas, normals, label, N)
            new = flood(areas, normals, adj, label, N)
            if energy(areas, normals, new, N) > energy(areas, normals, label, N) + 1e-12:
                raised += 1
            label = new
    assert raised > 0


def test_regions_are_connected() -> None:
    p, f = noisy_sphere(5)
    label, N, _, _ = vsa(p, f, 12)
    adj = face_adjacency(f)
    for i in set(label):
        faces = [t for t in range(len(f)) if label[t] == i]
        seen, stack = {faces[0]}, [faces[0]]
        while stack:
            t = stack.pop()
            for u in adj[t]:
                if label[u] == i and u not in seen:
                    seen.add(u)
                    stack.append(u)
        assert len(seen) == len(faces)


def test_a_box_gives_its_six_sides() -> None:
    size = (2, 3, 5)
    for div in ((2, 2, 2), (3, 4, 5)):
        p, f = box_mesh(size, div)
        p = to_float(p)
        label, N, X, h = vsa(p, f, 6)
        assert h[-1] == 0 and len(N) == 6
        axes = sorted(tuple(round(c) for c in n) for n in N)
        assert axes == sorted([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)])
        _, normals = face_data(p, f)
        for t in range(len(f)):
            assert normals[t] == N[label[t]]
        anchors, polygons = coarse_mesh(p, f, label, N, X)
        corners = sorted((sx * size[0] / 2, sy * size[1] / 2, sz * size[2] / 2)
                         for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1))
        assert len(anchors) == 8
        assert all(max(abs(a - b) for a, b in zip(x, y)) < 1e-12 for x, y in zip(sorted(anchors), corners))
        assert len(polygons) == 6
        for i, poly in polygons:
            assert len(poly) == 4
            q = [anchors[a] for a in poly]
            assert all(abs(dot(x, N[i]) - dot(q[0], N[i])) < 1e-12 for x in q)  # one side of the box
            # Newell's normal of the quad points out, along the proxy (exact on the float values)
            nw = [Fraction(0)] * 3
            qe = [exact(x) for x in q]
            for a, b in zip(qe, qe[1:] + qe[:1]):
                nw[0] += (a[1] - b[1]) * (a[2] + b[2])
                nw[1] += (a[2] - b[2]) * (a[0] + b[0])
                nw[2] += (a[0] - b[0]) * (a[1] + b[1])
            assert dot(nw, exact(N[i])) > 0


def test_fewer_than_six_proxies_leave_error_on_a_box() -> None:
    p, f = box_mesh((2, 3, 5), (2, 2, 2))
    p = to_float(p)
    for k in range(1, 6):
        label, N, _, h = vsa(p, f, k)
        assert len(set(label)) == k and h[-1] > 0
    assert math.isclose(vsa(p, f, 1)[3][-1], 2 * 62)  # one proxy on a closed surface: m = 0, energy 2A
