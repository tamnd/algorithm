# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/moravec-corner-detector/. The authors are listed in prov/S56VW3.jsonl.

import random

from moravec_corner_detector import SHIFTS, moravec_corners, moravec_response, shift_change


def oracle_corners(img, r, tau, m):
    """Brute force: build the four shifted windows as lists and compare them."""
    h, w = len(img), len(img[0])
    defined = {}
    for v in range(h):
        for u in range(w):
            if not (r + 1 <= u <= w - r - 2 and r + 1 <= v <= h - r - 2):
                continue
            best = None
            for a, b in [(1, 0), (0, 1), (1, 1), (1, -1)]:
                win = [img[v + j][u + i] for j in range(-r, r + 1) for i in range(-r, r + 1)]
                moved = [img[v + j + b][u + i + a] for j in range(-r, r + 1) for i in range(-r, r + 1)]
                e = sum((x - y) ** 2 for x, y in zip(win, moved))
                best = e if best is None else min(best, e)
            defined[(u, v)] = best
    out = []
    for (u, v), c in defined.items():
        if c > tau and all(
            defined.get((u + du, v + dv), -1) <= c
            for du in range(-m, m + 1)
            for dv in range(-m, m + 1)
        ):
            out.append((u, v))
    return sorted(out, key=lambda p: (p[1], p[0]))


def corner_image():
    return [[9 if (u >= 4 and v >= 4) else 0 for u in range(8)] for v in range(8)]


def test_worked_example_corner():
    img = corner_image()
    resp = moravec_response(img, 1)
    assert [shift_change(img, 4, 4, a, b, 1) for a, b in SHIFTS] == [162, 162, 405, 243]
    assert resp[(4, 4)] == 162
    assert resp[(3, 3)] == 81 and resp[(4, 3)] == 81 and resp[(3, 4)] == 81
    assert resp[(5, 4)] == 0 and resp[(4, 5)] == 0 and resp[(2, 2)] == 0
    assert moravec_corners(img, 1, 0, 1) == [(4, 4)]


def test_slanted_edge_gives_false_corners():
    img = [[9 if 2 * v >= u + 3 else 0 for u in range(10)] for v in range(10)]
    resp = moravec_response(img, 1)
    assert [shift_change(img, 5, 4, a, b, 1) for a, b in SHIFTS] == [81, 243, 162, 324]
    corners = moravec_corners(img, 1, 0, 1)
    assert len(corners) == 17
    assert all(resp[p] == 81 for p in corners)


def test_straight_edges_give_zero():
    vert = [[5 if u >= 4 else 0 for u in range(9)] for v in range(9)]
    diag = [[5 if u + v >= 8 else 0 for u in range(9)] for v in range(9)]
    for img in (vert, diag):
        assert all(c == 0 for c in moravec_response(img, 1).values())
        assert moravec_corners(img, 1, 0, 1) == []


def test_flat_and_tiny_images():
    assert moravec_corners([[7] * 6 for _ in range(6)], 1, 0, 1) == []
    assert moravec_response([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1) == {}
    assert moravec_corners([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1, 0, 1) == []


def test_random_against_oracle():
    rng = random.Random(1980)
    for _ in range(600):
        w, h = rng.randint(4, 8), rng.randint(4, 8)
        img = [[rng.randint(0, 3) for _ in range(w)] for _ in range(h)]
        r = rng.choice([0, 1])
        m = rng.choice([1, 2])
        tau = rng.choice([0, 2, 5])
        assert moravec_corners(img, r, tau, m) == oracle_corners(img, r, tau, m)


def test_offset_and_gain():
    rng = random.Random(7)
    for _ in range(50):
        img = [[rng.randint(0, 20) for _ in range(9)] for _ in range(9)]
        base = moravec_response(img, 1)
        shifted = moravec_response([[x + 100 for x in row] for row in img], 1)
        scaled = moravec_response([[3 * x for x in row] for row in img], 1)
        assert shifted == base
        assert all(scaled[p] == 9 * base[p] for p in base)
        assert moravec_corners([[3 * x for x in row] for row in img]) == moravec_corners(img)


def test_opposite_shift_identity():
    # E for the shift -s at p equals E for the shift s at p - s.
    rng = random.Random(11)
    img = [[rng.randint(0, 50) for _ in range(10)] for _ in range(10)]
    for v in range(3, 7):
        for u in range(3, 7):
            for a, b in SHIFTS:
                assert shift_change(img, u, v, -a, -b, 1) == shift_change(img, u - a, v - b, a, b, 1)
