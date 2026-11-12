# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transform-coding/. The authors are listed in prov/H7K4T6.jsonl.

import math
import random

from transform_coding import (
    coding_gain, coefficient_variances, decode_block, empirical_entropy, encode_block, high_rate_allocation,
    reverse_water_filling,
)


def dct_matrix(n):
    return [[(math.sqrt(1 / n) if k == 0 else math.sqrt(2 / n)) * math.cos(math.pi * (2 * i + 1) * k / (2 * n)) for i in range(n)] for k in range(n)]


def ar1(n, rho):
    return [[rho ** abs(i - j) for j in range(n)] for i in range(n)]


def ar1_blocks(rng, count, n, rho):
    s = math.sqrt(1 - rho * rho)
    out = []
    for _ in range(count):
        v = rng.gauss(0, 1)
        b = [v]
        for _ in range(n - 1):
            v = rho * v + s * rng.gauss(0, 1)
            b.append(v)
        out.append(b)
    return out


def test_dct_variances_and_gain_ar1():
    # The example of the page: AR(1), rho = 0.9, N = 8, 8-point DCT.
    var = coefficient_variances(dct_matrix(8), ar1(8, 0.9))
    want = [6.1855, 1.0059, 0.3461, 0.1659, 0.1046, 0.0757, 0.0616, 0.0547]
    assert max(abs(a - b) for a, b in zip(var, want)) < 1e-4
    assert abs(sum(var) - 8.0) < 1e-12
    g = coding_gain(var)
    assert abs(10 * math.log10(g) - 6.2761) < 1e-4
    # The KLT gain has the closed form (1 - rho^2)^(-(N-1)/N); the DCT is just below it.
    assert g < (1 - 0.81) ** (-7 / 8) < g * 1.01


def test_gain_is_one_for_white_source_and_identity():
    assert abs(coding_gain([2.0] * 5) - 1.0) < 1e-12
    var = coefficient_variances([[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)], ar1(4, 0.9))
    assert abs(coding_gain(var) - 1.0) < 1e-12


def test_high_rate_allocation():
    var = coefficient_variances(dct_matrix(8), ar1(8, 0.9))
    b = high_rate_allocation(var, 2.0)
    assert abs(sum(b) / 8 - 2.0) < 1e-12
    want = [4.357, 3.047, 2.277, 1.747, 1.414, 1.181, 1.032, 0.946]
    assert max(abs(x - y) for x, y in zip(b, want)) < 1e-3
    # Equal distortion var_k 2^(-2 b_k) in each coefficient.
    d = [v * 2 ** (-2 * bk) for v, bk in zip(var, b)]
    assert max(d) - min(d) < 1e-12
    # At b = 1 the formula asks for a negative rate in the last coefficient.
    assert high_rate_allocation(var, 1.0)[7] < 0


def test_reverse_water_filling():
    var = coefficient_variances(dct_matrix(8), ar1(8, 0.9))
    theta, rates, dist = reverse_water_filling(var, 1.0)
    assert abs(sum(rates) - 8.0) < 1e-9
    assert min(rates) == 0.0 and rates[7] == 0.0
    assert abs(theta - 0.05956) < 1e-4
    theta, rates, dist = reverse_water_filling(var, 0.5)
    assert abs(sum(rates) - 4.0) < 1e-9
    assert rates[3:] == [0.0] * 5
    # The distortion of a coefficient with no bits is its variance.
    assert dist[3:] == var[3:]
    # At high rate it agrees with the formula.
    theta, rates, dist = reverse_water_filling(var, 4.0)
    assert max(abs(a - b) for a, b in zip(rates, high_rate_allocation(var, 4.0))) < 1e-9


def test_am_gm_random_orthogonal_transforms():
    # For any orthogonal transform the gain is at most that of the KLT, whose GM is det(R)^(1/N).
    rng = random.Random(27)
    for _ in range(500):
        n = rng.randint(2, 5)
        rho = rng.uniform(-0.95, 0.95)
        r = ar1(n, rho)
        a = [rng.gauss(0, 1) for _ in range(n)]
        aa = sum(t * t for t in a)
        h = [[(1.0 if i == j else 0.0) - 2 * a[i] * a[j] / aa for j in range(n)] for i in range(n)]
        var = coefficient_variances(h, r)
        det = (1 - rho * rho) ** (n - 1)
        assert coding_gain(var) <= (sum(var) / n) / det ** (1 / n) + 1e-9
        assert coding_gain(var) >= 1 - 1e-12


def test_monte_carlo_rate_saving():
    # Uniform quantizer with the same step for PCM and for the DCT coefficients:
    # same distortion step^2/12, and the rate drops by (1/2) log2(G) bits per sample.
    rng = random.Random(4)
    n, rho, step = 8, 0.9, 0.02
    blocks = ar1_blocks(rng, 20000, n, rho)
    c = dct_matrix(n)
    steps = [step] * n
    qs = [encode_block(c, steps, b) for b in blocks]
    rate_tc = sum(empirical_entropy([q[k] for q in qs]) for k in range(n)) / n
    rate_pcm = empirical_entropy([int(math.floor(v / step + 0.5)) for b in blocks for v in b])
    predicted = 0.5 * math.log2(coding_gain(coefficient_variances(c, ar1(n, rho))))
    assert abs((rate_pcm - rate_tc) - predicted) < 0.02
    mse = sum(sum((p - q) ** 2 for p, q in zip(decode_block(c, steps, qq), b)) for qq, b in zip(qs[:5000], blocks[:5000])) / (5000 * n)
    assert abs(mse / (step * step / 12) - 1) < 0.03


def test_round_trip_without_quantization_loss():
    rng = random.Random(28)
    c = dct_matrix(4)
    for _ in range(200):
        x = [rng.randint(-50, 50) for _ in range(4)]
        q = encode_block(c, [1e-6] * 4, x)
        y = decode_block(c, [1e-6] * 4, q)
        assert max(abs(a - b) for a, b in zip(x, y)) < 1e-5
