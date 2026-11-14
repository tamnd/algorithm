# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/pc-algorithm/. The authors are listed in prov/MTZ8ME.jsonl.
"""The PC algorithm for learning the Markov equivalence class of a DAG.

A DAG is given as a dict that maps each node to the set of its parents.
The algorithm sees the distribution only through a test ci(a, b, S) that
returns True when a and b are independent given the set S. With a
d-separation oracle for a DAG G, the output is the CPDAG of G: the skeleton
of G, with an edge directed exactly when all DAGs Markov equivalent to G
direct it the same way.

The output graph is a pair (adj, arrows): adj maps each node to its set of
neighbours, and (u, v) in arrows means u -> v. An adjacent pair with no
arrow in either direction is an undirected edge.
"""

import itertools
import math
from typing import NamedTuple


class PCResult(NamedTuple):
    adj: dict        # node -> set of neighbours in the output graph
    arrows: set      # (u, v) for each directed edge u -> v
    sepset: dict     # frozenset({a, b}) -> the set S that separated a and b
    tests: int       # number of calls to the independence test


def ancestors(parents, nodes):
    """The nodes and all their ancestors."""
    seen = set(nodes)
    stack = list(nodes)
    while stack:
        v = stack.pop()
        for p in parents[v]:
            if p not in seen:
                seen.add(p)
                stack.append(p)
    return seen


def d_separated(parents, xs, ys, zs):
    """True if zs d-separates xs from ys in the DAG.

    Uses the moral graph of the ancestral set of xs, ys and zs (Lauritzen):
    zs d-separates xs and ys exactly when zs separates them there.
    """
    xs, ys, zs = set(xs), set(ys), set(zs)
    keep = ancestors(parents, xs | ys | zs)
    nb = {v: set() for v in keep}
    for v in keep:
        ps = [p for p in parents[v] if p in keep]
        for p in ps:
            nb[v].add(p)
            nb[p].add(v)
        for p, q in itertools.combinations(ps, 2):
            nb[p].add(q)
            nb[q].add(p)
    seen = set(xs - zs)
    stack = list(seen)
    while stack:
        v = stack.pop()
        if v in ys:
            return False
        for w in nb[v]:
            if w not in seen and w not in zs:
                seen.add(w)
                stack.append(w)
    return True


def dsep_oracle(parents):
    """A perfect independence test for any distribution faithful to the DAG."""
    return lambda a, b, s: d_separated(parents, {a}, {b}, s)


def is_undirected(adj, arrows, u, v):
    return v in adj[u] and (u, v) not in arrows and (v, u) not in arrows


def orient(arrows, u, v):
    arrows.add((u, v))


def meek_rules(adj, arrows):
    """Apply Meek's rules R1 to R3 until no undirected edge can be oriented."""
    changed = True
    while changed:  # @line L9
        changed = False
        for b in sorted(adj):
            for c in sorted(adj[b]):
                if not is_undirected(adj, arrows, b, c):
                    continue
                into_b = [a for a in adj[b] if (a, b) in arrows]
                # R1: a -> b - c with a and c not adjacent gives b -> c.
                r1 = any(a not in adj[c] and a != c for a in into_b)  # @line L10
                # R2: b -> a -> c with b - c gives b -> c.
                r2 = any((b, a) in arrows and (a, c) in arrows for a in adj[b])  # @line L11
                # R3: b - a1, b - a2, a1 -> c <- a2, a1 and a2 not adjacent, gives b -> c.
                cand = [a for a in adj[b] if is_undirected(adj, arrows, b, a) and (a, c) in arrows]
                r3 = any(a2 not in adj[a1] for a1, a2 in itertools.combinations(cand, 2))  # @line L12
                if r1 or r2 or r3:
                    orient(arrows, b, c)  # @line L13
                    changed = True
    return arrows


def pc(nodes, ci):
    """Run the PC algorithm with the independence test ci(a, b, S)."""
    nodes = sorted(nodes)
    adj = {v: set(nodes) - {v} for v in nodes}  # @line L1
    sepset = {}
    tests = 0
    k = 0  # @line L1
    while any(len(adj[a]) - 1 >= k for a in nodes):  # @line L2
        for a in nodes:
            for b in sorted(adj[a]):  # @line L3
                if b not in adj[a] or len(adj[a]) - 1 < k:
                    continue
                for s in itertools.combinations(sorted(adj[a] - {b}), k):  # @line L4
                    tests += 1
                    if ci(a, b, set(s)):  # @line L5
                        adj[a].discard(b)
                        adj[b].discard(a)
                        sepset[frozenset((a, b))] = set(s)  # @line L5
                        break
        k += 1  # @line L6
    arrows = set()
    for c in nodes:
        for a, b in itertools.combinations(sorted(adj[c]), 2):  # @line L7
            if b in adj[a]:
                continue
            if c not in sepset[frozenset((a, b))]:  # @line L8
                for u in (a, b):
                    if (c, u) not in arrows:
                        orient(arrows, u, c)  # @line L8
    meek_rules(adj, arrows)
    return PCResult(adj, arrows, sepset, tests)  # @line L14


def cpdag_edges(adj, arrows):
    """The output as (sorted list of directed edges, sorted list of undirected edges)."""
    directed = sorted(arrows)
    undirected = sorted((u, v) for u in adj for v in adj[u] if u < v and is_undirected(adj, arrows, u, v))
    return directed, undirected


def gaussian_ci_test(data, alpha=0.01):
    """Fisher z test of zero partial correlation for rows of real data.

    data: list of rows (lists of floats), columns are the variables 0..p-1.
    Returns ci(a, b, S) for use with pc().
    """
    n = len(data)
    p = len(data[0])
    mean = [sum(r[j] for r in data) / n for j in range(p)]
    cov = [[sum((r[i] - mean[i]) * (r[j] - mean[j]) for r in data) / (n - 1) for j in range(p)] for i in range(p)]

    def inv(m):
        q = len(m)
        a = [row[:] + [1.0 if i == j else 0.0 for j in range(q)] for i, row in enumerate(m)]
        for c in range(q):
            piv = max(range(c, q), key=lambda r: abs(a[r][c]))
            a[c], a[piv] = a[piv], a[c]
            pv = a[c][c]
            a[c] = [v / pv for v in a[c]]
            for r in range(q):
                if r != c:
                    f = a[r][c]
                    a[r] = [x - f * y for x, y in zip(a[r], a[c])]
        return [row[q:] for row in a]

    def ci(a, b, s):
        idx = [a, b] + sorted(s)
        prec = inv([[cov[i][j] for j in idx] for i in idx])
        r = -prec[0][1] / math.sqrt(prec[0][0] * prec[1][1])
        r = max(-0.9999999, min(0.9999999, r))
        z = 0.5 * math.log((1 + r) / (1 - r)) * math.sqrt(n - len(s) - 3)
        pval = math.erfc(abs(z) / math.sqrt(2))
        return pval > alpha

    return ci


if __name__ == "__main__":
    g = {"A": set(), "B": {"A"}, "C": {"A"}, "D": {"B", "C"}, "E": {"D"}}
    res = pc(g, dsep_oracle(g))
    print("tests", res.tests)
    print("sepsets", {tuple(sorted(k)): sorted(v) for k, v in res.sepset.items()})
    print("cpdag", cpdag_edges(res.adj, res.arrows))
