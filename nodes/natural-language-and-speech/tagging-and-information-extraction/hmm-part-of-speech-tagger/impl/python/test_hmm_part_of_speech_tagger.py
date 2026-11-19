# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-part-of-speech-tagger/. The authors are listed in prov/GZMMN9.jsonl.

import math
import random
from fractions import Fraction
from itertools import product

import pytest

from hmm_part_of_speech_tagger import (BOS, EOS, HMMTagger, brute_force, deleted_interpolation,
                                       log_joint, tag_events, viterbi)

CORPUS = [
    ("the dog runs".split(), ["D", "N", "V"]),
    ("the old dog runs".split(), ["D", "J", "N", "V"]),
    ("dogs run".split(), ["N", "V"]),
    ("the runs".split(), ["D", "N"]),
    ("old dogs walk".split(), ["J", "N", "V"]),
]


def random_tables(rng, tags, vocab, m):
    """A random order m HMM: rows of positive weights normalized to 1."""
    states = list(product([BOS] + list(tags), repeat=m))
    trans = {}
    for h in states:
        ws = [rng.random() + 0.01 for _ in range(len(tags) + 1)]
        z = sum(ws)
        for t, w in zip(list(tags) + [EOS], ws):
            trans[(h, t)] = math.log(w / z)
    emit = {}
    for t in tags:
        ws = [rng.random() + 0.01 for _ in vocab]
        z = sum(ws)
        for v, w in zip(vocab, ws):
            emit[(v, t)] = math.log(w / z)
    return (lambda h, t: trans[(h, t)]), (lambda w, t: emit[(w, t)])


@pytest.mark.parametrize("m", [1, 2])
def test_viterbi_matches_brute_force(m):
    rng = random.Random(7 + m)
    vocab = ["a", "b", "c", "d"]
    for k in (1, 2, 3):
        tags = ["T%d" % i for i in range(k)]
        for n in range(1, 7):
            lt, le = random_tables(rng, tags, vocab, m)
            words = [rng.choice(vocab) for _ in range(n)]
            y, s = viterbi(words, tags, m, lt, le)
            yb, sb = brute_force(words, tags, m, lt, le)
            assert abs(s - sb) < 1e-9
            assert abs(log_joint(words, y, m, lt, le) - s) < 1e-9
            if n <= 2:
                assert y == yb


def test_viterbi_with_zero_emissions_matches_brute_force():
    rng = random.Random(3)
    tags = ["A", "B", "C"]
    vocab = ["x", "y"]
    lt, le0 = random_tables(rng, tags, vocab, 1)
    zero = {("x", "B"), ("y", "A")}

    def le(w, t):
        return -math.inf if (w, t) in zero else le0(w, t)

    for n in range(1, 7):
        for words in product(vocab, repeat=n):
            # Two orders of the same transitions give equal scores in exact
            # arithmetic, so compare scores and not the paths themselves.
            y, s = viterbi(list(words), tags, 1, lt, le)
            yb, sb = brute_force(list(words), tags, 1, lt, le)
            assert abs(s - sb) < 1e-9
            assert abs(log_joint(list(words), y, 1, lt, le) - s) < 1e-9


def test_tag_events_counts():
    ngram, hist, N = tag_events([["D", "N"]], 2)
    assert N == 3
    assert ngram[(BOS, BOS, "D")] == 1 and ngram[(BOS, "D", "N")] == 1 and ngram[("D", "N", EOS)] == 1
    assert ngram[("D",)] == 1 and ngram[(EOS,)] == 1
    assert hist[(BOS,)] == 1 and hist[(BOS, BOS)] == 1 and hist[("N",)] == 1 and hist[("D", "N")] == 1


def test_deleted_interpolation_hand_values():
    tags = [t for _, t in CORPUS]
    assert deleted_interpolation(tags, 1) == [Fraction(4, 19), Fraction(15, 19)]
    assert deleted_interpolation(tags, 2) == [Fraction(4, 19), Fraction(4, 19), Fraction(11, 19)]


