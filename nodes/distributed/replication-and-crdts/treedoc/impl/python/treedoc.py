# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/treedoc/. The authors are listed in prov/13DJ1S.jsonl.

"""Treedoc (Preguica, Marques, Shapiro and Letia 2009), a sequence CRDT on a binary tree.

The position of an element is a path from the root: a list of steps
(side, dis), where side 0 is left and side 1 is right. Concurrent inserts at
the same path become mini-nodes of one major node, told apart and ordered by
a unique disambiguator dis = (clock, site). The document is the infix walk of
the tree: left subtree, the node, right subtree, with mini-nodes in dis order.
A delete leaves a tombstone. To insert between adjacent p and q, a replica
makes a right child of p when p has none, and a left child of q otherwise.
flatten rebuilds a balanced tree with no tombstones. It changes every
position, so all replicas must run it on the same state, which needs a
commitment protocol; the method here is only the local step.
"""

import bisect
from typing import Any

Dis = tuple[int, int]  # (clock, site)
Step = tuple[int, Dis]  # (side, dis)
Path = tuple[Step, ...]
FLAT: Dis = (0, -1)  # the disambiguator used by flatten


def key(path: Path) -> tuple:
    """A sort key whose order is the infix order of the tree."""
    return tuple((2 * side, dis) for side, dis in path) + ((1,),)  # @line L1


class Treedoc:
    """One Treedoc replica with site id site."""

    def __init__(self, site: int) -> None:
        self.site = site
        self.clock = 0
        self.keys: list[tuple] = [key(())]  # the root, a fixed start mark
        self.path: dict[tuple, Path] = {key(()): ()}
        self.val: dict[Path, Any] = {}
        self.dead: set[Path] = set()
        self.right_kids: set[Path] = set()  # paths that have at least one right child

    def _add(self, p: Path, value: Any) -> None:
        k = key(p)
        if k in self.path:
            return
        bisect.insort(self.keys, k)  # @line L2
        self.path[k] = p
        self.val[p] = value
        if p and p[-1][0] == 1:
            self.right_kids.add(p[:-1])

    def _visible(self) -> list[Path]:
        return [self.path[k] for k in self.keys[1:] if self.path[k] not in self.dead]

    def new_path(self, p: Path, q: Path | None) -> Path:
        """A path strictly between p and its successor q in the full order."""
        self.clock += 1
        dis = (self.clock, self.site)  # @line L3
        if p not in self.right_kids:  # @line L4
            return p + ((1, dis),)  # @line L5
        assert q is not None, "p has a right child, so p has a successor"
        return q + ((0, dis),)  # @line L6

    def local_insert(self, i: int, value: Any) -> tuple:
        vis = self._visible()
        p = vis[i - 1] if i > 0 else ()
        j = bisect.bisect_right(self.keys, key(p))
        q = self.path[self.keys[j]] if j < len(self.keys) else None
        op = ("ins", self.new_path(p, q), value)
        self.apply(op)
        return op

    def local_delete(self, i: int) -> tuple:
        op = ("del", self._visible()[i])
        self.apply(op)
        return op

    def apply(self, op: tuple) -> None:
        if op[0] == "ins":
            self._add(op[1], op[2])
        else:
            self.dead.add(op[1])  # @line L7

    def flatten(self) -> None:
        """Rebuild a balanced tree of the live elements. Run only on an agreed state."""
        items = [self.val[p] for p in self._visible()]
        self.__init__(self.site)
        clock = self.clock

        def build(lo: int, hi: int, prefix: Path) -> None:
            if lo >= hi:
                return
            mid = (lo + hi) // 2
            self._add(prefix, items[mid])
            build(lo, mid, prefix + ((0, FLAT),))
            build(mid + 1, hi, prefix + ((1, FLAT),))

        build(0, len(items), ((1, FLAT),))
        self.clock = clock

    def value(self) -> list[Any]:
        return [self.val[p] for p in self._visible()]

    def order(self) -> list[Path]:
        return [self.path[k] for k in self.keys]

    def check_invariant(self) -> None:
        assert self.keys == sorted(self.keys) and len(set(self.keys)) == len(self.keys)
        assert self.dead <= set(self.val)
