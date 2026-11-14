# SPDX-License-Identifier: MIT
# Shared helper of the sim1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Gate netlists and gate functions for the logic simulation pages.

A value is 0, 1 or X = 2, where X means "unknown, it can be 0 or 1".
A circuit has named primary inputs, gates (out, op, ins) and named primary
outputs. Every net is a primary input or the output of exactly one gate.
The gates may form loops, but direct_eval needs a circuit without loops.
This module holds no simulation algorithm. It gives the gate functions, the
netlist, a direct recursive evaluation that serves as the reference, random
circuits for tests and the binary completions of a three-valued vector.
"""

from __future__ import annotations

import itertools
import random
from typing import Dict, Iterator, List, Optional, Sequence, Tuple

X = 2
OPS = ("AND", "OR", "NAND", "NOR", "XOR", "XNOR", "NOT", "BUF")
ONE_INPUT = ("NOT", "BUF")


def eval2(op: str, vals: Sequence[int]) -> int:
    """The gate function on values in {0, 1}."""
    if op == "AND":
        return int(all(vals))
    if op == "OR":
        return int(any(vals))
    if op == "NAND":
        return 1 - int(all(vals))
    if op == "NOR":
        return 1 - int(any(vals))
    if op == "XOR":
        return sum(vals) & 1
    if op == "XNOR":
        return 1 - (sum(vals) & 1)
    if op == "NOT":
        return 1 - vals[0]
    if op == "BUF":
        return vals[0]
    raise ValueError(f"unknown gate {op}")


def not3(v: int) -> int:
    return X if v == X else 1 - v


def eval3(op: str, vals: Sequence[int]) -> int:
    """Kleene's strong three-valued gate function on values in {0, 1, X}."""
    if op in ("AND", "NAND"):
        r = 0 if 0 in vals else (X if X in vals else 1)
        return r if op == "AND" else not3(r)
    if op in ("OR", "NOR"):
        r = 1 if 1 in vals else (X if X in vals else 0)
        return r if op == "OR" else not3(r)
    if op in ("XOR", "XNOR"):
        r = X if X in vals else sum(vals) & 1
        return r if op == "XOR" else not3(r)
    if op == "NOT":
        return not3(vals[0])
    if op == "BUF":
        return vals[0]
    raise ValueError(f"unknown gate {op}")


class Circuit:
    """A gate netlist. gates is a list of (output net, op, list of input nets)."""

    def __init__(self, inputs: Sequence[str], gates: Sequence[Tuple[str, str, Sequence[str]]], outputs: Sequence[str]):
        self.inputs: List[str] = list(inputs)
        self.gates: List[Tuple[str, str, List[str]]] = [(out, op, list(ins)) for out, op, ins in gates]
        self.outputs: List[str] = list(outputs)
        self.driver: Dict[str, int] = {}
        for i, (out, op, ins) in enumerate(self.gates):
            if op not in OPS:
                raise ValueError(f"unknown gate {op}")
            if not ins or (op in ONE_INPUT and len(ins) != 1):
                raise ValueError(f"gate {out} has a wrong number of inputs")
            if out in self.driver or out in self.inputs:
                raise ValueError(f"net {out} has two drivers")
            self.driver[out] = i
        self.nets: List[str] = self.inputs + [g[0] for g in self.gates]
        self.fanout: Dict[str, List[int]] = {n: [] for n in self.nets}
        for i, (out, op, ins) in enumerate(self.gates):
            for n in ins:
                if n not in self.fanout:
                    raise ValueError(f"net {n} has no driver")
                if i not in self.fanout[n]:
                    self.fanout[n].append(i)
        for n in self.outputs:
            if n not in self.fanout:
                raise ValueError(f"output {n} has no driver")

    def is_acyclic(self) -> bool:
        """True when no gate depends on its own output (three-colour depth-first search)."""
        colour = [0] * len(self.gates)
        for root in range(len(self.gates)):
            if colour[root]:
                continue
            colour[root] = 1
            stack = [(root, iter(self.gates[root][2]))]
            while stack:
                g, it = stack[-1]
                nxt = None
                for n in it:
                    if n in self.driver:
                        nxt = self.driver[n]
                        break
                if nxt is None:
                    colour[g] = 2
                    stack.pop()
                elif colour[nxt] == 1:
                    return False
                elif colour[nxt] == 0:
                    colour[nxt] = 1
                    stack.append((nxt, iter(self.gates[nxt][2])))
        return True

    def direct_eval(self, vec: Dict[str, int], three: bool = False) -> Dict[str, int]:
        """Value of every net, each computed from its definition with memoization."""
        f = eval3 if three else eval2
        val: Dict[str, int] = {n: vec[n] for n in self.inputs}
        busy = set()

        def get(n: str) -> int:
            if n in val:
                return val[n]
            if n in busy:
                raise ValueError("the circuit has a loop")
            busy.add(n)
            out, op, ins = self.gates[self.driver[n]]
            val[n] = f(op, [get(m) for m in ins])
            return val[n]

        for n in self.nets:
            get(n)
        return val


def random_circuit(rng: random.Random, n_inputs: int, n_gates: int, n_outputs: Optional[int] = None,
                   loops: bool = False, ops: Sequence[str] = OPS) -> Circuit:
    """A random circuit. Without loops, gate k reads only inputs and gates 0..k-1."""
    inputs = [f"i{k}" for k in range(n_inputs)]
    names = [f"g{k}" for k in range(n_gates)]
    gates = []
    for k in range(n_gates):
        op = rng.choice(ops)
        pool = inputs + (names if loops else names[:k])
        arity = 1 if op in ONE_INPUT else rng.randint(2, 3)
        ins = rng.sample(pool, min(arity, len(pool)))
        if op not in ONE_INPUT and len(ins) < 2:
            op = "BUF"
        gates.append((names[k], op, ins))
    if n_outputs is None:
        n_outputs = min(3, n_gates)
    return Circuit(inputs, gates, names[n_gates - n_outputs:])


def all_vectors(names: Sequence[str]) -> Iterator[Dict[str, int]]:
    """Every assignment of 0 and 1 to the names."""
    for bits in itertools.product((0, 1), repeat=len(names)):
        yield dict(zip(names, bits))


def completions(vec: Dict[str, int]) -> Iterator[Dict[str, int]]:
    """Every binary vector that agrees with vec wherever vec is not X."""
    free = [n for n, v in vec.items() if v == X]
    for bits in itertools.product((0, 1), repeat=len(free)):
        out = dict(vec)
        out.update(zip(free, bits))
        yield out
