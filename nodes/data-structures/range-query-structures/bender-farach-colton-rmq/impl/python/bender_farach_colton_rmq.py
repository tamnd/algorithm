# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/bender-farach-colton-rmq/. The authors are listed in prov/WNYTAQ.jsonl.

from typing import Sequence


class BenderFarachColtonRMQ:
    """Range minimum queries in O(1) after O(n) preprocessing.

    The array is turned into its Cartesian tree, the tree into the depth
    sequence of an Euler tour (adjacent depths differ by one), and that
    sequence is cut into blocks of size about (lg m) / 2 for m = 2n - 1.
    A sparse table over the block minima answers spans of whole blocks, and
    one table per block shape answers queries inside a block. query(l, r)
    returns the position of the leftmost minimum of a[l..r].
    """

    def __init__(self, a: Sequence[int], block: int = 0) -> None:
        """Preprocess a; block <= 0 picks max(1, floor(lg m / 2))."""
        self.a = list(a)
        n = len(self.a)
        self.n = n
        # L1: Cartesian tree with the leftmost minimum at the root.
        parent = [-1] * n
        left = [-1] * n
        right = [-1] * n
        stack: list[int] = []
        for i in range(n):  # @line L1
            last = -1
            while stack and self.a[stack[-1]] > self.a[i]:
                last = stack.pop()
            if last != -1:
                left[i] = last
                parent[last] = i
            if stack:
                right[stack[-1]] = i
                parent[i] = stack[-1]
            stack.append(i)
        self.root = stack[0] if stack else -1
        self.parent = parent
        # L2: Euler tour of node ids, their depths and first occurrences.
        self.euler: list[int] = []
        self.depth: list[int] = []
        self.first = [0] * n
        if n:
            # state 0: first visit, 1: the left child is done, 2: both are done
            work = [(self.root, 0, 0)]
            while work:  # @line L2
                v, d, st = work.pop()
                if st == 0:
                    self.first[v] = len(self.euler)
                self.euler.append(v)
                self.depth.append(d)
                if st == 0 and left[v] != -1:
                    work.append((v, d, 1))
                    work.append((left[v], d + 1, 0))
                elif st <= 1 and right[v] != -1:
                    work.append((v, d, 2))
                    work.append((right[v], d + 1, 0))
        m = len(self.depth)
        self.m = m
        b = block if block > 0 else max(1, (max(m, 1).bit_length() - 1) // 2)  # @line L3
        self.b = b
        nb = (m + b - 1) // b
        self.block_min: list[int] = []
        self.block_shape: list[tuple[int, int]] = []
        self.tables: dict[tuple[int, int], list[list[int]]] = {}
        for j in range(nb):  # @line L4
            s, e = j * b, min(m, (j + 1) * b)
            best = s
            sig = 0
            for k in range(s + 1, e):
                if self.depth[k] < self.depth[best]:
                    best = k
                if self.depth[k] > self.depth[k - 1]:
                    sig |= 1 << (k - s - 1)
            self.block_min.append(best)
            shape = (e - s, sig)
            self.block_shape.append(shape)
            if shape not in self.tables:  # @line L6
                self.tables[shape] = self._shape_table(*shape)
        # L5: sparse table over the block minima, storing positions in depth.
        self.sparse: list[list[int]] = [list(self.block_min)]
        h = 1
        while 2 * h <= nb:  # @line L5
            prev = self.sparse[-1]
            row = []
            for j in range(nb - 2 * h + 1):
                x, y = prev[j], prev[j + h]
                row.append(x if self.depth[x] <= self.depth[y] else y)
            self.sparse.append(row)
            h *= 2

    @staticmethod
    def _shape_table(length: int, sig: int) -> list[list[int]]:
        """table[i][k] = offset of the leftmost minimum of offsets i..k."""
        d = [0] * length
        for k in range(1, length):
            d[k] = d[k - 1] + (1 if sig >> (k - 1) & 1 else -1)
        table = [[0] * length for _ in range(length)]
        for i in range(length):
            best = i
            for k in range(i, length):
                if d[k] < d[best]:
                    best = k
                table[i][k] = best
        return table

    def _in_block(self, j: int, x: int, y: int) -> int:
        s = j * self.b
        return s + self.tables[self.block_shape[j]][x - s][y - s]

    def _better(self, x: int, y: int) -> int:
        return x if self.depth[x] <= self.depth[y] else y

    def _blocks(self, i: int, j: int) -> int:
        """Position of a minimum depth over the blocks i..j, i <= j."""
        k = (j - i + 1).bit_length() - 1
        row = self.sparse[k]
        return self._better(row[i], row[j - (1 << k) + 1])

    def query(self, l: int, r: int) -> int:
        """Position of the leftmost minimum of a[l..r], 0 <= l <= r < n."""
        if not 0 <= l <= r < self.n:
            raise IndexError(f"bad range [{l}, {r}] for length {self.n}")
        x, y = self.first[l], self.first[r]  # @line L7
        if x > y:
            x, y = y, x
        bx, by = x // self.b, y // self.b  # @line L8
        if bx == by:  # @line L9
            k = self._in_block(bx, x, y)
        else:  # @line L10
            k = self._better(self._in_block(bx, x, bx * self.b + self.b - 1), self._in_block(by, by * self.b, y))
            if bx + 1 <= by - 1:
                k = self._better(k, self._blocks(bx + 1, by - 1))
        return self.euler[k]  # @line L11

    def check_invariant(self) -> None:
        """Check the Cartesian tree, the Euler tour and the block data."""
        for v in range(self.n):
            p = self.parent[v]
            if p == -1:
                assert v == self.root
            else:
                assert self.a[p] <= self.a[v]
                assert self.a[p] < self.a[v] or p < v
        assert self.m == (2 * self.n - 1 if self.n else 0)
        for k in range(1, self.m):
            assert abs(self.depth[k] - self.depth[k - 1]) == 1
        for v in range(self.n):
            assert self.euler[self.first[v]] == v
        for j, best in enumerate(self.block_min):
            s, e = j * self.b, min(self.m, (j + 1) * self.b)
            assert self.depth[best] == min(self.depth[s:e])
        assert len(self.tables) <= 2 ** max(0, self.b - 1) + 1
