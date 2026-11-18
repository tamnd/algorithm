# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bpe-dropout/. The authors are listed in prov/ZZH1HW.jsonl.

import random
from fractions import Fraction

from bpe_dropout import bpe, distribution, segment, train_bpe

FREQ = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
MERGES = [("e", "s"), ("es", "t"), ("l", "o"), ("lo", "w"), ("e", "w"), ("ew", "est")]


def test_training_gives_the_page_merges():
    assert train_bpe(FREQ, 6) == MERGES
    assert bpe("lowest", MERGES) == ("low", "est")


def test_p_zero_is_bpe_and_p_one_is_characters():
    rng = random.Random(0)
    for w in ["lowest", "newer", "widest", "slow", "esteem"]:
        assert segment(w, MERGES, 0.0, rng) == bpe(w, MERGES)
        assert segment(w, MERGES, 1.0, rng) == tuple(w)
        assert distribution(w, MERGES, Fraction(0)) == {bpe(w, MERGES): 1}
        assert distribution(w, MERGES, Fraction(1)) == {tuple(w): 1}


def test_page_distribution_of_low():
    d = distribution("low", MERGES, Fraction(1, 10))
    assert d == {("low",): Fraction(81, 100), ("l", "o", "w"): Fraction(1, 10), ("lo", "w"): Fraction(9, 100)}


def test_page_distribution_of_lowest():
    d = distribution("lowest", MERGES, Fraction(1, 10))
    assert len(d) == 9 and sum(d.values()) == 1
    assert d[("low", "est")] == Fraction(807003, 1000000)
    assert d[("lo", "w", "est")] == Fraction(2187, 25000)
    assert d[("l", "o", "w", "est")] == Fraction(81, 1000)
    assert d[tuple("lowest")] == Fraction(1, 100)


def test_samples_follow_the_exact_law():
    rng = random.Random(42)
    n = 20000
    for w, p in [("lowest", 0.1), ("lowest", 0.5), ("newest", 0.3)]:
        exact = distribution(w, MERGES, Fraction(p).limit_denominator(100))
        counts = {}
        for _ in range(n):
            s = segment(w, MERGES, p, rng)
            counts[s] = counts.get(s, 0) + 1
        assert set(counts) <= set(exact)
        for s, q in exact.items():
            q = float(q)
            sd = (q * (1 - q) / n) ** 0.5
            assert abs(counts.get(s, 0) / n - q) <= 5 * sd + 1e-9


def test_overlapping_occurrences():
    merges = [("a", "a")]
    d = distribution("aaa", merges, Fraction(1, 2))
    # Both positions survive (1/4): merge the left one. Only the left (1/4) or
    # only the right (1/4) survives: merge it. None survives (1/4): stop.
    assert d == {("aa", "a"): Fraction(1, 2), ("a", "aa"): Fraction(1, 4), ("a", "a", "a"): Fraction(1, 4)}


def test_every_sample_is_a_segmentation_with_known_units():
    rng = random.Random(7)
    units = set("abc")
    corpus = {"".join(rng.choice("abc") for _ in range(rng.randint(2, 7))): rng.randint(1, 5) for _ in range(8)}
    merges = train_bpe(corpus, 10)
    units |= {a + b for a, b in merges}
    for _ in range(500):
        w = "".join(rng.choice("abc") for _ in range(rng.randint(1, 8)))
        s = segment(w, merges, rng.random(), rng)
        assert "".join(s) == w and set(s) <= units


def test_exact_law_sums_to_one_on_random_words():
    rng = random.Random(9)
    corpus = {"".join(rng.choice("ab") for _ in range(rng.randint(2, 6))): rng.randint(1, 5) for _ in range(6)}
    merges = train_bpe(corpus, 6)
    for _ in range(30):
        w = "".join(rng.choice("ab") for _ in range(rng.randint(1, 6)))
        p = Fraction(rng.randint(0, 10), 10)
        d = distribution(w, merges, p)
        assert sum(d.values()) == 1
        assert all("".join(s) == w for s in d)
