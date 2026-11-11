# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fair-coin-flipping/. The authors are listed in prov/5SB3X8.jsonl.
# There are no official test vectors for coin flipping protocols. The tests
# run local simulated parties and measure the bias of each strategy.

import random
from fractions import Fraction
from functools import lru_cache
from math import comb

from fair_coin_flipping import (
    AbortingAlice,
    HonestAlice,
    LyingAlice,
    blum_flip,
    check_open,
    commit,
    majority_attack_value,
    no_commitment_flip,
)

RUNS = 4000


def frequency_of_one(make_alice, seed):
    rng = random.Random(seed)
    ones = sum(blum_flip(make_alice(rng), rng) for _ in range(RUNS))
    return ones / RUNS


def test_commitment_opens():
    c, r = commit(1)
    assert check_open(c, 1, r)
    assert not check_open(c, 0, r)
    assert not check_open(c, 2, r)


def test_honest_flip_is_fair():
    f = frequency_of_one(HonestAlice, 1)
    # The standard deviation of the mean is 1/(2 sqrt(4000)), about 0.008.
    assert abs(f - 0.5) < 0.04


def test_binding_stops_a_lying_alice():
    # Alice cannot open her commitment to the other bit, so Bob treats the
    # bad opening as an abort and outputs a random bit: Pr[1] = 3/4, the
    # same as an abort, and no more.
    f = frequency_of_one(lambda rng: LyingAlice(rng, 1), 2)
    assert abs(f - 0.75) < 0.04


def test_aborting_alice_biases_the_naive_protocol():
    # Alice wants 1. When a xor b = 0 she does not open, and Bob outputs a
    # fresh random bit. Pr[1] = 1/2 + 1/2 * 1/2 = 3/4: a bias of 1/4.
    f = frequency_of_one(lambda rng: AbortingAlice(rng, 1), 3)
    measured_bias = f - 0.5
    assert 0.21 < measured_bias < 0.29


def test_aborting_alice_against_a_fixed_default():
    # If Bob outputs a fixed default 0 on abort, an Alice who wants 0 always
    # gets it: the bias is 1/2.
    rng = random.Random(4)
    zeros = 0
    for _ in range(RUNS):
        alice = AbortingAlice(rng, 0)
        alice.first()
        b = rng.getrandbits(1)
        opening = alice.second(b)
        out = 0 if opening is None else opening[0] ^ b
        zeros += out == 0
    assert zeros == RUNS


def test_without_commitment_bob_decides():
    for a in (0, 1):
        for wish in (0, 1):
            assert no_commitment_flip(a, wish) == wish


def test_majority_attack_exact_values():
    # One flip: the abort attack gives exactly 3/4.
    assert majority_attack_value(1) == Fraction(3, 4)
    rs = (1, 3, 9, 25, 81)
    biases = [float(majority_attack_value(r)) - 0.5 for r in rs]
    # The bias falls as r grows ...
    assert all(x > y for x, y in zip(biases, biases[1:]))
    # ... about like 1/sqrt(r): bias * sqrt(r) stays in a narrow band.
    scaled = [b * r ** 0.5 for r, b in zip(rs[2:], biases[2:])]
    assert max(scaled) / min(scaled) < 1.3
    # It always stays above the order 1/r of Cleve's lower bound.
    for r, b in zip(rs, biases):
        assert b >= 1 / (4 * r)


def test_majority_attack_matches_simulation():
    # An independent recursive form of Alice's optimal rule, run as a game.
    r = 5
    need = (r + 1) // 2

    def tail(k, s):
        return Fraction(sum(comb(k, j) for j in range(k + 1) if s + j >= need), 2 ** k)

    @lru_cache(maxsize=None)
    def cont(i, s):
        # value before round i with s ones so far, Alice still free to abort
        if i > r:
            return Fraction(1 if s >= need else 0)
        ab = tail(r - i + 1, s)
        return (max(cont(i + 1, s), ab) + max(cont(i + 1, s + 1), ab)) / 2

    assert cont(1, 0) == majority_attack_value(r)
    rng = random.Random(9)
    ones = 0
    trials = 20000
    for _ in range(trials):
        s = 0
        for i in range(1, r + 1):
            c = rng.getrandbits(1)                       # Alice sees the coin first
            if tail(r - i + 1, s) > cont(i + 1, s + c):  # abort pays more
                s += sum(rng.getrandbits(1) for _ in range(r - i + 1))
                break
            s += c
        ones += s >= need
    assert abs(ones / trials - float(cont(1, 0))) < 0.02
