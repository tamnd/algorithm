# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/tango-tree/. The authors are listed in prov/MK70WC.jsonl.
"""A tango tree over the keys 1..n, with each preferred path kept as a sorted list.

The reference tree P is the balanced BST on 1..n whose root is the middle key.
Each node has a preferred child (None, 'L' or 'R'). The preferred paths are
stored as sorted Python lists of keys; a search in a path is a binary search,
which makes O(log log n) comparisons as in a real tango tree. Cut and join are
list slices here, which cost O(log n) element moves instead of the O(log log n)
of the split and concatenate of red-black trees in the real structure.
"""

from bisect import bisect_left
from typing import Dict, List, Optional, Tuple


class Path:
    __slots__ = ("keys",)

    def __init__(self, keys: List[int]) -> None:
        self.keys = keys  # sorted keys of the nodes on the path


class TangoTree:
    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError("n must be at least 1")
        self.n = n
        self.lo: Dict[int, int] = {}
        self.hi: Dict[int, int] = {}
        self.depth: Dict[int, int] = {}
        self.left: Dict[int, Optional[int]] = {}
        self.right: Dict[int, Optional[int]] = {}
        self.root = (1 + n) // 2
        stack = [(1, n, 0)]
        while stack:
            a, b, d = stack.pop()
            m = (a + b) // 2
            self.lo[m], self.hi[m], self.depth[m] = a, b, d
            self.left[m] = (a + m - 1) // 2 if a <= m - 1 else None
            self.right[m] = (m + 1 + b) // 2 if m + 1 <= b else None
            if a <= m - 1:
                stack.append((a, m - 1, d + 1))
            if m + 1 <= b:
                stack.append((m + 1, b, d + 1))
        self.pref: Dict[int, Optional[str]] = {y: None for y in self.lo}
        self.top: Dict[int, Path] = {y: Path([y]) for y in self.lo}  # path by its top node
        self.comparisons = 0
        self.lr_switches = 0  # preferred child changes between L and R: the interleave bound

    def _child(self, u: int, side: Optional[str]) -> Optional[int]:
        if side == "L":
            return self.left[u]
        if side == "R":
            return self.right[u]
        return None

    def _cut(self, path: Path, u: int) -> None:
        """Remove from path the nodes below u; they become a path of their own."""
        c = self._child(u, self.pref[u])
        if c is None:
            return
        ks = path.keys
        i, j = bisect_left(ks, self.lo[c]), bisect_left(ks, self.hi[c] + 1)
        self.top[c] = Path(ks[i:j])
        del ks[i:j]

    def _join(self, path: Path, c: Optional[int]) -> None:
        """Append to path (which ends at the parent of c) the path whose top is c."""
        if c is None:
            return
        lower = self.top.pop(c)
        ks = path.keys
        i = bisect_left(ks, self.lo[c])
        ks[i:i] = lower.keys

    def _search(self, ks: List[int], x: int) -> int:
        """Binary search; counts the comparisons, which are O(log log n)."""
        a, b = 0, len(ks)
        while a < b:
            self.comparisons += 1
            m = (a + b) // 2
            if ks[m] < x:
                a = m + 1
            else:
                b = m
        return a

    def access(self, x: int) -> Tuple[int, int]:
        """Access key x. Return (paths visited, L-R switches of this access)."""
        if x not in self.lo:
            raise KeyError(x)
        path = self.top[self.root]  # @line L1
        switches: List[Tuple[int, int]] = []
        while True:  # @line L2
            ks = path.keys
            i = self._search(ks, x)  # @line L3
            if i < len(ks) and ks[i] == x:  # @line L4
                break
            cands = [ks[j] for j in (i - 1, i) if 0 <= j < len(ks)]  # @line L5
            u = max(cands, key=lambda y: self.depth[y])
            side = "L" if x < u else "R"  # @line L6
            c = self._child(u, side)
            switches.append((u, c))
            path = self.top[c]  # @line L7
        before = self.lr_switches
        p = self.top[self.root]  # each join moves the lower path into this one
        for u, c in switches:  # @line L8
            if self.pref[u] is not None:
                self.lr_switches += 1
            self._cut(p, u)  # @line L9
            self._join(p, c)  # @line L10
            self.pref[u] = "L" if c == self.left[u] else "R"
        if self.pref[x] != "L":  # @line L11
            if self.pref[x] == "R":
                self.lr_switches += 1
            self._cut(p, x)
            self._join(p, self.left[x])
            self.pref[x] = "L"
        return len(switches) + 1, self.lr_switches - before

    def paths(self) -> List[List[int]]:
        return [p.keys for p in self.top.values()]

    def check_invariant(self) -> None:
        seen = set()
        for t, p in self.top.items():
            assert p.keys == sorted(p.keys)
            # the path is the chain of preferred children from t
            chain = []
            y: Optional[int] = t
            while y is not None:
                chain.append(y)
                y = self._child(y, self.pref[y])
            assert sorted(chain) == p.keys, (t, chain, p.keys)
            for y in chain:
                assert y not in seen
                seen.add(y)
            # the top is the root or a child that is not its parent's preferred child
            if t != self.root:
                par = self._parent(t)
                assert self._child(par, self.pref[par]) != t
        assert seen == set(self.lo)

    def _parent(self, y: int) -> int:
        v = self.root
        while True:
            c = self.left[v] if y < v else self.right[v]
            if c == y:
                return v
            v = c  # type: ignore[assignment]
