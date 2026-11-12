# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/channel-coding-theorem/. The authors are listed in prov/VK14Z9.jsonl.

import math
import random

from channel_coding_theorem import (
    bsc_capacity, fano_lower_bound, ml_decode, random_code_error_rate, typicality_decode, union_bound,
)

P = 0.11  # capacity is close to 1/2
TRIALS = 600


def se(x: float, n: int) -> float:
    return math.sqrt(max(x * (1 - x), 1e-4) / n)


def test_capacity_value() -> None:
    assert abs(bsc_capacity(P) - 0.5) < 0.001


def test_below_capacity_error_falls() -> None:
    rate = 0.25
    errs = [random_code_error_rate(n, rate, P, TRIALS, seed=n) for n in (8, 24, 40)]
    assert errs[0] > errs[2]
    for n, e in zip((8, 24, 40), errs):
        assert e <= union_bound(n, 2 ** round(n * rate), P) + 3 * se(e, TRIALS)
    # the bound itself goes to 0 for R < C
    assert union_bound(200, 2 ** 50, P) < 1e-4


def test_above_capacity_error_grows() -> None:
    rate = 0.75
    errs = [random_code_error_rate(n, rate, P, 300, seed=100 + n) for n in (4, 16)]
    assert errs[1] > errs[0]
    for n, e in zip((4, 16), errs):
        assert e >= fano_lower_bound(n, rate, bsc_capacity(P)) - 3 * se(e, 300)
    assert fano_lower_bound(10 ** 6, rate, bsc_capacity(P)) > 0.33  # tends to 1 - C/R = 1/3


def test_typicality_decoder_is_weaker_but_works() -> None:
    n, rate = 40, 0.2
    ml = random_code_error_rate(n, rate, P, TRIALS, seed=5)
    typ = random_code_error_rate(n, rate, P, TRIALS, seed=5, decoder="typ", delta=0.1)
    assert typ >= ml - 3 * se(ml, TRIALS)
    assert typ < 0.3


def test_ml_decoder_exhaustive_small() -> None:
    # nearest codeword with random tie-breaking: compare with brute force over all y
    rng = random.Random(9)
    code = [0b0000, 0b0111, 0b1011, 0b1100]
    for y in range(16):
        dists = [(c ^ y).bit_count() for c in code]
        out = ml_decode(code, y, rng)
        assert dists[out] == min(dists)
    assert typicality_decode(code, 0b0001, 4, 0.25, 0.0) == 0  # only 0000 is at distance 1


def test_union_bound_is_exact_for_two_codewords() -> None:
    # for m = 2 and ties as errors, the bound is exact: compare with full enumeration, n = 6
    n, p = 6, 0.2
    exact = 0.0
    for z in range(1 << n):
        pz = p ** z.bit_count() * (1 - p) ** (n - z.bit_count())
        for other in range(1 << n):  # the other codeword, uniform; the sent one is 0
            if (other ^ z).bit_count() <= z.bit_count():
                exact += pz / (1 << n)
    assert math.isclose(union_bound(n, 2, p), exact)
