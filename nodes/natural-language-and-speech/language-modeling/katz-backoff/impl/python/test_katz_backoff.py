# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/katz-backoff/. The authors are listed in prov/99DA92.jsonl.

import itertools
import random
from collections import Counter
from fractions import Fraction as F

import pytest

from katz_backoff import BOS, EOS, KatzLM, katz_discounts

TOY = [s.split() for s in ["a a b", "a b c", "a", "c a"]]


def test_toy_values() -> None:
    m = KatzLM(TOY, 2, k=2)
    assert m.total == 13
    assert m.d[2] == {1: F(1, 3), 2: F(1, 2)}
    assert m.distribution((BOS,)) == {EOS: F(1, 9), "a": F(3, 4), "b": F(1, 18), "c": F(1, 12)}
    assert m.distribution(("a",)) == {EOS: F(1, 5), "a": F(1, 15), "b": F(1, 5), "c": F(8, 15)}
    assert m.distribution(("b",)) == {EOS: F(1, 6), "a": F(10, 21), "b": F(4, 21), "c": F(1, 6)}
    assert m.distribution(("c",)) == {EOS: F(1, 6), "a": F(1, 6), "b": F(1, 3), "c": F(1, 3)}
    assert m.alpha(("a",)) == F(52, 15)
    assert m.sentence_prob(["a", "b"]) == F(1, 40)


def test_discount_values() -> None:
    # N_1 = 6, N_2 = 2, N_3 = 1, k = 2: mu = 1/2, r*(1) = 2/3, r*(2) = 3/2
    assert katz_discounts({1: 6, 2: 2, 3: 1}, 2) == {1: F(1, 3), 2: F(1, 2)}
    assert katz_discounts({2: 3}, 2) == {}  # no singletons
    assert katz_discounts({1: 2, 2: 5, 3: 4}, 2) == {}  # mu >= 1
    assert katz_discounts({1: 4, 3: 1}, 1) == {}  # d_1 = 0


def test_k_one_is_degenerate() -> None:
    # with k = 1, r*(1) = mu, so d_1 = 0 and the discounts are rejected
    rng = random.Random(1)
    for _ in range(50):
        nr = {r: rng.randrange(1, 20) for r in range(1, 6)}
        assert katz_discounts(nr, 1) == {}


def test_discounted_mass_is_n1() -> None:
    """When the discounts are valid, the counts 1 to k give up exactly N_1."""
    rng = random.Random(2)
    found = 0
    for _ in range(400):
        k = rng.randrange(2, 7)
        nr = {r: int(rng.uniform(0.5, 1.5) * 300 / r**2) for r in range(1, 10)}
        nr = {r: v for r, v in nr.items() if v > 0}
        d = katz_discounts(nr, k)
        if not d:
            continue
        found += 1
        assert sum(nr[r] * r * (1 - d[r]) for r in d) == nr[1]
        assert all(0 < x <= 1 for x in d.values())
    assert found > 20


def direct_bigram(corpus, k):
    """The bigram Katz formula written out, with counts found by a plain scan."""
    pairs, toks = [], []
    for s in corpus:
        x = [BOS] + s + [EOS]
        pairs += list(zip(x, x[1:]))
        toks += x[1:]
    n = len(toks)
    vocab = set(toks)
    pc = Counter(pairs)
    nr = Counter(pc.values())
    d = katz_discounts(dict(nr), k)

    def uni(w):
        return F(toks.count(w), n)

    def bi(w, v):
        cv = sum(c for (a, _), c in pc.items() if a == v)
        if cv == 0:
            return uni(w)
        seen = {b for (a, b) in pc if a == v}
        if seen == vocab:
            return F(pc[(v, w)], cv)
        if w in seen:
            return d.get(pc[(v, w)], 1) * F(pc[(v, w)], cv)
        beta = 1 - sum(d.get(pc[(v, x)], 1) * F(pc[(v, x)], cv) for x in seen)
        return beta * uni(w) / (1 - sum(uni(x) for x in seen))

    return bi, vocab


def test_against_direct_formula() -> None:
    rng = random.Random(4)
    for _ in range(60):
        words = ["a", "b", "c", "d", "e"][: rng.randrange(2, 6)]
        corpus = [[rng.choice(words) for _ in range(rng.randrange(0, 6))] for _ in range(rng.randrange(1, 7))]
        k = rng.randrange(1, 4)
        m = KatzLM(corpus, 2, k=k)
        bi, vocab = direct_bigram(corpus, k)
        assert m.vocab == vocab
        for v in [BOS] + words:
            for w in vocab:
                assert m.prob(w, [v]) == bi(w, v)


def test_rows_sum_to_one() -> None:
    rng = random.Random(9)
    for _ in range(80):
        n = rng.randrange(1, 4)
        words = ["a", "b", "c", "d"]
        corpus = [[rng.choice(words) for _ in range(rng.randrange(0, 7))] for _ in range(rng.randrange(1, 7))]
        m = KatzLM(corpus, n, k=rng.randrange(2, 5))
        for h in itertools.product([BOS] + words, repeat=n - 1):
            d = m.distribution(h)
            assert sum(d.values()) == 1
            assert all(p >= 0 for p in d.values())


def test_errors() -> None:
    m = KatzLM(TOY, 2, k=2)
    with pytest.raises(KeyError):
        m.prob("z", ["a"])
    with pytest.raises(KeyError):
        m.prob(BOS, ["a"])
    with pytest.raises(ValueError):
        KatzLM(TOY, 0)
