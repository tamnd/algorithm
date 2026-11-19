# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bleu/. The authors are listed in prov/FSSX1F.jsonl.

import math
import random
from fractions import Fraction

from bleu import (
    bleu_details,
    brevity_penalty,
    closest_ref_length,
    corpus_bleu,
    corpus_stats,
    sentence_bleu,
    sentence_stats,
)


def toks(s):
    return s.split()


def brute_clipped(cand, refs, n):
    """Clipped matches and total by scanning lists, with no Counter."""
    grams = [tuple(cand[i:i + n]) for i in range(len(cand) - n + 1)]
    seen = []
    m = 0
    for g in grams:
        if g in seen:
            continue
        seen.append(g)
        in_cand = sum(1 for x in grams if x == g)
        in_ref = 0
        for r in refs:
            k = sum(1 for i in range(len(r) - n + 1) if tuple(r[i:i + n]) == g)
            in_ref = max(in_ref, k)
        m += min(in_cand, in_ref)
    return m, len(grams)


def test_check_value():
    cand = toks("the cat sat on the mat")
    ref = toks("the cat sat on the red mat")
    ps, bp, score = bleu_details([cand], [[ref]])
    assert ps == [Fraction(6, 6), Fraction(4, 5), Fraction(3, 4), Fraction(2, 3)]
    assert abs(bp - 0.846482) < 1e-6
    assert abs(score - 0.673182) < 1e-6


def test_papineni_clipping():
    cand = toks("the the the the the the the")
    st = sentence_stats(cand, [toks("the cat is on the mat")], 1)
    assert Fraction(st.matches[0], st.totals[0]) == Fraction(2, 7)
    st2 = sentence_stats(cand, [toks("the cat is on the mat"), toks("there is a cat on the mat")], 1)
    assert Fraction(st2.matches[0], st2.totals[0]) == Fraction(2, 7)


def test_identical_and_empty():
    s = toks("a b c d e f")
    assert corpus_bleu([s], [[s]]) == 1.0
    assert corpus_bleu([[]], [[s]]) == 0.0
    # three tokens: no 4-gram, so the unsmoothed and the smoothed score are 0
    assert corpus_bleu([toks("a b c")], [[toks("a b c")]]) == 0.0
    assert sentence_bleu(toks("a b c"), [toks("a b c")]) == 0.0


def test_brevity_penalty():
    assert brevity_penalty(7, 6) == 1.0
    assert brevity_penalty(6, 6) == 1.0
    assert abs(brevity_penalty(6, 7) - math.exp(1 - 7 / 6)) < 1e-15
    assert brevity_penalty(0, 3) == 0.0
    # a candidate longer than the reference gets no penalty
    cand = toks("the cat sat on the red mat today")
    ps, bp, _ = bleu_details([cand], [[toks("the cat sat on the red mat")]])
    assert bp == 1.0
    assert ps[0] == Fraction(7, 8)


def test_closest_reference_tie():
    assert closest_ref_length(5, [3, 7]) == 3
    assert closest_ref_length(5, [7, 3]) == 3
    assert closest_ref_length(5, [6, 9, 4]) == 4
    assert closest_ref_length(5, [5, 4]) == 5


def test_zero_count_and_smoothing():
    cand = toks("a b x c d")
    ref = toks("a b y c d")
    st = sentence_stats(cand, [ref])
    assert st.matches == [4, 2, 0, 0]
    assert sentence_bleu(cand, [ref], smoothing="none") == 0.0
    # method 3: p3 = 1/(2 * 3), p4 = 1/(4 * 2)
    want = math.exp((math.log(4 / 5) + math.log(2 / 4) + math.log(1 / 6) + math.log(1 / 8)) / 4)
    assert abs(sentence_bleu(cand, [ref], smoothing="exp") - want) < 1e-12


def test_corpus_is_not_mean_of_sentences():
    c1, r1 = toks("the cat sat on the mat"), toks("the cat sat on the red mat")
    c2, r2 = toks("a dog ran in the park"), toks("a dog ran in the park")
    corpus = corpus_bleu([c1, c2], [[r1], [r2]])
    mean = (corpus_bleu([c1], [[r1]]) + corpus_bleu([c2], [[r2]])) / 2
    assert abs(corpus - mean) > 0.005
    ps, bp, _ = bleu_details([c1, c2], [[r1], [r2]])
    assert ps == [Fraction(12, 12), Fraction(9, 10), Fraction(7, 8), Fraction(5, 6)]
    assert abs(bp - math.exp(1 - 13 / 12)) < 1e-15


def test_random_against_brute_force():
    rng = random.Random(311)
    vocab = ["a", "b", "c", "d"]
    for _ in range(300):
        cand = [rng.choice(vocab) for _ in range(rng.randint(0, 9))]
        refs = [[rng.choice(vocab) for _ in range(rng.randint(1, 9))] for _ in range(rng.randint(1, 3))]
        st = sentence_stats(cand, refs)
        for n in range(1, 5):
            assert (st.matches[n - 1], st.totals[n - 1]) == brute_clipped(cand, refs, n)
        lens = [len(r) for r in refs]
        best = min(abs(x - len(cand)) for x in lens)
        assert st.r == min(x for x in lens if abs(x - len(cand)) == best)
        score = corpus_bleu([cand], [refs])
        assert 0.0 <= score <= 1.0
        if 0.0 < score:
            assert all(m > 0 for m in st.matches)


def test_corpus_stats_add_up():
    rng = random.Random(7)
    vocab = ["x", "y", "z"]
    cands = [[rng.choice(vocab) for _ in range(rng.randint(1, 8))] for _ in range(5)]
    refs = [[[rng.choice(vocab) for _ in range(rng.randint(1, 8))]] for _ in range(5)]
    total = corpus_stats(cands, refs)
    parts = [sentence_stats(c, r) for c, r in zip(cands, refs)]
    assert total.matches == [sum(p.matches[i] for p in parts) for i in range(4)]
    assert total.totals == [sum(p.totals[i] for p in parts) for i in range(4)]
    assert total.c == sum(p.c for p in parts) and total.r == sum(p.r for p in parts)
