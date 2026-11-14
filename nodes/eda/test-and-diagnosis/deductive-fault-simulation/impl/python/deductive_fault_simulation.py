# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deductive-fault-simulation/. The authors are listed in prov/WGDS9V.jsonl.
"""Deductive fault simulation (Armstrong 1972) of single stuck-at faults.

For one vector, the good circuit is simulated once. Each line then gets its
fault list: the set of faults under which the line has the opposite of its
good value. The list of a line follows from the good values and the lists of
its inputs by set operations, with no faulty gate evaluation:

- buffer, inverter and fanout branch: the list of the input;
- AND, NAND, OR, NOR with controlling value c: if no input has the value c,
  the union of the input lists; else the intersection of the lists of the
  inputs at c, minus the union of the lists of the other inputs;
- XOR, XNOR: the faults that are in an odd number of input lists;

and then the fault of the line stuck at the opposite of its good value is
added. The list of a primary output is the set of faults that the vector
detects there.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

from gatenet import Circuit, Fault, controlling


def gate_list(op: str, vals: Sequence[int], lists: Sequence[set[Fault]]) -> set[Fault]:
    """The faults that flip the output of one gate, from its good input values and input lists."""
    if op in ("BUF", "NOT"):
        return set(lists[0])
    if op in ("XOR", "XNOR"):
        odd: set[Fault] = set()
        for lst in lists:
            odd ^= lst
        return odd
    c = controlling(op)
    at_c = [lst for v, lst in zip(vals, lists) if v == c]
    if not at_c:  # every input is non-controlling: any flipped input flips the output
        out: set[Fault] = set()
        for lst in lists:
            out |= lst
        return out
    out = set.intersection(*at_c)  # every controlling input must flip
    for v, lst in zip(vals, lists):
        if v != c:
            out -= lst  # and no other input may flip to c
    return out


def deductive_fault_simulation(
    c: Circuit,
    vectors: Iterable[Sequence[int]],
    faults: Optional[Sequence[Fault]] = None,
    drop: bool = True,
    stats: Optional[dict[str, int]] = None,
    lists_out: Optional[list[list[set[Fault]]]] = None,
) -> list[set[Fault]]:
    """For each vector, the set of faults it detects among the faults still simulated.

    With drop=True a fault is removed after the first vector that detects it.
    If lists_out is a list, the fault lists of all lines are appended to it
    for each vector. Vectors hold the values 0 and 1 only.
    """
    alive = set(c.faults() if faults is None else faults)
    local: list[list[Fault]] = [[] for _ in range(c.n_lines)]
    for f in alive:
        local[f[0]].append(f)
    result: list[set[Fault]] = []
    elements = 0
    for vector in vectors:  # @line L1
        good = c.simulate(vector)  # @line L2
        lst: list[set[Fault]] = [set() for _ in range(c.n_lines)]
        for line in range(c.n_lines):  # @line L3
            if c.kind[line] == "pi":  # @line L4
                here: set[Fault] = set()
            else:  # @line L5
                ins = c.fanin[line]
                here = gate_list(c.op[line], [good[j] for j in ins], [lst[j] for j in ins])
                elements += sum(len(lst[j]) for j in ins)
            for f in local[line]:  # @line L6
                if f in alive and f[1] != good[line]:
                    here.add(f)
            lst[line] = here
        detected: set[Fault] = set()
        for o in c.po:  # @line L7
            detected |= lst[o]
        result.append(detected)
        if lists_out is not None:
            lists_out.append(lst)
        if drop:  # @line L8
            alive -= detected
    if stats is not None:
        stats.update(list_elements=elements)
    return result
