# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/additive-white-gaussian-noise-channel/. The authors are listed in prov/QYZ6QZ.jsonl.

import math
import random

from awgn_channel import (
    bi_awgn_capacity, bpsk_bit_error_rate, db, from_db, gaussian_capacity, hard_decision_capacity,
    q_function, required_ebn0_db, shannon_limit_ebn0, sigma2_for, simulate_bpsk, transmit,
)


def test_noise_statistics() -> None:
    rng = random.Random(4)
    y = transmit([0.0] * 50000, 0.7, rng)
    mean = sum(y) / len(y)
    var = sum(v * v for v in y) / len(y)
    assert abs(mean) < 0.01 and abs(var - 0.49) < 0.01


def test_q_function() -> None:
    assert math.isclose(q_function(0.0), 0.5)
    assert math.isclose(q_function(1.0), 0.15865525393145707, rel_tol=1e-12)
    assert math.isclose(q_function(-1.0), 1 - q_function(1.0))


def test_uncoded_bpsk() -> None:
    # 1e-5 needs about 9.6 dB
    assert bpsk_bit_error_rate(from_db(9.5)) > 1e-5 > bpsk_bit_error_rate(from_db(9.7))
    for e in (0.0, 4.0):
        mc = simulate_bpsk(200000, e, seed=17)
        exact = bpsk_bit_error_rate(from_db(e))
        assert abs(mc - exact) < 4 * math.sqrt(exact / 200000)


def test_shannon_limit() -> None:
    assert math.isclose(db(shannon_limit_ebn0(0.5)), 0.0, abs_tol=1e-12)
    assert abs(db(shannon_limit_ebn0(1.0)) - 1.76) < 0.005
    assert abs(db(shannon_limit_ebn0(1e-9)) - db(math.log(2))) < 1e-6
    assert abs(db(math.log(2)) + 1.59) < 0.005
    rates = [0.01 * i for i in range(1, 300)]
    vals = [shannon_limit_ebn0(r) for r in rates]
    assert all(a < b for a, b in zip(vals, vals[1:]))  # increasing in R
    # at the limit the Gaussian capacity equals the rate
    for r in (0.25, 0.5, 2.0):
        e = shannon_limit_ebn0(r)
        assert math.isclose(gaussian_capacity(2 * r * e), r)


def test_binary_input_capacity() -> None:
    for s2 in (0.05, 0.3, 1.0, 4.0):
        c = bi_awgn_capacity(s2)
        assert 0 < c < 1
        assert c < gaussian_capacity(1 / s2)  # binary inputs lose against Gaussian inputs
        assert hard_decision_capacity(s2) < c  # and the sign alone loses more
    assert bi_awgn_capacity(0.02) > 0.999999
    # finer integration agrees
    assert abs(bi_awgn_capacity(1.0, 400) - bi_awgn_capacity(1.0, 4000)) < 1e-9
    # at low SNR, C is close to SNR / (2 ln 2), the Gaussian value
    s2 = 400.0
    assert abs(bi_awgn_capacity(s2) / (1 / s2 / (2 * math.log(2))) - 1) < 0.01


def test_binary_input_capacity_by_monte_carlo() -> None:
    rng = random.Random(23)
    s2 = 1.0
    n = 200000
    acc = 0.0
    for _ in range(n):
        y = 1.0 + rng.gauss(0.0, 1.0)
        acc += math.log2(1 + math.exp(-2 * y / s2))
    assert abs((1 - acc / n) - bi_awgn_capacity(s2)) < 0.005


def test_limits_at_rate_one_half() -> None:
    soft = required_ebn0_db(0.5, bi_awgn_capacity)
    hard = required_ebn0_db(0.5, hard_decision_capacity)
    assert abs(soft - 0.187) < 0.005
    assert abs(hard - 1.77) < 0.01
    assert soft > db(shannon_limit_ebn0(0.5))


def test_hard_decision_low_rate_limit() -> None:
    # as R -> 0, hard decisions need pi ln 2 / 2 (about 0.37 dB) against ln 2 (about -1.59 dB)
    hard = required_ebn0_db(1e-3, hard_decision_capacity)
    assert abs(hard - db(math.pi * math.log(2) / 2)) < 0.01
    assert abs(db(math.pi / 2) - 1.96) < 0.005
    assert math.isclose(sigma2_for(0.5, 1.0), 1.0)
