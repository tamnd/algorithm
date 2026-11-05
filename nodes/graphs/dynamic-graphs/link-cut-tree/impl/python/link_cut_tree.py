# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/link-cut-tree/. The authors are listed in prov/45BF01.jsonl.

"""Link-cut trees (Sleator and Tarjan) on splay trees.

The forest is split into vertex-disjoint preferred paths. Each path is kept in
a splay tree ordered by depth. The root of a splay tree keeps a path-parent
pointer to the tree node above the top of its path. The structure supports
link, cut, make_root (evert), find_root, connected and path sums and maxima in
O(log n) amortized time per operation. It is fully dynamic for forests and
deterministic. All loops are iterative, so long paths cause no recursion.
"""

NEG = float("-inf")


class LinkCutForest:
    """A forest on the vertices 0..n-1 with integer vertex values."""

    def __init__(self, n: int, values: list[int] | None = None) -> None:
        self.n = n
        self.left = [-1] * n
        self.right = [-1] * n
        self.par = [-1] * n  # splay parent, or path-parent at a splay root
        self.rev = [False] * n
        self.val = list(values) if values is not None else [0] * n
        self.sum = list(self.val)
        self.mx = list(self.val)

    # ----- splay tree helpers -----

    def _is_root(self, x: int) -> bool:
        p = self.par[x]
        return p == -1 or (self.left[p] != x and self.right[p] != x)

    def _pull(self, x: int) -> None:
        s, m = self.val[x], self.val[x]
        for c in (self.left[x], self.right[x]):
            if c != -1:
                s += self.sum[c]
                if self.mx[c] > m:
                    m = self.mx[c]
        self.sum[x], self.mx[x] = s, m

    def _push(self, x: int) -> None:
        if self.rev[x]:
            l, r = self.left[x], self.right[x]
            self.left[x], self.right[x] = r, l
            if l != -1:
                self.rev[l] = not self.rev[l]
            if r != -1:
                self.rev[r] = not self.rev[r]
            self.rev[x] = False

    def _rotate(self, x: int) -> None:
        p = self.par[x]
        g = self.par[p]
        p_root = self._is_root(p)
        if self.left[p] == x:
            b = self.right[x]
            self.left[p] = b
            self.right[x] = p
        else:
            b = self.left[x]
            self.right[p] = b
            self.left[x] = p
        if b != -1:
            self.par[b] = p
        self.par[p] = x
        self.par[x] = g
        if not p_root:
            if self.left[g] == p:
                self.left[g] = x
            else:
                self.right[g] = x
        self._pull(p)
        self._pull(x)

    def _splay(self, x: int) -> None:
        # Push pending reversals from the splay root down to x first.
        path = [x]
        y = x
        while not self._is_root(y):
            y = self.par[y]
            path.append(y)
        for y in reversed(path):
            self._push(y)
        while not self._is_root(x):
            p = self.par[x]
            if not self._is_root(p):
                g = self.par[p]
                zigzig = (self.left[g] == p) == (self.left[p] == x)
                self._rotate(p if zigzig else x)
            self._rotate(x)

    # ----- the operations of the main pseudocode -----

    def access(self, v: int) -> None:
        """Make the path from the tree root to v preferred, and splay v."""
        last = -1  # @line L1
        x = v  # @line L2
        while x != -1:
            self._splay(x)  # @line L3
            self.right[x] = last  # @line L4
            self._pull(x)
            last = x  # @line L5
            x = self.par[x]
        self._splay(v)  # @line L6

    def make_root(self, v: int) -> None:
        self.access(v)  # @line L7
        self.rev[v] = not self.rev[v]  # @line L8

    def find_root(self, v: int) -> int:
        self.access(v)  # @line L9
        x = v
        self._push(x)
        while self.left[x] != -1:
            x = self.left[x]
            self._push(x)
        self._splay(x)  # @line L10
        return x

    def connected(self, u: int, v: int) -> bool:
        return u == v or self.find_root(u) == self.find_root(v)

    def link(self, u: int, v: int) -> None:
        """Add the edge {u, v}; u and v must be in different trees."""
        if self.connected(u, v):
            raise ValueError("link would create a cycle")
        self.make_root(u)  # @line L11
        self.access(v)
        self.par[u] = v  # @line L12

    def cut(self, u: int, v: int) -> None:
        """Remove the edge {u, v}, which must be in the forest."""
        self.make_root(u)  # @line L13
        self.access(v)
        if self.left[v] != u or self.right[u] != -1:
            raise ValueError("no such edge")
        self.left[v] = -1  # @line L14
        self.par[u] = -1
        self._pull(v)

    def path_sum(self, u: int, v: int) -> int:
        """Sum of the values on the tree path from u to v."""
        self.make_root(u)  # @line L15
        self.access(v)
        return self.sum[v]  # @line L16

    def path_max(self, u: int, v: int) -> int:
        self.make_root(u)
        self.access(v)
        return self.mx[v]

    def set_value(self, v: int, x: int) -> None:
        self.access(v)
        self.val[v] = x
        self._pull(v)

    def lca(self, root: int, u: int, v: int) -> int:
        """Lowest common ancestor of u and v when the tree is rooted at root."""
        self.make_root(root)
        self.access(u)
        last = -1
        x = v
        while x != -1:
            self._splay(x)
            self.right[x] = last
            self._pull(x)
            last = x
            x = self.par[x]
        self._splay(v)
        return last
