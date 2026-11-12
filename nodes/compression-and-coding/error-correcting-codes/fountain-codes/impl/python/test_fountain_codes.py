# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fountain-codes/. The authors are listed in prov/BM90XJ.jsonl.

import itertools
import random
from fractions import Fraction

from fountain_codes import (OnlineDecoder, encode_symbol, expected_symbols, full_rank_probability,
                            symbols_needed)


def test_round_trip_any_order_any_symbols():
    rng = random.Random(1)
    k = 40
    source = [rng.getrandbits(128) for _ in range(k)]
    seeds = rng.sample(range(10 ** 6), 200)
    dec = OnlineDecoder(k)
    for s in seeds:  # any symbols, in any order
        if dec.done():
            break
        dec.add(*encode_symbol(source, s))
    assert dec.solve() == source


def test_full_rank_probability_exact_small():
    # brute force over all n x k binary matrices
    for k, n in ((2, 2), (2, 3), (3, 3), (3, 4)):
        good = 0
        for rows in itertools.product(range(1 << k), repeat=n):
            basis = []
            for v in rows:
                for b in basis:
                    v = min(v, v ^ b)
                if v:
                    basis.append(v)
            good += len(basis) == k
        assert Fraction(good, 2 ** (n * k)) == full_rank_probability(k, n)


def test_failure_bound_two_to_minus_e():
    for k in (5, 20, 100):
        for e in range(0, 12):
            fail = 1 - full_rank_probability(k, k + e)
            assert fail <= Fraction(1, 2 ** e)


def test_expected_overhead_and_monte_carlo():
    k, trials = 16, 1500
    rng = random.Random(2)
    counts = []
    for t in range(trials):
        source = [rng.getrandbits(8) for _ in range(k)]
        n, got = symbols_needed(source, 10 ** 6 * t)
        assert got == source
        counts.append(n)
    mean = sum(counts) / trials
    exact = float(expected_symbols(k))
    assert abs(exact - k - 1.6067) < 0.001  # sum 1/(2^j - 1) tends to 1.60669...
    assert abs(mean - exact) < 0.15
    for e in (0, 2, 5):
        frac = sum(c > k + e for c in counts) / trials
        assert abs(frac - float(1 - full_rank_probability(k, k + e))) < 0.04
