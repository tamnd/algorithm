# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/genie3/. The authors are listed in prov/NVTX2V.jsonl.
"""GENIE3: rank regulatory links by the importance of each gene in tree ensembles.

The expression data is a list of m genes, and each gene is a list of n samples
(floats). Genes are numbered 0 .. m-1. For each target gene j, the code scales
row j to unit variance, grows T regression trees that predict it from the
candidate regulators, and sums the importance of each regulator over the trees.

This is a small version of the method of Huynh-Thu et al. (2010). It keeps the
Random Forest variant (bootstrap samples and K random inputs at each node),
fully grown trees and the variance reduction importance. It leaves out the
Extra-Trees variant, the default of 1000 trees, parallel runs over targets,
and any filtering of the final list.

Random draws. All draws come from one random.Random passed in by the caller,
in this order: targets in index order; for each target, trees in order; for
each tree, first n calls rng.randrange(n) for the bootstrap sample (only when
bootstrap is on), then the nodes in depth-first order, left child first, with
one call rng.sample(inputs, K) at each node with at least min_split samples
and a positive sum of squares (only when K is less than the number of inputs).
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

Link = Tuple[int, int, float]


def scale_to_unit_variance(y: Sequence[float]) -> List[float]:
    """Divide y by its population standard deviation (a constant y is left as zeros)."""
    n = len(y)
    mean = sum(y) / n
    var = sum((v - mean) ** 2 for v in y) / n
    if var <= 0.0:
        return [0.0] * n
    sd = math.sqrt(var)
    return [v / sd for v in y]


def sum_of_squares(y: Sequence[float], idx: Sequence[int]) -> float:
    """Sum of squared deviations from the mean of y over the samples idx: #S * Var(S)."""
    if not idx:
        return 0.0
    mean = sum(y[s] for s in idx) / len(idx)
    return sum((y[s] - mean) ** 2 for s in idx)


def best_split(x: Sequence[Sequence[float]], y: Sequence[float], idx: Sequence[int], features: Sequence[int]):
    """Best threshold split of the samples idx over the given input rows.

    Returns (reduction, feature, threshold), or None if no feature takes two
    values on idx. The reduction is #S Var(S) - #L Var(L) - #R Var(R), which
    equals sL^2/nL + sR^2/nR - s^2/n for the sums s of y. Ties keep the first
    feature in the given order and the leftmost threshold.
    """
    n = len(idx)
    total = sum(y[s] for s in idx)
    base = total * total / n
    best = None
    for f in features:
        row = x[f]
        order = sorted(idx, key=lambda s: row[s])
        left = 0.0
        for pos in range(n - 1):
            left += y[order[pos]]
            a, b = row[order[pos]], row[order[pos + 1]]
            if a == b:
                continue
            nl = pos + 1
            right = total - left
            red = left * left / nl + right * right / (n - nl) - base
            if best is None or red > best[0]:
                best = (red, f, (a + b) / 2.0)
    return best


class Node:
    __slots__ = ("feature", "threshold", "left", "right", "value")

    def __init__(self, value: float):
        self.feature = -1
        self.threshold = 0.0
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.value = value


def grow_tree(rng, x, y, idx, inputs, k, importance: Dict[int, float], min_split: int = 2) -> Node:
    """Grow a regression tree on the samples idx (with repeats) and add to importance.

    A node is split when it has at least min_split samples, its sum of squares
    is positive and some candidate input takes two values on it.
    """
    node = Node(sum(y[s] for s in idx) / len(idx))
    if len(idx) < min_split or sum_of_squares(y, idx) <= 1e-12:
        return node
    feats = list(inputs) if k >= len(inputs) else rng.sample(list(inputs), k)
    split = best_split(x, y, idx, feats)  # @line L5
    if split is None:
        return node
    red, f, thr = split
    importance[f] = importance.get(f, 0.0) + red  # @line L6
    node.feature, node.threshold = f, thr
    node.left = grow_tree(rng, x, y, [s for s in idx if x[f][s] <= thr], inputs, k, importance, min_split)
    node.right = grow_tree(rng, x, y, [s for s in idx if x[f][s] > thr], inputs, k, importance, min_split)
    return node


def predict(node: Node, x: Sequence[Sequence[float]], s: int) -> float:
    """Prediction of the tree for sample s of the input rows x."""
    while node.left is not None:
        node = node.left if x[node.feature][s] <= node.threshold else node.right
    return node.value


def target_importances(rng, x, y, inputs, n_trees: int, k: int, bootstrap: bool = True) -> Dict[int, float]:
    """Mean over n_trees trees of the importance of each input for the target y."""
    n = len(y)
    total: Dict[int, float] = {f: 0.0 for f in inputs}
    for _ in range(n_trees):  # @line L3
        if bootstrap:
            idx = [rng.randrange(n) for _ in range(n)]  # @line L4
        else:
            idx = list(range(n))
        imp: Dict[int, float] = {}
        grow_tree(rng, x, y, idx, inputs, k, imp)
        for f, v in imp.items():
            total[f] += v
    return {f: v / n_trees for f, v in total.items()}


def genie3(
    rng,
    data: Sequence[Sequence[float]],
    n_trees: int = 50,
    k: Optional[int] = None,
    regulators: Optional[Sequence[int]] = None,
    bootstrap: bool = True,
) -> List[Link]:
    """Ranked list of links (regulator, target, weight), largest weight first.

    k is the number of inputs tried at each node; None means round(sqrt(p)),
    at least 1, for p candidate inputs. regulators restricts the candidate
    regulators (all genes by default). Ties in weight are ordered by
    (regulator, target).
    """
    m = len(data)
    regs = list(range(m)) if regulators is None else sorted(set(regulators))
    weights: List[Link] = []
    for j in range(m):  # @line L1
        y = scale_to_unit_variance(data[j])  # @line L2
        inputs = [i for i in regs if i != j]
        if not inputs:
            continue
        kk = max(1, round(math.sqrt(len(inputs)))) if k is None else k
        imp = target_importances(rng, data, y, inputs, n_trees, kk, bootstrap)
        for i in inputs:
            weights.append((i, j, imp[i]))
    weights.sort(key=lambda t: (-t[2], t[0], t[1]))  # @line L7
    return weights  # @line L8


def auroc(scores: Sequence[float], labels: Sequence[bool]) -> float:
    """Area under the ROC curve: the chance that a random positive outscores a random negative (ties count 1/2)."""
    pos = [s for s, l in zip(scores, labels) if l]
    neg = [s for s, l in zip(scores, labels) if not l]
    wins = 0.0
    for a in pos:
        for b in neg:
            wins += 1.0 if a > b else 0.5 if a == b else 0.0
    return wins / (len(pos) * len(neg))
