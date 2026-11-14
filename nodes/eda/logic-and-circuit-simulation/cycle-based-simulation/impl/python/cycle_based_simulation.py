# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/cycle-based-simulation/. The authors are listed in prov/BBKYW7.jsonl.
"""Cycle-based simulation of a synchronous design with one clock.

The registers cut every loop. The logic between them is levelized once and
then evaluated once per clock cycle with zero delay, and all registers take
their new values together at the clock edge. There is no time inside a cycle.
"""

from __future__ import annotations

from typing import Dict, List, Sequence, Tuple

from logicnet import Circuit, eval2


class CombinationalLoop(ValueError):
    """A loop of gates that no register cuts."""


class SyncDesign:
    """inputs: primary inputs. regs: (q, d, initial value) for each D flip-flop.

    gates: (out, op, ins) of the logic. outputs: nets observed each cycle.
    """

    def __init__(self, inputs: Sequence[str], regs: Sequence[Tuple[str, str, int]],
                 gates: Sequence[Tuple[str, str, Sequence[str]]], outputs: Sequence[str]):
        self.inputs = list(inputs)
        self.regs = [(q, d, v) for q, d, v in regs]
        # The register outputs become inputs of the logic and the D nets its outputs.
        self.logic = Circuit(self.inputs + [q for q, _, _ in self.regs], gates, list(outputs) + [d for _, d, _ in self.regs])  # @line L1
        self.outputs = list(outputs)


def levelize(c: Circuit) -> List[int]:
    """Kahn's algorithm on the gate graph of the logic."""
    waiting = [len({n for n in ins if n in c.driver}) for _, _, ins in c.gates]
    order = [i for i in range(len(c.gates)) if waiting[i] == 0]
    head = 0
    while head < len(order):
        out = c.gates[order[head]][0]
        head += 1
        for h in c.fanout[out]:
            waiting[h] -= 1
            if waiting[h] == 0:
                order.append(h)
    if len(order) != len(c.gates):
        raise CombinationalLoop("a loop of gates is not cut by a register")
    return order


def simulate(design: SyncDesign, stimulus: Sequence[Dict[str, int]]) -> Tuple[List[Dict[str, int]], Dict[str, int]]:
    """Run one cycle per entry of stimulus. Returns the outputs of each cycle and the final state."""
    c = design.logic
    order = levelize(c)  # @line L2
    state = {q: v for q, _, v in design.regs}  # @line L3
    trace: List[Dict[str, int]] = []
    for x in stimulus:  # @line L4
        val = dict(x)
        val.update(state)
        for g in order:  # @line L5
            out, op, ins = c.gates[g]
            val[out] = eval2(op, [val[n] for n in ins])
        trace.append({o: val[o] for o in design.outputs})  # @line L6
        state = {q: val[d] for q, d, _ in design.regs}  # @line L7
    return trace, state  # @line L8
