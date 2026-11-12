# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fitch-margoliash/. The authors are listed in prov/94EV9J.jsonl.

"""The Fitch-Margoliash method: weighted least squares trees from distances.

The input is a symmetric n x n distance matrix D with n >= 3 and positive
entries off the diagonal. The model is an unrooted binary tree on the n taxa
with real edge lengths; the tree gives each pair the sum of the lengths on its
path. The score of a tree is the weighted sum of squares

    Q = sum over pairs i < j of w_ij (D_ij - d_ij)^2,   w_ij = 1 / D_ij^power,

with power = 2 for Fitch and Margoliash (1967) and power = 0 for ordinary
least squares. For a fixed topology the best edge lengths solve the normal
equations (A^T W A) b = A^T W D, where A is the path-edge incidence matrix;
they are computed exactly with Fractions. Edge lengths are not constrained to
be positive. The topology is found by stepwise addition followed by
nearest-neighbor interchanges; this is a heuristic over the (2n-5)!! trees.

Trees are lists of edges (u, v). Leaves are 0 to n-1, internal nodes are n,
n+1, and so on.
"""

from fractions import Fraction
from math import gcd as _gcd


def _exact(x):
    return Fraction(x) if isinstance(x, int) else x


def _paths(leaves, edges):
    """Map each leaf pair (i, j), i < j, to the indices of the edges on its path."""
    adj = {}
    for k, (u, v) in enumerate(edges):
        adj.setdefault(u, []).append((v, k))
        adj.setdefault(v, []).append((u, k))
    out = {}
    for s in leaves:
        back = {s: None}
        stack = [s]
        while stack:
            x = stack.pop()
            for y, k in adj[x]:
                if y not in back:
                    back[y] = (x, k)
                    stack.append(y)
        for t in leaves:
            if s < t:
                path, y = [], t
                while back[y] is not None:
                    y, k = back[y]
                    path.append(k)
                out[(s, t)] = path
    return out


def _solve(M, rhs):
    """Exact solution of M x = rhs for a nonsingular rational M.

    The system is scaled to integers and reduced by fraction-free (Bareiss)
    elimination, then solved by back substitution in Fractions.
    """
    k = len(M)
    rows = [list(map(Fraction, row)) + [Fraction(rhs[i])] for i, row in enumerate(M)]
    A = []
    for row in rows:
        s = 1
        for x in row:
            s = s * x.denominator // _gcd(s, x.denominator)
        A.append([int(x * s) for x in row])
    prev = 1
    for c in range(k):
        p = next(r for r in range(c, k) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        piv, top = A[c][c], A[c]
        for r in range(c + 1, k):
            row, f = A[r], A[r][c]
            for j in range(c + 1, k + 1):
                row[j] = (row[j] * piv - f * top[j]) // prev
            row[c] = 0
        prev = piv
    x = [Fraction(0)] * k
    for i in range(k - 1, -1, -1):
        x[i] = (A[i][k] - sum(A[i][j] * x[j] for j in range(i + 1, k))) / Fraction(A[i][i])
    return x


def fit(D, edges, weights=None, power=2):
    """Least squares edge lengths for a fixed tree. Returns (lengths, Q).

    The leaves of the tree are the nodes below len(D) that occur in edges.
    """
    n = len(D)
    d = [[_exact(x) for x in row] for row in D]
    leaves = sorted({x for e in edges for x in e if x < n})
    if weights is None:
        weights = [[Fraction(1) / d[i][j] ** power if i != j else 0 for j in range(n)] for i in range(n)]
    paths = _paths(leaves, edges)
    # Scaling all weights by one constant does not move the minimizer, and
    # integer weights keep the Fractions in the elimination small.
    scale = 1
    for i, j in paths:
        q = Fraction(weights[i][j]).denominator
        scale = scale * q // _gcd(scale, q)
    k = len(edges)
    M = [[Fraction(0)] * k for _ in range(k)]
    rhs = [Fraction(0)] * k
    for (i, j), path in paths.items():
        w = weights[i][j] * scale
        for a in path:
            rhs[a] += w * d[i][j]
            row = M[a]
            for b in path:
                row[b] += w
    b = _solve(M, rhs)
    Q = Fraction(0)
    for (i, j), path in paths.items():
        r = d[i][j] - sum(b[a] for a in path)
        Q += weights[i][j] * r * r
    return b, Q


def _attach(edges, k, x, p):
    """Subdivide edge k by the new node p and hang leaf x from p."""
    u, v = edges[k]
    return edges[:k] + [(u, p), (p, v), (p, x)] + edges[k + 1:]


def _nni_neighbors(edges, n):
    adj = {}
    for u, v in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    out = []
    for u, v in edges:
        if u < n or v < n:
            continue
        a, b = [y for y in adj[u] if y != v]
        for c in [y for y in adj[v] if y != u]:
            swap = {(u, b): (u, c), (b, u): (c, u), (v, c): (v, b), (c, v): (b, v)}
            out.append([swap.get(e, e) for e in edges])
    return out


def fitch_margoliash(D, power=2):
    """Return (edges, lengths, Q) of the tree found by addition and NNI."""
    n = len(D)
    if n < 3:
        raise ValueError("need at least three taxa")
    d = [[_exact(x) for x in row] for row in D]
    if any(d[i][j] <= 0 for i in range(n) for j in range(n) if i != j):
        raise ValueError("off-diagonal distances must be positive")
    weights = [[Fraction(1) / d[i][j] ** power if i != j else 0 for j in range(n)] for i in range(n)]
    edges = [(0, n), (1, n), (2, n)]  # @line L1
    nxt = n + 1
    for x in range(3, n):  # @line L2
        best = None
        for k in range(len(edges)):  # @line L3
            cand = _attach(edges, k, x, nxt)  # @line L3
            _, Q = fit(d, cand, weights)  # @line L4
            if best is None or Q < best[0]:  # @line L5
                best = (Q, cand)  # @line L5
        edges = best[1]
        nxt += 1
    lengths, Q = fit(d, edges, weights)
    while True:  # @line L6
        better = None
        for cand in _nni_neighbors(edges, n):  # @line L7
            b2, Q2 = fit(d, cand, weights)  # @line L7
            if Q2 < Q and (better is None or Q2 < better[0]):  # @line L8
                better = (Q2, cand, b2)  # @line L8
        if better is None:  # @line L9
            break  # @line L9
        Q, edges, lengths = better  # @line L8
    return edges, lengths, Q  # @line L10
