# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orb-slam/. The authors are listed in prov/TY0PRT.jsonl.

import math
import random

from orb_slam import (
    InvertedIndex,
    ToyOrbSlam,
    between,
    bow_vector,
    compose,
    fit_rigid,
    graph_cost,
    inverse,
    l1_score,
    optimize_pose_graph,
    robust_rigid,
    transform,
    wrap,
)


def simulate(seed, keyframes=32, per_lap=24, radius=5.0, vocabulary=40, bias=0.015):
    """A robot on a circle among two rings of landmarks, with biased odometry."""
    rng = random.Random(seed)
    marks = []
    for ring in (3.0, 7.0):
        for _ in range(30):
            a = rng.uniform(-math.pi, math.pi)
            r = ring + rng.uniform(-0.3, 0.3)
            marks.append((r * math.cos(a), r * math.sin(a), rng.randrange(vocabulary)))
    counts = {}
    for _, _, w in marks:
        counts[w] = counts.get(w, 0) + 1
    idf = {w: math.log(len(marks) / n) for w, n in counts.items()}
    step = 2.0 * math.pi / per_lap
    truth = []
    for k in range(keyframes):
        a = -math.pi / 2 + k * step
        truth.append((radius * math.cos(a), radius * math.sin(a) + radius, wrap(a + math.pi / 2)))
    shift = (0.0, radius, 0.0)
    marks = [(x + shift[0], y + shift[1], w) for x, y, w in marks]
    frames = []
    for k, pose in enumerate(truth):
        if k == 0:
            motion = pose
        else:
            m = between(truth[k - 1], pose)
            motion = (m[0] + rng.gauss(0, 0.01), m[1] + rng.gauss(0, 0.01), m[2] + bias + rng.gauss(0, 0.005))
        feats = []
        for x, y, w in marks:
            p = transform(inverse(pose), (x, y))
            if math.hypot(p[0], p[1]) < 3.0:
                feats.append((w, (p[0] + rng.gauss(0, 0.02), p[1] + rng.gauss(0, 0.02))))
        frames.append((motion, feats))
    return truth, frames, idf


def run(seed, **kw):
    truth, frames, idf = simulate(seed, **kw)
    slam = ToyOrbSlam(idf)
    before = None
    loops = []
    for k, (motion, feats) in enumerate(frames):
        snapshot = list(slam.poses)
        out = slam.add_keyframe(motion, feats)
        if out is not None:
            loops.append(out)
            if before is None:
                before = snapshot + [compose(snapshot[-1], motion)]
    return truth, slam, loops, before


def max_error(poses, truth):
    return max(math.hypot(p[0] - t[0], p[1] - t[1]) for p, t in zip(poses, truth))


def test_score_and_inverted_index_match_the_hand_example():
    idf = {1: 0.0, 2: math.log(2), 3: 2 * math.log(2), 4: 2 * math.log(2)}
    q = bow_vector([1, 1, 2, 3], idf)
    b = bow_vector([1, 2, 3, 4], idf)
    c = bow_vector([1, 1, 1, 4], idf)
    assert abs(l1_score(q, b) - 0.6) < 1e-12
    assert abs(l1_score(q, c)) < 1e-12
    index = InvertedIndex()
    index.add("b", b)
    index.add("c", c)
    got = index.query(q)
    assert abs(got["b"] - 0.6) < 1e-12 and "c" not in got


def test_inverted_index_equals_brute_force():
    rng = random.Random(3)
    idf = {w: rng.uniform(0.1, 2.0) for w in range(30)}
    vecs = [bow_vector([rng.randrange(30) for _ in range(12)], idf) for _ in range(25)]
    index = InvertedIndex()
    for k, v in enumerate(vecs):
        index.add(k, v)
    for v in vecs[:5]:
        got = index.query(v)
        for k, u in enumerate(vecs):
            assert abs(got.get(k, 0.0) - l1_score(v, u)) < 1e-12


def test_rigid_fit_recovers_a_pose_with_outliers():
    rng = random.Random(5)
    pose = (0.7, -1.2, 0.9)
    pairs = []
    for _ in range(10):
        p = (rng.uniform(-3, 3), rng.uniform(-3, 3))
        pairs.append((p, transform(pose, p)))
    assert all(abs(a - b) < 1e-12 for a, b in zip(fit_rigid(pairs), pose))
    for _ in range(3):
        pairs.append(((rng.uniform(-3, 3), rng.uniform(-3, 3)), (rng.uniform(-3, 3), rng.uniform(-3, 3))))
    got, ins = robust_rigid(pairs, 0.05)
    assert sorted(ins) == list(range(10))
    assert all(abs(a - b) < 1e-9 for a, b in zip(got, pose))


def test_pose_graph_optimization_reaches_a_local_minimum():
    # a square of four odometry steps that turn a little too much, and a loop
    # edge that says that the end is the start
    poses = [(0.0, 0.0, 0.0)]
    for _ in range(4):
        poses.append(compose(poses[-1], (1.0, 0.0, math.pi / 2 + 0.05)))
    edges = [(k, k + 1, between(poses[k], poses[k + 1])) for k in range(4)]
    edges.append((0, 4, (0.0, 0.0, 0.0)))
    start = graph_cost(poses, edges)
    out = optimize_pose_graph(poses, edges)
    best = graph_cost(out, edges)
    assert out[0] == (0.0, 0.0, 0.0)
    # the turn error of 0.2 rad is spread over five edges: about 5 * 0.04^2 = 0.008
    assert abs(best - 0.008) < 2e-4 and start > 0.05
    rng = random.Random(9)
    for _ in range(50):
        moved = [out[0]] + [(p[0] + rng.gauss(0, 1e-3), p[1] + rng.gauss(0, 1e-3), p[2] + rng.gauss(0, 1e-3)) for p in out[1:]]
        assert graph_cost(moved, edges) >= best - 1e-12


def relative_error(poses, truth, j, k):
    a, b = between(poses[j], poses[k]), between(truth[j], truth[k])
    return math.hypot(a[0] - b[0], a[1] - b[1]), abs(wrap(a[2] - b[2]))


def test_the_toy_closes_the_loop_once_and_removes_the_drift():
    for seed in (1, 2, 3):
        truth, slam, loops, before = run(seed)
        assert len(loops) == 1
        j, k = loops[0]
        # the loop links the second lap to the start of the first lap
        assert j < 6 and 24 <= k < 30
        dist, ang = relative_error(before, truth, j, k)
        assert dist > 1.0 and ang > 0.2
        dist, ang = relative_error(slam.poses, truth, j, k)
        assert dist < 0.05 and ang < 0.05
        assert max_error(slam.poses[: k + 1], truth) < 0.5 * max_error(before[: k + 1], truth)
        # map points were fused: the loop keyframe now shares points with the old one
        assert slam.weights[k].get(j, 0) >= slam.min_inliers


def test_no_loop_without_a_revisit():
    truth, slam, loops, _ = run(4, keyframes=22)
    assert loops == []


def test_consistency_needs_three_keyframes():
    slam = ToyOrbSlam({})
    slam.neighbors = lambda j: {j + 1}
    assert slam._consistent([5]) == []
    assert slam._consistent([6]) == []
    assert slam._consistent([7]) == [7]
    slam.groups = []
    assert slam._consistent([5]) == []
    assert slam._consistent([20]) == []
    assert slam._consistent([6]) == []
