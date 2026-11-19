# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/modified-kneser-ney-smoothing/. The authors are listed in prov/R2ZAVZ.jsonl.

import math
import random
from collections import Counter
from fractions import Fraction

import pytest

from modified_kneser_ney_smoothing import (
    BOS,
    EOS,
    ModifiedKneserNeyLM,
    chen_goodman_discounts,
    check_discounts,
    level_counts,
)

CHECK = [["a", "b"], ["a", "c"], ["b", "c"]]
Q = Fraction(3, 4)


def random_corpus(seed, sentences, words, max_len):
    rng = random.Random(seed)
    return [[rng.choice(words) for _ in range(rng.randint(0, max_len))] for _ in range(sentences)]


def zipf_corpus(seed, sentences, size, max_len):
    """Words w0, w1, ... with weights 1, 1/2, 1/3, ..., so that small counts are common."""
    rng = random.Random(seed)
    words = [f"w{i}" for i in range(size)]
    weights = [1 / (i + 1) for i in range(size)]
    return [rng.choices(words, weights, k=rng.randint(0, max_len)) for _ in range(sentences)]


def prefixes(corpus, n):
    out = {()}
    for s in corpus:
        for i in range(len(s) + 1):
            out.add(tuple(s[:i]))
    out.add(("zz",) * max(n - 1, 1))
    return out


def test_equal_discounts_give_the_kneser_ney_check_value():
    lm = ModifiedKneserNeyLM(CHECK, 2, discounts=[(0, 0, 0), (Q, Q, Q)])
    assert lm.prob("a") == Fraction(41, 84)
    assert lm.prob("b") == Fraction(19, 84)
    assert lm.prob("c") == Fraction(1, 7)
    assert lm.prob(EOS) == Fraction(1, 7)
    assert lm.prob(EOS, ["a", "c"]) == Fraction(41, 56)


def test_chen_goodman_discounts_by_hand():
    # counts of counts n_1..n_4 = 6, 3, 2, 1
    counts = Counter({i: k for i, k in enumerate([1] * 6 + [2] * 3 + [3] * 2 + [4])})
    y = Fraction(6, 12)
    d1, d2, d3 = chen_goodman_discounts(counts)
    assert d1 == 1 - 2 * y * Fraction(3, 6) == y
    assert d2 == 2 - 3 * y * Fraction(2, 3) == 1
    assert d3 == 3 - 4 * y * Fraction(1, 2) == 2


def test_d1_always_equals_y():
    rng = random.Random(3)
    for _ in range(50):
        n1, n2, n3, n4 = (rng.randint(1, 40) for _ in range(4))
        counts = Counter({i: k for i, k in enumerate([1] * n1 + [2] * n2 + [3] * n3 + [4] * n4)})
        try:
            d = chen_goodman_discounts(counts)
        except ValueError:
            continue
        assert d[0] == Fraction(n1, n1 + 2 * n2)


def test_one_history_by_hand():
    # After "x": y three times, z twice, u once. Discounts (1/2, 1, 3/2).
    corpus = [["x", "y"]] * 3 + [["x", "z"]] * 2 + [["x", "u"]]
    d = [(0, 0, 0), (Fraction(1, 2), 1, Fraction(3, 2))]
    lm = ModifiedKneserNeyLM(corpus, 2, discounts=d)
    gamma = (Fraction(1, 2) * 1 + 1 * 1 + Fraction(3, 2) * 1) / 6
    assert gamma == Fraction(1, 2)
    uni = lm._prob("y", ())
    assert uni == Fraction(1, 7)  # 7 bigram types, and y follows only x
    assert lm.prob("y", ["x"]) == (3 - Fraction(3, 2)) / 6 + gamma * uni
    assert lm.prob("u", ["x"]) == (1 - Fraction(1, 2)) / 6 + gamma * lm._prob("u", ())
    assert sum(lm.distribution(["x"]).values()) == 1


