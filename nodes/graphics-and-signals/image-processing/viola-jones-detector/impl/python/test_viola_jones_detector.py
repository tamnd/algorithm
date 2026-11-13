# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/viola-jones-detector/. The authors are listed in prov/3QXCD1.jsonl.

import math
import random
import statistics
from fractions import Fraction

import pytest

from viola_jones_detector import (
    KINDS,
    best_stump,
    boost,
    corner_refs,
    enumerate_features,
    evaluate_cascade,
    feature_value,
    integral_image,
    merge_detections,
    scan,
    stump_predict,
    train_cascade,
    window_sigma,
)


def box(img, x0, y0, x1, y1):
    return sum(img[y][x] for y in range(y0, y1) for x in range(x0, x1))


def direct_value(img, feature, ox, oy):
    """The feature by its definition, with plain pixel sums."""
    kind, x, y, w, h = feature
    x += ox
    y += oy
    if kind == "2h":
        return box(img, x, y, x + w, y + h) - box(img, x + w, y, x + 2 * w, y + h)
    if kind == "2v":
        return box(img, x, y, x + w, y + h) - box(img, x, y + h, x + w, y + 2 * h)
    if kind == "3h":
        return box(img, x + w, y, x + 2 * w, y + h) - box(img, x, y, x + w, y + h) - box(img, x + 2 * w, y, x + 3 * w, y + h)
    if kind == "3v":
        return box(img, x, y + h, x + w, y + 2 * h) - box(img, x, y, x + w, y + h) - box(img, x, y + 2 * h, x + w, y + 3 * h)
    return (box(img, x, y, x + w, y + h) + box(img, x + w, y + h, x + 2 * w, y + 2 * h)
            - box(img, x + w, y, x + 2 * w, y + h) - box(img, x, y + h, x + w, y + 2 * h))


def test_feature_values_match_direct_rectangle_sums():
    rng = random.Random(1)
    img = [[rng.randint(0, 255) for _ in range(9)] for _ in range(8)]
    s = integral_image(img)
    feats = enumerate_features(6)
    assert len(feats) == 669
    for ox, oy in ((0, 0), (3, 2), (1, 1)):
        for f in feats:
            assert feature_value(s, f, ox, oy) == direct_value(img, f, ox, oy)


def test_array_references_6_8_9():
    want = {"2h": 6, "2v": 6, "3h": 8, "3v": 8, "4": 9}
    for f in enumerate_features(7):
        assert len(corner_refs(f)) == want[f[0]]


def test_feature_count_for_24_by_24():
    per = {k: len(enumerate_features(24, (k,))) for k in KINDS}
    assert per == {"2h": 43200, "2v": 43200, "3h": 27600, "3v": 27600, "4": 20736}
    assert sum(per.values()) == 162336


def test_window_sigma_matches_population_deviation():
    rng = random.Random(2)
    img = [[rng.randint(0, 255) for _ in range(10)] for _ in range(9)]
    s1 = integral_image(img)
    s2 = integral_image([[v * v for v in r] for r in img])
    for ox, oy, size in ((0, 0, 9), (2, 1, 5), (4, 4, 3)):
        vals = [img[y][x] for y in range(oy, oy + size) for x in range(ox, ox + size)]
        assert abs(window_sigma(s1, s2, ox, oy, size) - statistics.pstdev(vals)) < 1e-9
    flat = integral_image([[7] * 4 for _ in range(4)])
    flat2 = integral_image([[49] * 4 for _ in range(4)])
    assert window_sigma(flat, flat2, 0, 0, 4) == 1.0


def brute_stump_error(values, labels, weights):
    vs = sorted(set(values))
    cands = [vs[0] - 1, vs[-1] + 1] + [(a + b) / 2 for a, b in zip(vs, vs[1:])]
    best = None
    for theta in cands:
        for p in (1, -1):
            err = sum(w for v, y, w in zip(values, labels, weights) if stump_predict(v, p, theta) != y)
            if best is None or err < best:
                best = err
    return best


