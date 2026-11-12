# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/d-separation/. The authors are listed in prov/WVXXR3.jsonl.

"""d-separation in a DAG by its definition, by the moral ancestral graph, and
conditional independence in a discrete Bayesian network by exact enumeration.

Nodes are 0 .. n - 1 and an edge (u, v) means u -> v. Variables are binary.
"""

import itertools
from fractions import Fraction


def descendants(n: int, edges: list[tuple[int, int]], v: int) -> set[int]:
    children = [[b for a, b in edges if a == u] for u in range(n)]
    out: set[int] = set()
    stack = [v]
    while stack:
        for c in children[stack.pop()]:
            if c not in out:
                out.add(c)
                stack.append(c)
    return out


def d_separated(n: int, edges: list[tuple[int, int]], xs: set[int], ys: set[int], zs: set[int]) -> bool:
    """The definition: no simple trail from xs to ys is active given zs."""
    es = set(edges)
    desc = [descendants(n, edges, v) for v in range(n)]
    nbr: list[set[int]] = [set() for _ in range(n)]
    for a, b in edges:
        nbr[a].add(b)
        nbr[b].add(a)
    for x in xs:
        stack = [[x]]
        while stack:
            path = stack.pop()
            v = path[-1]
            if len(path) >= 3:  # test the node before v, now that both its neighbours are known
                a, m = path[-3], path[-2]
                if (a, m) in es and (v, m) in es:   # collider at m
                    if m not in zs and not (desc[m] & zs):
                        continue
                elif m in zs:                         # chain or fork at m
                    continue
            if v in ys:
                return False
            stack.extend(path + [w] for w in nbr[v] if w not in path)
    return True


def d_separated_moral(n: int, edges: list[tuple[int, int]], xs: set[int], ys: set[int], zs: set[int]) -> bool:
    """Lauritzen's criterion: separation in the moral graph of the ancestral set."""
    parents = [[a for a, b in edges if b == v] for v in range(n)]
    anc: set[int] = set()
    stack = list(xs | ys | zs)
    while stack:
        v = stack.pop()
        if v not in anc:
            anc.add(v)
            stack.extend(parents[v])
    nbr: dict[int, set[int]] = {v: set() for v in anc}
    for v in anc:
        for p in parents[v]:
            nbr[v].add(p)
            nbr[p].add(v)
        for p, q in itertools.combinations(parents[v], 2):  # marry the parents
            nbr[p].add(q)
            nbr[q].add(p)
    seen = set(xs)
    stack = list(xs)
    while stack:
        v = stack.pop()
        if v in ys:
            return False
        for w in nbr[v]:
            if w not in seen and w not in zs:
                seen.add(w)
                stack.append(w)
    return True


def joint(n: int, edges: list[tuple[int, int]], cpt: list[dict[tuple[int, ...], Fraction]]) -> dict[tuple[int, ...], Fraction]:
    """The joint of binary variables: cpt[v][parent values] = P(X_v = 1 | parents)."""
    parents = [sorted(a for a, b in edges if b == v) for v in range(n)]
    out = {}
    for x in itertools.product((0, 1), repeat=n):
        p = Fraction(1)
        for v in range(n):
            q = cpt[v][tuple(x[u] for u in parents[v])]
            p *= q if x[v] == 1 else 1 - q
        out[x] = p
    return out


def marginal(pj: dict[tuple[int, ...], Fraction], keep: list[int]) -> dict[tuple[int, ...], Fraction]:
    out: dict[tuple[int, ...], Fraction] = {}
    for x, p in pj.items():
        key = tuple(x[v] for v in keep)
        out[key] = out.get(key, Fraction(0)) + p
    return out


def independent(pj: dict[tuple[int, ...], Fraction], xs: set[int], ys: set[int], zs: set[int]) -> bool:
    """Exact test of X independent of Y given Z: p(x,y,z) p(z) = p(x,z) p(y,z) for all values."""
    X, Y, Z = sorted(xs), sorted(ys), sorted(zs)
    pxyz = marginal(pj, X + Y + Z)
    pxz, pyz, pz = marginal(pj, X + Z), marginal(pj, Y + Z), marginal(pj, Z)
    for a in itertools.product((0, 1), repeat=len(X)):
        for b in itertools.product((0, 1), repeat=len(Y)):
            for c in itertools.product((0, 1), repeat=len(Z)):
                if pxyz.get(a + b + c, 0) * pz.get(c, 0) != pxz.get(a + c, 0) * pyz.get(b + c, 0):
                    return False
    return True
