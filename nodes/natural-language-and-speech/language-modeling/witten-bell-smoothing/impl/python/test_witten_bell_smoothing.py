# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/witten-bell-smoothing/. The authors are listed in prov/FME53F.jsonl.

import itertools
import random
from fractions import Fraction as F

import pytest

from witten_bell_smoothing import BOS, EOS, WittenBellLM

TOY = [["a", "b"], ["a", "c"], ["b", "c"]]


def test_toy_values() -> None:
    m = WittenBellLM(TOY, 2)
    assert m.distribution(()) == {EOS: F(4, 13), "a": F(3, 13), "b": F(3, 13), "c": F(3, 13)}
    assert m.distribution((BOS,)) == {EOS: F(8, 65), "a": F(32, 65), "b": F(19, 65), "c": F(6, 65)}
    assert m.prob("b", ["a"]) == F(19, 52)
    assert m.prob(EOS, ["c"]) == F(10, 13)
    assert m.sentence_prob(["a", "b", "c"]) == F(32, 65) * F(19, 52) * F(19, 52) * F(10, 13)
    assert m.sentence_prob(["b", "a"]) > 0


def test_unk_in_vocabulary() -> None:
    m = WittenBellLM(TOY, 2, vocab={"a", "b", "c", "<unk>"})
    assert m.prob("<unk>", ["a"]) == F(2, 65)
    assert sum(m.distribution(["a"]).values()) == 1


def test_errors() -> None:
    m = WittenBellLM(TOY, 2)
    with pytest.raises(KeyError):
        m.prob("z", ["a"])
    with pytest.raises(ValueError):
        WittenBellLM(TOY, 2, vocab={"a"})
    with pytest.raises(ValueError):
        WittenBellLM(TOY, 2, vocab={"a", "b", "c", BOS})
    with pytest.raises(ValueError):
        WittenBellLM(TOY, 0)


def direct_bigram(corpus, vocab):
    """The bigram formula written out, with counts found by a plain scan."""
    pairs, toks = [], []
    for s in corpus:
        x = [BOS] + s + [EOS]
        pairs += list(zip(x, x[1:]))
        toks += x[1:]
    n = len(toks)
    t0 = len(set(toks))

    def uni(w):
        return (toks.count(w) + F(t0, len(vocab))) / (n + t0)

    def bi(w, v):
        cv = sum(1 for p in pairs if p[0] == v)
        if cv == 0:
            return uni(w)
        tv = len({p[1] for p in pairs if p[0] == v})
        return (pairs.count((v, w)) + tv * uni(w)) / (cv + tv)

    return bi


def test_against_direct_formula() -> None:
    rng = random.Random(4)
    for _ in range(40):
        words = ["a", "b", "c", "d", "e"][: rng.randrange(2, 6)]
        corpus = [[rng.choice(words) for _ in range(rng.randrange(0, 5))] for _ in range(rng.randrange(1, 6))]
        vocab = set(words) | {EOS}
        m = WittenBellLM(corpus, 2, vocab=words)
        bi = direct_bigram(corpus, vocab)
        for v in [BOS] + words:
            for w in vocab:
                assert m.prob(w, [v]) == bi(w, v)


def test_rows_sum_to_one() -> None:
    rng = random.Random(9)
    for _ in range(60):
        n = rng.randrange(1, 4)
        words = ["a", "b", "c", "d"]
        corpus = [[rng.choice(words[:3]) for _ in range(rng.randrange(0, 6))] for _ in range(rng.randrange(1, 5))]
        m = WittenBellLM(corpus, n, vocab=words)
        for h in itertools.product([BOS] + words, repeat=n - 1):
            d = m.distribution(h)
            assert sum(d.values()) == 1
            assert all(0 < p <= 1 for p in d.values())


def test_short_sentences_have_mass_below_one() -> None:
    m = WittenBellLM(TOY, 2)
    total = F(0)
    for length in range(4):
        for s in itertools.product(["a", "b", "c"], repeat=length):
            total += m.sentence_prob(list(s))
    assert F(1, 2) < total < 1
