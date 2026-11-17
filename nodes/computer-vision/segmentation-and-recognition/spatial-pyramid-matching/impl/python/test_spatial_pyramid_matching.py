# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spatial-pyramid-matching/. The authors are listed in prov/QX9B5V.jsonl.

import random
from fractions import Fraction

from spatial_pyramid_matching import (cell_of, dense_intersection, intersection,
                                      level_histogram, level_intersections,
                                      pyramid_vector, spm_kernel, spm_kernel_eq3)

X = [(0.5, 0.5, 0), (1.5, 0.5, 0), (3.5, 3.5, 1), (2.5, 0.5, 1)]
Y = [(0.5, 1.5, 0), (3.5, 0.5, 0), (3.5, 2.5, 1), (0.5, 3.5, 1)]


def random_features(rng, n, M, W, H):
    return [(rng.randrange(W), rng.randrange(H), rng.randrange(M)) for _ in range(n)]


def max_matching(X, Y, level, W, H):
    """Brute force: the largest one-to-one matching of X to Y that pairs only
    features with the same word in the same cell, by augmenting paths."""
    ok = [[cell_of(x[0], x[1], level, W, H) == cell_of(y[0], y[1], level, W, H) and x[2] == y[2]
           for y in Y] for x in X]
    match_of_y = [-1] * len(Y)

    def augment(i, seen):
        for j in range(len(Y)):
            if ok[i][j] and not seen[j]:
                seen[j] = True
                if match_of_y[j] < 0 or augment(match_of_y[j], seen):
                    match_of_y[j] = i
                    return True
        return False

    return sum(1 for i in range(len(X)) if augment(i, [False] * len(Y)))


def is_psd(G):
    """Exact test with Fractions: symmetric Gaussian elimination (LDL^T)."""
    A = [[Fraction(t) for t in row] for row in G]
    n = len(A)
    for p in range(n):
        if A[p][p] < 0:
            return False
        if A[p][p] == 0:
            if any(A[p][j] != 0 for j in range(p + 1, n)):
                return False
            continue
        for i in range(p + 1, n):
            f = A[i][p] / A[p][p]
            for j in range(p + 1, n):
                A[i][j] -= f * A[p][j]
    return True


def test_example_of_the_page():
    assert level_intersections(X, Y, 2, 4, 4) == [4, 2, 0]
    assert spm_kernel(X, Y, 2, 4, 4) == Fraction(3, 2)
    assert spm_kernel(X, Y, 1, 4, 4) == 3
    assert spm_kernel(X, X, 2, 4, 4) == 4
    assert spm_kernel(X, Y, 2, 4, 4, normalize=True) == Fraction(3, 8)


def test_cell_rule_and_far_edge():
    assert cell_of(0, 0, 2, 8, 8) == (0, 0)
    assert cell_of(1.99, 2.0, 2, 8, 8) == (0, 1)
    assert cell_of(8, 8, 2, 8, 8) == (3, 3)
    assert cell_of(7, 3, 0, 8, 8) == (0, 0)


def test_two_forms_and_the_vector_agree():
    rng = random.Random(1)
    for _ in range(30):
        M, L, W, H = rng.randint(1, 4), rng.randint(0, 3), rng.choice([8, 12]), rng.choice([8, 16])
        A = random_features(rng, rng.randint(0, 12), M, W, H)
        B = random_features(rng, rng.randint(0, 12), M, W, H)
        for norm in (False, True):
            k2 = spm_kernel(A, B, L, W, H, norm)
            assert k2 == spm_kernel_eq3(A, B, L, W, H, norm)
            assert k2 == dense_intersection(pyramid_vector(A, M, L, W, H, norm), pyramid_vector(B, M, L, W, H, norm))


def test_intersection_is_a_maximum_matching():
    rng = random.Random(2)
    for _ in range(40):
        M, W, H = rng.randint(1, 3), 8, 8
        A = random_features(rng, rng.randint(0, 8), M, W, H)
        B = random_features(rng, rng.randint(0, 8), M, W, H)
        I = level_intersections(A, B, 3, W, H)
        for level in range(4):
            assert I[level] == max_matching(A, B, level, W, H)


def test_intersections_decrease_with_the_level():
    rng = random.Random(3)
    for _ in range(50):
        A = random_features(rng, 15, 3, 16, 16)
        B = random_features(rng, 15, 3, 16, 16)
        I = level_intersections(A, B, 4, 16, 16)
        assert all(I[level] >= I[level + 1] for level in range(4))


def test_self_kernel_and_level_zero_is_bag_of_words():
    rng = random.Random(4)
    A = random_features(rng, 9, 3, 8, 8)
    B = random_features(rng, 7, 3, 8, 8)
    assert spm_kernel(A, A, 3, 8, 8) == 9
    assert spm_kernel(A, A, 3, 8, 8, normalize=True) == 1
    bow_a, bow_b = {}, {}
    for _, _, m in A:
        bow_a[m] = bow_a.get(m, 0) + 1
    for _, _, m in B:
        bow_b[m] = bow_b.get(m, 0) + 1
    assert spm_kernel(A, B, 0, 8, 8) == intersection(bow_a, bow_b)


def test_gram_matrices_are_positive_semidefinite():
    rng = random.Random(5)
    for _ in range(4):
        sets = [random_features(rng, rng.randint(1, 8), 2, 8, 8) for _ in range(7)]
        for norm in (False, True):
            G = [[spm_kernel(a, b, 2, 8, 8, norm) for b in sets] for a in sets]
            assert is_psd(G)
    assert not is_psd([[1, 2], [2, 1]])


def test_layout_matters_only_above_level_zero():
    moved = [(3.5 - u, 3.5 - v, m) for u, v, m in X]
    assert level_intersections(X, moved, 0, 4, 4) == [4]
    assert spm_kernel(X, moved, 2, 4, 4) < spm_kernel(X, X, 2, 4, 4)


def test_vector_length():
    assert len(pyramid_vector([], 200, 2, 8, 8)) == 4200
    assert len(level_histogram(X, 2, 4, 4)) == 4
