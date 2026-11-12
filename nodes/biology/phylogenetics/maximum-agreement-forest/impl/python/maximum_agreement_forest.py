# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-agreement-forest/. The authors are listed in prov/Q297EA.jsonl.

"""Maximum agreement forests of two binary phylogenetic trees, by exhaustive search over edge cuts.

The problem is NP-hard, so this exact method is for small trees (up to about 10
leaves). It tries k = 0, 1, 2, ... and, for each set of k edges of T1, takes the
leaf sets of the components that are left. These are the blocks of a candidate
forest. The candidate is an agreement forest if T1 and T2 induce the same tree on
each block and the subtrees of T2 that span the blocks are vertex-disjoint. The
subtrees of T1 are disjoint by construction. The first k that works gives a
maximum agreement forest with k + 1 components.

Trees are nested tuples, for example (("a", "b"), ("c", "d")). A leaf is any
value that is not a tuple.

* rooted_maf uses the convention of Bordewich and Semple (2005): a new leaf RHO
  is joined above the root of both trees, and the component that holds RHO is
  one of the blocks. With it, the size minus one is the rSPR distance.
* unrooted_maf reads the trees as unrooted. Its size minus one is the TBR
  distance (Allen and Steel 2001).
"""

from itertools import combinations
from typing import Dict, FrozenSet, Hashable, List, Optional, Set, Tuple

Cluster = FrozenSet[Hashable]


class _Rho:
    """The extra root leaf. Its own type, so that it never equals a user label."""

    def __repr__(self) -> str:
        return "RHO"


RHO = _Rho()


def clusters(tree: object) -> Set[Cluster]:
    """The leaf sets of all subtrees of a nested tuple, with the singletons and the full set."""
    res: Set[Cluster] = set()
    memo: Dict[int, Cluster] = {}
    stack: List[Tuple[object, bool]] = [(tree, False)]
    while stack:
        t, done = stack.pop()
        if not isinstance(t, tuple):
            memo[id(t)] = frozenset([t])
            res.add(memo[id(t)])
        elif not done:
            stack.append((t, True))
            stack.extend((c, False) for c in t)
        else:
            s = frozenset().union(*(memo[id(c)] for c in t))
            memo[id(t)] = s
            res.add(s)
    return res


# ---------- one tree, seen from a top node ----------

class _Hung:
    """A tree hung from a top vertex. Each other vertex is named by its cluster: the leaves below it.

    Rooted case: the top is the root of T^rho, and the clusters are those of T, plus {RHO} and X | {RHO}.
    Unrooted case: the top is the leaf r, and the clusters are the sides without r of all the splits,
    plus X itself for the leaf r.
    """

    def __init__(self, nodes: Set[Cluster], top: Cluster):
        self.nodes = nodes
        self.top = top
        self.X = top

    def lca(self, L: Cluster) -> Cluster:
        return min((C for C in self.nodes if L <= C), key=len)

    def span(self, L: Cluster, top_leaf: Optional[Hashable]) -> Set[Cluster]:
        """The vertices of the smallest subtree that connects the leaves in L."""
        if top_leaf is not None and top_leaf in L:
            # every path runs up to the top leaf
            return {C for C in self.nodes if C & L}
        A = self.lca(L)
        return {C for C in self.nodes if C & L and C <= A}

    def edges(self) -> List[Cluster]:
        """The edges, each named by its lower end."""
        return sorted((C for C in self.nodes if C != self.top), key=lambda c: (len(c), sorted(map(repr, c))))

    def blocks(self, cut: Tuple[Cluster, ...]) -> List[Cluster]:
        """Leaf sets of the components after the edges in cut are deleted (empty ones are dropped)."""
        out = []
        for C in cut + (self.top,):
            below = frozenset().union(*(D for D in cut if D < C)) if cut else frozenset()
            B = C - below
            if B:
                out.append(B)
        return out


def _rooted_view(tree: object) -> Tuple[_Hung, Set[Cluster]]:
    cl = clusters(tree)
    X = max(cl, key=len)
    nodes = set(cl) | {frozenset([RHO]), X | {RHO}}
    return _Hung(nodes, X | {RHO}), cl


def _unrooted_view(tree: object, r: Hashable) -> _Hung:
    cl = clusters(tree)
    X = max(cl, key=len)
    nodes = {(X - C) if r in C else C for C in cl if C != X}
    nodes.add(X)  # the vertex of the leaf r
    nodes.discard(frozenset())
    return _Hung(nodes, X)


def _first_leaf(tree: object) -> Hashable:
    while isinstance(tree, tuple):
        tree = tree[0]
    return tree


# ---------- agreement tests ----------

