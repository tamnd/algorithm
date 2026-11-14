# SPDX-License-Identifier: MIT
# Shared helper of the td1 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Gate-level combinational circuits with single stuck-at faults.

A circuit is built from named primary inputs, gates in topological order and
named primary outputs. Every place where a fault can sit is a *line*:

- one stem line for each primary input and for each gate output;
- when a net feeds two or more sinks (gate input pins or primary outputs), one
  branch line for each sink. A net with one sink has no branch line, and the
  sink reads the stem.

Lines are numbered 0, 1, ... in topological order, so every line comes after
the lines it reads. A single stuck-at fault is a pair (line, value). Values are
0, 1 and X (unknown), with X = 2. Building a circuit and simulating one vector
take O(L + P) time for L lines and P gate input pins.

This module holds the circuit model, plain simulation of the good circuit and
of one faulty circuit, and brute-force detection over all input vectors. It
holds no test generation or fault simulation algorithm.
"""

from __future__ import annotations

import random
from itertools import product
from typing import Optional, Sequence

X = 2
OPS = ("AND", "OR", "NAND", "NOR", "NOT", "BUF", "XOR", "XNOR")
_CONTROL = {"AND": 0, "NAND": 0, "OR": 1, "NOR": 1}
_INVERT = {"AND": 0, "OR": 0, "NAND": 1, "NOR": 1, "NOT": 1, "BUF": 0, "XOR": 0, "XNOR": 1}

Fault = tuple[int, int]


def controlling(op: str) -> Optional[int]:
    """The controlling input value of a gate type, or None (NOT, BUF, XOR, XNOR)."""
    return _CONTROL.get(op)


def inversion(op: str) -> int:
    """1 if the gate type inverts (NAND, NOR, NOT, XNOR), else 0."""
    return _INVERT[op]


def eval_gate(op: str, vals: Sequence[int]) -> int:
    """Three-valued output of a gate for input values in {0, 1, X}."""
    if op in ("XOR", "XNOR"):
        if X in vals:
            return X
        r = 0
        for v in vals:
            r ^= v
        return r ^ _INVERT[op]
    if op in ("NOT", "BUF"):
        v = vals[0]
        return X if v == X else v ^ _INVERT[op]
    c = _CONTROL[op]
    if c in vals:
        r = c
    elif X in vals:
        return X
    else:
        r = 1 - c
    return r ^ _INVERT[op]


class Circuit:
    """A combinational circuit as a DAG of lines (see the module comment)."""

    def __init__(
        self,
        inputs: Sequence[str],
        gates: Sequence[tuple[str, str, Sequence[str]]],
        outputs: Sequence[str],
    ) -> None:
        nets = list(inputs) + [g[0] for g in gates]
        if len(set(nets)) != len(nets):
            raise ValueError("net names must be unique")
        defined = set(inputs)
        sinks: dict[str, list[tuple[str, int, int]]] = {n: [] for n in nets}
        for gi, (name, op, fanin) in enumerate(gates):
            if op not in OPS:
                raise ValueError(f"unknown gate type {op}")
            if (op in ("NOT", "BUF")) != (len(fanin) == 1) or not fanin:
                raise ValueError(f"wrong number of inputs for {name}")
            for pin, src in enumerate(fanin):
                if src not in defined:
                    raise ValueError(f"{src} is used before it is defined")
                sinks[src].append(("gate", gi, pin))
            defined.add(name)
        for k, src in enumerate(outputs):
            if src not in defined:
                raise ValueError(f"unknown output {src}")
            sinks[src].append(("po", k, 0))

        self.name: list[str] = []
        self.kind: list[str] = []
        self.op: list[str] = []
        self.fanin: list[list[int]] = []
        self.index: dict[str, int] = {}
        pin_line: dict[tuple[str, int, int], int] = {}

        def add(name: str, kind: str, op: str, fanin: list[int]) -> int:
            line = len(self.name)
            self.name.append(name)
            self.kind.append(kind)
            self.op.append(op)
            self.fanin.append(fanin)
            self.index[name] = line
            return line

        def add_net(net: str, kind: str, op: str, fanin: list[int]) -> None:
            stem = add(net, kind, op, fanin)
            sk = sinks[net]
            if len(sk) < 2:
                for s in sk:
                    pin_line[s] = stem
                return
            for s in sk:
                if s[0] == "po":
                    label = f"{net}>out{s[1]}" if len(outputs) > 1 else f"{net}>out"
                else:
                    gname = gates[s[1]][0]
                    same = sum(1 for t in sk if t[0] == "gate" and t[1] == s[1])
                    label = f"{net}>{gname}" + (f".{s[2]}" if same > 1 else "")
                pin_line[s] = add(label, "branch", "BUF", [stem])

        self.pi: list[int] = []
        for net in inputs:
            add_net(net, "pi", "PI", [])
            self.pi.append(self.index[net])
        for gi, (name, op, fanin) in enumerate(gates):
            add_net(name, "gate", op, [pin_line[("gate", gi, p)] for p in range(len(fanin))])
        self.po: list[int] = [pin_line[("po", k, 0)] for k in range(len(outputs))]

        self.n_lines = len(self.name)
        self.fanout: list[list[int]] = [[] for _ in range(self.n_lines)]
        for line in range(self.n_lines):
            for j in self.fanin[line]:
                self.fanout[j].append(line)
        self.level = [0] * self.n_lines
        for line in range(self.n_lines):
            if self.fanin[line]:
                self.level[line] = 1 + max(self.level[j] for j in self.fanin[line])

    def line(self, name: str) -> int:
        return self.index[name]

    def faults(self) -> list[Fault]:
        """All 2L single stuck-at faults, in line order."""
        return [(line, v) for line in range(self.n_lines) for v in (0, 1)]

    def fault_name(self, fault: Fault) -> str:
        return f"{self.name[fault[0]]}/{fault[1]}"

    def simulate(self, vector: Sequence[int], fault: Optional[Fault] = None) -> list[int]:
        """Values of all lines for one input vector (entries 0, 1 or X), with an optional fault."""
        vals = [X] * self.n_lines
        k = 0
        for line in range(self.n_lines):
            if self.kind[line] == "pi":
                v = vector[k]
                k += 1
            else:
                v = eval_gate(self.op[line], [vals[j] for j in self.fanin[line]])
            if fault is not None and fault[0] == line:
                v = fault[1]
            vals[line] = v
        return vals

    def outputs(self, vector: Sequence[int], fault: Optional[Fault] = None) -> tuple[int, ...]:
        vals = self.simulate(vector, fault)
        return tuple(vals[o] for o in self.po)

    def detects(self, vector: Sequence[int], fault: Fault) -> bool:
        """True if some output has a known value in both circuits and the values differ."""
        good = self.outputs(vector)
        bad = self.outputs(vector, fault)
        return any(g != X and b != X and g != b for g, b in zip(good, bad))

    def all_vectors(self) -> list[tuple[int, ...]]:
        return list(product((0, 1), repeat=len(self.pi)))

    def detecting_vectors(self, fault: Fault) -> list[tuple[int, ...]]:
        """Brute force: every two-valued input vector that detects the fault."""
        return [v for v in self.all_vectors() if self.detects(v, fault)]

    def detectable(self, fault: Fault) -> bool:
        return any(self.detects(v, fault) for v in self.all_vectors())

    def cone(self, line: int) -> set[int]:
        """The lines reachable from a line, the line included."""
        seen = {line}
        stack = [line]
        while stack:
            u = stack.pop()
            for w in self.fanout[u]:
                if w not in seen:
                    seen.add(w)
                    stack.append(w)
        return seen


def completions(vector: Sequence[int]) -> list[tuple[int, ...]]:
    """All two-valued vectors that agree with a vector that may hold X."""
    choices = [(0, 1) if v == X else (v,) for v in vector]
    return list(product(*choices))


def random_circuit(
    rng: random.Random,
    n_inputs: int,
    n_gates: int,
    ops: Sequence[str] = ("AND", "OR", "NAND", "NOR", "NOT"),
    max_fanin: int = 3,
) -> Circuit:
    """A random circuit. Every net with no sink becomes a primary output."""
    inputs = [f"i{k}" for k in range(n_inputs)]
    nets = list(inputs)
    gates: list[tuple[str, str, list[str]]] = []
    for k in range(n_gates):
        op = rng.choice(list(ops))
        arity = 1 if op in ("NOT", "BUF") else rng.randint(2, max(2, min(max_fanin, len(nets))))
        arity = min(arity, len(nets))
        if op not in ("NOT", "BUF") and arity < 2:
            op, arity = "NOT", 1
        fanin = rng.sample(nets, arity)
        name = f"g{k}"
        gates.append((name, op, fanin))
        nets.append(name)
    used = {src for _, _, fanin in gates for src in fanin}
    outputs = [n for n in nets if n not in used]
    extra = [g[0] for g in gates if g[0] in used]
    if extra and rng.random() < 0.5:
        outputs.append(rng.choice(extra))
    return Circuit(inputs, gates, outputs)
