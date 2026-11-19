# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ctc-prefix-beam-search/. The authors are listed in prov/NXHD7B.jsonl.

import math
import random

import pytest

import nlslog
from ctc_prefix_beam_search import (
    collapse,
    exhaustive_best,
    exhaustive_scores,
    greedy_decode,
    lm_log_weight,
    prefix_beam_search,
)
from nlslog import log_add, log_sum

# The example of the page: symbols _ (blank, 0), a (1), b (2), T = 3 frames.
Y = [[0.5, 0.4, 0.1], [0.4, 0.3, 0.3], [0.3, 0.1, 0.6]]
LY = [[math.log(p) for p in row] for row in Y]
A, B = 1, 2
WIDE = 10 ** 6


def random_log_y(rng, T, K):
    rows = [[rng.random() + 0.05 for _ in range(K)] for _ in range(T)]
    return [[math.log(x / sum(r)) for x in r] for r in rows]


def bigram_lm(table):
    """A label bigram hook: lm(prefix, c) = ln table[last label or 0][c]."""

    def lm(prefix, c):
        return math.log(table[prefix[-1] if prefix else 0][c])

    return lm


def test_helper_header():
    with open(nlslog.__file__, encoding="utf-8") as f:
        lines = f.read().splitlines()
    assert lines[1] == "# Shared helper of the natural-language-and-speech pages of https://algorithm.tamnd.com/. The authors are listed in prov/."


def test_log_add_check_value():
    assert log_add(math.log(0.5), math.log(0.25)) == pytest.approx(-0.287682, abs=1e-6)


def test_collapse():
    assert collapse([A, A, 0, A, B, 0]) == (A, A, B)
    assert collapse([0, 0]) == ()


def test_page_example_full_beam_is_exact():
    best, score, final = prefix_beam_search(LY, WIDE)
    assert best == (A, B)
    assert math.exp(score) == pytest.approx(0.366, abs=1e-12)
    want = {(A, B): 0.366, (B,): 0.294, (A,): 0.176, (): 0.06, (B, A): 0.034, (B, B): 0.024}
    got = dict(final)
    for prefix, p in want.items():
        assert math.exp(got[prefix]) == pytest.approx(p, abs=1e-12)
    # The final scores of a full beam are the exact labeling probabilities, which sum to 1.
    assert log_sum([s for _, s in final]) == pytest.approx(0.0, abs=1e-12)


def test_page_example_beam_trace():
    _, _, beam1 = prefix_beam_search(LY[:1], 3)
    _, _, beam2 = prefix_beam_search(LY[:2], 3)
    assert [(p, round(math.exp(s), 12)) for p, s in beam1] == [((), 0.5), ((A,), 0.4), ((B,), 0.1)]
    assert [(p, round(math.exp(s), 12)) for p, s in beam2] == [((A,), 0.43), ((B,), 0.22), ((), 0.2)]


def test_greedy_differs_from_the_most_probable_labeling():
    assert greedy_decode(LY) == (B,)
    assert exhaustive_best(LY)[0] == (A, B)


def test_narrow_beams_can_be_wrong():
    # Beam 3 prunes "ab" (0.12) after frame 2 and returns "b" (0.294) instead of "ab" (0.366).
    best, score, _ = prefix_beam_search(LY, 3)
    assert best == (B,)
    assert math.exp(score) == pytest.approx(0.294, abs=1e-12)
    # Beam 2 returns the right labeling, but with a score that misses the pruned paths.
    best, score, _ = prefix_beam_search(LY, 2)
    assert best == (A, B)
    assert math.exp(score) == pytest.approx(0.258, abs=1e-12)
    # Beam 1 returns "b" with the probability of one path only.
    best, score, _ = prefix_beam_search(LY, 1)
    assert best == (B,) and math.exp(score) == pytest.approx(0.12, abs=1e-12)
    # A wider beam is not always better: 2 is right here, 3 is wrong, 4 is exact.
    assert prefix_beam_search(LY, 4)[0] == (A, B)


def test_recovery_of_pruned_prefixes():
    # The "l+ not in A_prev" step of Hannun et al. gets back the 0.108 that beam 3 lost.
    best, score, _ = prefix_beam_search(LY, 3, recover=True)
    assert best == (A, B) and math.exp(score) == pytest.approx(0.366, abs=1e-12)
    best, score, _ = prefix_beam_search(LY, 2, recover=True)
    assert best == (A, B) and math.exp(score) == pytest.approx(0.366, abs=1e-12)


def test_full_beam_against_exhaustive_search():
    rng = random.Random(2)
    for _ in range(80):
        T, K = rng.randint(1, 6), rng.randint(2, 3)
        ly = random_log_y(rng, T, K)
        scores = exhaustive_scores(ly)
        ranked = sorted(scores.values(), reverse=True)
        if len(ranked) > 1 and ranked[0] - ranked[1] < 1e-9:
            continue  # a tie; either answer is right
        best, score, final = prefix_beam_search(ly, WIDE, recover=rng.random() < 0.5)
        assert best == exhaustive_best(ly)[0]
        assert score == pytest.approx(scores[best], abs=1e-10)
        for prefix, s in final:
            if s == float("-inf"):
                assert prefix not in scores  # a prefix with too many repeats for T frames
            else:
                assert s == pytest.approx(scores[prefix], abs=1e-10)


def test_full_beam_with_a_language_model_against_exhaustive_search():
    rng = random.Random(4)
    for _ in range(60):
        T, K = rng.randint(1, 5), 3
        ly = random_log_y(rng, T, K)
        table = [[rng.random() + 0.05 for _ in range(K)] for _ in range(K)]
        lm = bigram_lm(table)
        scores = exhaustive_scores(ly, lm)
        ranked = sorted(scores.values(), reverse=True)
        if len(ranked) > 1 and ranked[0] - ranked[1] < 1e-9:
            continue
        best, score, _ = prefix_beam_search(ly, WIDE, lm=lm)
        assert best == exhaustive_best(ly, lm)[0]
        assert score == pytest.approx(scores[best], abs=1e-10)
        assert lm_log_weight(best, lm) == pytest.approx(sum(lm(best[:i], best[i]) for i in range(len(best))), abs=1e-12)


def test_language_model_changes_the_answer():
    # An LM that makes "b" after "a" very likely and "b" at the start unlikely.
    table = [[1.0, 0.5, 0.01], [1.0, 0.1, 0.9], [1.0, 0.5, 0.5]]
    lm = bigram_lm(table)
    assert prefix_beam_search(LY, WIDE, lm=lm)[0] == (A, B)
    table = [[1.0, 0.9, 0.9], [1.0, 0.05, 0.05], [1.0, 0.5, 0.5]]
    lm = bigram_lm(table)
    best, _, _ = prefix_beam_search(LY, WIDE, lm=lm)
    assert best == exhaustive_best(LY, lm)[0] == (B,)


def test_narrow_beam_is_never_better_than_the_optimum():
    rng = random.Random(9)
    wrong = 0
    for _ in range(60):
        T, K = rng.randint(2, 6), 3
        ly = random_log_y(rng, T, K)
        _, opt = exhaustive_best(ly)
        best, score, _ = prefix_beam_search(ly, 2)
        # A pruned search only drops paths, so its score is at most the true probability.
        assert score <= exhaustive_scores(ly)[best] + 1e-12 <= opt + 1e-12
        wrong += best != exhaustive_best(ly)[0]
    assert wrong > 0


def test_errors():
    with pytest.raises(ValueError):
        prefix_beam_search(LY, 0)
    with pytest.raises(ValueError):
        prefix_beam_search([], 4)
