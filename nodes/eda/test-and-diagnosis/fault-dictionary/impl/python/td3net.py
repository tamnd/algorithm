# SPDX-License-Identifier: MIT
# Shared helper of the td3 eda pages of https://algorithm.tamnd.com/. The authors are listed in prov/.
"""Gate-level combinational circuits with single stuck-at faults (two values).

A circuit is built from named primary inputs, gates in topological order and
named primary outputs. Every place where a fault can sit is a *line*:

- one stem line for each primary input and for each gate output;
- when a net feeds two or more sinks (gate input pins or primary outputs), one
  branch line for each sink. A net with one sink has no branch line.

Lines are numbered 0, 1, ... in topological order, so every line comes after
the lines it reads. A single stuck-at fault is a pair (line, value). Building a
circuit and simulating one vector take O(L + P) time for L lines and P gate
input pins.

This module holds the circuit model and plain simulation of the good circuit
and of one faulty circuit. It holds no diagnosis algorithm.
"""

from __future__ import annotations

import random
from typing import Optional, Sequence

OPS = ("AND", "OR", "NAND", "NOR", "NOT", "BUF", "XOR", "XNOR")

Fault = tuple[int, int]


def eval_gate(op: str, vals: Sequence[int]) -> int:
    """Two-valued output of a gate."""
    if op in ("AND", "NAND"):
        r = int(all(vals))
    elif op in ("OR", "NOR"):
        r = int(any(vals))
    elif op in ("XOR", "XNOR"):
        r = 0
        for v in vals:
            r ^= v
    else:
        r = vals[0]
    return r ^ int(op in ("NAND", "NOR", "XNOR", "NOT"))


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
                    label = f"{net}>out{s[1]}"
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

    def faults(self) -> list[Fault]:
        """All 2L single stuck-at faults, in line order."""
        return [(line, v) for line in range(self.n_lines) for v in (0, 1)]

    def fault_name(self, fault: Fault) -> str:
        return f"{self.name[fault[0]]}/{fault[1]}"

    def simulate(self, vector: Sequence[int], fault: Optional[Fault] = None) -> list[int]:
        """Values of all lines for one input vector, with an optional stuck-at fault."""
        vals = [0] * self.n_lines
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


def random_circuit(rng: random.Random, n_inputs: int, n_gates: int, max_fanin: int = 3) -> Circuit:
    """A random circuit of AND, OR, NAND, NOR, XOR and NOT gates. Every net with no sink is an output."""
    ops = ("AND", "OR", "NAND", "NOR", "XOR", "NOT")
    inputs = [f"i{k}" for k in range(n_inputs)]
    nets = list(inputs)
    gates: list[tuple[str, str, list[str]]] = []
    for k in range(n_gates):
        op = rng.choice(ops)
        if op == "NOT" or len(nets) < 2:
            op, fanin = "NOT", [rng.choice(nets)]
        else:
            fanin = rng.sample(nets, rng.randint(2, min(max_fanin, len(nets))))
        gates.append((f"g{k}", op, fanin))
        nets.append(f"g{k}")
    used = {src for _, _, fanin in gates for src in fanin}
    outputs = [n for n in nets if n not in used]
    inner = [g[0] for g in gates if g[0] in used]
    if inner and rng.random() < 0.5:
        outputs.append(rng.choice(inner))
    return Circuit(inputs, gates, outputs)
