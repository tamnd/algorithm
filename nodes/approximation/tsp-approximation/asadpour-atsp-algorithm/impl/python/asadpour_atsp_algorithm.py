# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/asadpour-atsp-algorithm/. The authors are listed in prov/7DRJZ2.jsonl.

"""The thin tree algorithm of Asadpour, Goemans, Madry, Oveis Gharan and Saberi for ATSP.

This code is for small instances only (n at most about 7). It solves the
ATSP LP exactly with fractions, separates cuts by trying all subsets, and
represents the max entropy distribution by listing all spanning trees of
the support. A real implementation uses min cuts, the matrix-tree theorem
and a convex solver, and runs in polynomial time.
"""

import itertools
import math
import random
from fractions import Fraction
from typing import Sequence

Arc = tuple[int, int]
Edge = tuple[int, int]


def simplex_min(cost: Sequence[Fraction], rows: Sequence[Sequence[Fraction]], senses: Sequence[str],
                rhs: Sequence[Fraction]) -> tuple[Fraction, list[Fraction]]:
    """Minimize cost.x subject to rows (senses '=', '>=' or '<=') rhs and x >= 0.

    Exact two-phase simplex with Bland's rule. Precondition: the LP is feasible
    and bounded. Cost: exponential in the worst case, fast for tiny LPs.
    """
    nv = len(cost)
    slack = sum(1 for s in senses if s != "=")
    a: list[list[Fraction]] = []
    b: list[Fraction] = []
    k = nv
    for row, sense, value in zip(rows, senses, rhs):
        r = [Fraction(v) for v in row] + [Fraction(0)] * slack
        if sense != "=":
            r[k] = Fraction(-1 if sense == ">=" else 1)
            k += 1
        v = Fraction(value)
        if v < 0:
            r, v = [-t for t in r], -v
        a.append(r)
        b.append(v)
    m = len(a)
    ncol = nv + slack
    for i in range(m):
        a[i] += [Fraction(1 if j == i else 0) for j in range(m)]
    total = ncol + m
    basis = [ncol + i for i in range(m)]
    allowed = [True] * total

    def pivot(r: int, e: int) -> None:
        p = a[r][e]
        a[r] = [t / p for t in a[r]]
        b[r] /= p
        for i in range(len(a)):
            if i != r and a[i][e] != 0:
                f = a[i][e]
                a[i] = [s - f * t for s, t in zip(a[i], a[r])]
                b[i] -= f * b[r]
        basis[r] = e

    def run(c: list[Fraction]) -> None:
        while True:
            d = [c[j] - sum(c[basis[i]] * a[i][j] for i in range(len(a))) for j in range(total)]
            e = next((j for j in range(total) if allowed[j] and d[j] < 0), None)
            if e is None:
                return
            r = None
            for i in range(len(a)):
                if a[i][e] > 0:
                    q = b[i] / a[i][e]
                    if r is None or q < b[r] / a[r][e] or (q == b[r] / a[r][e] and basis[i] < basis[r]):
                        r = i
            if r is None:
                raise ValueError("unbounded LP")
            pivot(r, e)

    run([Fraction(0)] * ncol + [Fraction(1)] * m)
    if any(basis[i] >= ncol and b[i] != 0 for i in range(len(a))):
        raise ValueError("infeasible LP")
    i = 0
    while i < len(a):
        if basis[i] >= ncol:
            j = next((j for j in range(ncol) if a[i][j] != 0), None)
            if j is None:
                del a[i], b[i], basis[i]
                continue
            pivot(i, j)
        i += 1
    for j in range(ncol, total):
        allowed[j] = False
    c2 = [Fraction(t) for t in cost] + [Fraction(0)] * (total - nv)
    run(c2)
    x = [Fraction(0)] * total
    for i, j in enumerate(basis):
        x[j] = b[i]
    return sum(c2[j] * x[j] for j in range(total)), x[:nv]


