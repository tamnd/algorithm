# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cost-complexity-pruning/. The authors are listed in prov/V06HEB.jsonl.

"""Minimal cost-complexity pruning (Breiman et al. 1984, Chapter 3).

A tree is made of Node objects; node.risk is R(t), the risk of t as a leaf
(misclassified cases, or the sum of squared errors), and node.children is
empty for a leaf. A pruned subtree is described by a set `cut` of node ids
that are made leaves. R_alpha(T) = sum of R over the leaves + alpha * leaves.

The module also has a small least-squares regression tree grower, used to
choose alpha by V-fold cross-validation.
"""

import random
from fractions import Fraction
from math import sqrt


class Node:
    __slots__ = ("id", "risk", "children", "value", "feature", "threshold")

    def __init__(self, risk, children=(), value=None, feature=None, threshold=None):
        self.id = 0
        self.risk, self.children = risk, list(children)
        self.value, self.feature, self.threshold = value, feature, threshold

    def is_leaf(self) -> bool:
        return not self.children


def number(root: Node) -> list:
    """Give the nodes preorder ids and return them in preorder."""
    out, stack = [], [root]
    while stack:
        t = stack.pop()
        t.id = len(out)
        out.append(t)
        stack.extend(reversed(t.children))
    return out


def smallest_optimal(root: Node, alpha) -> tuple:
    """(min R_alpha, cut) for the smallest pruned subtree T(alpha) that minimizes
    R_alpha: C(t) = min(R(t) + alpha, sum of C over the children), and t is
    made a leaf when R(t) + alpha <= that sum. Cost: O(|T|)."""
    cut: set = set()

    def c(t: Node):
        if t.is_leaf():
            return t.risk + alpha
        below = sum((c(u) for u in t.children), 0)
        if t.risk + alpha <= below:
            cut.add(t.id)
            return t.risk + alpha
        return below

    return c(root), cut


def _scan(t: Node, cut: set, g: dict) -> tuple:
    """(R(T_t), leaves of T_t) in the pruned tree, and g(t) for each internal node."""
    if t.is_leaf() or t.id in cut:
        return t.risk, 1
    r, k = 0, 0
    for u in t.children:
        a, b = _scan(u, cut, g)
        r, k = r + a, k + b
    g[t.id] = Fraction(t.risk - r) / (k - 1)
    return r, k


def weakest_link(root: Node) -> list:
    """The sequence [(alpha_1, cut_1), ..., (alpha_K, cut_K)] with alpha_1 = 0,
    T_1 = T(0), and T_K the root alone. Precondition: R(t) >= R(T_t) for each
    node (true for resubstitution risks). Cost: O(|T|) per step, O(|T|^2) in all."""
    cut: set = set()
    branch: dict = {}
    for t in reversed(number(root)):  # @line L1
        if t.is_leaf():  # @line L1
            branch[t.id] = t.risk  # @line L1
        else:  # @line L1
            branch[t.id] = sum(branch[u.id] for u in t.children)  # @line L1
            if t.risk == branch[t.id]:  # @line L1
                cut.add(t.id)  # @line L1
    seq = [(Fraction(0), frozenset(cut))]  # @line L1
    while not (root.is_leaf() or root.id in cut):  # @line L2
        g = {}  # @line L3
        _scan(root, cut, g)  # @line L3
        a = min(g.values())  # @line L4
        cut |= {i for i, v in g.items() if v == a}  # @line L5
        seq.append((a, frozenset(cut)))  # @line L5
    return seq


def at_alpha(seq: list, alpha):
    """The cut of T_k with alpha_k <= alpha < alpha_{k+1}."""
    return [c for a, c in seq if a <= alpha][-1]


def leaves(t: Node, cut) -> list:
    if t.is_leaf() or t.id in cut:
        return [t]
    return [l for u in t.children for l in leaves(u, cut)]


# ---- a least-squares regression tree, to pick alpha by cross-validation -------------

def grow_regression(X, y, idx, n_min: int = 2) -> Node:
    """CART-style growth on numeric features: binary cuts at midpoints of largest
    decrease in the sum of squared errors, until a node is pure or too small."""
    ys = [y[i] for i in idx]
    mean = sum(ys, Fraction(0)) / len(ys)
    node = Node(sum(((v - mean) ** 2 for v in ys), Fraction(0)), value=mean)
    if node.risk == 0 or len(idx) < n_min:
        return node
    best = None
    for j in range(len(X[idx[0]])):
        pts = sorted((X[i][j], y[i]) for i in idx)
        s, s2, m = sum(v for _, v in pts), sum(v * v for _, v in pts), len(pts)
        ls = ls2 = Fraction(0)
        for k in range(m - 1):
            ls, ls2 = ls + pts[k][1], ls2 + pts[k][1] ** 2
            if pts[k][0] == pts[k + 1][0]:
                continue
            left = ls2 - ls * ls / (k + 1)
            right = (s2 - ls2) - (s - ls) ** 2 / (m - k - 1)
            sse = left + right
            if best is None or sse < best[0]:
                best = (sse, j, Fraction(pts[k][0] + pts[k + 1][0]) / 2)
    if best is None:
        return node
    _, node.feature, node.threshold = best
    L = [i for i in idx if X[i][node.feature] <= node.threshold]
    R = [i for i in idx if X[i][node.feature] > node.threshold]
    node.children = [grow_regression(X, y, L, n_min), grow_regression(X, y, R, n_min)]
    return node


def predict(t: Node, cut, x):
    while not (t.is_leaf() or t.id in cut):
        t = t.children[0] if x[t.feature] <= t.threshold else t.children[1]
    return t.value


def choose_by_cv(X, y, folds: int = 10, rng: random.Random | None = None):
    """Grow on all the data, compute the sequence, and pick k by V-fold
    cross-validation at alpha'_k = sqrt(alpha_k alpha_{k+1}), with ties to the
    smaller tree. Returns (root, sequence, k, the cross-validated losses)."""
    y = [Fraction(v) for v in y]
    n = len(y)
    root = grow_regression(X, y, list(range(n)))
    seq = weakest_link(root)
    reps = [sqrt(seq[k][0] * seq[k + 1][0]) for k in range(len(seq) - 1)] + [float("inf")]
    order = list(range(n))
    (rng or random.Random(0)).shuffle(order)
    cv = [Fraction(0)] * len(seq)
    for v in range(folds):  # @line L6
        test = set(order[v::folds])  # @line L6
        train = [i for i in range(n) if i not in test]  # @line L6
        if not test or not train:
            continue
        tv = grow_regression(X, y, train)  # @line L6
        sv = weakest_link(tv)  # @line L6
        for k, r in enumerate(reps):  # @line L7
            cut = at_alpha(sv, r)  # @line L7
            cv[k] += sum((predict(tv, cut, X[i]) - y[i]) ** 2 for i in test)  # @line L7
    best = min(range(len(seq)), key=lambda k: (cv[k], -k))  # @line L8
    return root, seq, best, cv  # @line L8
