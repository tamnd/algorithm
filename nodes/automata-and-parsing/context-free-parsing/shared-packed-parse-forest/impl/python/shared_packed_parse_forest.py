# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shared-packed-parse-forest/. The authors are listed in prov/86960D.jsonl.
"""A binarized shared packed parse forest (SPPF) of all parse trees of a string.

A grammar is a list of productions (A, rhs), where rhs is a tuple of symbols.
The nonterminals are the left sides and the start symbol; every other symbol is
a terminal. A parse tree is (A, children), where each child is a tree or a
terminal symbol; a node for an empty production has no children.

Node keys:
  ("sym", X, i, j)       symbol node: X derives w[i:j] (X a terminal or a nonterminal)
  ("mid", p, m, i, j)    intermediate node: the first m >= 2 symbols of production p derive w[i:j]
A packed node is (p, k, left, right): production p, split k, left a node key or
None, right a node key or None (both None for an empty production).
"""

import math


class SPPF:
    """The forest of all parse trees of w. Build time O(|G| n^3), size O(|G| n^3)."""

    def __init__(self, prods, start, w):
        self.prods = [(a, tuple(r)) for a, r in prods]
        self.start = start
        self.w = list(w)
        self.nts = {a for a, _ in self.prods} | {start}
        self.packed = {}  # node key -> list of packed nodes
        self.root = None
        self._recognize()  # @line L1
        n = len(self.w)
        if (start, 0, n) not in self.derives:  # @line L2
            return
        self.root = ("sym", start, 0, n)  # @line L3
        self.packed[self.root] = []
        work = [self.root]
        while work:  # @line L4
            u = work.pop()
            if u[0] == "sym" and u[1] in self.nts:  # @line L5
                _, a, i, j = u
                for p in self.by_lhs.get(a, ()):
                    m = len(self.prods[p][1])
                    if (p, m, i, j) in self.prefix:
                        self._expand(u, p, m, i, j, work)
            elif u[0] == "mid":  # @line L6
                _, p, m, i, j = u
                self._expand(u, p, m, i, j, work)

    def _recognize(self):
        """Bottom-up chart: derives = {(X, i, j) : X =>* w[i:j]} and prefix =
        {(p, m, i, j) : the first m symbols of production p derive w[i:j]}."""
        n, prods, nts = len(self.w), self.prods, self.nts
        self.by_lhs = {}
        for p, (a, _) in enumerate(prods):
            self.by_lhs.setdefault(a, []).append(p)
        derives, prefix = set(), set()
        ends = {}  # (X, i) -> list of j with (X, i, j) in derives
        waiting = {}  # (X, j) -> list of (p, m, i): prefix (p, m, i, j) needs X next
        agenda = []
        for i, a in enumerate(self.w):
            agenda.append(("d", a, i, i + 1))
        for p in range(len(prods)):
            for i in range(n + 1):
                agenda.append(("p", p, 0, i, i))
        while agenda:
            fact = agenda.pop()
            if fact[0] == "d":
                _, x, i, j = fact
                if (x, i, j) in derives:
                    continue
                derives.add((x, i, j))
                ends.setdefault((x, i), []).append(j)
                for p, m, h in waiting.get((x, i), ()):
                    agenda.append(("p", p, m + 1, h, j))
            else:
                _, p, m, i, j = fact
                if (p, m, i, j) in prefix:
                    continue
                prefix.add((p, m, i, j))
                a, rhs = prods[p]
                if m == len(rhs):
                    agenda.append(("d", a, i, j))
                else:
                    x = rhs[m]
                    waiting.setdefault((x, j), []).append((p, m, i))
                    for k in ends.get((x, j), ()):
                        agenda.append(("p", p, m + 1, i, k))
        self.derives, self.prefix = derives, prefix

    def _node(self, key, work):
        """Return the node with this key, creating it (and scheduling its expansion) if new."""
        if key not in self.packed:
            self.packed[key] = []
            work.append(key)
        return key

    def _expand(self, u, p, m, i, j, work):
        """Add to u one packed node for each way the first m symbols of p split over w[i:j]."""
        rhs = self.prods[p][1]
        if m == 0:  # @line L7
            self.packed[u].append((p, i, None, None))
            return
        x = rhs[m - 1]
        if m == 1:  # @line L8
            if (x, i, j) in self.derives:
                self.packed[u].append((p, i, None, self._node(("sym", x, i, j), work)))
            return
        for k in range(i, j + 1):  # @line L9
            if (p, m - 1, i, k) in self.prefix and (x, k, j) in self.derives:  # @line L10
                if m - 1 == 1:
                    left = self._node(("sym", rhs[0], i, k), work)
                else:
                    left = self._node(("mid", p, m - 1, i, k), work)
                right = self._node(("sym", x, k, j), work)
                self.packed[u].append((p, k, left, right))  # @line L11

    # ---- queries -------------------------------------------------------

    def size(self):
        """(symbol nodes, intermediate nodes, packed nodes)."""
        sym = sum(1 for u in self.packed if u[0] == "sym")
        return sym, len(self.packed) - sym, sum(len(v) for v in self.packed.values())

    def _children(self, u):
        out = []
        for _, _, left, right in self.packed[u]:
            if left is not None:
                out.append(left)
            if right is not None:
                out.append(right)
        return out

    def is_cyclic(self):
        """True when the forest has a cycle, that is, w has infinitely many trees."""
        if self.root is None:
            return False
        color = {self.root: 1}
        stack = [(self.root, iter(self._children(self.root)))]
        while stack:
            u, it = stack[-1]
            v = next(it, None)
            if v is None:
                color[u] = 2
                stack.pop()
            elif color.get(v) == 1:
                return True
            elif v not in color:
                color[v] = 1
                stack.append((v, iter(self._children(v))))
        return False

    def _postorder(self):
        order, seen = [], {self.root}
        stack = [(self.root, iter(self._children(self.root)))]
        while stack:
            u, it = stack[-1]
            v = next(it, None)
            if v is None:
                order.append(u)
                stack.pop()
            elif v not in seen:
                seen.add(v)
                stack.append((v, iter(self._children(v))))
        return order

    def counts(self):
        """Number of trees below every node, or None when the forest is cyclic."""
        if self.root is None or self.is_cyclic():
            return None
        c = {}
        for u in self._postorder():
            if not self.packed[u]:
                c[u] = 1  # a terminal leaf
                continue
            total = 0
            for _, _, left, right in self.packed[u]:
                total += (1 if left is None else c[left]) * (1 if right is None else c[right])
            c[u] = total
        return c

    def count(self):
        """The number of parse trees of w: 0, a positive integer, or math.inf."""
        if self.root is None:
            return 0
        c = self.counts()
        return math.inf if c is None else c[self.root]

    def is_ambiguous(self):
        """True when w has at least two parse trees."""
        if self.root is None:
            return False
        return self.is_cyclic() or any(len(self.packed[u]) > 1 for u in self._postorder())

    def tree(self, r=0):
        """The r-th parse tree (0 <= r < count()) in a fixed order, built iteratively."""
        c = self.counts()
        if c is None or not 0 <= r < c[self.root]:
            raise IndexError("no such tree")
        # Unranking: pick the packed node by cumulative counts, then split the rank.
        ranks = {}

        def unrank(v, rv):
            for pk in self.packed[v]:
                _, _, left, right = pk
                cl = 1 if left is None else c[left]
                cr = 1 if right is None else c[right]
                if rv < cl * cr:
                    return pk, (rv // cr, rv % cr)
                rv -= cl * cr
            raise AssertionError("rank out of range")

        stack = [(self.root, r, False)]
        while stack:
            u, ru, expanded = stack.pop()
            if u[1] not in self.nts:
                ranks[(u, ru)] = u[1]
                continue
            if not expanded:
                seq = []
                pk, (rl, rr) = unrank(u, ru)
                p = pk[0]
                while True:
                    _, _, left, right = pk
                    if right is not None:
                        seq.append((right, rr))
                    if left is None:
                        break
                    if left[0] == "sym":
                        seq.append((left, rl))
                        break
                    pk, (rl, rr) = unrank(left, rl)
                seq.reverse()
                ranks[("seq", u, ru)] = (p, seq)
                stack.append((u, ru, True))
                for v, rv in seq:
                    stack.append((v, rv, False))
            else:
                p, seq = ranks[("seq", u, ru)]
                ranks[(u, ru)] = (self.prods[p][0], tuple(ranks[(v, rv)] for v, rv in seq))
        return ranks[(self.root, r)]

    def trees(self):
        """All parse trees of w, in the order of tree(0), tree(1), ... (finite forests only)."""
        total = self.count()
        if total == math.inf:
            raise ValueError("infinitely many trees")
        return [self.tree(r) for r in range(total)]

    def one_tree(self):
        """Some parse tree of w, also for a cyclic forest, or None. Each node gets
        the first packed node whose children all have trees already, so the
        choices are well founded and the tree is finite."""
        if self.root is None:
            return None
        parents = {}
        missing = {}
        known = {}
        queue = []
        for u, pks in self.packed.items():
            if not pks:
                known[u] = None
                queue.append(u)
            for idx, (_, _, left, right) in enumerate(pks):
                kids = [x for x in (left, right) if x is not None]
                missing[(u, idx)] = len(kids)
                for x in kids:
                    parents.setdefault(x, []).append((u, idx))
                if not kids and u not in known:
                    known[u] = idx
                    queue.append(u)
        while queue:
            v = queue.pop()
            for u, idx in parents.get(v, ()):
                missing[(u, idx)] -= 1
                if missing[(u, idx)] == 0 and u not in known:
                    known[u] = idx
                    queue.append(u)
        out = {}
        stack = [(self.root, False)]
        while stack:
            u, expanded = stack.pop()
            if u[1] not in self.nts:
                out[u] = u[1]
                continue
            if not expanded:
                pk = self.packed[u][known[u]]
                p, seq = pk[0], []
                while True:
                    _, _, left, right = pk
                    if right is not None:
                        seq.append(right)
                    if left is None:
                        break
                    if left[0] == "sym":
                        seq.append(left)
                        break
                    pk = self.packed[left][known[left]]
                seq.reverse()
                out[("seq", u)] = (p, seq)
                stack.append((u, True))
                stack.extend((v, False) for v in seq if v not in out)
            else:
                p, seq = out[("seq", u)]
                out[u] = (self.prods[p][0], tuple(out[v] for v in seq))
        return out[self.root]

    def _chain_ok(self, u, p, bounds):
        """True when the packed nodes of u (and the intermediate nodes below it)
        split production p at the given boundaries bounds[0] <= ... <= bounds[m]."""
        rhs, i = self.prods[p][1], bounds[0]
        m = len(rhs)
        if m == 0:
            return (p, i, None, None) in self.packed[u]
        node = u
        for mm in range(m, 0, -1):
            k = bounds[mm - 1]
            right = ("sym", rhs[mm - 1], k, bounds[mm])
            if mm == 1:
                left = None
            elif mm == 2:
                left = ("sym", rhs[0], i, k)
            else:
                left = ("mid", p, mm - 1, i, k)
            if (p, k, left, right) not in self.packed.get(node, ()):
                return False
            if mm <= 2:
                return True
            node = left
        return True

    def contains(self, tree):
        """True when the parse tree is one of the trees of the forest."""
        if self.root is None or isinstance(tree, str) or tree[0] != self.start:
            return False
        n, pos = len(self.w), 0
        stack = [(tree, [0])]  # (tree node, boundaries of its children so far)
        while stack:
            t, bounds = stack[-1]
            kids = t[1]
            if len(bounds) - 1 < len(kids):
                kid = kids[len(bounds) - 1]
                if isinstance(kid, str):
                    if pos >= n or self.w[pos] != kid:
                        return False
                    pos += 1
                    bounds.append(pos)
                else:
                    stack.append((kid, [pos]))
                continue
            stack.pop()
            a = t[0]
            rhs = tuple(k if isinstance(k, str) else k[0] for k in kids)
            u = ("sym", a, bounds[0], bounds[-1])
            if u not in self.packed:
                return False
            if not any(self.prods[p][1] == rhs and self._chain_ok(u, p, bounds)
                       for p in self.by_lhs.get(a, ())):
                return False
            if stack:
                stack[-1][1].append(pos)
        return pos == n