def atsp_lp(cost: Sequence[Sequence[float]]) -> tuple[Fraction, dict[Arc, Fraction]]:
    """Solve the ATSP LP (the Held-Karp relaxation) exactly by cutting planes.

    x(out(v)) = x(in(v)) = 1 for each v, x(out(U)) >= 1 for each U, x >= 0.
    Return LP* and the nonzero x. Precondition: n >= 2. Separation tries all
    2^n - 2 sets U, so the cost is exponential in n.
    """
    n = len(cost)
    arcs = [(i, j) for i in range(n) for j in range(n) if i != j]
    rows: list[list[Fraction]] = []
    for v in range(n):
        rows.append([Fraction(int(a[0] == v)) for a in arcs])
        rows.append([Fraction(int(a[1] == v)) for a in arcs])
    senses = ["="] * (2 * n)
    rhs = [Fraction(1)] * (2 * n)
    while True:
        value, x = simplex_min([Fraction(cost[i][j]) for i, j in arcs], rows, senses, rhs)
        worst = None
        for mask in range(1, (1 << n) - 1):
            row = [Fraction(int(mask >> i & 1 == 1 and mask >> j & 1 == 0)) for i, j in arcs]
            s = sum(r * t for r, t in zip(row, x))
            if s < 1 and (worst is None or s < worst[0]):
                worst = (s, row)
        if worst is None:
            return value, {a: t for a, t in zip(arcs, x) if t != 0}
        rows.append(worst[1])
        senses.append(">=")
        rhs.append(Fraction(1))


def spanning_trees(n: int, edges: Sequence[Edge]) -> list[tuple[int, ...]]:
    """List all spanning trees of (range(n), edges) as tuples of edge indices.

    Cost: C(m, n - 1) union-find checks for m edges, so small graphs only.
    """
    out = []
    for comb in itertools.combinations(range(len(edges)), n - 1):
        parent = list(range(n))
        ok = True
        for k in comb:
            u, v = edges[k]
            while parent[u] != u:
                u = parent[u]
            while parent[v] != v:
                v = parent[v]
            if u == v:
                ok = False
                break
            parent[u] = v
        if ok:
            out.append(comb)
    return out


def tree_probabilities(trees: Sequence[tuple[int, ...]], gamma: Sequence[float]) -> list[float]:
    """Pr[T] proportional to exp(sum of gamma_e over e in T)."""
    scores = [sum(gamma[k] for k in t) for t in trees]
    top = max(scores)
    w = [math.exp(s - top) for s in scores]
    total = sum(w)
    return [v / total for v in w]


