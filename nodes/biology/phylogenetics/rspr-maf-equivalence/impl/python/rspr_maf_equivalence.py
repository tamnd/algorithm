# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/rspr-maf-equivalence/. The authors are listed in prov/J6TD60.jsonl.

"""Both directions of the proof that d_rSPR(T1, T2) = m(T1^rho, T2^rho) - 1, as code.

A rooted binary tree on the leaf set X is the frozenset of its clusters, with
the singletons and X. T^rho adds the leaf RHO above the root, so its clusters
are those of T plus {RHO} and X | {RHO}. A rooted agreement forest is a list of
blocks that partition X | {RHO}.

* forest_to_moves follows the proof that d <= m - 1. It takes an agreement
  forest with m blocks and returns m - 1 rSPR moves that turn T1 into T2.
* move_to_forest follows the proof that m - 1 <= d. Given one move T1 -> T1'
  and an agreement forest of T1' and T2, it returns one for T1 and T2 with at
  most one more block.
* rspr_distance (breadth-first search) and maf_size (exhaustive search over
  cuts) compute the two sides of the equality for small trees.
"""

from collections import deque
from itertools import combinations
from typing import Dict, FrozenSet, Hashable, List, Optional, Set, Tuple

Cluster = FrozenSet[Hashable]
Tree = FrozenSet[Cluster]


class _Rho:
    def __repr__(self) -> str:
        return "RHO"


RHO = _Rho()


# ---------- cluster algebra ----------

def leaves(T: Tree) -> Cluster:
    return max(T, key=len)


def with_rho(T: Tree) -> Tree:
    return T | {frozenset([RHO]), leaves(T) | {RHO}}


def restrict(T: Tree, L: Cluster) -> Tree:
    """T|L: the nonempty sets C & L."""
    return frozenset(C & L for C in T) - {frozenset()}


def lca(T: Tree, L: Cluster) -> Cluster:
    return min((C for C in T if L <= C), key=len)


def span(T: Tree, L: Cluster) -> Set[Cluster]:
    """Vertices of the smallest subtree of T that connects the leaves in L."""
    top = lca(T, L)
    return {C for C in T if C & L and C <= top}


def prune(T: Tree, P: Cluster) -> Tuple[Tree, Tree]:
    inner = frozenset(C for C in T if C <= P)
    rest = frozenset(C - P for C in T if not C <= P)
    return inner, rest


def graft(inner: Tree, rest: Tree, Q: Cluster) -> Tree:
    """Join the tree inner on the edge above node Q of rest (above the root if Q is the root)."""
    P = leaves(inner)
    return frozenset(set(inner) | {C | P if Q < C else C for C in rest} | {Q | P})


def spr(T: Tree, P: Cluster, Q: Cluster) -> Tree:
    """The rSPR move that prunes the subtree with cluster P and regrafts it above node Q of the rest."""
    if P == leaves(T) or P not in T:
        raise ValueError("P must be a cluster below the root")
    inner, rest = prune(T, P)
    if Q not in rest:
        raise ValueError("Q must be a node of the pruned tree")
    return graft(inner, rest, Q)


def rspr_neighbors(T: Tree) -> Set[Tree]:
    X = leaves(T)
    out: Set[Tree] = set()
    for P in T:
        if P != X:
            inner, rest = prune(T, P)
            out.update(graft(inner, rest, Q) for Q in rest)
    out.discard(T)
    return out


def bfs_parents(T1: Tree, T2: Optional[Tree] = None) -> Dict[Tree, Optional[Tree]]:
    """Breadth-first search from T1 over rSPR moves. Stops early when T2 is reached."""
    parent: Dict[Tree, Optional[Tree]] = {T1: None}
    q = deque([T1])
    while q:
        x = q.popleft()
        if x == T2:
            break
        for y in rspr_neighbors(x):
            if y not in parent:
                parent[y] = x
                q.append(y)
    return parent


def rspr_distance(T1: Tree, T2: Tree, parent: Optional[Dict[Tree, Optional[Tree]]] = None) -> Tuple[int, List[Tree]]:
    """The distance and a shortest path T1, ..., T2. A search tree from T1 may be passed in."""
    if parent is None:
        parent = bfs_parents(T1, T2)
    path = [T2]
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    path.reverse()
    return len(path) - 1, path


# ---------- agreement forests ----------

def is_agreement_forest(T1: Tree, T2: Tree, F: List[Cluster]) -> bool:
    A, B = with_rho(T1), with_rho(T2)
    full = leaves(A)
    if leaves(B) != full or frozenset().union(*F) != full or sum(map(len, F)) != len(full):
        return False
    if any(restrict(A, L) != restrict(B, L) for L in F):
        return False
    for T in (A, B):
        used: Set[Cluster] = set()
        for L in F:
            S = span(T, L)
            if used & S:
                return False
            used |= S
    return True


