# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/spr-distance/. The authors are listed in prov/B2M14X.jsonl.

"""Exact rSPR, uSPR and TBR distances by breadth-first search over tree space.

This is a reference method for small trees (up to about 7 leaves), not a fast
algorithm: the three distance problems are NP-hard.

Trees are kept in a canonical form, so that equal trees compare equal.

* A rooted binary tree on the leaf set X is the frozenset of its clusters (the
  leaf sets of its subtrees), with the singletons and X itself.
* An unrooted binary tree on X is the frozenset of its splits, with the trivial
  ones. A split A | X - A is stored as the side that does not contain the
  reference leaf min(X).

Every move is set algebra on these forms. Pruning the subtree with cluster P
from a rooted tree leaves the clusters C - P of the other nodes. Regrafting P
on the edge above the node with cluster Q adds P to every cluster that
contains Q, and adds the new cluster Q | P.
"""

from collections import deque
from typing import Callable, Dict, FrozenSet, Hashable, Iterable, List, Set, Tuple

Cluster = FrozenSet[Hashable]
Rooted = FrozenSet[Cluster]
Unrooted = FrozenSet[Cluster]


# ---------- conversions ----------

def rooted_key(tree: object) -> Rooted:
    """Clusters of a nested-tuple rooted binary tree, such as ((1, 2), 3)."""
    out: Set[Cluster] = set()
    memo: Dict[int, Cluster] = {}
    stack: List[Tuple[object, bool]] = [(tree, False)]
    while stack:
        t, done = stack.pop()
        if not isinstance(t, tuple):
            memo[id(t)] = frozenset([t])
            out.add(memo[id(t)])
        elif not done:
            if len(t) != 2:
                raise ValueError("binary trees only")
            stack.append((t, True))
            stack.extend((c, False) for c in t)
        else:
            s = memo[id(t[0])] | memo[id(t[1])]
            memo[id(t)] = s
            out.add(s)
    return frozenset(out)


def leaves(key: Rooted) -> Cluster:
    """The leaf set of a rooted key: its largest cluster."""
    return max(key, key=len)


def _side(S: Cluster, X: Cluster, ref: Hashable) -> Cluster:
    return X - S if ref in S else S


def root_at(U: Unrooted, X: Cluster, r: Hashable) -> Rooted:
    """Root the unrooted tree U at leaf r and delete r: a rooted tree on X - {r}.
    Each split gives the side without r as a cluster."""
    return frozenset((X - S) if r in S else S for S in U)


def unroot(R: Rooted, X: Cluster, r: Hashable) -> Unrooted:
    """Inverse of root_at: attach leaf r above the root of R, a rooted tree on X - {r}."""
    ref = min(X)
    return frozenset(_side(C, X, ref) for C in R)


def unrooted_key(tree: object) -> Unrooted:
    """Splits of a nested tuple read as an unrooted tree (the root of degree 2 is suppressed)."""
    R = rooted_key(tree)
    X = leaves(R)
    ref = min(X)
    out = {_side(C, X, ref) for C in R if C != X}
    return frozenset(out)


# ---------- rooted SPR ----------

def prune(T: Rooted, P: Cluster) -> Tuple[Rooted, Rooted]:
    """Cut the edge above cluster P. Returns the subtree on P and the rest on X - P, with its unary node suppressed."""
    inner = frozenset(C for C in T if C <= P)
    rest = frozenset(C - P for C in T if not C <= P)
    return inner, rest


def graft(inner: Rooted, rest: Rooted, Q: Cluster) -> Rooted:
    """Attach the rooted tree inner (on P) on the edge above node Q of rest. Q may be the root of rest."""
    P = leaves(inner)
    out = set(inner)
    for C in rest:
        out.add(C | P if Q < C else C)
    out.add(Q | P)
    return frozenset(out)


def rspr_neighbors(T: Rooted) -> Set[Rooted]:
    """All trees one rSPR move away. Any non-root edge may be cut, and the subtree below it
    may be regrafted on any edge of the rest or above the root of the rest."""
    X = leaves(T)
    out: Set[Rooted] = set()
    for P in T:
        if P == X:
            continue
        inner, rest = prune(T, P)
        for Q in rest:
            out.add(graft(inner, rest, Q))
    out.discard(T)
    return out


# ---------- unrooted SPR and TBR ----------

