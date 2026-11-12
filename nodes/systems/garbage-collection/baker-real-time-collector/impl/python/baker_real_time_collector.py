# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/baker-real-time-collector/. The authors are listed in prov/DE61E5.jsonl.

"""Baker's real-time copying collector (Baker 1978).

Heap model: two semispaces of S cells each, with the addresses 0 to S - 1
and S to 2S - 1. A cell has p pointer fields (an address or None). The
mutator holds r registers (the roots) and runs four operations: load a field
into a register, store a register into a field, clear a register, allocate.
At every moment at most L cells are reachable.

To-space layout: copied cells grow up from the bottom (scan <= copy), and new
cells grow down from the top (top). Cells below scan and cells at or above top
are black; cells in [scan, copy) are gray.

The read barrier (LOAD) keeps the to-space invariant: a register never holds a
from-space address. Each allocation first scans k gray cells. A flip happens
when an allocation finds to-space full; then from-space and to-space swap and
the roots are evacuated.

The bound of the page: if S >= L + ceil(L / k), the scan always finishes before
to-space fills, so no allocation fails.
"""

from __future__ import annotations


class CollectorBehind(Exception):
    """To-space is full while gray cells remain: k is too small for L and S."""


class Baker:
    def __init__(self, semispace: int, registers: int, k: int, fields: int = 2) -> None:
        self.S, self.k, self.p = semispace, k, fields
        self.mem: list[list[int | None]] = [[None] * fields for _ in range(2 * semispace)]
        self.ident: list[int | None] = [None] * (2 * semispace)  # logical name of each cell
        self.forward: dict[int, int] = {}  # from-space address -> to-space address
        self.regs: list[int | None] = [None] * registers
        self.base = 0  # to-space is [base, base + S)
        self.scan = self.copy = 0
        self.top = semispace
        self.flips = 0
        self.max_scans = 0  # the most cells scanned by one allocation
        self.copied_in_cycle = 0
        self.max_copied = 0
        self.names = 0

    def in_to_space(self, a: int) -> bool:
        return self.base <= a < self.base + self.S

    def flip(self) -> None:
        self.base = self.S - self.base  # @line L1
        self.scan = self.copy = self.base
        self.top = self.base + self.S
        self.forward = {}
        self.flips += 1
        self.copied_in_cycle = 0
        for i, r in enumerate(self.regs):  # @line L2
            self.regs[i] = self.evacuate(r)

    def evacuate(self, a: int | None) -> int | None:
        if a is None or self.in_to_space(a):  # @line L3
            return a
        if a in self.forward:  # @line L4
            return self.forward[a]
        b = self.copy  # @line L5
        if b >= self.top:
            raise CollectorBehind("no room to copy")
        self.mem[b] = list(self.mem[a])
        self.ident[b] = self.ident[a]
        self.copy += 1
        self.forward[a] = b  # @line L6
        self.copied_in_cycle += 1
        self.max_copied = max(self.max_copied, self.copied_in_cycle)
        return b  # @line L7

    def load(self, x: int, f: int) -> int | None:
        """The read barrier: x is a to-space cell held by the mutator."""
        y = self.evacuate(self.mem[x][f])  # @line L8
        self.mem[x][f] = y
        return y

    def scan_steps(self) -> int:
        done = 0
        while done < self.k and self.scan < self.copy:  # @line L9
            row = self.mem[self.scan]
            for f in range(self.p):  # @line L10
                row[f] = self.evacuate(row[f])
            self.scan += 1  # @line L11
            done += 1
        return done

    def allocate(self) -> int:
        if self.copy == self.top:  # @line L12
            if self.scan < self.copy:  # @line L13
                raise CollectorBehind("to-space is full before the scan ended")
            self.flip()  # @line L14
        self.max_scans = max(self.max_scans, self.scan_steps())  # @line L15
        if self.copy == self.top:  # @line L16
            raise CollectorBehind("to-space is full")
        self.top -= 1  # @line L17
        self.mem[self.top] = [None] * self.p
        self.ident[self.top] = self.names
        self.names += 1
        return self.top  # @line L18

    # Mutator operations on registers.

    def op_load(self, i: int, j: int, f: int) -> None:
        if self.regs[j] is not None:
            self.regs[i] = self.load(self.regs[j], f)

    def op_store(self, i: int, f: int, j: int) -> None:
        if self.regs[i] is not None:
            self.mem[self.regs[i]][f] = self.regs[j]  # no write barrier is needed

    def op_alloc(self, i: int) -> None:
        self.regs[i] = self.allocate()

    def resolve(self, a: int | None) -> int | None:
        """Follow a forwarding address, as the mutator would see the cell."""
        if a is not None and not self.in_to_space(a) and a in self.forward:
            return self.forward[a]
        return a

    def logical_graph(self) -> tuple[list[int | None], dict[int, list[int | None]]]:
        """The registers and reachable cells, by logical name, with forwarding resolved."""
        regs = [None if r is None else self.ident[r] for r in self.regs]
        graph: dict[int, list[int | None]] = {}
        stack = [r for r in self.regs if r is not None]
        while stack:
            a = self.resolve(stack.pop())
            if self.ident[a] in graph:
                continue
            kids = [self.resolve(y) for y in self.mem[a]]
            graph[self.ident[a]] = [None if y is None else self.ident[y] for y in kids]
            stack.extend(y for y in kids if y is not None)
        return regs, graph
