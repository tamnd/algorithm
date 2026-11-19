# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fast-align/. The authors are listed in prov/NW40F8.jsonl.

import math
import random
from collections import defaultdict
from itertools import product

from fast_align import (
    NULL,
    distortion,
    em_step,
    expected_h,
    geo,
    h,
    log_likelihood,
    partition,
    partition_direct,
    train,
    viterbi_alignment,
)


def test_partition_closed_form() -> None:
    for m in range(1, 9):
        for l in range(1, 9):
            for j in range(1, m + 1):
                for lam in (0.0, 1e-7, 0.3, 4.0, 25.0):
                    assert math.isclose(partition(j, m, l, lam), partition_direct(j, m, l, lam), rel_tol=1e-9)


def test_partition_term_count() -> None:
    # above the diagonal point there are l - i_up terms; with one term fewer the last one is lost
    j, m, l, lam = 2, 5, 7, 4.0
    i_up = j * l // m
    lower = geo(math.exp(lam * h(i_up, j, m, l)), -lam / l, i_up)
    short = lower + geo(math.exp(lam * h(i_up + 1, j, m, l)), -lam / l, l - i_up - 1)
    assert not math.isclose(short, partition_direct(j, m, l, lam), rel_tol=1e-6)
    assert math.isclose(short + math.exp(lam * h(l, j, m, l)), partition_direct(j, m, l, lam), rel_tol=1e-12)


def test_expected_h() -> None:
    for m, l, j in [(1, 1, 1), (3, 5, 2), (6, 4, 6), (7, 7, 3), (2, 9, 1)]:
        for lam in (0.0, 0.5, 4.0, 30.0):
            z = partition_direct(j, m, l, lam)
            direct = sum(h(i, j, m, l) * math.exp(lam * h(i, j, m, l)) for i in range(1, l + 1)) / z
            assert math.isclose(expected_h(j, m, l, lam), direct, rel_tol=1e-9, abs_tol=1e-12)
            # it is the derivative of ln Z
            eps = 1e-6
            num = (math.log(partition(j, m, l, lam + eps)) - math.log(partition(j, m, l, lam + 2 * eps))) / -eps
            assert math.isclose(expected_h(j, m, l, lam + 1.5 * eps), num, rel_tol=1e-4, abs_tol=1e-7)


def test_distortion_sums_to_one() -> None:
    for m, l in [(1, 1), (4, 3), (5, 8)]:
        for j in range(1, m + 1):
            assert math.isclose(sum(distortion(i, j, m, l, 4.0, 0.08) for i in range(l + 1)), 1.0, rel_tol=1e-12)
    # lam = 0 gives a uniform distortion over the real words, as in Model 1
    assert all(math.isclose(distortion(i, 2, 3, 4, 0.0, 0.08), 0.92 / 4) for i in range(1, 5))


def random_corpus(rng: random.Random, n: int, vf: int, ve: int, lmax: int):
    out = []
    for _ in range(n):
        m, l = rng.randint(1, lmax), rng.randint(1, lmax)
        out.append(([f"f{rng.randrange(vf)}" for _ in range(m)], [f"e{rng.randrange(ve)}" for _ in range(l)]))
    return out


def test_e_step_against_all_alignments() -> None:
    rng = random.Random(3)
    corpus = random_corpus(rng, 4, 3, 3, 3)
    vf = sorted({x for f, _ in corpus for x in f})
    ve = sorted({y for _, e in corpus for y in e}) + [NULL]
    theta = {(x, y): rng.uniform(0.1, 1.0) for x in vf for y in ve}
    for y in ve:
        s = sum(theta[(x, y)] for x in vf)
        for x in vf:
            theta[(x, y)] /= s
    lam, p0 = 2.5, 0.08
    counts = defaultdict(float)
    for f, e in corpus:
        m, l, es = len(f), len(e), [NULL] + e
        joint = {}
        for a in product(range(l + 1), repeat=m):
            p = 1.0
            for j in range(1, m + 1):
                p *= distortion(a[j - 1], j, m, l, lam, p0) * theta[(f[j - 1], es[a[j - 1]])]
            joint[a] = p
        z = sum(joint.values())
        for a, p in joint.items():
            for j in range(1, m + 1):
                counts[(f[j - 1], es[a[j - 1]])] += p / z
    totals = defaultdict(float)
    for (x, y), c in counts.items():
        totals[y] += c
    new_theta, new_lam = em_step(corpus, theta, lam, p0, optimize_lambda=False)
    assert new_lam == lam
    for key, c in counts.items():
        assert math.isclose(new_theta[key], c / totals[key[1]], rel_tol=1e-9)
    # the likelihood is the log of the sum over all alignments
    brute = 0.0
    for f, e in corpus:
        m, l, es = len(f), len(e), [NULL] + e
        s = 0.0
        for a in product(range(l + 1), repeat=m):
            p = 1.0
            for j in range(1, m + 1):
                p *= distortion(a[j - 1], j, m, l, lam, p0) * theta[(f[j - 1], es[a[j - 1]])]
            s += p
        brute += math.log(s)
    assert math.isclose(log_likelihood(corpus, theta, lam, p0), brute, rel_tol=1e-12)


def test_likelihood_never_decreases() -> None:
    rng = random.Random(11)
    for _ in range(3):
        corpus = random_corpus(rng, 8, 5, 5, 6)
        _, _, hist = train(corpus, iterations=6)
        for a, b in zip(hist, hist[1:]):
            assert b >= a - 1e-9


def test_diagonal_corpus() -> None:
    # word k of e translates to word k of f, in the same order
    rng = random.Random(5)
    corpus = []
    for _ in range(30):
        n = rng.randint(3, 7)
        ids = [rng.randrange(6) for _ in range(n)]
        corpus.append(([f"f{k}" for k in ids], [f"e{k}" for k in ids]))
    theta, lam, hist = train(corpus, iterations=5)
    assert lam > 4.0
    f, e = ["f1", "f1", "f2", "f1"], ["e1", "e1", "e2", "e1"]
    assert viterbi_alignment(f, e, theta, lam) == [1, 2, 3, 4]
    # without the tension every f1 goes to the first e1
    assert viterbi_alignment(f, e, theta, 0.0) == [1, 1, 3, 1]


def test_lambda_fixed_option() -> None:
    corpus = [(["a", "b"], ["x", "y"])]
    _, lam, _ = train(corpus, iterations=2, lam=4.0, optimize_lambda=False)
    assert lam == 4.0


def test_long_sentence_no_underflow() -> None:
    # with theta uniform over 50 source words, each position has probability 1/50
    m = 200
    f = [f"f{j % 50}" for j in range(m)]
    e = [f"e{j % 50}" for j in range(m)]
    theta, lam, hist = train([(f, e)], iterations=0)
    probs = []
    for j in range(1, m + 1):
        probs.append(sum(distortion(i, j, m, m, lam, 0.08) * theta.get((f[j - 1], ([NULL] + e)[i]), 0.0)
                         for i in range(m + 1)))
    assert math.prod(probs) == 0.0
    assert math.isclose(hist[0], -m * math.log(50), rel_tol=1e-12)
