# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/drizzle/. The authors are listed in prov/GWCHWD.jsonl.

import random
from fractions import Fraction as F

from drizzle import drizzle, overlap_1d, shift_and_add, total_flux


def rand_frame(rng, n1, n2, lo=0, hi=9):
    return [[F(rng.randint(lo, hi)) for _ in range(n2)] for _ in range(n1)]


def brute_drizzle(frames, shifts, s, p, out_shape, q):
    """Drizzle with each overlap area found by counting cells of side 1/q.

    Every drop edge and every output pixel edge must lie on the lattice of
    step 1/q; then the count of lattice cells whose centers lie in both
    squares, times 1/q^2, is the exact overlap area.
    """
    m1, m2 = out_shape
    wsum = [[F(0)] * m2 for _ in range(m1)]
    vsum = [[F(0)] * m2 for _ in range(m1)]
    cell = F(1, q)
    for frame, (dx, dy) in zip(frames, shifts):
        for i, row in enumerate(frame):
            for j, d in enumerate(row):
                x0 = j + dx + F(1, 2) - p / 2
                y0 = i + dy + F(1, 2) - p / 2
                steps = int(p * q)
                for u in range(steps):
                    for v in range(steps):
                        cx = x0 + (u + F(1, 2)) * cell
                        cy = y0 + (v + F(1, 2)) * cell
                        oj, oi = int(cx // s), int(cy // s)
                        if 0 <= oi < m1 and 0 <= oj < m2:
                            wsum[oi][oj] += cell * cell
                            vsum[oi][oj] += cell * cell * d
    out = [[s * s * vsum[i][j] / wsum[i][j] if wsum[i][j] else F(0) for j in range(m2)] for i in range(m1)]
    return out, wsum


def test_overlap_1d():
    assert overlap_1d(F(0), F(1), F(1, 2), F(3)) == F(1, 2)
    assert overlap_1d(F(0), F(1), F(2), F(3)) == 0
    assert overlap_1d(F(1, 4), F(3, 4), F(0), F(2)) == F(1, 2)
    assert overlap_1d(0.0, 1.0, 1.0, 2.0) == 0


def test_matches_brute_force_cell_counting():
    rng = random.Random(1)
    q = 20
    for _ in range(4):
        n = 3
        frames = [rand_frame(rng, n, n) for _ in range(3)]
        shifts = [(F(rng.randint(0, 20), q), F(rng.randint(0, 20), q)) for _ in range(3)]
        s = F(rng.choice([10, 12, 15]), q)
        p = F(rng.choice([6, 10, 14, 20]), q)
        out_shape = (int((n + 2) / s) + 1, int((n + 2) / s) + 1)
        got = drizzle(frames, shifts, s, p, out_shape)
        assert got == brute_drizzle(frames, shifts, s, p, out_shape, q)


def test_weighted_flux_is_kept_exactly():
    # sum_o W_o I_o = s^2 p^2 sum_i w_i d_i when every drop lies inside the output grid.
    rng = random.Random(2)
    for _ in range(5):
        n = 4
        k = 3
        frames = [rand_frame(rng, n, n) for _ in range(k)]
        weights = [[[F(rng.choice([0, 1, 1, 2])) for _ in range(n)] for _ in range(n)] for _ in range(k)]
        shifts = [(F(rng.randint(0, 9), 7), F(rng.randint(0, 9), 7)) for _ in range(k)]
        s = F(rng.choice([1, 2, 3]), 3)
        p = F(rng.choice([1, 2, 3]), 3)
        m = int((n + 3) / s) + 1
        img, wmap = drizzle(frames, shifts, s, p, (m, m), weights)
        left = total_flux(img, wmap)
        right = s * s * p * p * sum(w * d for fr, wf in zip(frames, weights) for rf, rw in zip(fr, wf) for d, w in zip(rf, rw))
        assert left == right
        # The total weight is p^2 times the total input weight.
        assert sum(v for row in wmap for v in row) == p * p * sum(v for wf in weights for row in wf for v in row)


def test_constant_input_gives_a_constant_output():
    c = F(7)
    frames = [[[c] * 5 for _ in range(5)] for _ in range(2)]
    shifts = [(F(0), F(0)), (F(1, 3), F(2, 5))]
    s, p = F(2, 3), F(3, 4)
    img, wmap = drizzle(frames, shifts, s, p, (9, 9))
    for i in range(9):
        for j in range(9):
            if wmap[i][j] != 0:
                assert img[i][j] == c * s * s


def test_unit_pixels_and_integer_shifts_give_shift_and_add():
    rng = random.Random(3)
    frames = [rand_frame(rng, 4, 4) for _ in range(3)]
    shifts = [(0, 0), (1, 0), (1, 2)]
    img, _ = drizzle(frames, [(F(a), F(b)) for a, b in shifts], F(1), F(1), (6, 6))
    assert img == shift_and_add(frames, shifts, (6, 6))


def test_four_half_pixel_dithers_interlace_exactly():
    # With s = p = 1/2 and the shifts (-1/4 + b/2, -1/4 + a/2), the drop of
    # pixel (i, j) of frame (a, b) is exactly output pixel (2 i + a, 2 j + b).
    rng = random.Random(4)
    n = 4
    fine = rand_frame(rng, 2 * n + 2, 2 * n + 2)
    frames, shifts = [], []
    for a in (0, 1):
        for b in (0, 1):
            frames.append([[fine[2 * i + a + 1][2 * j + b + 1] for j in range(n)] for i in range(n)])
            shifts.append((F(-1, 4) + F(b, 2) + F(1, 2), F(-1, 4) + F(a, 2) + F(1, 2)))
    s = p = F(1, 2)
    img, wmap = drizzle(frames, shifts, s, p, (2 * n + 2, 2 * n + 2))
    for i in range(1, 2 * n + 1):
        for j in range(1, 2 * n + 1):
            assert wmap[i][j] == F(1, 4)
            assert img[i][j] == fine[i][j] / 4


def test_linear_in_the_data():
    rng = random.Random(5)
    f1 = [rand_frame(rng, 3, 3, -5, 5) for _ in range(2)]
    f2 = [rand_frame(rng, 3, 3, -5, 5) for _ in range(2)]
    shifts = [(F(0), F(0)), (F(2, 5), F(1, 5))]
    s, p = F(1, 2), F(3, 5)
    alpha = F(3, 7)
    mix = [[[alpha * x + y for x, y in zip(r1, r2)] for r1, r2 in zip(a, b)] for a, b in zip(f1, f2)]
    i1, w1 = drizzle(f1, shifts, s, p, (8, 8))
    i2, _ = drizzle(f2, shifts, s, p, (8, 8))
    im, wm = drizzle(mix, shifts, s, p, (8, 8))
    assert wm == w1
    assert im == [[alpha * x + y for x, y in zip(r1, r2)] for r1, r2 in zip(i1, i2)]


def test_bad_pixels_are_left_out():
    frames = [[[F(1), F(100)], [F(1), F(1)]], [[F(1), F(1)], [F(1), F(1)]]]
    weights = [[[1, 0], [1, 1]], [[1, 1], [1, 1]]]
    img, wmap = drizzle(frames, [(F(0), F(0)), (F(0), F(0))], F(1), F(1), (2, 2), weights)
    assert img == [[1, 1], [1, 1]]
    assert wmap == [[2, 1], [2, 2]]


def test_uncovered_output_pixels_have_zero_weight():
    frames = [[[F(5)]]]
    img, wmap = drizzle(frames, [(F(0), F(0))], F(1, 2), F(1, 2), (2, 2))
    # The drop [1/4, 3/4]^2 touches all four output pixels of side 1/2.
    assert wmap == [[F(1, 16)] * 2] * 2
    img2, wmap2 = drizzle(frames, [(F(0), F(0))], F(1, 2), F(1, 2), (4, 4))
    assert wmap2[3][3] == 0 and img2[3][3] == 0


def test_float_input_agrees_with_fractions():
    rng = random.Random(6)
    frames = [rand_frame(rng, 3, 3) for _ in range(2)]
    shifts = [(F(0), F(0)), (F(3, 10), F(7, 10))]
    exact, _ = drizzle(frames, shifts, F(1, 2), F(7, 10), (8, 8))
    ff = [[[float(v) for v in row] for row in fr] for fr in frames]
    fs = [(float(a), float(b)) for a, b in shifts]
    approx, _ = drizzle(ff, fs, 0.5, 0.7, (8, 8))
    for ra, rb in zip(exact, approx):
        for a, b in zip(ra, rb):
            assert abs(float(a) - b) < 1e-12
