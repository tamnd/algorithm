# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/transition-density/. The authors are listed in prov/G6GC4V.jsonl.
"""Transition density propagation (Najm 1993).

Each primary input x is a 0-1 signal in time with equilibrium probability
p[x] = P(x = 1) and transition density d[x] (mean number of transitions per
unit time). The inputs are independent. transition_densities(c, p, d) walks the
gates of a netlist.Circuit in topological order and sets, for y = f(z_1..z_k),

    P(y) by the signal probability formula for independent fanins,
    D(y) = sum_j P(df/dz_j) D(z_j),

where df/dz_j = f(z_j = 0) XOR f(z_j = 1) is the Boolean difference. The
result is exact when the fanins of every gate depend on disjoint sets of
inputs (for example in a fanout-free circuit) and no two inputs switch at
the same instant. Values are Fractions when the inputs are.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence


def gate_probability(kind: str, q: Sequence[Fraction]) -> Fraction:
    """P(output = 1) for independent fanins with P(fanin j = 1) = q[j]."""
    if kind in ("AND", "NAND"):
        r = Fraction(1)
        for v in q:
            r *= v
    elif kind in ("OR", "NOR"):
        r = Fraction(1)
        for v in q:
            r *= 1 - v
        r = 1 - r
    elif kind in ("XOR", "XNOR"):
        r = Fraction(0)
        for v in q:
            r = r + v - 2 * r * v
    elif kind in ("BUF", "NOT"):
        r = Fraction(q[0])
    else:
        raise ValueError(kind)
    return 1 - r if kind in ("NAND", "NOR", "XNOR", "NOT") else r


def boolean_difference_probability(kind: str, q: Sequence[Fraction], j: int) -> Fraction:
    """P(df/dz_j = 1) for one gate, with independent fanins.

    AND and NAND are sensitive to pin j when every other pin is 1, OR and NOR
    when every other pin is 0, and XOR, XNOR, BUF and NOT always.
    """
    r = Fraction(1)
    if kind in ("AND", "NAND"):
        for k, v in enumerate(q):
            if k != j:
                r *= v
    elif kind in ("OR", "NOR"):
        for k, v in enumerate(q):
            if k != j:
                r *= 1 - v
    elif kind not in ("XOR", "XNOR", "BUF", "NOT"):
        raise ValueError(kind)
    return r


def transition_densities(c, p: Mapping[str, Fraction], d: Mapping[str, Fraction]):
    """Return (P, D): the probability and the transition density of every node."""
    P: dict[str, Fraction] = {}
    D: dict[str, Fraction] = {}
    for x in c.inputs:
        P[x], D[x] = Fraction(p[x]), Fraction(d[x])  # @line L1
    for y, kind, fins in c.gates:  # @line L2
        q = [P[z] for z in fins]
        P[y] = gate_probability(kind, q)  # @line L3
        D[y] = Fraction(0)  # @line L4
        for j, z in enumerate(fins):  # @line L5
            b = boolean_difference_probability(kind, q, j)  # @line L6
            D[y] += b * D[z]  # @line L7
    return P, D  # @line L8
