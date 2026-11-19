# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/word-error-rate/. The authors are listed in prov/8WQ3ZQ.jsonl.

import random
from fractions import Fraction
from functools import lru_cache

import pytest

from word_error_rate import align, corpus_wer, normalize, wer


def brute_edits(ref, hyp):
    """The least number of edits, by plain recursion over the first words."""

    @lru_cache(maxsize=None)
    def go(i, j):
        if i == len(ref):
            return len(hyp) - j
        if j == len(hyp):
            return len(ref) - i
        return min(go(i + 1, j + 1) + (ref[i] != hyp[j]), go(i + 1, j) + 1, go(i, j + 1) + 1)

    return go(0, 0)


def test_check_values():
    assert wer("the cat sat on the mat".split(), "the cat sit on mat".split()) == Fraction(1, 3)
    S, D, I, _ = align("the cat sat on the mat".split(), "the cat sit on mat".split())
    assert (S, D, I) == (1, 1, 0)
    assert wer("a b".split(), "x y z w".split()) == 2
    assert float(wer("the cat sat on the mat".split(), "the cat sit on mat".split())) == pytest.approx(0.333333, abs=1e-6)


def test_edge_cases():
    assert wer(["a", "b", "c"], []) == 1  # an empty hypothesis: every word deleted
    assert wer(["a", "b"], ["a", "b"]) == 0
    assert wer(["a"], ["a", "x", "y"]) == 2  # insertions only, above 1
    with pytest.raises(ValueError):
        wer([], ["a"])


def test_against_brute_force():
    rng = random.Random(1)
    vocab = ["a", "b", "c", "d"]
    for _ in range(300):
        ref = [rng.choice(vocab) for _ in range(rng.randint(1, 7))]
        hyp = [rng.choice(vocab) for _ in range(rng.randint(0, 7))]
        S, D, I, ops = align(ref, hyp)
        assert S + D + I == brute_edits(tuple(ref), tuple(hyp))
        # the alignment reads back the two strings
        assert [r for op, r, _ in ops if op != "I"] == ref
        assert [h for op, _, h in ops if op != "D"] == hyp
        assert D - I == len(ref) - len(hyp)


def test_corpus_wer_is_not_the_mean_of_sentence_wers():
    pairs = [(["a"], ["b"]), ("a b c d e f g h i".split(), "a b c d e f g h i".split())]
    assert corpus_wer(pairs) == Fraction(1, 10)
    assert (wer(*pairs[0]) + wer(*pairs[1])) / 2 == Fraction(1, 2)


def test_normalization_changes_the_score():
    ref, hyp = "The cat sat.", "the cat sat"
    assert wer(ref.split(), hyp.split()) == Fraction(2, 3)
    assert wer(normalize(ref), normalize(hyp)) == 0
