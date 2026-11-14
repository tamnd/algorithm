# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/globally-optimal-direction-fields/. The authors are listed in prov/8TE408.jsonl.

import math
import random

from globally_optimal_direction_fields import energy, energy_matrices, face_indices, hermitian_form, smoothest_field
from mx2geom import euler_characteristic

TET_V = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
TET_F = [(0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2)]
OCTA_V = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
OCTA_F = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
PYR_V = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (0, 0, 1)]
PYR_F = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
_T = (1 + 5 ** 0.5) / 2
ICO_V = [(-1, _T, 0), (1, _T, 0), (-1, -_T, 0), (1, -_T, 0), (0, -1, _T), (0, 1, _T),
         (0, -1, -_T), (0, 1, -_T), (_T, 0, -1), (_T, 0, 1), (-_T, 0, -1), (-_T, 0, 1)]
ICO_F = [(0, 11, 5), (0, 5, 1), (0, 1, 7), (0, 7, 10), (0, 10, 11), (1, 5, 9), (5, 11, 4), (11, 10, 2), (10, 7, 6), (7, 1, 8),
         (3, 9, 4), (3, 4, 2), (3, 2, 6), (3, 6, 8), (3, 8, 9), (4, 9, 5), (2, 4, 11), (6, 2, 10), (8, 6, 7), (9, 8, 1)]
CLOSED = [(TET_V, TET_F), (OCTA_V, OCTA_F), (ICO_V, ICO_F)]


def jittered(vertices, seed, amount=0.15):
    rng = random.Random(seed)
    return [tuple(c + rng.uniform(-amount, amount) for c in p) for p in vertices]


def flat_disk(seed):
    """A jittered hexagonal patch of the plane, 19 vertices."""
    rng = random.Random(seed)
    pts, index = [], {}
    for i in range(-2, 3):
        for j in range(-2, 3):
            if abs(i + j) <= 2:
                index[(i, j)] = len(pts)
                pts.append((i + 0.5 * j + rng.uniform(-0.1, 0.1), j * math.sqrt(3) / 2 + rng.uniform(-0.1, 0.1), 0.0))
    faces = []
    for (i, j), v in index.items():
        if (i + 1, j) in index and (i, j + 1) in index:
            faces.append((v, index[(i + 1, j)], index[(i, j + 1)]))
        if (i + 1, j) in index and (i + 1, j - 1) in index:
            faces.append((v, index[(i + 1, j - 1)], index[(i + 1, j)]))
    return pts, faces


def jacobi_eigenvalues(s, sweeps=100):
    """All eigenvalues of a real symmetric matrix by cyclic Jacobi rotations (a slow, independent reference)."""
    a = [row[:] for row in s]
    n = len(a)
    for _ in range(sweeps):
        off = sum(a[p][q] ** 2 for p in range(n) for q in range(n) if p != q)
        if off < 1e-30:
            break
        for p in range(n - 1):
            for q in range(p + 1, n):
                if abs(a[p][q]) < 1e-300:
                    continue
                theta = (a[q][q] - a[p][p]) / (2 * a[p][q])
                t = (1.0 if theta >= 0 else -1.0) / (abs(theta) + math.sqrt(theta * theta + 1))
                c = 1 / math.sqrt(t * t + 1)
                sn = t * c
                for k in range(n):
                    akp, akq = a[k][p], a[k][q]
                    a[k][p], a[k][q] = c * akp - sn * akq, sn * akp + c * akq
                for k in range(n):
                    apk, aqk = a[p][k], a[q][k]
                    a[p][k], a[q][k] = c * apk - sn * aqk, sn * apk + c * aqk
    return sorted(a[i][i] for i in range(n))


