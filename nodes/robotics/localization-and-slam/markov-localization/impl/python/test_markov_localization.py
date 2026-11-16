# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-localization/. The authors are listed in prov/599C1C.jsonl.

import random
from fractions import Fraction as F

import pytest

from markov_localization import (
    DIRS,
    expected_range,
    is_free,
    markov_localization,
    measurement_model,
    motion_model,
    poses,
    uniform_belief,
)

MAP = [
    "########",
    "#......#",
    "#.#.##.#",
    "#...#..#",
    "########",
]
P_MOVE, Z_MAX, W_RAND = F(4, 5), 6, F(1, 10)


def true_step(m, x, u):
    r, c, h = x
    if u == "L":
        return (r, c, (h + 3) % 4)
    if u == "R":
        return (r, c, (h + 1) % 4)
    if u == "F":
        dr, dc = DIRS[h]
        if is_free(m, r + dr, c + dc):
            return (r + dr, c + dc, h)
    return x


def test_models_are_distributions():
    for x in poses(MAP):
        for u in "FLR":
            assert sum(p for _, p in motion_model(MAP, x, u, P_MOVE)) == 1
    for d in range(Z_MAX + 1):
        assert sum(measurement_model(z, d, Z_MAX, W_RAND) for z in range(Z_MAX + 1)) == 1


def brute_force_posterior(m, prior, controls, readings):
    """Sum the joint probability of every path of poses that the motion model allows."""
    paths = [((x,), p) for x, p in prior.items() if p > 0]
    for u, z in zip(controls, readings):
        new = []
        for path, w in paths:
            succ = [(path[-1], 1)] if u is None else motion_model(m, path[-1], u, P_MOVE)
            for x, pr in succ:
                lik = 1 if z is None else measurement_model(z, expected_range(m, x), Z_MAX, W_RAND)
                if pr * lik > 0:
                    new.append((path + (x,), w * pr * lik))
        paths = new
    post = {x: F(0) for x in prior}
    for path, w in paths:
        post[path[-1]] += w
    total = sum(post.values())
    return {x: v / total for x, v in post.items()}


def test_exact_against_sum_over_paths():
    controls = [None, "F", "F", "L", "F"]
    x, readings = (3, 1, 1), []
    for u in controls:
        x = true_step(MAP, x, u)
        readings.append(expected_range(MAP, x))
    readings[2] = None  # one step without a reading
    bel = uniform_belief(MAP)
    for u, z in zip(controls, readings):
        bel = markov_localization(bel, u, z, MAP, P_MOVE, Z_MAX, W_RAND)
    assert sum(bel.values()) == 1
    assert bel == brute_force_posterior(MAP, uniform_belief(MAP), controls, readings)


def test_page_example_global_localization():
    bel = uniform_belief(MAP)
    x = (3, 1, 1)
    counts = []
    for u in [None, "F", "F", "L", "F", "F", "R"]:
        x = true_step(MAP, x, u)
        bel = markov_localization(bel, u, expected_range(MAP, x), MAP, P_MOVE, Z_MAX, W_RAND)
        counts.append(sum(1 for v in bel.values() if v > F(1, 20)))
    assert counts == [10, 10, 10, 4, 4, 4, 1]
    assert x == (1, 3, 1)
    assert max(bel, key=bel.get) == x
    assert abs(float(bel[x]) - 0.9075) < 1e-4


def test_symmetric_map_keeps_two_modes():
    sym = [
        "#####",
        "#...#",
        "#.#.#",
        "#...#",
        "#####",
    ]
    bel = uniform_belief(sym)
    x = (1, 1, 1)
    for u in [None, "F", "R", "F", "F"]:
        x = true_step(sym, x, u)
        bel = markov_localization(bel, u, expected_range(sym, x), sym, P_MOVE, 3, W_RAND)
    # The ring is the same after a rotation by 90 degrees, which maps the pose
    # (r, c, h) to (c, 4 - r, h + 1). No reading can tell the four images of
    # the true pose apart, so they keep the same belief.
    images = [x]
    for _ in range(3):
        r, c, h = images[-1]
        images.append((c, 4 - r, (h + 1) % 4))
    assert len(set(images)) == 4
    assert all(bel[y] == bel[x] for y in images)
    assert bel[x] == max(bel.values())
    assert bel[x] < F(1, 4)


def test_random_runs_converge_and_stay_normalized():
    rng = random.Random(3)
    one = 1.0
    for _ in range(3):
        x = rng.choice(poses(MAP))
        bel = uniform_belief(MAP, one)
        for _ in range(25):
            u = rng.choice("FFFLR")
            if u == "F":
                y = true_step(MAP, x, "F")
                x = y if rng.random() < 0.8 else x
            else:
                x = true_step(MAP, x, u)
            d = expected_range(MAP, x)
            r = rng.random()
            z = d if r < 0.6 else min(max(d + rng.choice((-1, 1)), 0), Z_MAX) if r < 0.9 else rng.randint(0, Z_MAX)
            bel = markov_localization(bel, u, z, MAP, 0.8, Z_MAX, 0.1)
            assert abs(sum(bel.values()) - 1.0) < 1e-9
        assert bel[x] > 0.0


def test_impossible_reading_raises():
    bel = {(1, 1, 1): F(1)}
    with pytest.raises(ValueError):
        markov_localization(bel, None, 3, MAP, P_MOVE, Z_MAX, F(0))
