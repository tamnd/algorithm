# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/concurrent-fault-simulation/. The authors are listed in prov/NCVK7P.jsonl.
"""Concurrent fault simulation (Ulrich and Baker 1973) of single stuck-at faults.

The good circuit is simulated event by event. Each line also keeps a list of
the faults whose faulty circuit has a different value on that line, with that
value. A faulty circuit is evaluated only at lines where it differs from the
good circuit on an input, or where its fault sits. All other faulty circuits
agree with the good circuit there and cost nothing.

Ulrich and Baker keep the list per gate, with the input and output values of
each faulty copy of the gate. This version keeps the list per line, with the
output value only. The faulty input values are then read from the lists of
the input lines. The information is the same.
"""

from __future__ import annotations

import heapq
from typing import Iterable, Optional, Sequence

from gatenet import X, Circuit, Fault, eval_gate


def concurrent_fault_simulation(
    c: Circuit,
    vectors: Iterable[Sequence[int]],
    faults: Optional[Sequence[Fault]] = None,
    drop: bool = True,
    stats: Optional[dict[str, int]] = None,
) -> list[set[Fault]]:
    """For each vector, the set of faults it detects among the faults still simulated.

    With drop=True a fault is removed after the first vector that detects it,
    so it appears in at most one set. Vectors hold the values 0 and 1 only.
    """
    if faults is None:
        faults = c.faults()
    alive = set(faults)
    local: list[list[Fault]] = [[] for _ in range(c.n_lines)]
    for f in faults:
        local[f[0]].append(f)
    good = [X] * c.n_lines
    lists: list[dict[Fault, int]] = [{} for _ in range(c.n_lines)]
    pi_pos = {line: k for k, line in enumerate(c.pi)}
    result: list[set[Fault]] = []
    events = gate_evals = fault_evals = 0

    for vector in vectors:  # @line L1
        queue = list(c.pi)  # @line L2
        heapq.heapify(queue)
        queued = set(queue)
        while queue:  # @line L3
            k = heapq.heappop(queue)
            queued.discard(k)
            events += 1
            ins = c.fanin[k]
            if c.kind[k] == "pi":  # @line L4
                g = vector[pi_pos[k]]
            else:
                g = eval_gate(c.op[k], [good[j] for j in ins])
            gate_evals += 1
            here = {f for f in local[k] if f in alive}  # @line L5
            seen = set(here)
            for j in ins:
                seen.update(f for f in lists[j] if f in alive)
            new: dict[Fault, int] = {}
            for f in seen:  # @line L6
                if f in here:
                    v = f[1]
                else:
                    v = eval_gate(c.op[k], [lists[j].get(f, good[j]) for j in ins])
                    fault_evals += 1
                if v != g:  # @line L7
                    new[f] = v
            old = {f: v for f, v in lists[k].items() if f in alive}
            if g != good[k] or new != old:  # @line L8
                good[k] = g
                lists[k] = new
                for w in c.fanout[k]:
                    if w not in queued:
                        queued.add(w)
                        heapq.heappush(queue, w)
        detected = {f for o in c.po for f in lists[o] if f in alive}  # @line L9
        result.append(detected)
        if drop:  # @line L10
            alive -= detected  # the lists keep dropped faults until they are rebuilt; reads skip them

    if stats is not None:
        stats.update(events=events, gate_evals=gate_evals, fault_evals=fault_evals)
    return result
