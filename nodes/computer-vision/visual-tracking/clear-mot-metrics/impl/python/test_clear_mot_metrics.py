# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/clear-mot-metrics/. The authors are listed in prov/TXWACJ.jsonl.

import itertools
import random
from fractions import Fraction

from clear_mot_metrics import best_matching, clear_mot, iou

HALF = Fraction(1, 2)


def brute_matching(sim, threshold):
    """All matchings of valid pairs; the key is (number of pairs, total sim)."""
    rows = len(sim)
    cols = len(sim[0]) if rows else 0
    best_key, best = (0, Fraction(0)), []
    for k in range(min(rows, cols) + 1):
        for rs in itertools.combinations(range(rows), k):
            for cs in itertools.permutations(range(cols), k):
                pairs = list(zip(rs, cs))
                if all(sim[i][j] >= threshold for i, j in pairs):
                    key = (k, sum((sim[i][j] for i, j in pairs), Fraction(0)))
                    if key > best_key:
                        best_key, best = key, pairs
    return best_key


def key_of(sim, pairs):
    return (len(pairs), sum((sim[i][j] for i, j in pairs), Fraction(0)))


def test_iou_values():
    assert iou((0, 0, 10, 10), (1, 0, 11, 10)) == Fraction(9, 11)
    assert iou((0, 0, 10, 10), (3, 0, 13, 10)) == Fraction(7, 13)
    assert iou((0, 0, 10, 10), (20, 0, 30, 10)) == 0


def test_best_matching_against_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        r, c = rng.randint(0, 4), rng.randint(0, 4)
        sim = [[Fraction(rng.randint(0, 10), 10) for _ in range(c)] for _ in range(r)]
        if r == 0:
            sim = []
        pairs = best_matching(sim, HALF)
        assert len({i for i, _ in pairs}) == len(pairs) == len({j for _, j in pairs})
        assert all(sim[i][j] >= HALF for i, j in pairs)
        assert key_of(sim, pairs) == brute_matching(sim, HALF)


PAGE_GT = [
    {1: (0, 0, 10, 10), 2: (20, 0, 30, 10)},
    {1: (2, 0, 12, 10), 2: (22, 0, 32, 10)},
    {1: (4, 0, 14, 10), 2: (24, 0, 34, 10)},
]
PAGE_HYP = [
    {"a": (1, 0, 11, 10), "b": (20, 0, 30, 10), "c": (50, 50, 60, 60)},
    {"b": (22, 0, 32, 10)},
    {"d": (4, 0, 14, 10), "b": (25, 0, 35, 10)},
]


def test_page_example():
    r = clear_mot(PAGE_GT, PAGE_HYP)
    assert (r["gt"], r["matches"], r["fn"], r["fp"], r["idsw"]) == (6, 5, 1, 1, 1)
    assert r["mota"] == HALF
    assert r["motp"] == Fraction(51, 55)


def test_previous_pairs_are_kept():
    gt = [{1: (0, 0, 10, 10)}, {1: (0, 0, 10, 10)}]
    hyp = [{"h": (0, 0, 10, 10)}, {"h": (3, 0, 13, 10), "g": (1, 0, 11, 10)}]
    kept = clear_mot(gt, hyp)
    assert (kept["idsw"], kept["fp"], kept["mota"]) == (0, 1, HALF)
    assert kept["motp"] == (1 + Fraction(7, 13)) / 2
    plain = clear_mot(gt, hyp, keep_previous=False)
    assert (plain["idsw"], plain["fp"], plain["mota"]) == (1, 1, 0)


def test_switch_is_counted_against_the_last_match():
    box = (0, 0, 10, 10)
    gt = [{1: box}] * 4
    hyp = [{"a": box}, {}, {"a": box}, {"b": box}]
    r = clear_mot(gt, hyp)
    assert (r["matches"], r["fn"], r["idsw"]) == (3, 1, 1)


