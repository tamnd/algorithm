# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bitset-adjacency-matrix/. The authors are listed in prov/WJ5KV3.jsonl.


class BitsetAdjacencyMatrix:
    """A graph on 0, ..., n - 1 whose matrix rows are packed into w-bit words.

    Bit v % w of word rows[u][v // w] is 1 when (u, v) is an edge. adjacent,
    add_edge and remove_edge take O(1) word operations; neighbors takes
    O(n/w + d(u)); degree and common take O(n/w). The space is n * ceil(n/w)
    words.
    """

    def __init__(self, n: int, directed: bool = False, w: int = 64) -> None:
        if n < 0 or w < 1:
            raise ValueError("need n >= 0 and w >= 1")
        self.n = n
        self.w = w
        self.directed = directed
        words = -(-n // w)
        self.rows: list[list[int]] = [[0] * words for _ in range(n)]  # @line L1

    def _check(self, u: int, v: int) -> None:
        if not (0 <= u < self.n and 0 <= v < self.n):
            raise IndexError("vertex out of range")

    def add_edge(self, u: int, v: int) -> None:
        self._check(u, v)
        if not self.directed and u == v:
            raise ValueError("an undirected graph has no self-loops")
        w = self.w
        self.rows[u][v // w] |= 1 << (v % w)  # @line L2
        if not self.directed:
            self.rows[v][u // w] |= 1 << (u % w)  # @line L3

    def remove_edge(self, u: int, v: int) -> None:
        self._check(u, v)
        w = self.w
        self.rows[u][v // w] &= ~(1 << (v % w))  # @line L4
        if not self.directed:
            self.rows[v][u // w] &= ~(1 << (u % w))  # @line L5

    def adjacent(self, u: int, v: int) -> bool:
        self._check(u, v)
        w = self.w
        return (self.rows[u][v // w] >> (v % w)) & 1 == 1  # @line L6

    def neighbors(self, u: int) -> list[int]:
        self._check(u, u)
        out = []
        for j, word in enumerate(self.rows[u]):  # @line L7
            x = word  # @line L8
            while x:  # @line L9
                out.append(j * self.w + (x & -x).bit_length() - 1)  # @line L10
                x &= x - 1  # @line L11
        return out

    def degree(self, u: int) -> int:
        self._check(u, u)
        return sum(x.bit_count() for x in self.rows[u])  # @line L12

    def common(self, u: int, v: int) -> int:
        self._check(u, v)
        return sum((a & b).bit_count() for a, b in zip(self.rows[u], self.rows[v]))  # @line L13

    def add_vertex(self) -> int:
        if self.n % self.w == 0:
            for row in self.rows:
                row.append(0)  # @line L14
        self.rows.append([0] * (-(-(self.n + 1) // self.w)))  # @line L15
        self.n += 1
        return self.n - 1

    def edges(self) -> list[tuple[int, int]]:
        return [
            (u, v)
            for u in range(self.n)
            for v in self.neighbors(u)
            if self.directed or u < v
        ]

    def complement(self) -> "BitsetAdjacencyMatrix":
        """The complement graph: NOT of each word, then clear padding and, if undirected, the diagonal."""
        c = BitsetAdjacencyMatrix(self.n, self.directed, self.w)
        full = (1 << self.w) - 1
        r = self.n % self.w
        last = full if r == 0 else (1 << r) - 1
        for u in range(self.n):
            row = [~x & full for x in self.rows[u]]
            if row:
                row[-1] &= last
            if not self.directed:
                row[u // self.w] &= ~(1 << (u % self.w))
            c.rows[u] = row
        return c

    def check_invariant(self) -> None:
        words = -(-self.n // self.w)
        assert len(self.rows) == self.n
        r = self.n % self.w
        for u in range(self.n):
            row = self.rows[u]
            assert len(row) == words
            for x in row:
                assert 0 <= x < (1 << self.w)
            if row and r:
                assert row[-1] >> r == 0
            if not self.directed:
                assert not self.adjacent(u, u)
                for v in self.neighbors(u):
                    assert self.adjacent(v, u)
