# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/list-decoding/. The authors are listed in prov/4JPZFM.jsonl.

import itertools
import math
import random

from list_decoding import (capacity_radius, entropy_q, hamming_distance, johnson_list_bound,
                           johnson_radius, list_decode_brute_force)


def rs_code(p: int, xs: list[int], k: int) -> list[tuple[int, ...]]:
    """All codewords (f(x))_x for deg f < k over GF(p), in the order of the coefficients."""
    out = []
    for coeffs in itertools.product(range(p), repeat=k):
        out.append(tuple(sum(c * pow(x, i, p) for i, c in enumerate(coeffs)) % p for x in xs))
    return out


def test_reed_solomon_example() -> None:
    # RS over GF(7) at the points 1 .. 6, k = 2, d = 5: unique decoding radius 2
    code = rs_code(7, [1, 2, 3, 4, 5, 6], 2)
    y = (0, 0, 0, 4, 5, 6)
    assert list_decode_brute_force(code, y, 2) == []
    assert list_decode_brute_force(code, y, 3) == [(0,) * 6, (1, 2, 3, 4, 5, 6)]  # f = 0 and f = x
    assert len(list_decode_brute_force(code, y, 4)) == 11
    assert johnson_list_bound(6, 5, 3) == 4
    assert johnson_list_bound(6, 5, 4) is None


def test_johnson_bound_on_random_words() -> None:
    rng = random.Random(1962)
    cases = [(7, list(range(1, 7)), 2, 400), (11, list(range(1, 11)), 3, 150)]
    for p, xs, k, trials in cases:
        code = rs_code(p, xs, k)
        n, d = len(xs), len(xs) - k + 1
        e = max(r for r in range(n) if johnson_list_bound(n, d, r) is not None)
        bound = johnson_list_bound(n, d, e)
        assert bound is not None
        for _ in range(trials):
            if rng.random() < 0.5:
                y = tuple(rng.randrange(p) for _ in xs)
            else:  # a mix of two codewords, which tends to give larger lists
                c1, c2 = rng.sample(code, 2)
                cut = rng.randrange(n + 1)
                y = c1[:cut] + c2[cut:]
            assert len(list_decode_brute_force(code, y, e)) <= bound


def test_reed_muller_1_4_all_words() -> None:
    # RM(1, 4) = [16, 5, 8]: unique radius 3; the Johnson bound allows radius 4 with at most 4 words
    gens = [0xFFFF, 0x5555, 0x3333, 0x0F0F, 0x00FF]
    code = [0]
    for g in gens:
        code += [c ^ g for c in code]
    assert min(bin(c).count("1") for c in code if c) == 8
    bound = johnson_list_bound(16, 8, 4)
    assert bound == 4 and johnson_list_bound(16, 8, 5) is None
    worst3 = worst4 = 0
    for y in range(1 << 16):
        dists = [bin(y ^ c).count("1") for c in code]
        worst3 = max(worst3, sum(1 for t in dists if t <= 3))
        worst4 = max(worst4, sum(1 for t in dists if t <= 4))
    assert worst3 == 1
    assert worst4 == bound  # the bound is tight here


def test_johnson_radius_values() -> None:
    assert johnson_radius(0.5, 2) == 0.5
    # for Reed-Solomon codes, delta = 1 - R, and J = 1 - sqrt(R) exceeds the unique radius (1 - R) / 2
    for rate in (0.1, 0.25, 0.5, 0.75, 0.9):
        j = johnson_radius(1 - rate)
        assert abs(j - (1 - math.sqrt(rate))) < 1e-12
        assert j > (1 - rate) / 2
    # J_q decreases to the alphabet free value 1 - sqrt(1 - delta) as q grows
    vals = [johnson_radius(0.4, q) for q in (2, 4, 16, 256, 1 << 20)]
    assert vals == sorted(vals, reverse=True) and abs(vals[-1] - johnson_radius(0.4)) < 1e-5


def test_capacity() -> None:
    assert abs(entropy_q(0.5, 2) - 1) < 1e-12
    assert abs(entropy_q(1 - 1 / 5, 5) - 1) < 1e-12
    assert abs(capacity_radius(0.5, 2) - 0.110028) < 1e-5  # h_2(0.110028) = 1/2
    for rate in (0.25, 0.5, 0.75):
        ps = [capacity_radius(rate, q) for q in (2, 16, 256, 1 << 16, 1 << 40)]
        assert ps == sorted(ps) and ps[-1] < 1 - rate
        assert 1 - rate - ps[-1] < 0.05  # large alphabets approach 1 - R
        # for Reed-Solomon codes the Johnson radius 1 - sqrt(R) is below the capacity 1 - R
        assert 1 - math.sqrt(rate) < 1 - rate


def test_distance_helper() -> None:
    assert hamming_distance((1, 2, 3), (1, 0, 3)) == 1
    assert list_decode_brute_force([(0, 0), (1, 1)], (0, 1), 1) == [(0, 0), (1, 1)]
