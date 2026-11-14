# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/generalized-symbolic-trajectory-evaluation/. The authors are listed in prov/KNN3V9.jsonl.
"""Generalized symbolic trajectory evaluation (Yang and Seger) under the strong semantics.

An assertion graph has vertices, an initial vertex v0, and edges (src, dst, ant,
cons). The antecedent ant and the consequent cons of an edge are lists of
constraints (node, e, g), read "if g then node is e" at the time the edge is
taken, with e and g BDDs over the symbolic variables. The graph says: for every
path e0 e1 ... ek from v0 and every run that meets ant(ei) at time i for all
i <= k, the run meets cons(ek) at time k.

The check computes for each edge a ternary symbolic state sim(e), the least
information common to all states in which a run can take e. Values are
dual-rail pairs (one, zero) of BDDs on the lattice X below 0 and 1 below TOP,
as on the STE page. The fixed point starts at TOP (no state) and goes down.

Precondition: gates in topological order. Every round costs O(E (N + P)) dual-
rail operations, and there are at most 2 N E + 1 rounds.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from bdd import BDD, FALSE, TRUE

Val = tuple[int, int]          # (one, zero)
XV: Val = (FALSE, FALSE)
TV: Val = (TRUE, TRUE)


@dataclass(frozen=True)
class Circuit:
    """inputs; latches as (name, next_state_node); gates as (name, op, fanins) in topological order."""

    inputs: tuple[str, ...]
    latches: tuple[tuple[str, str], ...]
    gates: tuple[tuple[str, str, tuple[str, ...]], ...]

    def nodes(self) -> list[str]:
        return list(self.inputs) + [s for s, _ in self.latches] + [g for g, _, _ in self.gates]


Constraint = tuple[str, int, int]             # (node, value BDD, guard BDD)


@dataclass(frozen=True)
class Edge:
    src: int
    dst: int
    ant: tuple[Constraint, ...] = ()
    cons: tuple[Constraint, ...] = ()


@dataclass
class Result:
    passed: bool
    residual: int                  # the assignments where some edge fails
    failing: dict[int, int]        # edge index -> its own residual
    sim: list[dict[str, Val]]      # the fixed point, one state per edge
    rounds: int


def join(m: BDD, a: Val, b: Val) -> Val:
    return (m.disj(a[0], b[0]), m.disj(a[1], b[1]))


def meet(m: BDD, a: Val, b: Val) -> Val:
    return (m.conj(a[0], b[0]), m.conj(a[1], b[1]))


def leq(m: BDD, a: Val, b: Val) -> int:
    return m.conj(m.disj(m.neg(a[0]), b[0]), m.disj(m.neg(a[1]), b[1]))


def gate_value(m: BDD, op: str, args: list[Val]) -> Val:
    """The monotone ternary extension of a gate on dual-rail values."""
    if op == "BUF":
        return args[0]
    if op == "NOT":
        return (args[0][1], args[0][0])
    if op in ("AND", "NAND", "OR", "NOR"):
        conj_like = op in ("AND", "NAND")
        one, zero = (TRUE, FALSE) if conj_like else (FALSE, TRUE)
        for a1, a0 in args:
            if conj_like:
                one, zero = m.conj(one, a1), m.disj(zero, a0)
            else:
                one, zero = m.disj(one, a1), m.conj(zero, a0)
        return (zero, one) if op in ("NAND", "NOR") else (one, zero)
    if op in ("XOR", "XNOR"):
        one, zero = FALSE, TRUE
        for a1, a0 in args:
            one, zero = (m.disj(m.conj(one, a0), m.conj(zero, a1)),
                         m.disj(m.conj(one, a1), m.conj(zero, a0)))
        return (zero, one) if op == "XNOR" else (one, zero)
    raise ValueError(f"unknown gate type {op}")


def delta(m: BDD, cs: tuple[Constraint, ...]) -> dict[str, Val]:
    """The least values that a list of constraints asks for at one time."""
    out: dict[str, Val] = {}
    for u, e, g in cs:
        out[u] = join(m, out.get(u, XV), (m.conj(g, e), m.conj(g, m.neg(e))))
    return out


def empty(m: BDD, state: dict[str, Val]) -> int:
    """The assignments where some node is TOP, that is, where the state set is empty."""
    bad = FALSE
    for one, zero in state.values():
        bad = m.disj(bad, m.conj(one, zero))
    return bad


def empty_where_top(m: BDD, state: dict[str, Val], bad: int = FALSE) -> dict[str, Val]:
    """Where bad holds or some node is TOP the state is empty, so set every node to TOP there."""
    bad = m.disj(bad, empty(m, state))
    return {u: (m.disj(one, bad), m.disj(zero, bad)) for u, (one, zero) in state.items()}


def gste(c: Circuit, m: BDD, edges: list[Edge], v0: int = 0) -> Result:
    """Check the assertion graph given by edges, with initial vertex v0, on the circuit c."""
    nodes = c.nodes()
    top = {u: TV for u in nodes}
    allx = {u: XV for u in nodes}
    ants = [delta(m, e.ant) for e in edges]
    sim = [dict(top) for _ in edges]                                       # @line L1
    rounds = 0
    while True:                                                            # @line L2
        rounds += 1
        pre_of: dict[int, dict[str, Val]] = {}
        for v in {e.src for e in edges}:
            pre = dict(allx) if v == v0 else dict(top)
            for j, e in enumerate(edges):
                if e.dst == v:
                    pre = {u: meet(m, pre[u], sim[j][u]) for u in nodes}
            pre_of[v] = pre
        new = []
        for i, e in enumerate(edges):                                      # @line L3
            pre = pre_of[e.src]                                            # @line L4
            sigma = {u: ants[i].get(u, XV) for u in nodes}                 # @line L5
            for s, nxt in c.latches:
                sigma[s] = join(m, sigma[s], pre[nxt])
            for g, op, fanins in c.gates:                                  # @line L6
                sigma[g] = join(m, sigma[g], gate_value(m, op, [sigma[f] for f in fanins]))
            new.append(empty_where_top(m, sigma, empty(m, pre)))           # @line L7
        if new == sim:                                                     # @line L8
            break
        sim = new
    failing: dict[int, int] = {}
    residual = FALSE
    for i, e in enumerate(edges):                                          # @line L9
        ok = TRUE
        for u, v in delta(m, e.cons).items():
            ok = m.conj(ok, leq(m, v, sim[i][u]))
        failing[i] = m.neg(ok)
        residual = m.disj(residual, failing[i])
    return Result(residual == FALSE, residual, failing, sim, rounds)       # @line L10


def is_(node: str, e: int, guard: int = TRUE) -> Constraint:
    """The constraint "if guard then node is e" at the time of the edge."""
    return (node, e, guard)


def counterexample(m: BDD, r: Result) -> Optional[dict[int, int]]:
    return m.sat_one(r.residual)
