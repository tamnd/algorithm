# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/hmm-alignment-model/. The authors are listed in prov/S290AK.jsonl.

import math
import random
from collections import defaultdict
from itertools import product

from hmm_alignment_model import (
    NULL,
    count_update,
    em_step,
    expected_counts,
    forward_backward,
    jump_m_step,
    jump_objective,
    log_jump_row,
    log_likelihood,
    train,
    uniform_c,
    uniform_t,
    viterbi_alignment,
)


def random_corpus(rng, n, vf, ve, lmax):
    return [([f"f{rng.randrange(vf)}" for _ in range(rng.randint(1, lmax))],
             [f"e{rng.randrange(ve)}" for _ in range(rng.randint(1, lmax))]) for _ in range(n)]


def random_params(rng, corpus):
    t = {k: rng.random() + 0.05 for k in uniform_t(corpus)}
    tot = defaultdict(float)
    for (x, y), v in t.items():
        tot[y] += v
    t = {(x, y): v / tot[y] for (x, y), v in t.items()}
    c = {d: rng.random() + 0.05 for d in uniform_c(corpus)}
    return t, c


def joint(f, e, a, t, c, p0, null):
    """p(f, a | e) straight from the definition, with the remembered position r."""
    l = len(e)
    r, p = 0, 1.0
    for j, i in enumerate(a):
        if i == 0:
            if not null:
                return 0.0
            p *= p0 * t[(f[j], NULL)]
        else:
            z = sum(c[k - r] for k in range(1, l + 1))
            p *= (1 - p0) * c[i - r] / z * t[(f[j], e[i - 1])]
            r = i
    return p


def alignments(m, l, null):
    return product(range(0 if null else 1, l + 1), repeat=m)


def test_forward_and_posteriors_against_all_alignments() -> None:
    rng = random.Random(41)
    for null in (False, True):
        corpus = random_corpus(rng, 4, 3, 3, 4)
        t, c = random_params(rng, corpus)
        p0 = 0.2 if null else 0.0
        ct, nj = expected_counts(corpus, t, c, p0, null)
        bt = defaultdict(float)
        for f, e in corpus:
            ps = {a: joint(f, e, a, t, c, p0, null) for a in alignments(len(f), len(e), null)}
            z = sum(ps.values())
            assert math.isclose(forward_backward(f, e, t, c, p0, null)[2], math.log(z), rel_tol=1e-12)
            for a, p in ps.items():
                for j, i in enumerate(a):
                    bt[(f[j], e[i - 1] if i else NULL)] += p / z
        for k in set(ct) | set(bt):
            assert math.isclose(ct.get(k, 0.0), bt.get(k, 0.0), rel_tol=1e-9, abs_tol=1e-12)
        # every source word gives one unit to the link counts and one jump or null step
        assert math.isclose(sum(ct.values()), sum(len(f) for f, _ in corpus))


def test_rows_are_distributions() -> None:
    c = {d: 1.0 + 0.1 * d * d for d in range(-4, 6)}
    for null, p0 in ((False, 0.0), (True, 0.2)):
        for l in (1, 3, 5):
            for r in range(0, l + 1):
                row = log_jump_row(r, l, c, p0, null)
                assert math.isclose(sum(math.exp(v) for v in row.values()), 1.0, rel_tol=1e-12)


def test_viterbi_against_brute_force() -> None:
    rng = random.Random(42)
    for null in (False, True):
        corpus = random_corpus(rng, 6, 3, 3, 4)
        t, c = random_params(rng, corpus)
        p0 = 0.2 if null else 0.0
        for f, e in corpus:
            a, lp = viterbi_alignment(f, e, t, c, p0, null)
            best = max(joint(f, e, b, t, c, p0, null) for b in alignments(len(f), len(e), null))
            assert math.isclose(lp, math.log(best), rel_tol=1e-12)
            assert math.isclose(joint(f, e, tuple(a), t, c, p0, null), best, rel_tol=1e-12)


def test_likelihood_never_decreases() -> None:
    rng = random.Random(43)
    for null in (False, True):
        corpus = random_corpus(rng, 5, 4, 4, 4)
        t, c = random_params(rng, corpus)
        p0 = 0.2 if null else 0.0
        _, _, hist = train(corpus, 6, p0, null, t=t, c=c)
        assert all(y >= x - 1e-9 for x, y in zip(hist, hist[1:]))
        # the jump step never lowers its part of the expected complete-data log likelihood,
        # and it is at least as good as the plain count update
        _, nj = expected_counts(corpus, t, c, p0, null)
        _, c2 = em_step(corpus, t, c, p0, null)
        assert jump_objective(nj, c2) >= jump_objective(nj, c)
        assert jump_objective(nj, c2) >= jump_objective(nj, count_update(nj, c)) - 1e-12


def test_count_update_is_not_the_m_step() -> None:
    # from uniform t and c the posteriors of each row are uniform, so uniform c is optimal;
    # the count update favours small widths, which occur in more rows, and lowers the objective
    rng = random.Random(46)
    corpus = random_corpus(rng, 6, 4, 4, 5)
    t, c = uniform_t(corpus), uniform_c(corpus)
    _, nj = expected_counts(corpus, t, c, 0.2, True)
    q = jump_objective(nj, c)
    assert jump_objective(nj, count_update(nj, c)) < q - 1e-6
    assert math.isclose(jump_objective(nj, jump_m_step(nj, c)), q, rel_tol=1e-9)


def test_uniform_jumps_give_model_1() -> None:
    rng = random.Random(44)
    corpus = random_corpus(rng, 4, 3, 3, 4)
    t, _ = random_params(rng, corpus)
    c = uniform_c(corpus)
    for f, e in corpus:
        m1 = sum(math.log(sum(t[(x, y)] for y in e) / len(e)) for x in f)
        assert math.isclose(forward_backward(f, e, t, c, 0.0, False)[2], m1, rel_tol=1e-12)


def test_learns_short_forward_jumps() -> None:
    # a corpus where every word is translated in place, with the word pairs mixed up
    rng = random.Random(45)
    lex = {f"e{k}": f"f{k}" for k in range(6)}
    corpus = []
    for _ in range(12):
        e = [f"e{rng.randrange(6)}" for _ in range(rng.randint(2, 5))]
        corpus.append(([lex[y] for y in e], e))
    t, c, hist = train(corpus, 6, 0.2, True)
    assert max(c, key=c.get) == 1
    f, e = ["f3", "f1", "f1", "f4"], ["e3", "e1", "e1", "e4"]
    a, _ = viterbi_alignment(f, e, t, c, 0.2, True)
    assert a == [1, 2, 3, 4]


def test_long_sentence_log_space() -> None:
    # 200 source words of 50 types and a 4-word target: p(f | e) = 50^-200 underflows
    m = 200
    f = [f"f{j % 50}" for j in range(m)]
    e = ["e0", "e1", "e2", "e3"]
    corpus = [(f, e)]
    t, c = uniform_t(corpus), uniform_c(corpus)
    assert math.prod(sum(t[(x, y)] / len(e) for y in e) for x in f) == 0.0
    for null, p0 in ((False, 0.0), (True, 0.2)):
        _, _, logp = forward_backward(f, e, t, c, p0, null)
        assert math.isclose(logp, -m * math.log(50), rel_tol=1e-12)
