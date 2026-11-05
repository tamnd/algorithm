# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farach-algorithm/. The authors are listed in prov/5GVP55.jsonl.

from collections.abc import Hashable, Sequence


class Tree:
    """A rooted tree with string depths. Node 0 is the root; label[v] is a suffix position or -1."""

    def __init__(self) -> None:
        self.depth: list[int] = []
        self.kids: list[list[int]] = []
        self.label: list[int] = []
        self.pos: list[int] = []  # a suffix position in the subtree: the leftmost leaf

    def new(self, depth: int, label: int = -1) -> int:
        self.depth.append(depth)
        self.kids.append([])
        self.label.append(label)
        self.pos.append(label)
        return len(self.depth) - 1

    def add(self, parent: int, child: int) -> None:
        if not self.kids[parent] and self.label[parent] < 0:
            self.pos[parent] = self.pos[child]
        self.kids[parent].append(child)


def tree_from_sa(sa: list[int], lcp: list[int], size: int) -> Tree:
    """The compacted trie of the suffixes sa, in order, with their adjacent LCP values (stack build)."""
    tree = Tree()
    stack = [tree.new(0)]
    for k, p in enumerate(sa):
        h, last = (lcp[k] if k else 0), -1
        while tree.depth[stack[-1]] > h:
            last = stack.pop()
            if tree.depth[stack[-1]] >= h:
                tree.add(stack[-1], last)
                last = -1
        if tree.depth[stack[-1]] < h:
            v = tree.new(h)
            tree.add(v, last)
            stack.append(v)
        stack.append(tree.new(size - p, p))
    while len(stack) > 1:
        last = stack.pop()
        tree.add(stack[-1], last)
    return tree


class SparseMin:
    """Range minimum values over a fixed list in O(1) per query."""

    def __init__(self, a: list[int]) -> None:
        self.t = [a[:]]
        j = 1
        while 2 * j <= len(a):
            prev = self.t[-1]
            self.t.append([min(prev[i], prev[i + j]) for i in range(len(a) - 2 * j + 1)])
            j *= 2

    def query(self, lo: int, hi: int) -> int:
        """min a[lo .. hi], lo <= hi."""
        k = (hi - lo + 1).bit_length() - 1
        return min(self.t[k][lo], self.t[k][hi - (1 << k) + 1])


def farach(codes: list[int]) -> tuple[list[int], list[int]]:
    """SA and LCP of t = codes + [0], where the codes are positive integers.

    LCP[0] = 0 and LCP[k] is the lcp of the suffixes at ranks k - 1 and k. The
    recursion is on half the length, so its depth is O(log n).
    """
    t = codes + [0]
    N = len(t)
    if N <= 4:  # @line L1
        sa = sorted(range(N), key=lambda p: t[p:])
        return sa, [0] + [_lcp_naive(t, sa[k - 1], sa[k]) for k in range(1, N)]
    pairs = [(t[p], t[p + 1] if p + 1 < N else 0) for p in range(1, N, 2)]  # @line L2
    name = {pr: r + 1 for r, pr in enumerate(sorted(set(pairs)))}
    sa_r, lcp_r = farach([name[pr] for pr in pairs])  # @line L3
    sa_o = [2 * r + 1 for r in sa_r[1:]]  # @line L4
    lcp_o = [0] * len(sa_o)
    for k in range(1, len(sa_o)):
        h = lcp_r[k + 1]
        x, y = sa_o[k - 1] + 2 * h, sa_o[k] + 2 * h
        lcp_o[k] = 2 * h + (t[x] == t[y])
    rank = [0] * N
    for k, p in enumerate(sa_o):
        rank[p] = k
    sa_e = sorted(range(0, N, 2), key=lambda p: (t[p], rank[p + 1] if p + 1 < N else -1))  # @line L5
    rmq = SparseMin(lcp_o)
    lcp_e = [0] * len(sa_e)
    for k in range(1, len(sa_e)):  # @line L6
        a, b = sa_e[k - 1], sa_e[k]
        if t[a] == t[b]:
            lo, hi = sorted((rank[a + 1], rank[b + 1]))
            lcp_e[k] = 1 + rmq.query(lo + 1, hi)
    tree_o, tree_e = tree_from_sa(sa_o, lcp_o, N), tree_from_sa(sa_e, lcp_e, N)  # @line L7
    m = Merged(t, tree_o, tree_e)  # @line L8
    sa, i, j = [], 0, 0
    while i < len(sa_o) or j < len(sa_e):  # @line L9
        if j == len(sa_e) or (i < len(sa_o) and m.less(sa_o[i], sa_e[j])):
            sa.append(sa_o[i])
            i += 1
        else:
            sa.append(sa_e[j])
            j += 1
    lcp = [0] + [m.lcp(sa[k - 1], sa[k]) for k in range(1, N)]  # @line L10
    return sa, lcp  # @line L11


