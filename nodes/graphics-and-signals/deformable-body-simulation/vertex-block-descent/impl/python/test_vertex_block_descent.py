# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/vertex-block-descent/. The authors are listed in prov/B1423N.jsonl.

"""Tests of vertex block descent: derivatives, the coloring, descent and convergence to backward Euler."""

import math
import random

from anim import num_grad
import vertex_block_descent as vb


def crumpled(seed):
    rng = random.Random(seed)
    s = vb.cloth(6, 6, 0.1, 1000.0, mass=0.01, pin_top=False)
    x = [(0.4 * p[0] + rng.uniform(-0.01, 0.01), 0.4 * p[1] + rng.uniform(-0.01, 0.01)) for p in s.rest]
    return s, x


def test_example_one_spring():
    """A pinned spring and one vertex: a single Newton step is exact for the backward Euler step along the line."""
    s = vb.System([(0.0, 0.0), (1.5, 0.0)], [(0, 1, 1.0, 100.0)], [1.0, 1.0], pinned=[0])
    cols = vb.greedy_coloring(s)
    x1, v1 = vb.vbd_step(s, cols, [(0.0, 0.0), (1.5, 0.0)], [(0.0, 0.0)] * 2, 0.1, 1, gravity=(0.0, 0.0))
    assert math.dist(x1[1], (1.25, 0.0)) < 1e-14 and math.dist(v1[1], (-2.5, 0.0)) < 1e-12


def test_force_and_hessian_against_num_grad():
    rng = random.Random(41)
    s = vb.cloth(4, 4, 0.1, 500.0, mass=0.02)
    x = [(p[0] + rng.uniform(-0.03, 0.03), p[1] + rng.uniform(-0.03, 0.03)) for p in s.rest]
    y = [(p[0] + 0.01, p[1] - 0.01) for p in x]
    dt = 0.02
    for i in range(len(x)):
        if i in s.pinned:
            continue
        f, h = vb.force_and_hessian(s, x, y, dt, i)

        def gi(z):
            return vb.local_energy(s, x, y, dt, i, (z[0], z[1]))

        ng = num_grad(gi, list(x[i]))
        assert max(abs(ng[d] + f[d]) for d in range(2)) < 1e-5 * max(1.0, abs(f[0]) + abs(f[1]))
        for q in range(2):
            def gq(z, q=q):
                xs = list(x)
                xs[i] = (z[0], z[1])
                return -vb.force_and_hessian(s, xs, y, dt, i)[0][q]

            col = num_grad(gq, list(x[i]))
            for p in range(2):
                assert abs(col[p] - h[q][p]) < 1e-4 * max(1.0, abs(h[q][p]))
        assert abs(h[0][1] - h[1][0]) < 1e-12


def test_coloring_is_proper_and_small():
    s = vb.cloth(8, 8, 0.1, 100.0)
    cols = vb.greedy_coloring(s)
    color = {i: c for c, group in enumerate(cols) for i in group}
    assert set(color) == set(range(64)) - s.pinned
    for a, b, _, _ in s.springs:
        if a in color and b in color:
            assert color[a] != color[b]
    assert len(cols) <= 1 + max(len(adj) for adj in s.adj)


def test_parallel_updates_in_a_color_equal_sequential_updates():
    s, x = crumpled(42)
    y = [(p[0], p[1] - 0.001) for p in x]
    cols = vb.greedy_coloring(s)
    group = cols[0]
    par = list(x)
    moves = [(i, vb.vertex_update(s, x, y, 1.0 / 30.0, i)) for i in group]
    for i, d in moves:
        par[i] = (par[i][0] + d[0], par[i][1] + d[1])
    seq = list(x)
    for i in group:
        d = vb.vertex_update(s, seq, y, 1.0 / 30.0, i)
        seq[i] = (seq[i][0] + d[0], seq[i][1] + d[1])
    assert par == seq


