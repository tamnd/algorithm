# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/length-normalization/. The authors are listed in prov/AP6ENR.jsonl.

import math
import random

from length_normalization import (
    EOS,
    beam_search_normalized,
    gnmt_coverage,
    gnmt_penalty,
    normalized,
    power_penalty,
    rerank,
    word_reward,
)
from nlslog import NEG_INF, log_normalize

SHORT = (["x", "y", EOS], -2.0)
LONG = (["x", "y", "z", "x", "y", "z", "w", EOS], -3.2)


def random_model(seed, vocab, n):
    def model(prefix):
        if len(prefix) >= n - 1:
            return {w: (0.0 if w == EOS else NEG_INF) for w in vocab}
        rng = random.Random(f"{seed}|{' '.join(prefix)}")
        raw = [math.log(rng.random() ** 2 + 1e-3) for _ in vocab]
        return dict(zip(vocab, log_normalize(raw)))

    return model


def exhaustive(model, n):
    out = []

    def rec(prefix, s):
        for w, lp in model(tuple(prefix)).items():
            if lp == NEG_INF:
                continue
            if w == EOS:
                out.append((prefix + [w], s + lp))
            elif len(prefix) + 1 < n:
                rec(prefix + [w], s + lp)

    rec([], 0.0)
    return out


def test_gnmt_check_value() -> None:
    assert round(gnmt_penalty(0.6)(10), 6) == 1.732862
    assert gnmt_penalty(0.6)(1) == 1.0
    assert gnmt_penalty(0.0)(10) == 1.0


def test_example() -> None:
    hyps = [SHORT, LONG]
    assert rerank(hyps, power_penalty(0.0))[0] == SHORT[0]
    y, s = rerank(hyps, power_penalty(1.0))
    assert y == LONG[0] and math.isclose(s, -0.4)
    assert math.isclose(normalized(-2.0, 3, power_penalty(1.0)), -2.0 / 3)
    assert rerank(hyps, gnmt_penalty(0.6))[0] == SHORT[0]
    assert rerank(hyps, gnmt_penalty(1.0))[0] == LONG[0]
    assert math.isclose(normalized(-2.0, 3, gnmt_penalty(1.0)), -1.5)
    assert math.isclose(normalized(-3.2, 8, gnmt_penalty(1.0)), -3.2 * 6 / 13)
    assert rerank(hyps, power_penalty(0.6))[0] == LONG[0]


def test_rerank_against_brute_force() -> None:
    rng = random.Random(1)
    for _ in range(300):
        hyps = [(["t"] * rng.randrange(1, 12), -rng.uniform(0, 15)) for _ in range(rng.randrange(1, 8))]
        for lp in (power_penalty(0.0), power_penalty(0.7), gnmt_penalty(0.6), gnmt_penalty(1.0)):
            y, s = rerank(hyps, lp)
            best = max(h[1] / lp(len(h[0])) for h in hyps)
            assert s == best
            assert any(h[0] == y and h[1] / lp(len(h[0])) == best for h in hyps)


def test_normalized_score_is_not_monotone() -> None:
    lp = power_penalty(1.0)
    before = normalized(-1.0, 1, lp)
    after = normalized(-1.0 + math.log(0.9), 2, lp)
    assert after > before
    # The raw log probability can only go down.
    assert -1.0 + math.log(0.9) < -1.0


def test_wide_beam_finds_the_best_normalized_output() -> None:
    vocab = ["a", "b", "c", EOS]
    for seed in range(40):
        model = random_model(seed, vocab, 5)
        outs = exhaustive(model, 5)
        for lp in (power_penalty(0.0), power_penalty(1.0), gnmt_penalty(0.6), gnmt_penalty(2.0)):
            got = beam_search_normalized(model, 5, 10**6, lp)
            want = max(s / lp(len(y)) for y, s in outs)
            assert math.isclose(got[1], want)


def test_normalization_changes_the_length_of_the_choice() -> None:
    vocab = ["a", "b", "c", EOS]
    shorter = longer = 0
    for seed in range(40):
        model = random_model(seed, vocab, 6)
        raw = beam_search_normalized(model, 6, 10**6, power_penalty(0.0))
        norm = beam_search_normalized(model, 6, 10**6, power_penalty(1.0))
        assert len(norm[0]) >= len(raw[0]) or norm[1] >= raw[1] / len(raw[0])
        shorter += len(raw[0]) < len(norm[0])
        longer += len(raw[0]) > len(norm[0])
    assert shorter > 0 and longer == 0


def test_coverage_penalty() -> None:
    # Two target positions attend to three source words.
    attention = [[0.7, 0.3, 0.0], [0.6, 0.3, 0.1]]
    cp = gnmt_coverage(attention, 0.2)
    assert math.isclose(cp, 0.2 * (math.log(1.0) + math.log(0.6) + math.log(0.1)))
    assert gnmt_coverage(attention, 0.0) == 0.0
    assert gnmt_coverage([[1.0, 0.0]], 0.2) == NEG_INF


def test_word_reward() -> None:
    # The long hypothesis wins when 5 r > 1.2, that is r > 0.24.
    assert word_reward(-3.2, 8, 0.3) > word_reward(-2.0, 3, 0.3)
    assert word_reward(-3.2, 8, 0.2) < word_reward(-2.0, 3, 0.2)
    assert word_reward(-3.2, 8, 0.0) < word_reward(-2.0, 3, 0.0)


def test_long_hypothesis_in_log_space() -> None:
    log_p = 1000 * math.log(0.4)
    assert math.exp(log_p) == 0.0
    assert math.isclose(normalized(log_p, 1000, power_penalty(1.0)), math.log(0.4))
