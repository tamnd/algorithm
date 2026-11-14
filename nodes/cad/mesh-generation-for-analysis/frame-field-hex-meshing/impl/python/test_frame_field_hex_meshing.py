# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-field-hex-meshing/. The authors are listed in prov/WR7B7E.jsonl.

import math
import random
from itertools import product

from frame_field_hex_meshing import (
    OCTA,
    axis_rotation,
    closest_rotation,
    det,
    edge_energy,
    field_energy,
    frame_sweep,
    horn_matrix,
    inner,
    jacobi_eigen,
    mat_mul,
    quat_to_matrix,
    transpose,
)

EYE = [[1.0 if a == b else 0.0 for b in range(3)] for a in range(3)]


def random_rotation(rng):
    q = [rng.gauss(0, 1) for _ in range(4)]
    n = math.sqrt(sum(x * x for x in q))
    return quat_to_matrix([x / n for x in q])


def small_rotation(rng, eps):
    axis = [rng.gauss(0, 1) for _ in range(3)]
    n = math.sqrt(sum(x * x for x in axis))
    half = eps / 2
    return quat_to_matrix([math.cos(half)] + [math.sin(half) * x / n for x in axis])


def close(a, b, tol=1e-9):
    return all(abs(a[i][j] - b[i][j]) < tol for i in range(3) for j in range(3))


def grid(n, interior):
    frames = {c: [row[:] for row in EYE] for c in product(range(n), repeat=3)}
    free = [c for c in sorted(frames) if all(0 < c[t] < n - 1 for t in range(3))]
    for c, r in zip(free, interior):
        frames[c] = r
    return frames, free


def test_octahedral_group():
    assert len(OCTA) == 24
    keys = {tuple(map(tuple, g)) for g in OCTA}
    assert len(keys) == 24 and tuple(map(tuple, EYE)) in keys
    for g in OCTA:
        assert det(g) == 1 and close(mat_mul(transpose(g), g), EYE)
        for h in OCTA:
            assert tuple(map(tuple, mat_mul(g, h))) in keys


def test_page_example():
    for deg, before, turn in ((30, 24 - 12 * math.sqrt(3), 0), (45, 24 - 12 * math.sqrt(2), 0), (60, 24 - 12 * math.sqrt(3), 90)):
        frames, free = grid(3, [axis_rotation(2, math.radians(deg))])
        assert free == [(1, 1, 1)]
        assert abs(field_energy(frames) - before) < 1e-9
        frame_sweep(frames, free)
        assert abs(field_energy(frames)) < 1e-9
        assert close(frames[(1, 1, 1)], axis_rotation(2, math.radians(turn)))


def test_edge_energy_against_brute_force_and_symmetry():
    rng = random.Random(24)
    for _ in range(100):
        a, b = random_rotation(rng), random_rotation(rng)
        brute = min(sum((a[i][j] - mat_mul(b, g)[i][j]) ** 2 for i in range(3) for j in range(3)) for g in OCTA)
        assert abs(edge_energy(a, b) - brute) < 1e-9
        g, h = rng.choice(OCTA), rng.choice(OCTA)
        assert abs(edge_energy(mat_mul(a, g), mat_mul(b, h)) - brute) < 1e-9
        assert abs(edge_energy(b, a) - brute) < 1e-9


def test_closest_rotation_random():
    rng = random.Random(1987)
    for trial in range(500):
        if trial % 3 == 0:
            m = [[rng.gauss(0, 1) for _ in range(3)] for _ in range(3)]
        else:
            m = [[0.0] * 3 for _ in range(3)]
            for _ in range(rng.randint(1, 6)):
                r = random_rotation(rng)
                m = [[m[i][j] + r[i][j] for j in range(3)] for i in range(3)]
        # Horn's matrix gives the trace for every quaternion
        n = horn_matrix(m)
        q = [rng.gauss(0, 1) for _ in range(4)]
        assert abs(sum(q[a] * n[a][b] * q[b] for a in range(4) for b in range(4)) - inner(quat_to_matrix(q), m)) < 1e-9
        # the Jacobi solver gives eigenpairs
        vals, vecs = jacobi_eigen(n)
        for k in range(4):
            v = [vecs[i][k] for i in range(4)]
            nv = [sum(n[i][j] * v[j] for j in range(4)) for i in range(4)]
            assert all(abs(nv[i] - vals[k] * v[i]) < 1e-9 for i in range(4))
        r = closest_rotation(m)
        assert close(mat_mul(transpose(r), r), EYE) and abs(det(r) - 1) < 1e-9
        best = inner(r, m)
        # first order condition: R^T M is symmetric at a maximizer
        s = mat_mul(transpose(r), m)
        assert all(abs(s[i][j] - s[j][i]) < 1e-8 for i in range(3) for j in range(3))
        # brute force: no random rotation and no small turn of R does better
        for _ in range(20):
            assert inner(random_rotation(rng), m) <= best + 1e-9
        for _ in range(6):
            assert inner(mat_mul(r, small_rotation(rng, 1e-3)), m) <= best + 1e-9


def test_closest_rotation_of_a_scaled_rotation():
    rng = random.Random(5)
    for _ in range(50):
        r0 = random_rotation(rng)
        c = rng.uniform(0.1, 10)
        assert close(closest_rotation([[c * x for x in row] for row in r0]), r0, 1e-8)


def test_sweep_decreases_the_energy():
    for seed in range(12):
        rng = random.Random(seed)
        frames, free = grid(4, [random_rotation(rng) for _ in range(8)])
        start = field_energy(frames)
        e = start
        for c in free:
            frame_sweep(frames, [c])
            e_new = field_energy(frames)
            assert e_new <= e + 1e-9
            e = e_new
        assert e < start - 1e-6
        for c in frames:
            r = frames[c]
            assert close(mat_mul(transpose(r), r), EYE) and abs(det(r) - 1) < 1e-9
    # the measured run on the page
    rng = random.Random(0)
    frames, free = grid(4, [random_rotation(rng) for _ in range(8)])
    energies = [field_energy(frames)]
    for _ in range(3):
        frame_sweep(frames, free)
        energies.append(field_energy(frames))
    assert [round(x, 2) for x in energies] == [41.43, 14.23, 0.84, 0.03]