def maf_size(T1: Tree, T2: Tree) -> Tuple[int, List[Cluster]]:
    """Exhaustive search: delete k = 0, 1, ... edges of T1^rho and test the pieces."""
    A, B = with_rho(T1), with_rho(T2)
    top = leaves(A)
    edges = sorted((C for C in A if C != top), key=lambda c: (len(c), sorted(map(repr, c))))
    for k in range(len(edges) + 1):
        for cut in combinations(edges, k):
            F = []
            for C in cut + (top,):
                below = frozenset().union(*(D for D in cut if D < C))
                if C - below:
                    F.append(C - below)
            if len(F) == k + 1 and is_agreement_forest(T1, T2, F):
                return k + 1, F
    raise AssertionError("unreachable: the singletons form an agreement forest")


# ---------- the proof of d <= m - 1 ----------

def forest_to_moves(T1: Tree, T2: Tree, F: List[Cluster]) -> List[Tuple[Cluster, Cluster]]:
    """Turn an agreement forest with m blocks into m - 1 rSPR moves (P, Q) from T1 to T2.

    Each step takes a block L_j that is a cluster of T1. In T2^rho it walks up from
    the root of T2(L_j) to the first vertex w on another piece T2(L_h). The move
    regrafts L_j in T1 at the matching place of T1(L_h), and the two blocks merge.
    """
    if not is_agreement_forest(T1, T2, F):
        raise ValueError("not an agreement forest")
    F = list(F)
    T = T1
    moves: List[Tuple[Cluster, Cluster]] = []
    B = with_rho(T2)
    while len(F) > 1:
        # a block other than the RHO block whose leaf set is a cluster of T (the deepest one always is)
        j = next(i for i, L in enumerate(F) if RHO not in L and L in T)
        Lj = F[j]
        spans = {i: span(B, L) for i, L in enumerate(F) if i != j}
        v = lca(B, Lj)
        h, w = None, None
        for C in sorted((C for C in B if v < C), key=len):  # ancestors of v, upward
            h = next((i for i, S in spans.items() if C in S), None)
            if h is not None:
                w = C
                break
        if h is None:  # the path went over the root of T2^rho down to RHO, and the RHO block is {RHO}
            h = next(i for i, L in enumerate(F) if RHO in L)
            w = frozenset([RHO])
        Lh = F[h]
        inner, rest = prune(T, Lj)
        A = w & Lh - {RHO}
        Q = leaves(rest) if not A else lca(rest, A)
        moves.append((Lj, Q))
        T = graft(inner, rest, Q)
        F = [L for i, L in enumerate(F) if i not in (j, h)] + [Lh | Lj]
        assert is_agreement_forest(T, T2, F)
    assert T == T2
    return moves


# ---------- the proof of m - 1 <= d ----------

def move_to_forest(T1: Tree, P: Cluster, Q: Cluster, F2: List[Cluster]) -> List[Cluster]:
    """T1' = spr(T1, P, Q). From an agreement forest F2 of T1' and T2, build one of T1 and T2.

    The pruned edge of T1' lies on at most one piece, so splitting that block by P
    adds at most one block."""
    out: List[Cluster] = []
    split = 0
    for L in F2:
        a, b = L & P, L - P
        if a and b:
            split += 1
            out.extend([a, b])
        else:
            out.append(L)
    assert split <= 1
    return out


def moves_of_path(path: List[Tree]) -> List[Tuple[Cluster, Cluster]]:
    """Recover (P, Q) for each step of a path of rSPR moves."""
    out = []
    for S, T in zip(path, path[1:]):
        X = leaves(S)
        found = None
        for P in S:
            if P == X or P not in T:
                continue
            inner, rest = prune(S, P)
            for Q in rest:
                if graft(inner, rest, Q) == T:
                    found = (P, Q)
                    break
            if found:
                break
        if found is None:
            raise ValueError("not one rSPR move")
        out.append(found)
    return out


def forest_from_path(path: List[Tree]) -> List[Cluster]:
    """Walk a move path backward from T2, where {X | RHO} is a forest, splitting one block per move."""
    F = [leaves(path[-1]) | {RHO}]
    for (P, Q), S in reversed(list(zip(moves_of_path(path), path))):
        F = move_to_forest(S, P, Q, F)
    return F


# ---------- enumeration ----------

def all_rooted(labels: List[Hashable]) -> List[Tree]:
    trees = [frozenset([frozenset([labels[0]])])]
    for x in labels[1:]:
        leaf = frozenset([frozenset([x])])
        trees = [graft(leaf, T, Q) for T in trees for Q in T]
    return trees


def from_tuple(t: object) -> Tree:
    out: Set[Cluster] = set()
    memo: Dict[int, Cluster] = {}
    stack: List[Tuple[object, bool]] = [(t, False)]
    while stack:
        s, done = stack.pop()
        if not isinstance(s, tuple):
            memo[id(s)] = frozenset([s])
            out.add(memo[id(s)])
        elif not done:
            stack.append((s, True))
            stack.extend((c, False) for c in s)
        else:
            memo[id(s)] = frozenset().union(*(memo[id(c)] for c in s))
            out.add(memo[id(s)])
    return frozenset(out)
