# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/luhn-summarization/. The authors are listed in prov/JX112C.jsonl.

import random
from fractions import Fraction

from luhn_summarization import (
    clusters,
    luhn_above,
    luhn_scores,
    luhn_summarize,
    sentence_score,
    significant_words,
    word_frequencies,
)


def brute_score(sentence, sig, gap):
    """Best score over all maximal clusters, found by testing every pair of positions."""
    pos = [i for i, w in enumerate(sentence) if w.lower() in sig]
    best = Fraction(0)
    for i in range(len(pos)):
        for j in range(i, len(pos)):
            inner = all(pos[t + 1] - pos[t] - 1 <= gap for t in range(i, j))
            left = i == 0 or pos[i] - pos[i - 1] - 1 > gap
            right = j == len(pos) - 1 or pos[j + 1] - pos[j] - 1 > gap
            if inner and left and right:
                m = j - i + 1
                best = max(best, Fraction(m * m, pos[j] - pos[i] + 1))
    return best


def brute_significant(doc, low, high, stop):
    words = [w.lower() for s in doc for w in s]
    stop = {w.lower() for w in stop}
    out = set()
    for w in set(words):
        if w in stop:
            continue
        c = sum(1 for x in words if x == w)
        if low <= c <= high:
            out.add(w)
    return out


def test_luhn_figure_two_shape():
    # Four significant words in a bracket of seven words: 4^2 / 7.
    s = "S x S S x x S".split()
    assert sentence_score(s, {"s"}) == Fraction(16, 7)
    assert clusters(s, {"s"}) == [(0, 6, 4)]


def test_gap_limit():
    # Four non-significant words keep one cluster, five split it.
    s4 = "S a b c d S".split()
    s5 = "S a b c d e S".split()
    assert clusters(s4, {"s"}) == [(0, 5, 2)]
    assert sentence_score(s4, {"s"}) == Fraction(4, 6)
    assert clusters(s5, {"s"}) == [(0, 0, 1), (6, 6, 1)]
    assert sentence_score(s5, {"s"}) == 1


def test_not_the_best_subspan():
    # The score uses maximal clusters; a dense part of a cluster does not count alone.
    s = "S a b c d S S S".split()
    assert sentence_score(s, {"s"}) == Fraction(16, 8)
    assert Fraction(9, 3) > sentence_score(s, {"s"})


def test_no_significant_word():
    assert sentence_score("a b c".split(), {"z"}) == 0
    assert sentence_score([], {"z"}) == 0


def test_page_example():
    doc = [
        "The new solar cell turns light into power".split(),
        "Engineers built the solar cell from thin silicon".split(),
        "The weather was cold that week".split(),
        "A thin silicon solar cell costs less to build".split(),
        "Power from light is clean".split(),
    ]
    stop = {"the", "a", "into", "from", "to", "was", "that", "is", "less"}
    f = word_frequencies(doc, stop)
    assert f["solar"] == 3 and f["cell"] == 3 and f["thin"] == 2
    sig = significant_words(doc, 2, 3, stop)
    assert sig == {"solar", "cell", "light", "power", "thin", "silicon"}
    scores = luhn_scores(doc, 2, 3, stop)
    assert scores == [Fraction(8, 3), Fraction(16, 5), 0, Fraction(4), Fraction(4, 3)]
    assert clusters(doc[1], sig) == [(3, 7, 4)]
    assert luhn_summarize(doc, 2, 2, 3, stop) == [1, 3]
    assert luhn_above(doc, Fraction(2), 2, 3, stop) == [0, 1, 3]


def test_ties_go_to_the_earlier_sentence():
    doc = [["x", "y"], ["x", "y"], ["q"]]
    assert luhn_summarize(doc, 1, 2, 2) == [0]
    assert luhn_summarize(doc, 5, 2, 2) == [0, 1]


def test_random_against_brute_force():
    rng = random.Random(1958)
    vocab = ["w%d" % i for i in range(7)]
    for _ in range(600):
        doc = [[rng.choice(vocab) for _ in range(rng.randint(0, 12))]
               for _ in range(rng.randint(1, 5))]
        stop = set(rng.sample(vocab, rng.randint(0, 2)))
        low = rng.randint(1, 3)
        high = low + rng.randint(0, 6)
        gap = rng.randint(0, 4)
        sig = significant_words(doc, low, high, stop)
        assert sig == brute_significant(doc, low, high, stop)
        got = luhn_scores(doc, low, high, stop, gap)
        want = [brute_score(s, sig, gap) for s in doc]
        assert got == want
        for s, x in zip(doc, got):
            # A cluster has len >= m and len <= m + (m - 1) gap, so m / (gap + 1) < m^2 / len <= m.
            r = sum(1 for w in s if w.lower() in sig)
            assert 0 <= x <= r
            if r > 0:
                assert x >= Fraction(1, gap + 1)
        k = rng.randint(0, 4)
        chosen = luhn_summarize(doc, k, low, high, stop, gap)
        assert chosen == sorted(chosen) and len(chosen) <= k
        rest = [i for i in range(len(doc)) if i not in chosen]
        for i in chosen:
            assert got[i] > 0
            for j in rest:
                assert got[i] > got[j] or (got[i] == got[j] and i < j)
