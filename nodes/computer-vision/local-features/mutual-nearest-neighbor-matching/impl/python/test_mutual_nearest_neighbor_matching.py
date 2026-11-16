# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mutual-nearest-neighbor-matching/. The authors are listed in prov/5K7F44.jsonl.

import random

from mutual_nearest_neighbor_matching import mutual_nn_match, nearest, sqdist


def brute(A, B):
    """Keep (i, j) when d(i, j) is the first smallest of row i and of column j."""
    out = []
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            d = sqdist(a, b)
            row = all(d < sqdist(a, B[k]) or (d == sqdist(a, B[k]) and j <= k) for k in range(len(B)))
            col = all(d < sqdist(A[k], b) or (d == sqdist(A[k], b) and i <= k) for k in range(len(A)))
            if row and col:
                out.append((i, j))
    return out


def greedy(A, B):
    pairs = sorted((sqdist(a, b), i, j) for i, a in enumerate(A) for j, b in enumerate(B))
    used_a, used_b, out = set(), set(), set()
    for _, i, j in pairs:
        if i not in used_a and j not in used_b:
            used_a.add(i)
            used_b.add(j)
            out.add((i, j))
    return out


def test_worked_example():
    A = [(0.0, 0.0), (4.0, 0.0), (5.0, 0.0)]
    B = [(1.0, 0.0), (4.5, 0.0), (9.0, 0.0)]
    # f = (0, 1, 1), g = (0, 1, 2): row 2 and row 1 both pick b_1, b_1 picks a_1 on a tie
    assert [nearest(a, B) for a in A] == [0, 1, 1]
    assert [nearest(b, A) for b in B] == [0, 1, 2]
    assert mutual_nn_match(A, B) == [(0, 0), (1, 1)]


def test_many_small_inputs_against_the_definition():
    rng = random.Random(1)
    for _ in range(600):
        d = rng.randint(1, 3)
        A = [tuple(rng.randint(0, 4) for _ in range(d)) for _ in range(rng.randint(0, 6))]
        B = [tuple(rng.randint(0, 4) for _ in range(d)) for _ in range(rng.randint(0, 6))]
        got = mutual_nn_match(A, B)
        assert got == brute(A, B)
        assert len({i for i, _ in got}) == len(got) == len({j for _, j in got})
        if A and B:
            assert got  # the first smallest pair is always kept
            m = min(sqdist(a, b) for a in A for b in B)
            i0 = min(i for i, a in enumerate(A) if any(sqdist(a, b) == m for b in B))
            assert (i0, nearest(A[i0], B)) in got


def test_swapping_the_sets_transposes_the_result():
    rng = random.Random(2)
    for _ in range(200):
        A = [tuple(rng.randint(0, 3) for _ in range(2)) for _ in range(rng.randint(1, 6))]
        B = [tuple(rng.randint(0, 3) for _ in range(2)) for _ in range(rng.randint(1, 6))]
        assert sorted((j, i) for i, j in mutual_nn_match(A, B)) == mutual_nn_match(B, A)


def test_subset_of_the_greedy_matching_for_distinct_distances():
    rng = random.Random(3)
    for _ in range(200):
        A = [tuple(rng.random() for _ in range(3)) for _ in range(rng.randint(1, 8))]
        B = [tuple(rng.random() for _ in range(3)) for _ in range(rng.randint(1, 8))]
        assert set(mutual_nn_match(A, B)) <= greedy(A, B)


def test_empty_and_single():
    assert mutual_nn_match([], [(1.0,)]) == []
    assert mutual_nn_match([(1.0,)], []) == []
    assert mutual_nn_match([(1.0,)], [(7.0,)]) == [(0, 0)]