def test_line_search_never_increases_the_objective():
    s, x = crumpled(5)
    dt = 1.0 / 30.0
    y = vb.predict(s, x, [(0.0, 0.0)] * len(x), dt, (0.0, 0.0))
    cols = vb.greedy_coloring(s)
    z, prev = list(y), vb.objective(s, y, y, dt)
    for _ in range(60):
        for group in cols:
            z = vb.vbd_iteration(s, [group], z, y, dt, line_search=True)
            g = vb.objective(s, z, y, dt)
            assert g <= prev * (1.0 + 1e-14)
            prev = g


def test_without_line_search_the_objective_can_increase():
    """Measured: from a crumpled start, a plain Newton sweep raises the objective."""
    s, x = crumpled(5)
    dt = 1.0 / 30.0
    y = vb.predict(s, x, [(0.0, 0.0)] * len(x), dt, (0.0, 0.0))
    z = vb.vbd_iteration(s, vb.greedy_coloring(s), y, y, dt)
    assert vb.objective(s, z, y, dt) > 1e3 * vb.objective(s, y, y, dt)


def test_converges_to_a_backward_euler_step():
    s = vb.cloth(6, 6, 0.1, 1000.0, mass=0.01)
    cols = vb.greedy_coloring(s)
    dt = 1.0 / 60.0
    x, v = list(s.rest), [(0.0, 0.0)] * 36
    for _ in range(10):
        x, v = vb.vbd_step(s, cols, x, v, dt, 20)
    y = vb.predict(s, x, v, dt)
    z = list(y)
    norms = []
    for it in range(1, 251):
        z = vb.vbd_iteration(s, cols, z, y, dt)
        if it in (10, 100, 250):
            norms.append(vb.gradient_norm(s, z, y, dt))
    assert norms[0] > norms[1] > norms[2] and norms[2] < 1e-6


def test_singular_vertex_is_skipped():
    """In compression the tangent stiffness m/dt^2 + k (1 - r/l) is zero at l = r k / (k + m/dt^2)."""
    k, m, dt, r = 100.0, 1.0, 0.1, 1.0
    ln = r * k / (k + m / dt ** 2)
    s = vb.System([(0.0, 0.0), (ln, 0.0)], [(0, 1, r, k)], [m, m], pinned=[0])
    x = [(0.0, 0.0), (ln, 0.0)]
    assert vb.vertex_update(s, x, x, dt, 1, eps=1e-9) == (0.0, 0.0)


def test_momentum_error_shrinks_as_the_iterations_converge():
    """Block descent does not keep momentum exactly per sweep; the converged step does (measured)."""
    rng = random.Random(43)
    s = vb.cloth(4, 4, 0.1, 300.0, mass=0.05, pin_top=False)
    x = [(p[0] + rng.uniform(-0.01, 0.01), p[1] + rng.uniform(-0.01, 0.01)) for p in s.rest]
    v = [(rng.uniform(-0.5, 0.5), rng.uniform(-0.5, 0.5)) for _ in x]
    cols = vb.greedy_coloring(s)
    p0 = [sum(m * u[d] for m, u in zip(s.mass, v)) for d in range(2)]
    errs = []
    for it in (1, 10, 200):
        _, v1 = vb.vbd_step(s, cols, x, v, 1.0 / 30.0, it, gravity=(0.0, 0.0))
        p1 = [sum(m * u[d] for m, u in zip(s.mass, v1)) for d in range(2)]
        errs.append(max(abs(a - b) for a, b in zip(p0, p1)))
    assert errs[0] > errs[1] > errs[2] and errs[2] < 1e-7


def test_free_fall_is_symplectic_euler():
    s = vb.System([(0.0, 0.0)], [], [1.0])
    x, v = [(0.0, 0.0)], [(0.0, 0.0)]
    for _ in range(10):
        x, v = vb.vbd_step(s, [[0]], x, v, 0.1, 2)
    assert abs(x[0][1] + 5.3955) < 1e-12
