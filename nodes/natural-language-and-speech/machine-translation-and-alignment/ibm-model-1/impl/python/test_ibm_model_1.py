# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ibm-model-1/. The authors are listed in prov/Q63VWQ.jsonl.

import math
import random
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

from ibm_model_1 import (
    NULL,
    em_step,
    expected_counts,
    likelihood,
    log_likelihood,
    train,
    uniform_table,
    viterbi_alignment,
)

# Koehn's example: English (the generated side) given German, no null word.
KOEHN = [(["the", "house"], ["das", "Haus"]), (["the", "book"], ["das", "Buch"]), (["a", "book"], ["ein", "Buch"])]


def test_check_values() -> None:
    t, hist = train(KOEHN, 3)
    assert hist[0] == F(1, 4096)
    assert hist[1] == F(81, 16384)
    assert hist[2] == F(114511401, 17014071844)
    assert math.isclose(float(hist[2]), 0.0067304, rel_tol=1e-4)
    assert math.isclose(float(hist[3]), 0.0086974, rel_tol=1e-4)
    t1 = em_step(KOEHN, uniform_table(KOEHN))
    assert t1[("the", "das")] == F(1, 2) and t1[("house", "Haus")] == F(1, 2)
    t2 = em_step(KOEHN, t1)
    assert t2[("the", "das")] == F(7, 11) and t2[("book", "Buch")] == F(7, 11)
    assert t2[("house", "Haus")] == F(4, 7) and t2[("the", "Haus")] == F(3, 7)
    assert t2[("a", "ein")] == F(4, 7) and t2[("book", "ein")] == F(3, 7)
    for key in [("a", "Buch"), ("the", "Buch"), ("book", "das"), ("house", "das")]:
        assert t2[key] == F(2, 11)
    assert t[("the", "das")] == F(29435, 39357)
    assert t[("house", "Haus")] == F(164, 251)


def test_rows_sum_to_one() -> None:
    t, _ = train(KOEHN, 2, null=True)
    rows = defaultdict(F)
    for (x, y), v in t.items():
        rows[y] += v
        assert 0 <= v <= 1
    assert set(rows.values()) == {F(1)}
    assert NULL in rows


def brute_counts(corpus, t, null):
    """Expected link counts by a sum over all (l + 1)^m (or l^m) alignments."""
    c = defaultdict(F)
    for f, e in corpus:
        es = ([NULL] if null else []) + list(e)
        joint = {}
        for a in product(range(len(es)), repeat=len(f)):
            p = F(1)
            for j, i in enumerate(a):
                p *= t[(f[j], es[i])]
            joint[a] = p
        z = sum(joint.values())
        for a, p in joint.items():
            for j, i in enumerate(a):
                c[(f[j], es[i])] += p / z
    return c


def random_corpus(rng, n, vf, ve, lmax):
    return [([f"f{rng.randrange(vf)}" for _ in range(rng.randint(1, lmax))],
             [f"e{rng.randrange(ve)}" for _ in range(rng.randint(1, lmax))]) for _ in range(n)]


def random_table(rng, corpus, null):
    t = uniform_table(corpus, null)
    for key in t:
        t[key] = F(rng.randint(1, 9))
    rows = defaultdict(F)
    for (x, y), v in t.items():
        rows[y] += v
    return {(x, y): v / rows[y] for (x, y), v in t.items()}


def test_e_step_against_all_alignments() -> None:
    rng = random.Random(4)
    for null in (False, True):
        corpus = random_corpus(rng, 3, 3, 3, 4)
        t = random_table(rng, corpus, null)
        fast = expected_counts(corpus, t, null)
        slow = brute_counts(corpus, t, null)
        assert {k: v for k, v in fast.items() if v} == {k: v for k, v in slow.items() if v}
        # the likelihood is the sum over all alignments, divided by (l + 1)^m or l^m
        total = F(1)
        for f, e in corpus:
            es = ([NULL] if null else []) + list(e)
            s = F(0)
            for a in product(range(len(es)), repeat=len(f)):
                p = F(1)
                for j, i in enumerate(a):
                    p *= t[(f[j], es[i])]
                s += p
            total *= s / F(len(es)) ** len(f)
        assert likelihood(corpus, t, null) == total


def test_likelihood_never_decreases() -> None:
    rng = random.Random(9)
    for null in (False, True):
        corpus = random_corpus(rng, 4, 3, 3, 3)
        _, hist = train(corpus, 4, null)
        assert all(b >= a for a, b in zip(hist, hist[1:]))


def test_log_likelihood_is_concave() -> None:
    rng = random.Random(12)
    corpus = random_corpus(rng, 5, 4, 4, 4)
    for _ in range(20):
        t1, t2 = random_table(rng, corpus, True), random_table(rng, corpus, True)
        mid = {k: (t1[k] + t2[k]) / 2 for k in t1}
        lhs = log_likelihood(corpus, mid, True)
        rhs = (log_likelihood(corpus, t1, True) + log_likelihood(corpus, t2, True)) / 2
        assert lhs >= rhs - 1e-12


def test_maximizer_not_unique() -> None:
    # one pair (a b | x y): every t with t(a | x) = p, t(a | y) = 1 - p has likelihood 1/4,
    # the maximum, and EM does not move it, so the start decides the alignment
    corpus = [(["a", "b"], ["x", "y"])]
    for p in (F(1, 5), F(1, 2), F(4, 5)):
        t = {("a", "x"): p, ("b", "x"): 1 - p, ("a", "y"): 1 - p, ("b", "y"): p}
        assert likelihood(corpus, t) == F(1, 4)
        assert em_step(corpus, t) == t
    t_left = {("a", "x"): F(4, 5), ("b", "x"): F(1, 5), ("a", "y"): F(1, 5), ("b", "y"): F(4, 5)}
    t_right = {("a", "x"): F(1, 5), ("b", "x"): F(4, 5), ("a", "y"): F(4, 5), ("b", "y"): F(1, 5)}
    assert viterbi_alignment(["a", "b"], ["x", "y"], t_left) == [1, 2]
    assert viterbi_alignment(["a", "b"], ["x", "y"], t_right) == [2, 1]


def test_viterbi_and_null() -> None:
    t, _ = train(KOEHN, 3)
    assert viterbi_alignment(["the", "house"], ["das", "Haus"], t) == [1, 2]
    assert viterbi_alignment(["a", "book"], ["ein", "Buch"], t) == [1, 2]
    tn, _ = train(KOEHN, 3, null=True)
    assert viterbi_alignment(["the", "house"], ["das", "Haus"], tn, null=True) == [1, 2]


def test_long_sentence_log_space() -> None:
    m = 200
    f = [f"f{j % 50}" for j in range(m)]
    e = [f"e{j % 50}" for j in range(m)]
    t = uniform_table([(f, e)])
    tf = {k: float(v) for k, v in t.items()}
    per_word = [sum(tf[(x, y)] for y in e) / len(e) for x in f]
    assert math.prod(per_word) == 0.0
    assert math.isclose(log_likelihood([(f, e)], tf), -m * math.log(50), rel_tol=1e-12)
