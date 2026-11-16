# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/reeds-shepp-path/. The authors are listed in prov/FYPPAD.jsonl.

import math
import random

from reeds_shepp_path import (
    TYPES,
    endpoint,
    gear_changes,
    reeds_shepp_candidates,
    reeds_shepp_path,
    wrap,
)

HALF_PI = 0.5 * math.pi


def pose_error(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(wrap(a[2] - b[2])))


def random_pose(rng, size=5.0):
    return (rng.uniform(-size, size), rng.uniform(-size, size), rng.uniform(-math.pi, math.pi))


def test_every_candidate_ends_at_the_goal():
    rng = random.Random(21)
    for _ in range(1500):
        q0, q1 = random_pose(rng), random_pose(rng)
        rho = rng.uniform(0.3, 2.0)
        cands = reeds_shepp_candidates(q0, q1, rho)
        assert cands
        for length, word, seg in cands:
            assert len(word) == len(seg)
            assert abs(length - sum(abs(a) for a in seg)) < 1e-12
            assert pose_error(endpoint(q0, word, seg, rho), q1) < 1e-9


def random_signed_path(rng, rho):
    """A random path of the car: a random word of up to five segments with random signs,
    or a word of the Reeds-Shepp shape with arcs of exactly pi / 2 where the shape has them."""
    if rng.random() < 0.5:
        word = "".join(rng.choice("LSR") for _ in range(rng.randint(1, 5)))
        seg = [rng.choice((-1.0, 1.0)) * (rng.uniform(0.0, 4.0) if k == "S" else rho * rng.uniform(0.0, math.pi)) for k in word]
        return word, seg
    word = rng.choice(TYPES)
    seg = []
    for i, k in enumerate(word):
        sign = rng.choice((-1.0, 1.0))
        fixed = "S" in word and k != "S" and (word[i - 1:i] == "S" or word[i + 1:i + 2] == "S") and len(word) >= 4
        if k == "S":
            seg.append(sign * rng.uniform(0.0, 4.0))
        elif fixed and rng.random() < 0.7:
            seg.append(sign * rho * HALF_PI)
        else:
            seg.append(sign * rho * rng.uniform(0.0, math.pi))
    return word, seg


def test_no_random_path_is_shorter():
    rng = random.Random(22)
    for _ in range(4000):
        rho = rng.uniform(0.5, 1.5)
        q0 = random_pose(rng)
        word, seg = random_signed_path(rng, rho)
        q1 = endpoint(q0, word, seg, rho)
        # 1e-7: a segment of length 0 can come out near 1e-8 from a square root.
        assert reeds_shepp_path(q0, q1, rho)[0] <= sum(abs(a) for a in seg) + 1e-7


def test_no_forward_path_is_shorter():
    # A forward path is also a Reeds-Shepp path, so the result is never longer.
    rng = random.Random(23)
    for _ in range(1500):
        q0 = random_pose(rng)
        word = "".join(rng.choice("LSR") for _ in range(rng.randint(1, 3)))
        seg = [rng.uniform(0.0, 3.0) for _ in word]
        q1 = endpoint(q0, word, seg, 1.0)
        assert reeds_shepp_path(q0, q1, 1.0)[0] <= sum(seg) + 1e-7


def test_reversal_symmetry():
    # Driving a path backward in time is a valid path from the goal to the start.
    rng = random.Random(24)
    for _ in range(800):
        q0, q1 = random_pose(rng), random_pose(rng)
        a = reeds_shepp_path(q0, q1, 1.0)[0]
        b = reeds_shepp_path(q1, q0, 1.0)[0]
        assert abs(a - b) < 1e-9


def test_every_base_type_is_optimal_somewhere():
    rng = random.Random(25)
    seen = set()
    for _ in range(4000):
        q0, q1 = random_pose(rng, 3.0), random_pose(rng, 3.0)
        seen.add(reeds_shepp_path(q0, q1, 1.0)[1])
    assert seen == set(TYPES)


def test_hand_cases():
    # Straight back by 4 m.
    length, word, seg = reeds_shepp_path((0.0, 0.0, 0.0), (-4.0, 0.0, 0.0), 1.0)
    assert abs(length - 4.0) < 1e-12 and word[seg.index(min(seg))] == "S"
    # U-turn on the spot with radius 1 m: three arcs of pi / 3 with two gear changes.
    length, word, seg = reeds_shepp_path((0.0, 0.0, 0.0), (0.0, 0.0, math.pi), 1.0)
    assert abs(length - math.pi) < 1e-9 and word in ("LRL", "RLR") and gear_changes(seg) == 2
    # A goal that a forward path reaches best: the same as the Dubins path (5.1763 m).
    length, word, seg = reeds_shepp_path((0.0, 0.0, 0.0), (3.0, 4.0, math.pi / 2.0), 1.0)
    assert word == "LSL" and abs(length - (math.atan2(3.0, 2.0) + math.sqrt(13.0) + math.pi / 2.0 - math.atan2(3.0, 2.0))) < 1e-9
    # Parallel shift by 1 m to the left: four arcs, shorter than 2.64 m.
    length, word, seg = reeds_shepp_path((0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 1.0)
    assert len(word) == 4 and abs(length - 2.6362) < 1e-4
    # Scaling.
    a = reeds_shepp_path((0.0, 0.0, 0.3), (2.0, 1.0, -1.0), 1.0)[0]
    b = reeds_shepp_path((0.0, 0.0, 0.3), (6.0, 3.0, -1.0), 3.0)[0]
    assert abs(3.0 * a - b) < 1e-9


def test_at_most_five_segments_and_two_gear_changes():
    rng = random.Random(26)
    for _ in range(1500):
        q0, q1 = random_pose(rng), random_pose(rng)
        length, word, seg = reeds_shepp_path(q0, q1, 1.0)
        assert len(word) <= 5
        assert gear_changes(seg) <= 2
