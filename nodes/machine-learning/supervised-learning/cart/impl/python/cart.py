# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cart/. The authors are listed in prov/6A3KDC.jsonl.

"""CART (Breiman, Friedman, Olshen and Stone 1984): binary trees on numeric
features, grown by the Gini decrease (classification) or the decrease in the
sum of squared errors (regression), with surrogate splits for missing values
(None), then pruned by minimal cost-complexity pruning with alpha chosen by
V-fold cross-validation.

All impurity sums use fractions.Fraction, so ties and the pruning sequence
are exact. R(t) is the resubstitution risk of node t as a leaf: the number of
misclassified cases (classification) or the sum of squared errors (regression).
"""

import random
from fractions import Fraction
from math import sqrt
from typing import Any, Hashable, Sequence


class Node:
    __slots__ = ("id", "n", "value", "risk", "feature", "threshold", "left", "right",
                 "surrogates", "majority_left")

    def __init__(self, n, value, risk):
        self.id = 0
        self.n, self.value, self.risk = n, value, risk
        self.feature = self.threshold = self.left = self.right = None
        self.surrogates: list = []  # (lambda, feature, threshold, le_goes_left)
        self.majority_left = True

    def is_leaf(self) -> bool:
        return self.feature is None


# ---- impurity: N(t) * i(t), exact --------------------------------------------

class Stats:
    """Running sums of a set of cases: class counts or (sum y, sum y^2)."""

    __slots__ = ("task", "n", "counts", "s1", "s2")

    def __init__(self, task: str):
        self.task, self.n, self.counts, self.s1, self.s2 = task, 0, {}, Fraction(0), Fraction(0)

    def add(self, y, sign: int = 1):
        self.n += sign
        if self.task == "classification":
            self.counts[y] = self.counts.get(y, 0) + sign
        else:
            self.s1 += sign * y
            self.s2 += sign * y * y

    def impurity(self) -> Fraction:
        """N * Gini = N - sum c^2 / N, or the SSE = sum y^2 - (sum y)^2 / N."""
        if self.n == 0:
            return Fraction(0)
        if self.task == "classification":
            return self.n - Fraction(sum(c * c for c in self.counts.values()), self.n)
        return self.s2 - self.s1 * self.s1 / self.n


def leaf_value(task: str, ys: Sequence) -> tuple:
    """(prediction, R(t)): the majority class (ties to the smallest) and its error
    count, or the mean and the sum of squared errors."""
    if task == "classification":
        c: dict = {}
        for y in ys:
            c[y] = c.get(y, 0) + 1
        best = max(sorted(c), key=lambda k: c[k])
        return best, Fraction(len(ys) - c[best])
    mean = sum(ys, Fraction(0)) / len(ys)
    return mean, sum(((y - mean) ** 2 for y in ys), Fraction(0))


# ---- the split search ----------------------------------------------------------

def best_cut(X, y, idx, j: int, task: str):
    """The cut x[j] <= theta of largest impurity decrease on the cases of idx with
    x[j] known: (decrease, theta), theta a midpoint, or None. Ties go to the
    smallest theta. Cost: O(m log m) to sort and O(m) for the scan (classes bounded)."""
    known = sorted((X[i][j], y[i]) for i in idx if X[i][j] is not None)
    if len(known) < 2:
        return None
    left, right = Stats(task), Stats(task)
    for _, yi in known:
        right.add(yi)
    parent = right.impurity()
    best = None
    for k in range(len(known) - 1):
        left.add(known[k][1])
        right.add(known[k][1], -1)
        if known[k][0] == known[k + 1][0]:
            continue
        dec = parent - left.impurity() - right.impurity()
        if best is None or dec > best[0]:
            best = (dec, Fraction(known[k][0] + known[k + 1][0]) / 2)
    return best


def goes_left(node: Node, x) -> bool:
    """The primary split, else the first surrogate with a known value, else the larger side."""
    if x[node.feature] is not None:
        return x[node.feature] <= node.threshold
    for _, j, theta, le_left in node.surrogates:
        if x[j] is not None:
            return (x[j] <= theta) == le_left
    return node.majority_left


def find_surrogates(X, idx, primary: int, side: dict) -> list:
    """For each other feature, the cut and direction that agree most often with the
    primary split, on the cases with both values known. Keep those whose predictive
    association lambda = (min(pL, pR) - (1 - agreement)) / min(pL, pR) is positive,
    best first. Ties go to the smaller threshold, then to le_goes_left = True."""
    out = []
    d = len(X[idx[0]])
    for j in range(d):
        if j == primary:
            continue
        both = sorted((X[i][j], side[i]) for i in idx if X[i][j] is not None and X[i][primary] is not None)
        m = len(both)
        if m < 2:
            continue
        n_left = sum(1 for _, s in both if s)
        p_min = Fraction(min(n_left, m - n_left), m)
        if p_min == 0:
            continue
        best = None
        ll = 0  # primary-left cases among the first k + 1
        for k in range(m - 1):
            ll += both[k][1]
            if both[k][0] == both[k + 1][0]:
                continue
            theta = Fraction(both[k][0] + both[k + 1][0]) / 2
            agree_le = ll + (m - k - 1 - (n_left - ll))  # <= goes left
            for agree, le_left in ((agree_le, True), (m - agree_le, False)):
                if best is None or agree > best[0]:
                    best = (agree, theta, le_left)
        if best is None:
            continue
        lam = (p_min - (1 - Fraction(best[0], m))) / p_min
        if lam > 0:
            out.append((lam, j, best[1], best[2]))
    out.sort(key=lambda s: (-s[0], s[1]))
    return out


