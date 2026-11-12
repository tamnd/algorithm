# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zigzag-scan/. The authors are listed in prov/4K7DEC.jsonl.

import random

from zigzag_scan import EOB, ZRL, ac_run_length, ac_run_length_decode, scan, unscan, zigzag_order

# ITU-T T.81 (09/1992), Annex A.3.6, Figure A.6 "Zig-zag sequence of quantized
# DCT coefficients" (printed page 30), copied by hand. Entry [row][col] is the
# position of that coefficient in the zigzag sequence; row is the vertical
# frequency and col the horizontal frequency.
T81_FIGURE_A6 = [
    [0, 1, 5, 6, 14, 15, 27, 28],
    [2, 4, 7, 13, 16, 26, 29, 42],
    [3, 8, 12, 17, 25, 30, 41, 43],
    [9, 11, 18, 24, 31, 40, 44, 53],
    [10, 19, 23, 32, 39, 45, 52, 54],
    [20, 22, 33, 38, 46, 51, 55, 60],
    [21, 34, 37, 47, 50, 56, 59, 61],
    [35, 36, 48, 49, 57, 58, 62, 63],
]


def test_matches_t81_figure_a6() -> None:
    for k, (r, c) in enumerate(zigzag_order(8)):
        assert T81_FIGURE_A6[r][c] == k


def test_permutation_and_diagonals() -> None:
    for n in range(1, 17):
        order = zigzag_order(n)
        assert sorted(order) == [(r, c) for r in range(n) for c in range(n)]
        sums = [r + c for r, c in order]
        assert sums == sorted(sums)  # by increasing row + col
        for a, b in zip(order, order[1:]):
            s = a[0] + a[1]
            if b[0] + b[1] == s:  # inside one diagonal the direction alternates
                assert b[0] == a[0] + (1 if s % 2 == 1 else -1)
            else:  # a step to the next diagonal moves to a neighbour cell
                assert abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1


def test_scan_unscan() -> None:
    rng = random.Random(11)
    for n in (1, 2, 4, 8):
        block = [[rng.randint(-50, 50) for _ in range(n)] for _ in range(n)]
        assert unscan(scan(block), n) == block


def test_worked_example() -> None:
    block = [[0] * 8 for _ in range(8)]
    block[0][0], block[0][1], block[1][0], block[2][2], block[3][5] = 12, 5, -3, 1, 2
    zz = scan(block)
    assert zz[:3] == [12, 5, -3] and zz[12] == 1 and zz[40] == 2
    pairs = ac_run_length(zz)
    assert pairs == [(0, 5), (0, -3), (9, 1), ZRL, (11, 2), EOB]
    assert ac_run_length_decode(pairs, 12) == zz
    row_order = [v for row in block for v in row]
    assert ac_run_length(row_order) == [(0, 5), (6, -3), (9, 1), (10, 2), EOB]
    # On a block whose nonzero values fill the corner triangle r + c <= 3,
    # the zigzag list has no zero before its last nonzero value.
    tri = [[(r + c + 1) if r + c <= 3 else 0 for c in range(8)] for r in range(8)]
    assert ac_run_length(scan(tri)) == [(0, v) for v in scan(tri)[1:10]] + [EOB]
    assert len(ac_run_length([v for row in tri for v in row])) == 10


def test_edge_cases() -> None:
    assert ac_run_length([7] + [0] * 63) == [EOB]
    last = [0] * 64
    last[63] = 4
    assert ac_run_length(last) == [ZRL, ZRL, ZRL, (14, 4)]  # no EOB after the last coefficient
    sixteen = [0] * 64
    sixteen[17] = 1
    assert ac_run_length(sixteen) == [ZRL, (0, 1), EOB]
    full = list(range(1, 65))
    assert ac_run_length(full) == [(0, v) for v in range(2, 65)]


def test_run_length_round_trip_random() -> None:
    rng = random.Random(2024)
    for _ in range(1000):
        density = rng.random()
        zz = [rng.randint(-9, 9) if rng.random() < density else 0 for _ in range(64)]
        pairs = ac_run_length(zz)
        assert ac_run_length_decode(pairs, zz[0]) == zz
        assert all(0 <= r <= 15 for r, _ in pairs)
        assert pairs.count(EOB) <= 1 and (EOB not in pairs or pairs[-1] == EOB)
