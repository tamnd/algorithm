# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-password-model/. The authors are listed in prov/Q34M2V.jsonl.

import itertools
import math
import random
from fractions import Fraction

import pytest

from markov_password_model import (
    END,
    START,
    estimate_guess_number,
    guess_number,
    next_prob,
    probability,
    sample_probabilities,
    strength_bits,
    train,
)

# The training lists are made up in the test from a seeded generator. No real
# password list is used.


def made_up_list(rng: random.Random, alphabet: str, size: int, max_len: int) -> list:
    return ["".join(rng.choice(alphabet) for _ in range(rng.randint(1, max_len))) for _ in range(size)]


def oracle_probability(passwords: list, k: int, alphabet: str, delta: Fraction, w: str) -> Fraction:
    """Count each transition again by a scan of the padded strings."""
    padded = [START * k + x + END for x in passwords]
    sigma = len(set(alphabet)) + 1
    target = START * k + w + END
    p = Fraction(1)
    for i in range(k, len(target)):
        ctx, a = target[i - k : i], target[i]
        c_ctx = sum(1 for x in padded for j in range(k, len(x)) if x[j - k : j] == ctx)
        c_pair = sum(1 for x in padded for j in range(k, len(x)) if x[j - k : j] == ctx and x[j] == a)
        den = c_ctx + delta * sigma
        p *= Fraction(0) if den == 0 else (c_pair + delta) / den
    return p


PAGE_LIST = ["ab1", "ab11", "abab", "b1", "ba1", "a1", "ab", "bb1"]


def test_page_example() -> None:
    m = train(PAGE_LIST, 1, "ab1", Fraction(1))
    assert m.totals == {START: 8, "1": 7, "a": 7, "b": 9}
    assert probability(m, "ab1") == Fraction(1, 2) * Fraction(6, 11) * Fraction(5, 13) * Fraction(7, 11)
    assert probability(m, "ab1") == Fraction(105, 1573)
    assert round(strength_bits(m, "ab1"), 2) == 3.91
    assert probability(m, "1b") == Fraction(1, 12) * Fraction(1, 11) * Fraction(3, 13)
    assert round(strength_bits(m, "1b"), 2) == 9.16
    assert [guess_number(m, w, 12) for w in ["ab1", "ba", "1b", "b1a"]] == [5, 24, 50, 80]


def test_against_recount() -> None:
    rng = random.Random(2012)
    checked = 0
    for _ in range(120):
        alphabet = rng.choice(["ab", "ab1", "a1!"])
        passwords = made_up_list(rng, alphabet, rng.randint(1, 8), 5)
        k = rng.randint(0, 3)
        delta = rng.choice([Fraction(0), Fraction(1, 10), Fraction(1, 2), Fraction(1)])
        m = train(passwords, k, alphabet, delta)
        for _ in range(5):
            w = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
            assert probability(m, w) == oracle_probability(passwords, k, alphabet, delta, w)
            checked += 1
    assert checked == 600


def test_probabilities_sum_to_one() -> None:
    """With delta > 0 the strings of length at most L and the prefixes of
    length L + 1 carry all the mass, exactly."""
    rng = random.Random(5)
    for _ in range(12):
        alphabet = rng.choice(["ab", "a1"])
        passwords = made_up_list(rng, alphabet, rng.randint(1, 6), 4)
        k = rng.randint(0, 2)
        m = train(passwords, k, alphabet, rng.choice([Fraction(1, 3), Fraction(1)]))
        L = 4
        total = sum(
            (probability(m, "".join(t)) for n in range(L + 1) for t in itertools.product(m.alphabet, repeat=n)),
            Fraction(0),
        )
        # mass of the prefixes of length L + 1 = P(prefix without the end symbol)
        no_end = Fraction(0)
        for t in itertools.product(m.alphabet, repeat=L + 1):
            w = "".join(t)
            p_with_end = probability(m, w)
            ctx = (START * k + w)[len(START * k + w) - k :] if k else ""
            no_end += p_with_end / next_prob(m, ctx, END)
        assert total + no_end == 1


def test_guess_number_against_enumeration() -> None:
    rng = random.Random(77)
    checked = 0
    for _ in range(60):
        alphabet = "ab"
        passwords = made_up_list(rng, alphabet, rng.randint(2, 6), 4)
        m = train(passwords, rng.randint(0, 2), alphabet, Fraction(1))
        max_len = 6
        all_strings = ["".join(t) for n in range(max_len + 1) for t in itertools.product("ab", repeat=n)]
        probs = {s: probability(m, s) for s in all_strings}
        for _ in range(4):
            w = rng.choice(all_strings[:31])  # length at most 4
            expected = 1 + sum(1 for s in all_strings if probs[s] > probs[w])
            assert guess_number(m, w, max_len) == expected
            checked += 1
    assert checked == 240


def test_ties_and_order() -> None:
    m = train(["ab", "ba"], 0, "ab", Fraction(0))
    # order 0 with these counts: P(a) = P(b) = P(END) = 1/3
    assert probability(m, "ab") == probability(m, "ba") == Fraction(1, 27)
    assert guess_number(m, "ab", 4) == 1 + 1 + 2  # the empty string and "a", "b"
    assert probability(m, "") == Fraction(1, 3)


def test_unseen_with_no_smoothing() -> None:
    m = train(["aa"], 1, "ab", Fraction(0))
    assert probability(m, "ab") == 0
    assert strength_bits(m, "ab") == math.inf
    with pytest.raises(ValueError):
        probability(m, "ac")
    with pytest.raises(ValueError):
        train(["a\x03"], 1, "a\x03")


def test_monte_carlo_estimate() -> None:
    """The estimate of Dell'Amico and Filippone is close to the exact count."""
    rng = random.Random(2015)
    m = train(made_up_list(random.Random(9), "ab1", 20, 4), 1, "ab1", Fraction(1, 2))
    samples = sample_probabilities(m, rng, 4000, 12)
    for w in ["ab", "a1b", "bb11", "1a1a1"]:
        exact = guess_number(m, w, 12)
        est = estimate_guess_number(probability(m, w), samples)
        assert abs(est - exact) <= 0.2 * exact, (w, est, exact)
