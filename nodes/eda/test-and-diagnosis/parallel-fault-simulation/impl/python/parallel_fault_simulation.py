# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/parallel-fault-simulation/. The authors are listed in prov/S63TGE.jsonl.
"""Parallel fault simulation of single stuck-at faults (one fault per bit).

Each line holds a word of w bits. Bit 0 is the good circuit and bits 1 to
w - 1 are faulty circuits, one fault each. A gate is evaluated once per word
with bitwise operations, so one pass over the circuit simulates w - 1 faulty
circuits and the good one. A fault is put in its own bit by two masks on its
line: a clear mask for stuck-at 0 and a set mask for stuck-at 1. The faults
are cut into groups of w - 1, and each vector takes one pass per group.

Python integers have no fixed width. The parameter width plays the part of
the machine word, so that the number of passes is the one a real word gives.
"""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

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


def parallel_fault_simulation(
    c: Circuit,
    vectors: Iterable[Sequence[int]],
    faults: Optional[Sequence[Fault]] = None,
    drop: bool = True,
    width: int = 64,
    stats: Optional[dict[str, int]] = None,
) -> list[set[Fault]]:
    """For each vector, the set of faults it detects among the faults still simulated.

    width is the word size w >= 2: bit 0 is the good circuit, so a pass holds
    w - 1 faults. With drop=True a fault is removed after the first vector that
    detects it. Vectors hold the values 0 and 1 only.
    """
    if width < 2:
        raise ValueError("the word needs a bit for the good circuit and one for a fault")
    alive = list(c.faults() if faults is None else faults)
    result: list[set[Fault]] = []
    passes = word_evals = 0
    for vector in vectors:  # @line L1
        detected: set[Fault] = set()
        for start in range(0, len(alive), width - 1):  # @line L2
            group = alive[start:start + width - 1]
            mask = (1 << (len(group) + 1)) - 1
            clear = [0] * c.n_lines  # @line L3
            setm = [0] * c.n_lines
            for k, (line, v) in enumerate(group, 1):
                if v == 0:
                    clear[line] |= 1 << k
                else:
                    setm[line] |= 1 << k
            word = [0] * c.n_lines
            pi = 0
            for line in range(c.n_lines):  # @line L4
                if c.kind[line] == "pi":  # @line L5
                    w = mask if vector[pi] else 0
                    pi += 1
                else:  # @line L6
                    w = eval_word(c.op[line], [word[j] for j in c.fanin[line]], mask)
                word[line] = (w & ~clear[line]) | setm[line]  # @line L7
            diff = 0
            for o in c.po:  # @line L8
                good = mask if word[o] & 1 else 0
                diff |= word[o] ^ good
            for k in range(1, len(group) + 1):  # @line L9
                if diff >> k & 1:
                    detected.add(group[k - 1])
            passes += 1
            word_evals += c.n_lines
        result.append(detected)
        if drop:  # @line L10
            alive = [f for f in alive if f not in detected]
    if stats is not None:
        stats.update(passes=passes, word_evals=word_evals)
    return result
