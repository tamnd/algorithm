# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/force-directed-layout/. The authors are listed in prov/MAJJEY.jsonl.

import math
import random
from itertools import combinations

from force_directed_layout import force_directed_layout


def energy(n, edges, x, k):
    """E = sum over edges of d^3 / (3k) minus sum over pairs of k^2 ln d."""
    e = 0.0
    for u, v in edges:
        e += math.dist(x[u], x[v]) ** 3 / (3 * k)
    for u, v in combinations(range(n), 2):
        e -= k * k * math.log(math.dist(x[u], x[v]))
    return e


def minus_gradient(n, edges, x, k, h=1e-6):
    """The force on each vertex as the negative gradient of E, by central differences."""
    out = []
    for v in range(n):
        g = []
        for axis in range(2):
            up = [list(p) for p in x]
            down = [list(p) for p in x]
            up[v][axis] += h
            down[v][axis] -= h
            g.append(-(energy(n, edges, up, k) - energy(n, edges, down, k)) / (2 * h))
        out.append(g)
    return out


def random_case(rng):
    n = rng.randint(2, 7)
    edges = [(u, v) for u, v in combinations(range(n), 2) if rng.random() < 0.4]
    pos = [(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(n)]
    return n, edges, pos


def test_one_round_is_capped_gradient_step():
    rng = random.Random(1991)
    checked = 0
    while checked < 600:
        n, edges, pos = random_case(rng)
        if min(math.dist(p, q) for p, q in combinations(pos, 2)) < 0.05:
            continue
        k = rng.uniform(0.5, 2.0)
        t = rng.choice([1e9, 0.05])
        got = force_directed_layout(n, edges, pos, k=k, t0=t, rounds=1)
        force = minus_gradient(n, edges, pos, k)
        for v in range(n):
            length = math.hypot(*force[v])
            step = min(length, t)
            want = (pos[v][0] + force[v][0] / length * step, pos[v][1] + force[v][1] / length * step)
            assert math.dist(got[v], want) <= 1e-5 * max(1.0, step)
        checked += 1


def test_single_edge_reaches_length_k():
    for k in (0.5, 1.0, 3.0):
        p = force_directed_layout(2, [(0, 1)], [(0.0, 0.0), (0.1 * k, 0.05 * k)], k=k, t0=0.2 * k, rounds=400)
        assert abs(math.dist(p[0], p[1]) - k) < 1e-3 * k


def test_path_of_three():
    p = force_directed_layout(3, [(0, 1), (1, 2)], [(0, 0), (0.5, 0.3), (1, 0)], k=1.0, t0=0.2, rounds=300)
    target = 1.5 ** (1 / 3)
    assert abs(math.dist(p[0], p[1]) - target) < 2e-3
    assert abs(math.dist(p[1], p[2]) - target) < 2e-3
    assert abs(math.dist(p[0], p[2]) - 2 * target) < 4e-3


def test_moves_are_bounded_and_translation_invariant():
    rng = random.Random(1129)
    for _ in range(200):
        n, edges, pos = random_case(rng)
        rounds = rng.randint(1, 6)
        t0 = 0.3
        got = force_directed_layout(n, edges, pos, k=1.0, t0=t0, rounds=rounds)
        bound = sum(t0 * (1 - r / rounds) for r in range(rounds)) + 1e-9
        for v in range(n):
            assert math.dist(got[v], pos[v]) <= bound
        shift = (rng.uniform(-5, 5), rng.uniform(-5, 5))
        moved = force_directed_layout(
            n, edges, [(a + shift[0], b + shift[1]) for a, b in pos], k=1.0, t0=t0, rounds=rounds
        )
        for v in range(n):
            assert math.dist(moved[v], (got[v][0] + shift[0], got[v][1] + shift[1])) < 1e-7


def test_coincident_points_separate():
    p = force_directed_layout(2, [], [(1.0, 1.0), (1.0, 1.0)], k=1.0, t0=0.1, rounds=1)
    assert p[0][0] < 1.0 < p[1][0]
    assert force_directed_layout(0, [], []) == []
    assert force_directed_layout(1, [], [(2.0, 3.0)]) == [(2.0, 3.0)]


if __name__ == "__main__":
    test_one_round_is_capped_gradient_step()
    test_single_edge_reaches_length_k()
    test_path_of_three()
    test_moves_are_bounded_and_translation_invariant()
    test_coincident_points_separate()
    print("ok")
