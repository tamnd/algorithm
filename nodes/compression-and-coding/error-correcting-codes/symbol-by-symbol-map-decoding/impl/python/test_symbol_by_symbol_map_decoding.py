# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbol-by-symbol-map-decoding/. The authors are listed in prov/M3KJWK.jsonl.

import math
import random

from symbol_by_symbol_map_decoding import bitwise_map, block_map, exact_rates_bsc, linear_code

EVEN3 = [(0, 0, 0), (0, 1, 1), (1, 0, 1), (1, 1, 0)]
G74 = [[1, 0, 0, 0, 1, 1, 0], [0, 1, 0, 0, 0, 1, 1], [0, 0, 1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 0, 1]]


def test_worked_example_decisions_differ() -> None:
    bits, post = bitwise_map(EVEN3, [1.0, 1.0, -0.5])
    assert bits == [0, 0, 1]
    assert tuple(bits) not in EVEN3
    assert block_map(EVEN3, [1.0, 1.0, -0.5]) == (0, 0, 0)
    # The tanh rule gives the same posterior LLRs for a single parity check.
    want3 = -0.5 + 2 * math.atanh(math.tanh(0.5) * math.tanh(0.5))
    want1 = 1.0 + 2 * math.atanh(math.tanh(0.5) * math.tanh(-0.25))
    assert abs(post[2] - want3) < 1e-12 and abs(post[0] - want1) < 1e-12
    assert abs(post[2] - (-0.0662)) < 1e-4 and abs(post[0] - 0.7727) < 1e-4


def test_hamming_bsc_table() -> None:
    code = linear_code(G74)
    r = exact_rates_bsc(code, 0.3)
    assert abs(r["map_ber"] - 0.3) < 1e-9
    assert abs(r["ml_ber"] - 0.32184) < 1e-9
    assert abs(r["ml_wer"] - 0.6705828) < 1e-9
    assert abs(r["map_wer"] - 0.9176457) < 1e-9
    r = exact_rates_bsc(code, 0.1)
    assert abs(r["map_ber"] - r["ml_ber"]) < 1e-12


def test_each_decoder_wins_its_own_criterion() -> None:
    rng = random.Random(21)
    for _ in range(40):
        n = rng.randrange(3, 7)
        k = rng.randrange(1, n)
        g = [[rng.randrange(2) for _ in range(n)] for _ in range(k)]
        code = sorted(set(linear_code(g)))
        if len(code) < 2:
            continue
        for p in (0.05, 0.2, 0.35):
            r = exact_rates_bsc(code, p)
            assert r["map_ber"] <= r["ml_ber"] + 1e-12
            assert r["ml_wer"] <= r["map_wer"] + 1e-12


def test_posterior_is_brute_force_on_random_inputs() -> None:
    rng = random.Random(5)
    code = linear_code(G74)
    for _ in range(500):
        llr = [rng.gauss(1.0, 2.0) for _ in range(7)]
        _, post = bitwise_map(code, llr)
        w = [math.exp(0.5 * sum((1 - 2 * b) * l for b, l in zip(c, llr))) for c in code]
        for i in range(7):
            p0 = sum(x for c, x in zip(code, w) if c[i] == 0)
            p1 = sum(x for c, x in zip(code, w) if c[i] == 1)
            assert abs(post[i] - math.log(p0 / p1)) < 1e-9


def test_awgn_monte_carlo() -> None:
    rng = random.Random(77)
    code = linear_code(G74)
    sigma = 1.0
    errs = {"map_b": 0, "ml_b": 0, "map_w": 0, "ml_w": 0}
    trials = 3000
    for _ in range(trials):
        c = code[rng.randrange(16)]
        llr = [2 * (1 - 2 * b + rng.gauss(0, sigma)) / sigma ** 2 for b in c]
        m, _ = bitwise_map(code, llr)
        d = block_map(code, llr)
        bm = sum(a != b for a, b in zip(m, c))
        bd = sum(a != b for a, b in zip(d, c))
        errs["map_b"] += bm
        errs["ml_b"] += bd
        errs["map_w"] += bm > 0
        errs["ml_w"] += bd > 0
    assert errs["map_b"] <= errs["ml_b"] * 1.02 + 5
    assert errs["ml_w"] <= errs["map_w"] * 1.02 + 5
