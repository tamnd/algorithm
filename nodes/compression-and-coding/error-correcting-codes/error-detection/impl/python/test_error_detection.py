# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/error-detection/. The authors are listed in prov/CXD68V.jsonl.

import itertools
import math
import random

from error_detection import (
    codewords, even_parity_rows, passes_check, simulate_arq, throughput_go_back_n,
    throughput_selective_repeat, throughput_stop_and_wait, undetected_by_enumeration,
    undetected_error_probability, weight_distribution,
)


def bits(s: str) -> int:
    return sum(1 << i for i, ch in enumerate(s) if ch == "1")


HAMMING_7_4 = [bits("1000110"), bits("0100011"), bits("0010111"), bits("0001101")]


def test_hamming_example() -> None:
    a = weight_distribution(HAMMING_7_4, 7)
    assert a == [1, 0, 0, 7, 7, 0, 0, 1]
    p = 0.01
    pud = undetected_error_probability(a, p)
    assert math.isclose(pud, undetected_by_enumeration(HAMMING_7_4, 7, p))
    assert abs(pud - 6.79e-6) < 1e-8
    # at p = 1/2 every nonzero pattern is equally likely: (2^k - 1) / 2^n
    assert math.isclose(undetected_error_probability(a, 0.5), 15 / 128)


def test_formula_equals_enumeration_on_random_codes() -> None:
    rng = random.Random(4)
    for _ in range(40):
        n = rng.randrange(3, 10)
        k = rng.randrange(1, n)
        rows = [(1 << i) | (rng.getrandbits(n - k) << k) for i in range(k)]
        a = weight_distribution(rows, n)
        for p in (0.01, 0.2, 0.5):
            assert math.isclose(undetected_error_probability(a, p), undetected_by_enumeration(rows, n, p),
                                rel_tol=1e-9, abs_tol=1e-15)


def test_detects_every_pattern_below_d() -> None:
    code = set(codewords(HAMMING_7_4))
    for c in code:
        for w in (1, 2):
            for pos in itertools.combinations(range(7), w):
                e = sum(1 << i for i in pos)
                assert not passes_check(code, c ^ e)
    # a linear code misses exactly the 2^k - 1 nonzero codewords as error patterns
    c = next(iter(code))
    missed = sum(1 for e in range(1, 128) if passes_check(code, c ^ e))
    assert missed == 15


def test_parity_detects_odd_weights() -> None:
    k = 7
    code = set(codewords(even_parity_rows(k)))
    assert len(code) == 2 ** k and all(c.bit_count() % 2 == 0 for c in code)
    for e in range(1, 1 << (k + 1)):
        assert passes_check(code, e) == (e.bit_count() % 2 == 0)


def test_monte_carlo_undetected() -> None:
    rng = random.Random(10)
    code = set(codewords(HAMMING_7_4))
    p, trials = 0.3, 100000
    sent = bits("1000110")
    missed = 0
    for _ in range(trials):
        e = 0
        for i in range(7):
            if rng.random() < p:
                e |= 1 << i
        if e and passes_check(code, sent ^ e):
            missed += 1
    exact = undetected_error_probability(weight_distribution(HAMMING_7_4, 7), p)
    assert abs(missed / trials - exact) < 4 * math.sqrt(exact / trials)


def test_arq_formulas_against_simulation() -> None:
    n, k, P = 1000, 968, 0.095
    blocks = 20000
    sr = simulate_arq("selective-repeat", P, blocks, n=n, seed=1)
    assert abs(k / sr - throughput_selective_repeat(P, k, n)) < 0.01
    gbn = simulate_arq("go-back-n", P, blocks, window=8, n=n, seed=2)
    assert abs(k / gbn - throughput_go_back_n(P, 8, k, n)) < 0.01
    sw = simulate_arq("stop-and-wait", P, blocks, idle_bits=7000, n=n, seed=3)
    assert abs(k / sw - throughput_stop_and_wait(P, 7000, k, n)) < 0.005
    # the order of the three schemes
    assert throughput_selective_repeat(P, k, n) > throughput_go_back_n(P, 8, k, n) > throughput_stop_and_wait(P, 7000, k, n)
    # with N = 1 go-back-N is selective repeat
    assert math.isclose(throughput_go_back_n(P, 1, k, n), throughput_selective_repeat(P, k, n))
