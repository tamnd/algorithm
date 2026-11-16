# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bytetrack/. The authors are listed in prov/0E34WD.jsonl.

import itertools
import random
from fractions import Fraction

from bytetrack import ByteTracker, iou, iou_matching


def brute_best_weight(boxes_a, boxes_b, rows, cols, iou_min):
    """Largest total of IoU - iou_min over all matchings that use pairs with IoU >= iou_min."""
    best = 0.0
    for k in range(1, min(len(rows), len(cols)) + 1):
        for rs in itertools.combinations(rows, k):
            for cs in itertools.permutations(cols, k):
                ws = [iou(boxes_a[i], boxes_b[j]) - iou_min for i, j in zip(rs, cs)]
                if all(w >= 0 for w in ws):
                    best = max(best, sum(ws))
    return best


def test_iou_values():
    assert iou(tuple(map(Fraction, (0, 0, 2, 2))), tuple(map(Fraction, (1, 1, 3, 3)))) == Fraction(1, 7)
    assert iou(tuple(map(Fraction, (0, 0, 10, 10))), tuple(map(Fraction, (5, 0, 15, 10)))) == Fraction(1, 3)


def test_matching_against_brute_force():
    rng = random.Random(8)
    for _ in range(150):
        a = []
        for _ in range(rng.randint(1, 4)):
            x, y = rng.uniform(0, 30), rng.uniform(0, 30)
            a.append((x, y, x + 10, y + 10))
        b = []
        for _ in range(rng.randint(1, 4)):
            x, y = rng.uniform(0, 30), rng.uniform(0, 30)
            b.append((x, y, x + 10, y + 10))
        rows, cols = list(range(len(a))), list(range(len(b)))
        for bound in (0.2, 0.5):
            m, fr, fc = iou_matching(a, b, rows, cols, bound)
            assert all(iou(a[i], b[j]) >= bound for i, j in m)
            assert len({i for i, _ in m}) == len(m) == len({j for _, j in m})
            got = sum(iou(a[i], b[j]) - bound for i, j in m)
            assert abs(got - brute_best_weight(a, b, rows, cols, bound)) < 1e-9
            assert sorted(fr + [i for i, _ in m]) == rows and sorted(fc + [j for _, j in m]) == cols


def warm_up(tracker, boxes, frames=3):
    for _ in range(frames):
        tracker.step([(b, 0.9) for b in boxes])


def test_page_example_second_association():
    a_box, b_box = (0.0, 0.0, 10.0, 20.0), (30.0, 0.0, 40.0, 20.0)
    frame = [((31.0, 1.0, 41.0, 21.0), 0.9), ((2.0, 0.0, 12.0, 20.0), 0.4), ((80.0, 80.0, 90.0, 100.0), 0.15)]
    assert iou(tuple(map(Fraction, (0, 0, 10, 20))), tuple(map(Fraction, (2, 0, 12, 20)))) == Fraction(2, 3)
    assert iou(tuple(map(Fraction, (30, 0, 40, 20))), tuple(map(Fraction, (31, 1, 41, 21)))) == Fraction(171, 229)
    results = {}
    for use_low in (True, False):
        tr = ByteTracker(use_low=use_low)
        warm_up(tr, [a_box, b_box])
        out = tr.step(frame)
        results[use_low] = (sorted(tid for tid, _ in out), len(tr.tracks), tr.next_id)
    # BYTE keeps both tracks; the low box at (80, 80) starts nothing.
    assert results[True] == ([1, 2], 2, 3)
    # Without the second association, track 1 is lost and not reported.
    assert results[False] == ([2], 2, 3)


def test_low_boxes_never_start_tracks():
    rng = random.Random(3)
    tr = ByteTracker()
    for _ in range(20):
        dets = []
        for _ in range(rng.randint(0, 5)):
            x, y = rng.uniform(0, 500), rng.uniform(0, 500)
            dets.append(((x, y, x + 20, y + 40), rng.uniform(0.0, 0.6)))
        assert tr.step(dets) == []
    assert tr.tracks == [] and tr.next_id == 1


def make_occlusion(seed):
    """Two people, 20 by 40 boxes, 40 frames. Person 0 walks right at 2 pixels
    per frame and is half hidden in frames 12 to 21, where its score is 0.3."""
    rng = random.Random(seed)
    frames, truth = [], []
    for f in range(40):
        gt = [(10.0 + 2 * f, 50.0, 30.0 + 2 * f, 90.0), (200.0, 40.0 + 0.5 * f, 220.0, 80.0 + 0.5 * f)]
        dets = []
        for k, b in enumerate(gt):
            score = 0.3 if (k == 0 and 12 <= f <= 21) else rng.uniform(0.75, 0.95)
            dets.append((tuple(x + rng.gauss(0.0, 0.7) for x in b), score))
        if f % 7 == 3:
            x = rng.uniform(300, 400)
            dets.append(((x, 10.0, x + 20.0, 50.0), 0.2))  # a weak false box
        rng.shuffle(dets)
        frames.append(dets)
        truth.append(gt)
    return frames, truth


def run(tracker, frames, truth):
    ids = {0: set(), 1: set()}
    count = {0: 0, 1: 0}
    for f, dets in enumerate(frames):
        for tid, box in tracker.step(dets):
            best = max(range(2), key=lambda k: iou(box, truth[f][k]))
            assert iou(box, truth[f][best]) > 0.5
            ids[best].add(tid)
            count[best] += 1
    return ids, count


def test_occlusion_low_scores_byte_against_baseline():
    frames, truth = make_occlusion(6)
    ids, count = run(ByteTracker(), frames, truth)
    assert ids == {0: {1}, 1: {2}}
    assert count == {0: 40, 1: 40}
    # The baseline that drops the low boxes misses person 0 for the 10 hidden frames.
    ids_b, count_b = run(ByteTracker(use_low=False), frames, truth)
    assert count_b == {0: 30, 1: 40}
    # The lost track is kept for 30 frames, so the first association finds it again.
    assert ids_b == {0: {1}, 1: {2}}


def test_lost_track_removed_after_max_lost():
    tr = ByteTracker(max_lost=5)
    warm_up(tr, [(0.0, 0.0, 10.0, 20.0)])
    for _ in range(5):
        tr.step([])
    assert len(tr.tracks) == 1
    tr.step([])
    assert tr.tracks == []
