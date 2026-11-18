# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/example-based-facial-rigging/. The authors are listed in prov/3M9YWE.jsonl.
"""Tests of example-based facial rigging.

If the actor is the generic face, the generic rig is a fixed point. The
energy never increases. The blendshape step is the minimizer in D, and the
weight step matches a brute force search over the faces of the box. The
Poisson step recovers a mesh from its own gradients. On a toy face, the
rig fits the actor much better than deformation transfer alone, and the
weights come close to the true ones. The check values of the page hold.
"""

import itertools
import random

from anim import solve
from example_based_facial_rigging import (
    blendshape_step,
    energy,
    facial_rig,
    flat_offsets,
    gradient,
    poisson_reconstruct,
    unflatten,
    weight_step,
)

V = [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (0.0, 1.0), (1.0, 1.0), (2.0, 1.0)]
TRIS = [(0, 1, 4), (0, 4, 3), (1, 2, 5), (1, 5, 4)]
A1 = [(x, 1.5 * y) for x, y in V]  # generic "open"
A2 = [(x + 0.2 * x * y, y) for x, y in V]  # generic "smile"
B0 = [(1.2 * x + 0.1 * y, 0.9 * y + 0.05 * x * x) for x, y in V]
B1 = [(x, y + 0.7 * (y - 0.05 * x * x) / 0.9 * (1.0 + 0.1 * x)) for x, y in B0]
B2 = [(x + 0.3 * x * y, y - 0.05 * x) for x, y in B0]
TRUE_ALPHA = [(1.0, 0.0), (0.0, 1.0), (0.6, 0.5)]
GUESS = [(0.9, 0.1), (0.1, 0.8), (0.5, 0.5)]


def blend(base, targets, weights):
    return [tuple(base[v][k] + sum(w * (t[v][k] - base[v][k]) for w, t in zip(weights, targets)) for k in range(2)) for v in range(len(base))]


EXAMPLES = [blend(B0, [B1, B2], a) for a in TRUE_ALPHA]


def dist(m, n):
    return max(abs(p[k] - q[k]) for p, q in zip(m, n) for k in range(2))


def test_generic_rig_is_a_fixed_point_for_the_generic_actor():
    examples = [blend(V, [A1, A2], a) for a in TRUE_ALPHA]
    targets, alpha, hist = facial_rig([V, A1, A2], V, examples, TRUE_ALPHA, TRIS, beta=0.1, iterations=3)
    assert dist(targets[0], A1) < 1e-10 and dist(targets[1], A2) < 1e-10
    assert max(abs(a - b) for r, s in zip(alpha, TRUE_ALPHA) for a, b in zip(r, s)) < 1e-10
    assert max(hist) < 1e-20


def test_energy_never_increases_and_weights_stay_in_the_box():
    for beta in (1.0, 0.1, 0.01):
        _, alpha, hist = facial_rig([V, A1, A2], B0, EXAMPLES, GUESS, TRIS, beta=beta, iterations=15)
        assert all(hist[i + 1] <= hist[i] + 1e-12 for i in range(len(hist) - 1))
        assert hist[-1] < 0.5 * hist[0]
        assert all(0.0 <= a <= 1.0 for row in alpha for a in row)


def test_blendshape_step_is_the_minimizer():
    rng = random.Random(3)
    n, m, size, beta = 3, 4, 8, 0.2
    alpha = [[rng.random() for _ in range(n)] for _ in range(m)]
    r = [[rng.uniform(-1, 1) for _ in range(size)] for _ in range(m)]
    h = [[rng.uniform(-1, 1) for _ in range(size)] for _ in range(n)]
    d = blendshape_step(alpha, r, h, beta)
    e = energy(d, alpha, r, h, beta)
    for _ in range(50):
        d2 = [[x + rng.uniform(-1e-3, 1e-3) for x in row] for row in d]
        assert energy(d2, alpha, r, h, beta) > e
    eps = 1e-6
    for i in range(n):
        for p in range(size):
            dp = [row[:] for row in d]
            dm = [row[:] for row in d]
            dp[i][p] += eps
            dm[i][p] -= eps
            assert abs(energy(dp, alpha, r, h, beta) - energy(dm, alpha, r, h, beta)) / (2 * eps) < 1e-7


