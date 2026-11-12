# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-agreement-subtree/. The authors are listed in prov/THDNB4.jsonl.

"""Maximum agreement subtree (MAST) of two rooted leaf-labeled trees.

A tree is a nested tuple. A leaf is any value that is not a tuple, for example
an int or a str, and it is the label of the leaf. An internal node is a tuple of
two or more subtrees. Labels are distinct inside one tree.

T|S is the restriction of T to the leaf set S: keep the leaves in S, delete the
others, and suppress the nodes that are left with one child. A MAST is a largest
S such that T1|S and T2|S are the same leaf-labeled rooted tree.

mast() is the dynamic program over pairs of nodes (Steel and Warnow 1993). Each
pair (u, v) combines its children by a maximum weight matching. For binary
trees the matching has two candidates, so the DP runs in O(n^2) time.
"""

from itertools import combinations
from typing import Dict, FrozenSet, Hashable, List, NamedTuple, Optional, Sequence, Set, Tuple

Tree = object


class _Flat:
    """A tree in preorder arrays. Node 0 is the root and a parent has a smaller index than its children."""

    def __init__(self, tree: Tree):
        self.kids: List[List[int]] = []
        self.label: List[Optional[Hashable]] = []
        stack: List[Tuple[Tree, int]] = [(tree, -1)]
        while stack:
            t, p = stack.pop()
            idx = len(self.kids)
            self.kids.append([])
            if p >= 0:
                self.kids[p].append(idx)
            if isinstance(t, tuple):
                if len(t) < 2:
                    raise ValueError("an internal node needs at least two children")
                self.label.append(None)
                for c in reversed(t):
                    stack.append((c, idx))
            else:
                self.label.append(t)
        n = len(self.kids)
        self.rank: Dict[Hashable, int] = {}
        for v in range(n):
            lab = self.label[v]
            if lab is not None:
                if lab in self.rank:
                    raise ValueError("duplicate leaf label %r" % (lab,))
                self.rank[lab] = len(self.rank)
        # leaves of a subtree are contiguous in preorder: [lo, hi]
        self.lo = [0] * n
        self.hi = [0] * n
        for v in range(n - 1, -1, -1):
            if self.label[v] is not None:
                self.lo[v] = self.hi[v] = self.rank[self.label[v]]
            else:
                self.lo[v] = min(self.lo[c] for c in self.kids[v])
                self.hi[v] = max(self.hi[c] for c in self.kids[v])

    def has_leaf(self, v: int, lab: Hashable) -> bool:
        r = self.rank.get(lab)
        return r is not None and self.lo[v] <= r <= self.hi[v]


def _matching(A: Sequence[int], B: Sequence[int], w) -> Tuple[int, List[Tuple[int, int]]]:
    """Maximum weight matching between the children A and B, by DP over subsets of the smaller side."""
    swap = len(B) > len(A)
    if swap:
        A, B = B, A
    nb = len(B)
    # f[mask] = best weight using a prefix of A and the B-children in mask
    best = {0: (0, ())}
    for a in A:
        new = dict(best)
        for mask, (val, pairs) in best.items():
            for j in range(nb):
                if not mask & (1 << j):
                    x = w(B[j], a) if swap else w(a, B[j])
                    if x > 0:
                        cand = (val + x, pairs + ((a, B[j]),))
                        m2 = mask | (1 << j)
                        if m2 not in new or new[m2][0] < cand[0]:
                            new[m2] = cand
        best = new
    val, pairs = max(best.values(), key=lambda t: t[0])
    if swap:
        pairs = tuple((b, a) for a, b in pairs)
    return val, list(pairs)


class MASTResult(NamedTuple):
    size: int
    leaves: FrozenSet[Hashable]
    tree: Optional[Tree]


