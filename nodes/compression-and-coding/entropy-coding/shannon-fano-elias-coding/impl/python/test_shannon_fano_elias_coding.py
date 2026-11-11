# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shannon-fano-elias-coding/. The authors are listed in prov/C2GA8M.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from shannon_fano_elias_coding import (
    first_bits,
    is_prefix_free,
    sfe_block_decode,
    sfe_block_encode,
    sfe_code,
)


def entropy(probs) -> float:
    return -sum(float(p) * math.log2(p) for p in probs)


def random_probs(rng: random.Random, n: int) -> list[Fraction]:
    w = [rng.randint(1, 50) for _ in range(n)]
    t = sum(w)
    return [Fraction(x, t) for x in w]


def test_worked_example() -> None:
    p = [Fraction(3, 10), Fraction(1, 10), Fraction(4, 10), Fraction(2, 10)]
    words = sfe_code(p)
    assert words == ["001", "01011", "100", "1110"]
    assert sum(q * len(c) for q, c in zip(p, words)) == Fraction(34, 10)


def test_prefix_free_and_bound_l_below_h_plus_2() -> None:
    rng = random.Random(7)
    for _ in range(500):
        p = random_probs(rng, rng.randint(1, 16))
        words = sfe_code(p)
        assert is_prefix_free(words)
        lengths = [len(c) for c in words]
        for q, l in zip(p, lengths):
            # l = ceil(log2(1/q)) + 1 means 2^-(l-1) <= q < 2^-(l-2).
            assert Fraction(1, 2 ** (l - 1)) <= q < Fraction(4, 2**l)
        mean = sum(float(q) * l for q, l in zip(p, lengths))
        h = entropy(p)
        assert h + 1 - 1e-12 <= mean < h + 2


def test_order_is_kept() -> None:
    # The intervals follow the symbol order, so the codewords do too.
    rng = random.Random(11)
    for _ in range(200):
        words = sfe_code(random_probs(rng, rng.randint(2, 12)))
        assert words == sorted(words)


def test_no_sorting_needed_but_unsorted_shannon_code_fails() -> None:
    # Without the extra bit, the first bits of the interval starts can collide
    # when the symbols are not sorted: 1/4 then 1/2 gives 00 and 0 (from 1/4 = 0.01).
    p = [Fraction(1, 4), Fraction(1, 2), Fraction(1, 4)]
    words = sfe_code(p)
    assert is_prefix_free(words)
    starts = [Fraction(0), Fraction(1, 4), Fraction(3, 4)]
    shannon_lengths = [2, 1, 2]
    naive = [first_bits(s, l) for s, l in zip(starts, shannon_lengths)]
    assert not is_prefix_free(naive)


def test_blocks_round_trip_and_rate_tends_to_entropy() -> None:
    p = [Fraction(7, 10), Fraction(2, 10), Fraction(1, 10)]
    h = entropy(p)
    rates = []
    for k in range(1, 6):
        words = {}
        mean = Fraction(0)
        for block in itertools.product(range(3), repeat=k):
            w = sfe_block_encode(p, block)
            words[block] = w
            prob = math.prod(p[s] for s in block)
            mean += prob * len(w)
            assert sfe_block_decode(p, w, k) == list(block)
        assert is_prefix_free(list(words.values()))
        rate = float(mean) / k
        assert h <= rate < h + 2 / k
        rates.append(rate)
    assert rates[-1] < rates[0]


def test_bad_input() -> None:
    with pytest.raises(ValueError):
        sfe_code([Fraction(1, 2), Fraction(1, 3)])
    assert sfe_code([Fraction(1)]) == ["1"]
