# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/patchmatch/. The authors are listed in prov/2WYA23.jsonl.

import random

from patchmatch import nnf_brute_force, patch_distance, patchmatch, random_image


def test_example_trace() -> None:
    A = [[5, 9, 2, 7, 4, 8]]
    B = [[1, 6, 5, 9, 2, 7, 4, 8, 3]]
    init = {(x, 0): (d, 0) for x, d in enumerate([6, 2, -1, 4, -3, 1])}
    want = {
        0: ([6, 2, -1, 4, -3, 1], [1, 0, 16, 1, 4, 16]),
        1: ([6, 2, 2, 2, 2, 2], [1, 0, 0, 0, 0, 0]),
        2: ([2, 2, 2, 2, 2, 2], [0, 0, 0, 0, 0, 0]),
    }
    for t, (offs, dists) in want.items():
        f, D = patchmatch(A, B, 0, t, random.Random(0), init=init, search=False)
        assert [f[(x, 0)][0] for x in range(6)] == offs
        assert [D[(x, 0)] for x in range(6)] == dists


def test_patch_distance() -> None:
    A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    B = [[1, 2, 3], [4, 6, 6], [7, 8, 0]]
    assert patch_distance(A, B, 1, 1, 1, 1, 1) == 1 + 81
    assert patch_distance(A, B, 1, 1, 1, 1, 0) == 1
    # Early termination returns a value at or above the limit.
    assert patch_distance(A, B, 1, 1, 1, 1, 1, limit=5) >= 5


def test_distances_match_field() -> None:
    rng = random.Random(3)
    A = random_image(rng, 14, 11)
    B = random_image(rng, 17, 13)
    r = 1
    f, D = patchmatch(A, B, r, 4, random.Random(4))
    for (x, y), (dx, dy) in f.items():
        bx, by = x + dx, y + dy
        assert r <= bx < 17 - r and r <= by < 13 - r
        assert D[(x, y)] == patch_distance(A, B, x, y, bx, by, r)


def test_cost_never_increases() -> None:
    rng = random.Random(5)
    A = random_image(rng, 16, 12, levels=16)
    B = random_image(rng, 18, 14, levels=16)
    hist = []
    patchmatch(A, B, 1, 5, random.Random(6), history=hist)
    assert len(hist) == 6
    for before, after in zip(hist, hist[1:]):
        assert all(after[a] <= before[a] for a in before)


def test_against_brute_force_coherent() -> None:
    # B holds a noisy copy of A: the field is coherent, and PatchMatch finds
    # the exact nearest neighbor distance of every patch.
    rng = random.Random(9)
    B = random_image(rng, 24, 20)
    A = [[v + rng.randint(-3, 3) for v in row[5:19]] for row in B[4:16]]
    r = 1
    exact = nnf_brute_force(A, B, r)
    f, D = patchmatch(A, B, r, 4, random.Random(10))
    assert D == exact
    assert all(v == (5, 4) for v in f.values())


def test_against_brute_force_incoherent() -> None:
    # Two unrelated noise images: no coherence, so propagation helps little.
    # The answer is an upper bound on the exact distance and improves with T.
    rng = random.Random(7)
    A = random_image(rng, 12, 10, levels=8)
    B = random_image(rng, 14, 12, levels=8)
    r = 1
    exact = nnf_brute_force(A, B, r)
    total = []
    for t in (1, 4, 16):
        _, D = patchmatch(A, B, r, t, random.Random(8))
        assert all(D[a] >= exact[a] for a in exact)
        total.append(sum(D.values()))
    assert total[0] >= total[1] >= total[2]
    assert total[2] <= 1.2 * sum(exact.values())


def test_recovers_shifted_copy() -> None:
    for seed in (11, 12, 13):
        rng = random.Random(seed)
        B = random_image(rng, 30, 26)
        sx, sy = rng.randint(1, 8), rng.randint(1, 8)
        A = [row[sx:sx + 20] for row in B[sy:sy + 16]]
        f, D = patchmatch(A, B, 2, 5, random.Random(seed + 100))
        assert all(v == (sx, sy) for v in f.values())
        assert all(d == 0 for d in D.values())


def test_propagation_fills_region() -> None:
    # One correct seed and no random search: a forward and a backward pass
    # give every patch the true offset (the lemma of the proof).
    rng = random.Random(21)
    B = random_image(rng, 22, 18)
    A = [row[4:16] for row in B[3:15]]
    r = 1
    for seed_pos in ((1, 1), (5, 6), (10, 10), (10, 1)):
        init = {}
        for y in range(r, 12 - r):
            for x in range(r, 12 - r):
                init[(x, y)] = (rng.randint(-3, 8), rng.randint(-2, 5))
                if (x + init[(x, y)][0], y + init[(x, y)][1]) == (x + 4, y + 3):
                    init[(x, y)] = (-1, -1)
        init[seed_pos] = (4, 3)
        f, _ = patchmatch(A, B, r, 2, random.Random(0), init=init, search=False)
        assert all(v == (4, 3) for v in f.values())
        f1, _ = patchmatch(A, B, r, 1, random.Random(0), init=init, search=False)
        sx, sy = seed_pos
        for (x, y), v in f1.items():
            if x >= sx and y >= sy:
                assert v == (4, 3)


def test_deterministic() -> None:
    rng = random.Random(31)
    A = random_image(rng, 10, 9)
    B = random_image(rng, 12, 11)
    out1 = patchmatch(A, B, 1, 3, random.Random(32))
    out2 = patchmatch(A, B, 1, 3, random.Random(32))
    assert out1 == out2
