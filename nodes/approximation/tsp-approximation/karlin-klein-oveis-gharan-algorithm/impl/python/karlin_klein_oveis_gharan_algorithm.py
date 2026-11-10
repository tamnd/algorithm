# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karlin-klein-oveis-gharan-algorithm/. The authors are listed in prov/879EXX.jsonl.

"""The max entropy algorithm for metric TSP, the method of Karlin, Klein and Oveis Gharan.

This code is for small instances only (n at most about 9). It solves the
subtour LP exactly with fractions, separates cuts by trying all subsets,
and represents the max entropy distribution by listing all spanning trees
of the support. A real implementation uses min cuts, the matrix-tree
theorem and a convex solver, and runs in polynomial time.
"""

import itertools
import math
import random
from fractions import Fraction
from typing import Sequence

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


def subtour_lp(cost: Sequence[Sequence[Fraction]]) -> tuple[Fraction, dict[Edge, Fraction]]:
    """Solve the subtour LP exactly by cutting planes. Return LP* and the nonzero x.

    Precondition: symmetric costs, n >= 3. Separation tries all 2^(n-1) cuts.
    """
    n = len(cost)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    rows: list[list[Fraction]] = [[Fraction(int(v in e)) for e in edges] for v in range(n)]
    senses = ["="] * n
    rhs = [Fraction(2)] * n
    while True:
        value, x = simplex_min([Fraction(cost[i][j]) for i, j in edges], rows, senses, rhs)
        worst = None
        for mask in range(1, 1 << (n - 1)):
            side = mask << 1 | 1
            if side == (1 << n) - 1:
                continue
            row = [Fraction(int((side >> i & 1) != (side >> j & 1))) for i, j in edges]
            s = sum(r * t for r, t in zip(row, x))
            if s < 2 and (worst is None or s < worst[0]):
                worst = (s, row)
        if worst is None:
            return value, {e: t for e, t in zip(edges, x) if t != 0}
        rows.append(worst[1])
        senses.append(">=")
        rhs.append(Fraction(2))


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


def min_weight_perfect_matching(cost: Sequence[Sequence[float]], vertices: Sequence[int]) -> list[Edge]:
    """Exact matching by a bitmask DP in O(2^k k) time for k vertices (k even)."""
    k = len(vertices)
    best: dict[int, tuple[float, list[Edge]]] = {0: (0, [])}
    for mask in range(1, 1 << k):
        if bin(mask).count("1") % 2:
            continue
        i = (mask & -mask).bit_length() - 1
        cand = None
        for j in range(i + 1, k):
            if mask >> j & 1:
                rest = best[mask ^ (1 << i) ^ (1 << j)]
                v = rest[0] + cost[vertices[i]][vertices[j]]
                if cand is None or v < cand[0]:
                    cand = (v, rest[1] + [(vertices[i], vertices[j])])
        if cand is not None:
            best[mask] = cand
    return best[(1 << k) - 1][1]


def euler_circuit(n: int, edges: Sequence[Edge], start: int = 0) -> list[int]:
    """Hierholzer's algorithm with an explicit stack, O(n + m)."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for idx, (u, v) in enumerate(edges):
        adj[u].append((v, idx))
        adj[v].append((u, idx))
    used = [False] * len(edges)
    ptr = [0] * n
    stack, out = [start], []
    while stack:
        u = stack[-1]
        while ptr[u] < len(adj[u]) and used[adj[u][ptr[u]][1]]:
            ptr[u] += 1
        if ptr[u] == len(adj[u]):
            out.append(stack.pop())
        else:
            v, idx = adj[u][ptr[u]]
            used[idx] = True
            stack.append(v)
    return out[::-1]


def tree_to_tour(cost: Sequence[Sequence[float]], tree: Sequence[Edge]) -> tuple[list[int], list[Edge]]:
    """Christofides' completion of a spanning tree: return the tour and the matching."""
    n = len(cost)
    deg = [0] * n
    for u, v in tree:
        deg[u] += 1
        deg[v] += 1
    odd = [v for v in range(n) if deg[v] % 2]                    # @line L5
    matching = min_weight_perfect_matching(cost, odd)            # @line L6
    walk = euler_circuit(n, list(tree) + matching)               # @line L7
    seen: set[int] = set()
    tour = []
    for v in walk:                                               # @line L8
        if v not in seen:
            seen.add(v)
            tour.append(v)
    return tour, matching


def max_entropy_distribution(cost: Sequence[Sequence[float]]):
    """Lines L1 to L3. Return (LP*, x, edges, z, trees, probs, gamma)."""
    n = len(cost)
    value, x = subtour_lp([[Fraction(v) for v in row] for row in cost])  # @line L1
    edges = sorted(x)
    z = [x[e] * (n - 1) / n for e in edges]                               # @line L2
    trees = spanning_trees(n, edges)
    gamma = max_entropy_gamma(trees, [float(t) for t in z])               # @line L3
    probs = tree_probabilities(trees, gamma)
    return value, x, edges, z, trees, probs, gamma


def kko_tour(cost: Sequence[Sequence[float]], rng: random.Random) -> list[int]:
    """Return a tour as a list of vertices, for symmetric metric costs, n >= 3.

    Expected cost at most (1 - 1/n) LP* + LP*/2 <= 3/2 OPT (proved on the page);
    KKO's analysis gives (3/2 - 10^(-36)) OPT for their variant (cited).
    """
    value, x, edges, z, trees, probs, gamma = max_entropy_distribution(cost)
    pick = rng.choices(range(len(trees)), weights=probs)[0]             # @line L4
    tour, _ = tree_to_tour(cost, [edges[k] for k in trees[pick]])
    return tour                                                          # @line L9


def tour_cost(cost: Sequence[Sequence[float]], tour: Sequence[int]) -> float:
    return sum(cost[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))
