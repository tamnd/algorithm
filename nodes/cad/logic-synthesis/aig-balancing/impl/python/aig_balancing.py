# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/aig-balancing/. The authors are listed in prov/AX6R7V.jsonl.

"""AIG balancing: rebuild every multi-input AND tree of an AIG with the least depth.

An AIG uses the literal code of the and-inverter-graph page: a literal is
2 * id + c, node 0 is the constant 0, nodes 1 to n are inputs, and every
later node is an AND of two literals of older nodes. A supergate of a
node v is the tree of AND nodes reached from v through edges that are not
complemented and lead to AND nodes with exactly one fanout. Balancing
rebuilds each supergate over its distinct leaves and always ANDs the two
leaves of lowest level first.
"""

import heapq
from typing import Iterable


class Aig:
    """A small structurally hashed AIG, as on the and-inverter-graph page."""

    def __init__(self, n: int) -> None:
        self.n = n
        self.fanin0: list[int] = [-1] * (n + 1)
        self.fanin1: list[int] = [-1] * (n + 1)
        self.level: list[int] = [0] * (n + 1)
        self.table: dict[tuple[int, int], int] = {}

    def is_and(self, v: int) -> bool:
        return v > self.n

    def and_(self, a: int, b: int) -> int:
        if a > b:
            a, b = b, a
        if a == 0 or a == b ^ 1:
            return 0
        if a == 1:
            return b
        if a == b:
            return a
        v = self.table.get((a, b))
        if v is None:
            v = len(self.fanin0)
            self.fanin0.append(a)
            self.fanin1.append(b)
            self.level.append(1 + max(self.level[a >> 1], self.level[b >> 1]))
            self.table[(a, b)] = v
        return 2 * v

    def simulate(self, outputs: Iterable[int]) -> list[int]:
        full = (1 << (1 << self.n)) - 1
        val = [0] * len(self.fanin0)
        for i in range(1, self.n + 1):
            t = 0
            for m in range(1 << self.n):
                if (m >> (self.n - i)) & 1:
                    t |= 1 << m
            val[i] = t
        for v in range(self.n + 1, len(self.fanin0)):
            a, b = self.fanin0[v], self.fanin1[v]
            val[v] = (val[a >> 1] ^ (full if a & 1 else 0)) & (val[b >> 1] ^ (full if b & 1 else 0))
        return [val[o >> 1] ^ (full if o & 1 else 0) for o in outputs]

    def cone(self, outputs: Iterable[int]) -> set[int]:
        """The AND nodes that the given literals reach."""
        seen: set[int] = set()
        stack = [o >> 1 for o in outputs]
        while stack:
            v = stack.pop()
            if v in seen or not self.is_and(v):
                continue
            seen.add(v)
            stack.append(self.fanin0[v] >> 1)
            stack.append(self.fanin1[v] >> 1)
        return seen

    def depth(self, outputs: Iterable[int]) -> int:
        return max((self.level[o >> 1] for o in outputs), default=0)


def supergate_leaves(g: Aig, v: int, refs: list[int]) -> list[int]:
    """The leaf literals of the supergate of AND node v, with repeats."""
    leaves: list[int] = []
    stack = [g.fanin1[v], g.fanin0[v]]
    while stack:
        lit = stack.pop()
        u = lit >> 1
        if lit & 1 == 0 and g.is_and(u) and refs[u] == 1:
            stack.append(g.fanin1[u])
            stack.append(g.fanin0[u])
        else:
            leaves.append(lit)
    return leaves


def balance(g: Aig, outputs: list[int]) -> tuple[Aig, list[int]]:
    """A new AIG with the same functions, no more AND nodes and no more depth."""
    live = g.cone(outputs)
    refs = [0] * len(g.fanin0)
    for v in live:
        refs[g.fanin0[v] >> 1] += 1
        refs[g.fanin1[v] >> 1] += 1
    for o in outputs:
        refs[o >> 1] += 1
    h = Aig(g.n)  # @line L1
    memo: dict[int, int] = {}

    def bal(v: int) -> int:
        if not g.is_and(v):  # @line L3
            return 2 * v
        if v in memo:  # @line L4
            return memo[v]
        leaves = supergate_leaves(g, v, refs)  # @line L5
        new = {bal(lit >> 1) ^ (lit & 1) for lit in leaves}  # @line L6
        new.discard(1)
        if 0 in new or any(x ^ 1 in new for x in new):  # @line L7
            r = 0
        else:
            heap = [(h.level[x >> 1], x) for x in sorted(new)]  # @line L8
            heapq.heapify(heap)
            while len(heap) > 1:  # @line L9
                _, x = heapq.heappop(heap)
                _, y = heapq.heappop(heap)
                z = h.and_(x, y)
                heapq.heappush(heap, (h.level[z >> 1], z))
            r = heap[0][1] if heap else 1  # @line L10
        memo[v] = r  # @line L11
        return r

    new_outputs = [bal(o >> 1) ^ (o & 1) for o in outputs]  # @line L2
    return h, new_outputs


def min_tree_depth(levels: list[int]) -> int:
    """The least depth of a binary tree of ANDs over leaves with these levels: ceil(log2(sum of 2^level))."""
    s = sum(1 << a for a in levels)
    return (s - 1).bit_length()
