# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symbolic-simulation/. The authors are listed in prov/HYGZ61.jsonl.
"""Symbolic simulation of a synchronous gate-level circuit with BDDs.

Each primary input gets a fresh Boolean variable in each cycle, and each latch
starts from a constant or from a fresh variable. One pass over the gates in
topological order per cycle gives every node a BDD over these variables, so the
BDD of an output in cycle t is the function that maps every input sequence (and
every initial state) to the value of that output in cycle t.

Precondition: the gates are listed in topological order, every gate input is a
primary input, a latch or an earlier gate, and the circuit has no combinational
cycle. Cost: one BDD operation per gate and cycle, each O(|f| |g|) for operand
sizes |f| and |g|; the sizes can grow exponentially in the number of variables.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from bdd import BDD, FALSE, TRUE

OPS = ("BUF", "NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR")


@dataclass(frozen=True)
class Circuit:
    """A synchronous circuit with one clock.

    latches holds (name, next_state_node, init) with init 0, 1 or None; None
    means that the initial value is unknown and gets its own variable.
    gates holds (name, op, fanins) in topological order.
    """

    inputs: tuple[str, ...]
    latches: tuple[tuple[str, str, Optional[int]], ...]
    gates: tuple[tuple[str, str, tuple[str, ...]], ...]
    outputs: tuple[str, ...]


@dataclass
class Trace:
    mgr: BDD
    outputs: list[dict[str, int]]          # outputs[t][o] is the BDD of o in cycle t
    states: list[dict[str, int]]           # states[t][s] is the BDD of latch s at the start of cycle t
    variables: dict[tuple, int] = field(default_factory=dict)  # ("init", s) or ("in", x, t) -> variable


def apply_gate(mgr: BDD, op: str, args: list[int]) -> int:
    """The BDD of one gate applied to the BDDs of its fanins."""
    if op == "BUF":
        return args[0]
    if op == "NOT":
        return mgr.neg(args[0])
    if op in ("AND", "NAND"):
        r = TRUE
        for a in args:
            r = mgr.conj(r, a)
        return mgr.neg(r) if op == "NAND" else r
    if op in ("OR", "NOR"):
        r = FALSE
        for a in args:
            r = mgr.disj(r, a)
        return mgr.neg(r) if op == "NOR" else r
    if op in ("XOR", "XNOR"):
        r = FALSE
        for a in args:
            r = mgr.xor(r, a)
        return mgr.neg(r) if op == "XNOR" else r
    raise ValueError(f"unknown gate type {op}")


def symbolic_simulation(c: Circuit, k: int, mgr: Optional[BDD] = None) -> Trace:
    """Simulate c for k cycles with symbolic inputs and return the BDDs.

    The variable order is: the unknown initial latch values in latch order, then
    the inputs of cycle 0, cycle 1, and so on.
    """
    mgr = mgr or BDD()
    variables: dict[tuple, int] = {}
    nxt = 0
    state: dict[str, int] = {}
    for s, _, init in c.latches:                               # @line L1
        if init is None:
            variables[("init", s)] = nxt
            state[s] = mgr.var(nxt)
            nxt += 1
        else:
            state[s] = TRUE if init else FALSE
    outputs: list[dict[str, int]] = []
    states: list[dict[str, int]] = []
    for t in range(k):                                          # @line L2
        value: dict[str, int] = {}
        for x in c.inputs:                                      # @line L3
            variables[("in", x, t)] = nxt
            value[x] = mgr.var(nxt)
            nxt += 1
        states.append(dict(state))
        for s, _, _ in c.latches:                               # @line L4
            value[s] = state[s]
        for name, op, fanins in c.gates:                        # @line L5
            value[name] = apply_gate(mgr, op, [value[f] for f in fanins])
        outputs.append({o: value[o] for o in c.outputs})        # @line L6
        state = {s: value[n] for s, n, _ in c.latches}          # @line L7
    return Trace(mgr, outputs, states, variables)               # @line L8


def instance(trace: Trace, init: dict[str, int], seq: list[dict[str, int]]) -> dict[int, int]:
    """The variable assignment for one concrete run (unknown initial values and inputs)."""
    a: dict[int, int] = {}
    for key, v in trace.variables.items():
        if key[0] == "init":
            a[v] = init[key[1]]
        else:
            a[v] = seq[key[2]][key[1]]
    return a
