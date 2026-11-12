# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/c4-5/. The authors are listed in prov/MDWZEM.jsonl.

"""C4.5 (Quinlan 1993): a decision tree grown by the gain ratio with the
average-gain filter, binary thresholds on numeric attributes, fractional
cases for missing values (None), and pessimistic error-based pruning with
the upper confidence limit U_CF(E, N), by subtree replacement and raising.

A case is (x, y, w): an attribute tuple, a class label and a weight.
kinds[a] is "cat" for a categorical attribute and "num" for a numeric one.
"""

from bisect import bisect_right
from math import exp, lgamma, log, log2
from typing import Hashable, Sequence

EPS = 1e-9


class Node:
    """A leaf when attr is None. A numeric test is x[attr] <= theta, with
    outcomes True and False; a categorical test has one outcome per value.
    probs[o] is the fraction of the known weight at the node that went to o."""

    __slots__ = ("attr", "theta", "branches", "probs", "dist", "label")

    def __init__(self, dist, label, attr=None, theta=None, branches=None, probs=None):
        self.dist, self.label = dist, label
        self.attr, self.theta = attr, theta
        self.branches, self.probs = branches or {}, probs or {}

    def is_leaf(self) -> bool:
        return self.attr is None


def info(dist: dict) -> float:
    """Entropy in bits of a weighted class distribution."""
    n = sum(dist.values())
    return -sum(w / n * log2(w / n) for w in dist.values() if w > EPS) if n > EPS else 0.0


def class_dist(cases) -> dict:
    d: dict = {}
    for _, y, w in cases:
        d[y] = d.get(y, 0.0) + w
    return d


def best_label(dist: dict, fallback: Hashable) -> Hashable:
    """The class of largest weight; a tie goes to the smallest label."""
    live = [c for c in dist if dist[c] > EPS]
    return max(sorted(live), key=lambda c: dist[c]) if live else fallback


def scores(groups: Sequence[dict], w_unknown: float):
    """(gain, split info) of a test with known outcome distributions groups.
    gain = F * (info(known) - sum W_o/W_K info(o)), F = W_K / W, and the
    split info treats the unknown cases as one more outcome."""
    wk = sum(sum(g.values()) for g in groups)
    w = wk + w_unknown
    known: dict = {}
    for g in groups:
        for c, x in g.items():
            known[c] = known.get(c, 0.0) + x
    rem = sum(sum(g.values()) / wk * info(g) for g in groups)
    gain = wk / w * (info(known) - rem)
    parts = [sum(g.values()) for g in groups] + [w_unknown]
    split = -sum(p / w * log2(p / w) for p in parts if p > EPS)
    return gain, split


def eval_categorical(cases, a: int, min_objs: float):
    """(gain, split, None), or None if fewer than two outcomes have min_objs weight."""
    groups: dict = {}
    wu = 0.0
    for x, y, w in cases:
        if x[a] is None:
            wu += w
        else:
            g = groups.setdefault(x[a], {})
            g[y] = g.get(y, 0.0) + w
    if sum(1 for g in groups.values() if sum(g.values()) >= min_objs - EPS) < 2:
        return None
    return (*scores(list(groups.values()), wu), None)


def eval_numeric(cases, a: int, min_objs: float, all_values: Sequence):
    """Best threshold of numeric attribute a by gain: (gain, split, theta), or None.
    Each side needs min_objs weight. The threshold is the largest value of a in
    the whole training set that does not exceed the midpoint of the cut.
    Cost: O(n log n) to sort plus O(n k) for the scan."""
    known = sorted((x[a], y, w) for x, y, w in cases if x[a] is not None)
    wu = sum(w for x, _, w in cases if x[a] is None)
    right = class_dist(known)
    left: dict = {}
    wl, wr = 0.0, sum(right.values())
    best = None
    for i in range(len(known) - 1):
        v, y, w = known[i]
        left[y] = left.get(y, 0.0) + w
        right[y] -= w
        wl, wr = wl + w, wr - w
        if v == known[i + 1][0] or wl < min_objs - EPS or wr < min_objs - EPS:
            continue
        g, s = scores([left, right], wu)
        if best is None or g > best[0] + EPS:
            mid = (v + known[i + 1][0]) / 2
            theta = all_values[bisect_right(all_values, mid) - 1]
            best = (g, s, theta)
    return best