def mast(t1: Tree, t2: Tree) -> MASTResult:
    """A maximum agreement subtree of two rooted trees.

    Time O(n^2) for binary trees on n leaves. For degree d the matching step
    costs O(d 2^d) per pair here; Steel and Warnow use a weighted bipartite
    matching instead.
    """
    F, G = _Flat(t1), _Flat(t2)
    n1, n2 = len(F.kids), len(G.kids)
    val = [[0] * n2 for _ in range(n1)]
    how: List[List[object]] = [[None] * n2 for _ in range(n1)]
    for u in range(n1 - 1, -1, -1):
        for v in range(n2 - 1, -1, -1):
            if F.label[u] is not None:
                ok = G.has_leaf(v, F.label[u])
                val[u][v] = 1 if ok else 0
                how[u][v] = ("leaf", F.label[u]) if ok else ("none",)
                continue
            if G.label[v] is not None:
                ok = F.has_leaf(u, G.label[v])
                val[u][v] = 1 if ok else 0
                how[u][v] = ("leaf", G.label[v]) if ok else ("none",)
                continue
            b, h = 0, ("none",)
            for c in F.kids[u]:  # the agreement subtree lies under one child of u
                if val[c][v] > b:
                    b, h = val[c][v], ("go", c, v)
            for c in G.kids[v]:  # the agreement subtree lies under one child of v
                if val[u][c] > b:
                    b, h = val[u][c], ("go", u, c)
            m, pairs = _matching(F.kids[u], G.kids[v], lambda x, y: val[x][y])
            if m > b and len(pairs) >= 2:  # the root of the agreement subtree maps to u and to v
                b, h = m, ("match", pairs)
            val[u][v], how[u][v] = b, h
    leaves: Set[Hashable] = set()
    stack = [(0, 0)]
    while stack:
        u, v = stack.pop()
        h = how[u][v]
        if h[0] == "leaf":
            leaves.add(h[1])
        elif h[0] == "go":
            stack.append((h[1], h[2]))
        elif h[0] == "match":
            stack.extend(h[1])
    S = frozenset(leaves)
    return MASTResult(val[0][0], S, restrict(t1, S))


def restrict(tree: Tree, S) -> Optional[Tree]:
    """T|S as a nested tuple, children in the order of T, unary nodes suppressed."""
    out: Dict[int, Optional[Tree]] = {}
    stack: List[Tuple[Tree, bool]] = [(tree, False)]
    while stack:
        t, done = stack.pop()
        if not isinstance(t, tuple):
            out[id(t), ] = t if t in S else None
            continue
        if not done:
            stack.append((t, True))
            for c in t:
                stack.append((c, False))
            continue
        parts = [out[id(c), ] for c in t]
        parts = [p for p in parts if p is not None]
        out[id(t), ] = None if not parts else parts[0] if len(parts) == 1 else tuple(parts)
    return out[id(tree), ]


def clusters(tree: Tree) -> Set[FrozenSet[Hashable]]:
    """The leaf sets of all subtrees. Two trees with the same labels are equal as rooted trees iff their clusters agree."""
    res: Set[FrozenSet[Hashable]] = set()
    memo: Dict[int, FrozenSet[Hashable]] = {}
    stack: List[Tuple[Tree, bool]] = [(tree, False)]
    while stack:
        t, done = stack.pop()
        if not isinstance(t, tuple):
            memo[id(t), ] = frozenset([t])
            res.add(memo[id(t), ])
            continue
        if not done:
            stack.append((t, True))
            for c in t:
                stack.append((c, False))
            continue
        s = frozenset().union(*(memo[id(c), ] for c in t))
        memo[id(t), ] = s
        res.add(s)
    return res


def leaves_of(tree: Tree) -> List[Hashable]:
    out = []
    stack = [tree]
    while stack:
        t = stack.pop()
        if isinstance(t, tuple):
            stack.extend(reversed(t))
        else:
            out.append(t)
    return out


def agree_on(t1: Tree, t2: Tree, S) -> bool:
    """True if T1|S and T2|S are the same rooted tree: the clusters of T|S are the nonempty sets C & S."""
    S = frozenset(S)
    a = {c & S for c in clusters(t1)} - {frozenset()}
    b = {c & S for c in clusters(t2)} - {frozenset()}
    return a == b


def brute_force_mast(t1: Tree, t2: Tree) -> int:
    """Largest |S| with T1|S = T2|S, by trying the subsets of the common labels from the largest down."""
    common = sorted(set(leaves_of(t1)) & set(leaves_of(t2)), key=repr)
    c1, c2 = clusters(t1), clusters(t2)
    for k in range(len(common), 0, -1):
        for S in combinations(common, k):
            fs = frozenset(S)
            if {c & fs for c in c1} - {frozenset()} == {c & fs for c in c2} - {frozenset()}:
                return k
    return 0
