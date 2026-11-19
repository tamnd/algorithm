# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kneser-ney-smoothing/. The authors are listed in prov/M3W0NG.jsonl.

import math
import random
from fractions import Fraction

import pytest

from kneser_ney_smoothing import BOS, EOS, KneserNeyLM, default_discount, level_counts, log_fraction

CHECK = [["a", "b"], ["a", "c"], ["b", "c"]]


def random_corpus(seed, sentences, words, max_len):
    rng = random.Random(seed)
    return [[rng.choice(words) for _ in range(rng.randint(0, max_len))] for _ in range(sentences)]


def histories(lm, corpus):
    """Sentence prefixes that reach every seen history, plus a few unseen ones."""
    out = {()}
    for s in corpus:
        for i in range(len(s) + 1):
            out.add(tuple(s[:i]))
    out.add(("zz",) * (lm.n - 1))
    return out


def test_check_value_bigram():
    lm = KneserNeyLM(CHECK, 2, discounts=[0, Fraction(3, 4)])
    assert len(lm.a[2]) == 7
    assert lm.prob("a") == Fraction(41, 84)
    assert lm.prob("b") == Fraction(19, 84)
    assert lm.prob("c") == Fraction(1, 7)
    assert lm.prob(EOS) == Fraction(1, 7)
    assert lm.prob(EOS, ["a", "c"]) == Fraction(41, 56)


def test_continuation_unigram():
    lm = KneserNeyLM(CHECK, 2, discounts=[0, Fraction(3, 4)])
    uni = {w: lm._prob(w, ()) for w in lm.vocab}
    assert uni == {"a": Fraction(1, 7), "b": Fraction(2, 7), "c": Fraction(2, 7), EOS: Fraction(2, 7)}


def test_lower_level_uses_continuation_counts_not_raw_counts():
    # "francisco" is frequent but follows only "san"; "the" follows many words.
    corpus = [["san", "francisco"]] * 5 + [["a", "the"], ["b", "the"], ["c", "the"]]
    lm = KneserNeyLM(corpus, 2, discounts=[0, Fraction(3, 4)])
    assert lm.a[1][("francisco",)] == 1
    assert lm.a[1][("the",)] == 3
    # Raw counts are 5 and 3, but the lower level ranks the two words the other way.
    assert lm._prob("francisco", ()) == Fraction(1, 10)
    assert lm._prob("the", ()) == Fraction(3, 10)
    # Neither word was seen after "francisco", so the lower level decides.
    assert lm.prob("the", ["san", "francisco"]) == 3 * lm.prob("francisco", ["san", "francisco"])


def naive_prob(corpus, n, d, vocab, w, h):
    """The same model, with every count found again by a scan over all positions."""
    m = len(h) + 1
    lower = Fraction(1, len(vocab)) if m == 1 else naive_prob(corpus, n, d, vocab, w, h[1:])
    grams = []
    for s in corpus:
        toks = [BOS] * (n - 1) + s + [EOS]
        for i in range(n - 1, len(toks)):
            grams.append(tuple(toks[i - n + 1 : i + 1]))

    def a(g):
        if m == n:
            return sum(1 for x in grams if x == g)
        return len({x[-m - 1] for x in grams if x[-m:] == g})

    followers = {g[-1] for g in grams if g[-m:-1] == h}
    t = sum(a(h + (x,)) for x in followers)
    if t == 0:
        return lower
    types = sum(1 for x in followers if a(h + (x,)) > 0)
    return max(a(h + (w,)) - d[m - 1], Fraction(0)) / t +d[m - 1] * Fraction(types, t) * lower


@pytest.mark.parametrize("n", [1, 2, 3])
def test_matches_naive_reference(n):
    corpus = random_corpus(7 + n, 12, ["x", "y", "z", "u"], 5)
    lm = KneserNeyLM(corpus, n, discounts=[Fraction(1, 3)] + [Fraction(2, 3)] * (n - 1), vocab=["x", "y", "z", "u", "v"])
    d = [lm.d[m] for m in range(1, n + 1)]
    for toks in list(histories(lm, corpus))[:25]:
        h = lm.history(toks)
        for w in sorted(lm.vocab):
            assert lm.prob(w, toks) == naive_prob(corpus, n, d, lm.vocab, w, h)


@pytest.mark.parametrize("n,seed", [(1, 1), (2, 2), (3, 3), (4, 4)])
def test_every_distribution_sums_to_one(n, seed):
    corpus = random_corpus(seed, 40, ["a", "b", "c", "d", "e"], 6)
    lm = KneserNeyLM(corpus, n)
    for toks in histories(lm, corpus):
        dist = lm.distribution(toks)
        assert sum(dist.values()) == 1
        assert all(p > 0 for p in dist.values())


def test_sums_to_one_with_open_vocabulary_and_uniform_base():
    corpus = random_corpus(11, 30, ["a", "b", "c"], 5)
    lm = KneserNeyLM(corpus, 3, discounts=[Fraction(1, 2), Fraction(3, 4), Fraction(3, 4)], vocab=["a", "b", "c", "<unk>", "q"])
    for toks in histories(lm, corpus):
        dist = lm.distribution(toks)
        assert sum(dist.values()) == 1
        assert dist["q"] > 0


def test_default_discount_from_counts_of_counts():
    corpus = random_corpus(5, 50, ["a", "b", "c", "d"], 6)
    a = level_counts(corpus, 3)
    for m in (2, 3):
        n1 = sum(1 for k in a[m].values() if k == 1)
        n2 = sum(1 for k in a[m].values() if k == 2)
        assert default_discount(a[m]) == Fraction(n1, n1 + 2 * n2)
    lm = KneserNeyLM(corpus, 3)
    assert lm.d[1] == 0
    assert lm.d[3] == default_discount(a[3])


def test_log_space_where_the_product_underflows():
    corpus = random_corpus(3, 30, ["a", "b", "c", "d", "e", "f"], 8)
    lm = KneserNeyLM(corpus, 2)
    rng = random.Random(9)
    long_sent = [rng.choice(["a", "b", "c", "d", "e", "f"]) for _ in range(1500)]
    product = 1.0
    log_sum = 0.0
    for i, w in enumerate(long_sent + [EOS]):
        p = lm.prob(w, long_sent[:i])
        product *= float(p)
        log_sum += math.log(float(p))
    assert product == 0.0
    lp = lm.sentence_logprob(long_sent)
    assert math.isfinite(lp) and lp < -745
    assert lp == pytest.approx(log_sum, rel=1e-12)
    assert log_fraction(Fraction(1, 10**400)) == pytest.approx(-400 * math.log(10))


def test_bad_input():
    with pytest.raises(ValueError):
        KneserNeyLM(CHECK, 0)
    with pytest.raises(ValueError):
        KneserNeyLM(CHECK, 2, discounts=[0, Fraction(5, 4)])
    with pytest.raises(ValueError):
        KneserNeyLM(CHECK, 2, discounts=[0, Fraction(1, 2)], vocab=["a", "b", "c", "q"])
    lm = KneserNeyLM(CHECK, 2, discounts=[0, Fraction(3, 4)])
    with pytest.raises(KeyError):
        lm.prob("q")
