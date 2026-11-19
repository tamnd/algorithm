# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ibm-model-2/. The authors are listed in prov/Z3VPZP.jsonl.

import math
import random
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

from ibm_model_2 import (
    NULL,
    em_step,
    expected_counts,
    likelihood,
    log_likelihood,
    model1_t,
    train,
    uniform_a,
    uniform_t,
    viterbi_alignment,
)

KOEHN = [(["the", "house"], ["das", "Haus"]), (["the", "book"], ["das", "Buch"]), (["a", "book"], ["ein", "Buch"])]


def random_corpus(rng, n, vf, ve, lmax):
    return [([f"f{rng.randrange(vf)}" for _ in range(rng.randint(1, lmax))],
             [f"e{rng.randrange(ve)}" for _ in range(rng.randint(1, lmax))]) for _ in range(n)]


def normalize(d, group):
    tot = defaultdict(F)
    for k, v in d.items():
        tot[group(k)] += v
    return {k: v / tot[group(k)] for k, v in d.items()}


def random_tables(rng, corpus, null):
    t = {k: F(rng.randint(1, 9)) for k in uniform_t(corpus, null)}
    a = {k: F(rng.randint(1, 9)) for k in uniform_a(corpus, null)}
    return normalize(t, lambda k: k[1]), normalize(a, lambda k: k[1:])


def positions(l, null):
    return range(0 if null else 1, l + 1)


def brute(corpus, t, a, null):
    """Likelihood and expected counts by a sum over every alignment."""
    ct, ca, total = defaultdict(F), defaultdict(F), F(1)
    for f, e in corpus:
        l, m = len(e), len(f)
        es = [NULL] + list(e)
        joint = {}
        for al in product(positions(l, null), repeat=m):
            p = F(1)
            for j, i in enumerate(al, start=1):
                p *= a[(i, j, l, m)] * t[(f[j - 1], es[i])]
            joint[al] = p
        z = sum(joint.values())
        total *= z
        for al, p in joint.items():
            for j, i in enumerate(al, start=1):
                ct[(f[j - 1], es[i])] += p / z
                ca[(i, j, l, m)] += p / z
    return total, ct, ca


def nonzero(d):
    return {k: v for k, v in d.items() if v}


def test_e_step_against_all_alignments() -> None:
    rng = random.Random(21)
    for null in (False, True):
        corpus = random_corpus(rng, 3, 3, 3, 4)
        t, a = random_tables(rng, corpus, null)
        total, bt, ba = brute(corpus, t, a, null)
        ct, ca = expected_counts(corpus, t, a, null)
        assert nonzero(ct) == nonzero(bt)
        assert nonzero(ca) == nonzero(ba)
        assert likelihood(corpus, t, a, null) == total


def test_rows_sum_to_one_and_likelihood_never_decreases() -> None:
    rng = random.Random(22)
    for null in (False, True):
        corpus = random_corpus(rng, 3, 3, 3, 3)
        # exact: one Model 1 round and one Model 2 round (exact fractions grow long over many rounds)
        t, a, hist = train(corpus, 1, null, model1_rounds=1)
        assert all(y >= x for x, y in zip(hist, hist[1:]))
        for table, group in ((t, lambda k: k[1]), (a, lambda k: k[1:])):
            sums = defaultdict(F)
            for k, v in table.items():
                assert 0 <= v <= 1
                sums[group(k)] += v
            assert set(sums.values()) == {F(1)}
        # floats: ten rounds from a random start, with a tolerance for rounding
        tf, af = random_tables(rng, corpus, null)
        tf = {k: float(v) for k, v in tf.items()}
        af = {k: float(v) for k, v in af.items()}
        _, _, hist = train(corpus, 10, null, t=tf, a=af)
        assert all(y >= x * (1 - 1e-12) for x, y in zip(hist, hist[1:]))


