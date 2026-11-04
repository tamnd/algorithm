# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/range-min-max-tree/. The authors are listed in prov/EHY1SS.jsonl.
"""Range min-max tree over a balanced parenthesis sequence.

P is cut into blocks of b symbols. A complete binary tree over the
blocks stores, for each node, the total excess e of its range and the
minimum m and maximum M of the excess at the positions of the range,
relative to the excess just before the range. fwdsearch and bwdsearch
scan at most two blocks and walk O(log(n / b)) tree nodes.
"""

from __future__ import annotations

from typing import Optional, Sequence

_INF = 1 << 60


class RangeMinMaxTree:
    """fwdsearch, bwdsearch, findclose, findopen and enclose over parentheses."""

    def __init__(self, parens: Sequence[int] | str, b: int = 32) -> None:
        """``parens`` is a 0/1 sequence (1 = '(') or a string of '(' and ')'."""
        if isinstance(parens, str):
            parens = [1 if c == "(" else 0 for c in parens]
        self.P = list(parens)
        self.N = len(self.P)
        self.b = b
        nblocks = max(1, -(-self.N // b))
        size = 1
        while size < nblocks:
            size *= 2
        self.size = size
        self.e = [0] * (2 * size)
        self.m = [_INF] * (2 * size)
        self.M = [-_INF] * (2 * size)
        self.before = [0] * (nblocks + 1)  # excess before each block
        for k in range(nblocks):
            cur, lo, hi = 0, _INF, -_INF
            for j in range(k * b, min(self.N, (k + 1) * b)):
                cur += 1 if self.P[j] else -1
                lo, hi = min(lo, cur), max(hi, cur)
            v = size + k
            self.e[v], self.m[v], self.M[v] = cur, lo, hi
            self.before[k + 1] = self.before[k] + cur
        for v in range(size - 1, 0, -1):
            l, r = 2 * v, 2 * v + 1
            self.e[v] = self.e[l] + self.e[r]
            self.m[v] = min(self.m[l], self.e[l] + self.m[r])
            self.M[v] = max(self.M[l], self.e[l] + self.M[r])

    def _step(self, j: int) -> int:
        return 1 if self.P[j] else -1

    def excess(self, i: int) -> int:
        """E(i): opens minus closes in P[0..i]; E(-1) = 0."""
        if i < 0:
            return 0
        k = i // self.b
        cur = self.before[k]
        for j in range(k * self.b, i + 1):
            cur += self._step(j)
        return cur

    def _contains(self, v: int, base: int, t: int) -> bool:
        return base + self.m[v] <= t <= base + self.M[v]

    def fwdsearch(self, i: int, d: int) -> Optional[int]:
        """Least j > i with E(j) = E(i) + d, or None; 0 <= i < N."""
        t = self.excess(i) + d  # @line L1
        k = i // self.b
        cur = t - d
        for j in range(i + 1, min(self.N, (k + 1) * self.b)):  # @line L2
            cur += self._step(j)
            if cur == t:
                return j
        v, cur = self.size + k, self.before[k + 1]  # @line L3
        while v > 1:  # @line L4
            if v % 2 == 0 and self._contains(v + 1, cur, t):  # @line L5
                return self._descend_fwd(v + 1, cur, t)
            if v % 2 == 0:  # @line L6
                cur += self.e[v + 1]
            v //= 2  # @line L7
        return None  # @line L8

    def _descend_fwd(self, v: int, cur: int, t: int) -> int:
        """First position with excess t in the range of v; cur = excess before it."""
        while v < self.size:  # @line L9
            if self._contains(2 * v, cur, t):  # @line L10
                v = 2 * v
            else:  # @line L11
                cur += self.e[2 * v]
                v = 2 * v + 1
        k = v - self.size  # @line L12
        for j in range(k * self.b, min(self.N, (k + 1) * self.b)):
            cur += self._step(j)
            if cur == t:
                return j
        raise AssertionError("the min-max bounds promised a hit")

    def bwdsearch(self, i: int, d: int) -> Optional[int]:
        """Greatest j < i with E(j) = E(i) + d, or None; j = -1 stands for E(-1) = 0."""
        t = self.excess(i) + d
        k = i // self.b
        cur = t - d
        for j in range(i, k * self.b, -1):
            cur -= self._step(j)  # now cur = E(j - 1)
            if cur == t:
                return j - 1
        v, cur = self.size + k, self.before[k]  # cur = E(kb - 1)
        while v > 1:
            if v % 2 == 1 and self._contains(v - 1, cur - self.e[v - 1], t):
                return self._descend_bwd(v - 1, cur, t)
            if v % 2 == 1:
                cur -= self.e[v - 1]
            v //= 2
        return -1 if t == 0 else None

    def _descend_bwd(self, v: int, end_e: int, t: int) -> int:
        """Last position with excess t in the range of v; end_e = excess at its end."""
        while v < self.size:
            r = 2 * v + 1
            if self._contains(r, end_e - self.e[r], t):
                v = r
            else:
                end_e -= self.e[r]
                v = 2 * v
        k = v - self.size
        cur = end_e
        for j in range(min(self.N, (k + 1) * self.b) - 1, k * self.b - 1, -1):
            if cur == t:
                return j
            cur -= self._step(j)
        raise AssertionError("the min-max bounds promised a hit")

    def findclose(self, i: int) -> int:
        """The ')' matching the '(' at i."""
        j = self.fwdsearch(i, -1)  # @line L13
        assert j is not None
        return j

    def findopen(self, j: int) -> int:
        """The '(' matching the ')' at j."""
        i = self.bwdsearch(j, 0)  # @line L14
        assert i is not None
        return i + 1

    def enclose(self, i: int) -> Optional[int]:
        """The '(' of the tightest pair strictly containing the '(' at i, or None."""
        j = self.bwdsearch(i, -2)  # @line L15
        return None if j is None else j + 1

    def min_excess(self, i: int, j: int) -> int:
        """The minimum of E over positions i..j, 0 <= i <= j < N."""
        ki, kj = i // self.b, j // self.b
        cur = self.excess(i)
        best = cur
        if ki == kj:
            for x in range(i + 1, j + 1):
                cur += self._step(x)
                best = min(best, cur)
            return best
        for x in range(i + 1, (ki + 1) * self.b):
            cur += self._step(x)
            best = min(best, cur)
        nodes: list[int] = []
        self._cover(1, 0, self.size - 1, ki + 1, kj - 1, nodes)
        for v in nodes:
            best = min(best, cur + self.m[v])
            cur += self.e[v]
        for x in range(kj * self.b, j + 1):
            cur += self._step(x)
            best = min(best, cur)
        return best

    def _cover(self, v: int, lo: int, hi: int, a: int, z: int, out: list[int]) -> None:
        """Append, left to right, the canonical nodes covering blocks a..z."""
        if z < lo or hi < a or a > z:
            return
        if a <= lo and hi <= z:
            out.append(v)
            return
        mid = (lo + hi) // 2
        self._cover(2 * v, lo, mid, a, z, out)
        self._cover(2 * v + 1, mid + 1, hi, a, z, out)

    def rmq(self, i: int, j: int) -> int:
        """Leftmost position of the minimum of E over i..j."""
        mn = self.min_excess(i, j)
        e = self.excess(i)
        if e == mn:
            return i
        r = self.fwdsearch(i, mn - e)
        assert r is not None
        return r
