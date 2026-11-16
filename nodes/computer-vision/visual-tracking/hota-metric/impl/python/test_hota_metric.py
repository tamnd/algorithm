# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hota-metric/. The authors are listed in prov/SAT5C8.jsonl.

import itertools
import math
import random
from fractions import Fraction

from hota_metric import (ALPHAS, frame_matching, hota, hota_alpha, iou, lengths,
                         match_score, potential_counts)

P1 = (0, 0, 10, 10)
P2 = (40, 0, 50, 10)


def a_max_of(gt_frames, pr_frames, alpha):
    glen, plen = lengths(gt_frames), lengths(pr_frames)
    n = potential_counts(gt_frames, pr_frames, alpha)
    return {k: Fraction(v, glen[k[0]] + plen[k[1]] - v) for k, v in n.items()}


def test_page_example_swap():
    gt = [{1: P1, 2: P2}] * 6
    pr = [{"a": P1, "b": P2}] * 4 + [{"a": P2, "b": P1}] * 2
    r = hota(gt, pr)
    for x in r["per_alpha"]:
        assert (x["tp"], x["fn"], x["fp"]) == (12, 0, 0)
        assert x["tpa"] == {(1, "a"): 4, (2, "b"): 4, (1, "b"): 2, (2, "a"): 2}
        assert x["deta"] == 1 and x["assa"] == Fraction(2, 5)
    assert abs(r["hota"] - math.sqrt(0.4)) < 1e-12
    assert r["loca"] == 1


def test_page_example_offset():
    # IoU((0,0,8,10), (2,0,10,10)) = 60 / 100: a true positive for alpha <= 0.6 only
    assert iou((0, 0, 8, 10), (2, 0, 10, 10)) == Fraction(3, 5)
    gt = [{1: (0, 0, 8, 10)}] * 5
    pr = [{"a": (2, 0, 10, 10)}] * 5
    r = hota(gt, pr)
    assert [x["hota_sq"] for x in r["per_alpha"]] == [1] * 12 + [0] * 7
    assert abs(r["hota"] - 12 / 19) < 1e-12
    assert r["deta"] == Fraction(12, 19) and r["assa"] == Fraction(12, 19)
    assert r["loca"] == Fraction(3, 5)


def test_perfect_and_empty():
    gt = [{1: P1, 2: P2}] * 3
    assert hota(gt, gt)["hota"] == 1
    assert hota(gt, [{}] * 3)["hota"] == 0


def random_box(rng):
    x, y = rng.randint(0, 10), rng.randint(0, 10)
    return (x, y, x + rng.randint(3, 6), y + rng.randint(3, 6))


def random_sequence(rng, objects=3, frames=6):
    start = {o: random_box(rng) for o in range(objects)}
    names = {o: "abcde"[o] for o in range(objects)}
    gt_frames, pr_frames = [], []
    for t in range(rng.randint(1, frames)):
        gt, pr = {}, {}
        for o, b in start.items():
            if rng.random() < 0.8:
                gt[o] = (b[0] + t, b[1], b[2] + t, b[3])
                if rng.random() < 0.2:
                    names[o] = rng.choice("abcdef")
                if rng.random() < 0.8 and names[o] not in pr:
                    dx = rng.randint(-2, 2)
                    pr[names[o]] = (gt[o][0] + dx, gt[o][1], gt[o][2] + dx, gt[o][3] + rng.randint(-1, 1))
        if rng.random() < 0.3:
            pr["z"] = random_box(rng)
        gt_frames.append(gt)
        pr_frames.append(pr)
    return gt_frames, pr_frames


def brute_frame_matching(gt, pr, alpha, a_max):
    gs, ps = list(gt), list(pr)
    best_count, best_score = 0, Fraction(0)
    for k in range(min(len(gs), len(ps)) + 1):
        for rs in itertools.combinations(gs, k):
            for cs in itertools.permutations(ps, k):
                pairs = list(zip(rs, cs))
                if all(iou(gt[g], pr[p]) >= alpha for g, p in pairs):
                    best_count = max(best_count, k)
                    s = sum((match_score(iou(gt[g], pr[p]), a_max.get((g, p), 0)) for g, p in pairs), Fraction(0))
                    best_score = max(best_score, s)
    return best_count, best_score


def test_frame_matching_against_brute_force():
    rng = random.Random(1)
    for _ in range(25):
        gt_frames, pr_frames = random_sequence(rng, objects=4)
        alpha = rng.choice(ALPHAS)
        a_max = a_max_of(gt_frames, pr_frames, alpha)
        for gt, pr in zip(gt_frames, pr_frames):
            pairs = frame_matching(gt, pr, alpha, a_max)
            score = sum((match_score(iou(gt[g], pr[p]), a_max.get((g, p), 0)) for g, p in pairs), Fraction(0))
            count, best = brute_frame_matching(gt, pr, alpha, a_max)
            assert score == best
            assert len(pairs) == count  # the most true positives come first


def test_association_scores_from_the_set_definitions():
    rng = random.Random(2)
    for _ in range(25):
        gt_frames, pr_frames = random_sequence(rng)
        alpha = rng.choice(ALPHAS)
        r = hota_alpha(gt_frames, pr_frames, alpha)
        a_max = a_max_of(gt_frames, pr_frames, alpha)
        tps, fns, fps = [], [], []
        for t, (gt, pr) in enumerate(zip(gt_frames, pr_frames)):
            pairs = frame_matching(gt, pr, alpha, a_max)
            tps += [(t, g, p) for g, p in pairs]
            fns += [(t, g) for g in gt if g not in {g2 for g2, _ in pairs}]
            fps += [(t, p) for p in pr if p not in {p2 for _, p2 in pairs}]
        sum_a = Fraction(0)
        for _, g, p in tps:
            tpa = [k for k in tps if k[1] == g and k[2] == p]
            fna = [k for k in tps if k[1] == g and k[2] != p] + [k for k in fns if k[1] == g]
            fpa = [k for k in tps if k[2] == p and k[1] != g] + [k for k in fps if k[1] == p]
            sum_a += Fraction(len(tpa), len(tpa) + len(fna) + len(fpa))
        assert (r["tp"], r["fn"], r["fp"]) == (len(tps), len(fns), len(fps))
        total = len(tps) + len(fns) + len(fps)
        if total:
            assert r["hota_sq"] == sum_a / total
        if tps:
            assert r["assa"] == sum_a / len(tps)
            assert r["hota_sq"] == r["deta"] * r["assa"]
        assert 0 <= r["deta"] <= 1 and 0 <= r["assa"] <= 1


def test_detection_accuracy_does_not_grow_with_alpha():
    rng = random.Random(3)
    for _ in range(10):
        gt_frames, pr_frames = random_sequence(rng)
        r = hota(gt_frames, pr_frames)
        deta = [x["deta"] for x in r["per_alpha"]]
        assert all(a >= b for a, b in zip(deta, deta[1:]))
        assert 0 <= r["hota"] <= 1
