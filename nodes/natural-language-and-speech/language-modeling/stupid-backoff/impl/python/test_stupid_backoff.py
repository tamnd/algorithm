# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/stupid-backoff/. The authors are listed in prov/0ZTM89.jsonl.

import math
import random
from fractions import Fraction

import pytest

from stupid_backoff import ALPHA, BOS, EOS, StupidBackoff

CHECK = [["a", "b"], ["a", "c"], ["b", "c"]]


def random_corpus(seed, sentences, words, max_len):
    rng = random.Random(seed)
    return [[rng.choice(words) for _ in range(rng.randint(0, max_len))] for _ in range(sentences)]


def prefixes(corpus):
    out = {()}
    for s in corpus:
        for i in range(len(s) + 1):
            out.add(tuple(s[:i]))
    out.add(("zz", "zz", "zz"))
    return out


def brute_score(corpus, n, alpha, w, h):
    """The definition, with every count found by a scan of the padded sentences."""
    padded = [[BOS] * (n - 1) + s + [EOS] for s in corpus]

    def count(g):
        k = 0
        for toks in padded:
            for i in range(n - 1, len(toks)):
                if tuple(toks[i - len(g) + 1 : i + 1]) == g:
                    k += 1
        return k

    hist = sum(count(h + (x,)) for x in {t for toks in padded for t in toks if t != BOS})
    k = count(h + (w,))
    if k > 0:
        return Fraction(k, hist)
    if not h:
        return Fraction(0)
    return alpha * brute_score(corpus, n, alpha, w, h[1:])


def test_check_corpus_by_hand():
    sb = StupidBackoff(CHECK, 2)
    assert sb.score("a") == Fraction(2, 3)
    assert sb.score("b") == Fraction(1, 3)
    assert sb.score("c") == ALPHA * Fraction(2, 9)
    assert sb.score(EOS) == ALPHA * Fraction(3, 9)
    assert sum(sb.scores().values()) == Fraction(11, 9)  # not a distribution
    assert sb.score("q") == 0


@pytest.mark.parametrize("n", [1, 2, 3])
def test_matches_brute_force(n):
    corpus = random_corpus(n, 10, ["x", "y", "z", "u"], 5)
    sb = StupidBackoff(corpus, n)
    for toks in list(prefixes(corpus))[:15]:
        h = sb.history(toks)
        for w in sorted(sb.vocab):
            assert sb.score(w, toks) == brute_score(corpus, n, ALPHA, w, h)


@pytest.mark.parametrize("n,seed", [(2, 1), (3, 2), (4, 3)])
def test_scores_are_bounded_but_not_normalized(n, seed):
    corpus = random_corpus(seed, 40, ["a", "b", "c", "d", "e", "f"], 6)
    sb = StupidBackoff(corpus, n)
    bound = sum(ALPHA**k for k in range(n))
    above_one = 0
    for toks in prefixes(corpus):
        sc = sb.scores(toks)
        assert all(0 < s <= 1 for s in sc.values())
        total = sum(sc.values())
        assert total <= bound
        if sb.ch[sb.history(toks)] > 0:
            assert total >= 1
        above_one += total > 1
    assert above_one > 0


def test_alpha_zero_is_maximum_likelihood_after_seen_histories():
    corpus = random_corpus(4, 30, ["a", "b", "c", "d"], 5)
    sb = StupidBackoff(corpus, 3, alpha=0)
    for toks in prefixes(corpus):
        if sb.ch[sb.history(toks)] > 0:
            assert sum(sb.scores(toks).values()) == 1


def test_float_alpha_agrees_with_fraction():
    corpus = random_corpus(5, 30, ["a", "b", "c", "d"], 5)
    exact = StupidBackoff(corpus, 3)
    approx = StupidBackoff(corpus, 3, alpha=0.4)
    for toks in list(prefixes(corpus))[:20]:
        for w in exact.vocab:
            assert float(approx.score(w, toks)) == pytest.approx(float(exact.score(w, toks)), rel=1e-12)


def test_log_space_where_the_product_underflows():
    corpus = random_corpus(6, 40, ["a", "b", "c", "d", "e", "f"], 8)
    sb = StupidBackoff(corpus, 3)
    rng = random.Random(7)
    sent = [rng.choice(["a", "b", "c", "d", "e", "f"]) for _ in range(1500)]
    product, log_sum = 1.0, 0.0
    for i, w in enumerate(sent + [EOS]):
        s = float(sb.score(w, sent[:i]))
        product *= s
        log_sum += math.log(s)
    assert product == 0.0
    ls = sb.sentence_logscore(sent)
    assert ls < -745 and ls == pytest.approx(log_sum, rel=1e-12)
    assert sb.sentence_logscore(["q"]) == -math.inf


def test_bad_input():
    with pytest.raises(ValueError):
        StupidBackoff(CHECK, 0)
    with pytest.raises(ValueError):
        StupidBackoff(CHECK, 2, alpha=Fraction(3, 2))
