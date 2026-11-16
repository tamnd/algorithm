# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deep-sort/. The authors are listed in prov/Q69QVS.jsonl.

import itertools
import math
import random
from fractions import Fraction

from deep_sort import (
    CHI2_95_4DOF,
    CONFIRMED,
    DeepSortTracker,
    box_to_xyah,
    gallery_distance,
    hungarian_min,
    iou,
    kf_initiate,
    kf_predict,
    kf_project,
    kf_update,
    mahalanobis_sq,
    matching_cascade,
    min_cost_matching,
    xyah_to_box,
)


def cholesky(a):
    n = len(a)
    low = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = a[i][j] - sum(low[i][k] * low[j][k] for k in range(j))
            low[i][j] = math.sqrt(s) if i == j else s / low[j][j]
    return low


def test_chi_square_gate_value():
    g = CHI2_95_4DOF
    assert abs(1.0 - math.exp(-g / 2.0) * (1.0 + g / 2.0) - 0.95) < 1e-4


def test_gate_keeps_95_percent_of_model_measurements():
    rng = random.Random(5)
    mean, cov = kf_initiate(box_to_xyah((100.0, 50.0, 120.0, 90.0)))
    for _ in range(3):
        mean, cov = kf_predict(mean, cov)
    zp, s = kf_project(mean, cov)
    low = cholesky(s)
    inside, trials = 0, 4000
    for _ in range(trials):
        w = [rng.gauss(0.0, 1.0) for _ in range(4)]
        z = [zp[i] + sum(low[i][k] * w[k] for k in range(4)) for i in range(4)]
        inside += mahalanobis_sq(mean, cov, z) <= CHI2_95_4DOF
    assert abs(inside / trials - 0.95) < 0.015


def test_box_round_trip_and_iou_values():
    b = (4.0, 0.0, 14.0, 20.0)
    assert box_to_xyah(b) == [9.0, 10.0, 0.5, 20.0]
    assert xyah_to_box(box_to_xyah(b)) == b
    assert iou(tuple(map(Fraction, (0, 0, 2, 2))), tuple(map(Fraction, (1, 1, 3, 3)))) == Fraction(1, 7)
    assert iou(tuple(map(Fraction, (0, 0, 10, 10))), tuple(map(Fraction, (5, 0, 15, 10)))) == Fraction(1, 3)


def test_gallery_distance_is_the_minimum():
    gallery = [[1.0, 0.0], [0.0, 1.0]]
    assert abs(gallery_distance(gallery, [0.6, 0.8]) - 0.2) < 1e-12
    assert abs(gallery_distance(gallery, [12.0, 5.0]) - 1.0 / 13.0) < 1e-12


def brute_min_cost(cost, allowed, rows, cols):
    """The rule of min_cost_matching by search: a full assignment of least cost,
    where a forbidden pair costs 1 more than the largest allowed cost."""
    vals = {(i, j): cost(i, j) for i in rows for j in cols if allowed(i, j)}
    top = max(vals.values(), default=0.0) + 1.0
    k = min(len(rows), len(cols))
    best = None
    for rs in itertools.permutations(rows, k):
        for cs in itertools.combinations(cols, k):
            total = sum(vals.get((i, j), top) for i, j in zip(rs, cs))
            if best is None or total < best:
                best = total
    return best, top


def test_min_cost_matching_against_brute_force():
    rng = random.Random(9)
    for _ in range(150):
        n, m = rng.randint(1, 4), rng.randint(1, 4)
        c = [[rng.random() for _ in range(m)] for _ in range(n)]
        ok = [[rng.random() < 0.7 for _ in range(m)] for _ in range(n)]
        rows, cols = list(range(n)), list(range(m))
        matches, fr, fc = min_cost_matching(lambda i, j: c[i][j], lambda i, j: ok[i][j], rows, cols)
        best, top = brute_min_cost(lambda i, j: c[i][j], lambda i, j: ok[i][j], rows, cols)
        k = min(n, m)
        got = sum(c[i][j] for i, j in matches) + top * (k - len(matches))
        assert abs(got - best) < 1e-9
        assert all(ok[i][j] for i, j in matches)
        assert sorted(fr + [i for i, _ in matches]) == rows
        assert sorted(fc + [j for _, j in matches]) == cols


def test_hungarian_against_brute_force():
    rng = random.Random(2)
    for _ in range(100):
        n, m = rng.randint(1, 5), rng.randint(1, 5)
        c = [[rng.random() for _ in range(m)] for _ in range(n)]
        pairs = hungarian_min(c)
        if n <= m:
            best = min(sum(c[i][j] for i, j in enumerate(p)) for p in itertools.permutations(range(m), n))
        else:
            best = min(sum(c[i][j] for j, i in enumerate(p)) for p in itertools.permutations(range(n), m))
        assert abs(sum(c[i][j] for i, j in pairs) - best) < 1e-9


