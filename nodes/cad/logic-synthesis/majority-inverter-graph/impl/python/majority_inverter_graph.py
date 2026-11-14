# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/majority-inverter-graph/. The authors are listed in prov/AVZMQ8.jsonl.

"""A majority-inverter graph with complemented edges, a normal form and hashing.

A literal is 2 * id + c as on the and-inverter-graph page: node 0 is the
constant 0, so literal 1 is the constant 1, and nodes 1 to n are inputs.
Every later node is a majority M(a, b, c) of three literals of older
nodes. MAJ puts each call in a normal form before the hash lookup: the
fanins are sorted, the rules M(x, x, z) = x and M(x, not x, z) = z are
applied, and at most one fanin is complemented, using the axiom
not M(x, y, z) = M(not x, not y, not z). AND is M(a, b, 0) and OR is
M(a, b, 1).
"""

from typing import Iterable


def maj3(x: int, y: int, z: int) -> int:
    """Bitwise majority of three integers."""
    return (x & y) | (x & z) | (y & z)


class Mig:
    """A structurally hashed MIG over n primary inputs."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.fanins: list[tuple[int, int, int]] = [(-1, -1, -1)] * (n + 1)
        self.table: dict[tuple[int, int, int], int] = {}

    def input(self, i: int) -> int:
        if not 1 <= i <= self.n:
            raise ValueError("no such input")
        return 2 * i

    def num_nodes(self) -> int:
        return len(self.fanins) - self.n - 1

    def maj(self, a: int, b: int, c: int) -> int:
        """The literal of M(a, b, c) in normal form."""
        a, b, c = sorted((a, b, c))  # @line L1
        if a == b or b == c:  # @line L2
            return b
        if a ^ 1 == b:  # @line L3
            return c
        if b ^ 1 == c:
            return a
        if (a & 1) + (b & 1) + (c & 1) >= 2:  # @line L4
            return self.maj(a ^ 1, b ^ 1, c ^ 1) ^ 1
        node = self.table.get((a, b, c))  # @line L5
        if node is not None:
            return 2 * node
        node = len(self.fanins)  # @line L6
        self.fanins.append((a, b, c))
        self.table[(a, b, c)] = node
        return 2 * node

    def and_(self, a: int, b: int) -> int:
        return self.maj(a, b, 0)

    def or_(self, a: int, b: int) -> int:
        return self.maj(a, b, 1)

    def simulate(self, outputs: Iterable[int]) -> list[int]:
        """Truth tables of the given literals over all 2^n points, x1 the high bit of the point."""
        full = (1 << (1 << self.n)) - 1
        val = [0] * len(self.fanins)  # @line L7
        for i in range(1, self.n + 1):
            t = 0
            for m in range(1 << self.n):
                if (m >> (self.n - i)) & 1:
                    t |= 1 << m
            val[i] = t

        def lit(x: int) -> int:
            return val[x >> 1] ^ (full if x & 1 else 0)

        for v in range(self.n + 1, len(self.fanins)):  # @line L8
            a, b, c = self.fanins[v]
            val[v] = maj3(lit(a), lit(b), lit(c))
        return [lit(o) for o in outputs]  # @line L9

    def levels(self) -> list[int]:
        lev = [0] * len(self.fanins)
        for v in range(self.n + 1, len(self.fanins)):
            lev[v] = 1 + max(lev[x >> 1] for x in self.fanins[v])
        return lev

    def depth(self, outputs: Iterable[int]) -> int:
        lev = self.levels()
        return max((lev[o >> 1] for o in outputs), default=0)
