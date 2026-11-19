# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-bayes-risk-decoding/. The authors are listed in prov/FTCX13.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

from minimum_bayes_risk_decoding import (
    expected_losses,
    mbr_decode,
    mbr_from_log_probs,
    mbr_from_samples,
    word_edit_distance,
    zero_one_loss,
)

A, B, C, D = ("a", "b", "c"), ("a", "b", "d"), ("a", "e", "d"), ("f", "b", "d")
DIST = [(A, Fraction(7, 25)), (B, Fraction(6, 25)), (C, Fraction(6, 25)), (D, Fraction(6, 25))]


def brute_edit(a, b):
    if not a:
        return len(b)
    if not b:
        return len(a)
    return min(brute_edit(a[1:], b) + 1, brute_edit(a, b[1:]) + 1, brute_edit(a[1:], b[1:]) + (a[0] != b[0]))


def test_example() -> None:
    assert sum(w for _, w in DIST) == 1
    risks = expected_losses([A, B, C, D], DIST, word_edit_distance)
    assert risks == [Fraction(6, 5), Fraction(19, 25), Fraction(32, 25), Fraction(32, 25)]
    assert mbr_decode([A, B, C, D], DIST, word_edit_distance) == (B, Fraction(19, 25))
    # The mode is A, and 0-1 loss picks the mode.
    assert max(DIST, key=lambda t: t[1])[0] == A
    assert mbr_decode([A, B, C, D], DIST, zero_one_loss) == (A, Fraction(18, 25))


def test_edit_distance_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        a = tuple(rng.choice("abc") for _ in range(rng.randrange(6)))
        b = tuple(rng.choice("abc") for _ in range(rng.randrange(6)))
        assert word_edit_distance(a, b) == brute_edit(a, b)
    assert word_edit_distance(["the", "cat", "sat"], ["the", "cat", "sat", "down"]) == 1


def test_zero_one_loss_gives_the_map_output() -> None:
    rng = random.Random(2)
    for _ in range(200):
        ys = [tuple(rng.choice("ab") for _ in range(3)) for _ in range(6)]
        ys = list(dict.fromkeys(ys))
        ws = [Fraction(rng.randrange(1, 20)) for _ in ys]
        dist = [(y, w / sum(ws)) for y, w in zip(ys, ws)]
        got, _ = mbr_decode(ys, dist, zero_one_loss)
        assert dict(dist)[got] == max(w for _, w in dist)


def test_samples_with_zero_one_loss_give_the_most_frequent_sample() -> None:
    rng = random.Random(3)
    for _ in range(200):
        samples = [rng.choice(["x", "y", "z", "w"]) for _ in range(rng.randrange(1, 15))]
        got, risk = mbr_from_samples(samples, zero_one_loss)
        counts = Counter(samples)
        assert counts[got] == max(counts.values())
        assert math.isclose(risk, 1 - counts[got] / len(samples))


def test_number_of_loss_calls() -> None:
    calls = [0]

    def counted(a, b):
        calls[0] += 1
        return word_edit_distance(a, b)

    rng = random.Random(4)
    samples = [rng.choice([A, B, C, D]) for _ in range(30)]
    mbr_from_samples(samples, counted)
    assert calls[0] == 30 * len(set(samples))
    assert calls[0] <= 30 * 30


def test_sampled_mbr_finds_the_exact_choice() -> None:
    rng = random.Random(5)
    ys = [y for y, _ in DIST]
    ws = [float(w) for _, w in DIST]
    samples = rng.choices(ys, weights=ws, k=2000)
    got, risk = mbr_from_samples(samples, word_edit_distance)
    assert got == B
    assert abs(risk - 19 / 25) < 0.05


def test_scaling_and_log_space_weights() -> None:
    scaled = [(y, w * 1000) for y, w in DIST]
    assert mbr_decode([A, B, C, D], scaled, word_edit_distance)[0] == B
    # Log probabilities near -1000 underflow to 0 in exp, but the choice is the same.
    logs = [(y, -1000.0 + math.log(float(w))) for y, w in DIST]
    assert all(math.exp(v) == 0.0 for _, v in logs)
    got, risk = mbr_from_log_probs([A, B, C, D], logs, word_edit_distance)
    assert got == B and math.isclose(risk, 19 / 25)


def test_ties_keep_the_first_candidate() -> None:
    dist = [(C, Fraction(1, 2)), (D, Fraction(1, 2))]
    assert mbr_decode([C, D], dist, word_edit_distance)[0] == C
    assert mbr_decode([D, C], dist, word_edit_distance)[0] == D
