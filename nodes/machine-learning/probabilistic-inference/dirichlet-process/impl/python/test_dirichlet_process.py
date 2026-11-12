# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dirichlet-process/. The authors are listed in prov/CRF0XV.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

from dirichlet_process import (block_sizes, crp, ewens, expected_tables,
                               number_of_tables_distribution, polya_urn, seatings,
                               sequential_probability, stick_breaking, stirling_first_unsigned)

ALPHAS = [Fraction(1, 3), Fraction(1), Fraction(2), Fraction(7, 2)]
BELL = [1, 1, 2, 5, 15, 52, 203, 877]


def uniform(rng):
    return rng.random()


def test_crp_probability_is_the_ewens_formula():
    for n in range(1, 7):
        all_seatings = list(seatings(n))
        assert len(all_seatings) == BELL[n]
        for a in ALPHAS:
            total = Fraction(0)
            for s in all_seatings:
                p = sequential_probability(s, a)
                assert p == ewens(block_sizes(s), a)
                total += p
            assert total == 1


def test_number_of_tables_is_given_by_stirling_numbers():
    c = stirling_first_unsigned(7)
    assert c[4][1:5] == [6, 11, 6, 1] and sum(c[7]) == math.factorial(7)
    for n in range(1, 8):
        for a in ALPHAS:
            dist = number_of_tables_distribution(n, a)
            by_k = [Fraction(0)] * (n + 1)
            for s in seatings(n):
                by_k[max(s) + 1] += ewens(block_sizes(s), a)
            assert by_k == dist and sum(dist) == 1
            assert sum(k * p for k, p in enumerate(dist)) == expected_tables(n, a)


def test_example_of_the_page():
    dist = number_of_tables_distribution(4, 2)
    assert dist[1:] == [Fraction(1, 10), Fraction(11, 30), Fraction(2, 5), Fraction(2, 15)]
    assert expected_tables(4, 2) == Fraction(77, 30)
    assert ewens([2, 1, 1], 2) == Fraction(1, 15)
    assert sequential_probability([0, 0, 1, 2], 2) == Fraction(1, 15)
    assert abs(float(expected_tables(1000, 1)) - 7.4855) < 1e-4
    assert abs(float(expected_tables(1000, 10)) - 10 * (math.log(1 + 1000 / 10))) < 1


def test_crp_sampler_matches_ewens():
    rng = random.Random(1)
    n, a, s = 4, 2.0, 40000
    freq = Counter(tuple(crp(n, a, rng)[0]) for _ in range(s))
    tv = sum(abs(freq[tuple(x)] / s - float(ewens(block_sizes(x), Fraction(2)))) for x in seatings(n)) / 2
    assert tv < 0.015


def test_expected_number_of_tables_by_simulation():
    rng = random.Random(2)
    n, a, s = 200, 3.0, 2000
    mean = sum(len(crp(n, a, rng)[1]) for _ in range(s)) / s
    assert abs(mean - float(expected_tables(n, a))) < 0.15


def test_stick_breaking_mass_and_remainder():
    rng = random.Random(3)
    a, k, s = 2.0, 5, 40000
    acc = 0.0
    for _ in range(s):
        w, _, rem = stick_breaking(a, k, uniform, rng)
        assert all(x > 0 for x in w) and abs(sum(w) + rem - 1) < 1e-12
        acc += rem
    assert abs(acc / s - (a / (1 + a)) ** k) < 0.005
    w, _, rem = stick_breaking(a, 300, uniform, rng)
    assert rem < 1e-20


def test_two_constructions_agree_on_ties():
    # P(theta_1 = theta_2) is 1 / (1 + alpha) in the urn, and E[sum pi_k^2] for stick breaking.
    rng = random.Random(4)
    a, s = 1.5, 30000
    urn = sum(len(set(polya_urn(2, a, uniform, rng))) == 1 for _ in range(s)) / s
    sticks = 0.0
    for _ in range(s // 10):
        w, _, _ = stick_breaking(a, 120, uniform, rng)
        sticks += sum(x * x for x in w)
    sticks /= s // 10
    assert abs(urn - 1 / (1 + a)) < 0.015 and abs(sticks - 1 / (1 + a)) < 0.015