def _rooted_restrict(cl: Set[Cluster], L: Cluster) -> Set[Cluster]:
    return {C & L for C in cl} - {frozenset()}


def _unrooted_restrict(cl: Set[Cluster], X: Cluster, L: Cluster) -> Set[FrozenSet[Cluster]]:
    """Nontrivial splits of T|L, each as an unordered pair of sides."""
    out = set()
    for C in cl:
        A = C & L
        B = L - A
        if len(A) >= 2 and len(B) >= 2:
            out.add(frozenset([A, B]))
    return out


def is_rooted_agreement_forest(t1: object, t2: object, blocks: List[Cluster]) -> bool:
    """Blocks partition X | {RHO}, both trees with RHO added induce the same rooted tree on each block,
    and the spanning subtrees are vertex-disjoint in both trees."""
    views = [_rooted_view(t1), _rooted_view(t2)]
    full = views[0][0].X
    if views[1][0].X != full or frozenset().union(*blocks) != full or sum(map(len, blocks)) != len(full):
        return False
    rho_cl = [cl | {frozenset([RHO]), full} for _, cl in views]
    for L in blocks:
        if _rooted_restrict(rho_cl[0], L) != _rooted_restrict(rho_cl[1], L):
            return False
    for h, _ in views:
        used: Set[Cluster] = set()
        for L in blocks:
            S = h.span(L, None)
            if used & S:
                return False
            used |= S
    return True


def is_unrooted_agreement_forest(t1: object, t2: object, blocks: List[Cluster]) -> bool:
    """Blocks partition X, both trees induce the same unrooted tree on each block,
    and the spanning subtrees are vertex-disjoint in both trees."""
    c1, c2 = clusters(t1), clusters(t2)
    X = max(c1, key=len)
    if max(c2, key=len) != X or frozenset().union(*blocks) != X or sum(map(len, blocks)) != len(X):
        return False
    for L in blocks:
        if _unrooted_restrict(c1, X, L) != _unrooted_restrict(c2, X, L):
            return False
    r = _first_leaf(t1)
    for t in (t1, t2):
        h = _unrooted_view(t, r)
        used: Set[Cluster] = set()
        for L in blocks:
            S = h.span(L, r)
            if used & S:
                return False
            used |= S
    return True


# ---------- exhaustive search ----------

def rooted_maf(t1: object, t2: object) -> List[Cluster]:
    """A maximum agreement forest of two rooted binary trees on the same leaves, with the RHO convention.
    Returns its blocks. One block holds RHO; the rSPR distance is len(result) - 1."""
    h1, c1 = _rooted_view(t1)
    h2, c2 = _rooted_view(t2)
    if h1.X != h2.X:
        raise ValueError("the trees need the same leaves")
    full = h1.X
    r1 = c1 | {frozenset([RHO]), full}
    r2 = c2 | {frozenset([RHO]), full}
    E = h1.edges()
    for k in range(len(E) + 1):
        for cut in combinations(E, k):
            blocks = h1.blocks(cut)
            if len(blocks) != k + 1:
                continue  # some component has no leaf: a smaller cut gives the same blocks
            if any(_rooted_restrict(r1, L) != _rooted_restrict(r2, L) for L in blocks):
                continue
            used: Set[Cluster] = set()
            ok = True
            for L in blocks:
                S = h2.span(L, None)
                if used & S:
                    ok = False
                    break
                used |= S
            if ok:
                return blocks
    raise AssertionError("the singletons always form an agreement forest")


def unrooted_maf(t1: object, t2: object) -> List[Cluster]:
    """A maximum agreement forest of two unrooted binary trees on the same leaves. The TBR distance is len(result) - 1."""
    c1, c2 = clusters(t1), clusters(t2)
    X = max(c1, key=len)
    if max(c2, key=len) != X:
        raise ValueError("the trees need the same leaves")
    r = _first_leaf(t1)
    h1, h2 = _unrooted_view(t1, r), _unrooted_view(t2, r)
    E = h1.edges()
    for k in range(len(E) + 1):
        for cut in combinations(E, k):
            blocks = h1.blocks(cut)
            if len(blocks) != k + 1:
                continue
            if any(_unrooted_restrict(c1, X, L) != _unrooted_restrict(c2, X, L) for L in blocks):
                continue
            used: Set[Cluster] = set()
            ok = True
            for L in blocks:
                S = h2.span(L, r)
                if used & S:
                    ok = False
                    break
                used |= S
            if ok:
                return blocks
    raise AssertionError("the singletons always form an agreement forest")


def rspr_from_maf(t1: object, t2: object) -> int:
    return len(rooted_maf(t1, t2)) - 1


def tbr_from_maf(t1: object, t2: object) -> int:
    return len(unrooted_maf(t1, t2)) - 1