def grow(X, y, idx, task: str, n_min: int, depth: int = 0, max_depth: int | None = None) -> Node:
    """Grow the maximal tree on the cases idx."""
    value, risk = leaf_value(task, [y[i] for i in idx])
    node = Node(len(idx), value, risk)
    if risk == 0 or len(idx) < n_min or (max_depth is not None and depth >= max_depth):  # @line L1
        return node  # @line L1
    best = None  # @line L2
    for j in range(len(X[idx[0]])):  # @line L2
        c = best_cut(X, y, idx, j, task)  # @line L2
        if c is not None and (best is None or c[0] > best[0]):  # @line L3
            best = (c[0], j, c[1])  # @line L3
    if best is None:  # @line L3
        return node  # @line L3
    node.feature, node.threshold = best[1], best[2]
    side = {i: X[i][node.feature] <= node.threshold for i in idx if X[i][node.feature] is not None}
    node.surrogates = find_surrogates(X, idx, node.feature, side)  # @line L4
    node.majority_left = 2 * sum(side.values()) >= len(side)
    L = [i for i in idx if goes_left(node, X[i])]  # @line L5
    R = [i for i in idx if not goes_left(node, X[i])]  # @line L5
    if not L or not R:
        node.feature = None
        return node
    node.left = grow(X, y, L, task, n_min, depth + 1, max_depth)  # @line L6
    node.right = grow(X, y, R, task, n_min, depth + 1, max_depth)  # @line L6
    return node


def number(root: Node) -> list:
    """Give the nodes preorder ids; return them in preorder."""
    out, stack = [], [root]
    while stack:
        t = stack.pop()
        t.id = len(out)
        out.append(t)
        if not t.is_leaf():
            stack += [t.right, t.left]
    return out


# ---- minimal cost-complexity pruning ---------------------------------------------

def _branch(t: Node, cut: set) -> tuple:
    """(R(T_t), number of leaves of T_t) in the subtree where the nodes in cut are leaves."""
    if t.is_leaf() or t.id in cut:
        return t.risk, 1
    a, b = _branch(t.left, cut), _branch(t.right, cut)
    return a[0] + b[0], a[1] + b[1]


def _internal(t: Node, cut: set) -> list:
    if t.is_leaf() or t.id in cut:
        return []
    return [t] + _internal(t.left, cut) + _internal(t.right, cut)


def pruning_sequence(root: Node) -> list:
    """The weakest-link sequence [(alpha_1 = 0, cut_1), (alpha_2, cut_2), ...]: cut_k is
    the set of nodes made leaves in T_k, and T_k is the smallest subtree that
    minimizes R(T) + alpha |leaves(T)| for alpha in [alpha_k, alpha_{k+1})."""
    number(root)
    cut: set = set()
    for t in reversed(_internal(root, cut)):  # @line L7
        if t.risk == _branch(t, cut)[0]:  # @line L7
            cut.add(t.id)  # @line L7
    seq = [(Fraction(0), frozenset(cut))]
    while _internal(root, cut):  # @line L8
        g = {t.id: (t.risk - r) / (k - 1) for t in _internal(root, cut) for r, k in [_branch(t, cut)]}  # @line L8
        a = min(g.values())  # @line L8
        cut |= {i for i, v in g.items() if v == a}  # @line L9
        seq.append((a, frozenset(cut)))  # @line L9
    return seq


def subtree(root: Node, cut) -> Node:
    """A copy of the tree with the nodes in cut made leaves."""
    t = Node(root.n, root.value, root.risk)
    t.id = root.id
    if root.is_leaf() or root.id in cut:
        return t
    t.feature, t.threshold = root.feature, root.threshold
    t.surrogates, t.majority_left = root.surrogates, root.majority_left
    t.left, t.right = subtree(root.left, cut), subtree(root.right, cut)
    return t


def predict(t: Node, x) -> Any:
    while not t.is_leaf():
        t = t.left if goes_left(t, x) else t.right
    return t.value


def loss(task: str, pred, y) -> Fraction:
    return Fraction(int(pred != y)) if task == "classification" else (Fraction(pred) - y) ** 2


def cart(X, y, task: str = "classification", folds: int = 10, rng: random.Random | None = None,
         n_min: int = 2, max_depth: int | None = None):
    """Grow the maximal tree, compute its pruning sequence, and pick T_k by V-fold
    cross-validation at alpha'_k = sqrt(alpha_k alpha_{k+1}). Returns
    (tree, the sequence, the cross-validated loss of each T_k)."""
    if task == "regression":
        y = [Fraction(v) for v in y]
    full = grow(X, y, list(range(len(y))), task, n_min, 0, max_depth)
    seq = pruning_sequence(full)
    alphas = [a for a, _ in seq]
    reps = [sqrt(alphas[k] * alphas[k + 1]) for k in range(len(seq) - 1)] + [float("inf")]
    order = list(range(len(y)))
    (rng or random.Random(0)).shuffle(order)
    cv = [Fraction(0)] * len(seq)
    for v in range(folds):  # @line L10
        test = set(order[v::folds])  # @line L10
        train = [i for i in range(len(y)) if i not in test]  # @line L10
        if not test or not train:
            continue
        tv = grow(X, y, train, task, n_min, 0, max_depth)  # @line L10
        sv = pruning_sequence(tv)  # @line L10
        for k, r in enumerate(reps):  # @line L10
            cut = [c for a, c in sv if a <= r][-1]  # @line L10
            pruned = subtree(tv, cut)  # @line L10
            cv[k] += sum(loss(task, predict(pruned, X[i]), y[i]) for i in test)  # @line L10
    best = min(range(len(seq)), key=lambda k: (cv[k], -k))  # @line L10
    return subtree(full, seq[best][1]), seq, cv
