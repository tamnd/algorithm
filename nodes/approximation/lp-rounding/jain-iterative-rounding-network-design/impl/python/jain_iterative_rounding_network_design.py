# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/jain-iterative-rounding-network-design/. The authors are listed in prov/GSS56Z.jsonl.

from fractions import Fraction
from typing import Mapping, Sequence

Number = int | Fraction


def _pivot(t: list[list[Fraction]], basis: list[int], r: int, col: int) -> None:
    pv = t[r][col]
    t[r] = [v / pv for v in t[r]]
    pr = t[r]
    nz = [k for k, v in enumerate(pr) if v]
    for i, row in enumerate(t):
        f = row[col]
        if i != r and f:
            for k in nz:
                row[k] -= f * pr[k]
    basis[r] = col


def _run(t: list[list[Fraction]], basis: list[int], cost: list[Fraction], ncols: int) -> None:
    """Primal simplex with Bland's rule on a feasible tableau."""
    while True:
        inb = set(basis)
        enter = None
        for j in range(ncols):
            if j not in inb:
                d = cost[j] - sum(cost[basis[i]] * row[j] for i, row in enumerate(t) if row[j])
                if d < 0:
                    enter = j
                    break
        if enter is None:
            return
        best = None
        for i, row in enumerate(t):
            if row[enter] > 0:
                q = row[-1] / row[enter]
                if best is None or q < best[0] or (q == best[0] and basis[i] < basis[best[1]]):
                    best = (q, i)
        if best is None:
            raise ValueError("the LP is unbounded")
        _pivot(t, basis, best[1], enter)


def lp_min(c: Sequence[Number], rows: Sequence[tuple[Sequence[Number], str, Number]]):
    """Minimize c.x subject to the rows and x >= 0, in exact arithmetic.

    Each row is (a, sense, b) with sense '<=', '>=' or '='. Returns (value, x) for a basic
    optimal solution, which is a vertex of the feasible region, or None if the LP is
    infeasible. Two-phase simplex with Bland's rule. For small instances only.
    """
    n = len(c)
    norm = []
    for a, sense, b in rows:
        a, b = [Fraction(v) for v in a], Fraction(b)
        if b < 0:
            a, b, sense = [-v for v in a], -b, {"<=": ">=", ">=": "<=", "=": "="}[sense]
        norm.append((a, sense, b))
    n_sl = sum(1 for _, s, _ in norm if s != "=")
    n_ar = sum(1 for _, s, _ in norm if s != "<=")
    first_ar = n + n_sl
    t, basis = [], []
    ks, ka = n, first_ar
    for a, sense, b in norm:
        row = a + [Fraction(0)] * (n_sl + n_ar) + [b]
        if sense == "<=":
            row[ks] = Fraction(1)
            basis.append(ks)
            ks += 1
        else:
            if sense == ">=":
                row[ks] = Fraction(-1)
                ks += 1
            row[ka] = Fraction(1)
            basis.append(ka)
            ka += 1
        t.append(row)
    _run(t, basis, [Fraction(0)] * first_ar + [Fraction(1)] * n_ar, first_ar + n_ar)
    if any(basis[i] >= first_ar and t[i][-1] != 0 for i in range(len(t))):
        return None
    i = 0
    while i < len(t):
        if basis[i] >= first_ar:
            j = next((j for j in range(first_ar) if t[i][j] != 0), None)
            if j is None:
                del t[i], basis[i]
                continue
            _pivot(t, basis, i, j)
        i += 1
    t = [row[:first_ar] + [row[-1]] for row in t]
    cost = [Fraction(v) for v in c] + [Fraction(0)] * n_sl
    _run(t, basis, cost, first_ar)
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = t[i][-1]
    return sum((cost[j] * x[j] for j in range(n)), Fraction(0)), x


def requirement(n: int, r: Mapping[tuple[int, int], int]) -> dict[int, int]:
    """f(S) = max r_uv over the pairs that S separates, for each S (a bit mask) without vertex n - 1."""
    f = {}
    for mask in range(1, 2 ** (n - 1)):
        f[mask] = max([q for (u, v), q in r.items() if ((mask >> u) & 1) != ((mask >> v) & 1)], default=0)
    return f


def crosses(mask: int, u: int, v: int) -> bool:
    return ((mask >> u) & 1) != ((mask >> v) & 1)


def jain_iterative_rounding(n: int, edges: Sequence[tuple[int, int, Number]], r: Mapping[tuple[int, int], int]):
    """Jain's iterative rounding for the survivable network design problem (2001).

    The graph has vertices 0 .. n - 1 and edges (u, v, cost), cost >= 0; each edge may be
    bought once. r[(u, v)] is the number of edge-disjoint u-v paths required. Returns
    (chosen, rounds): chosen lists the bought edges, and rounds holds (lp_value, x) for each
    LP solved, with x a vertex solution on the remaining edges. The cost of chosen is at most
    2 times the first LP value. Raises ValueError if even all edges do not meet r.
    The LP has 2^(n-1) - 1 cut rows, so this is for small graphs only.
    """
    f = requirement(n, r)
    chosen: list[int] = []  # @line L1
    rounds = []
    while True:
        g = {s: f[s] - sum(1 for e in chosen if crosses(s, edges[e][0], edges[e][1])) for s in f}
        if all(v <= 0 for v in g.values()):  # @line L2
            break
        rest = [e for e in range(len(edges)) if e not in chosen]
        rows = []
        for s, need in g.items():
            if need > 0:
                rows.append(([1 if crosses(s, edges[e][0], edges[e][1]) else 0 for e in rest], ">=", need))
        for k in range(len(rest)):
            rows.append(([1 if q == k else 0 for q in range(len(rest))], "<=", 1))
        sol = lp_min([edges[e][2] for e in rest], rows)  # @line L3
        if sol is None:  # @line L4
            raise ValueError("the requirements cannot be met with these edges")
        value, xs = sol
        x = {e: xs[k] for k, e in enumerate(rest)}
        rounds.append((value, x))
        heavy = [e for e in rest if x[e] >= Fraction(1, 2)]  # @line L5
        if not heavy:
            raise AssertionError("no edge with x_e >= 1/2: this contradicts Jain's theorem")
        chosen.extend(heavy)  # @line L6
    return chosen, rounds  # @line L7
