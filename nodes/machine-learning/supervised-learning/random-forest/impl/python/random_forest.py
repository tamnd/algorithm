# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/random-forest/. The authors are listed in prov/N15Y9F.jsonl.
"""Random forest (Breiman 2001): CART trees grown on bootstrap samples, with m features
drawn at random at each node, combined by majority vote or by the average.

Data model: xs is a list of n rows of d real features, ys holds class labels (kind
"classification") or real targets (kind "regression"). A split sends x[k] <= thr left.
Also: out-of-bag (OOB) predictions and error, permutation importance, and the strength,
correlation and margin quantities of Theorem 2.3, computed on a finite sample.
"""

import math
import random
from typing import Optional, Sequence

Row = Sequence[float]


def default_mtry(d: int, kind: str) -> int:
    """The common defaults: floor(sqrt(d)) for classification, floor(d/3) for regression, at least 1."""
    return max(1, math.isqrt(d)) if kind == "classification" else max(1, d // 3)


def default_leaf_size(kind: str) -> int:
    return 1 if kind == "classification" else 5


def leaf_value(ys: Sequence, ids: Sequence[int], kind: str):
    if kind == "classification":  # majority class, ties to the smallest label
        counts: dict = {}
        for i in ids:
            counts[ys[i]] = counts.get(ys[i], 0) + 1
        return min(counts, key=lambda c: (-counts[c], c))
    return sum(ys[i] for i in ids) / len(ids)


def best_split_on(xs: Sequence[Row], ys: Sequence, ids: Sequence[int], k: int, kind: str,
                  n_leaf: int) -> Optional[tuple[float, float]]:
    """Return (cost, thr) of the CART split on feature k with the smallest child impurity.

    The cost is n_L Gini_L + n_R Gini_R (classification) or SSE_L + SSE_R (regression), so the
    smallest cost is the largest impurity decrease. Each child must have at least n_leaf rows.
    """
    order = sorted(ids, key=lambda i: xs[i][k])
    n = len(order)
    best: Optional[tuple[float, float]] = None
    if kind == "classification":
        right: dict = {}
        for i in order:
            right[ys[i]] = right.get(ys[i], 0) + 1
        left: dict = {}
        sq_l, sq_r = 0, sum(c * c for c in right.values())
    else:
        s_l = q_l = 0.0
        s_r, q_r = sum(ys[i] for i in order), sum(ys[i] ** 2 for i in order)
    for j in range(1, n):  # j rows go left
        y = ys[order[j - 1]]
        if kind == "classification":
            sq_l += 2 * left.get(y, 0) + 1
            left[y] = left.get(y, 0) + 1
            sq_r -= 2 * right[y] - 1
            right[y] -= 1
        else:
            s_l, q_l, s_r, q_r = s_l + y, q_l + y * y, s_r - y, q_r - y * y
        a, b = xs[order[j - 1]][k], xs[order[j]][k]
        if a == b or j < n_leaf or n - j < n_leaf:
            continue
        if kind == "classification":
            cost = (j - sq_l / j) + ((n - j) - sq_r / (n - j))
        else:
            cost = (q_l - s_l * s_l / j) + (q_r - s_r * s_r / (n - j))
        if best is None or cost < best[0] - 1e-12:
            best = (cost, (a + b) / 2)
    return best


def grow_tree(xs: Sequence[Row], ys: Sequence, sample: Sequence[int], kind: str, mtry: int, n_leaf: int,
              rng: random.Random) -> list:
    """Grow one unpruned tree. Nodes: ("leaf", value) or ("split", k, thr, left, right, candidates)."""
    d = len(xs[0])
    nodes: list = [None]
    stack = [(0, list(sample))]
    while stack:
        node, ids = stack.pop()
        if len(ids) < 2 * n_leaf or len(set(ys[i] for i in ids)) == 1:  # @line L5
            nodes[node] = ("leaf", leaf_value(ys, ids, kind))
            continue
        cand = rng.sample(range(d), mtry)  # @line L6
        best = None
        for k in cand:  # @line L7
            sp = best_split_on(xs, ys, ids, k, kind, n_leaf)
            if sp is not None and (best is None or sp[0] < best[0] - 1e-12):
                best = (sp[0], k, sp[1])
        if best is None:  # @line L8
            nodes[node] = ("leaf", leaf_value(ys, ids, kind))
            continue
        _, k, thr = best
        left, right = len(nodes), len(nodes) + 1
        nodes.extend([None, None])
        nodes[node] = ("split", k, thr, left, right, tuple(cand))  # @line L9
        stack.append((right, [i for i in ids if xs[i][k] > thr]))
        stack.append((left, [i for i in ids if xs[i][k] <= thr]))
    return nodes


def tree_predict(nodes: list, x: Row):
    node = nodes[0]
    while node[0] == "split":
        node = nodes[node[3]] if x[node[1]] <= node[2] else nodes[node[4]]
    return node[1]


def combine(values: Sequence, kind: str):
    """Majority vote (ties to the smallest label) or the average."""
    if kind == "classification":
        return leaf_value(values, range(len(values)), kind)
    return sum(values) / len(values)


def random_forest(xs: Sequence[Row], ys: Sequence, kind: str, n_trees: int, rng: random.Random,
                  mtry: Optional[int] = None, n_leaf: Optional[int] = None) -> list:
    """Return a list of (tree, in_bag) pairs, where in_bag is the set of rows of its bootstrap sample."""
    n, d = len(xs), len(xs[0])
    mtry = default_mtry(d, kind) if mtry is None else mtry
    n_leaf = default_leaf_size(kind) if n_leaf is None else n_leaf
    forest = []
    for _ in range(n_trees):  # @line L1
        sample = [rng.randrange(n) for _ in range(n)]  # @line L2
        tree = grow_tree(xs, ys, sample, kind, mtry, n_leaf, rng)  # @line L3
        forest.append((tree, frozenset(sample)))
    return forest


def predict(forest: list, x: Row, kind: str):
    return combine([tree_predict(t, x) for t, _ in forest], kind)  # @line L4


def oob_trees(forest: list, i: int) -> list:
    """The trees whose bootstrap sample does not contain row i."""
    return [t for t, in_bag in forest if i not in in_bag]


def oob_predict(forest: list, xs: Sequence[Row], i: int, kind: str):
    trees = oob_trees(forest, i)  # @line L10
    return combine([tree_predict(t, xs[i]) for t in trees], kind) if trees else None


def error(preds: Sequence, ys: Sequence, kind: str) -> float:
    if kind == "classification":
        return sum(p != y for p, y in zip(preds, ys)) / len(ys)
    return sum((p - y) ** 2 for p, y in zip(preds, ys)) / len(ys)


def oob_error(forest: list, xs: Sequence[Row], ys: Sequence, kind: str) -> float:
    """Error of the OOB predictions over the rows that are out of bag for at least one tree."""
    pairs = [(oob_predict(forest, xs, i, kind), ys[i]) for i in range(len(xs))]
    pairs = [(p, y) for p, y in pairs if p is not None]
    return error([p for p, _ in pairs], [y for _, y in pairs], kind)  # @line L11


def permutation_importance(forest: list, xs: Sequence[Row], ys: Sequence, kind: str,
                           rng: random.Random) -> list[float]:
    """For each feature k: the average over trees of the increase of the tree's OOB error
    when column k is permuted among the OOB rows of that tree (Breiman 2001, Section 10)."""
    n, d = len(xs), len(xs[0])
    imp = []
    for k in range(d):
        total, count = 0.0, 0
        for tree, in_bag in forest:
            oob = [i for i in range(n) if i not in in_bag]
            if not oob:
                continue
            base = error([tree_predict(tree, xs[i]) for i in oob], [ys[i] for i in oob], kind)
            col = [xs[i][k] for i in oob]
            rng.shuffle(col)  # @line L12
            rows = [tuple(v if j != k else c for j, v in enumerate(xs[i])) for i, c in zip(oob, col)]
            total += error([tree_predict(tree, r) for r in rows], [ys[i] for i in oob], kind) - base
            count += 1
        imp.append(total / count if count else 0.0)  # @line L13
    return imp


def strength_correlation(trees: Sequence[list], xs: Sequence[Row], ys: Sequence) -> dict:
    """The quantities of Breiman's Theorem 2.3 when Theta is uniform over the given trees and
    (X, Y) is uniform over the given rows. Returns s, rho_bar, the margin variance, PE* and the bound."""
    labels = sorted(set(ys) | {tree_predict(t, x) for t in trees for x in xs})
    m, p = len(trees), len(xs)
    h = [[tree_predict(t, x) for x in xs] for t in trees]
    mg, rmg = [], [[0.0] * p for _ in range(m)]
    for q in range(p):
        frac = {c: sum(h[t][q] == c for t in range(m)) / m for c in labels}
        others = [c for c in labels if c != ys[q]]
        jhat = min(others, key=lambda c: (-frac[c], c))
        mg.append(frac[ys[q]] - frac[jhat])
        for t in range(m):
            rmg[t][q] = float(h[t][q] == ys[q]) - float(h[t][q] == jhat)
    s = sum(mg) / p
    var_mg = sum((v - s) ** 2 for v in mg) / p
    mean = [sum(r) / p for r in rmg]
    sd = [math.sqrt(sum((v - mu) ** 2 for v in r) / p) for r, mu in zip(rmg, mean)]
    cov_sum = sum(sum((rmg[a][q] - mean[a]) * (rmg[b][q] - mean[b]) for q in range(p)) / p
                  for a in range(m) for b in range(m)) / (m * m)
    mean_sd = sum(sd) / m
    rho_bar = cov_sum / mean_sd ** 2 if mean_sd > 0 else 0.0
    return {"s": s, "var_mg": var_mg, "cov_sum": cov_sum, "mean_sd": mean_sd, "rho_bar": rho_bar,
            "mean_var": sum(v * v for v in sd) / m, "pe": sum(v < 0 for v in mg) / p,
            "bound": rho_bar * (1 - s * s) / (s * s) if s > 0 else math.inf}
