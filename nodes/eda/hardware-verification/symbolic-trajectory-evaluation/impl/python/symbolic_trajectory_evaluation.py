# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbolic-trajectory-evaluation/. The authors are listed in prov/NEAHJQ.jsonl.
"""Symbolic trajectory evaluation (Seger and Bryant 1995) on a gate-level circuit.

Values lie in the lattice X below 0 and 1, and 0 and 1 below TOP. A symbolic
value is a dual-rail pair (one, zero) of BDDs over the symbolic variables: for
an assignment phi of the variables the node is X when neither holds, 1 when only
one holds, 0 when only zero holds, and TOP when both hold. The join is the OR of
the rails, and a <= b is (a.one -> b.one) and (a.zero -> b.zero).

An assertion A ==> C is given by two lists of constraints (t, node, e, g), each
meaning "if g then node is e at time t", with e and g BDDs over the variables.
The check builds the defining trajectory of A by ternary simulation and tests
that the defining sequence of C lies below it, for each phi at once.

Precondition: gates in topological order, as in the Circuit of the page. Cost:
O(d P) dual-rail operations for depth d and P gate inputs, each a BDD operation
on BDDs over the variables of the assertion only.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from bdd import BDD, FALSE, TRUE

Val = tuple[int, int]          # (one, zero)
XV: Val = (FALSE, FALSE)


@dataclass(frozen=True)
class Circuit:
    """inputs; latches as (name, next_state_node); gates as (name, op, fanins) in topological order."""

    inputs: tuple[str, ...]
    latches: tuple[tuple[str, str], ...]
    gates: tuple[tuple[str, str, tuple[str, ...]], ...]


Constraint = tuple[int, str, int, int]   # (time, node, value BDD, guard BDD)


@dataclass
class Result:
    passed: bool
    residual: int                 # the assignments phi where the assertion fails
    antecedent_failure: int       # the assignments phi where the trajectory reaches TOP
    trajectory: list[dict[str, Val]]


def join(m: BDD, a: Val, b: Val) -> Val:
    return (m.disj(a[0], b[0]), m.disj(a[1], b[1]))


def leq(m: BDD, a: Val, b: Val) -> int:
    """The BDD of the assignments where a is below or equal to b."""
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
            if conj_like:          # 1 when all are 1, 0 when some is 0
                one, zero = m.conj(one, a1), m.disj(zero, a0)
            else:                  # 1 when some is 1, 0 when all are 0
                one, zero = m.disj(one, a1), m.conj(zero, a0)
        return (zero, one) if op in ("NAND", "NOR") else (one, zero)
    if op in ("XOR", "XNOR"):
        one, zero = FALSE, TRUE
        for a1, a0 in args:
            one, zero = (m.disj(m.conj(one, a0), m.conj(zero, a1)),
                         m.disj(m.conj(one, a1), m.conj(zero, a0)))
        return (zero, one) if op == "XNOR" else (one, zero)
    raise ValueError(f"unknown gate type {op}")


def defining_sequence(m: BDD, cs: list[Constraint], depth: int) -> list[dict[str, Val]]:
    """delta: for each time, the least values that the constraints ask for."""
    seq: list[dict[str, Val]] = [dict() for _ in range(depth + 1)]
    for t, u, e, g in cs:
        v = (m.conj(g, e), m.conj(g, m.neg(e)))
        seq[t][u] = join(m, seq[t].get(u, XV), v)
    return seq


def ste(c: Circuit, m: BDD, antecedent: list[Constraint], consequent: list[Constraint]) -> Result:
    """Check the assertion antecedent ==> consequent on the circuit c."""
    depth = max([t for t, *_ in antecedent + consequent], default=0)       # @line L1
    da = defining_sequence(m, antecedent, depth)
    dc = defining_sequence(m, consequent, depth)
    traj: list[dict[str, Val]] = []
    for t in range(depth + 1):                                            # @line L2
        tau: dict[str, Val] = {}
        for u in list(c.inputs) + [s for s, _ in c.latches] + [g for g, _, _ in c.gates]:
            tau[u] = da[t].get(u, XV)                                     # @line L3
        if t > 0:
            for s, nxt in c.latches:                                      # @line L4
                tau[s] = join(m, tau[s], traj[t - 1][nxt])
        for g, op, fanins in c.gates:                                     # @line L5
            tau[g] = join(m, tau[g], gate_value(m, op, [tau[f] for f in fanins]))
        traj.append(tau)
    af = FALSE
    for tau in traj:                                                      # @line L6
        for one, zero in tau.values():
            af = m.disj(af, m.conj(one, zero))
    ok = TRUE
    for t in range(depth + 1):                                            # @line L7
        for u, v in dc[t].items():
            ok = m.conj(ok, leq(m, v, traj[t][u]))
    residual = m.neg(m.disj(ok, af))                                      # @line L8
    return Result(residual == FALSE, residual, af, traj)


def is_(t: int, node: str, e: int, guard: int = TRUE) -> Constraint:
    """The constraint "if guard then node is e at time t"."""
    return (t, node, e, guard)


def counterexample(m: BDD, r: Result) -> Optional[dict[int, int]]:
    """One assignment of the symbolic variables where the assertion fails."""
    return m.sat_one(r.residual)
