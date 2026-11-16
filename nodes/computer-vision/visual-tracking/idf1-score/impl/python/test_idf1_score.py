# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/idf1-score/. The authors are listed in prov/QK543C.jsonl.

import itertools
import random
from fractions import Fraction

from idf1_score import idf1, iou, max_overlap_matching, min_cost_with_dummy_nodes, overlap_counts

HALF = Fraction(1, 2)
P1 = (0, 0, 10, 10)
P2 = (40, 0, 50, 10)


def brute_max_total(n):
    rows = len(n)
    cols = len(n[0]) if rows else 0
    best = 0
    for k in range(min(rows, cols) + 1):
        for rs in itertools.combinations(range(rows), k):
            for cs in itertools.permutations(range(cols), k):
                best = max(best, sum(n[i][j] for i, j in zip(rs, cs)))
    return best


def test_page_example_swap():
    # object 1 stays at P1 and object 2 at P2; a and b swap after frame 4
    gt = [{1: P1, 2: P2}] * 6
    hyp = [{"a": P1, "b": P2}] * 4 + [{"a": P2, "b": P1}] * 2
    r = idf1(gt, hyp)
    assert r["matching"] == [(1, "a"), (2, "b")]
    assert (r["idtp"], r["idfn"], r["idfp"]) == (8, 4, 4)
    assert r["idf1"] == r["idp"] == r["idr"] == Fraction(2, 3)


def test_one_switch_against_one_false_positive():
    gt = [{1: P1}] * 100
    switch = [{"a": P1}] * 50 + [{"b": P1}] * 50
    assert idf1(gt, switch)["idf1"] == HALF
    extra = [{"a": P1}] * 100
    extra[37] = {"a": P1, "z": P2}
    assert idf1(gt, extra)["idf1"] == Fraction(200, 201)


def test_perfect_and_empty():
    gt = [{1: P1, 2: P2}] * 3
    assert idf1(gt, gt)["idf1"] == 1
    r = idf1(gt, [{}] * 3)
    assert (r["idf1"], r["idr"], r["idp"]) == (0, 0, None)


def test_matching_against_brute_force():
    rng = random.Random(1)
    for _ in range(300):
        r, c = rng.randint(1, 4), rng.randint(1, 4)
        n = [[rng.randint(0, 6) for _ in range(c)] for _ in range(r)]
        pairs, total = max_overlap_matching(n)
        assert len({i for i, _ in pairs}) == len(pairs) == len({j for _, j in pairs})
        assert total == brute_max_total(n)


def random_box(rng):
    x, y = rng.randint(0, 10), rng.randint(0, 10)
    return (x, y, x + rng.randint(3, 6), y + rng.randint(3, 6))


def random_sequence(rng):
    start = {o: random_box(rng) for o in range(3)}
    names = {o: "abc"[o] for o in range(3)}
    gt_frames, hyp_frames = [], []
    for t in range(rng.randint(1, 8)):
        gt, hyp = {}, {}
        for o, b in start.items():
            if rng.random() < 0.8:
                gt[o] = (b[0] + t, b[1], b[2] + t, b[3])
                if rng.random() < 0.2:
                    names[o] = rng.choice("abcde")
                if rng.random() < 0.8 and names[o] not in hyp:
                    dx = rng.randint(-1, 1)
                    hyp[names[o]] = (gt[o][0] + dx, gt[o][1], gt[o][2] + dx, gt[o][3])
        if rng.random() < 0.3:
            hyp["z"] = random_box(rng)
        gt_frames.append(gt)
        hyp_frames.append(hyp)
    return gt_frames, hyp_frames


def frame_max_matches(gt, hyp):
    objs, hyps = list(gt), list(hyp)
    best = 0
    for k in range(min(len(objs), len(hyps)) + 1):
        for rs in itertools.combinations(objs, k):
            for cs in itertools.permutations(hyps, k):
                if all(iou(gt[o], hyp[h]) >= HALF for o, h in zip(rs, cs)):
                    best = max(best, k)
    return best


def test_dummy_node_form_and_detection_bound():
    rng = random.Random(2)
    for _ in range(80):
        gt_frames, hyp_frames = random_sequence(rng)
        _, _, n, glen, hlen = overlap_counts(gt_frames, hyp_frames)
        r = idf1(gt_frames, hyp_frames)
        assert r["idtp"] == brute_max_total(n)
        # the minimum cost of the form of the paper is IDFN + IDFP
        assert min_cost_with_dummy_nodes(n, glen, hlen) == r["idfn"] + r["idfp"]
        assert r["idfn"] + r["idtp"] == sum(glen)
        assert r["idfp"] + r["idtp"] == sum(hlen)
        # IDF1 is at most the F1 of detections with the best matching in each frame
        tp = sum(frame_max_matches(g, h) for g, h in zip(gt_frames, hyp_frames))
        total = sum(glen) + sum(hlen)
        if total:
            assert r["idf1"] <= Fraction(2 * tp, total)
            assert r["idf1"] == 2 / (1 / r["idp"] + 1 / r["idr"]) if r["idtp"] else r["idf1"] == 0


def test_symmetry():
    rng = random.Random(3)
    for _ in range(40):
        gt_frames, hyp_frames = random_sequence(rng)
        a = idf1(gt_frames, hyp_frames)
        b = idf1(hyp_frames, gt_frames)
        assert a["idtp"] == b["idtp"] and a["idf1"] == b["idf1"]
        assert (a["idp"], a["idr"]) == (b["idr"], b["idp"])
