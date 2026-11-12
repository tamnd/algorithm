# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-bayesian-network/. The authors are listed in prov/YPNGR6.jsonl.

"""Exact filtering in a factored dynamic Bayesian network by the frontier algorithm.

The DBN has K binary hidden chains X^0..X^(K-1), and chain k has one observed child Y^k
in each slice. The 2TBN (two-slice temporal Bayes net) is given by
prior[k]       P(X_1^k = 1); the chains are independent in the first slice
parents[k]     tuple of the chains in slice t-1 that are parents of X_t^k
cpt[k][u]      P(X_t^k = 1 | the parents take the values u), u a tuple of bits in the order of parents[k]
emit[k][x][y]  P(Y_t^k = y | X_t^k = x)
An observation at one time is a tuple of K symbols. The numbers may be floats or
fractions.Fraction. A belief is a dict from a tuple of K bits to a probability.

The frontier algorithm (Zweig 1996; Murphy 2002, Section 3.3) keeps one factor, the
frontier, over a set of variables that separates the past from the future. To go from
slice t-1 to slice t it adds the nodes of slice t one at a time, multiplying in their
CPT and evidence, and sums out a node of slice t-1 as soon as all of its children are in.
"""

import math
import random
from itertools import product
from typing import Optional, Sequence


class DBN:
    def __init__(self, prior: Sequence, parents: Sequence[tuple], cpt: Sequence[dict], emit: Sequence) -> None:
        K = len(prior)
        if K == 0 or not (len(parents) == len(cpt) == len(emit) == K):
            raise ValueError("need K >= 1 chains and K entries in parents, cpt and emit")
        for k in range(K):
            if any(not 0 <= i < K for i in parents[k]) or len(set(parents[k])) != len(parents[k]):
                raise ValueError(f"bad parents for chain {k}")
            if set(cpt[k]) != set(product((0, 1), repeat=len(parents[k]))):
                raise ValueError(f"the CPT of chain {k} needs one entry per parent assignment")
            if len(emit[k]) != 2 or len(emit[k][0]) != len(emit[k][1]):
                raise ValueError(f"emit[{k}] needs two rows of the same length")
        self.K = K
        self.prior = list(prior)
        self.parents = [tuple(p) for p in parents]
        self.cpt = [dict(c) for c in cpt]
        self.emit = [[list(r) for r in e] for e in emit]
        # children[i] = the chains in slice t whose CPT uses chain i of slice t-1
        self.children = [frozenset(k for k in range(K) if i in self.parents[k]) for i in range(K)]


def _add_node(vars_: list, table: dict, k: int, p1_of, ev0, ev1):
    """Multiply the factor by P(x_k | its parents) P(y_k | x_k) and add x_k as its last variable."""
    new = {}
    for a, v in table.items():
        p1 = p1_of(a)
        new[a + (0,)] = v * (1 - p1) * ev0
        new[a + (1,)] = v * p1 * ev1
    return vars_ + [("c", k)], new


def _sum_out(vars_: list, table: dict, var) -> tuple:
    i = vars_.index(var)
    new: dict = {}
    for a, v in table.items():
        b = a[:i] + a[i + 1:]
        new[b] = new[b] + v if b in new else v
    return vars_[:i] + vars_[i + 1:], new