def outcome(node: Node, x):
    v = x[node.attr]
    if v is None:
        return None
    o = v <= node.theta if node.theta is not None else v
    return o if o in node.branches else None


def partition(node: Node, cases, probs: dict) -> dict:
    """Send known cases down their branch, unknown ones down every branch o with weight w * probs[o]."""
    parts: dict = {o: [] for o in node.branches}
    for x, y, w in cases:
        o = outcome(node, x)
        if o is None:
            for p, q in probs.items():
                if q > EPS:
                    parts[p].append((x, y, w * q))
        else:
            parts[o].append((x, y, w))
    return parts


def grow(cases, attrs, kinds, values, min_objs, fallback) -> Node:
    """Build the unpruned C4.5 tree on the weighted cases."""
    dist = class_dist(cases)
    n = sum(dist.values())
    label = best_label(dist, fallback)
    if sum(1 for c in dist.values() if c > EPS) <= 1 or n < 2 * min_objs - EPS:  # @line L1
        return Node(dist, label)  # @line L1
    cand = []  # @line L2
    for a in attrs:  # @line L2
        r = eval_categorical(cases, a, min_objs) if kinds[a] == "cat" else eval_numeric(cases, a, min_objs, values[a])  # @line L2
        if r is not None:  # @line L2
            cand.append((a, *r))  # @line L2
    avg = sum(c[1] for c in cand) / len(cand) if cand else 0.0  # @line L3
    best = None  # @line L4
    for a, g, s, theta in cand:  # @line L4
        if g >= avg - EPS and s > EPS and (best is None or g / s > best[1] / best[2] + EPS):  # @line L4
            best = (a, g, s, theta)  # @line L4
    if best is None or best[1] <= EPS:  # @line L5
        return Node(dist, label)  # @line L5
    a, _, _, theta = best
    outs = [True, False] if theta is not None else values[a]
    node = Node(dist, label, a, theta, {o: None for o in outs})  # @line L6
    known: dict = {o: 0.0 for o in outs}  # @line L6
    for x, _, w in cases:  # @line L6
        o = outcome(node, x)  # @line L6
        if o is not None:  # @line L6
            known[o] += w  # @line L6
    wk = sum(known.values())  # @line L6
    node.probs = {o: known[o] / wk for o in outs}  # @line L6
    parts = partition(node, cases, node.probs)  # @line L7
    rest = [b for b in attrs if b != a] if kinds[a] == "cat" else attrs
    for o in outs:  # @line L8
        sub = parts[o]  # @line L8
        if sum(w for _, _, w in sub) > EPS:  # @line L9
            node.branches[o] = grow(sub, rest, kinds, values, min_objs, label)  # @line L9
        else:  # @line L9
            node.branches[o] = Node({}, label)  # @line L9
    return node  # @line L10


def _betacf(a: float, b: float, x: float) -> float:
    """Continued fraction of the incomplete beta function (modified Lentz)."""
    tiny = 1e-300
    qab, qap, qam = a + b, a + 1, a - 1
    c, d = 1.0, 1 - qab * x / qap
    d = 1 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 400):
        m2 = 2 * m
        for aa in (m * (b - m) * x / ((qam + m2) * (a + m2)),
                   -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))):
            d = 1 + aa * d
            d = 1 / (d if abs(d) > tiny else tiny)
            c = 1 + aa / c
            c = c if abs(c) > tiny else tiny
            h *= d * c
        if abs(d * c - 1) < 1e-15:
            break
    return h


def betainc(a: float, b: float, x: float) -> float:
    """The regularized incomplete beta function I_x(a, b)."""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbt = lgamma(a + b) - lgamma(a) - lgamma(b) + a * log(x) + b * log(1 - x)
    if x < (a + 1) / (a + b + 2):
        return exp(lbt) * _betacf(a, b, x) / a
    return 1 - exp(lbt) * _betacf(b, a, 1 - x) / b


