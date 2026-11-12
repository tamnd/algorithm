# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/gradient-boosting/. The authors are listed in prov/QJH6MQ.jsonl.
"""Gradient tree boosting (Friedman 2001, TreeBoost), with shrinkage and subsampling (Friedman 2002).

Two losses:
- "squared": l(y, F) = (y - F)^2 / 2. Pseudo-residual r = y - F. Leaf value: mean of r.
- "logistic": y in {0, 1}, p = 1 / (1 + exp(-F)), l = -y log p - (1 - y) log(1 - p).
  Pseudo-residual r = y - p. Leaf value: one Newton step, sum r / sum p (1 - p).

Each tree is a least squares regression tree fitted to the pseudo-residuals.
Its leaf values are then replaced by the per-leaf line search of the loss.
"""

import math
import random
from typing import Optional, Sequence

Point = Sequence[float]


def sigmoid(f: float) -> float:
    if f >= 0:
        return 1.0 / (1.0 + math.exp(-f))
    e = math.exp(f)
    return e / (1.0 + e)


def loss(kind: str, y: float, f: float) -> float:
    if kind == "squared":
        return 0.5 * (y - f) ** 2
    # log(1 + exp(f)) - y f, written to avoid overflow
    return max(f, 0.0) + math.log1p(math.exp(-abs(f))) - y * f


def mean_loss(kind: str, ys: Sequence[float], fs: Sequence[float]) -> float:
    return sum(loss(kind, y, f) for y, f in zip(ys, fs)) / len(ys)


def pseudo_residual(kind: str, y: float, f: float) -> float:
    """The negative derivative of the loss with respect to F."""
    return y - f if kind == "squared" else y - sigmoid(f)


def initial_value(kind: str, ys: Sequence[float]) -> float:
    """F_0 = argmin_c sum l(y_i, c)."""
    m = sum(ys) / len(ys)
    if kind == "squared":
        return m
    m = min(max(m, 1e-12), 1 - 1e-12)
    return math.log(m / (1 - m))


def best_split(xs: Sequence[Point], r: Sequence[float], idx: list[int], min_leaf: int) -> Optional[tuple[int, float, float]]:
    """The split (feature, threshold, SSE decrease) of least squared error on targets r, or None."""
    tot, cnt = sum(r[i] for i in idx), len(idx)
    best: Optional[tuple[int, float, float]] = None
    for f in range(len(xs[0])):
        order = sorted(idx, key=lambda i: xs[i][f])
        s = 0.0
        for k in range(1, cnt):
            s += r[order[k - 1]]
            if xs[order[k - 1]][f] == xs[order[k]][f] or k < min_leaf or cnt - k < min_leaf:
                continue
            # SSE decrease = sL^2/nL + sR^2/nR - s^2/n
            gain = s * s / k + (tot - s) ** 2 / (cnt - k) - tot * tot / cnt
            if gain > 1e-12 and (best is None or gain > best[2] + 1e-12):
                best = (f, (xs[order[k - 1]][f] + xs[order[k]][f]) / 2, gain)
    return best


def fit_tree(xs: Sequence[Point], r: Sequence[float], idx: list[int], max_depth: int, min_leaf: int = 1) -> tuple[list, list[list[int]]]:
    """A least squares tree on targets r over the examples idx. Iterative, with an explicit stack.

    Node list entries: ("split", f, thr, left, right) or ("leaf", leaf_number).
    Returns the nodes and the example indices of each leaf.
    """
    nodes: list = [None]
    leaves: list[list[int]] = []
    stack = [(0, idx, 0)]
    while stack:
        node, ids, depth = stack.pop()
        sp = best_split(xs, r, ids, min_leaf) if depth < max_depth else None
        if sp is None:
            nodes[node] = ("leaf", len(leaves))
            leaves.append(ids)
            continue
        f, thr, _ = sp
        left, right = len(nodes), len(nodes) + 1
        nodes.extend([None, None])
        nodes[node] = ("split", f, thr, left, right)
        stack.append((right, [i for i in ids if xs[i][f] > thr], depth + 1))
        stack.append((left, [i for i in ids if xs[i][f] <= thr], depth + 1))
    return nodes, leaves


def leaf_of(nodes: list, x: Point) -> int:
    node = nodes[0]
    while node[0] == "split":
        _, f, thr, left, right = node
        node = nodes[left] if x[f] <= thr else nodes[right]
    return node[1]


def leaf_value(kind: str, ys: Sequence[float], fs: Sequence[float], ids: list[int]) -> float:
    """The per-leaf line search: exact for squared loss, one Newton step for log loss."""
    if kind == "squared":
        return sum(ys[i] - fs[i] for i in ids) / len(ids)
    num = sum(ys[i] - sigmoid(fs[i]) for i in ids)
    den = sum(sigmoid(fs[i]) * (1 - sigmoid(fs[i])) for i in ids)
    return num / max(den, 1e-12)


class Model:
    def __init__(self, kind: str, f0: float, nu: float) -> None:
        self.kind, self.f0, self.nu = kind, f0, nu
        self.trees: list[tuple[list, list[float]]] = []

    def score(self, x: Point) -> float:
        return self.f0 + self.nu * sum(vals[leaf_of(nodes, x)] for nodes, vals in self.trees)


def gradient_boost(xs: Sequence[Point], ys: Sequence[float], kind: str, rounds: int, nu: float = 0.1, max_depth: int = 2,
                   subsample: float = 1.0, rng: Optional[random.Random] = None, trace: Optional[list] = None) -> Model:
    """Friedman's gradient tree boosting. trace, if given, gets one dict per round."""
    n = len(xs)
    model = Model(kind, initial_value(kind, ys), nu)
    fs = [model.f0] * n  # @line L1
    for _ in range(rounds):  # @line L2
        r = [pseudo_residual(kind, y, f) for y, f in zip(ys, fs)]  # @line L3
        if subsample < 1.0:  # @line L4
            ids = sorted((rng or random.Random(0)).sample(range(n), max(1, int(subsample * n))))
        else:
            ids = list(range(n))
        nodes, leaves = fit_tree(xs, r, ids, max_depth)  # @line L5
        vals = [leaf_value(kind, ys, fs, leaf) for leaf in leaves]  # @line L6
        model.trees.append((nodes, vals))
        fs = [f + nu * vals[leaf_of(nodes, x)] for f, x in zip(fs, xs)]  # @line L7
        if trace is not None:
            trace.append({"residuals": r, "ids": ids, "leaves": leaves, "values": vals, "loss": mean_loss(kind, ys, fs)})
    return model  # @line L8
