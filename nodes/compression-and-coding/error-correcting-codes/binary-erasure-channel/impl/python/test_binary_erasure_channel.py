# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/binary-erasure-channel/. The authors are listed in prov/6KVV6B.jsonl.

import itertools
import math
import random

from binary_erasure_channel import capacity, decode, encode, recoverable, transmit

HAMMING_7_4 = [
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 1, 0, 1],
]


def all_codewords(g):
    k = len(g)
    return [tuple(encode(g, m)) for m in itertools.product((0, 1), repeat=k)]


def test_erasure_rate() -> None:
    rng = random.Random(11)
    eps, n = 0.3, 100000
    y = transmit([1] * n, eps, rng)
    assert abs(y.count(None) / n - eps) < 0.01
    assert all(b in (None, 1) for b in y)  # bits are lost, never flipped
    assert capacity(0.3) == 0.7


def test_decode_exhaustive_on_hamming_code() -> None:
    g = HAMMING_7_4
    code = all_codewords(g)
    for m in itertools.product((0, 1), repeat=4):
        c = encode(g, m)
        for r in range(8):
            for erased in itertools.combinations(range(7), r):
                y = [None if j in erased else c[j] for j in range(7)]
                # brute force: the codewords that agree with y where it is not erased
                fits = [w for w in code if all(y[j] is None or y[j] == w[j] for j in range(7))]
                out = decode(g, y)
                if len(fits) == 1:
                    assert out == list(m)
                else:
                    assert out is None
                assert (len(fits) == 1) == recoverable(g, erased)


def test_recoverable_iff_no_codeword_inside_erasures() -> None:
    g = HAMMING_7_4
    supports = {frozenset(j for j in range(7) if w[j]) for w in all_codewords(g) if any(w)}
    count = {r: 0 for r in range(8)}
    for r in range(8):
        for erased in itertools.combinations(range(7), r):
            inside = any(s <= set(erased) for s in supports)
            assert recoverable(g, erased) == (not inside)
            count[r] += recoverable(g, erased)
    # all patterns of 0, 1, 2 erasures (d = 3), and 28 of the 35 patterns of 3 erasures
    assert [count[r] for r in range(4)] == [1, 7, 21, 28]
    assert count[4] == 0  # more erasures than n - k = 3 can never be filled


def test_repetition_fails_with_probability_eps_to_the_n() -> None:
    eps, n = 0.4, 3
    g = [[1] * n]
    fail = 0.0
    for pattern in itertools.product((0, 1), repeat=n):
        prob = math.prod(eps if e else 1 - eps for e in pattern)
        y = [None if e else 1 for e in pattern]
        if decode(g, y) is None:
            fail += prob
    assert math.isclose(fail, eps ** n)


def test_random_linear_codes_near_capacity() -> None:
    # a random k x n code fails on e erasures only if the kept n - e columns have rank < k,
    # which has probability at most 2^(k - (n - e)): a few spare kept positions are enough
    rng = random.Random(3)
    n, k = 60, 40
    fails = 0
    trials = 300
    for _ in range(trials):
        g = [[rng.randrange(2) for _ in range(n)] for _ in range(k)]
        erased = rng.sample(range(n), n - k - 8)  # keep k + 8 positions
        fails += not recoverable(g, erased)
    assert fails / trials <= 2 ** -8 * 4 + 0.02


def test_feedback_retransmission_reaches_capacity() -> None:
    # with feedback, resending each erased bit gives 1 / (1 - eps) uses per bit on average
    rng = random.Random(8)
    eps, bits = 0.25, 40000
    uses = 0
    for _ in range(bits):
        while True:
            uses += 1
            if rng.random() >= eps:
                break
    assert abs(bits / uses - capacity(eps)) < 0.01