@pytest.mark.parametrize("seed", range(8))
def test_stump_equals_brute_force_over_thresholds(seed):
    rng = random.Random(10 + seed)
    m = rng.randint(2, 14)
    values = [Fraction(rng.randint(-5, 5)) for _ in range(m)]
    labels = [rng.randint(0, 1) for _ in range(m)]
    weights = [Fraction(rng.randint(1, 9)) for _ in range(m)]
    tot = sum(weights)
    weights = [w / tot for w in weights]
    err, p, theta = best_stump(values, labels, weights)
    assert err == brute_stump_error(values, labels, weights)
    # The chosen stump has that error when it is evaluated directly.
    assert err == sum(w for v, y, w in zip(values, labels, weights) if stump_predict(v, p, theta) != y)


def test_adaboost_weights_follow_table_1():
    rng = random.Random(3)
    n_pos, n_neg, n_feat = 7, 11, 5
    labels = [1] * n_pos + [0] * n_neg
    table = [[Fraction(rng.randint(0, 20)) + (3 if labels[i] and f == 0 else 0) for i in range(len(labels))]
             for f in range(n_feat)]
    rows = list(range(len(labels)))
    states = []
    for st in boost(table, labels, rows):
        states.append(st)
        if len(states) == 6:
            break
    assert len(states) >= 2
    first = states[0]["weights"]
    assert first[:n_pos] == [Fraction(1, 2 * n_pos)] * n_pos
    assert first[n_pos:] == [Fraction(1, 2 * n_neg)] * n_neg
    for a, b in zip(states, states[1:]):
        f, p, theta, alpha = a["weak"][-1]
        eps = a["eps"]
        assert 0 < eps < Fraction(1, 2)
        assert abs(alpha - math.log((1 - eps) / eps)) < 1e-12
        # After the update, the stump just chosen has weighted error exactly 1/2.
        w = b["weights"]
        assert sum(w) == 1
        err = sum(wi for i, wi in enumerate(w) if stump_predict(table[f][i], p, theta) != labels[i])
        assert err == Fraction(1, 2)


def hand_cascade():
    f = [("2h", 0, 0, 1, 1), ("2v", 0, 0, 1, 1), ("4", 0, 0, 1, 1), ("3h", 0, 0, 1, 1), ("3v", 0, 0, 1, 1)]
    return [
        {"weak": [(f[0], 1, 0.0, 1.0)], "threshold": 0.5},
        {"weak": [(f[1], 1, 0.0, 1.0), (f[2], -1, 0.0, 2.0)], "threshold": 1.5},
        {"weak": [(f[3], 1, 1.0, 1.0), (f[4], 1, 1.0, 1.0), (f[0], -1, -5.0, 1.0)], "threshold": 2.0},
    ]


def test_window_rejected_early_is_never_seen_by_later_stages():
    stages = hand_cascade()
    stage_of = {}
    for k, st in enumerate(stages):
        for feat, *_ in st["weak"]:
            stage_of.setdefault(feat, k)
    rng = random.Random(4)
    seen_runs = set()
    for _ in range(300):
        vals = {feat: rng.uniform(-3, 3) for feat in stage_of}
        calls = []

        def value_of(feat):
            calls.append(feat)
            return vals[feat]

        ok, run = evaluate_cascade(stages, value_of)
        seen_runs.add(run)
        assert len(calls) == sum(len(st["weak"]) for st in stages[:run])
        assert all(stage_of[c] < run for c in calls)
        if not ok:
            k = run - 1
            assert sum(a for feat, p, th, a in stages[k]["weak"] if stump_predict(vals[feat], p, th)) < stages[k]["threshold"]
    assert seen_runs == {1, 2, 3}


