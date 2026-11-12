# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lt-codes/. The authors are listed in prov/1YD9K5.jsonl.

import math
import random
from fractions import Fraction

from lt_codes import (Sampler, decode, encode, ideal_soliton, neighbors, robust_soliton,
                      success_rate)


def test_ideal_soliton_exact():
    for k in (1, 2, 5, 40):
        rho = [Fraction(1, k)] + [Fraction(1, d * (d - 1)) for d in range(2, k + 1)]
        assert sum(rho) == 1  # 1/k + sum (1/(d-1) - 1/d) = 1/k + 1 - 1/k
        mean = sum((d + 1) * r for d, r in enumerate(rho))
        assert mean == Fraction(1, k) + sum(Fraction(1, j) for j in range(1, k))
        approx = ideal_soliton(k)
        assert all(math.isclose(approx[d + 1], float(rho[d])) for d in range(k))


def test_robust_soliton_formula_and_mackay_example():
    k, c, delta = 10000, 0.2, 0.05
    mu, r, beta = robust_soliton(k, c, delta)
    assert math.isclose(r, c * math.log(k / delta) * math.sqrt(k))
    assert round(r) == 244 and int(k / r) == 40 and round(k / r) == 41
    assert abs(beta - 1.31) < 0.01
    assert math.isclose(sum(mu), 1.0)
    spike = int(k / r)
    for d in (1, 2, 3, spike - 1, spike, spike + 1, k):
        rho = 1 / k if d == 1 else 1 / (d * (d - 1))
        tau = r / (d * k) if d < spike else (r * math.log(r / delta) / k if d == spike else 0)
        assert math.isclose(mu[d], (rho + tau) / beta)


def test_round_trip_with_packets():
    rng = random.Random(1)
    k = 200
    mu, _, _ = robust_soliton(k, 0.1, 0.5)
    s = Sampler(mu)
    source = [rng.getrandbits(256) for _ in range(k)]
    seeds = list(range(1000, 1000 + 2 * k))  # generous overhead: must decode
    vals = encode(source, seeds, s)
    assert decode(k, seeds, vals, s) == source
    # the decoder only needs the seed of each packet, not its degree or neighbors
    assert neighbors(1234, k, s) == neighbors(1234, k, s)


def test_partial_results_are_right():
    rng = random.Random(2)
    k = 300
    mu, _, _ = robust_soliton(k, 0.1, 0.5)
    s = Sampler(mu)
    source = [rng.getrandbits(32) for _ in range(k)]
    seeds = [rng.getrandbits(40) for _ in range(k)]  # no overhead: usually incomplete
    got = decode(k, seeds, encode(source, seeds, s), s)
    assert all(g is None or g == v for g, v in zip(got, source))


def test_success_rate_against_overhead():
    k = 500
    mu, _, _ = robust_soliton(k, 0.1, 0.5)
    robust, ideal = Sampler(mu), Sampler(ideal_soliton(k))
    rates = [success_rate(k, ov, robust, 20, 7) for ov in (0.05, 0.25, 0.5)]
    assert rates == [0.0, 0.8, 1.0]
    ideal_rates = [success_rate(k, ov, ideal, 20, 7) for ov in (0.25, 0.5)]
    assert ideal_rates == [0.2, 0.6]  # the ideal soliton loses its ripple too often