def test_deleted_interpolation_brute_force():
    """Recompute the weights by deleting one occurrence of each trigram and re-estimating."""
    rng = random.Random(11)
    for _ in range(30):
        seqs = [[rng.choice("ABC") for _ in range(rng.randint(1, 5))] for _ in range(rng.randint(1, 6))]
        events = []
        for s in seqs:
            q = [BOS, BOS] + s + [EOS]
            events += [tuple(q[i - 2:i + 1]) for i in range(2, len(q))]
        lam = [0, 0, 0]
        for g in sorted(set(events)):
            c = events.count(g)
            rest = list(events)
            rest.remove(g)

            def est(order):
                if order == 0:
                    return Fraction(sum(1 for e in rest if e[2] == g[2]), len(rest)) if rest else Fraction(0)
                tail = g[2 - order:]
                den = sum(1 for e in rest if e[2 - order:2] == tail[:-1])
                num = sum(1 for e in rest if e[2 - order:] == tail)
                return Fraction(num, den) if den else Fraction(0)

            vals = [est(o) for o in (2, 1, 0)]
            lam[2 - vals.index(max(vals))] += c
        assert deleted_interpolation(seqs, 2) == [Fraction(x, sum(lam)) for x in lam]


@pytest.mark.parametrize("m", [1, 2])
def test_transition_rows_sum_to_one(m):
    """A row sums to 1 when every suffix of its history was seen; else it is deficient, as in TnT."""
    tagger = HMMTagger(CORPUS, m=m)
    full = 0
    for h in product([BOS] + tagger.tags, repeat=m):
        row = [tagger.trans(h, t) for t in tagger.tags + [EOS]]
        assert all(0 <= p <= 1 for p in row)
        if all(h[m - j:] in tagger.hist for j in range(1, m + 1)):
            assert sum(row) == 1
            full += 1
        else:
            assert sum(row) < 1
    assert full >= 4


def test_known_emissions_sum_to_one():
    tagger = HMMTagger(CORPUS, m=2)
    for t in tagger.tags:
        assert sum(Fraction(c, tagger.ft[t]) for (w, u), c in tagger.wt.items() if u == t) == 1


def test_suffix_model_is_a_distribution_and_uses_suffixes():
    corpus = [
        ("he is walking".split(), ["P", "A", "G"]),
        ("she is talking".split(), ["P", "A", "G"]),
        ("he was singing".split(), ["P", "A", "G"]),
        ("the talk".split(), ["D", "N"]),
        ("the walk".split(), ["D", "N"]),
    ]
    tagger = HMMTagger(corpus, m=2)
    for w in ("jumping", "xyz", "ing", "k"):
        d = tagger.suffix_dist(w)
        assert abs(sum(d.values()) - 1) < 1e-12
    assert max(tagger.suffix_dist("jumping").items(), key=lambda kv: kv[1])[0] == "G"
    assert tagger.tag("she was jumping".split()) == ["P", "A", "G"]


@pytest.mark.parametrize("m", [1, 2])
def test_trained_tagger_matches_brute_force(m):
    tagger = HMMTagger(CORPUS, m=m)
    for words in (["the", "dog", "runs"], ["the", "runs"], ["old", "dogs", "run"], ["the", "cat", "runs"]):
        y = tagger.tag(words)
        yb, _ = brute_force(words, tagger.tags, m, tagger.log_trans, tagger.log_emit)
        assert y == yb


def test_trained_tagger_on_training_sentences():
    tagger = HMMTagger(CORPUS, m=2)
    for words, tags in CORPUS:
        assert tagger.tag(words) == tags


def test_underflow():
    rng = random.Random(5)
    tags = ["A", "B", "C"]
    vocab = ["a", "b", "c", "d"]
    lt, le = random_tables(rng, tags, vocab, 1)
    words = [rng.choice(vocab) for _ in range(400)]
    y, s = viterbi(words, tags, 1, lt, le)
    p = 1.0
    h = (BOS,)
    for w, t in zip(words, y):
        p *= math.exp(lt(h, t)) * math.exp(le(w, t))
        h = (t,)
    p *= math.exp(lt(h, EOS))
    assert p == 0.0
    assert math.isfinite(s) and s < -745
    assert abs(log_joint(words, y, 1, lt, le) - s) < 1e-6


def test_errors():
    with pytest.raises(ValueError):
        viterbi([], ["A"], 1, lambda h, t: 0.0, lambda w, t: 0.0)
    with pytest.raises(ValueError):
        viterbi(["x"], ["A"], 1, lambda h, t: 0.0, lambda w, t: -math.inf)
    with pytest.raises(ValueError):
        HMMTagger(CORPUS, m=0)
