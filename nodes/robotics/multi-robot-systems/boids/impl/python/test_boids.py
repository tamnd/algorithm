# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/boids/. The authors are listed in prov/PDJW2G.jsonl.

import math
import random

from boids import Params, allocate, order_parameter, random_flock, rules, simulate, step


def close(a, b, tol=1e-9):
    return all(math.dist(x, y) <= tol for x, y in zip(a, b))


def brute_rules(i, pos, vel, prm):
    nb = [j for j in range(len(pos)) if j != i and math.dist(pos[i], pos[j]) <= prm.radius]
    if not nb:
        return (0.0, 0.0), (0.0, 0.0), (0.0, 0.0)
    sep = [0.0, 0.0]
    for j in nb:
        d = math.dist(pos[i], pos[j])
        if 0 < d <= prm.sep_radius:
            for c in range(2):
                sep[c] += (pos[i][c] - pos[j][c]) / d / d
    ali = tuple(sum(vel[j][c] for j in nb) / len(nb) - vel[i][c] for c in range(2))
    coh = tuple(sum(pos[j][c] for j in nb) / len(nb) - pos[i][c] for c in range(2))
    return tuple(sep), ali, coh


def test_hand_example() -> None:
    prm = Params(radius=1.0, sep_radius=0.5)
    pos = [(0.0, 0.0), (0.5, 0.0), (0.0, 0.8), (3.0, 3.0)]
    vel = [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (-1.0, 0.0)]
    sep, ali, coh = rules(0, pos, vel, prm)
    assert close([sep], [(-2.0, 0.0)])
    assert close([ali], [(-0.5, 1.0)])
    assert close([coh], [(0.25, 0.4)])
    assert rules(3, pos, vel, prm) == ((0.0, 0.0), (0.0, 0.0), (0.0, 0.0))


def test_rules_against_brute_force() -> None:
    rng = random.Random(1)
    prm = Params(radius=1.2, sep_radius=0.5)
    for _ in range(50):
        pos, vel = random_flock(rng.randrange(1, 12), rng)
        for i in range(len(pos)):
            got, want = rules(i, pos, vel, prm), brute_rules(i, pos, vel, prm)
            assert close(got, want)


def test_permutation_equivariance() -> None:
    rng = random.Random(2)
    prm = Params(max_accel=2.0, min_speed=0.5, max_speed=2.0)
    pos, vel = random_flock(10, rng)
    perm = list(range(10))
    rng.shuffle(perm)
    p1, v1 = step(pos, vel, prm)
    p2, v2 = step([pos[k] for k in perm], [vel[k] for k in perm], prm)
    assert close(p2, [p1[k] for k in perm], 1e-12) and close(v2, [v1[k] for k in perm], 1e-12)


def test_translation_and_rotation_invariance() -> None:
    rng = random.Random(3)
    prm = Params(max_accel=3.0, min_speed=0.3, max_speed=2.0, prioritized=True)
    pos, vel = random_flock(12, rng)
    c, s, t = math.cos(0.7), math.sin(0.7), (5.0, -2.0)
    rot = lambda v: (c * v[0] - s * v[1], s * v[0] + c * v[1])
    p1, v1 = simulate(pos, vel, prm, 20)
    p2, v2 = simulate([rot(p) for p in pos], [rot(v) for v in vel], prm, 20)
    assert close(p2, [rot(p) for p in p1], 1e-9) and close(v2, [rot(v) for v in v1], 1e-9)
    p3, v3 = simulate([(p[0] + t[0], p[1] + t[1]) for p in pos], vel, prm, 20)
    assert close(p3, [(p[0] + t[0], p[1] + t[1]) for p in p1], 1e-9) and close(v3, v1, 1e-9)


def test_alignment_alone_is_consensus() -> None:
    rng = random.Random(4)
    prm = Params(radius=100.0, w_sep=0.0, w_coh=0.0, w_ali=1.0, dt=0.1)
    pos, vel = random_flock(8, rng)
    mean0 = tuple(sum(v[c] for v in vel) / 8 for c in range(2))
    p, v = simulate(pos, vel, prm, 200)
    mean1 = tuple(sum(x[c] for x in v) / 8 for c in range(2))
    assert math.dist(mean0, mean1) < 1e-12
    assert max(math.dist(x, mean0) for x in v) < 1e-9


def spread(q):
    c = tuple(sum(x[k] for x in q) / len(q) for k in range(2))
    return max(math.dist(x, c) for x in q)


def test_cohesion_alone_oscillates_about_a_fixed_center() -> None:
    rng = random.Random(5)
    prm = Params(radius=100.0, w_sep=0.0, w_ali=0.0, w_coh=1.0)
    pos, _ = random_flock(7, rng)
    vel = [(0.0, 0.0)] * 7
    c0 = tuple(sum(p[c] for p in pos) / 7 for c in range(2))
    p, v = pos, vel
    late = []
    for k in range(200):
        p, v = step(p, v, prm)
        if k >= 100:
            late.append(spread(p))
    c1 = tuple(sum(x[c] for x in p) / 7 for c in range(2))
    assert math.dist(c0, c1) < 1e-12
    assert max(late) > 0.5 * spread(pos)


def test_cohesion_with_alignment_contracts() -> None:
    rng = random.Random(8)
    prm = Params(radius=100.0, w_sep=0.0, w_ali=1.0, w_coh=1.0, dt=0.1)
    pos, vel = random_flock(7, rng)
    p, v = simulate(pos, vel, prm, 400)
    assert spread(p) < 1e-6 * spread(pos)
    assert spread(v) < 1e-6


def test_separation_pushes_apart() -> None:
    prm = Params(radius=1.0, sep_radius=0.5, w_ali=0.0, w_coh=0.0)
    p, _ = simulate([(0.0, 0.0), (0.2, 0.0)], [(0.0, 0.0), (0.0, 0.0)], prm, 5)
    assert p[0][0] < 0.0 < 0.2 < p[1][0] and abs(p[0][1]) < 1e-15


def test_prioritized_allocation() -> None:
    assert allocate([(3.0, 0.0), (0.0, 4.0)], 10.0) == (3.0, 4.0)
    assert allocate([(3.0, 0.0), (0.0, 4.0)], 5.0) == (3.0, 2.0)
    assert allocate([(6.0, 0.0), (0.0, 4.0)], 5.0) == (5.0, 0.0)


def test_limits_hold() -> None:
    rng = random.Random(6)
    prm = Params(max_accel=1.0, min_speed=0.5, max_speed=1.5, dt=0.1)
    pos, vel = random_flock(15, rng)
    for _ in range(30):
        new_p, new_v = step(pos, vel, prm)
        for v0, v1 in zip(vel, new_v):
            assert 0.5 - 1e-12 <= math.hypot(*v1) <= 1.5 + 1e-12
        pos, vel = new_p, new_v


def test_flock_aligns_on_this_seed() -> None:
    rng = random.Random(7)
    prm = Params(radius=2.0, sep_radius=0.4, max_accel=2.0, min_speed=0.5, max_speed=1.0)
    pos, vel = random_flock(20, rng, box=2.5)
    before = order_parameter(vel)
    _, v = simulate(pos, vel, prm, 300)
    assert before < 0.5 < 0.95 < order_parameter(v)