def test_uniform_a_gives_model_1() -> None:
    # with a uniform, the first Model 2 round moves t exactly as Model 1 does
    t0, a0 = uniform_t(KOEHN), uniform_a(KOEHN)
    t1, a1 = em_step(KOEHN, t0, a0)
    assert t1 == model1_t(KOEHN, 1)
    assert t1[("the", "das")] == F(1, 2)
    t2 = model1_t(KOEHN, 2)
    assert t2[("the", "das")] == F(7, 11) and t2[("house", "Haus")] == F(4, 7)
    # Model 2 then learns positions: in every pair the first word goes with the first word
    t, a, hist = train(KOEHN, 3, model1_rounds=2)
    assert a[(1, 1, 2, 2)] > F(1, 2) and a[(2, 2, 2, 2)] > F(1, 2)
    assert all(y >= x for x, y in zip(hist, hist[1:]))
    assert hist[-1] > likelihood(KOEHN, t2, a0)


def test_not_concave() -> None:
    # one pair a b | x y: the diagonal and the crossed solutions both give likelihood 1,
    # and their midpoint gives 1/4, so the log likelihood is not concave in (t, a)
    corpus = [(["a", "b"], ["x", "y"])]
    one, zero = F(1), F(0)
    t_diag = {("a", "x"): one, ("b", "x"): zero, ("a", "y"): zero, ("b", "y"): one}
    t_cross = {("a", "x"): zero, ("b", "x"): one, ("a", "y"): one, ("b", "y"): zero}
    a_diag = {(1, 1, 2, 2): one, (2, 1, 2, 2): zero, (1, 2, 2, 2): zero, (2, 2, 2, 2): one}
    a_cross = {(1, 1, 2, 2): zero, (2, 1, 2, 2): one, (1, 2, 2, 2): one, (2, 2, 2, 2): zero}
    assert likelihood(corpus, t_diag, a_diag) == 1
    assert likelihood(corpus, t_cross, a_cross) == 1
    t_mid = {k: (t_diag[k] + t_cross[k]) / 2 for k in t_diag}
    a_mid = {k: (a_diag[k] + a_cross[k]) / 2 for k in a_diag}
    assert likelihood(corpus, t_mid, a_mid) == F(1, 4)
    # the midpoint is a fixed point of EM, and a small push decides which maximum EM reaches
    assert em_step(corpus, t_mid, a_mid) == (t_mid, a_mid)
    # (in floats: exact fractions grow too long over many rounds)
    for eps, want in ((0.05, [1, 2]), (-0.05, [2, 1])):
        t = {k: float(v) + (eps if k in (("a", "x"), ("b", "y")) else -eps) for k, v in t_mid.items()}
        t, a, hist = train(corpus, 30, t=t, a={k: float(v) for k, v in a_mid.items()})
        assert hist[-1] > 0.99
        assert viterbi_alignment(["a", "b"], ["x", "y"], t, a) == want


def test_viterbi_against_brute_force() -> None:
    rng = random.Random(23)
    for null in (False, True):
        corpus = random_corpus(rng, 5, 3, 3, 4)
        t, a = random_tables(rng, corpus, null)
        for f, e in corpus:
            l, m = len(e), len(f)
            es = [NULL] + list(e)

            def score(al):
                p = F(1)
                for j, i in enumerate(al, start=1):
                    p *= a[(i, j, l, m)] * t[(f[j - 1], es[i])]
                return p

            best = max(score(al) for al in product(positions(l, null), repeat=m))
            assert score(viterbi_alignment(f, e, t, a, null)) == best


def test_long_sentence_log_space() -> None:
    m = 200
    f = [f"f{j % 50}" for j in range(m)]
    e = [f"e{j % 50}" for j in range(m)]
    corpus = [(f, e)]
    t = {k: float(v) for k, v in uniform_t(corpus).items()}
    a = {k: float(v) for k, v in uniform_a(corpus).items()}
    per_word = [sum(a[(i, j, m, m)] * t[(f[j - 1], e[i - 1])] for i in range(1, m + 1)) for j in range(1, m + 1)]
    assert math.prod(per_word) == 0.0
    assert math.isclose(log_likelihood(corpus, t, a), -m * math.log(50), rel_tol=1e-12)
