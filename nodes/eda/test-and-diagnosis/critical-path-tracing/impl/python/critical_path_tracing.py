# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/critical-path-tracing/. The authors are listed in prov/KS79ZE.jsonl.
"""Critical path tracing (Abramovici, Menon and Miller 1984) for single stuck-at faults.

A line is critical under a vector when flipping its value flips some primary
output. Then the vector detects the line stuck at the opposite of its good
value, and no other fault of the line. The circuit splits into fanout-free
regions: each region is a tree whose root is a line with no fanout or with
two or more, and whose other lines each have exactly one fanout. Inside a
region, criticality is found by a backward trace from the root through the
sensitive gate inputs, with no fault simulation. A gate input is sensitive
when flipping it alone flips the gate output. A root with two or more
fanouts is a reconvergent stem in general: its criticality is checked here by
flipping it and propagating the change forward to the outputs.
"""

from __future__ import annotations

import heapq
from typing import Iterable, Optional, Sequence

from gatenet import Circuit, Fault, controlling, eval_gate


def sensitive_inputs(op: str, vals: Sequence[int]) -> list[int]:
    """Positions of the gate inputs whose flip alone flips the output, for good values vals."""
    c = controlling(op)
    if c is None:  # BUF, NOT, XOR, XNOR: every input is sensitive
        return list(range(len(vals)))
    at_c = [i for i, v in enumerate(vals) if v == c]
    if not at_c:
        return list(range(len(vals)))
    if len(at_c) == 1:
        return at_c
    return []


def stem_is_critical(c: Circuit, good: list[int], stem: int, po: set[int], counter: list[int]) -> bool:
    """Flip the stem and propagate the change forward. True if some primary output changes."""
    bad = {stem: 1 - good[stem]}
    heap = list(c.fanout[stem])
    heapq.heapify(heap)
    queued = set(heap)
    while heap:
        k = heapq.heappop(heap)
        v = eval_gate(c.op[k], [bad.get(j, good[j]) for j in c.fanin[k]])
        counter[0] += 1
        if v != good[k]:
            if k in po:
                return True
            bad[k] = v
            for u in c.fanout[k]:
                if u not in queued:
                    queued.add(u)
                    heapq.heappush(heap, u)
    return False


def critical_lines(c: Circuit, vector: Sequence[int], counter: Optional[list[int]] = None) -> list[bool]:
    """crit[line] is True when flipping the line flips some primary output under the vector."""
    if counter is None:
        counter = [0, 0]
    good = c.simulate(vector)  # @line L2
    po = set(c.po)
    crit = [False] * c.n_lines
    for root in range(c.n_lines):  # @line L3
        if len(c.fanout[root]) == 1:
            continue  # not a root: the line belongs to the region of its only fanout
        if root in po:  # @line L4
            ok = True
        elif len(c.fanout[root]) >= 2:  # @line L5
            counter[1] += 1
            ok = stem_is_critical(c, good, root, po, counter)
        else:
            ok = False  # a line that feeds nothing and is not an output
        if not ok:
            continue
        stack = [root]  # @line L6
        while stack:
            k = stack.pop()
            crit[k] = True  # @line L7
            if c.kind[k] == "pi":
                continue
            ins = c.fanin[k]
            for pos in sensitive_inputs(c.op[k], [good[j] for j in ins]):  # @line L8
                j = ins[pos]
                if len(c.fanout[j]) == 1:  # @line L9
                    stack.append(j)
    return crit


def critical_path_tracing(
    c: Circuit,
    vectors: Iterable[Sequence[int]],
    faults: Optional[Sequence[Fault]] = None,
    drop: bool = True,
    stats: Optional[dict[str, int]] = None,
) -> list[set[Fault]]:
    """For each vector, the set of faults it detects among the faults still listed.

    With drop=True a fault is removed after the first vector that detects it.
    Vectors hold the values 0 and 1 only.
    """
    alive = set(c.faults() if faults is None else faults)
    result: list[set[Fault]] = []
    counter = [0, 0]  # gate evaluations in stem checks, number of stem checks
    for vector in vectors:  # @line L1
        crit = critical_lines(c, vector, counter)
        good = c.simulate(vector)
        detected = {(k, 1 - good[k]) for k in range(c.n_lines) if crit[k]} & alive  # @line L10
        result.append(detected)
        if drop:  # @line L11
            alive -= detected
    if stats is not None:
        stats.update(stem_gate_evals=counter[0], stem_checks=counter[1])
    return result