def upper_limit(e: float, n: float, cf: float = 0.25) -> float:
    """U_CF(E, N): the p with P(Binomial(N, p) <= E) = CF, so the upper end of a
    one-sided confidence interval of level 1 - CF for the error rate. For
    fractional E and N the binomial tail is the beta form 1 - I_p(E + 1, N - E)."""
    if e <= EPS:
        return 1 - cf ** (1 / n)
    if e >= n - EPS:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(100):
        p = (lo + hi) / 2
        if 1 - betainc(e + 1, n - e, p) > cf:
            lo = p
        else:
            hi = p
    return (lo + hi) / 2


def _estimate(node: Node, cases, cf: float, update: bool, raising: bool = True):
    """Predicted errors sum N * U_CF(E, N) of the subtree on the cases; when
    update is true, prune it bottom-up and return the new subtree. A leaf
    keeps its label; a node becomes a leaf, or (if raising) is replaced by its
    largest branch, when that does not raise the estimate by more than 0.1."""
    dist = class_dist(cases)
    n = sum(dist.values())
    leaf_est = n * upper_limit(n - dist.get(node.label, 0.0), n, cf) if n > EPS else 0.0
    if update:
        node.dist = dist
    if node.is_leaf():  # @line L11
        return node, leaf_est  # @line L11
    known: dict = {o: 0.0 for o in node.branches}
    for x, _, w in cases:
        o = outcome(node, x)
        if o is not None:
            known[o] += w
    wk = sum(known.values())
    probs = {o: known[o] / wk for o in known} if wk > EPS else node.probs
    if update:
        node.probs = probs
    parts = partition(node, cases, probs)
    tree_est = 0.0  # @line L12
    for o in list(node.branches):  # @line L12
        child, e = _estimate(node.branches[o], parts[o], cf, update, raising)  # @line L12
        node.branches[o] = child  # @line L12
        tree_est += e  # @line L12
    if not update:
        return node, tree_est
    branch_est = float("inf")  # @line L13
    if raising:  # @line L13
        big = max(node.branches, key=lambda o: sum(w for _, _, w in parts[o]))  # @line L13
        _, branch_est = _estimate(node.branches[big], cases, cf, False)  # @line L13
    if leaf_est <= branch_est + 0.1 and leaf_est <= tree_est + 0.1:  # @line L14
        return Node(dist, node.label), leaf_est  # @line L14
    if branch_est <= tree_est + 0.1:  # @line L15
        return _estimate(node.branches[big], cases, cf, True, raising)  # @line L15
    return node, tree_est  # @line L16


def prune(tree: Node, cases, cf: float = 0.25, raising: bool = True):
    """C4.5 error-based pruning of tree on its training cases.
    Returns (the pruned tree, its estimated errors)."""
    return _estimate(tree, cases, cf, True, raising)


def estimated_errors(tree: Node, cases, cf: float = 0.25) -> float:
    """The pessimistic error estimate of the tree, without changing it."""
    return _estimate(tree, cases, cf, False)[1]


def c45(X, y, kinds, w=None, cf: float = 0.25, min_objs: float = 2, pruning: bool = True,
        raising: bool = True) -> Node:
    """Grow and (by default) prune a C4.5 tree. None marks a missing value."""
    w = [1.0] * len(y) if w is None else list(w)
    cases = list(zip(X, y, w))
    values = {a: sorted({x[a] for x in X if x[a] is not None}) for a in range(len(kinds))}
    tree = grow(cases, list(range(len(kinds))), kinds, values, min_objs, best_label(class_dist(cases), None))
    return prune(tree, cases, cf, raising)[0] if pruning else tree


def class_probs(node: Node, x) -> dict:
    """Class probabilities of x; a missing value follows every branch o with weight probs[o]."""
    if node.is_leaf():
        n = sum(node.dist.values())
        return {c: v / n for c, v in node.dist.items()} if n > EPS else {node.label: 1.0}
    o = outcome(node, x)
    if o is not None:
        return class_probs(node.branches[o], x)
    out: dict = {}
    for o, p in node.probs.items():
        if p > EPS:
            for c, q in class_probs(node.branches[o], x).items():
                out[c] = out.get(c, 0.0) + p * q
    return out


def predict(node: Node, x) -> Hashable:
    pr = class_probs(node, x)
    return max(sorted(pr), key=lambda c: pr[c])
