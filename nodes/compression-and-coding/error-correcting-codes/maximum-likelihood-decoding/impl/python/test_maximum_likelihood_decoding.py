# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-likelihood-decoding/. The authors are listed in prov/16771S.jsonl.

import math
import random
from itertools import product

from maximum_likelihood_decoding import (
    binary_asymmetric,
    bsc,
    codewords,
    likelihood,
    map_decode,
    min_distance_decode,
    ml_decode,
    soft_ml_decode,
)

G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]
REP3 = [(0, 0, 0), (1, 1, 1)]


def dist(a, b):
    return sum(x != y for x, y in zip(a, b))


def q_func(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


def test_ml_equals_min_distance_on_bsc_exhaustive():
    rng = random.Random(1)
    codes = [codewords(G74), codewords([[1, 0, 1, 1, 0], [0, 1, 0, 1, 1]])]
    for _ in range(20):
        n, k = rng.randint(3, 7), rng.randint(1, 3)
        codes.append(codewords([[rng.randrange(2) for _ in range(n)] for _ in range(k)]))
    for code in codes:
        n = len(code[0])
        for p in (0.01, 0.1, 0.3, 0.49):
            w = bsc(p)
            for y in product(range(2), repeat=n):
                a = ml_decode(code, w, y)
                b = min_distance_decode(code, y)
                assert dist(a, y) == dist(b, y)
                assert math.isclose(likelihood(w, a, y), likelihood(w, b, y))


def test_bsc_above_half_prefers_far_codewords():
    w = bsc(0.9)
    assert ml_decode(REP3, w, (0, 0, 1)) == (1, 1, 1)
    assert min_distance_decode(REP3, (0, 0, 1)) == (0, 0, 0)


def test_z_channel_example():
    w = binary_asymmetric(0.0, 0.4)
    y = (0, 0, 1)
    assert likelihood(w, (0, 0, 0), y) == 0.0
    assert math.isclose(likelihood(w, (1, 1, 1), y), 0.096)
    assert ml_decode(REP3, w, y) == (1, 1, 1)
    assert min_distance_decode(REP3, y) == (0, 0, 0)


def test_asymmetric_channel_both_below_half():
    w = binary_asymmetric(0.01, 0.3)
    code = [(0, 0, 0, 0, 0), (1, 1, 1, 1, 0)]
    y = (1, 0, 0, 0, 0)
    assert math.isclose(likelihood(w, code[0], y), 0.01 * 0.99**4)
    assert math.isclose(likelihood(w, code[1], y), 0.7 * 0.3**3 * 0.99)
    assert ml_decode(code, w, y) == code[1]
    assert min_distance_decode(code, y) == code[0]


def test_map_versus_ml():
    w = bsc(0.1)
    y = (0, 1, 1)
    assert ml_decode(REP3, w, y) == (1, 1, 1)
    assert map_decode(REP3, [0.5, 0.5], w, y) == (1, 1, 1)
    assert map_decode(REP3, [0.95, 0.05], w, y) == (0, 0, 0)
    post0 = 0.95 * 0.1**2 * 0.9 / (0.95 * 0.1**2 * 0.9 + 0.05 * 0.1 * 0.9**2)
    assert abs(post0 - 19 / 28) < 1e-12


def test_soft_versus_hard():
    r = [0.9, -0.2, -0.3]
    hard = tuple(0 if x > 0 else 1 for x in r)
    assert min_distance_decode(REP3, hard) == (1, 1, 1)
    assert soft_ml_decode(REP3, r) == (0, 0, 0)


def test_correlation_equals_gaussian_likelihood():
    rng = random.Random(9)
    code = codewords(G74)
    for _ in range(500):
        r = [rng.gauss(0, 1.5) for _ in range(7)]
        a = soft_ml_decode(code, r)
        best = min(sum((ri - (1 - 2 * b)) ** 2 for ri, b in zip(r, c)) for c in code)
        assert math.isclose(sum((ri - (1 - 2 * b)) ** 2 for ri, b in zip(r, a)), best)


def test_monte_carlo_bsc_exact_formula():
    rng = random.Random(2026)
    code = codewords(G74)
    w = bsc(0.05)
    trials, errors = 20000, 0
    for _ in range(trials):
        c = code[rng.randrange(16)]
        y = tuple(b ^ (1 if rng.random() < 0.05 else 0) for b in c)
        errors += ml_decode(code, w, y) != c
    exact = 1 - 0.95**7 - 7 * 0.05 * 0.95**6
    assert abs(exact - 0.0443805) < 1e-6
    sd = math.sqrt(exact * (1 - exact) / trials)
    assert abs(errors / trials - exact) < 4 * sd


def test_monte_carlo_awgn_union_bound():
    code = codewords(G74)
    rate = 4 / 7
    spectrum = {3: 7, 4: 7, 7: 1}
    ebn0 = 10 ** (4.0 / 10)
    sigma = math.sqrt(1 / (2 * rate * ebn0))
    union = sum(a * q_func(math.sqrt(2 * w * rate * ebn0)) for w, a in spectrum.items())
    lower = q_func(math.sqrt(2 * 3 * rate * ebn0))
    rng = random.Random(7)
    trials, errors = 20000, 0
    for _ in range(trials):
        c = code[rng.randrange(16)]
        r = [1 - 2 * b + rng.gauss(0, sigma) for b in c]
        errors += soft_ml_decode(code, r) != c
    rate_hat = errors / trials
    sd = math.sqrt(union * (1 - union) / trials)
    assert lower < rate_hat < union + 3 * sd
    ph = q_func(math.sqrt(2 * rate * ebn0))
    hard = 1 - (1 - ph) ** 7 - 7 * ph * (1 - ph) ** 6
    assert rate_hat < hard
