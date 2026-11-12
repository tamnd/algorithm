# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/xgboost/. The authors are listed in prov/57E0E8.jsonl.
"""The tree learner of XGBoost (Chen and Guestrin 2016): second-order objective,
exact greedy split finding, and sparsity-aware default directions.

A missing feature value is None. For a node with gradient sums G, H:
  leaf weight      w* = -G / (H + lam)
  leaf objective      -G^2 / (2 (H + lam)) + gamma
  split gain       (G_L^2/(H_L+lam) + G_R^2/(H_R+lam) - G^2/(H+lam)) / 2 - gamma
The weighted quantile sketch (approximate split finding) is not implemented here.
"""

import math
from typing import Optional, Sequence

Row = Sequence[Optional[float]]


def grad_hess(kind: str, y: float, pred: float) -> tuple[float, float]:
    """First and second derivative of the loss in the prediction."""
    if kind == "squared":  # l = (y - pred)^2 / 2
        return pred - y, 1.0
    p = 1.0 / (1.0 + math.exp(-pred))  # log loss, y in {0, 1}, pred is the log-odds
    return p - y, p * (1 - p)


def leaf_weight(g: float, h: float, lam: float) -> float:
    return -g / (h + lam)


def leaf_objective(g: float, h: float, lam: float, gamma: float) -> float:
    """min over w of g w + (h + lam) w^2 / 2, plus gamma for the leaf."""
    return -g * g / (2 * (h + lam)) + gamma


def split_gain(gl: float, hl: float, gr: float, hr: float, lam: float, gamma: float) -> float:
    g, h = gl + gr, hl + hr
    return 0.5 * (gl * gl / (hl + lam) + gr * gr / (hr + lam) - g * g / (h + lam)) - gamma


def best_split(xs: Sequence[Row], g: Sequence[float], h: Sequence[float], ids: list[int], lam: float, gamma: float,
               min_child_weight: float = 0.0) -> Optional[tuple[float, int, float, bool]]:
    """Exact greedy split with default directions (Algorithms 1 and 3 of the paper).

    Returns (gain, feature, threshold, missing_go_left) of the largest gain, or None if no split has a positive gain.
    A present value v goes left when v <= threshold.
    """
    G, H = sum(g[i] for i in ids), sum(h[i] for i in ids)  # @line L7
    best: Optional[tuple[float, int, float, bool]] = None
    for f in range(len(xs[ids[0]])):  # @line L8
        present = sorted((i for i in ids if xs[i][f] is not None), key=lambda i: xs[i][f])  # @line L9
        if not present:
            continue
        n_miss = len(ids) - len(present)
        gm = G - sum(g[i] for i in present)  # gradient sums of the missing values
        hm = H - sum(h[i] for i in present)
        # Candidate k: the first k present values (in sorted order) are <= the threshold.
        # k = 0 and k = len(present) are useful only when some values are missing.
        gl = hl = 0.0  # @line L10
        for k in range(len(present) + 1):  # @line L11
            if k > 0:
                gl += g[present[k - 1]]  # @line L12
                hl += h[present[k - 1]]
            if 0 < k < len(present) and xs[present[k - 1]][f] == xs[present[k]][f]:
                continue  # no threshold between equal values
            if k == 0:
                thr = xs[present[0]][f] - 1.0
            elif k == len(present):
                thr = xs[present[-1]][f]
            else:
                thr = (xs[present[k - 1]][f] + xs[present[k]][f]) / 2
            for miss_left in (False, True):  # @line L13
                lg, lh = (gl + gm, hl + hm) if miss_left else (gl, hl)  # @line L14
                n_left = k + (n_miss if miss_left else 0)
                if n_left == 0 or n_left == len(ids):
                    continue
                if lh < min_child_weight or H - lh < min_child_weight:
                    continue
                gain = split_gain(lg, lh, G - lg, H - lh, lam, gamma)  # @line L15
                if gain > 1e-12 and (best is None or gain > best[0] + 1e-12):  # @line L16
                    best = (gain, f, thr, miss_left)
    return best  # @line L17


def goes_left(x: Row, f: int, thr: float, miss_left: bool) -> bool:
    return miss_left if x[f] is None else x[f] <= thr


def grow_tree(xs: Sequence[Row], g: Sequence[float], h: Sequence[float], max_depth: int, lam: float, gamma: float,
              min_child_weight: float = 0.0) -> list:
    """Grow one tree. Nodes: ("split", f, thr, miss_left, left, right) or ("leaf", w)."""
    nodes: list = [None]
    stack = [(0, list(range(len(xs))), 0)]
    while stack:
        node, ids, depth = stack.pop()
        sp = best_split(xs, g, h, ids, lam, gamma, min_child_weight) if depth < max_depth else None  # @line L4
        if sp is None:
            nodes[node] = ("leaf", leaf_weight(sum(g[i] for i in ids), sum(h[i] for i in ids), lam))  # @line L5
            continue
        _, f, thr, ml = sp
        left, right = len(nodes), len(nodes) + 1
        nodes.extend([None, None])
        nodes[node] = ("split", f, thr, ml, left, right)
        stack.append((right, [i for i in ids if not goes_left(xs[i], f, thr, ml)], depth + 1))
        stack.append((left, [i for i in ids if goes_left(xs[i], f, thr, ml)], depth + 1))
    return nodes


def tree_predict(nodes: list, x: Row) -> float:
    node = nodes[0]
    while node[0] == "split":
        _, f, thr, ml, left, right = node
        node = nodes[left] if goes_left(x, f, thr, ml) else nodes[right]
    return node[1]


def boost(xs: Sequence[Row], ys: Sequence[float], kind: str, rounds: int, eta: float = 0.3, max_depth: int = 3,
          lam: float = 1.0, gamma: float = 0.0, base: float = 0.0, min_child_weight: float = 0.0) -> list:
    """Additive training: each round grows a tree on (g_i, h_i) at the current predictions."""
    preds = [base] * len(xs)
    trees = []
    for _ in range(rounds):  # @line L1
        gh = [grad_hess(kind, y, p) for y, p in zip(ys, preds)]  # @line L2
        g, h = [a for a, _ in gh], [b for _, b in gh]
        tree = grow_tree(xs, g, h, max_depth, lam, gamma, min_child_weight)  # @line L3
        trees.append(tree)
        preds = [p + eta * tree_predict(tree, x) for p, x in zip(preds, xs)]  # @line L6
    return trees


def predict(trees: list, x: Row, eta: float = 0.3, base: float = 0.0) -> float:
    return base + eta * sum(tree_predict(t, x) for t in trees)
