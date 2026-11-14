# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/common-centroid-layout/. The authors are listed in prov/JQ9ZE3.jsonl.

import itertools
import random
from fractions import Fraction

import pytest

from common_centroid_layout import centroids, common_centroid_pattern, device_means, second_moments


def all_patterns(rows: int, cols: int, counts: list):
    """Every assignment of the cells to the devices with the given counts."""
    cells = [(i, j) for i in range(rows) for j in range(cols)]

    def rec(d: int, free: list, grid: list):
        if d == len(counts) - 1:
            for i, j in free:
                grid[i][j] = d
            yield [row[:] for row in grid]
            return
        for pick in itertools.combinations(free, counts[d]):
            for i, j in pick:
                grid[i][j] = d
            rest = [c for c in free if c not in pick]
            yield from rec(d + 1, rest, grid)

    yield from rec(0, cells, [[-1] * cols for _ in range(rows)])


def linear(gx: Fraction, gy: Fraction):
    return lambda x, y: 5 + gx * x + gy * y


def quadratic(rows: int, cols: int, g: tuple, h: tuple):
    cx, cy = Fraction(cols, 2), Fraction(rows, 2)
    gx, gy = g
    hxx, hxy, hyy = h

    def p(x, y):
        dx, dy = x - cx, y - cy
        return 5 + gx * dx + gy * dy + Fraction(1, 2) * (hxx * dx * dx + 2 * hxy * dx * dy + hyy * dy * dy)

    return p


def is_point_symmetric(grid: list) -> bool:
    r, c = len(grid), len(grid[0])
    return all(grid[i][j] == grid[r - 1 - i][c - 1 - j] for i in range(r) for j in range(c))


def test_examples() -> None:
    assert common_centroid_pattern(1, 4, [2, 2]) == [[0, 1, 1, 0]]
    assert common_centroid_pattern(2, 2, [2, 2]) == [[0, 1], [1, 0]]
    g = common_centroid_pattern(3, 3, [4, 5])
    assert g[1][1] == 1
    with pytest.raises(ValueError):
        common_centroid_pattern(1, 6, [3, 3])
    with pytest.raises(ValueError):
        common_centroid_pattern(3, 3, [3, 3, 3])


def test_pattern_has_one_centroid_and_cancels_linear_gradients() -> None:
    rng = random.Random(1989)
    for rows in range(1, 5):
        for cols in range(1, 6):
            n = rows * cols
            for k in (2, 3):
                for counts in itertools.product(range(n + 1), repeat=k):
                    if sum(counts) != n or len([c for c in counts if c % 2]) != n % 2:
                        continue
                    g = common_centroid_pattern(rows, cols, list(counts))
                    assert is_point_symmetric(g)
                    assert sorted(sum(row.count(d) for row in g) for d in range(k)) == sorted(counts)
                    cs = set(centroids(g).values())
                    assert cs == {(Fraction(cols, 2), Fraction(rows, 2))}
                    gx, gy = Fraction(rng.randint(-50, 50), 7), Fraction(rng.randint(-50, 50), 7)
                    assert len(set(device_means(g, linear(gx, gy)).values())) == 1


def test_brute_force_linear_cancels_iff_same_centroid() -> None:
    rng = random.Random(7)
    for rows, cols, counts in ((2, 4, [4, 4]), (3, 3, [4, 5]), (1, 6, [3, 3]), (2, 3, [2, 4])):
        grads = [(Fraction(rng.randint(-9, 9)), Fraction(rng.randint(-9, 9))) for _ in range(4)] + [(1, 0), (0, 1)]
        any_cc = False
        for g in all_patterns(rows, cols, counts):
            same = len(set(centroids(g).values())) == 1
            cancels = all(len(set(device_means(g, linear(*gr)).values())) == 1 for gr in grads)
            assert same == cancels
            any_cc |= same
        assert any_cc == (len([c for c in counts if c % 2]) == (rows * cols) % 2)


def test_quadratic_residual_formula() -> None:
    rng = random.Random(42)
    for rows, cols, counts in ((1, 4, [2, 2]), (2, 2, [2, 2]), (2, 4, [4, 4]), (3, 3, [4, 5]), (4, 4, [8, 8])):
        g = common_centroid_pattern(rows, cols, counts)
        m = second_moments(g)
        for _ in range(5):
            grad = (Fraction(rng.randint(-9, 9)), Fraction(rng.randint(-9, 9)))
            h = tuple(Fraction(rng.randint(-9, 9), 4) for _ in range(3))
            means = device_means(g, quadratic(rows, cols, grad, h))
            (a0, a1, a2), (b0, b1, b2) = m[0], m[1]
            predicted = Fraction(1, 2) * h[0] * (a0 - b0) + h[1] * (a1 - b1) + Fraction(1, 2) * h[2] * (a2 - b2)
            assert means[0] - means[1] == predicted


def test_brute_force_best_quadratic_residual() -> None:
    # For the pure curvature p = (x - cx)^2, the best mismatch over all
    # common-centroid patterns of a 2 x 4 array is reached by some pattern,
    # and the generated pattern is never better than the best.
    p = quadratic(2, 4, (0, 0), (Fraction(2), 0, 0))
    best = None
    for g in all_patterns(2, 4, [4, 4]):
        if len(set(centroids(g).values())) == 1:
            means = device_means(g, p)
            r = abs(means[0] - means[1])
            best = r if best is None else min(best, r)
    gen = device_means(common_centroid_pattern(2, 4, [4, 4]), p)
    assert best == 0
    assert abs(gen[0] - gen[1]) >= best