def test_expected_cost_identity():
    stages = hand_cascade()
    sizes = [len(st["weak"]) for st in stages]
    rng = random.Random(5)
    feats = {feat for st in stages for feat, *_ in st["weak"]}
    runs = []
    total = 0
    for _ in range(500):
        vals = {feat: rng.uniform(-3, 3) for feat in feats}
        count = [0]

        def value_of(feat):
            count[0] += 1
            return vals[feat]

        _, run = evaluate_cascade(stages, value_of)
        runs.append(run)
        total += count[0]
    reach = [sum(1 for r in runs if r > i) for i in range(len(stages))]
    assert reach[0] == len(runs)
    rates = [Fraction(reach[i + 1], reach[i]) for i in range(len(stages) - 1)]
    expected = sum(sizes[i] * math.prod(rates[:i]) for i in range(len(stages)))
    assert Fraction(total, len(runs)) == expected


N = 8
BASE = [[150] * N for _ in range(N)]
for _y in (2, 3):
    for _x in (1, 2, 5, 6):
        BASE[_y][_x] = 40
for _x in range(2, 6):
    BASE[6][_x] = 70


def pattern(rng):
    return [[max(0, min(255, BASE[y][x] + rng.randint(-40, 40))) for x in range(N)] for y in range(N)]


def shifted(rng):
    big = [[150 + rng.randint(-40, 40) for _ in range(16)] for _ in range(16)]
    p = pattern(rng)
    for y in range(N):
        for x in range(N):
            big[4 + y][4 + x] = p[y][x]
    while True:
        dx, dy = rng.randint(-4, 4), rng.randint(-4, 4)
        if max(abs(dx), abs(dy)) >= 3:
            break
    return [row[4 + dx:12 + dx] for row in big[4 + dy:12 + dy]]


@pytest.fixture(scope="module")
def trained():
    rng = random.Random(5)
    pos = [pattern(rng) for _ in range(30)]
    neg = [[[rng.randint(0, 255) for _ in range(N)] for _ in range(N)] for _ in range(40)]
    neg += [shifted(rng) for _ in range(80)]
    feats = enumerate_features(N)[::8]
    stages = train_cascade(pos, neg, feats, max_stages=4, max_rounds=10, stage_fp=Fraction(1, 5))
    return rng, pos, neg, stages


def test_trained_cascade_accepts_all_training_positives(trained):
    from viola_jones_detector import window_values
    _, pos, neg, stages = trained
    assert stages
    for win in pos:
        s1 = integral_image(win)
        s2 = integral_image([[v * v for v in r] for r in win])
        sig = window_sigma(s1, s2, 0, 0, N)
        ok, _ = evaluate_cascade(stages, lambda f: feature_value(s1, f) / sig)
        assert ok


def test_planted_pattern_is_detected(trained):
    rng, _, _, stages = trained
    img = [[150 + rng.randint(-40, 40) for _ in range(30)] for _ in range(26)]
    p = pattern(rng)
    for y in range(N):
        for x in range(N):
            img[7 + y][11 + x] = p[y][x]
    dets, cost = scan(img, stages, N)
    assert (11, 7, 8) in dets
    merged = merge_detections(dets)
    assert any(x0 <= 15 <= x1 and y0 <= 11 <= y1 for x0, y0, x1, y1 in merged)
    # Window count: scale 1 (stride 1), 1.25 (stride 1), 1.5625 (stride 2), 1.953125 (stride 2), 2.44 (stride 2), 3.05 (stride 3).
    count = 0
    s = 1.0
    while int(N * s) <= 26:
        size, stride = int(N * s), max(1, int(s + 0.5))
        count += len(range(0, 30 - size + 1, stride)) * len(range(0, 26 - size + 1, stride))
        s *= 1.25
    assert len(cost) == count


def test_merge_groups_overlapping_boxes_transitively():
    dets = [(0, 0, 4), (3, 3, 4), (6, 6, 4), (20, 20, 4), (21, 20, 4)]
    merged = merge_detections(dets)
    assert merged == [(Fraction(3), Fraction(3), Fraction(7), Fraction(7)),
                      (Fraction(41, 2), Fraction(20), Fraction(49, 2), Fraction(24))]
    # Touching edges do not overlap.
    assert len(merge_detections([(0, 0, 4), (4, 0, 4)])) == 2
