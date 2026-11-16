# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/null-space-projection/. The authors are listed in prov/SA0J6T.jsonl.
"""Tests of null-space projection: the projector identities, the closest
joint velocity against a KKT solve, the planar 3R example of the page, and
a gradient projection run that lowers a joint cost while the tip stays."""

import math
import random

import rbm
from null_space_projection import gradient_projection_run, null_space_step, projector


def maxdiff(a, b):
    if a and isinstance(a[0], list):
        return max(abs(x - y) for ra, rb in zip(a, b) for x, y in zip(ra, rb))
    return max(abs(x - y) for x, y in zip(a, b))


def rand_matrix(rng, m, n):
    return [[rng.uniform(-1.0, 1.0) for _ in range(n)] for _ in range(m)]


def fk3(q):
    a = x = y = 0.0
    for t in q:
        a += t
        x += math.cos(a)
        y += math.sin(a)
    return [x, y]


def jac3(q):
    n = len(q)
    out = [[0.0] * n, [0.0] * n]
    for j in range(n):
        a = sum(q[: j + 1])
        for i in range(j + 1):
            out[0][i] -= math.sin(a)
            out[1][i] += math.cos(a)
    return out


def test_projector_identities():
    rng = random.Random(41)
    for m, n in [(2, 3), (3, 7), (6, 7), (1, 4)]:
        j = rand_matrix(rng, m, n)
        p = projector(j)
        assert maxdiff(rbm.mul(j, p), rbm.zeros(m, n)) < 1e-12
        assert maxdiff(rbm.mul(p, p), p) < 1e-12
        assert maxdiff(p, rbm.transpose(p)) < 1e-12
        assert abs(sum(p[i][i] for i in range(n)) - (n - m)) < 1e-12


def test_step_is_closest_to_z():
    rng = random.Random(42)
    for m, n in [(2, 3), (3, 7), (6, 7)]:
        j = rand_matrix(rng, m, n)
        xdot = [rng.uniform(-1.0, 1.0) for _ in range(m)]
        z = [rng.uniform(-1.0, 1.0) for _ in range(n)]
        qd = null_space_step(j, xdot, z)
        assert maxdiff(rbm.matvec(j, qd), xdot) < 1e-12
        # KKT system of min |q' - z|^2 / 2 subject to J q' = x'
        kkt = rbm.zeros(n + m, n + m)
        for i in range(n):
            kkt[i][i] = 1.0
        for r in range(m):
            for c in range(n):
                kkt[n + r][c] = j[r][c]
                kkt[c][n + r] = j[r][c]
        sol = rbm.solve(kkt, z + xdot)
        assert maxdiff(qd, sol[:n]) < 1e-12


def test_planar_3r_example():
    q = [0.0, math.pi / 2.0, -math.pi / 2.0]
    assert maxdiff(fk3(q), [2.0, 1.0]) < 1e-15
    j = jac3(q)
    assert maxdiff(j, [[-1.0, -1.0, 0.0], [2.0, 1.0, 1.0]]) < 1e-15
    assert maxdiff(rbm.num_jacobian(fk3, [0.3, 0.8, -0.4]), jac3([0.3, 0.8, -0.4])) < 1e-6
    p = projector(j)
    n = [1.0, -1.0, -1.0]
    nn = rbm.dot(n, n)
    assert maxdiff(p, [[a * b / nn for b in n] for a in n]) < 1e-15
    qd = null_space_step(j, [0.0, 0.0], [0.0, 0.0, 3.0])
    assert maxdiff(qd, [-1.0, 1.0, 1.0]) < 1e-14


def test_gradient_projection_lowers_the_cost_and_keeps_the_tip():
    q0 = [0.2, 1.2, -0.9]
    x_d = fk3(q0)

    def grad_h(q):
        return list(q)  # h(q) = |q|^2 / 2, distance from the middle of the joint range

    path = gradient_projection_run(fk3, jac3, grad_h, q0, x_d, 10.0, 1.0, 0.01, 1500)
    hs = [rbm.dot(q, q) / 2.0 for q in path]
    tips = [rbm.norm(rbm.sub(fk3(q), x_d)) for q in path]
    assert max(tips) < 1e-3
    assert hs[-1] < 0.8 * hs[0]
    assert all(b <= a + 1e-12 for a, b in zip(hs, hs[1:]))
    # at the end the gradient of h has no component left in the null space
    qe = path[-1]
    assert rbm.norm(rbm.matvec(projector(jac3(qe)), grad_h(qe))) < 1e-3
