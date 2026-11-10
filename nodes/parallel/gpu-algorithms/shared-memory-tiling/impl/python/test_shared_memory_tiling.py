# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-memory-tiling/.

import random

from shared_memory_tiling import matmul_reference, naive_loads, tiled_loads, tiled_matmul


def rand_matrix(rng, rows, cols):
    return [[rng.randrange(-9, 10) for _ in range(cols)] for _ in range(rows)]


def test_tiled_product_equals_the_triple_loop():
    rng = random.Random(10)
    for m, k, n in ((1, 1, 1), (4, 4, 4), (8, 8, 8), (5, 7, 3), (9, 4, 6), (2, 13, 11)):
        for T in (1, 2, 4):
            A, B = rand_matrix(rng, m, k), rand_matrix(rng, k, n)
            C, cnt = tiled_matmul(A, B, T)
            assert C == matmul_reference(A, B)
            assert cnt.global_loads == tiled_loads(m, k, n, T)


def test_traffic_drops_by_the_tile_size_for_square_matrices():
    for n in (4, 8, 16):
        for T in (2, 4):
            assert tiled_loads(n, n, n, T) * T == naive_loads(n, n, n)
    _, cnt = tiled_matmul([[1] * 16 for _ in range(16)], [[1] * 16 for _ in range(16)], 4)
    assert cnt.global_loads == 2 * 16**3 // 4 == 2048


def test_both_barriers_are_needed():
    rng = random.Random(11)
    A, B = rand_matrix(rng, 8, 8), rand_matrix(rng, 8, 8)
    ref = matmul_reference(A, B)
    assert tiled_matmul(A, B, 4)[0] == ref
    assert tiled_matmul(A, B, 4, barrier1=False)[0] != ref
    assert tiled_matmul(A, B, 4, barrier2=False)[0] != ref