def _lcp_naive(t: list[int], a: int, b: int) -> int:
    k = 0
    while t[a + k] == t[b + k]:
        k += 1
    return k


class Merged:
    """The overmerged tree M of the odd tree and the even tree, with LCA and the d-tree depths."""

    def __init__(self, t: list[int], tree_o: Tree, tree_e: Tree) -> None:
        self.t, self.n = t, len(t) - 1
        self.M = M = Tree()
        root = M.new(0)  # @line L12
        stack = [(root, (0, 0), (0, 0))]
        while stack:
            v, so, se = stack.pop()
            co, ce = self._next(tree_o, so), self._next(tree_e, se)
            for a in sorted(set(co) | set(ce)):  # @line L13
                x, y = co.get(a), ce.get(a)
                d = min(tree_o.depth[x] if x is not None else 1 << 62, tree_e.depth[y] if y is not None else 1 << 62)  # @line L14
                c = M.new(d)
                for tree, z in ((tree_o, x), (tree_e, y)):
                    if z is not None and tree.depth[z] == d and tree.label[z] >= 0:
                        M.label[c] = M.pos[c] = tree.label[z]
                M.add(v, c)
                stack.append((c, (x, d) if x is not None else None, (y, d) if y is not None else None))  # @line L15
        self._euler()
        self.memo: dict[int, int] = {}

    def _next(self, tree: Tree, s: tuple[int, int] | None) -> dict[int, int]:
        """First symbol -> target node of the edges below the point s = (node, depth) of tree."""
        if s is None:
            return {}
        v, d = s
        if d < tree.depth[v]:
            return {self.t[tree.pos[v] + d]: v}
        return {self.t[tree.pos[c] + d]: c for c in tree.kids[v]}

    def _euler(self) -> None:
        M = self.M
        self.leaf = [0] * len(self.t)
        self.first = [0] * len(M.depth)
        tour: list[int] = []
        stack = [(0, 0)]
        while stack:
            v, k = stack.pop()
            if k == 0:
                self.first[v] = len(tour)
                if M.label[v] >= 0:
                    self.leaf[M.label[v]] = v
            tour.append(v)
            if k < len(M.kids[v]):
                stack.append((v, k + 1))
                stack.append((M.kids[v][k], 0))
        self.tour = tour
        enc = [M.depth[v] * len(M.depth) + v for v in tour]  # depth first, then the node id
        self.rmq = SparseMin(enc)

    def lca(self, a: int, b: int) -> int:
        """LCA in M of the leaves of the suffixes a and b."""
        i, j = sorted((self.first[self.leaf[a]], self.first[self.leaf[b]]))
        return self.rmq.query(i, j) % len(self.M.depth)

    def ell(self, x: int, y: int) -> int:
        """lcp of suffixes x and y of different parity: the depth of LCA(x, y) in the d-tree."""
        chain = []
        while True:
            v = self.lca(x, y)  # @line L16
            if v == 0:
                base = 0
                break
            if v in self.memo:  # @line L17
                base = self.memo[v]
                break
            chain.append(v)  # @line L18
            x, y = x + 1, y + 1
        for v in reversed(chain):
            base += 1
            self.memo[v] = base
        return base

    def lcp(self, a: int, b: int) -> int:
        if (a - b) % 2 == 0:
            return self.M.depth[self.lca(a, b)]
        return self.ell(a, b)

    def less(self, a: int, b: int) -> bool:
        h = self.lcp(a, b)
        return self.t[a + h] < self.t[b + h]


def suffix_array_lcp(text: Sequence[Hashable]) -> tuple[list[int], list[int]]:
    """SA and LCP of text + $, with $ unique and smaller than every symbol; 0-based."""
    code = {c: r + 1 for r, c in enumerate(sorted(set(text)))}
    return farach([code[c] for c in text])


def suffix_tree(text: Sequence[Hashable]) -> Tree:
    """The suffix tree of text + $, built from Farach's SA and LCP."""
    sa, lcp = suffix_array_lcp(text)
    return tree_from_sa(sa, lcp, len(text) + 1)
