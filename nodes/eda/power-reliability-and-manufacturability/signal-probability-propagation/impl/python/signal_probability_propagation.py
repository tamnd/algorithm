# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/signal-probability-propagation/. The authors are listed in prov/CC4R1Y.jsonl.
"""Signal probability propagation (Parker and McCluskey 1975).

The probability of a node is the probability that it is 1 when each primary
input x is 1 with probability p[x], independently of the others.

signal_probabilities(c, p, mode) runs the gate formulas in topological order:

- mode "numeric": one Fraction per node. Exact when no gate has two fanins
  whose supports meet (for example a fanout-free circuit), wrong in general.
- mode "polynomial": one multilinear polynomial per node in the input
  probabilities, with exponent suppression (x^k = x) after each product, then
  evaluated at p. Exact on every circuit, with up to 2^n terms per node.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence, Union


class Poly:
    """A polynomial with integer coefficients over the input names, kept suppressed.

    A monomial is a frozenset of input names, so x * x = x by construction.
    """

    __slots__ = ("terms",)

    def __init__(self, terms: Mapping[frozenset[str], int]) -> None:
        self.terms = {m: c for m, c in terms.items() if c != 0}

    @staticmethod
    def var(name: str) -> "Poly":
        return Poly({frozenset([name]): 1})

    @staticmethod
    def _lift(other: Union["Poly", int]) -> "Poly":
        return other if isinstance(other, Poly) else Poly({frozenset(): other})

    def __add__(self, other: Union["Poly", int]) -> "Poly":
        r = dict(self.terms)
        for m, c in Poly._lift(other).terms.items():
            r[m] = r.get(m, 0) + c
        return Poly(r)

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other: Union["Poly", int]) -> "Poly":
        return self + (-Poly._lift(other))

    def __rsub__(self, other: int) -> "Poly":
        return Poly._lift(other) + (-self)

    def __mul__(self, other: Union["Poly", int]) -> "Poly":
        r: dict[frozenset[str], int] = {}
        for ma, ca in self.terms.items():
            for mb, cb in Poly._lift(other).terms.items():
                m = ma | mb  # exponent suppression
                r[m] = r.get(m, 0) + ca * cb
        return Poly(r)

    __rmul__ = __mul__

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Poly) and self.terms == other.terms

    def __repr__(self) -> str:
        return f"Poly({self.terms!r})"

    def evaluate(self, p: Mapping[str, Fraction]) -> Fraction:
        total = Fraction(0)
        for m, c in self.terms.items():
            t = Fraction(c)
            for x in m:
                t *= p[x]
            total += t
        return total


Value = Union[Fraction, Poly]


def gate_formula(kind: str, q: Sequence[Value]) -> Value:
    """P(output = 1) from P(input = 1) = q, by the formulas for independent gate inputs."""
    if kind in ("AND", "NAND"):
        r = q[0]
        for v in q[1:]:
            r = r * v  # @line L5
    elif kind in ("OR", "NOR"):
        r = 1 - q[0]
        for v in q[1:]:
            r = r * (1 - v)
        r = 1 - r  # @line L6
    elif kind in ("XOR", "XNOR"):
        r = q[0]
        for v in q[1:]:
            r = r + v - 2 * r * v  # @line L7
    elif kind in ("BUF", "NOT"):
        r = q[0]  # @line L8
    else:
        raise ValueError(kind)
    if kind in ("NAND", "NOR", "XNOR", "NOT"):
        r = 1 - r  # @line L9
    return r


def signal_probabilities(c, p: Mapping[str, Fraction], mode: str = "numeric") -> dict[str, Fraction]:
    """P(node = 1) for every node of the netlist.Circuit c."""
    if mode not in ("numeric", "polynomial"):
        raise ValueError(mode)
    val: dict[str, Value] = {}
    for x in c.inputs:  # @line L1
        val[x] = Fraction(p[x]) if mode == "numeric" else Poly.var(x)  # @line L2
    for y, kind, fins in c.gates:  # @line L3
        q = [val[z] for z in fins]  # @line L4
        val[y] = gate_formula(kind, q)  # @line L10
    if mode == "polynomial":  # @line L11
        return {v: f.evaluate(p) for v, f in val.items()}  # @line L12
    return val  # @line L13


def probability_polynomials(c) -> dict[str, Poly]:
    """The suppressed polynomial of every node, before evaluation."""
    val: dict[str, Poly] = {x: Poly.var(x) for x in c.inputs}
    for y, kind, fins in c.gates:
        val[y] = gate_formula(kind, [val[z] for z in fins])
    return val


def propagate(c, p: Mapping[str, Fraction]) -> dict[str, Fraction]:
    """The numeric mode."""
    return signal_probabilities(c, p, "numeric")


def exact_probabilities(c, p: Mapping[str, Fraction]) -> dict[str, Fraction]:
    """The polynomial mode."""
    return signal_probabilities(c, p, "polynomial")
