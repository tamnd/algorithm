# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bdd-switching-activity-estimation/. The authors are listed in prov/D7CR16.jsonl.
"""BDD-based switching activity estimation (Ghosh, Devadas, Keutzer and White 1992).

A clock cycle takes the inputs from x to x'. For each input i the pair
(x_i, x'_i) has the joint law J[i][(v, v')], and the pairs of different inputs
are independent. Input i has BDD variable 2i for x_i and 2i + 1 for x'_i, so
the two copies of an input are next to each other in the order.

switching_activity(c, J) returns, for every node y, the exact probability that
y changes in the cycle under the zero-delay model, P(y(x) XOR y(x')).

transport_activity(c, J) returns the exact expected number of transitions of
every node in the cycle under the transport delay model of netlist.waveforms,
glitches included, from the BDDs of the node values at each time step.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Mapping, Sequence

from bdd import BDD

Joint = Mapping[tuple[int, int], Fraction]


def gate_bdd(m: BDD, kind: str, fs: Sequence[int]) -> int:
    """The BDD of a gate applied to the BDDs fs of its fanins."""
    r = fs[0]
    for f in fs[1:]:
        if kind in ("AND", "NAND"):
            r = m.AND(r, f)
        elif kind in ("OR", "NOR"):
            r = m.OR(r, f)
        elif kind in ("XOR", "XNOR"):
            r = m.XOR(r, f)
        else:
            raise ValueError(kind)
    return m.NOT(r) if kind in ("NOT", "NAND", "NOR", "XNOR") else r


def pair_probability(m: BDD, u: int, J: Sequence[Joint], memo: dict[int, Fraction]) -> Fraction:
    """P(f_u = 1) when the pairs (x_i, x'_i) are independent with laws J[i]."""

    def child(a: int, v: int, b: int) -> int:
        """The cofactor of a at variable v = b (a itself if a does not test v)."""
        if m.var_of[a] != v:
            return a
        return m.hi[a] if b else m.lo[a]

    def rec(a: int) -> Fraction:
        if m.is_terminal(a):
            return Fraction(a)  # @line L8
        r = memo.get(a)
        if r is not None:
            return r
        v = m.var_of[a]
        i = v // 2
        r = Fraction(0)
        if v % 2 == 0:  # @line L9
            for (b, b2), w in J[i].items():
                if w:
                    r += w * rec(child(child(a, v, b), v + 1, b2))
        else:  # @line L10
            for (b, b2), w in J[i].items():
                if w:
                    r += w * rec(child(a, v, b2))
        memo[a] = r
        return r

    return rec(u)


def switching_activity(c, J: Sequence[Joint]) -> dict[str, Fraction]:
    """Zero-delay switching activity of every node of the netlist.Circuit c."""
    m = BDD()
    F: dict[str, int] = {}
    F2: dict[str, int] = {}
    alpha: dict[str, Fraction] = {}
    memo: dict[int, Fraction] = {}
    for i, x in enumerate(c.inputs):  # @line L1
        F[x], F2[x] = m.var(2 * i), m.var(2 * i + 1)  # @line L2
        alpha[x] = pair_probability(m, m.XOR(F[x], F2[x]), J, memo)
    for y, kind, fins in c.gates:  # @line L3
        F[y] = gate_bdd(m, kind, [F[z] for z in fins])  # @line L4
        F2[y] = gate_bdd(m, kind, [F2[z] for z in fins])
        A = m.XOR(F[y], F2[y])  # @line L5
        alpha[y] = pair_probability(m, A, J, memo)  # @line L6
    return alpha  # @line L7


def transport_activity(c, J: Sequence[Joint]) -> dict[str, Fraction]:
    """Expected transitions per cycle under transport delay, by symbolic simulation."""
    m = BDD()
    old: dict[str, int] = {}
    for i, x in enumerate(c.inputs):
        old[x] = m.var(2 * i)
    for y, kind, fins in c.gates:
        old[y] = gate_bdd(m, kind, [old[z] for z in fins])
    horizon = max(c.arrival().values())
    wave: dict[str, list[int]] = {}
    for i, x in enumerate(c.inputs):
        wave[x] = [old[x]] + [m.var(2 * i + 1)] * (horizon + 1)  # index 0 is time -1
    for y, kind, fins in c.gates:
        d = c.delay[y]
        w = [old[y]]
        for t in range(horizon + 1):
            s = t - d
            w.append(gate_bdd(m, kind, [wave[z][s + 1] if s >= -1 else old[z] for z in fins]))
        wave[y] = w
    memo: dict[int, Fraction] = {}
    out = {}
    for v, w in wave.items():
        out[v] = sum((pair_probability(m, m.XOR(w[t], w[t - 1]), J, memo) for t in range(1, len(w))), Fraction(0))
    return out


def independent_pairs(p: Mapping[str, Fraction], inputs: Sequence[str]) -> list[Joint]:
    """Laws J[i] for inputs that are fresh and independent in each cycle."""
    J = []
    for x in inputs:
        q = Fraction(p[x])
        J.append({(a, b): (q if a else 1 - q) * (q if b else 1 - q) for a in (0, 1) for b in (0, 1)})
    return J
