# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sort-tracker/. The authors are listed in prov/2C1PFP.jsonl.

import itertools
import math
import random
from fractions import Fraction

from sort_tracker import (
    SortTracker,
    Track,
    associate,
    box_to_z,
    hungarian_min,
    iou,
    z_to_box,
)


def brute_max_sum(ious):
    """Largest total IoU over all assignments of size min(n, m)."""
    n, m = len(ious), len(ious[0])
    best = -1.0
    if n <= m:
        for cols in itertools.permutations(range(m), n):
            best = max(best, sum(ious[i][c] for i, c in enumerate(cols)))
    else:
        for rows in itertools.permutations(range(n), m):
            best = max(best, sum(ious[r][j] for j, r in enumerate(rows)))
    return best


def test_iou_check_values():
    assert iou(tuple(map(Fraction, (0, 0, 2, 2))), tuple(map(Fraction, (1, 1, 3, 3)))) == Fraction(1, 7)
    assert iou(tuple(map(Fraction, (0, 0, 10, 10))), tuple(map(Fraction, (5, 0, 15, 10)))) == Fraction(1, 3)
    assert iou((0, 0, 1, 1), (2, 2, 3, 3)) == 0


def test_state_round_trip():
    box = (4.0, 0.0, 14.0, 10.0)
    assert box_to_z(box) == [9.0, 5.0, 100.0, 1.0]
    rng = random.Random(1)
    for _ in range(50):
        x1, y1 = rng.uniform(-50, 50), rng.uniform(-50, 50)
        b = (x1, y1, x1 + rng.uniform(1, 40), y1 + rng.uniform(1, 40))
        assert all(abs(p - q) < 1e-9 for p, q in zip(z_to_box(box_to_z(b)), b))


def test_hungarian_against_brute_force():
    rng = random.Random(7)
    for _ in range(200):
        n, m = rng.randint(1, 5), rng.randint(1, 5)
        c = [[rng.random() for _ in range(m)] for _ in range(n)]
        pairs = hungarian_min([[-x for x in row] for row in c])
        assert len(pairs) == min(n, m)
        assert len({i for i, _ in pairs}) == len(pairs) == len({j for _, j in pairs})
        assert abs(sum(c[i][j] for i, j in pairs) - brute_max_sum(c)) < 1e-9


def test_page_example_global_beats_greedy():
    preds = [(0, 0, 10, 10), (6, 0, 16, 10)]
    dets = [(4, 0, 14, 10), (9, 0, 19, 10), (40, 40, 50, 50)]
    fr = [tuple(map(Fraction, b)) for b in preds]
    fd = [tuple(map(Fraction, b)) for b in dets]
    assert [[iou(p, d) for d in fd] for p in fr] == [
        [Fraction(3, 7), Fraction(1, 19), 0],
        [Fraction(2, 3), Fraction(7, 13), 0],
    ]
    matches, um_t, um_d, _ = associate(preds, dets, 0.3)
    assert matches == [(0, 0), (1, 1)] and um_t == [] and um_d == [2]
    # The greedy rule takes the largest IoU first, (B, d1), and then A is left
    # with d2 at IoU 1/19 < 0.3, so A loses its detection.
    assert max((iou(p, d), i, j) for i, p in enumerate(preds) for j, d in enumerate(dets))[1:] == (1, 0)


def test_iou_min_filter_keeps_only_strong_pairs():
    rng = random.Random(3)
    for _ in range(100):
        preds, dets = [], []
        for _ in range(rng.randint(1, 4)):
            x, y = rng.uniform(0, 60), rng.uniform(0, 60)
            preds.append((x, y, x + 10, y + 10))
        for _ in range(rng.randint(1, 4)):
            x, y = rng.uniform(0, 60), rng.uniform(0, 60)
            dets.append((x, y, x + 10, y + 10))
        matches, um_t, um_d, ious = associate(preds, dets, 0.3)
        assert all(ious[i][j] >= 0.3 for i, j in matches)
        assert sorted([i for i, _ in matches] + um_t) == list(range(len(preds)))
        assert sorted([j for _, j in matches] + um_d) == list(range(len(dets)))


