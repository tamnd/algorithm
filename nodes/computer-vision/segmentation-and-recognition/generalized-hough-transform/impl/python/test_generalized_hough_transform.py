# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-hough-transform/. The authors are listed in prov/GZ6ZY6.jsonl.

import math
import random

from generalized_hough_transform import (build_r_table, detect, direction_bin,
                                         edge_points, paste, peak, rotate90,
                                         sobel, vote, vote_rotations)

SQUARE = [[1 if 2 <= u <= 4 and 2 <= v <= 4 else 0 for u in range(7)] for v in range(7)]


def l_shape():
    """A 9 x 9 template with an L-shaped blob (no rotational symmetry), margin 2."""
    img = [[0] * 9 for _ in range(9)]
    for v in range(2, 7):
        img[v][2] = img[v][3] = 5
    for u in range(4, 7):
        img[5][u] = img[6][u] = 5
    return img


def blank(W, H):
    return [[0] * W for _ in range(H)]


def test_example_of_the_page():
    E = edge_points(SQUARE, 1)
    assert len(E) == 24
    R = build_r_table(E, (3, 3))
    assert [len(R[b]) for b in range(8)] == [4, 2, 4, 2, 4, 2, 4, 2]
    assert sorted(R[2]) == [(-1, 2), (0, 1), (0, 2), (1, 2)]
    img = paste(blank(12, 10), SQUARE, 4, 2)
    (votes, u, v), A = detect(img, R, 1)
    assert (votes, u, v) == (24, 7, 5)
    others = sorted((a for row in A for a in row), reverse=True)
    assert others[1] == 6


def test_translated_copy_with_clutter():
    T = l_shape()
    E = edge_points(T, 1)
    m = len(E)
    ref = (4, 4)
    R = build_r_table(E, ref)
    clean = paste(blank(30, 24), T, 13, 9)
    (votes, u, v), _ = detect(clean, R, 1)
    assert (votes, u, v) == (m, ref[0] + 13, ref[1] + 9)
    rng = random.Random(1)
    noisy = paste(blank(30, 24), T, 13, 9)
    for _ in range(40):
        uu, vv = rng.randrange(1, 29), rng.randrange(1, 23)
        if not (10 <= uu <= 23 and 6 <= vv <= 19):
            noisy[vv][uu] = rng.randint(1, 9)
    (votes, u, v), A = detect(noisy, R, 1)
    assert A[ref[1] + 9][ref[0] + 13] >= m
    assert (u, v) == (ref[0] + 13, ref[1] + 9)


def test_votes_equal_direct_count():
    rng = random.Random(2)
    T = l_shape()
    R = build_r_table(edge_points(T, 1), (4, 4))
    tmpl = edge_points(T, 1)
    img = [[rng.randint(0, 3) for _ in range(14)] for _ in range(12)]
    E = edge_points(img, 2)
    A = vote(E, R, 14, 12)
    direct = [[0] * 14 for _ in range(12)]
    for u, v, b in E:
        for tu, tv, tb in tmpl:
            if tb == b:
                pu, pv = u + 4 - tu, v + 4 - tv
                if 0 <= pu < 14 and 0 <= pv < 12:
                    direct[pv][pu] += 1
    assert A == direct


def test_bins_never_on_a_boundary_for_integer_gradients():
    for gx in range(-30, 31):
        for gy in range(-30, 31):
            if gx == 0 and gy == 0:
                continue
            q = math.atan2(gy, gx) / (math.pi / 4)
            assert abs(q - math.floor(q) - 0.5) > 1e-4
            assert direction_bin(-gy, gx) == (direction_bin(gx, gy) + 2) % 8
    assert direction_bin(1, 0) == 0 and direction_bin(0, 1) == 2
    assert direction_bin(-1, 0) == 4 and direction_bin(0, -1) == 6


def test_sobel_rotates_with_the_image():
    rng = random.Random(3)
    img = [[rng.randint(0, 9) for _ in range(7)] for _ in range(6)]
    H = len(img)
    gx, gy = sobel(img)
    rot = rotate90(img)
    rx, ry = sobel(rot)
    for v in range(1, H - 1):
        for u in range(1, 6):
            assert (rx[u][H - 1 - v], ry[u][H - 1 - v]) == (-gy[v][u], gx[v][u])


def test_rotation_by_90_degrees():
    T = l_shape()
    ref = (4, 4)
    E = edge_points(T, 1)
    m = len(E)
    R = build_r_table(E, ref)
    rot = rotate90(T)
    ref_rot = (len(T) - 1 - ref[1], ref[0])
    img = paste(blank(26, 22), rot, 9, 6)
    acc = vote_rotations(edge_points(img, 1), R, 26, 22, steps=[0, 2, 4, 6])
    best = max((peak(A), k) for (k, s), A in acc.items())
    assert best == ((m, ref_rot[0] + 9, ref_rot[1] + 6), 2)
    assert peak(acc[(0, 1.0)])[0] < m


def test_scale_two_offsets():
    R = [[(1, 0)], [], [], [], [], [], [], []]
    acc = vote_rotations([(5, 5, 0)], R, 12, 12, steps=[0], scales=(1.0, 2.0))
    assert acc[(0, 1.0)][5][6] == 1 and acc[(0, 2.0)][5][7] == 1


def test_affine_intensity_change_keeps_edges():
    T = l_shape()
    brighter = [[3 * a + 7 for a in row] for row in T]
    assert edge_points(T, 1) == edge_points(brighter, 1)