def frontier_step(dbn: DBN, belief: Optional[dict], y: Sequence[int], order: Optional[Sequence[int]] = None):
    """One slice of filtering. belief = P(X_(t-1) | y_1..y_(t-1)), or None for the first slice.

    Return (P(X_t | y_1..y_t), P(y_t | y_1..y_(t-1)), the largest number of variables in the frontier).
    """
    K = dbn.K
    order = list(range(K)) if order is None else list(order)
    if sorted(order) != list(range(K)) or len(y) != K:
        raise ValueError("order must list each chain once, and y needs one symbol per chain")
    if belief is None:
        vars_: list = []
        table: dict = {(): 1}
    else:
        vars_ = [("p", i) for i in range(K)]
        table = dict(belief)
    added: set = set()

    def drop_finished(vs, tb):
        # a node of slice t-1 leaves the frontier once all of its children have joined it
        for i in range(K):
            if ("p", i) in vs and dbn.children[i] <= added:
                vs, tb = _sum_out(vs, tb, ("p", i))
        return vs, tb

    if belief is not None:
        vars_, table = drop_finished(vars_, table)
    largest = len(vars_)
    for k in order:
        e = dbn.emit[k]
        if belief is None:
            p1_of = lambda a, k=k: dbn.prior[k]
        else:
            idx = [vars_.index(("p", i)) for i in dbn.parents[k]]
            p1_of = lambda a, k=k, idx=idx: dbn.cpt[k][tuple(a[j] for j in idx)]
        vars_, table = _add_node(vars_, table, k, p1_of, e[0][y[k]], e[1][y[k]])
        largest = max(largest, len(vars_))
        added.add(k)
        if belief is not None:
            vars_, table = drop_finished(vars_, table)
    norm = sum(table.values())
    if norm == 0:
        raise ValueError("the observations have probability 0")
    perm = [vars_.index(("c", k)) for k in range(K)]
    out = {tuple(a[j] for j in perm): v / norm for a, v in table.items()}
    return out, norm, largest


def frontier_filter(dbn: DBN, ys: Sequence[Sequence[int]], order: Optional[Sequence[int]] = None):
    """Unrolled forward filtering over T slices.

    Return (beliefs, norms, largest): beliefs[t-1] = P(X_t | y_1..y_t), norms[t-1] =
    P(y_t | y_1..y_(t-1)), so P(y_1..y_T) is the product of the norms, and largest is the
    largest frontier seen. With F the largest frontier, the time is O(T K 2^F).
    """
    if len(ys) == 0:
        raise ValueError("empty observation sequence")
    beliefs, norms, largest = [], [], 0
    belief = None
    for y in ys:
        belief, n, f = frontier_step(dbn, belief, y, order)
        beliefs.append(belief)
        norms.append(n)
        largest = max(largest, f)
    return beliefs, norms, largest


def log_likelihood(norms: Sequence) -> float:
    return math.fsum(math.log(n) for n in norms)


def flat_hmm(dbn: DBN):
    """The same process as an HMM on the 2^K product states, for checking.

    Return (states, pi, A, b) with b(s, y) = P(y | state s). Building A costs O(4^K K).
    """
    K = dbn.K
    states = list(product((0, 1), repeat=K))

    def bern(p, x):
        return p if x else 1 - p

    pi = []
    for s in states:
        w = 1
        for k in range(K):
            w = w * bern(dbn.prior[k], s[k])
        pi.append(w)
    A = []
    for s in states:
        row = []
        for s2 in states:
            w = 1
            for k in range(K):
                w = w * bern(dbn.cpt[k][tuple(s[i] for i in dbn.parents[k])], s2[k])
            row.append(w)
        A.append(row)

    def b(si: int, y) -> object:
        w = 1
        for k in range(K):
            w = w * dbn.emit[k][states[si][k]][y[k]]
        return w

    return states, pi, A, b


def _draw(p1, rng: random.Random) -> int:
    return 1 if rng.random() < p1 else 0


def _draw_symbol(row, rng: random.Random) -> int:
    u, acc = rng.random(), 0.0
    for y, p in enumerate(row):
        acc += p
        if u < acc:
            return y
    return max(y for y, p in enumerate(row) if p > 0)


def sample(dbn: DBN, T: int, rng: random.Random):
    """Draw (hidden states, observations) for T slices by ancestral sampling of the unrolled network."""
    xs, ys = [], []
    x: tuple = ()
    for t in range(T):
        if t == 0:
            x = tuple(_draw(dbn.prior[k], rng) for k in range(dbn.K))
        else:
            x = tuple(_draw(dbn.cpt[k][tuple(x[i] for i in dbn.parents[k])], rng) for k in range(dbn.K))
        xs.append(x)
        ys.append(tuple(_draw_symbol(dbn.emit[k][x[k]], rng) for k in range(dbn.K)))
    return xs, ys