def naive_prob(corpus, n, d, vocab, w, h):
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

    def disc(k):
        return Fraction(0) if k == 0 else Fraction(d[m - 1][min(k, 3) - 1])

    followers = {g[-1] for g in grams if g[-m:-1] == h}
    t = sum(a(h + (x,)) for x in followers)
    if t == 0:
        return lower
    gamma = sum(disc(a(h + (x,))) for x in followers) / t
    k = a(h + (w,))
    return (k - disc(k)) / t + gamma * lower


@pytest.mark.parametrize("n", [1, 2, 3])
def test_matches_naive_reference(n):
    corpus = random_corpus(20 + n, 14, ["x", "y", "z", "u"], 5)
    d = [(Fraction(1, 3), Fraction(1, 2), Fraction(1, 2))] + [(Fraction(1, 2), Fraction(5, 4), 2)] * (n - 1)
    vocab = ["x", "y", "z", "u", "v"]
    lm = ModifiedKneserNeyLM(corpus, n, discounts=d, vocab=vocab)
    for toks in list(prefixes(corpus, n))[:25]:
        h = lm.history(toks)
        for w in sorted(lm.vocab):
            assert lm.prob(w, toks) == naive_prob(corpus, n, d, lm.vocab, w, h)


@pytest.mark.parametrize("n,seed", [(1, 1), (2, 2), (3, 3), (4, 5)])
def test_every_distribution_sums_to_one_with_default_discounts(n, seed):
    corpus = zipf_corpus(seed + 2, 300, 50, 6)
    lm = ModifiedKneserNeyLM(corpus, n)
    for m in range(2, n + 1):
        assert lm.d[m][0] == chen_goodman_discounts(level_counts(corpus, n)[m])[0]
    for toks in list(prefixes(corpus, n))[:60]:
        dist = lm.distribution(toks)
        assert sum(dist.values()) == 1
        assert all(p > 0 for p in dist.values())


def test_sums_to_one_at_the_edges_of_the_ranges():
    corpus = random_corpus(8, 40, ["a", "b", "c"], 6)
    for d in [(0, 0, 0), (1, 2, 3), (1, 0, 3), (Fraction(1, 7), 2, 0)]:
        lm = ModifiedKneserNeyLM(corpus, 3, discounts=[(Fraction(1, 2),) * 3, d, d], vocab=["a", "b", "c", "q"])
        for toks in prefixes(corpus, 3):
            assert sum(lm.distribution(toks).values()) == 1


def test_log_space_where_the_product_underflows():
    corpus = zipf_corpus(3, 300, 50, 6)
    lm = ModifiedKneserNeyLM(corpus, 2)
    sent = zipf_corpus(9, 1, 50, 1)[0] + [w for s in zipf_corpus(10, 400, 50, 6) for w in s]
    assert len(sent) > 900
    product, log_sum = 1.0, 0.0
    for i, w in enumerate(sent + [EOS]):
        p = float(lm.prob(w, sent[:i]))
        product *= p
        log_sum += math.log(p)
    assert product == 0.0
    lp = lm.sentence_logprob(sent)
    assert lp < -745 and lp == pytest.approx(log_sum, rel=1e-12)


def test_bad_input():
    with pytest.raises(ValueError):
        check_discounts((Fraction(3, 2), 1, 1))
    with pytest.raises(ValueError):
        check_discounts((1, 1, 4))
    with pytest.raises(ValueError):
        check_discounts((1, 1))
    with pytest.raises(ValueError):
        chen_goodman_discounts(Counter({"a": 1, "b": 2}))  # n_3 = 0
    with pytest.raises(ValueError):
        # n_1..n_4 = 1, 1, 6, 0: Y = 1/3 and D2 = 2 - 3 (1/3) 6 = -4
        chen_goodman_discounts(Counter({i: k for i, k in enumerate([1, 2, 3, 3, 3, 3, 3, 3])}))
    with pytest.raises(ValueError):
        ModifiedKneserNeyLM(CHECK, 2, discounts=[(0, 0, 0), (Q, Q, Q)], vocab=["a", "b", "c", "q"])
