# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/maximum-agreement-forest/. The authors are listed in prov/Q297EA.jsonl.

import random
from collections import deque

from maximum_agreement_forest import (
    RHO,
    clusters,
    is_rooted_agreement_forest,
    is_unrooted_agreement_forest,
    rooted_maf,
    rspr_from_maf,
    tbr_from_maf,
    unrooted_maf,
)

# ---------- reference: breadth-first search over tree space ----------
# A rooted tree is the frozenset of its clusters. An unrooted tree is the frozenset of its splits,
# each stored as the side without leaf 0.


def graft(inner, rest, Q):
    P = max(inner, key=len)
    return frozenset(set(inner) | {C | P if Q < C else C for C in rest} | {Q | P})


def rspr_neighbors(T):
    X = max(T, key=len)
    out = set()
    for P in T:
        if P != X:
            inner = frozenset(C for C in T if C <= P)
            rest = frozenset(C - P for C in T if not C <= P)
            out.update(graft(inner, rest, Q) for Q in rest)
    out.discard(T)
    return out


def side(S, A, ref):
    return A - S if ref in S else S


def restrict_u(U, A):
    ref = min(A)
    return frozenset(side(S & A, A, ref) for S in U if S & A and not A <= S)


def tbr_neighbors(U, X):
    out = set()
    for S in U:
        A, B = S, X - S
        VA, VB = restrict_u(U, A), restrict_u(U, B)
        if len(A) == 1:
            rootings = [frozenset([A])]
        else:
            rootings = [frozenset({A} | {s if (s <= e or s <= A - e) else A - s for s in VA} | {e, A - e}) for e in VA]
        r = min(B)
        RB = frozenset((B - s) if r in s else s for s in VB) if len(B) > 1 else None
        for RA in rootings:
            targets = [RA] if RB is None else [graft(RA, RB, Q) for Q in RB]
            for T in targets:
                out.add(frozenset(side(C, X, 0) for C in T))
    out.discard(U)
    return out


def bfs(start, nbrs):
    dist = {start: 0}
    q = deque([start])
    while q:
        x = q.popleft()
        for y in nbrs(x):
            if y not in dist:
                dist[y] = dist[x] + 1
                q.append(y)
    return dist


def all_rooted(labels):
    trees = [frozenset([frozenset([labels[0]])])]
    for x in labels[1:]:
        leaf = frozenset([frozenset([x])])
        trees = [graft(leaf, T, Q) for T in trees for Q in T]
    return trees


def to_tuple(T):
    X = max(T, key=len)
    kids = {C: [] for C in T}
    for C in T:
        if C != X:
            kids[min((D for D in T if C < D), key=len)].append(C)
    out = {}
    for C in sorted(T, key=len):
        out[C] = next(iter(C)) if len(C) == 1 else tuple(out[p] for p in sorted(kids[C], key=min))
    return out[X]


def unrooted_of(T):
    X = max(T, key=len)
    return frozenset(side(C, X, 0) for C in T if C != X)


def random_tree(labels, rng):
    parts = list(labels)
    rng.shuffle(parts)
    while len(parts) > 1:
        i, j = rng.sample(range(len(parts)), 2)
        a, b = parts[i], parts[j]
        parts = [p for k, p in enumerate(parts) if k not in (i, j)] + [(a, b)]
    return parts[0]


# ---------- tests ----------


def test_worked_example():
    t1 = (("a", ("b", "c")), "d")
    t2 = ((("a", "d"), "b"), "c")
    F = rooted_maf(t1, t2)
    assert len(F) == 3
    assert any(RHO in B for B in F)
    assert is_rooted_agreement_forest(t1, t2, F)
    assert is_rooted_agreement_forest(t1, t2, [frozenset("a"), frozenset("b"), frozenset({"c", "d", RHO})])
    # without the root leaf, {a, d} and {b, c} would be a forest of size 2; with it, the RHO piece fails
    assert not is_rooted_agreement_forest(t1, t2, [frozenset("ad"), frozenset({"b", "c", RHO})])
    assert not is_rooted_agreement_forest(t1, t2, [frozenset({"a", "d", RHO}), frozenset("bc")])
    # as unrooted trees they are equal
    assert len(unrooted_maf(t1, t2)) == 1


def test_identical_trees_need_one_component():
    rng = random.Random(1)
    for n in range(1, 9):
        t = random_tree(range(n), rng)
        assert len(rooted_maf(t, t)) == 1
        assert len(unrooted_maf(t, t)) == 1


def test_rooted_maf_matches_rspr_bfs():
    # all pairs for n <= 4, and for n = 5 every tree against one tree of each of the three shapes
    for n in range(2, 6):
        R = all_rooted(list(range(n)))
        if n <= 4:
            sources = R
        else:
            sources = [frozenset(map(frozenset, s)) for s in (
                [[0], [1], [2], [3], [4], [0, 1], [0, 1, 2], [0, 1, 2, 3], range(5)],
                [[0], [1], [2], [3], [4], [0, 1], [2, 3], [0, 1, 2, 3], range(5)],
                [[0], [1], [2], [3], [4], [0, 1], [0, 1, 2], [3, 4], range(5)],
            )]
        for a in sources:
            d = bfs(a, rspr_neighbors)
            ta = to_tuple(a)
            for b in R:
                tb = to_tuple(b)
                F = rooted_maf(ta, tb)
                assert is_rooted_agreement_forest(ta, tb, F)
                assert len(F) - 1 == d[b]


def test_unrooted_maf_matches_tbr_bfs():
    for n in range(3, 7):
        R = all_rooted(list(range(1, n)))
        X = frozenset(range(n))
        U = [unrooted_of(graft(frozenset([frozenset([0])]), T, max(T, key=len))) for T in R]
        assert len(set(U)) == len(U)
        rng = random.Random(n)
        for a in (U if n <= 5 else rng.sample(U, 2)):
            d = bfs(a, lambda V: tbr_neighbors(V, X))
            assert len(d) == len(U)
            ta = (0, to_tuple(frozenset(C for C in a) | {X - {0}}))
            for b in U:
                tb = (0, to_tuple(frozenset(C for C in b) | {X - {0}}))
                F = unrooted_maf(ta, tb)
                assert is_unrooted_agreement_forest(ta, tb, F)
                assert len(F) - 1 == d[b]


def test_tbr_below_rspr_and_symmetric():
    rng = random.Random(5)
    for _ in range(60):
        n = rng.randint(3, 8)
        t1, t2 = random_tree(range(n), rng), random_tree(range(n), rng)
        r, u = rspr_from_maf(t1, t2), tbr_from_maf(t1, t2)
        assert u <= r <= n - 2
        assert u <= max(0, n - 3)
        assert rspr_from_maf(t2, t1) == r
        assert tbr_from_maf(t2, t1) == u


def test_blocks_partition_the_leaves():
    rng = random.Random(9)
    for _ in range(30):
        n = rng.randint(2, 8)
        t1, t2 = random_tree(range(n), rng), random_tree(range(n), rng)
        F = rooted_maf(t1, t2)
        assert frozenset().union(*F) == frozenset(range(n)) | {RHO}
        assert sum(map(len, F)) == n + 1
        G = unrooted_maf(t1, t2)
        assert frozenset().union(*G) == frozenset(range(n))
        assert len(G) <= len(F)
        assert clusters(t1) and clusters(t2)
