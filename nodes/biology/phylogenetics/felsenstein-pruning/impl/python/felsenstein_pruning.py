# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/felsenstein-pruning/. The authors are listed in prov/9J75HR.jsonl.
"""Felsenstein's pruning algorithm for the likelihood of a rooted tree.

A tree is a pair (children, root): children maps each internal node to the
list of its children, and a node that is not a key (or maps to an empty list)
is a leaf. P maps each non-root node c to the k x k transition matrix of the
branch above c, so P[c][a][b] is the probability of state b at c given state
a at the parent of c. pi is the distribution of the state at the root. A site
maps each leaf to its state (an int in range(k)) or to None for missing data.

The code uses only +, * and comparisons on matrix entries, so it works with
float and with fractions.Fraction alike.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Dict, Hashable, List, Mapping, Optional, Sequence

Node = Hashable
Matrix = Sequence[Sequence[float]]


def jc69_matrix(t: float) -> List[List[float]]:
    """JC69 transition matrix for a branch of t expected substitutions per site."""
    x = math.exp(-4.0 * t / 3.0)
    same, diff = 0.25 + 0.75 * x, 0.25 - 0.25 * x
    return [[same if i == j else diff for j in range(4)] for i in range(4)]


def jc69_matrix_from_x(x: Fraction) -> List[List[Fraction]]:
    """JC69 matrix written with x = exp(-4t/3); exact when x is a Fraction."""
    same = Fraction(1, 4) + Fraction(3, 4) * x
    diff = Fraction(1, 4) - Fraction(1, 4) * x
    return [[same if i == j else diff for j in range(4)] for i in range(4)]


def postorder(children: Mapping[Node, Sequence[Node]], root: Node) -> List[Node]:
    """Nodes in post-order (each child before its parent), with an explicit stack."""
    order: List[Node] = []
    stack = [root]
    while stack:
        v = stack.pop()
        order.append(v)
        stack.extend(children.get(v, ()))
    order.reverse()
    return order


def conditional_likelihoods(children: Mapping[Node, Sequence[Node]], root: Node,
                            P: Mapping[Node, Matrix], site: Mapping[Node, Optional[int]],
                            k: int, one=1) -> Dict[Node, List]:
    """L[v][a] = Pr(the leaf states below v | state a at v), for every node v."""
    zero = one - one
    L: Dict[Node, List] = {}
    for v in postorder(children, root):  # @line L1
        kids = children.get(v, ())
        if not kids:
            s = site[v]
            if s is not None:
                L[v] = [one if a == s else zero for a in range(k)]  # @line L2
            else:
                L[v] = [one] * k  # @line L3
            continue
        vec = [one] * k
        for c in kids:
            Pc, Lc = P[c], L[c]
            for a in range(k):  # @line L4
                row = Pc[a]
                acc = zero
                for b in range(k):
                    acc += row[b] * Lc[b]
                vec[a] *= acc  # @line L5
        L[v] = vec
    return L


def felsenstein_pruning(children: Mapping[Node, Sequence[Node]], root: Node,
                        P: Mapping[Node, Matrix], pi: Sequence, site: Mapping[Node, Optional[int]]):
    """Likelihood of one site: sum over a of pi[a] * L[root][a]."""
    k = len(pi)
    one = pi[0] - pi[0] + 1
    L = conditional_likelihoods(children, root, P, site, k, one)
    total = one - one
    for a in range(k):
        total += pi[a] * L[root][a]
    return total  # @line L6


def site_log_likelihood(children: Mapping[Node, Sequence[Node]], root: Node,
                        P: Mapping[Node, Matrix], pi: Sequence[float],
                        site: Mapping[Node, Optional[int]]) -> float:
    """Natural log of the site likelihood in floats, with rescaling at each node.

    Each internal vector is divided by its largest entry, and the log of that
    factor is added to the result, so deep trees do not underflow.
    """
    k = len(pi)
    L: Dict[Node, List[float]] = {}
    log_scale = 0.0
    for v in postorder(children, root):
        kids = children.get(v, ())
        if not kids:
            s = site[v]
            L[v] = [1.0] * k if s is None else [1.0 if a == s else 0.0 for a in range(k)]
            continue
        vec = [1.0] * k
        for c in kids:
            Pc, Lc = P[c], L[c]
            for a in range(k):
                row = Pc[a]
                vec[a] *= sum(row[b] * Lc[b] for b in range(k))
        top = max(vec)
        if top <= 0.0:
            return -math.inf
        log_scale += math.log(top)
        L[v] = [x / top for x in vec]
    return log_scale + math.log(sum(pi[a] * L[root][a] for a in range(k)))


def tree_log_likelihood(children: Mapping[Node, Sequence[Node]], root: Node,
                        P: Mapping[Node, Matrix], pi: Sequence[float],
                        alignment: Mapping[Node, Sequence[Optional[int]]]) -> float:
    """Log-likelihood of an alignment (leaf -> list of states), sites independent.

    Identical site patterns are computed once and weighted by their count.
    """
    leaves = sorted(alignment, key=repr)
    m = len(alignment[leaves[0]]) if leaves else 0
    counts: Dict[tuple, int] = {}
    for j in range(m):
        pattern = tuple(alignment[v][j] for v in leaves)
        counts[pattern] = counts.get(pattern, 0) + 1
    total = 0.0
    for pattern, c in counts.items():
        site = dict(zip(leaves, pattern))
        total += c * site_log_likelihood(children, root, P, pi, site)
    return total
