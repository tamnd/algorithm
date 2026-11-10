# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/mapreduce-communication-lower-bounds/. The authors are listed in prov/7HM42M.jsonl.
"""One-round MapReduce algorithms (mapping schemas) that meet the lower bounds
of Afrati, Das Sarma, Salihoglu and Ullman on the replication rate r for a
reducer size q.

A schema is a dict: reducer key -> list of the inputs it receives. The input
set is all possible inputs of the problem, as in the paper.
  q = the largest reducer input,
  r = (the sum of the reducer input sizes) / (the number of inputs).
"""

import math
from itertools import combinations


def schema_stats(schema, num_inputs):
    sizes = [len(v) for v in schema.values()]
    return max(sizes, default=0), sum(sizes) / num_inputs


# ---------------------------------------------------------------- Hamming distance 1


def hamming1_splitting(b, k, inputs=None):
    """Split the b bits into k segments of b/k bits. Reducer (i, rest) gets
    every string whose bits outside segment i equal rest. Each string goes to
    k reducers; a reducer gets 2^(b/k) strings of the full input. Returns
    (the schema, the set of pairs at distance 1 that the reducers output)."""
    if k < 1 or b % k:
        raise ValueError("k must divide b")
    seg = b // k
    inputs = range(1 << b) if inputs is None else inputs
    schema = {}
    for x in inputs:
        for i in range(k):
            mask = ((1 << seg) - 1) << (i * seg)
            schema.setdefault((i, x & ~mask), []).append(x)
    found = set()
    for key, xs in schema.items():
        for x, y in combinations(sorted(xs), 2):
            if bin(x ^ y).count("1") == 1:
                found.add((x, y))
    return schema, found


def hamming1_brute(inputs):
    xs = sorted(inputs)
    return {(x, y) for x, y in combinations(xs, 2) if bin(x ^ y).count("1") == 1}


def hamming1_lower_bound(b, q):
    """Theorem 3.2 of the paper: r >= b / log2 q, for q >= 2."""
    if q < 2:
        raise ValueError("q must be at least 2")
    return b / math.log2(q)


def triangle_lower_bound(n, q):
    """The recipe with |I| = n(n-1)/2, |O| = n(n-1)(n-2)/6 and
    g(q) = (2^(1/2)/3) q^(3/2) gives r >= (n - 2) / (2q)^(1/2). The paper
    rounds |I| and |O| to n^2/2 and n^3/6 and states n / (2q)^(1/2)."""
    return (n - 2) / math.sqrt(2 * q)


def max_edges_in_subset(b, q):
    """The largest number of distance-1 pairs among q strings of b bits, by
    trying all subsets (use only for small b)."""
    edges = [(x, x | (1 << j)) for x in range(1 << b) for j in range(b) if not x >> j & 1]
    best = 0
    for s in combinations(range(1 << b), q):
        inside = set(s)
        best = max(best, sum(1 for x, y in edges if x in inside and y in inside))
    return best


# ---------------------------------------------------------------- triangles


def triangle_schema(n, k):
    """Hash vertex v to group v mod k. There is one reducer for each multiset
    of 3 groups. The edge (u, v) goes to every reducer whose multiset contains
    the multiset of the groups of u and v; that is k reducers for every edge.
    Returns the schema on all n(n-1)/2 possible edges."""
    def group(v):
        return v % k
    schema = {}
    for u, v in combinations(range(n), 2):
        a, b = sorted((group(u), group(v)))
        for c in range(k):
            key = tuple(sorted((a, b, c)))
            schema.setdefault(key, []).append((u, v))
    return schema


def triangles_from_schema(schema, k, graph_edges):
    """Run the reducers on an actual graph: each reducer keeps the edges of
    the graph that it receives, and outputs the triangles whose multiset of
    groups is its own key (so each triangle is output once)."""
    present = set(graph_edges)
    out = []
    for key, es in schema.items():
        es = [e for e in es if e in present]
        adj = {}
        for u, v in es:
            adj.setdefault(u, set()).add(v)
            adj.setdefault(v, set()).add(u)
        for u, v in es:
            for w in adj[u] & adj[v]:
                if w > v and tuple(sorted((u % k, v % k, w % k))) == key:
                    out.append((u, v, w))
    return out


def triangles_brute(n, graph_edges):
    e = set(graph_edges)
    return [(u, v, w) for u, v, w in combinations(range(n), 3)
            if (u, v) in e and (u, w) in e and (v, w) in e]


# ---------------------------------------------------------------- matrix multiplication


def matmul_schema(A, B, g):
    """Split the rows of A and the columns of B into g groups. Reducer (I, J)
    gets the rows of group I of A and the columns of group J of B, and
    computes that block of C = AB. Returns (C, the schema)."""
    n = len(A)
    rows = [[i for i in range(n) if i % g == I] for I in range(g)]
    schema = {}
    C = [[0] * n for _ in range(n)]
    for I in range(g):
        for J in range(g):
            got = [("A", i, j) for i in rows[I] for j in range(n)]
            got += [("B", i, j) for j in rows[J] for i in range(n)]
            schema[(I, J)] = got
            for i in rows[I]:
                for j in rows[J]:
                    C[i][j] = sum(A[i][t] * B[t][j] for t in range(n))
    return C, schema
