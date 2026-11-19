# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/minimum-risk-training/. The authors are listed in prov/1GGJMF.jsonl.

import itertools
import math
import random

import pytest

from minimum_risk_training import corpus_risk, dedupe, risk_and_gradient

VOCAB = ["a", "b", "c"]


def toy_logp(theta, y):
    """log P(y) for a toy model with an independent softmax over VOCAB at each position."""
    total = 0.0
    for t, w in enumerate(y):
        row = theta[t]
        m = max(row)
        z = m + math.log(sum(math.exp(v - m) for v in row))
        total += row[VOCAB.index(w)] - z
    return total


def toy_dlogp(theta, y):
    """d log P(y) / d theta, row by row."""
    out = []
    for t, w in enumerate(y):
        row = theta[t]
        m = max(row)
        e = [math.exp(v - m) for v in row]
        z = sum(e)
        out.append([(1.0 if VOCAB[j] == w else 0.0) - e[j] / z for j in range(len(row))])
    return out


def hamming(y, ref):
    return sum(1 for a, b in zip(y, ref) if a != b) / len(ref)


def test_page_example():
    logp = [math.log(0.5), math.log(0.3), math.log(0.2)]
    loss = [0.0, 0.5, 1.0]
    r, q, g = risk_and_gradient(logp, loss, 1.0)
    assert abs(r - 0.35) < 1e-12
    assert all(abs(a - b) < 1e-12 for a, b in zip(q, [0.5, 0.3, 0.2]))
    assert all(abs(a - b) < 1e-12 for a, b in zip(g, [-0.175, 0.045, 0.13]))
    r, q, _ = risk_and_gradient(logp, loss, 0.5)
    assert [round(x, 4) for x in q] == [0.4154, 0.3218, 0.2628]
    assert round(r, 4) == 0.4237


def test_full_subset_with_alpha_one_is_expected_loss():
    rng = random.Random(1683)
    for _ in range(20):
        theta = [[rng.uniform(-2, 2) for _ in VOCAB] for _ in range(2)]
        ref = ("a", "b")
        ys = list(itertools.product(VOCAB, repeat=2))
        logp = [toy_logp(theta, y) for y in ys]
        loss = [hamming(y, ref) for y in ys]
        r, q, _ = risk_and_gradient(logp, loss, 1.0)
        assert abs(sum(math.exp(x) for x in logp) - 1) < 1e-12
        want = sum(math.exp(lp) * d for lp, d in zip(logp, loss))
        assert abs(r - want) < 1e-12
        assert all(abs(a - math.exp(b)) < 1e-12 for a, b in zip(q, logp))


def test_gradient_by_finite_differences():
    rng = random.Random(5)
    h = 1e-6
    for _ in range(5):
        theta = [[rng.uniform(-1, 1) for _ in VOCAB] for _ in range(3)]
        ref = ("c", "a", "b")
        samples = [tuple(rng.choice(VOCAB) for _ in range(3)) for _ in range(8)]
        cands = dedupe(samples)
        loss = [hamming(y, ref) for y in cands]
        alpha = rng.choice([0.005, 0.5, 1.0, 3.0])

        def risk():
            return risk_and_gradient([toy_logp(theta, y) for y in cands], loss, alpha)[0]

        _, _, g = risk_and_gradient([toy_logp(theta, y) for y in cands], loss, alpha)
        grad = [[0.0] * len(VOCAB) for _ in range(3)]
        for gk, y in zip(g, cands):
            d = toy_dlogp(theta, y)
            for t in range(3):
                for j in range(len(VOCAB)):
                    grad[t][j] += gk * d[t][j]
        for t in range(3):
            for j in range(len(VOCAB)):
                old = theta[t][j]
                theta[t][j] = old + h
                up = risk()
                theta[t][j] = old - h
                down = risk()
                theta[t][j] = old
                assert abs((up - down) / (2 * h) - grad[t][j]) < 1e-5


def test_shift_invariance_and_zero_sum():
    rng = random.Random(9)
    for _ in range(50):
        n = rng.randint(1, 8)
        logp = [rng.uniform(-30, 0) for _ in range(n)]
        loss = [rng.random() for _ in range(n)]
        alpha = rng.uniform(0.01, 2)
        r1, _, g = risk_and_gradient(logp, loss, alpha)
        r2, _, _ = risk_and_gradient([x - 7.5 for x in logp], loss, alpha)
        assert abs(r1 - r2) < 1e-12
        assert abs(sum(g)) < 1e-12
        assert min(loss) - 1e-12 <= r1 <= max(loss) + 1e-12


def test_alpha_limits():
    logp = [-1.0, -2.0, -4.0]
    loss = [0.6, 0.2, 0.9]
    # a large alpha puts all the mass on the most probable candidate
    assert abs(risk_and_gradient(logp, loss, 200.0)[0] - 0.6) < 1e-12
    # a small alpha makes Q nearly uniform
    assert abs(risk_and_gradient(logp, loss, 1e-9)[0] - sum(loss) / 3) < 1e-8


def test_no_underflow():
    # the probabilities exp(-2000) underflow to 0 in double precision
    logp = [-2000.0, -2001.0]
    assert math.exp(logp[0]) == 0.0
    r, q, _ = risk_and_gradient(logp, [0.0, 1.0], 1.0)
    want = 1 / (1 + math.e)
    assert abs(r - want) < 1e-12 and abs(q[1] - want) < 1e-12


def test_corpus_and_helpers():
    batch = [([-1.0, -2.0], [0.0, 1.0]), ([-0.5], [0.3])]
    total, grads = corpus_risk(batch, 1.0)
    r0 = risk_and_gradient(*batch[0], 1.0)[0]
    assert abs(total - (r0 + 0.3)) < 1e-12 and grads[1] == [0.0]
    assert dedupe([["a"], ["b"], ["a"]]) == [("a",), ("b",)]
    with pytest.raises(ValueError):
        risk_and_gradient([], [], 1.0)
    with pytest.raises(ValueError):
        risk_and_gradient([0.0], [1.0], 0.0)
