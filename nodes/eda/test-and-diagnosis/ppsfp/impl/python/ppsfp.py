# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/ppsfp/. The authors are listed in prov/THPQ1N.jsonl.
"""Parallel-pattern single-fault propagation (PPSFP) of single stuck-at faults.

The vectors are cut into blocks of w. Bit i of a word is vector i of the
block. The good circuit is simulated once per block with bitwise operations.
Then each fault is simulated on its own, against all w vectors at once: its
line gets the constant word of its stuck value, and the difference is pushed
forward in topological order, only through lines where the faulty word
differs from the good word. When no line differs any more, the fault is done
with this block. The bits where a primary output differs are the vectors of
the block that detect the fault.

Python integers have no fixed width. The parameter width plays the part of
the machine word.
"""

from __future__ import annotations

import heapq
from typing import Optional, Sequence

from gatenet import Circuit, Fault


def eval_word(op: str, words: Sequence[int], mask: int) -> int:
    """One gate on words: bit k of the result is the gate on bit k of each input."""
    if op in ("BUF", "NOT"):
        r = words[0]
    elif op in ("AND", "NAND"):
        r = mask
        for w in words:
            r &= w
    elif op in ("OR", "NOR"):
        r = 0
        for w in words:
            r |= w
    else:  # XOR, XNOR
        r = 0
        for w in words:
            r ^= w
    if op in ("NOT", "NAND", "NOR", "XNOR"):
        r ^= mask
    return r


def good_words(c: Circuit, block: Sequence[Sequence[int]], mask: int) -> list[int]:
    """The good circuit on a block of vectors: bit i of word[line] is the line under vector i."""
    word = [0] * c.n_lines
    pi = 0
    for line in range(c.n_lines):
        if c.kind[line] == "pi":
            w = 0
            for i, vector in enumerate(block):
                w |= vector[pi] << i
            pi += 1
        else:
            w = eval_word(c.op[line], [word[j] for j in c.fanin[line]], mask)
        word[line] = w
    return word


def propagate(c: Circuit, good: list[int], fault: Fault, mask: int, counter: list[int]) -> int:
    """The mask of vectors of the block on which some primary output differs under the fault."""
    line, v = fault
    start = mask if v else 0
    if start == good[line]:
        return 0  # no vector of the block gives the line the opposite value
    bad = {line: start}
    heap = list(c.fanout[line])
    heapq.heapify(heap)
    queued = set(heap)
    while heap:  # lines in increasing index order, so inputs are final first
        k = heapq.heappop(heap)
        w = eval_word(c.op[k], [bad.get(j, good[j]) for j in c.fanin[k]], mask)
        counter[0] += 1
        if w != good[k]:  # the difference goes on only where it is still alive
            bad[k] = w
            for u in c.fanout[k]:
                if u not in queued:
                    queued.add(u)
                    heapq.heappush(heap, u)
    seen = 0
    for o in c.po:
        if o in bad:
            seen |= bad[o] ^ good[o]
    return seen


def ppsfp(
    c: Circuit,
    vectors: Sequence[Sequence[int]],
    faults: Optional[Sequence[Fault]] = None,
    drop: bool = True,
    width: int = 64,
    stats: Optional[dict[str, int]] = None,
) -> list[set[Fault]]:
    """For each vector, the set of faults it detects among the faults still simulated.

    With drop=True a fault is reported only at the first vector that detects
    it and is not simulated in later blocks. Vectors hold 0 and 1 only.
    """
    if width < 1:
        raise ValueError("a block holds at least one vector")
    alive = list(c.faults() if faults is None else faults)
    result: list[set[Fault]] = [set() for _ in vectors]
    counter = [0]
    blocks = fault_runs = 0
    for start in range(0, len(vectors), width):  # @line L1
        block = vectors[start:start + width]
        mask = (1 << len(block)) - 1
        good = good_words(c, block, mask)  # @line L2
        blocks += 1
        still: list[Fault] = []
        for f in alive:  # @line L3
            fault_runs += 1
            seen = propagate(c, good, f, mask, counter)  # @line L4
            if seen == 0:  # @line L5
                still.append(f)
                continue
            if drop:  # @line L6
                first = (seen & -seen).bit_length() - 1
                result[start + first].add(f)
            else:
                for i in range(len(block)):
                    if seen >> i & 1:
                        result[start + i].add(f)
                still.append(f)
        alive = still  # @line L7
    if stats is not None:
        stats.update(blocks=blocks, fault_runs=fault_runs, gate_evals=counter[0])
    return result
