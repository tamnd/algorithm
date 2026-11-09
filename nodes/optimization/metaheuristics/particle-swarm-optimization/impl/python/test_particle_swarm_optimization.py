# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/particle-swarm-optimization/. The authors are listed in prov/F6H8KV.jsonl.

import math
import random

from particle_swarm_optimization import (
    constriction_coefficient,
    order1_stable,
    order2_stable_equal,
    particle_swarm_optimization,
    sphere,
)


def rastrigin(x):
    return 10 * len(x) + sum(t * t - 10 * math.cos(2 * math.pi * t) for t in x)


def test_every_move_obeys_the_update_rule() -> None:
    w, c1, c2 = 0.7, 1.4, 1.6
    moves = []
    particle_swarm_optimization(sphere, [-3] * 3, [3] * 3, 6, w, c1, c2, 40, random.Random(1), on_move=lambda *a: moves.append(a))
    assert len(moves) == 6 * 40
    for i, x, v, p, g, r1, r2, v_new, x_new in moves:
        for d in range(3):
            assert 0 <= r1[d] < 1 and 0 <= r2[d] < 1
            assert v_new[d] == w * v[d] + c1 * r1[d] * (p[d] - x[d]) + c2 * r2[d] * (g[d] - x[d])
            assert x_new[d] == x[d] + v_new[d]


def test_personal_and_global_bests() -> None:
    moves = []
    f = rastrigin
    g, fg, hist, ps = particle_swarm_optimization(f, [-5.12] * 2, [5.12] * 2, 8, 0.6, 1.5, 1.5, 60, random.Random(2), on_move=lambda *a: moves.append(a))
    visited: dict[int, list[list[float]]] = {}
    for i, x, v, p, gg, r1, r2, v_new, x_new in moves:
        visited.setdefault(i, [list(x)])  # the first x_old of a particle is its start
        visited[i].append(x_new)
    for i, pts in visited.items():
        assert f(ps[i]) == min(f(y) for y in pts)  # p_i is the best point that particle i visited
    assert fg == f(g) == min(f(p) for p in ps)  # g is the best of the personal bests
    assert all(hist[t + 1] <= hist[t] for t in range(len(hist) - 1))


def test_fixed_seed_reaches_the_minimum() -> None:
    chi = constriction_coefficient(4.1)
    c = 2.05 * chi
    g, fg, hist, ps = particle_swarm_optimization(sphere, [-5] * 5, [5] * 5, 20, chi, c, c, 300, random.Random(0))
    assert fg < 1e-15
    g, fg, hist, ps = particle_swarm_optimization(rastrigin, [-5.12] * 2, [5.12] * 2, 30, chi, c, c, 200, random.Random(0))
    assert fg < 1e-12 and max(abs(t) for t in g) < 1e-6


def test_constriction_values() -> None:
    chi = constriction_coefficient(4.1)
    assert abs(chi - 0.7298437881) < 1e-9
    assert abs(2.05 * chi - 1.4961797657) < 1e-9
    assert order1_stable(chi, 2.05 * chi, 2.05 * chi)
    assert order2_stable_equal(chi, 4.1 * chi)


def _decays(step, state, steps=6000) -> bool:
    for _ in range(steps):
        state = step(state)
        if max(abs(s) for s in state) > 1e12:
            return False
    return max(abs(s) for s in state) < 1e-6


def test_order1_region_matches_the_mean_recursion() -> None:
    # Under stagnation with p = g = 0, E[x] follows m' = (1 + w - (c1 + c2) / 2) m - w m_prev.
    checked = 0
    for w in (-0.6, -0.2, 0.0, 0.3, 0.5, 0.7, 0.85):
        for k in range(1, 60):
            c = 0.15 * k
            limit = 4 * (1 + w)
            if abs(c - limit) < 0.05 * limit or c < 0.3:
                continue
            mu = 1 + w - c / 2
            got = _decays(lambda s: (mu * s[0] - w * s[1], s[0]), (1.0, 1.0))
            assert got == order1_stable(w, c / 2, c / 2)
            checked += 1
    assert checked > 300


def test_order2_region_matches_the_second_moment_recursion() -> None:
    # With c1 = c2 = c / 2 and y = x - p, the vector (E y_t^2, E y_t y_(t-1), E y_(t-1)^2) follows a 3 x 3 linear map.
    checked = 0
    for w in (-0.6, -0.2, 0.0, 0.3, 0.5, 0.7, 0.85):
        for k in range(1, 50):
            c = 0.15 * k
            limit = 24 * (1 - w * w) / (7 - 5 * w)
            if abs(c - limit) < 0.05 * limit or c < 0.3:
                continue
            mu = 1 + w - c / 2
            s2 = mu * mu + 2 * (c / 2) ** 2 / 12

            def step(z, mu=mu, s2=s2, w=w):
                a, b, e = z
                return (s2 * a - 2 * w * mu * b + w * w * e, mu * a - w * b, a)

            assert _decays(step, (1.0, 1.0, 1.0)) == order2_stable_equal(w, c)
            checked += 1
    assert checked > 250