def test_bounds_of_mota():
    box = (0, 0, 10, 10)
    gt = [{1: box}] * 3
    assert clear_mot(gt, [{"a": box}] * 3)["mota"] == 1
    assert clear_mot(gt, [{}] * 3)["mota"] == 0
    far = {"x": (50, 0, 60, 10), "y": (70, 0, 80, 10), "z": (90, 0, 100, 10)}
    assert clear_mot(gt, [dict(far, a=box)] * 3)["mota"] == -2


def random_box(rng):
    x, y = rng.randint(0, 12), rng.randint(0, 12)
    return (x, y, x + rng.randint(3, 6), y + rng.randint(3, 6))


def reference(gt_frames, hyp_frames, threshold):
    """The same procedure with a brute force matching in each frame; returns the counts."""
    previous, last = {}, {}
    out = [0, 0, 0, 0, 0, Fraction(0)]
    for gt, hyp in zip(gt_frames, hyp_frames):
        cur = {o: h for o, h in previous.items() if o in gt and h in hyp and iou(gt[o], hyp[h]) >= threshold}
        objs = [o for o in sorted(gt) if o not in cur]
        hyps = [h for h in sorted(hyp) if h not in cur.values()]
        sim = [[iou(gt[o], hyp[h]) for h in hyps] for o in objs]
        best_key, best = (-1, 0), []
        for k in range(min(len(objs), len(hyps)) + 1):
            for rs in itertools.combinations(range(len(objs)), k):
                for cs in itertools.permutations(range(len(hyps)), k):
                    pairs = list(zip(rs, cs))
                    if all(sim[i][j] >= threshold for i, j in pairs):
                        key = key_of(sim, pairs)
                        if key > best_key:
                            best_key, best = key, pairs
        for i, j in best:
            cur[objs[i]] = hyps[j]
        for o, h in cur.items():
            out[4] += o in last and last[o] != h
            last[o] = h
            out[5] += iou(gt[o], hyp[h])
        out[0] += len(gt)
        out[1] += len(cur)
        out[2] += len(gt) - len(cur)
        out[3] += len(hyp) - len(cur)
        previous = cur
    return out


def random_sequence(rng):
    """Objects that move a little; a tracker that copies them with jitter, sometimes
    with another identity, sometimes not at all, plus random false positives."""
    start = {o: random_box(rng) for o in range(4)}
    names = {o: "abcd"[o] for o in range(4)}
    gt_frames, hyp_frames = [], []
    for t in range(rng.randint(1, 6)):
        gt, hyp = {}, {}
        for o, b in start.items():
            if rng.random() < 0.8:
                gt[o] = (b[0] + t, b[1], b[2] + t, b[3])
                if rng.random() < 0.15:
                    names[o] = rng.choice("abcdef")
                if rng.random() < 0.8 and names[o] not in hyp:
                    dx = rng.randint(-1, 1)
                    g = gt[o]
                    hyp[names[o]] = (g[0] + dx, g[1], g[2] + dx, g[3] + rng.randint(-1, 1))
        if rng.random() < 0.4:
            hyp["z"] = random_box(rng)
        gt_frames.append(gt)
        hyp_frames.append(hyp)
    return gt_frames, hyp_frames


def test_against_reference_and_invariants():
    rng = random.Random(2)
    switches = 0
    for _ in range(80):
        gt_frames, hyp_frames = random_sequence(rng)
        r = clear_mot(gt_frames, hyp_frames)
        ref = reference(gt_frames, hyp_frames, HALF)
        assert [r[k] for k in ("gt", "matches", "fn", "fp", "idsw", "sum_iou")] == ref
        switches += r["idsw"]
        hyp_total = sum(len(h) for h in hyp_frames)
        assert r["fn"] + r["matches"] == r["gt"]
        assert r["fp"] + r["matches"] == hyp_total
        assert r["idsw"] <= r["matches"]
        if r["gt"]:
            assert r["mota"] == 1 - Fraction(r["fn"] + r["fp"] + r["idsw"], r["gt"])
            assert r["mota"] <= 1
        if r["matches"]:
            assert HALF <= r["motp"] <= 1
    assert switches >= 5  # the sequences do exercise identity switches
