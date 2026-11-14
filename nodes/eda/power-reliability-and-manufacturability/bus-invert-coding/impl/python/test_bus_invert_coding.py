# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bus-invert-coding/. The authors are listed in prov/7HE5BF.jsonl.

import itertools
import random
from fractions import Fraction
from math import comb

from bus_invert_coding import decode, encode, encode_data_only, popcount, toggles


def test_decode_inverts_encode():
    rng = random.Random(1)
    for n in range(1, 9):
        words = [rng.randrange(1 << n) for _ in range(50)]
        states = encode(words, n)
        assert [decode(b, i, n) for b, i in states] == words


def test_each_transfer_takes_the_cheaper_codeword_exhaustive():
    # every state (bus, inv) and every word, for n <= 6
    for n in range(1, 7):
        mask = (1 << n) - 1
        for bus, inv, d in itertools.product(range(1 << n), (0, 1), range(1 << n)):
            (s,) = encode([d], n, bus, inv)
            cost = toggles([s], (bus, inv))[0]
            plain = popcount(bus ^ d) + inv
            inverted = popcount(bus ^ d ^ mask) + (1 - inv)
            assert plain + inverted == n + 1
            assert cost == min(plain, inverted)
            assert cost <= (n + 1) // 2  # = ceil(n / 2)


def test_bound_is_reached():
    for n in range(1, 9):
        worst = max(
            toggles(encode([d], n, bus, inv), (bus, inv))[0]
            for bus in range(1 << n)
            for inv in (0, 1)
            for d in range(1 << n)
        )
        assert worst == (n + 1) // 2


def test_data_only_rule_can_toggle_one_more_line():
    for n in range(2, 7):
        worst = max(
            toggles(encode_data_only([d], n, bus, inv), (bus, inv))[0]
            for bus in range(1 << n)
            for inv in (0, 1)
            for d in range(1 << n)
        )
        assert worst == n // 2 + 1


def test_greedy_is_optimal_over_whole_sequences():
    # Against all 2^T choices of the INV bits for the same word sequence.
    rng = random.Random(2)
    for _ in range(60):
        n = rng.randint(1, 6)
        t = rng.randint(1, 7)
        mask = (1 << n) - 1
        words = [rng.randrange(1 << n) for _ in range(t)]
        best = min(
            sum(toggles([(d ^ mask if x else d, x) for d, x in zip(words, xs)]))
            for xs in itertools.product((0, 1), repeat=t)
        )
        assert sum(toggles(encode(words, n))) == best


def expected_toggles(n):
    """E[min(B, n + 1 - B)] with B binomial(n, 1/2), in fractions."""
    return sum(Fraction(comb(n, b), 2**n) * min(b, n + 1 - b) for b in range(n + 1))


def test_expected_toggles_on_uniform_data_exhaustive():
    # Average over all states and all words equals the binomial formula.
    for n in range(1, 7):
        tot = Fraction(0)
        for bus, inv, d in itertools.product(range(1 << n), (0, 1), range(1 << n)):
            tot += toggles(encode([d], n, bus, inv), (bus, inv))[0]
        assert tot / (2 * 4**n) == expected_toggles(n)


def test_page_numbers():
    assert expected_toggles(8) == Fraction(837, 256)
    trace = encode([0b11111110, 0b11110000, 0b00001111, 0b00001110], 8)
    assert trace == [(0b00000001, 1), (0b00001111, 1), (0b00001111, 0), (0b00001110, 0)]
    assert toggles(trace) == [2, 3, 1, 1]
