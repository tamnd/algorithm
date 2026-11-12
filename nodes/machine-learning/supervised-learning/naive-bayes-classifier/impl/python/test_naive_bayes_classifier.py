# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naive-bayes-classifier/. The authors are listed in prov/3AW3WK.jsonl.

import math
import random
from fractions import Fraction as F

import pytest

from naive_bayes_classifier import (
    BernoulliNB,
    GaussianNB,
    MultinomialNB,
    bernoulli_as_logistic,
    bernoulli_posterior_exact,
    log_sum_exp,
    multinomial_posterior_exact,
)

# Manning, Raghavan and Schutze, Introduction to Information Retrieval, Table 13.1.
DOCS = [s.split() for s in ["Chinese Beijing Chinese", "Chinese Chinese Shanghai", "Chinese Macao", "Tokyo Japan Chinese"]]
LABELS = ["china", "china", "china", "other"]
D5 = "Chinese Chinese Chinese Tokyo Japan".split()


def test_multinomial_hand_computed() -> None:
    # P(Chinese | china) = 6/14, P(Tokyo | china) = P(Japan | china) = 1/14,
    # and 2/9 for each of the three terms in class other.
    joint_c = F(3, 4) * F(3, 7) ** 3 * F(1, 14) ** 2
    joint_o = F(1, 4) * F(2, 9) ** 5
    want = joint_c / (joint_c + joint_o)
    assert want == F(4782969, 6934265)
    assert multinomial_posterior_exact(DOCS, LABELS, D5)["china"] == want
    m = MultinomialNB().fit(DOCS, LABELS)
    assert m.predict_proba(D5)["china"] == pytest.approx(float(want), rel=1e-12)
    assert math.exp(m.log_theta["china"]["Chinese"]) == pytest.approx(3 / 7)
    assert m.predict(D5) == "china"


def test_bernoulli_hand_computed() -> None:
    joint_c = F(3, 4) * F(4, 5) * F(1, 5) * F(1, 5) * (1 - F(2, 5)) ** 3
    joint_o = F(1, 4) * F(2, 3) ** 3 * (1 - F(1, 3)) ** 3
    want = joint_c / (joint_c + joint_o)
    assert bernoulli_posterior_exact(DOCS, LABELS, D5)["china"] == want
    b = BernoulliNB().fit(DOCS, LABELS)
    assert b.predict_proba(D5)["china"] == pytest.approx(float(want), rel=1e-12)
    assert b.predict(D5) == "other"


def test_exact_and_float_agree_on_random_corpora() -> None:
    rng = random.Random(3)
    words = list("abcdef")
    for _ in range(200):
        n = rng.randrange(2, 9)
        docs = [[rng.choice(words) for _ in range(rng.randrange(0, 6))] for _ in range(n)]
        labels = [rng.randrange(3) for _ in range(n)]
        if not any(docs):
            continue
        doc = [rng.choice(words + ["zz"]) for _ in range(rng.randrange(0, 8))]
        pm = MultinomialNB().fit(docs, labels).predict_proba(doc)
        for c, v in multinomial_posterior_exact(docs, labels, doc).items():
            assert pm[c] == pytest.approx(float(v), rel=1e-9, abs=1e-12)
        pb = BernoulliNB().fit(docs, labels).predict_proba(doc)
        for c, v in bernoulli_posterior_exact(docs, labels, doc).items():
            assert pb[c] == pytest.approx(float(v), rel=1e-9, abs=1e-12)


def test_bernoulli_is_a_logistic_model() -> None:
    b = BernoulliNB().fit(DOCS, LABELS)
    w, bias = bernoulli_as_logistic(b, "china", "other")
    rng = random.Random(4)
    for _ in range(50):
        doc = [t for t in b.vocab if rng.random() < 0.5]
        z = bias + sum(w[t] for t in doc)
        assert b.predict_proba(doc)["china"] == pytest.approx(1 / (1 + math.exp(-z)))


def test_log_space_avoids_underflow() -> None:
    docs = [["a"] * 3 + ["b"], ["b"] * 3 + ["a"]]
    m = MultinomialNB().fit(docs, [0, 1])
    long_doc = ["a"] * 1800 + ["b"] * 1200
    assert math.prod(math.exp(m.log_theta[0][t]) for t in long_doc) == 0.0
    p = m.predict_proba(long_doc)
    assert p[0] + p[1] == pytest.approx(1.0) and p[0] > 0.999


def test_smoothing_removes_zero_probabilities() -> None:
    m = MultinomialNB(alpha=1.0).fit([["a", "a"], ["b"]], [0, 1])
    assert math.exp(m.log_theta[0]["b"]) == pytest.approx(1 / 4)
    p = m.predict_proba(["a", "b"])
    assert 0 < p[0] < 1 and 0 < p[1] < 1


def test_gaussian_against_closed_form() -> None:
    xs = [(1.0, 2.0), (2.0, 1.0), (1.5, 1.5), (4.0, 5.0), (5.0, 4.0), (4.5, 5.5)]
    ys = [0, 0, 0, 1, 1, 1]
    g = GaussianNB(eps=0.0).fit(xs, ys)
    assert g.mean[1] == pytest.approx([4.5, 29 / 6])
    assert g.var[1] == pytest.approx([1 / 6, 7 / 18])

    def logpdf(x, mu, v):
        return -0.5 * math.log(2 * math.pi * v) - (x - mu) ** 2 / (2 * v)

    q = (3.0, 3.0)
    s = {c: math.log(0.5) + sum(logpdf(q[j], g.mean[c][j], g.var[c][j]) for j in range(2)) for c in (0, 1)}
    want = math.exp(s[1]) / (math.exp(s[0]) + math.exp(s[1]))
    assert g.predict_proba(q)[1] == pytest.approx(want)
    assert g.predict(q) == 1


def test_xor_cannot_be_learned() -> None:
    # Each feature is independent of the label, so naive Bayes sees no signal.
    b = BernoulliNB().fit([["a"], ["b"], ["a", "b"], []], [1, 1, 0, 0])
    for doc in (["a"], ["b"], ["a", "b"], []):
        assert b.predict_proba(doc)[1] == pytest.approx(0.5)


def test_log_sum_exp() -> None:
    assert log_sum_exp([-1000.0, -1000.0]) == pytest.approx(-1000 + math.log(2))
    assert log_sum_exp([-math.inf, -math.inf]) == -math.inf
