# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gilbert-varshamov-bound/. The authors are listed in prov/12WDFJ.jsonl.

import random
from itertools import product
from math import log2

from gilbert_varshamov_bound import (
    distance, gilbert_bound, gilbert_greedy, gv_rate, min_distance_linear, null_space,
    random_parity_check_distance, span, varshamov_dimension, varshamov_parity_check, volume,
)

# A_2(n, d) from A. E. Brouwer, Table of general binary codes, https://aeb.win.tue.nl/codes/binary-1.html
BROUWER = {(7, 3): 16, (10, 3): 72, (12, 4): 144, (15, 5): 256, (16, 6): 256, (23, 7): 4096}


def test_values_table() -> None:
    # (n, d): (Gilbert, Varshamov 2^k, binary lexicode size)
    table = {(7, 3): (5, 16, 16), (10, 3): (19, 64, 64), (12, 4): (14, 32, 128),
             (15, 5): (17, 64, 128), (16, 6): (10, 32, 128), (23, 7): (58, 128, None)}
    for (n, d), (g, v, lex) in table.items():
        assert gilbert_bound(2, n, d) == g
        assert 2 ** varshamov_dimension(2, n, d) == v
        assert g <= v <= BROUWER[(n, d)]
        if lex is not None and n <= 12:
            assert len(gilbert_greedy(2, n, d)) == lex


def test_gilbert_greedy_is_maximal_and_large() -> None:
    rng = random.Random(1952)
    for q, n, d in ((2, 8, 3), (2, 9, 4), (3, 5, 3), (3, 6, 4), (4, 4, 3)):
        allw = list(product(range(q), repeat=n))
        for order in (allw, rng.sample(allw, len(allw))):
            code = gilbert_greedy(q, n, d, order)
            assert all(distance(x, y) >= d for i, x in enumerate(code) for y in code[i + 1:])
            # every word is within d - 1 of the code (the covering step of the proof)
            assert all(any(distance(w, c) < d for c in code) for w in allw)
            assert len(code) * volume(q, n, d - 1) >= q ** n
            assert len(code) >= gilbert_bound(q, n, d)


def test_binary_lexicodes_are_linear() -> None:
    for n in range(4, 11):
        for d in (3, 4, 5):
            code = set(gilbert_greedy(2, n, d))
            for x in code:
                for y in code:
                    assert tuple(a ^ b for a, b in zip(x, y)) in code


def test_varshamov_construction() -> None:
    rng = random.Random(1957)
    cases = [(2, 7, 3), (2, 15, 3), (2, 15, 5), (2, 12, 4), (2, 16, 6), (3, 8, 3), (3, 7, 4), (5, 6, 3)]
    for q, n, d in cases:
        k = varshamov_dimension(q, n, d)
        assert volume(q, n - 1, d - 2) < q ** (n - k)
        for gen_rng in (None, rng):
            cols = varshamov_parity_check(q, n, k, d, gen_rng)
            basis = null_space(cols, q)
            assert len(basis) >= k
            assert min_distance_linear(span(basis, q)) >= d
    # with d = 3 the construction picks all nonzero columns up to scaling: a Hamming code
    cols = varshamov_parity_check(2, 15, 11, 3)
    assert sorted(cols) == sorted(set(cols)) and len(cols) == 15


def test_random_linear_codes() -> None:
    # A nonzero word lies in the kernel of a random r x n matrix with probability 2^-r, so
    # P(d < D) <= (V_2(n, D - 1) - 1) / 2^r. With n = 10, r = 7, D = 3 this is 55/128.
    rng = random.Random(2024)
    trials = 300
    good = sum(random_parity_check_distance(10, 3, rng) >= 3 for _ in range(trials))
    assert good / trials >= 1 - 55 / 128 - 0.05


def test_asymptotic() -> None:
    assert abs(gv_rate(0.11) - 0.5) < 0.001
    assert gv_rate(0.5) == 0.0
    for delta in (0.1, 0.2, 0.3):
        n = 2000
        d = int(delta * n)
        r = log2(gilbert_bound(2, n, d)) / n
        assert abs(r - gv_rate(d / n)) < 0.01
        k = varshamov_dimension(2, n, d)
        assert abs(k / n - gv_rate(d / n)) < 0.01