def test_filter_after_assignment_differs_from_gating_first():
    # Claim 3 of the proof: tracks A, B and detections a, b with IoU_min = 0.3.
    c = [[0.9, 0.5], [0.5, 0.25]]
    pairs = hungarian_min([[-x for x in row] for row in c])
    assert pairs == [(0, 0), (1, 1)]
    kept = [(i, j) for i, j in pairs if c[i][j] >= 0.3]
    assert kept == [(0, 0)]
    big = 1e6  # forbid the weak pair before the assignment
    gated = hungarian_min([[-x if x >= 0.3 else big for x in row] for row in c])
    assert [(i, j) for i, j in gated if c[i][j] >= 0.3] == [(0, 1), (1, 0)]


def test_kalman_constant_velocity_converges():
    t = Track((0.0, 0.0, 10.0, 20.0), 1)
    for k in range(1, 40):
        t.predict()
        t.update((3.0 * k, 2.0 * k, 3.0 * k + 10.0, 2.0 * k + 20.0))
    assert abs(t.x[4] - 3.0) < 1e-2 and abs(t.x[5] - 2.0) < 1e-2 and abs(t.x[6]) < 1e-2
    p = t.predict()
    assert all(abs(a - b) < 0.05 for a, b in zip(p, (120.0, 80.0, 130.0, 100.0)))
    # P stays symmetric
    assert all(abs(t.P[i][j] - t.P[j][i]) < 1e-9 for i in range(7) for j in range(7))


def make_sequence(seed):
    """Three boxes with constant velocity, 30 frames, noise of 1 pixel on the corners.

    Object 0 is missed in frame 12. A false box appears in frame 20 only.
    Objects 0 and 1 pass each other; their boxes overlap with IoU at most 1/7.
    """
    rng = random.Random(seed)
    starts = [(10.0, 20.0, 3.0, 0.0), (150.0, 50.0, -3.0, 0.0), (80.0, 0.0, 1.0, 0.5)]
    frames, truth = [], []
    for f in range(30):
        dets, gt = [], []
        for k, (x, y, vx, vy) in enumerate(starts):
            b = (x + vx * f, y + vy * f, x + vx * f + 20.0, y + vy * f + 40.0)
            gt.append(b)
            if k == 0 and f == 12:
                continue
            dets.append(tuple(c + rng.gauss(0.0, 1.0) for c in b))
        if f == 20:
            dets.append((300.0, 300.0, 320.0, 340.0))
        rng.shuffle(dets)
        frames.append(dets)
        truth.append(gt)
    return frames, truth


def test_sequence_keeps_identities():
    frames, truth = make_sequence(11)
    tr = SortTracker()
    ids = {0: set(), 1: set(), 2: set()}
    errors = []
    for f, dets in enumerate(frames):
        out = tr.step(dets)
        for tid, box in out:
            best = max(range(3), key=lambda k: iou(box, truth[f][k]))
            assert iou(box, truth[f][best]) > 0.5  # no output on the false box
            ids[best].add(tid)
            cu, cv = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
            g = truth[f][best]
            errors.append(math.hypot(cu - (g[0] + g[2]) / 2, cv - (g[1] + g[3]) / 2))
    assert all(len(s) == 1 for s in ids.values())  # one identity per object, no switch
    assert len(set().union(*ids.values())) == 3
    assert sum(errors) / len(errors) < 1.5
    # the track of object 0 survives the missed frame 12 (max_age = 1)
    assert tr.next_id == 5  # three objects and the false box of frame 20


def test_track_deleted_after_two_misses():
    tr = SortTracker()
    box = (0.0, 0.0, 10.0, 10.0)
    for _ in range(4):
        tr.step([box])
    assert len(tr.tracks) == 1
    tr.step([])
    assert len(tr.tracks) == 1  # one miss is allowed
    tr.step([])
    assert tr.tracks == []
