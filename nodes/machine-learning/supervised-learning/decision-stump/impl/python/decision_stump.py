# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/decision-stump/. The authors are listed in prov/H1E126.jsonl.

"""Exact weighted 0-1 loss minimization over decision stumps.

A stump is (j, theta, a, b): it predicts a when x[j] <= theta and b otherwise.
The constant stump has j = -1 and predicts a everywhere.
"""

from typing import Any, Hashable, NamedTuple, Sequence


class Stump(NamedTuple):
    error: Any  # the total weight of the misclassified examples
    j: int
    theta: Any
    a: Hashable
    b: Hashable

    def predict(self, x: Sequence[Any]) -> Hashable:
        if self.j < 0 or x[self.j] <= self.theta:
            return self.a
        return self.b


def _argmax(weights: dict) -> Hashable:
    # The class of largest weight; ties go to the smallest class key.
    return max(sorted(weights), key=lambda c: weights[c])


def best_stump(X: Sequence[Sequence[Any]], y: Sequence[Hashable], w: Sequence[Any] | None = None) -> Stump:
    """Return a stump of least weighted training error.

    Precondition: n >= 1, the rows of X have d features, the weights are >= 0,
    and the class labels can be sorted. Ties keep the first stump found: the
    constant stump, then features in order, then thresholds in increasing order.
    Cost: O(d n log n) comparisons for the sorts and O(d n k) arithmetic for
    the scan, with k the number of classes; O(n + k) extra memory.
    """
    n = len(y)
    if n == 0:
        raise ValueError("need at least one example")
    w = [1] * n if w is None else list(w)
    d = len(X[0])
    total = {}
    for yi, wi in zip(y, w):
        total[yi] = total.get(yi, 0) + wi
    W = sum(total.values())
    c0 = _argmax(total)
    best = Stump(W - total[c0], -1, None, c0, c0)  # @line L1
    for j in range(d):  # @line L2
        order = sorted(range(n), key=lambda i: X[i][j])  # @line L3
        left = {c: 0 for c in total}  # @line L4
        right = dict(total)  # @line L4
        for t in range(n - 1):  # @line L5
            i = order[t]
            left[y[i]] += w[i]  # @line L6
            right[y[i]] -= w[i]  # @line L6
            if X[i][j] < X[order[t + 1]][j]:  # @line L7
                a, b = _argmax(left), _argmax(right)
                e = (sum(left.values()) - left[a]) + (sum(right.values()) - right[b])  # @line L8
                if e < best.error:  # @line L9
                    best = Stump(e, j, X[i][j], a, b)  # @line L9
    return best  # @line L10


def weighted_error(s: Stump, X, y, w) -> Any:
    """The total weight of the examples that s gets wrong. Cost: O(n)."""
    return sum(wi for xi, yi, wi in zip(X, y, w) if s.predict(xi) != yi)