def uspr_neighbors(U: Unrooted, X: Cluster) -> Set[Unrooted]:
    """All trees one uSPR move away: cut an edge, keep one side attached at the cut end,
    and regraft it on an edge of the other side.

    Rooting at a leaf r on the side that stays turns this into an rSPR move whose
    regraft above the root means the edge next to r. Every move has such an r."""
    out: Set[Unrooted] = set()
    for r in X:
        R = root_at(U, X, r)
        for T2 in rspr_neighbors(R):
            out.add(unroot(T2, X, r))
    out.discard(U)
    return out


def restrict_unrooted(U: Unrooted, X: Cluster, A: Cluster) -> Unrooted:
    """U|A, stored by the side without min(A)."""
    ref = min(A)
    out = set()
    for S in U:
        P = S & A
        if P and P != A:
            out.add(_side(P, A, ref))
    return frozenset(out)


def rootings(V: Unrooted, A: Cluster) -> List[Rooted]:
    """All rooted trees on A that put a root on an edge of the unrooted tree V on A."""
    if len(A) == 1:
        return [frozenset([A])]
    out = []
    for e in V:
        S, T = e, A - e
        cl = {A, S, T}
        for s in V:
            side = s if (s <= S or s <= T) else A - s
            cl.add(side)
        out.append(frozenset(cl))
    return out


def tbr_neighbors(U: Unrooted, X: Cluster) -> Set[Unrooted]:
    """All trees one TBR move away: cut an edge, then join any edge of one side (or the leaf,
    if the side is one leaf) to any edge of the other side by a new edge."""
    out: Set[Unrooted] = set()
    for S in U:
        A, B = S, X - S
        VA = restrict_unrooted(U, X, A)
        VB = restrict_unrooted(U, X, B)
        r = min(B)
        RB = root_at(VB, B, r) if len(B) > 1 else frozenset()
        for RA in rootings(VA, A):
            if not RB:
                out.add(unroot(RA, X, r))
                continue
            for Q in RB:
                out.add(unroot(graft(RA, RB, Q), X, r))
    out.discard(U)
    return out


# ---------- distances ----------

def bfs(start, neighbors: Callable[[object], Iterable[object]], goal=None) -> Dict[object, int]:
    """Breadth-first search in tree space. Stops when goal is dequeued."""
    dist = {start: 0}
    q = deque([start])
    while q:
        x = q.popleft()
        if x == goal:
            break
        for y in neighbors(x):
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def rspr_distance(t1: object, t2: object) -> int:
    a, b = rooted_key(t1), rooted_key(t2)
    if leaves(a) != leaves(b):
        raise ValueError("the trees need the same leaves")
    return bfs(a, rspr_neighbors, b)[b]


def uspr_distance(t1: object, t2: object) -> int:
    X = leaves(rooted_key(t1))
    a, b = unrooted_key(t1), unrooted_key(t2)
    return bfs(a, lambda U: uspr_neighbors(U, X), b)[b]


def tbr_distance(t1: object, t2: object) -> int:
    X = leaves(rooted_key(t1))
    a, b = unrooted_key(t1), unrooted_key(t2)
    return bfs(a, lambda U: tbr_neighbors(U, X), b)[b]


# ---------- enumeration and printing ----------

def all_rooted(X: Iterable[Hashable]) -> List[Rooted]:
    """All (2n - 3)!! rooted binary trees on X, by adding the leaves one at a time on every edge."""
    labels = sorted(X)
    trees = [frozenset([frozenset([labels[0]])])]
    for x in labels[1:]:
        leaf = frozenset([frozenset([x])])
        trees = [graft(leaf, T, Q) for T in trees for Q in T]
    return trees


def all_unrooted(X: Iterable[Hashable]) -> List[Unrooted]:
    """All (2n - 5)!! unrooted binary trees on X, n >= 3: rooted trees on X - {min X} with min X joined at the root."""
    labels = sorted(X)
    Xs = frozenset(labels)
    return [unroot(R, Xs, labels[0]) for R in all_rooted(labels[1:])]


def to_newick(T: Rooted) -> str:
    """Nested parentheses for a rooted key, children ordered by their smallest label."""
    X = leaves(T)
    kids: Dict[Cluster, List[Cluster]] = {C: [] for C in T}
    for C in T:
        if C != X:
            kids[min((D for D in T if C < D), key=len)].append(C)
    out: Dict[Cluster, str] = {}
    for C in sorted(T, key=len):
        if len(C) == 1:
            out[C] = str(next(iter(C)))
        else:
            out[C] = "(" + ",".join(out[p] for p in sorted(kids[C], key=min)) + ")"
    return out[X]
