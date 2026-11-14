# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/orthogonal-array/. The authors are listed in prov/5Q12GA.jsonl.

import random
from itertools import product

from orthogonal_array import dual_distance, from_linear_code, from_mols, has_strength, rao_bound, strength

SIMPLEX = [[1, 0, 1, 0, 1, 0, 1], [0, 1, 1, 0, 0, 1, 1], [0, 0, 0, 1, 1, 1, 1]]  # columns 1..7 in binary
EXT_HAMMING = [[1] * 8, [0, 0, 0, 0, 1, 1, 1, 1], [0, 0, 1, 1, 0, 0, 1, 1], [0, 1, 0, 1, 0, 1, 0, 1]]


def test_small_examples() -> None:
    oa4 = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    assert strength(oa4, 2) == 2 and rao_bound(3, 2, 2) == 4
    oa9 = from_mols([[[0, 1, 2], [1, 2, 0], [2, 0, 1]], [[0, 1, 2], [2, 0, 1], [1, 2, 0]]])
    assert len(oa9) == 9 and strength(oa9, 3) == 2 and rao_bound(4, 3, 2) == 9


def test_simplex_code_meets_the_rao_bound() -> None:
    oa = from_linear_code(SIMPLEX, 2)
    assert len(oa) == 8 and strength(oa, 2) == 2
    assert dual_distance(SIMPLEX, 2) == 3  # the dual is the Hamming [7, 4, 3] code
    assert rao_bound(7, 2, 2) == 8


def test_extended_hamming_is_a_tight_strength_three_array() -> None:
    oa = from_linear_code(EXT_HAMMING, 2)
    assert len(oa) == 16 and strength(oa, 2) == 3
    assert rao_bound(8, 2, 3) == 16
    assert dual_distance(EXT_HAMMING, 2) == 4  # the code is self-dual


def test_code_duality_on_random_codes() -> None:
    rng = random.Random(1)
    for p, k_max in ((2, 8), (3, 5)):
        for _ in range(30):
            k = rng.randint(3, k_max)
            m = rng.randint(1, k - 1)
            gen = [[rng.randrange(p) for _ in range(k)] for _ in range(m)]
            rows = from_linear_code(gen, p)
            # dual_distance returns k + 1 when the dual code is {0}; then the array is all of GF(p)^k
            assert strength(rows, p) == min(dual_distance(gen, p), k + 1) - 1


def test_rao_bound_holds_for_every_array_found() -> None:
    rng = random.Random(2)
    for _ in range(60):
        k = rng.randint(3, 7)
        m = rng.randint(1, k)
        gen = [[rng.randrange(2) for _ in range(k)] for _ in range(m)]
        rows = from_linear_code(gen, 2)
        t = strength(rows, 2)
        if t >= 1:
            assert len(rows) >= rao_bound(k, 2, t)


HAMMING = [[1, 0, 0, 0, 0, 1, 1], [0, 1, 0, 0, 1, 0, 1], [0, 0, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 1]]
MOLS4 = [[[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
         [[0, 1, 2, 3], [2, 3, 0, 1], [3, 2, 1, 0], [1, 0, 3, 2]],
         [[0, 1, 2, 3], [3, 2, 1, 0], [1, 0, 3, 2], [2, 3, 0, 1]]]
PB12 = "++-+++---+-"


def test_hamming_code_is_a_strength_three_array_above_the_rao_bound() -> None:
    oa = from_linear_code(HAMMING, 2)
    assert len(oa) == 16 and strength(oa, 2) == 3
    assert sorted(sum(r) for r in oa) == [0] + [3] * 7 + [4] * 7 + [7]  # the [7, 4, 3] code
    assert dual_distance(HAMMING, 2) == 4  # the dual is the [7, 3] simplex code
    assert rao_bound(7, 2, 3) == 14  # and N must be a multiple of 2^3, so 16 is the least possible
    assert rao_bound(7, 2, 3) < 16 and 16 % 8 == 0 and 14 % 8 != 0


def test_examples_and_non_examples() -> None:
    # complete set of MOLS of order 4: OA(16, 5, 4, 2) meeting the Rao bound 1 + 5 * 3
    oa = from_mols(MOLS4)
    assert len(oa) == 16 and strength(oa, 4) == 2 and rao_bound(5, 4, 2) == 16
    # the half fraction I = ABC: strength exactly 2
    half = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
    assert has_strength(half, 2, 2) and not has_strength(half, 2, 3)
    # the 12-run Plackett-Burman design: OA(12, 11, 2, 2), on the Rao bound, strength not 3
    g = [1 if c == "+" else 0 for c in PB12]
    pb = [tuple(g[(j + i) % 11] for j in range(11)) for i in range(11)] + [(0,) * 11]
    assert strength(pb, 2) == 2 and rao_bound(11, 2, 2) == 12
    # a covering array of strength 2 that is not an orthogonal array
    cover = [(0, 0, 0, 0), (0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0)]
    for a in range(4):
        for b in range(a + 1, 4):
            pairs = [(r[a], r[b]) for r in cover]
            assert sorted(pairs.count(p) for p in product((0, 1), repeat=2)) == [1, 1, 1, 2]
            assert pairs.count((1, 1)) == 2
    assert not has_strength(cover, 2, 2)
    # no OA(8, 8, 2, 2): the Rao bound is 9
    assert rao_bound(8, 2, 2) == 9
    # the extended Hamming code: the 2^(8-4) design of resolution IV is an OA of strength 3
    assert strength(from_linear_code(EXT_HAMMING, 2), 2) == 3


def test_strength_two_gives_orthogonal_main_effects() -> None:
    # centered functions of two different columns are orthogonal over the runs
    oa = from_linear_code([[1, 0, 1, 2], [0, 1, 1, 1]], 3)  # OA(9, 4, 3, 2)
    assert strength(oa, 3) == 2
    rng = random.Random(3)
    for _ in range(50):
        f = [rng.randint(-5, 5) for _ in range(3)]
        g = [rng.randint(-5, 5) for _ in range(3)]
        f = [3 * v - sum(f) for v in f]
        g = [3 * v - sum(g) for v in g]
        for i in range(4):
            for j in range(4):
                if i != j:
                    assert sum(f[r[i]] * g[r[j]] for r in oa) == 0


def test_full_factorial_has_strength_k() -> None:
    for s, k in ((2, 4), (3, 3)):
        rows = list(product(range(s), repeat=k))
        assert strength(rows, s) == k and has_strength(rows, s, k)
