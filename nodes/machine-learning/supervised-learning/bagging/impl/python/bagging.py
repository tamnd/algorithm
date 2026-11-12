# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bagging/. The authors are listed in prov/251C6Y.jsonl.
"""Bagging (Breiman 1996): fit a base learner on B bootstrap samples and average the
predictions (regression) or take a majority vote (classification). Also the out-of-bag
(OOB) predictions and error.

Data model: xs is a list of n inputs, ys a list of n labels. A base learner is a function
fit(xs, ys) that returns a predictor, a function from an input to a label.
"""

import random
from fractions import Fraction
from typing import Callable, Optional, Sequence

Learner = Callable[[Sequence, Sequence], Callable]


def bootstrap_sample(n: int, rng: random.Random) -> list[int]:
    """n indices drawn uniformly with replacement from range(n)."""
    return [rng.randrange(n) for _ in range(n)]


def expected_distinct_fraction(n: int) -> Fraction:
    """E[number of distinct indices in a bootstrap sample] / n = 1 - (1 - 1/n)^n, exactly."""
    return 1 - (1 - Fraction(1, n)) ** n


def combine(values: Sequence, kind: str):
    if kind == "classification":  # majority vote, ties to the smallest label
        counts: dict = {}
        for v in values:
            counts[v] = counts.get(v, 0) + 1
        return min(counts, key=lambda c: (-counts[c], c))
    return sum(values) / len(values)


def bag(xs: Sequence, ys: Sequence, fit: Learner, b: int, rng: random.Random) -> list:
    """Return a list of (predictor, in_bag) pairs, where in_bag is the set of indices of its sample."""
    n = len(xs)
    models = []
    for _ in range(b):  # @line L1
        idx = bootstrap_sample(n, rng)  # @line L2
        model = fit([xs[i] for i in idx], [ys[i] for i in idx])  # @line L3
        models.append((model, frozenset(idx)))
    return models


def predict(models: list, x, kind: str):
    return combine([f(x) for f, _ in models], kind)  # @line L4


def oob_predict(models: list, xs: Sequence, i: int, kind: str):
    """Combine only the models whose sample does not contain example i; None if there are none."""
    preds = [f(xs[i]) for f, in_bag in models if i not in in_bag]  # @line L5
    return combine(preds, kind) if preds else None


def oob_error(models: list, xs: Sequence, ys: Sequence, kind: str) -> Optional[float]:
    pairs = [(oob_predict(models, xs, i, kind), ys[i]) for i in range(len(xs))]
    pairs = [(p, y) for p, y in pairs if p is not None]
    if not pairs:
        return None
    if kind == "classification":
        return sum(p != y for p, y in pairs) / len(pairs)  # @line L6
    return sum((p - y) ** 2 for p, y in pairs) / len(pairs)


def fit_one_nn(xs: Sequence, ys: Sequence) -> Callable:
    """1-nearest neighbor on real inputs, an unstable base learner. Ties go to the first point."""
    pts = list(zip(xs, ys))
    return lambda x: min(pts, key=lambda p: abs(p[0] - x))[1]


def fit_stump(xs: Sequence, ys: Sequence) -> Callable:
    """A regression stump on real inputs: the split x <= t of least squared error, leaf means."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    best = (sum((y - sum(ys) / len(ys)) ** 2 for y in ys), None, sum(ys) / len(ys), sum(ys) / len(ys))
    for j in range(1, len(order)):
        a, b = xs[order[j - 1]], xs[order[j]]
        if a == b:
            continue
        left = [ys[i] for i in order[:j]]
        right = [ys[i] for i in order[j:]]
        ml, mr = sum(left) / len(left), sum(right) / len(right)
        sse = sum((y - ml) ** 2 for y in left) + sum((y - mr) ** 2 for y in right)
        if sse < best[0] - 1e-12:
            best = (sse, (a + b) / 2, ml, mr)
    _, t, ml, mr = best
    return (lambda x: ml) if t is None else (lambda x: ml if x <= t else mr)
