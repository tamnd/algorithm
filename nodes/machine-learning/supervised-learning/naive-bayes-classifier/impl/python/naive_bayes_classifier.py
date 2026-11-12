# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/naive-bayes-classifier/. The authors are listed in prov/3AW3WK.jsonl.

"""Naive Bayes classifiers: multinomial, Bernoulli and Gaussian, computed in log space.

Each model stores log P(c) and per-class feature parameters. Scores are
log P(c) + sum of log P(feature | c); posteriors use the log-sum-exp trick.
Ties in the score go to the class that comes first in sorted order.
"""

import math
from collections import Counter
from fractions import Fraction
from typing import Hashable, Sequence


def log_sum_exp(xs: Sequence[float]) -> float:
    m = max(xs)
    if m == -math.inf:
        return m
    return m + math.log(sum(math.exp(x - m) for x in xs))


def _posteriors(scores: dict) -> dict:
    z = log_sum_exp(list(scores.values()))
    return {c: math.exp(s - z) for c, s in scores.items()}


def _argmax(scores: dict) -> Hashable:
    best = max(scores.values())
    return min(c for c in scores if scores[c] == best)


class MultinomialNB:
    """Documents are lists of tokens. alpha = 1 is Laplace (add-one) smoothing."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha

    def fit(self, docs: Sequence[Sequence[str]], labels: Sequence[Hashable]) -> "MultinomialNB":
        n = len(docs)
        self.vocab = sorted({t for d in docs for t in d})  # @line L1
        self.classes = sorted(set(labels))
        self.log_prior, self.log_theta = {}, {}
        for c in self.classes:  # @line L2
            members = [d for d, y in zip(docs, labels) if y == c]
            self.log_prior[c] = math.log(len(members) / n)  # @line L3
            counts = Counter(t for d in members for t in d)  # @line L4
            total = sum(counts.values()) + self.alpha * len(self.vocab)
            self.log_theta[c] = {  # @line L5
                t: math.log((counts[t] + self.alpha) / total) for t in self.vocab
            }
        return self

    def scores(self, doc: Sequence[str]) -> dict:
        out = {}
        for c in self.classes:  # @line L6
            out[c] = self.log_prior[c] + sum(
                self.log_theta[c][t] for t in doc if t in self.log_theta[c]
            )
        return out

    def predict_proba(self, doc: Sequence[str]) -> dict:
        return _posteriors(self.scores(doc))  # @line L7

    def predict(self, doc: Sequence[str]) -> Hashable:
        return _argmax(self.scores(doc))  # @line L8


class BernoulliNB:
    """Each document is the set of vocabulary terms present; absent terms count too."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha

    def fit(self, docs: Sequence[Sequence[str]], labels: Sequence[Hashable]) -> "BernoulliNB":
        n = len(docs)
        self.vocab = sorted({t for d in docs for t in d})
        self.classes = sorted(set(labels))
        self.log_prior, self.p = {}, {}
        for c in self.classes:
            members = [set(d) for d, y in zip(docs, labels) if y == c]
            self.log_prior[c] = math.log(len(members) / n)
            self.p[c] = {
                t: (sum(t in d for d in members) + self.alpha) / (len(members) + 2 * self.alpha)
                for t in self.vocab
            }
        return self

    def scores(self, doc: Sequence[str]) -> dict:
        present = set(doc)
        return {
            c: self.log_prior[c]
            + sum(math.log(self.p[c][t] if t in present else 1 - self.p[c][t]) for t in self.vocab)
            for c in self.classes
        }

    def predict_proba(self, doc: Sequence[str]) -> dict:
        return _posteriors(self.scores(doc))

    def predict(self, doc: Sequence[str]) -> Hashable:
        return _argmax(self.scores(doc))


class GaussianNB:
    """Real features; each feature is normal given the class, with its own mean and variance.
    The variance is the maximum likelihood estimate plus eps, which keeps it positive."""

    def __init__(self, eps: float = 1e-9) -> None:
        self.eps = eps

    def fit(self, xs: Sequence[Sequence[float]], labels: Sequence[Hashable]) -> "GaussianNB":
        n, d = len(xs), len(xs[0])
        self.classes = sorted(set(labels))
        self.log_prior, self.mean, self.var = {}, {}, {}
        for c in self.classes:
            rows = [x for x, y in zip(xs, labels) if y == c]
            m = len(rows)
            self.log_prior[c] = math.log(m / n)
            mu = [sum(r[j] for r in rows) / m for j in range(d)]
            self.mean[c] = mu
            self.var[c] = [sum((r[j] - mu[j]) ** 2 for r in rows) / m + self.eps for j in range(d)]
        return self

    def scores(self, x: Sequence[float]) -> dict:
        out = {}
        for c in self.classes:
            s = self.log_prior[c]
            for xj, mu, v in zip(x, self.mean[c], self.var[c]):
                s -= 0.5 * math.log(2 * math.pi * v) + (xj - mu) ** 2 / (2 * v)
            out[c] = s
        return out

    def predict_proba(self, x: Sequence[float]) -> dict:
        return _posteriors(self.scores(x))

    def predict(self, x: Sequence[float]) -> Hashable:
        return _argmax(self.scores(x))


def multinomial_posterior_exact(docs, labels, doc, alpha: int = 1) -> dict:
    """The multinomial naive Bayes posterior in exact rational arithmetic, by the product formula."""
    vocab = {t for d in docs for t in d}
    joint = {}
    for c in sorted(set(labels)):
        members = [d for d, y in zip(docs, labels) if y == c]
        counts = Counter(t for d in members for t in d)
        total = sum(counts.values()) + alpha * len(vocab)
        p = Fraction(len(members), len(docs))
        for t in doc:
            if t in vocab:
                p *= Fraction(counts[t] + alpha, total)
        joint[c] = p
    z = sum(joint.values())
    return {c: v / z for c, v in joint.items()}


def bernoulli_posterior_exact(docs, labels, doc, alpha: int = 1) -> dict:
    """The Bernoulli naive Bayes posterior in exact rational arithmetic."""
    vocab = {t for d in docs for t in d}
    present = set(doc)
    joint = {}
    for c in sorted(set(labels)):
        members = [set(d) for d, y in zip(docs, labels) if y == c]
        p = Fraction(len(members), len(docs))
        for t in vocab:
            q = Fraction(sum(t in d for d in members) + alpha, len(members) + 2 * alpha)
            p *= q if t in present else 1 - q
        joint[c] = p
    z = sum(joint.values())
    return {c: v / z for c, v in joint.items()}


def bernoulli_as_logistic(model: BernoulliNB, pos: Hashable, neg: Hashable) -> tuple[dict, float]:
    """Weights w and bias b with log P(pos | x) / P(neg | x) = b + sum of w_t over present t."""
    w, b = {}, model.log_prior[pos] - model.log_prior[neg]
    for t in model.vocab:
        p1, p0 = model.p[pos][t], model.p[neg][t]
        w[t] = math.log(p1 / p0) - math.log((1 - p1) / (1 - p0))
        b += math.log((1 - p1) / (1 - p0))
    return w, b
