# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/language-model-watermarking/. The authors are listed in prov/635TD2.jsonl.

"""Tests of the green list watermark on a seeded toy bigram model over integer tokens."""

import math
import random

import mlkit
from language_model_watermarking import (
    detect,
    draw,
    false_positive_bound,
    generate,
    green_count,
    green_list,
    green_probability,
    green_size,
    spike_entropy,
    toy_bigram_model,
    z_score,
)

V = 64
GAMMA = 0.25
KEY = b"test-key-1"


def test_green_list_is_deterministic_and_has_the_right_size():
    for prev in range(V):
        g = green_list(KEY, prev, GAMMA, V)
        assert len(g) == 16
        assert g == green_list(KEY, prev, GAMMA, V)
        assert all(0 <= v < V for v in g)
    assert green_list(KEY, 3, GAMMA, V) != green_list(b"other-key", 3, GAMMA, V)
    assert green_size(10, 0.25) == 2 and green_size(4, 0.0) == 1 and green_size(4, 1.0) == 3


def test_each_token_is_green_for_about_gamma_of_the_contexts():
    hits = [0] * V
    for prev in range(V):
        for v in green_list(KEY, prev, GAMMA, V):
            hits[v] += 1
    assert sum(hits) == 16 * V
    keys = [bytes([i]) for i in range(200)]
    frac = sum(1 for k in keys if 5 in green_list(k, 7, GAMMA, V)) / len(keys)
    assert abs(frac - 0.25) < 0.1


def test_z_score_values():
    assert z_score(25, 100, 0.25) == 0.0
    assert abs(z_score(50, 100, 0.25) - 25 / math.sqrt(18.75)) < 1e-12
    assert abs(z_score(50, 100, 0.25) - 5.773502691896258) < 1e-12
    assert z_score(0, 0, 0.25) == 0.0


def test_watermarked_text_is_detected():
    rng = random.Random(2023)
    model = toy_bigram_model(rng, V, 1.0)
    for _ in range(8):
        text = generate(model, 0, 200, GAMMA, 2.0, KEY, rng)
        z, flagged = detect([0] + text, GAMMA, KEY, V, 4.0)
        assert flagged and z > 6.0


def test_plain_text_and_a_wrong_key_are_not_flagged():
    rng = random.Random(7)
    model = toy_bigram_model(rng, V, 1.0)
    flagged = 0
    for _ in range(40):
        plain = generate(model, 0, 150, GAMMA, 0.0, KEY, rng)
        flagged += detect([0] + plain, GAMMA, KEY, V, 4.0)[1]
        marked = generate(model, 0, 150, GAMMA, 2.0, KEY, rng)
        flagged += detect([0] + marked, GAMMA, b"wrong-key", V, 4.0)[1]
    assert flagged == 0


def test_false_positive_rate_over_random_keys_is_below_the_bound():
    # The theorem: for a text that does not depend on the key, P(z > z*) <= exp(-2 z*^2 gamma (1 - gamma)).
    rng = random.Random(99)
    model = toy_bigram_model(rng, V, 1.0)
    text = [0] + generate(model, 0, 60, GAMMA, 0.0, b"unused", rng)
    for threshold in (1.0, 2.0):
        bound = false_positive_bound(threshold, 0.25)
        hits = sum(1 for i in range(600) if detect(text, GAMMA, b"k%d" % i, V, threshold)[1])
        assert hits / 600 <= bound
    assert abs(false_positive_bound(4.0, 0.25) - math.exp(-6.0)) < 1e-15


def test_repeated_pairs_are_scored_once():
    text = [1, 2, 1, 2, 1, 2, 1, 2, 1]
    count, scored = green_count(text, GAMMA, KEY, V)
    assert scored == 2
    assert count == (2 in green_list(KEY, 1, GAMMA, V)) + (1 in green_list(KEY, 2, GAMMA, V))


def test_the_bonus_never_lowers_the_green_mass():
    rng = random.Random(3)
    for _ in range(200):
        probs = mlkit.softmax([rng.gauss(0, 2) for _ in range(V)])
        green = green_list(KEY, rng.randrange(V), GAMMA, V)
        delta = rng.uniform(0.0, 5.0)
        q, q2 = green_probability(probs, green, delta)
        assert q2 >= q - 1e-15
        z = [math.log(p) + (delta if v in green else 0.0) for v, p in enumerate(probs)]
        assert abs(math.fsum(mlkit.softmax(z)[v] for v in green) - q2) < 1e-12


def test_low_entropy_text_carries_a_weak_watermark():
    rng = random.Random(5)
    peaked = toy_bigram_model(rng, V, 12.0)
    flat = toy_bigram_model(rng, V, 1.0)
    zs = {}
    for name, model in (("peaked", peaked), ("flat", flat)):
        text = generate(model, 0, 200, GAMMA, 2.0, KEY, rng)
        zs[name] = detect([0] + text, GAMMA, KEY, V, 4.0)[0]
    assert zs["peaked"] < zs["flat"]
    assert spike_entropy(mlkit.softmax(peaked[0]), GAMMA, 2.0) < spike_entropy(mlkit.softmax(flat[0]), GAMMA, 2.0)


def test_expected_green_count_meets_the_spike_entropy_bound():
    # Theorem 4.2 of Kirchenbauer et al. for one step, averaged exactly over 300 random green lists.
    rng = random.Random(11)
    delta = 2.0
    a = math.exp(delta)
    for _ in range(5):
        probs = mlkit.softmax([rng.gauss(0, 1.5) for _ in range(V)])
        mean = sum(green_probability(probs, green_list(b"s%d" % i, 0, GAMMA, V), delta)[1] for i in range(300)) / 300
        bound = GAMMA * a / (1 + (a - 1) * GAMMA) * spike_entropy(probs, GAMMA, delta)
        assert mean >= bound - 0.03


def test_one_edit_changes_at_most_two_scores():
    rng = random.Random(13)
    model = toy_bigram_model(rng, V, 1.0)
    text = [0] + generate(model, 0, 200, GAMMA, 2.0, KEY, rng)
    count, _ = green_count(text, GAMMA, KEY, V)
    edited = list(text)
    positions = rng.sample(range(1, len(text)), 20)
    for p in positions:
        edited[p] = rng.randrange(V)
    count2, _ = green_count(edited, GAMMA, KEY, V)
    # An edit at position p changes only the pairs at p and p + 1, so the set of distinct green pairs loses at most 2.
    assert count - count2 <= 2 * len(positions)
    assert detect(edited, GAMMA, KEY, V, 4.0)[1]


def test_draw_follows_the_distribution():
    rng = random.Random(1)
    probs = [0.1, 0.6, 0.3]
    counts = [0, 0, 0]
    for _ in range(3000):
        counts[draw(probs, rng)] += 1
    assert all(abs(c / 3000 - p) < 0.04 for c, p in zip(counts, probs))
