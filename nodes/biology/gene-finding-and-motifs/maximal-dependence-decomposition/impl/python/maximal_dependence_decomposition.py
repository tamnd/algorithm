# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximal-dependence-decomposition/. The authors are listed in prov/7S803Q.jsonl.
"""Maximal dependence decomposition (MDD) of aligned signal sites.

The input is a list of aligned sites of the same length p over ACGT, for
example donor splice sites. Each position i has a consensus base c[i]. MDD
builds a binary tree:
- At a node with the set D of sites and the set R of positions not yet used,
  it computes, for every pair i != j in R, the chi-squared statistic of the
  2 x 4 table that crosses "x[i] == c[i]" with the base x[j].
- If no statistic is above the cutoff, or fewer than two positions are left,
  the node is a leaf with a weight matrix (one base distribution per position
  of R) estimated from D.
- Otherwise it picks the position i* with the largest sum S_i of its
  statistics, splits D into the sites with x[i*] == c[i*] and the others, and
  builds both children with R - {i*}, unless one part has fewer than min_size
  sites, in which case the node is a leaf.

The model gives each site x the probability
P(x | leaf) = product over j in R of w[j][x[j]], and
P(x | split on i) = q[x[i]] * P(x | child chosen by x[i] == c[i]),
where q is the base distribution at i* of the node. All probabilities use the
counts plus a pseudocount, and they are Fractions, so they are exact.
Ties between positions go to the smaller position.
"""

from __future__ import annotations

import math
from collections import namedtuple
from fractions import Fraction
from typing import Dict, List, Optional, Sequence, Tuple

BASES = "ACGT"

Leaf = namedtuple("Leaf", ["size", "positions", "wmm"])
Split = namedtuple("Split", ["size", "pos", "base", "dist", "match", "other"])


def consensus(sites: Sequence[str]) -> str:
    """The most frequent base at each position; ties go to the first in ACGT order."""
    p = len(sites[0])
    out = []
    for i in range(p):
        counts = {b: 0 for b in BASES}
        for s in sites:
            counts[s[i]] += 1
        out.append(max(BASES, key=lambda b: (counts[b], -BASES.index(b))))
    return "".join(out)


def chi_squared(sites: Sequence[str], i: int, j: int, c: str) -> Fraction:
    """Pearson's chi-squared statistic of (x[i] == c) against the base x[j], exact."""
    table = {(m, b): 0 for m in (True, False) for b in BASES}
    for s in sites:
        table[(s[i] == c, s[j])] += 1
    n = len(sites)
    rows = {m: sum(table[(m, b)] for b in BASES) for m in (True, False)}
    cols = {b: table[(True, b)] + table[(False, b)] for b in BASES}
    total = Fraction(0)
    for m in (True, False):
        for b in BASES:
            if rows[m] and cols[b]:
                e = Fraction(rows[m] * cols[b], n)
                total += (table[(m, b)] - e) ** 2 / e
    return total


def base_distribution(sites: Sequence[str], i: int, pseudo: Fraction) -> Dict[str, Fraction]:
    """The base frequencies at position i with a pseudocount added to each base."""
    counts = {b: 0 for b in BASES}
    for s in sites:
        counts[s[i]] += 1
    z = len(sites) + 4 * pseudo
    return {b: (counts[b] + pseudo) / z for b in BASES}


def _leaf(sites, R, pseudo):
    return Leaf(len(sites), tuple(R), {j: base_distribution(sites, j, pseudo) for j in R})


def build_mdd(sites: Sequence[str], cons: Optional[str] = None, positions: Optional[Sequence[int]] = None,
              cutoff: float = 16.3, min_size: int = 20, pseudo: Fraction = Fraction(1, 2)):
    """The MDD tree of the sites. cutoff 16.3 is about the 0.001 level of chi-squared with 3 df."""
    if not sites:
        raise ValueError("need at least one site")
    p = len(sites[0])
    if any(len(s) != p or any(c not in BASES for c in s) for s in sites):
        raise ValueError("sites must have the same length and use only ACGT")
    c = cons if cons is not None else consensus(sites)
    R = list(range(p)) if positions is None else sorted(positions)
    return _build(list(sites), R, c, cutoff, min_size, Fraction(pseudo))


def _build(D, R, c, cutoff, min_size, pseudo):
    if len(R) <= 1:  # @line L1
        return _leaf(D, R, pseudo)
    chi = {(i, j): chi_squared(D, i, j, c[i]) for i in R for j in R if i != j}  # @line L2
    if not any(v > cutoff for v in chi.values()):  # @line L3
        return _leaf(D, R, pseudo)
    best = max(R, key=lambda i: (sum(chi[(i, j)] for j in R if j != i), -i))  # @line L4
    plus = [s for s in D if s[best] == c[best]]  # @line L5
    minus = [s for s in D if s[best] != c[best]]
    if len(plus) < min_size or len(minus) < min_size:  # @line L6
        return _leaf(D, R, pseudo)
    rest = [j for j in R if j != best]
    return Split(len(D), best, c[best], base_distribution(D, best, pseudo),  # @line L7
                 _build(plus, rest, c, cutoff, min_size, pseudo),
                 _build(minus, rest, c, cutoff, min_size, pseudo))


def prob(x: str, node) -> Fraction:
    """The exact probability of the site x under the tree."""
    out = Fraction(1)
    while isinstance(node, Split):
        out *= node.dist[x[node.pos]]
        node = node.match if x[node.pos] == node.base else node.other
    for j in node.positions:
        out *= node.wmm[j][x[j]]
    return out


def log_prob(x: str, node) -> float:
    """ln P(x) under the tree."""
    if isinstance(node, Leaf):
        return sum(math.log(node.wmm[j][x[j]]) for j in node.positions)  # @line L8
    return math.log(node.dist[x[node.pos]]) + log_prob(  # @line L9
        x, node.match if x[node.pos] == node.base else node.other)


def leaves(node) -> List[Tuple[str, int]]:
    """The leaves as (path, size), where the path lists the splits, such as '+3 -0'."""
    out: List[Tuple[str, int]] = []

    def rec(n, path):
        if isinstance(n, Leaf):
            out.append((" ".join(path), n.size))
        else:
            rec(n.match, path + ["+%d" % n.pos])
            rec(n.other, path + ["-%d" % n.pos])

    rec(node, [])
    return out
