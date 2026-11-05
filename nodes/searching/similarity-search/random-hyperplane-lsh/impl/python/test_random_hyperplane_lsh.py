# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-hyperplane-lsh/. The authors are listed in prov/7MZBA9.jsonl.

import math
import random

from random_hyperplane_lsh import RandomHyperplaneLSH, angle, hash_key, parameters

R = [(0.5, 1), (-1, 0.3), (0.2, -1), (1, -0.4)]


def test_example_keys() -> None:
    assert hash_key((1, 0), R) == (1, 0, 1, 1)
    assert hash_key((1, 1), R) == (1, 0, 0, 1)
    assert hash_key((0.9, 0.3), R) == (1, 0, 0, 1)
    assert hash_key((-1, 0.2), R) == (0, 1, 0, 0)
    assert abs(math.degrees(angle((1, 0), (1, 1))) - 45) < 1e-9


def test_example_parameters() -> None:
    assert parameters(10**6, math.pi / 6, math.pi / 3) == (35, 599)


def test_scale_invariant() -> None:
    rng = random.Random(3)
    planes = [tuple(rng.gauss(0, 1) for _ in range(5)) for _ in range(16)]
    x = tuple(rng.uniform(-1, 1) for _ in range(5))
    assert hash_key(x, planes) == hash_key(tuple(2.5 * v for v in x), planes)


def test_collision_probability() -> None:
    rng = random.Random(7)
    for x, y in [((1, 0, 0), (1, 1, 0)), ((1, 0, 0), (-1, 0.2, 0)), ((1, 2, 3), (3, -1, 0.5))]:
        trials = 20000
        same = sum(
            hash_key(x, [r]) == hash_key(y, [r])
            for r in (tuple(rng.gauss(0, 1) for _ in range(3)) for _ in range(trials))
        )
        assert abs(same / trials - (1 - angle(x, y) / math.pi)) < 0.02


def test_edges() -> None:
    empty = RandomHyperplaneLSH([], k=3, num_tables=2)
    assert empty.query((1, 0), 1.0) is None
    one = RandomHyperplaneLSH([(1, 0)], k=3, num_tables=2)
    assert one.query((2, 0), 0.1) == 0
    assert one.query((-1, 0), 1.0) is None
    try:
        RandomHyperplaneLSH([(0, 0)], k=1, num_tables=1)
        raise AssertionError("zero vector accepted")
    except ValueError:
        pass


def test_random_against_brute_force() -> None:
    rng = random.Random(2026)
    theta1, theta2 = math.pi / 6, math.pi / 3
    successes = trials = 0
    for t in range(600):
        n = rng.randint(1, 60)
        d = rng.randint(2, 6)
        pts = []
        while len(pts) < n:
            p = tuple(rng.gauss(0, 1) for _ in range(d))
            if any(p):
                pts.append(p)
        k, num_tables = parameters(max(n, 2), theta1, theta2)
        index = RandomHyperplaneLSH(pts, k, num_tables, seed=t)
        q = tuple(rng.gauss(0, 1) for _ in range(d))
        ans = index.query(q, theta2)
        if ans is not None:
            assert angle(q, pts[ans]) <= theta2
        if all(angle(q, p) > theta2 for p in pts):
            assert ans is None
        if any(angle(q, p) <= theta1 for p in pts):
            trials += 1
            successes += ans is not None
    assert trials > 50
    assert successes / trials >= 1 - 1 / math.e - 1 / 3
