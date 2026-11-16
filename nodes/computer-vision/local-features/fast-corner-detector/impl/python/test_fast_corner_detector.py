# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-corner-detector/. The authors are listed in prov/99A606.jsonl.

import random

from fast_corner_detector import CIRCLE, COMPASS, fast_corners, fast_scores, high_speed_reject, ring


def segment_test(img, u, v, t, n):
    """Brute force: is there a run of n circle pixels, all brighter or all darker?"""
    c = img[v][u]
    vals = [img[v + dv][u + du] for du, dv in CIRCLE]
    for start in range(16):
        run = [vals[(start + k) % 16] for k in range(n)]
        if all(x >= c + t for x in run) or all(x <= c - t for x in run):
            return True
    return False


def oracle(img, t, n):
    """Score by a linear scan over thresholds, then 3 x 3 suppression."""
    h, w = len(img), len(img[0])
    scores = {}
    for v in range(3, h - 3):
        for u in range(3, w - 3):
            if segment_test(img, u, v, t, n):
                s = t
                while segment_test(img, u, v, s + 1, n):
                    s += 1
                scores[(u, v)] = s
    keep = []
    for (u, v), s in scores.items():
        if all(scores.get((u + a, v + b), -1) <= s for a in (-1, 0, 1) for b in (-1, 0, 1)):
            keep.append((u, v))
    return sorted(keep, key=lambda p: (p[1], p[0])), scores


def block():
    return [[9 if (u >= 5 and v >= 5) else 0 for u in range(11)] for v in range(11)]


def test_circle_is_a_bresenham_circle_of_radius_3():
    assert len(set(CIRCLE)) == 16
    assert all(8 <= du * du + dv * dv <= 10 or du * dv == 0 for du, dv in CIRCLE)
    assert all(max(abs(du), abs(dv)) == 3 or (abs(du), abs(dv)) == (2, 2) for du, dv in CIRCLE)
    # Consecutive pixels touch, so the circle is a closed 8-connected loop.
    for i in range(16):
        (a, b), (c, d) = CIRCLE[i], CIRCLE[(i + 1) % 16]
        assert max(abs(a - c), abs(b - d)) == 1
    assert [CIRCLE[i] for i in COMPASS] == [(0, -3), (3, 0), (0, 3), (-3, 0)]


def test_worked_example_block_corner():
    img = block()
    assert ring(img, 5, 5) == [0, 0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0]
    scores = fast_scores(img, 1, 9)
    assert scores == {(5, 5): 9, (6, 5): 9, (7, 5): 9, (5, 6): 9, (6, 6): 9, (5, 7): 9}
    assert fast_corners(img, 1, 9) == [(5, 5), (6, 5), (7, 5), (5, 6), (6, 6), (5, 7)]
    # A right-angle corner leaves only 11 dark pixels on the circle, so FAST-12 misses it.
    assert fast_scores(img, 1, 12) == {}
    assert fast_scores(img, 10, 9) == {}


def test_flat_image_and_small_image():
    assert fast_corners([[4] * 9 for _ in range(9)], 1, 9) == []
    assert fast_corners([[1, 2, 3, 4, 5, 6]] * 6, 1, 9) == []


def test_single_bright_pixel():
    img = [[0] * 7 for _ in range(7)]
    img[3][3] = 50
    assert fast_scores(img, 1, 16) == {(3, 3): 50}
    assert fast_corners(img, 50, 9) == [(3, 3)]
    assert fast_corners(img, 51, 9) == []


def test_high_speed_test_is_exact_for_n_12():
    # For every set of brighter pixels on the circle: a run of 12 implies 3 of the 4 compass pixels.
    for mask in range(1 << 16):
        bits = [(mask >> i) & 1 for i in range(16)]
        run12 = any(all(bits[(s + k) % 16] for k in range(12)) for s in range(16))
        if run12:
            assert sum(bits[i] for i in COMPASS) >= 3


def test_high_speed_test_is_wrong_for_n_9():
    # A dark run of 9 that holds only 2 compass pixels: pixels 2 to 10.
    vals = [10] * 16
    for i in range(1, 10):
        vals[i] = 0
    assert sum(1 for i in COMPASS if vals[i] <= 10 - 5) == 2
    assert high_speed_reject(10, vals, 5)
    img = [[10] * 7 for _ in range(7)]
    for (du, dv), x in zip(CIRCLE, vals):
        img[3 + dv][3 + du] = x
    assert segment_test(img, 3, 3, 5, 9)
    assert fast_scores(img, 5, 9) == {(3, 3): 10}


def test_high_speed_flag_does_not_change_output():
    rng = random.Random(12)
    for _ in range(80):
        img = [[rng.choice([0, 0, 5, 9, 9]) for _ in range(9)] for _ in range(9)]
        assert fast_scores(img, 3, 12, True) == fast_scores(img, 3, 12, False)


def test_random_against_oracle():
    rng = random.Random(2006)
    for _ in range(600):
        w, h = rng.randint(7, 10), rng.randint(7, 10)
        img = [[rng.randint(0, 6) for _ in range(w)] for _ in range(h)]
        if rng.random() < 0.5:
            # Plant a bright or dark blob so that corners occur often.
            cu, cv = rng.randint(3, w - 4), rng.randint(3, h - 4)
            img[cv][cu] = rng.choice([0, 12])
        t = rng.randint(1, 4)
        n = rng.choice([9, 10, 11, 12])
        want, scores = oracle(img, t, n)
        assert fast_scores(img, t, n) == scores
        assert fast_corners(img, t, n) == want


def test_rotation_by_90_degrees():
    rng = random.Random(77)
    for _ in range(60):
        h, w = 9, 10
        img = [[rng.randint(0, 9) for _ in range(w)] for _ in range(h)]
        # rot[i][j] = img[h - 1 - j][i]: pixel (u, v) of img goes to (h - 1 - v, u).
        rot = [[img[h - 1 - j][i] for j in range(h)] for i in range(w)]
        a = fast_scores(img, 2, 9)
        b = fast_scores(rot, 2, 9)
        assert {(h - 1 - v, u): s for (u, v), s in a.items()} == b


def test_offset_invariance():
    rng = random.Random(3)
    for _ in range(40):
        img = [[rng.randint(0, 9) for _ in range(9)] for _ in range(9)]
        assert fast_scores([[x + 100 for x in r] for r in img], 2, 9) == fast_scores(img, 2, 9)
