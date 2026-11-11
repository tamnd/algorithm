# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cut-and-choose/. The authors are listed in prov/QC3Y6Z.jsonl.
# There are no official test vectors for cut-and-choose. The tests compare
# the exact escape probabilities of a cheating garbler with Monte Carlo runs
# of the template on local simulated parties, and check the selective
# failure attack and its fix.

import random
from fractions import Fraction
from math import comb, sqrt

from cut_and_choose import (
    CAUGHT,
    CORRECT,
    WRONG,
    abort_probability,
    any_good_ok,
    best_majority,
    cut_and_choose,
    escape_lindell13,
    escape_majority,
    majority_ok,
    min_circuits,
    monte_carlo,
    selective_failure_run,
)

S = 10


def close(observed: float, p: float, trials: int) -> bool:
    """Within 5 standard deviations (plus a little for p near 0)."""
    return abs(observed - p) <= 5 * sqrt(p * (1 - p) / trials) + 1e-4


def test_template_outcomes() -> None:
    good = [True, False, True, True]
    assert cut_and_choose(good, lambda s: {1}, majority_ok) == CAUGHT
    assert cut_and_choose(good, lambda s: {0}, majority_ok) == CORRECT      # 1 bad of 3
    assert cut_and_choose(good, lambda s: {0, 2}, majority_ok) == CORRECT   # tie: 1 bad of 2
    assert cut_and_choose(good, lambda s: {0, 2, 3}, majority_ok) == WRONG  # 1 bad of 1
    assert cut_and_choose(good, lambda s: {0, 2, 3}, any_good_ok) == WRONG
    assert cut_and_choose(good, lambda s: {0, 2}, any_good_ok) == CORRECT


def test_majority_formula_small_case() -> None:
    # s = 10, check 5, evaluate 5: the garbler needs k = 3, 4 or 5 bad ones,
    # all among the 5 evaluated.
    assert escape_majority(S, 5, 2) == 0
    assert escape_majority(S, 5, 3) == Fraction(comb(7, 5), comb(10, 5)) == Fraction(1, 12)
    assert escape_majority(S, 5, 6) == 0
    assert best_majority(S, 5) == (3, Fraction(1, 12))


def test_majority_formula_against_monte_carlo() -> None:
    rng = random.Random(2007)
    trials = 10_000
    for c, k in ((5, 3), (5, 4), (6, 3), (4, 4)):
        p = float(escape_majority(S, c, k))
        assert close(monte_carlo(S, k, "majority", trials, rng, c=c), p, trials), (c, k)


def test_lindell13_formula_against_monte_carlo() -> None:
    rng = random.Random(2013)
    trials = 20_000
    for k in (1, 5, 10):
        p = float(escape_lindell13(S, k))
        assert p == 2.0 ** -S
        assert close(monte_carlo(S, k, "lindell13", trials, rng), p, trials), k
    # Biased checking: probability q of checking each circuit.
    q = Fraction(3, 4)
    p = float(escape_lindell13(S, 2, q))
    assert p == 0.75 ** 8 * 0.25 ** 2
    assert close(monte_carlo(S, 2, "lindell13", trials, rng, q=0.75), p, trials)


def test_number_of_circuits_for_2_to_the_minus_40() -> None:
    assert min_circuits(40, "lindell13") == 40
    s = min_circuits(40, "majority", Fraction(3, 5))
    assert 110 <= s <= 130          # about 3 times as many with the majority rule
    k, p = best_majority(40, 24)
    assert p > Fraction(1, 2 ** 15)  # 40 circuits with majority give only about 2^-14.5


def test_selective_failure_without_encoding_reveals_the_bit() -> None:
    # One OT per input bit: a bad key for value 1 aborts exactly when y = 1.
    assert abort_probability(0, {0}, 1) == 0
    assert abort_probability(1, {0}, 1) == 1


def test_selective_failure_with_xor_encoding() -> None:
    s = 6
    # Corrupting fewer than s encoded wires: the abort probability does not
    # depend on y, so an abort says nothing about the input.
    for corrupted in ({0}, {1, 3}, {0, 1, 2, 3, 4}):
        assert abort_probability(0, corrupted, s) == abort_probability(1, corrupted, s)
        assert abort_probability(0, corrupted, s) == 1 - Fraction(1, 2 ** len(corrupted))
    # Corrupting all s: no abort means y = 0, but that happens with
    # probability only 2^-(s-1).
    everything = set(range(s))
    assert abort_probability(1, everything, s) == 1
    assert abort_probability(0, everything, s) == 1 - Fraction(1, 2 ** (s - 1))
    rng = random.Random(5)
    trials = 20_000
    for y in (0, 1):
        rate = sum(selective_failure_run(y, {1, 3}, s, rng) for _ in range(trials)) / trials
        assert close(rate, 0.75, trials)
