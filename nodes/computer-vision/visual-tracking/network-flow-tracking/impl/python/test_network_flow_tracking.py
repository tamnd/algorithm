# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/network-flow-tracking/. The authors are listed in prov/4Z2N0P.jsonl.

import itertools
import random

from network_flow_tracking import INF, detection_costs, track_by_flow, tracks_cost


def brute_force(n, det, enter, leave, links):
    """Least cost over all sets of disjoint tracks: each detection is unused, ends a track, or links to a successor."""
    options = []
    for i in range(n):
        succ = [j for (a, j) in links if a == i]
        options.append(["off", "end"] + succ)
    best = 0.0  # the empty set of tracks
    for choice in itertools.product(*options):
        used = [c != "off" for c in choice]
        targets = [c for c in choice if c not in ("off", "end")]
        if len(targets) != len(set(targets)):
            continue
        if any(not used[j] for j in targets):
            continue
        has_pred = set(targets)
        cost = 0.0
        for i, c in enumerate(choice):
            if c == "off":
                continue
            cost += det[i]
            if i not in has_pred:
                cost += enter[i]
            if c == "end":
                cost += leave[i]
            else:
                cost += links[(i, c)]
        best = min(best, cost)
    return best


def random_instance(rng):
    frames = [rng.randint(1, 2) for _ in range(3)]  # detections per frame
    frame_of = [f for f, k in enumerate(frames) for _ in range(k)]
    n = len(frame_of)
    det = [rng.uniform(-3.0, 1.0) for _ in range(n)]
    enter = [rng.uniform(0.0, 2.0) for _ in range(n)]
    leave = [rng.uniform(0.0, 2.0) for _ in range(n)]
    links = {}
    for i in range(n):
        for j in range(n):
            if 1 <= frame_of[j] - frame_of[i] <= 2 and rng.random() < 0.7:
                links[(i, j)] = rng.uniform(0.0, 3.0)
    return n, det, enter, leave, links


def test_optimal_against_brute_force():
    rng = random.Random(2008)
    for _ in range(150):
        n, det, enter, leave, links = random_instance(rng)
        tracks, total, path_costs = track_by_flow(n, det, enter, leave, links)
        assert abs(total - brute_force(n, det, enter, leave, links)) < 1e-9
        # the tracks are disjoint, follow allowed links, and their cost is the total
        flat = [i for tr in tracks for i in tr]
        assert len(flat) == len(set(flat))
        assert all((a, b) in links for tr in tracks for a, b in zip(tr, tr[1:]))
        assert abs(tracks_cost(tracks, det, enter, leave, links) - total) < 1e-9
        # the augmenting paths get no cheaper: the cost is convex in the number of tracks
        assert all(a <= b + 1e-9 for a, b in zip(path_costs, path_costs[1:]))
        assert len(tracks) == len(path_costs)


def test_page_example():
    # frame 0: a = 0, b = 1; frame 1: c = 2, d = 3
    det = [-2.0] * 4
    enter = [1.0] * 4
    leave = [1.0] * 4
    links = {(0, 2): 1.0, (0, 3): 0.1, (1, 2): 5.0, (1, 3): 0.2}
    tracks, total, path_costs = track_by_flow(4, det, enter, leave, links)
    # the first path takes a -> d; the second sends b to d and moves a to c through the residual edge
    assert tracks == [[0, 2], [1, 3]]
    assert abs(total + 2.8) < 1e-9
    assert [round(c, 9) for c in path_costs] == [-1.9, -0.9]


def test_a_weak_isolated_detection_is_dropped():
    det = [-0.5]
    tracks, total, _ = track_by_flow(1, det, [1.0], [1.0], {})
    assert tracks == [] and total == 0.0
    tracks, total, _ = track_by_flow(1, [-2.5], [1.0], [1.0], {})
    assert tracks == [[0]] and abs(total + 0.5) < 1e-12


def test_scene_with_misses_and_false_alarms():
    rng = random.Random(7)
    starts = [(0.0, 0.0), (0.0, 4.0), (0.0, 8.0)]
    vel = (1.0, 0.0)
    dets, truth = [], []
    for f in range(10):
        for k, (x0, y0) in enumerate(starts):
            if (k, f) in ((0, 4), (2, 6)):  # two missed detections
                continue
            dets.append((f, x0 + f * vel[0] + rng.gauss(0, 0.2), y0 + rng.gauss(0, 0.2), rng.uniform(0.8, 0.95)))
            truth.append(k)
        if f in (2, 5, 8):  # false alarms with a low score
            dets.append((f, rng.uniform(0, 10), rng.uniform(-2, 10), rng.uniform(0.5, 0.65)))
            truth.append(-1)
    det, enter, leave, links = detection_costs(dets, sigma=0.5, speed=vel)
    tracks, total, _ = track_by_flow(len(dets), det, enter, leave, links)
    assert len(tracks) == 3
    for tr in tracks:
        labels = {truth[i] for i in tr}
        assert len(labels) == 1 and -1 not in labels
        assert len(tr) == 10 - (1 if labels & {0, 2} else 0)


def test_empty():
    assert track_by_flow(0, [], [], [], {}) == ([], 0.0, [])
    assert INF > 0