def marginals(trees: Sequence[tuple[int, ...]], probs: Sequence[float], m: int) -> list[float]:
    p = [0.0] * m
    for t, q in zip(trees, probs):
        for k in t:
            p[k] += q
    return p


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Gaussian elimination with partial pivoting, O(m^3)."""
    m = len(b)
    rows = [a[i][:] + [b[i]] for i in range(m)]
    for col in range(m):
        piv = max(range(col, m), key=lambda r: abs(rows[r][col]))
        rows[col], rows[piv] = rows[piv], rows[col]
        p = rows[col][col]
        for r in range(m):
            if r != col and rows[r][col] != 0:
                f = rows[r][col] / p
                rows[r] = [x - f * y for x, y in zip(rows[r], rows[col])]
    return [rows[i][m] / rows[i][i] for i in range(m)]


def max_entropy_gamma(trees: Sequence[tuple[int, ...]], z: Sequence[float], tol: float = 1e-12,
                      max_iter: int = 200) -> list[float]:
    """Find gamma with Pr_gamma[e in T] = z_e by Newton's method on the convex dual
    log(sum_T exp(gamma(T))) - gamma.z. lambda_e = exp(gamma_e).

    Precondition: z is in the relative interior of the spanning tree polytope of
    the support. Cost per step: O(#trees * m^2 + m^3).
    """
    m = len(z)
    gamma = [0.0] * m

    def dual(g: list[float]) -> float:
        scores = [sum(g[k] for k in t) for t in trees]
        top = max(scores)
        return top + math.log(sum(math.exp(s - top) for s in scores)) - sum(a * b for a, b in zip(g, z))

    for _ in range(max_iter):
        probs = tree_probabilities(trees, gamma)
        p = marginals(trees, probs, m)
        grad = [p[e] - z[e] for e in range(m)]
        if max(abs(g) for g in grad) < tol:
            return gamma
        hess = [[-p[e] * p[f] for f in range(m)] for e in range(m)]
        for t, q in zip(trees, probs):
            for e in t:
                row = hess[e]
                for f in t:
                    row[f] += q
        for e in range(m):
            hess[e][e] += 1e-9
        step = solve_linear(hess, [-g for g in grad])
        f0 = dual(gamma)
        slope = sum(g * s for g, s in zip(grad, step))
        t = 1.0
        while t > 1e-12:
            trial = [g + t * s for g, s in zip(gamma, step)]
            if dual(trial) <= f0 + 1e-4 * t * slope:
                break
            t /= 2
        gamma = trial
    raise ArithmeticError("max entropy fit did not converge")


def max_entropy_distribution(cost: Sequence[Sequence[float]]):
    """Lines L1 to L3. Return (LP*, x, edges, z, trees, probs)."""
    n = len(cost)
    value, x = atsp_lp(cost)                                              # @line L1
    edges = sorted({(min(u, v), max(u, v)) for u, v in x})
    z = [(x.get((u, v), Fraction(0)) + x.get((v, u), Fraction(0))) * (n - 1) / n
         for u, v in edges]                                               # @line L2
    trees = spanning_trees(n, edges)
    gamma = max_entropy_gamma(trees, [float(t) for t in z])               # @line L3
    probs = tree_probabilities(trees, gamma)
    return value, x, edges, z, trees, probs


def edge_cost(cost: Sequence[Sequence[float]], e: Edge) -> float:
    """An undirected edge costs the cheaper of its two arcs."""
    u, v = e
    return min(cost[u][v], cost[v][u])


def balance_arcs(cost: Sequence[Sequence[float]], arcs: Sequence[Arc]) -> list[Arc]:
    """Least cost multiset of extra arcs that makes in-degree equal out-degree.

    With the directed triangle inequality this is the least cost circulation
    with flow at least 1 on each given arc: a vertex with more in-arcs than
    out-arcs sends one unit for each missing out-arc to a vertex with the
    opposite surplus, and a unit costs the direct arc. The transport problem
    is solved exactly by a DP over subsets of the k receiving units, O(k 2^k).
    """
    n = len(cost)
    bal = [0] * n
    for u, v in arcs:
        bal[u] -= 1
        bal[v] += 1
    senders = [v for v in range(n) for _ in range(max(bal[v], 0))]
    takers = [v for v in range(n) for _ in range(max(-bal[v], 0))]
    k = len(senders)
    best: list[tuple[float, list[Arc]] | None] = [None] * (1 << k)
    best[0] = (0, [])
    for mask in range(1 << k):
        cur = best[mask]
        if cur is None:
            continue
        i = bin(mask).count("1")
        if i == k:
            continue
        for j in range(k):
            if not mask >> j & 1:
                v = cur[0] + cost[senders[i]][takers[j]]
                nxt = best[mask | 1 << j]
                if nxt is None or v < nxt[0]:
                    best[mask | 1 << j] = (v, cur[1] + [(senders[i], takers[j])])
    return best[(1 << k) - 1][1]


def euler_circuit_directed(n: int, arcs: Sequence[Arc], start: int = 0) -> list[int]:
    """Hierholzer's algorithm on a balanced, connected multigraph, O(n + m), no recursion."""
    out: list[list[int]] = [[] for _ in range(n)]
    for u, v in arcs:
        out[u].append(v)
    ptr = [0] * n
    stack, walk = [start], []
    while stack:
        u = stack[-1]
        if ptr[u] < len(out[u]):
            stack.append(out[u][ptr[u]])
            ptr[u] += 1
        else:
            walk.append(stack.pop())
    return walk[::-1]


def tree_to_tour(cost: Sequence[Sequence[float]], tree: Sequence[Edge]) -> tuple[list[int], list[Arc], list[Arc]]:
    """Lines L6 to L9: orient, balance, walk and shortcut. Return (tour, oriented tree, extra arcs)."""
    n = len(cost)
    oriented = [(u, v) if cost[u][v] <= cost[v][u] else (v, u) for u, v in tree]   # @line L6
    extra = balance_arcs(cost, oriented)                                           # @line L7
    walk = euler_circuit_directed(n, oriented + extra)                             # @line L8
    seen: set[int] = set()
    tour = []
    for v in walk:                                                                 # @line L9
        if v not in seen:
            seen.add(v)
            tour.append(v)
    return tour, oriented, extra


def asadpour_tour(cost: Sequence[Sequence[float]], rng: random.Random, samples: int | None = None) -> list[int]:
    """Return a tour as a list of vertices, for asymmetric costs with the directed
    triangle inequality (for example shortest path costs), n >= 3.

    With 2 ceil(ln n) samples the tour costs O(log n / log log n) LP* with high
    probability (cited; the page proves the bound for each thin tree).
    Cost here: exponential, because of the exact LP and the tree list.
    """
    n = len(cost)
    value, x, edges, z, trees, probs = max_entropy_distribution(cost)
    k = samples if samples is not None else 2 * math.ceil(math.log(n))
    picks = rng.choices(range(len(trees)), weights=probs, k=k)                    # @line L4
    best = min(picks, key=lambda t: sum(edge_cost(cost, edges[i]) for i in trees[t]))  # @line L5
    tour, _, _ = tree_to_tour(cost, [edges[i] for i in trees[best]])
    return tour                                                                    # @line L10


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    return sum(cost[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))
