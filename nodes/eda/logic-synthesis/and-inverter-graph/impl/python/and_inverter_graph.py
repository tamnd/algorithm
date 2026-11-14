# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/and-inverter-graph/. The authors are listed in prov/PGBE80.jsonl.

"""An and-inverter graph with complemented edges and structural hashing.

A literal is the integer 2 * id + c, where id names a node and c = 1
means the edge is complemented. Node 0 is the constant 0, so literal 0
is false and literal 1 is true. Nodes 1 to n are the primary inputs.
Every later node is a two-input AND whose fanins are two literals of
older nodes. The hash table maps an ordered fanin pair to its node, so
the graph never holds two AND nodes with the same pair of fanins.
"""

from typing import Iterable


class Aig:
    """A structurally hashed AIG over n primary inputs."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.fanin0: list[int] = [-1] * (n + 1)
        self.fanin1: list[int] = [-1] * (n + 1)
        self.table: dict[tuple[int, int], int] = {}

    # ---------------------------------------------------------------- building

    def input(self, i: int) -> int:
        """The positive literal of input i, for 1 <= i <= n."""
        if not 1 <= i <= self.n:
            raise ValueError("no such input")
        return 2 * i

    def is_and(self, node: int) -> bool:
        return node > self.n

    def num_ands(self) -> int:
        return len(self.fanin0) - self.n - 1

    def and_(self, a: int, b: int) -> int:
        """The literal of a AND b, after the trivial rules and a hash lookup."""
        if a > b:  # @line L1
            a, b = b, a
        if a == 0:  # @line L2
            return 0
        if a == 1:  # @line L3
            return b
        if a == b:  # @line L4
            return a
        if a == b ^ 1:  # @line L5
            return 0
        node = self.table.get((a, b))  # @line L6
        if node is not None:
            return 2 * node
        node = len(self.fanin0)  # @line L7
        self.fanin0.append(a)
        self.fanin1.append(b)
        self.table[(a, b)] = node
        return 2 * node

    def or_(self, a: int, b: int) -> int:
        return self.and_(a ^ 1, b ^ 1) ^ 1

    def xor(self, a: int, b: int) -> int:
        """a XOR b as NOT(a AND b) AND NOT(NOT a AND NOT b), three AND nodes."""
        return self.and_(self.and_(a, b) ^ 1, self.and_(a ^ 1, b ^ 1) ^ 1)

    def mux(self, s: int, t: int, e: int) -> int:
        """The literal of (s AND t) OR (NOT s AND e)."""
        return self.or_(self.and_(s, t), self.and_(s ^ 1, e))

    # -------------------------------------------------------------- simulation

    def input_table(self, i: int) -> int:
        """The truth table of input i as an integer of 2^n bits, x1 the high bit of the minterm."""
        t = 0
        for m in range(1 << self.n):
            if (m >> (self.n - i)) & 1:
                t |= 1 << m
        return t

    def simulate(self, outputs: Iterable[int]) -> list[int]:
        """Truth tables of the given literals, one bit per input assignment."""
        full = (1 << (1 << self.n)) - 1
        val = [0] * len(self.fanin0)  # @line L8
        for i in range(1, self.n + 1):
            val[i] = self.input_table(i)
        for v in range(self.n + 1, len(self.fanin0)):  # @line L9
            a, b = self.fanin0[v], self.fanin1[v]
            va = val[a >> 1] ^ (full if a & 1 else 0)
            vb = val[b >> 1] ^ (full if b & 1 else 0)
            val[v] = va & vb
        return [val[o >> 1] ^ (full if o & 1 else 0) for o in outputs]  # @line L10

    # ---------------------------------------------------------------- measures

    def levels(self) -> list[int]:
        """The level of each node: 0 for inputs and the constant, 1 + the larger fanin level for an AND."""
        lev = [0] * len(self.fanin0)
        for v in range(self.n + 1, len(self.fanin0)):
            lev[v] = 1 + max(lev[self.fanin0[v] >> 1], lev[self.fanin1[v] >> 1])
        return lev

    def cone_size(self, outputs: Iterable[int]) -> int:
        """The number of AND nodes that the given literals reach."""
        seen: set[int] = set()
        stack = [o >> 1 for o in outputs]
        while stack:
            v = stack.pop()
            if v in seen or not self.is_and(v):
                continue
            seen.add(v)
            stack.append(self.fanin0[v] >> 1)
            stack.append(self.fanin1[v] >> 1)
        return len(seen)
