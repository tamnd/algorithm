# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/markov-property/. The authors are listed in prov/2VPWEJ.jsonl.

"""The pairwise, local and global Markov properties of an undirected graph,
and the local directed Markov property and factorization for a DAG, checked
exactly on a joint distribution of binary variables.

A joint is a dict from 0/1 tuples to Fractions; missing keys have probability 0.
An undirected graph is a list of neighbour sets. A DAG is a list of edges (u, v), u -> v.
"""

import itertools
from fractions import Fraction

Joint = dict[tuple[int, ...], Fraction]


def marginal(pj: Joint, keep: list[int]) -> Joint:
    out: Joint = {}
    for x, p in pj.items():
        key = tuple(x[i] for i in keep)
        out[key] = out.get(key, Fraction(0)) + p
    return out


def independent(pj: Joint, xs, ys, zs) -> bool:
    """Exact test of X independent of Y given Z."""
    X, Y, Z = sorted(xs), sorted(ys), sorted(zs)
    pxyz, pxz, pyz, pz = marginal(pj, X + Y + Z), marginal(pj, X + Z), marginal(pj, Y + Z), marginal(pj, Z)
    for a in itertools.product((0, 1), repeat=len(X)):
        for b in itertools.product((0, 1), repeat=len(Y)):
            for c in pz:
                if pxyz.get(a + b + c, 0) * pz[c] != pxz.get(a + c, 0) * pyz.get(b + c, 0):
                    return False
    return True


def separated(adj: list[set[int]], A: set[int], B: set[int], S: set[int]) -> bool:
    """True if every path from A to B in the graph meets S."""
    seen, stack = set(A), list(A)
    while stack:
        v = stack.pop()
        if v in B:
            return False
        for w in adj[v]:
            if w not in seen and w not in S:
                seen.add(w)
                stack.append(w)
    return True


def pairwise(pj: Joint, n: int, adj: list[set[int]]) -> bool:
    """(P): u and v are independent given all the others when they are not adjacent."""
    return all(independent(pj, {u}, {v}, set(range(n)) - {u, v})
               for u, v in itertools.combinations(range(n), 2) if v not in adj[u])


def local(pj: Joint, n: int, adj: list[set[int]]) -> bool:
    """(L): v is independent of its non-neighbours given its neighbours."""
    for v in range(n):
        rest = set(range(n)) - adj[v] - {v}
        if rest and not independent(pj, {v}, rest, adj[v]):
            return False
    return True


def global_(pj: Joint, n: int, adj: list[set[int]]) -> bool:
    """(G): A and B are independent given S whenever S separates A from B."""
    for lab in itertools.product(range(4), repeat=n):
        A = {v for v in range(n) if lab[v] == 0}
        B = {v for v in range(n) if lab[v] == 1}
        S = {v for v in range(n) if lab[v] == 2}
        if A and B and min(A) < min(B) and separated(adj, A, B, S):
            if not independent(pj, A, B, S):
                return False
    return True


def parents_of(n: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    return [sorted(a for a, b in edges if b == v) for v in range(n)]


def descendants(n: int, edges: list[tuple[int, int]], v: int) -> set[int]:
    out, stack = set(), [v]
    while stack:
        u = stack.pop()
        for a, b in edges:
            if a == u and b not in out:
                out.add(b)
                stack.append(b)
    return out


def local_directed(pj: Joint, n: int, edges: list[tuple[int, int]]) -> bool:
    """(DL): v is independent of its non-descendants given its parents."""
    pa = parents_of(n, edges)
    for v in range(n):
        nd = set(range(n)) - descendants(n, edges, v) - {v} - set(pa[v])
        if nd and not independent(pj, {v}, nd, set(pa[v])):
            return False
    return True


def factorizes(pj: Joint, n: int, edges: list[tuple[int, int]]) -> bool:
    """(DF): P(x) equals the product of P(x_v | x_pa(v)) computed from P itself."""
    pa = parents_of(n, edges)
    fam = [marginal(pj, [v] + pa[v]) for v in range(n)]
    par = [marginal(pj, pa[v]) for v in range(n)]
    for x in itertools.product((0, 1), repeat=n):
        q = Fraction(1)
        for v in range(n):
            den = par[v].get(tuple(x[u] for u in pa[v]), 0)
            if den == 0:
                q = Fraction(0)
                break
            q *= fam[v].get((x[v],) + tuple(x[u] for u in pa[v]), 0) / den
        if q != pj.get(x, 0):
            return False
    return True
