# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/zero-suppressed-bdd/. The authors are listed in prov/73ZZQJ.jsonl.

"""Zero-suppressed BDDs (ZDDs) for families of subsets of {0, ..., n-1}.

Node 0 is the empty family (written ⊥ on the page) and node 1 is the family
{∅} (written ⊤). An inner node u is nodes[u] = (v, lo, hi). It stands for
the family lo ∪ {S ∪ {v} : S ∈ hi}, where no set of lo or hi contains v or a
smaller element. The element order is 0 < 1 < ... < n-1, with 0 on top, and
the sinks have the variable n.

The zero-suppressed rule: getnode never makes a node with hi = ⊥. With the
unique table, equal families give the same node (canonicity).

Each binary operation is memoized, so it makes O(|P| |Q|) calls of getnode,
except join, which also calls union. The recursion depth is at most n + 1.
"""

EMPTY, BASE = 0, 1  # the families ∅ and {∅}


class ZDD:
    def __init__(self, n: int) -> None:
        self.n = n
        self.nodes: list[tuple[int, int, int]] = [(n, 0, 0), (n, 1, 1)]
        self.unique: dict[tuple[int, int, int], int] = {}
        self.memo: dict[tuple[str, int, int], int] = {}

    def var(self, u: int) -> int:
        return self.nodes[u][0]

    def getnode(self, v: int, lo: int, hi: int) -> int:
        if hi == EMPTY:  # @line L1
            return lo  # @line L2
        key = (v, lo, hi)
        u = self.unique.get(key)  # @line L3
        if u is None:
            u = len(self.nodes)  # @line L4
            self.nodes.append(key)
            self.unique[key] = u
        return u  # @line L5

    def split(self, u: int, v: int) -> tuple[int, int]:
        """The sets without v and the sets with v (v removed), when v <= var(u)."""
        w, lo, hi = self.nodes[u]
        return (lo, hi) if w == v else (u, EMPTY)

    def union(self, p: int, q: int) -> int:
        if p == EMPTY:  # @line L6
            return q
        if q == EMPTY or p == q:
            return p
        key = ("u", min(p, q), max(p, q))
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(p), self.var(q))  # @line L7
            p0, p1 = self.split(p, v)
            q0, q1 = self.split(q, v)
            r = self.getnode(v, self.union(p0, q0), self.union(p1, q1))  # @line L8
            self.memo[key] = r
        return r

    def intersect(self, p: int, q: int) -> int:
        if p == EMPTY or q == EMPTY:
            return EMPTY
        if p == q:
            return p
        key = ("i", min(p, q), max(p, q))
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(p), self.var(q))
            p0, p1 = self.split(p, v)
            q0, q1 = self.split(q, v)
            if v == self.n:
                r = BASE  # both are BASE here
            else:
                r = self.getnode(v, self.intersect(p0, q0), self.intersect(p1, q1))
            self.memo[key] = r
        return r

    def diff(self, p: int, q: int) -> int:
        if p == EMPTY or p == q:
            return EMPTY
        if q == EMPTY:
            return p
        key = ("d", p, q)
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(p), self.var(q))
            p0, p1 = self.split(p, v)
            q0, q1 = self.split(q, v)
            r = self.getnode(v, self.diff(p0, q0), self.diff(p1, q1))
            self.memo[key] = r
        return r

    def join(self, p: int, q: int) -> int:
        """The family {S ∪ T : S ∈ p, T ∈ q}."""
        if p == EMPTY or q == EMPTY:
            return EMPTY
        if p == BASE:
            return q
        if q == BASE:
            return p
        key = ("j", min(p, q), max(p, q))
        r = self.memo.get(key)
        if r is None:
            v = min(self.var(p), self.var(q))
            p0, p1 = self.split(p, v)
            q0, q1 = self.split(q, v)
            with_v = self.union(self.join(p1, q1), self.union(self.join(p1, q0), self.join(p0, q1)))
            r = self.getnode(v, self.join(p0, q0), with_v)
            self.memo[key] = r
        return r

    def subset0(self, p: int, v: int) -> int:
        """The sets of p that do not contain v."""
        if self.var(p) > v:
            return p
        if self.var(p) == v:
            return self.nodes[p][1]
        key = ("s0", p, v)
        r = self.memo.get(key)
        if r is None:
            w, lo, hi = self.nodes[p]
            r = self.getnode(w, self.subset0(lo, v), self.subset0(hi, v))
            self.memo[key] = r
        return r

    def subset1(self, p: int, v: int) -> int:
        """The sets of p that contain v, with v removed."""
        if self.var(p) > v:
            return EMPTY
        if self.var(p) == v:
            return self.nodes[p][2]
        key = ("s1", p, v)
        r = self.memo.get(key)
        if r is None:
            w, lo, hi = self.nodes[p]
            r = self.getnode(w, self.subset1(lo, v), self.subset1(hi, v))
            self.memo[key] = r
        return r

    def change(self, p: int, v: int) -> int:
        """Toggle v in each set of p."""
        if self.var(p) > v:
            return self.getnode(v, EMPTY, p)
        if self.var(p) == v:
            return self.getnode(v, self.nodes[p][2], self.nodes[p][1])
        key = ("c", p, v)
        r = self.memo.get(key)
        if r is None:
            w, lo, hi = self.nodes[p]
            r = self.getnode(w, self.change(lo, v), self.change(hi, v))
            self.memo[key] = r
        return r

    def count(self, p: int) -> int:
        c = {EMPTY: 0, BASE: 1}
        for u in self.below(p):
            c[u] = c[self.nodes[u][1]] + c[self.nodes[u][2]]
        return c[p]

    def reach(self, root: int) -> set[int]:
        """All nodes that root reaches, with the sinks."""
        seen = {root}
        stack = [root]
        while stack:
            u = stack.pop()
            if u > BASE:
                for w in self.nodes[u][1:]:
                    if w not in seen:
                        seen.add(w)
                        stack.append(w)
        return seen

    def below(self, root: int) -> list[int]:
        """The inner nodes that root reaches, children first (ids grow upward)."""
        return sorted(u for u in self.reach(root) if u > BASE)

    def size(self, root: int) -> int:
        """The number of nodes, with the sinks that root reaches."""
        return len(self.reach(root))

    def from_family(self, family: set[frozenset[int]]) -> int:
        r = EMPTY
        for s in family:
            u = BASE
            for v in sorted(s, reverse=True):
                u = self.getnode(v, EMPTY, u)
            r = self.union(r, u)
        return r

    def to_family(self, root: int) -> set[frozenset[int]]:
        out: set[frozenset[int]] = set()
        stack: list[tuple[int, frozenset[int]]] = [(root, frozenset())]
        while stack:
            u, acc = stack.pop()
            if u == BASE:
                out.add(acc)
            elif u > BASE:
                v, lo, hi = self.nodes[u]
                stack.append((lo, acc))
                stack.append((hi, acc | {v}))
        return out

    def check_invariant(self) -> None:
        for u in range(2, len(self.nodes)):
            v, lo, hi = self.nodes[u]
            assert hi != EMPTY and self.unique[(v, lo, hi)] == u
            assert self.var(lo) > v and self.var(hi) > v