def smallest_by_brute_force(a, m):
    """The smallest eigenvalue of A u = lambda M u: the Hermitian M^(-1/2) A M^(-1/2) as a real symmetric 2n matrix."""
    n = len(a)
    b = [[a[p][q] / math.sqrt(m[p] * m[q]) for q in range(n)] for p in range(n)]
    s = [[0.0] * (2 * n) for _ in range(2 * n)]
    for p in range(n):
        for q in range(n):
            s[p][q] = s[n + p][n + q] = b[p][q].real
            s[p][n + q] = -b[p][q].imag
            s[n + p][q] = b[p][q].imag
    return jacobi_eigenvalues(s)[0]


def test_matrix_is_the_energy():
    for v, f in CLOSED + [(PYR_V, PYR_F)]:
        for n in (1, 2, 4):
            a, m, edges = energy_matrices(v, f, n)
            assert all(abs(a[p][q] - a[q][p].conjugate()) < 1e-14 for p in range(len(v)) for q in range(len(v)))
            rng = random.Random(n)
            u = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in v]
            assert abs(hermitian_form(a, u) - energy(edges, u)) < 1e-12 * max(1.0, energy(edges, u))


def test_eigenvalue_matches_brute_force_on_tiny_meshes():
    for k, (v, f) in enumerate(CLOSED + [(PYR_V, PYR_F)]):
        for seed in (0, 1):
            vv = jittered(v, 10 * k + seed) if seed else v
            for n in (1, 2, 4):
                u, lam, _ = smoothest_field(vv, f, n)
                a, m, edges = energy_matrices(vv, f, n)
                assert abs(lam - smallest_by_brute_force(a, m)) < 1e-9


def test_no_random_field_is_smoother():
    v = jittered(OCTA_V, 3)
    for n in (1, 4):
        u, lam, _ = smoothest_field(v, OCTA_F, n)
        a, m, edges = energy_matrices(v, OCTA_F, n)
        rng = random.Random(5)
        for _ in range(2000):
            w = [complex(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in v]
            assert energy(edges, w) / sum(mi * abs(x) ** 2 for mi, x in zip(m, w)) >= lam - 1e-12
        # Small changes of the minimizer do not lower the quotient either.
        for _ in range(500):
            w = [x + complex(rng.gauss(0, 1e-3), rng.gauss(0, 1e-3)) for x in u]
            assert energy(edges, w) / sum(mi * abs(x) ** 2 for mi, x in zip(m, w)) >= lam - 1e-12


def test_eigenvector_residual_is_small():
    for v, f in CLOSED:
        for n in (1, 2, 4):
            u, lam, _ = smoothest_field(jittered(v, 7), f, n)
            a, m, _ = energy_matrices(jittered(v, 7), f, n)
            assert abs(sum(mi * abs(x) ** 2 for mi, x in zip(m, u)) - 1) < 1e-12
            res = max(abs(sum(a[p][q] * u[q] for q in range(len(u))) - lam * m[p] * u[p]) for p in range(len(u)))
            assert res < 1e-6


def test_flat_disk_has_a_parallel_field():
    for seed in range(3):
        v, f = flat_disk(seed)
        for n in (1, 4):
            u, lam, _ = smoothest_field(v, f, n)
            assert lam < 1e-10
            a, m, edges = energy_matrices(v, f, n)
            assert max(abs(u[j] - r * u[i]) for i, j, w, r in edges) < 1e-5


def test_indices_add_up_to_the_euler_characteristic():
    for k, (v, f) in enumerate(CLOSED):
        for seed in range(3):
            vv = jittered(v, 100 * k + seed)
            for n in (1, 2, 4):
                u, _, _ = smoothest_field(vv, f, n)
                idx = face_indices(vv, f, u, n)
                assert all(abs(x * n - round(x * n)) < 1e-9 for x in idx)
                assert abs(sum(idx) - euler_characteristic(f)) < 1e-9


def test_octahedron_cross_field():
    u, lam, _ = smoothest_field(OCTA_V, OCTA_F, 4)
    assert lam < 1e-10
    assert all(abs(x - 0.25) < 1e-9 for x in face_indices(OCTA_V, OCTA_F, u, 4))
