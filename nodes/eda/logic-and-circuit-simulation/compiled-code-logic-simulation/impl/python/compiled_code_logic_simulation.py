# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/compiled-code-logic-simulation/. The authors are listed in prov/6EDHZJ.jsonl.
"""Levelized compiled-code logic simulation with bit-parallel words.

The netlist is levelized once (Kahn's algorithm) and turned into straight-line
code with one statement for each gate. The delay model is zero delay, and the
values are 0 and 1. Bit j of every word belongs to input vector j, so one run
of the code simulates W vectors at once.
"""

from __future__ import annotations

from typing import Callable, Dict, List, Sequence, Tuple

from logicnet import Circuit


class CombinationalLoop(ValueError):
    """The netlist has a loop, so it has no levelized order."""


def levelize(c: Circuit) -> Tuple[List[int], Dict[str, int]]:
    """Kahn's algorithm: gates in an order where every gate follows the drivers of its inputs."""
    level = {n: 0 for n in c.inputs}
    waiting = [len({n for n in ins if n in c.driver}) for _, _, ins in c.gates]
    ready = [i for i in range(len(c.gates)) if waiting[i] == 0]
    order: List[int] = []
    head = 0
    while head < len(ready):
        g = ready[head]
        head += 1
        out, op, ins = c.gates[g]
        level[out] = 1 + max(level[n] for n in ins)
        order.append(g)
        for h in c.fanout[out]:
            waiting[h] -= 1
            if waiting[h] == 0:
                ready.append(h)
    if len(order) != len(c.gates):
        raise CombinationalLoop("the circuit has a loop of gates")
    order.sort(key=lambda g: level[c.gates[g][0]])  # stable: ties keep the Kahn order
    return order, level


def _expr(op: str, args: List[str]) -> str:
    if op == "BUF":
        return args[0]
    if op == "NOT":
        return f"{args[0]} ^ M"
    sym = {"AND": " & ", "NAND": " & ", "OR": " | ", "NOR": " | ", "XOR": " ^ ", "XNOR": " ^ "}[op]
    body = sym.join(args)
    return f"({body}) ^ M" if op in ("NAND", "NOR", "XNOR") else body


def compile_circuit(c: Circuit, width: int = 64) -> Tuple[str, Callable[[Sequence[int]], List[int]]]:
    """Return the source of the straight-line program and the compiled function.

    The function takes one word for each primary input and returns one word
    for each primary output.
    """
    order, _ = levelize(c)  # @line L1
    name = {n: f"v{k}" for k, n in enumerate(c.nets)}
    lines = ["def run(w):"]
    lines += [f"    {name[n]} = w[{k}]" for k, n in enumerate(c.inputs)]
    for g in order:  # @line L2
        out, op, ins = c.gates[g]
        lines.append(f"    {name[out]} = {_expr(op, [name[n] for n in ins])}")  # @line L3
    lines.append("    return [" + ", ".join(name[n] for n in c.outputs) + "]")
    src = "\n".join(lines) + "\n"
    env = {"M": (1 << width) - 1}
    exec(compile(src, "<compiled circuit>", "exec"), env)  # @line L4
    return src, env["run"]


def simulate(c: Circuit, vectors: Sequence[Dict[str, int]], width: int = 64) -> List[Dict[str, int]]:
    """Output values for each vector, W vectors per run of the compiled code."""
    _, run = compile_circuit(c, width)
    result: List[Dict[str, int]] = []
    for start in range(0, len(vectors), width):  # @line L5
        block = vectors[start:start + width]
        words = [sum(vec[n] << j for j, vec in enumerate(block)) for n in c.inputs]  # @line L6
        outs = run(words)  # @line L7
        for j in range(len(block)):  # @line L8
            result.append({o: (w >> j) & 1 for o, w in zip(c.outputs, outs)})
    return result