def brute_force_box(d, rj):
    n = len(d)

    def obj(a):
        return sum((sum(a[i] * d[i][p] for i in range(n)) - rj[p]) ** 2 for p in range(len(rj)))

    best = None
    for faces in itertools.product((0.0, 1.0, None), repeat=n):
        free = [i for i in range(n) if faces[i] is None]
        a = [0.0 if f is None else f for f in faces]
        if free:
            res = [rj[p] - sum(a[i] * d[i][p] for i in range(n)) for p in range(len(rj))]
            g = [[sum(d[i][p] * d[k][p] for p in range(len(rj))) for k in free] for i in free]
            b = [sum(d[i][p] * res[p] for p in range(len(rj))) for i in free]
            for i, v in zip(free, solve(g, b)):
                a[i] = v
        if all(-1e-12 <= x <= 1.0 + 1e-12 for x in a):
            v = obj(a)
            if best is None or v < best[0]:
                best = (v, a)
    return best


def test_weight_step_against_brute_force():
    rng = random.Random(11)
    for _ in range(30):
        n, size = rng.choice((2, 3)), 8
        d = [[rng.uniform(-1, 1) for _ in range(size)] for _ in range(n)]
        r = [[rng.uniform(-1.5, 1.5) for _ in range(size)] for _ in range(2)]
        alpha = weight_step(d, r, [[0.5] * n, [0.0] * n])
        for aj, rj in zip(alpha, r):
            want, _ = brute_force_box(d, rj)
            got = sum((sum(aj[i] * d[i][p] for i in range(n)) - rj[p]) ** 2 for p in range(size))
            assert abs(got - want) < 1e-10
            assert all(0.0 <= a <= 1.0 for a in aj)


def test_poisson_recovers_a_mesh_from_its_gradients():
    grads = [[gradient(B0, mesh, t) for t in TRIS] for mesh in (B1, B2)]
    out = poisson_reconstruct(B0, TRIS, grads)
    for mesh, rec in zip((B1, B2), out):
        shift = (B0[0][0] - mesh[0][0], B0[0][1] - mesh[0][1])
        assert dist([(x + shift[0], y + shift[1]) for x, y in mesh], rec) < 1e-12


def test_rig_beats_deformation_transfer_on_the_toy_face():
    targets, alpha, _ = facial_rig([V, A1, A2], B0, EXAMPLES, GUESS, TRIS, beta=0.1, iterations=30)
    transfer = poisson_reconstruct(B0, TRIS, [unflatten(flat_offsets(V, a, TRIS), len(TRIS)) for a in (A1, A2)])
    for got, dt, want in zip(targets, transfer, (B1, B2)):
        assert dist(got, want) < 0.05
        assert dist(dt, want) > 0.25
    assert max(abs(a - b) for r, s in zip(alpha, TRUE_ALPHA) for a, b in zip(r, s)) < 0.05


def test_check_values_of_the_page():
    d = blendshape_step([[0.5]], [[0.4, 0.0, -0.2, 1.0]], [[0.2, 0.6, 0.0, -1.0]], 0.25)
    want = [0.4 + 0.1, 0.0 + 0.3, -0.2 + 0.0, 1.0 - 0.5]
    assert max(abs(a - b) for a, b in zip(d[0], want)) < 1e-12
    w = weight_step([[1.0, 0.0, 0.0, 0.0]], [[2.0, 0, 0, 0], [0.3, 5, 0, 0], [-0.4, 0, 0, 0]], [[0.5]] * 3)
    assert w == [[1.0], [0.3], [0.0]]
