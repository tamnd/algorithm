# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/secure-multiparty-computation/. The authors are listed in prov/RFTBQB.jsonl.
# There are no official test vectors for MPC protocols. These tests compare the
# real protocol with the ideal functionality, and check counts and properties.

import random
from collections import Counter

from secure_multiparty_computation import (
    harness,
    ideal_world,
    real_weighted_sum,
    share_additive,
    weighted_sum_functionality,
)

M = 2**64


def test_worked_example() -> None:
    # Three salaries; the page's example.
    xs = [52, 61, 47]
    t = real_weighted_sum(xs, [1, 1, 1], 1000, random.Random(7))
    assert t.outputs == [160, 160, 160]
    assert t.messages == 2 * 3 * 2
    assert t.rounds == 2


def test_ideal_and_real_agree_on_random_inputs() -> None:
    rng = random.Random(1987)
    for _ in range(600):
        n = rng.randrange(2, 8)
        modulus = rng.choice([2, 5, 97, M])
        xs = [rng.randrange(modulus) for _ in range(n)]
        ws = [rng.randrange(modulus) for _ in range(n)]
        assert harness(xs, ws, modulus, rng)


def test_message_count_is_2n_n_minus_1() -> None:
    rng = random.Random(3)
    for n in range(2, 12):
        t = real_weighted_sum([1] * n, [1] * n, M, rng)
        assert t.messages == 2 * n * (n - 1)


def test_shares_add_up_and_one_share_is_uniform() -> None:
    rng = random.Random(11)
    for _ in range(200):
        x = rng.randrange(M)
        assert sum(share_additive(x, 5, M, rng)) % M == x
    # Over Z_5 the first share of x = 3 takes each value about equally often.
    counts = Counter(share_additive(3, 3, 5, rng)[0] for _ in range(10000))
    chi2 = sum((counts[v] - 2000) ** 2 / 2000 for v in range(5))
    assert chi2 < 18.5  # 0.999 quantile of chi-square with 4 degrees of freedom


def test_the_ideal_world_also_leaks_what_the_output_implies() -> None:
    # With two parties and f = x1 + x2, party 1 learns x2 = y - x1 in the
    # ideal world too. Security means "no more than this", not "nothing".
    f = weighted_sum_functionality([1, 1], M)
    y = ideal_world(f, [10, 32])[0]
    assert y - 10 == 32


def test_bad_functionality_is_rejected() -> None:
    try:
        ideal_world(lambda xs: [0], [1, 2])
    except ValueError:
        return
    raise AssertionError("expected ValueError")
