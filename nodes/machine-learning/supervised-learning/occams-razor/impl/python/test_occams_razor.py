# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/occams-razor/. The authors are listed in prov/XZEN4M.jsonl.

import math
import random
from fractions import Fraction
from itertools import combinations

from occams_razor import (decode, description_length, draw, encode, gamma_code, greedy_occam, literal_bits,
                          occam_bound, predict, random_target, sample_size, true_error)


def test_gamma_code() -> None:
    assert [gamma_code(n) for n in (1, 2, 3, 4, 9)] == ["1", "010", "011", "00100", "0001001"]
    for n in range(1, 200):
        assert len(gamma_code(n)) == 2 * (n.bit_length() - 1) + 1


def test_code_is_prefix_free_and_decodes() -> None:
    d = 3
    hyps = [c for s in range(2 * d + 1) for c in combinations(range(2 * d), s)]
    words = [encode(h, d) for h in hyps]
    for h, w in zip(hyps, words):
        assert decode(w + "1011", d) == (h, "1011")
    for a in words:
        for b in words:
            assert a == b or not b.startswith(a)


def test_kraft_sum_at_most_one() -> None:
    for d in (1, 2, 3, 5, 12):
        total = sum((Fraction(math.comb(2 * d, s), 2 ** (len(gamma_code(s + 1)) + s * literal_bits(d)))
                     for s in range(2 * d + 1)), Fraction(0))
        assert total <= 1


def test_greedy_is_consistent_and_short() -> None:
    rng = random.Random(7)
    for _ in range(200):
        d, k = rng.randint(3, 10), rng.randint(1, 3)
        target = random_target(d, k, rng)
        s = draw(target, d, rng.randint(1, 120), rng)
        h = greedy_occam(s, d)
        assert all(predict(h, x) == y for x, y in s)
        negs = sum(1 for _, y in s if y == 0)
        if negs:
            assert len(h) <= k * (math.log(negs) + 1)
        else:
            assert h == ()


def test_inconsistent_sample_is_rejected() -> None:
    s = [((0, 0), 1), ((1, 1), 1), ((0, 1), 0), ((1, 0), 0)]  # x0 xor x1 is false here: no conjunction fits
    try:
        greedy_occam(s, 2)
    except ValueError:
        return
    raise AssertionError("expected ValueError")


def test_occam_bound_fails_at_most_delta_of_the_time() -> None:
    rng = random.Random(3)
    d, delta, trials = 10, 0.1, 150
    fails = 0
    for _ in range(trials):
        target = random_target(d, 4, rng)
        n = rng.choice((20, 40, 80))
        h = greedy_occam(draw(target, d, n, rng), d)
        if true_error(h, target, d) > occam_bound(description_length(h, d), n, delta):
            fails += 1
    assert fails <= delta * trials


def test_sample_size_matches_bound() -> None:
    for bits in (5, 20, 38):
        for eps, delta in ((0.1, 0.05), (0.01, 0.01)):
            n = sample_size(bits, eps, delta)
            assert occam_bound(bits, n, delta) <= eps < occam_bound(bits, n - 1, delta)
