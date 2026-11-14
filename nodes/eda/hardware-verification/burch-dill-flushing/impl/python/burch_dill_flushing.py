# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/burch-dill-flushing/. The authors are listed in prov/W76CN0.jsonl.
"""Burch and Dill's commuting-diagram check of a pipeline against its ISA.

The machine is a two-stage pipeline with a register file of R registers and
three-operand instructions (op, rd, rs1, rs2) meaning rd <- op(rs1, rs2).
Stage 1 decodes the instruction and reads its operands; the pipeline register P
then holds (valid, op, rd, tag, a, b). Stage 2 applies the ALU to a and b and
writes rd at the clock edge. An instruction in stage 1 that reads the register
written by the instruction in stage 2 must take the ALU result by a bypass.

The ISA state is the register file alone. The abstraction function flushes the
pipeline by one stall cycle (input None, no fetch) and keeps the register file.

The data values are a parameter of the machine. With alu = term (an
uninterpreted function) and atoms for the register contents, two values are
equal in every interpretation of the ALU exactly when they are the same term, so
the check over all control values is the EUF check of Burch and Dill. With
integers and a real ALU it is an exhaustive check of one interpretation.

bug selects a faulty design: "no-bypass", "bypass-rs1-only", or "tag", which
compares the bypass against a copy of rd that agrees with rd in every reachable
state but not in every state.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from typing import Callable, Hashable, Iterable, Optional

OPS = ("ADD", "AND", "XOR")

Instr = Optional[tuple[str, int, int, int]]     # None is a stall cycle


@dataclass(frozen=True)
class Pipe:
    valid: bool
    op: str
    rd: int
    tag: int
    a: Hashable
    b: Hashable


State = tuple[tuple[Hashable, ...], Pipe]       # (register file, pipeline register)


def term(op: str, a: Hashable, b: Hashable) -> Hashable:
    """The uninterpreted ALU: the result is the term op(a, b)."""
    return (op, a, b)


def word_alu(width: int) -> Callable[[str, int, int], int]:
    mask = (1 << width) - 1

    def alu(op: str, a: int, b: int) -> int:
        if op == "ADD":
            return (a + b) & mask
        if op == "AND":
            return a & b
        return a ^ b

    return alu


class Machine:
    def __init__(self, nregs: int, alu: Callable, zero: Hashable, bug: Optional[str] = None) -> None:
        self.nregs, self.alu, self.zero, self.bug = nregs, alu, zero, bug
        self.depth = 1                      # stall cycles that empty the pipeline

    def bubble(self) -> Pipe:
        return Pipe(False, OPS[0], 0, 0, self.zero, self.zero)

    def spec_step(self, rf: tuple, ins: Instr) -> tuple:
        op, rd, rs1, rs2 = ins
        out = list(rf)
        out[rd] = self.alu(op, rf[rs1], rf[rs2])
        return tuple(out)

    def impl_step(self, q: State, ins: Instr) -> State:
        rf, p = q
        res = self.alu(p.op, p.a, p.b) if p.valid else None
        if ins is None:
            newp = self.bubble()
        else:
            op, rd, rs1, rs2 = ins
            a, b = rf[rs1], rf[rs2]
            if p.valid and self.bug != "no-bypass":
                key = p.tag if self.bug == "tag" else p.rd
                if key == rs1:
                    a = res
                if key == rs2 and self.bug != "bypass-rs1-only":
                    b = res
            newp = Pipe(True, op, rd, rd, a, b)
        if p.valid:
            rf = rf[:p.rd] + (res,) + rf[p.rd + 1:]
        return (rf, newp)

    def fetched(self, q: State, ins: Instr) -> bool:
        """Whether the implementation takes the instruction in this cycle (it never stalls itself)."""
        return ins is not None

    def flush(self, q: State) -> State:
        for _ in range(self.depth):
            q = self.impl_step(q, None)
        return q

    def abstraction(self, q: State) -> tuple:
        return self.flush(q)[0]

    def instructions(self) -> list[Instr]:
        r = range(self.nregs)
        return [(op, rd, s1, s2) for op in OPS for rd in r for s1 in r for s2 in r]


def commuting_check(m: Machine, states: Iterable[State], inputs: list[Instr]):
    """The first (q, i, left, right) where the diagram does not commute, or None."""
    for q in states:                                                   # @line L1
        s = m.abstraction(q)                                           # @line L2
        for i in inputs:                                               # @line L3
            q2 = m.impl_step(q, i)
            left = m.abstraction(q2)                                   # @line L4
            right = m.spec_step(s, i) if m.fetched(q, i) else s        # @line L5
            if left != right:                                          # @line L6
                return (q, i, left, right)
    return None                                                        # @line L7


def symbolic_states(m: Machine) -> Iterable[State]:
    """Every control value, with fresh atoms for all data: the states of the EUF check."""
    rf = tuple(f"r{j}" for j in range(m.nregs))
    r = range(m.nregs)
    for valid, op, rd, tag in product((False, True), OPS, r, r):
        yield (rf, Pipe(valid, op, rd, tag, "pa", "pb"))


def concrete_states(m: Machine, width: int) -> Iterable[State]:
    """Every state of the machine with width-bit words."""
    words = range(1 << width)
    r = range(m.nregs)
    for rf in product(words, repeat=m.nregs):
        for valid, op, rd, tag, a, b in product((False, True), OPS, r, r, words, words):
            yield (rf, Pipe(valid, op, rd, tag, a, b))


def euf_check(nregs: int, bug: Optional[str] = None):
    """The Burch-Dill check over all states, with an uninterpreted ALU."""
    m = Machine(nregs, term, "z", bug)
    return commuting_check(m, symbolic_states(m), [None] + m.instructions())
