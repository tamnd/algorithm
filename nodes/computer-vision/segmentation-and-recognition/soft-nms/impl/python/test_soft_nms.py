# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/soft-nms/. The authors are listed in prov/CXYXEQ.jsonl.

import math
import random
from fractions import Fraction

from soft_nms import greedy_nms_ge, iou, make_decay, soft_nms, soft_nms_reference

EXAMPLE_BOXES = [(0, 0, 10, 10), (1, 1, 11, 11), (6, 0, 16, 10), (20, 20, 30, 30), (7, 1, 17, 11)]
EXAMPLE_SCORES = [Fraction(9, 10), Fraction(8, 10), Fraction(3, 4), Fraction(3, 5), Fraction(1, 2)]


def random_instance(rng, n, size=20):
    boxes = []
    for _ in range(n):
        x, y = rng.randint(0, size), rng.randint(0, size)
        w, h = rng.randint(2, 8), rng.randint(2, 8)
        boxes.append((x, y, x + w, y + h))
    scores = [Fraction(rng.randint(1, 6), 6) for _ in range(n)]  # ties on purpose
    return boxes, scores


def test_page_example_linear():
    out = soft_nms(EXAMPLE_BOXES, EXAMPLE_SCORES, "linear", nt=Fraction(3, 10))
    assert [i for i, _ in out] == [0, 2, 3, 1, 4]
    assert [s for _, s in out] == [Fraction(9, 10), Fraction(3, 4), Fraction(3, 5),
                                   Fraction(152, 595), Fraction(19, 119)]
    assert iou(EXAMPLE_BOXES[1], EXAMPLE_BOXES[2]) == Fraction(9, 31)


def test_page_example_gaussian():
    floats = [float(s) for s in EXAMPLE_SCORES]
    out = soft_nms(EXAMPLE_BOXES, floats, "gaussian", sigma=0.5)
    assert [i for i, _ in out] == [0, 2, 3, 1, 4]
    assert abs(out[1][1] - 0.75 * math.exp(-0.125)) < 1e-12
    assert round(out[3][1], 4) == 0.2676 and round(out[4][1], 4) == 0.1664


def test_page_example_hard_is_greedy_nms():
    out = soft_nms(EXAMPLE_BOXES, EXAMPLE_SCORES, "hard", nt=Fraction(3, 10))
    assert [i for i, _ in out] == [0, 2, 3]
    assert greedy_nms_ge(EXAMPLE_BOXES, EXAMPLE_SCORES, Fraction(3, 10)) == [0, 2, 3]


def test_hard_rule_equals_greedy_nms():
    rng = random.Random(11)
    for trial in range(200):
        boxes, scores = random_instance(rng, rng.randint(0, 15))
        nt = rng.choice([Fraction(1, 10), Fraction(3, 10), Fraction(1, 2), Fraction(7, 10)])
        out = soft_nms(boxes, scores, "hard", nt=nt)
        assert [i for i, _ in out] == greedy_nms_ge(boxes, scores, nt)
        # The hard rule never changes a surviving score.
        assert all(s == scores[i] for i, s in out)


def test_matches_reference_exact():
    rng = random.Random(12)
    for trial in range(120):
        boxes, scores = random_instance(rng, rng.randint(0, 10))
        nt = rng.choice([Fraction(1, 5), Fraction(3, 10), Fraction(1, 2)])
        s_min = rng.choice([0, Fraction(1, 100), Fraction(1, 5)])
        f = make_decay("linear", nt=nt)
        got = soft_nms(boxes, scores, s_min=s_min, decay=f)
        assert got == soft_nms_reference(boxes, scores, f, s_min)


def test_matches_reference_gaussian():
    rng = random.Random(13)
    for trial in range(80):
        boxes, scores = random_instance(rng, rng.randint(0, 10))
        scores = [float(s) for s in scores]
        f = make_decay("gaussian", sigma=0.5)
        got = soft_nms(boxes, scores, s_min=0.05, decay=f)
        assert got == soft_nms_reference(boxes, scores, f, 0.05)


def test_scores_are_nonincreasing_and_closed_form():
    rng = random.Random(14)
    for method in ("linear", "gaussian"):
        for trial in range(60):
            boxes, scores = random_instance(rng, 20, size=25)
            if method == "gaussian":
                scores = [float(s) for s in scores]
            f = make_decay(method, nt=Fraction(3, 10), sigma=0.5)
            out = soft_nms(boxes, scores, s_min=0, decay=f)
            # With s_min = 0 every box is output exactly once.
            assert sorted(i for i, _ in out) == list(range(20))
            vals = [s for _, s in out]
            assert all(vals[k] >= vals[k + 1] for k in range(len(vals) - 1))
            # The output score is the input score times the decays of all
            # boxes selected before it, in the order of selection.
            for pos, (i, s) in enumerate(out):
                v = scores[i]
                for m, _ in out[:pos]:
                    v = v * f(iou(boxes[m], boxes[i]))
                assert v == s


def test_disjoint_boxes_keep_scores_and_rank_order():
    boxes = [(3 * i, 0, 3 * i + 2, 2) for i in range(12)]
    rng = random.Random(15)
    scores = [Fraction(rng.randint(1, 4), 4) for _ in range(12)]
    out = soft_nms(boxes, scores, "linear")
    assert [i for i, _ in out] == sorted(range(12), key=lambda i: (-scores[i], i))
    assert all(s == scores[i] for i, s in out)


def test_crowd_case_keeps_second_object():
    # Two true objects whose boxes overlap with IoU 3/5. Greedy NMS at 0.5
    # removes the second one; the linear rule keeps it with a lower score.
    a, b = (0, 0, 8, 10), (2, 0, 10, 10)
    assert iou(a, b) == Fraction(3, 5)
    out = soft_nms([a, b], [Fraction(9, 10), Fraction(4, 5)], "linear")
    assert out == [(0, Fraction(9, 10)), (1, Fraction(8, 25))]
    assert soft_nms([a, b], [Fraction(9, 10), Fraction(4, 5)], "hard", nt=Fraction(1, 2)) == [(0, Fraction(9, 10))]


def test_quadratic_overlap_count():
    calls = [0]

    def counting_iou(p, q):
        calls[0] += 1
        return iou(p, q)

    n = 25
    rng = random.Random(16)
    boxes, scores = random_instance(rng, n)
    soft_nms(boxes, [float(s) for s in scores], "gaussian", s_min=0, overlap=counting_iou)
    assert calls[0] == n * (n - 1) // 2
