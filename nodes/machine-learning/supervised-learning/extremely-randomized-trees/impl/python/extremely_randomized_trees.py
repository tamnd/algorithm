# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/extremely-randomized-trees/. The authors are listed in prov/ZH6FA9.jsonl.
"""Extremely randomized trees (Geurts, Ernst and Wehenkel 2006).

Data model: xs is a list of n rows of d real attributes, ys holds class labels (kind
"classification") or real outputs (kind "regression"). Each tree is grown on the whole
training set. At each node, K attributes are drawn among the non-constant ones, one cut
point is drawn uniformly at random for each, and the best of these K splits by the score
is kept. A split [a < c] sends the rows with x[a] < c to the left.
"""

import math
import random
from typing import Optional, Sequence

Row = Sequence[float]


def default_k(d: int, kind: str) -> int:
    """sqrt(d) rounded for classification, d for regression (the paper's defaults)."""
    return max(1, round(math.sqrt(d))) if kind == "classification" else d


def default_n_min(kind: str) -> int:
    return 2 if kind == "classification" else 5


def entropy(counts: Sequence[int]) -> float:
    n = sum(counts)
    return -sum(c / n * math.log(c / n) for c in counts if c)


def class_counts(ys: Sequence, ids: Sequence[int]) -> dict:
    out: dict = {}
    for i in ids:
        out[ys[i]] = out.get(ys[i], 0) + 1
    return out


def score(ys: Sequence, left: Sequence[int], right: Sequence[int], kind: str) -> float:
    """Classification: the normalized information gain 2 I / (H_c + H_s).
    Regression: the relative reduction of the variance of the output."""
    ids = list(left) + list(right)
    n = len(ids)
    if kind == "classification":
        h_c = entropy(list(class_counts(ys, ids).values()))
        h_s = entropy([len(left), len(right)])
        cond = sum(len(p) / n * entropy(list(class_counts(ys, p).values())) for p in (left, right))
        mutual = h_c - cond  # I = H_c - H(C | split)
        return 2 * mutual / (h_c + h_s)

    def var(p: Sequence[int]) -> float:
        mu = sum(ys[i] for i in p) / len(p)
        return sum((ys[i] - mu) ** 2 for i in p) / len(p)

    v = var(ids)
    return (v - len(left) / n * var(left) - len(right) / n * var(right)) / v


def pick_random_split(xs: Sequence[Row], ids: Sequence[int], a: int, rng: random.Random) -> float:
    """A cut point drawn uniformly between the smallest and largest value of a in the node.
    A draw equal to the smallest value would leave the left side empty, so it is drawn again."""
    lo = min(xs[i][a] for i in ids)
    hi = max(xs[i][a] for i in ids)
    while True:
        c = rng.uniform(lo, hi)  # @line L6
        if lo < c <= hi:
            return c


def leaf_value(ys: Sequence, ids: Sequence[int], kind: str):
    if kind == "classification":
        counts = class_counts(ys, ids)
        return min(counts, key=lambda c: (-counts[c], c))
    return sum(ys[i] for i in ids) / len(ids)


def build_tree(xs: Sequence[Row], ys: Sequence, kind: str, k: int, n_min: int, rng: random.Random) -> list:
    """Nodes: ("leaf", value, size) or ("split", a, c, left, right, candidates), where candidates
    is the list of (score, a, c) of the K random splits of the node."""
    d = len(xs[0])
    nodes: list = [None]
    stack = [(0, list(range(len(xs))))]  # the whole sample, no bootstrap
    while stack:
        node, ids = stack.pop()
        free = [a for a in range(d) if len({xs[i][a] for i in ids}) > 1]
        if len(ids) < n_min or not free or len({ys[i] for i in ids}) == 1:  # @line L4
            nodes[node] = ("leaf", leaf_value(ys, ids, kind), len(ids))
            continue
        chosen = rng.sample(free, min(k, len(free)))  # @line L5
        cands = []
        for a in chosen:
            c = pick_random_split(xs, ids, a, rng)
            left = [i for i in ids if xs[i][a] < c]
            right = [i for i in ids if xs[i][a] >= c]
            cands.append((score(ys, left, right, kind), a, c))
        best = max(cands, key=lambda t: t[0])  # @line L7
        _, a, c = best
        left_id, right_id = len(nodes), len(nodes) + 1
        nodes.extend([None, None])
        nodes[node] = ("split", a, c, left_id, right_id, cands)  # @line L8
        stack.append((right_id, [i for i in ids if xs[i][a] >= c]))
        stack.append((left_id, [i for i in ids if xs[i][a] < c]))
    return nodes


def tree_predict(nodes: list, x: Row):
    node = nodes[0]
    while node[0] == "split":
        node = nodes[node[3]] if x[node[1]] < node[2] else nodes[node[4]]
    return node[1]


def extra_trees(xs: Sequence[Row], ys: Sequence, kind: str, m: int, rng: random.Random,
                k: Optional[int] = None, n_min: Optional[int] = None) -> list:
    k = default_k(len(xs[0]), kind) if k is None else k
    n_min = default_n_min(kind) if n_min is None else n_min
    trees = []
    for _ in range(m):  # @line L1
        trees.append(build_tree(xs, ys, kind, k, n_min, rng))  # @line L2
    return trees


def predict(trees: list, x: Row, kind: str):
    votes = [tree_predict(t, x) for t in trees]  # @line L3
    if kind == "classification":
        return leaf_value(votes, range(len(votes)), kind)
    return sum(votes) / len(votes)
