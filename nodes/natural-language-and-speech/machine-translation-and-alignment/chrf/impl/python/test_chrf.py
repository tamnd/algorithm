# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chrf/. The authors are listed in prov/TFBFZV.jsonl.

import random
from fractions import Fraction

from chrf import corpus_chrf, corpus_stats, f_score, sentence_chrf, sentence_stats, split_words


def brute_matches(a, b, n):
    """Size of the multiset intersection of the n-grams, by removing items from a list."""
    rest = [tuple(b[i:i + n]) for i in range(len(b) - n + 1)]
    m = 0
    for i in range(len(a) - n + 1):
        g = tuple(a[i:i + n])
        if g in rest:
            rest.remove(g)
            m += 1
    return m


def brute_chrf(hyp, ref, order, beta):
    h, r = "".join(hyp.split()), "".join(ref.split())
    ps, rs = [], []
    for n in range(1, order + 1):
        th, tr = len(h) - n + 1, len(r) - n + 1
        if th > 0 and tr > 0:
            m = brute_matches(h, r, n)
            ps.append(m / th)
            rs.append(m / tr)
    if not ps:
        return 0.0
    p, rc = sum(ps) / len(ps), sum(rs) / len(rs)
    if p + rc == 0:
        return 0.0
    return (1 + beta * beta) * p * rc / (beta * beta * p + rc)


def test_hand_value():
    assert f_score(sentence_stats("ab", "abc", 2)) == Fraction(7, 11)


def test_page_example():
    st = sentence_stats("the cats", "the cat")
    assert st == [(6, 7, 6), (5, 6, 5), (4, 5, 4), (3, 4, 3), (2, 3, 2), (1, 2, 1)]
    assert abs(sentence_chrf("the cats", ["the cat"]) - 0.932588) < 1e-6
    assert abs(sentence_chrf("the cats", ["the cat"], beta=1) - 0.846946) < 1e-6


def test_edges():
    assert sentence_chrf("a cat", ["a cat"]) == 1.0
    assert sentence_chrf("xyz", ["abc"]) == 0.0
    assert sentence_chrf("", ["abc"]) == 0.0
    assert sentence_chrf("", [""]) == 0.0
    # white space does not count, so these are equal
    assert sentence_chrf("thecat", ["the cat"]) == 1.0


def test_symmetry_of_chrf1():
    rng = random.Random(5)
    for _ in range(100):
        a = "".join(rng.choice("ab c") for _ in range(rng.randint(0, 10)))
        b = "".join(rng.choice("ab c") for _ in range(rng.randint(0, 10)))
        assert sentence_chrf(a, [b], beta=1) == sentence_chrf(b, [a], beta=1)


def test_random_against_brute_force():
    rng = random.Random(2015)
    for _ in range(300):
        hyp = "".join(rng.choice("abc ") for _ in range(rng.randint(0, 12)))
        ref = "".join(rng.choice("abc ") for _ in range(rng.randint(0, 12)))
        beta = rng.choice([1, 2, 3])
        order = rng.randint(1, 6)
        st = sentence_stats(hyp, ref, order)
        h, r = "".join(hyp.split()), "".join(ref.split())
        for n in range(1, order + 1):
            assert st[n - 1][0] == brute_matches(h, r, n)
        got = sentence_chrf(hyp, [ref], order, beta=beta)
        assert abs(got - brute_chrf(hyp, ref, order, beta)) < 1e-12
        assert 0.0 <= got <= 1.0


def test_large_beta_tends_to_recall():
    st = sentence_stats("the cats", "the cat")
    assert abs(float(f_score(st, 1000)) - 1.0) < 1e-5
    st2 = sentence_stats("the cat", "the cats")
    assert float(f_score(st2, 1000)) < 0.74


def test_best_reference_and_corpus():
    one = corpus_stats(["the cat"], [["a dog", "the cat"]])
    assert one == sentence_stats("the cat", "the cat")
    hyps, refs = ["the cats", "a dog ran"], [["the cat"], ["a dog runs"]]
    c = corpus_chrf(hyps, refs)
    mean = (sentence_chrf(hyps[0], refs[0]) + sentence_chrf(hyps[1], refs[1])) / 2
    assert abs(c - mean) > 1e-4


def test_chrf_plus_plus_words():
    assert split_words("Hello, world!") == ["Hello", ",", "world", "!"]
    assert split_words("(hi) a .") == ["(hi", ")", "a", "."]
    assert split_words("'tis") == ["'", "tis"]
    st = sentence_stats("the cats", "the cat", 6, 2)
    assert st[6:] == [(1, 2, 2), (0, 1, 1)]
    assert sentence_chrf("a b", ["a b"], word_order=2) == 1.0