def test_page_example_cascade_priority_and_lost_pair():
    # Track 0 was updated one frame ago, track 1 two frames ago. Detections a = 0, b = 1.
    c = {(0, 0): 0.10, (0, 1): 0.12, (1, 0): 0.05}
    cost = lambda i, j: c[(i, j)]  # noqa: E731
    allowed = lambda i, j: (i, j) in c  # noqa: E731
    matches, um_tracks, free = matching_cascade({0: 1, 1: 2}, cost, allowed, [0, 1], 30)
    assert matches == [(0, 0)] and um_tracks == [1] and free == [1]
    # One assignment over both tracks keeps two pairs, at total cost 0.17.
    flat, _, _ = min_cost_matching(cost, allowed, [0, 1], [0, 1])
    assert sorted(flat) == [(0, 1), (1, 0)]
    assert abs(sum(c[p] for p in flat) - 0.17) < 1e-12


def test_uncertain_track_has_a_wider_gate():
    # The same offset has a smaller Mahalanobis distance for a track that was
    # predicted more times without an update, which is why the cascade is needed.
    mean, cov = kf_initiate(box_to_xyah((100.0, 50.0, 120.0, 90.0)))
    for k in range(1, 6):
        mean, cov = kf_predict(mean, cov)
        mean, cov = kf_update(mean, cov, box_to_xyah((100.0 + 2 * k, 50.0, 120.0 + 2 * k, 90.0)))
    dists = []
    m2, c2 = mean, cov
    for _ in range(10):
        m2, c2 = kf_predict(m2, c2)
        dists.append(mahalanobis_sq(m2, c2, [m2[0] + 10.0, m2[1] + 10.0, m2[2], m2[3]]))
    assert all(a > b for a, b in zip(dists, dists[1:]))
    # The page example: about 15.0 after one prediction, 9.0 after two, 1.0 after ten.
    assert dists[0] > CHI2_95_4DOF > dists[1]
    assert abs(dists[0] - 14.98) < 0.01 and abs(dists[1] - 8.99) < 0.01 and abs(dists[9] - 1.03) < 0.01
    assert all(abs(cov[i][j] - cov[j][i]) < 1e-9 for i in range(8) for j in range(8))


def unit(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v]


def make_sequence(seed, hide=range(10, 20)):
    """Two people, 20 by 40 boxes, 40 frames, 8-dim embeddings.

    Person 0 walks right at 2 pixels per frame and is not detected in the frames
    in `hide`. Person 1 stands at x = 60 to 80 and walks down slowly.
    """
    rng = random.Random(seed)
    base = [unit([rng.gauss(0, 1) for _ in range(8)]) for _ in range(2)]
    frames, truth = [], []
    for f in range(40):
        gt = [(10.0 + 2 * f, 50.0, 30.0 + 2 * f, 90.0), (60.0, 52.0 + 0.2 * f, 80.0, 92.0 + 0.2 * f)]
        dets = []
        for k, b in enumerate(gt):
            if k == 0 and f in hide:
                continue
            box = tuple(x + rng.gauss(0.0, 0.7) for x in b)
            emb = unit([x + rng.gauss(0.0, 0.05) for x in base[k]])
            dets.append((box, emb))
        rng.shuffle(dets)
        frames.append(dets)
        truth.append(gt)
    return frames, truth


def run(tracker, frames, truth):
    ids = {0: set(), 1: set()}
    for f, dets in enumerate(frames):
        for tid, box in tracker.step(dets):
            best = max(range(2), key=lambda k: iou(box, truth[f][k]))
            assert iou(box, truth[f][best]) > 0.5
            ids[best].add(tid)
    return ids


def test_reidentifies_after_occlusion():
    # Person 0 passes behind person 1 and is not detected for 10 frames.
    frames, truth = make_sequence(4)
    tr = DeepSortTracker()
    ids = run(tr, frames, truth)
    assert len(ids[0]) == 1 and len(ids[1]) == 1 and ids[0] != ids[1]
    assert tr.next_id == 3
    assert all(t.state == CONFIRMED for t in tr.tracks)


def test_short_memory_loses_the_identity():
    # With max_age = 1, as in SORT, the same occlusion gives person 0 a new identity.
    frames, truth = make_sequence(4)
    ids = run(DeepSortTracker(max_age=1), frames, truth)
    assert len(ids[0]) == 2 and len(ids[1]) == 1


def test_tentative_track_needs_n_init_hits():
    tr = DeepSortTracker()
    det = ((0.0, 0.0, 10.0, 20.0), [1.0, 0.0])
    assert tr.step([det]) == []
    assert tr.step([det]) == []
    out = tr.step([det])
    assert len(out) == 1 and out[0][0] == 1
    # A tentative track that misses one frame is deleted.
    tr2 = DeepSortTracker()
    tr2.step([det])
    tr2.step([])
    assert tr2.tracks == []


def test_gallery_budget():
    tr = DeepSortTracker(budget=5)
    rng = random.Random(1)
    for f in range(12):
        tr.step([((f * 1.0, 0.0, f + 10.0, 20.0), unit([1.0, rng.uniform(-0.01, 0.01)]))])
    assert len(tr.tracks) == 1 and len(tr.tracks[0].gallery) == 5
