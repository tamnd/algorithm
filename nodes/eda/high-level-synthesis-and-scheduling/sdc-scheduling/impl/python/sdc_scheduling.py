# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/sdc-scheduling/. The authors are listed in prov/11PCP9.jsonl.

"""SDC-based scheduling (Cong and Zhang) for one data flow graph.

Operations are 0 .. n-1. Operation v has a latency lat[v] >= 0 in cycles and
a combinational delay dly[v]. An operation with lat[v] == 0 is
combinational: it may share a step with its predecessors (chaining), and
dly[v] must be at most the clock period. An operation with lat[v] >= 1
registers its result, so it breaks combinational paths. It keeps its unit
busy for occ(v) = max(1, lat[v]) steps, from s[v] to s[v] + occ(v) - 1.

Every constraint is a difference constraint s[v] - s[u] >= w, kept as the
triple (u, v, w). All arithmetic is exact (int and Fraction).
"""

from fractions import Fraction
from typing import Optional

Constraint = tuple[int, int, int]


def occ(lat: list[int], v: int) -> int:
    return max(1, lat[v])


def topological_order(n: int, edges: list[tuple[int, int]]) -> list[int]:
    succ: list[list[int]] = [[] for _ in range(n)]
    indeg = [0] * n
    for (u, v) in edges:
        succ[u].append(v)
        indeg[v] += 1
    order: list[int] = []
    ready = sorted(v for v in range(n) if indeg[v] == 0)
    while ready:
        u = ready.pop(0)
        order.append(u)
        for v in succ[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                ready.append(v)
        ready.sort()
    if len(order) != n:
        raise ValueError("the data flow graph has a cycle")
    return order


def chain_delays(n: int, edges: list[tuple[int, int]], lat: list[int], dly: list) -> dict:
    """D[(u, v)] = the largest delay of a path from u to v through latency-0 operations only."""
    order = topological_order(n, edges)
    succ: list[list[int]] = [[] for _ in range(n)]
    for (u, v) in edges:
        succ[u].append(v)
    D: dict = {}
    for u in order:
        if lat[u] != 0:
            continue
        best = {u: dly[u]}
        for x in order:
            if x in best:
                for y in succ[x]:
                    if lat[y] == 0 and best[x] + dly[y] > best.get(y, -1):
                        best[y] = best[x] + dly[y]
        for v, d in best.items():
            D[(u, v)] = d
    return D


def ceil_div(a, b) -> int:
    q = Fraction(a) / Fraction(b)
    return -((-q.numerator) // q.denominator)


def least_solution(n: int, cons: list[Constraint]) -> Optional[list[int]]:
    """Least s >= 0 with s[v] - s[u] >= w for all (u, v, w), or None (a positive cycle)."""
    s = [0] * n
    for _ in range(n + 1):
        changed = False
        for (u, v, w) in cons:
            if s[u] + w > s[v]:
                s[v] = s[u] + w
                changed = True
        if not changed:
            return s
    return None


def build_constraints(n, edges, lat, dly, kind, limits, period, latency_bound=None, extra=()):
    """Return (constraints, upper) where upper[v] bounds s[v] from above, or None."""
    for v in range(n):
        if lat[v] == 0 and dly[v] > period:
            raise ValueError("a combinational operation is slower than the clock period")
    cons: list[Constraint] = []
    for (u, v) in edges:                                          # @line L2
        cons.append((u, v, lat[u]))
    for (u, v), d in sorted(chain_delays(n, edges, lat, dly).items()):   # @line L3
        k = ceil_div(d, period) - 1
        if u != v and k >= 1:
            cons.append((u, v, k))
    cons.extend(extra)
    asap = least_solution(n, cons)                                # @line L4
    if asap is None:
        return None, None
    span = max(asap[v] + occ(lat, v) for v in range(n)) if n else 0
    alap = [span - occ(lat, v) for v in range(n)]
    for _ in range(n + 1):
        for (u, v, w) in cons:
            alap[u] = min(alap[u], alap[v] - w)
    topo = {v: i for i, v in enumerate(topological_order(n, edges))}
    for k in sorted(limits):                                      # @line L5
        o = sorted((v for v in range(n) if kind[v] == k), key=lambda v: (alap[v], asap[v], topo[v]))  # @line L6
        c = limits[k]
        for i in range(len(o) - c):                               # @line L7
            cons.append((o[i], o[i + c], occ(lat, o[i])))
    upper = None
    if latency_bound is not None:                                 # @line L8
        upper = [latency_bound - occ(lat, v) for v in range(n)]
    return cons, upper


def lp_max(c: list, A: list[list], b: list):
    """Maximize c.x subject to A x <= b and x >= 0, by the simplex method with Bland's rule.

    Returns (value, x) with exact fractions, None if infeasible. Raises ValueError if unbounded.
    """
    m, n = len(A), len(c)
    F = Fraction
    N = list(range(n))
    B = list(range(n, n + m))
    T = [[F(a) for a in row] for row in A]
    rhs = [F(x) for x in b]
    obj = [F(0)] * n
    val = F(0)

    def pivot(l, e):
        nonlocal val, m
        piv = T[l][e]
        rhs[l] /= piv
        for j in range(len(N)):
            if j != e:
                T[l][j] /= piv
        T[l][e] = 1 / piv
        for i in range(m):
            if i != l and T[i][e] != 0:
                coef = T[i][e]
                rhs[i] -= coef * rhs[l]
                for j in range(len(N)):
                    if j != e:
                        T[i][j] -= coef * T[l][j]
                T[i][e] = -coef * T[l][e]
        val += obj[e] * rhs[l]
        ce = obj[e]
        for j in range(len(N)):
            if j != e:
                obj[j] -= ce * T[l][j]
        obj[e] = -ce * T[l][e]
        B[l], N[e] = N[e], B[l]

    def run():
        while True:
            cand = [j for j in range(len(N)) if obj[j] > 0]
            if not cand:
                return
            e = min(cand, key=lambda j: N[j])
            rows = [i for i in range(m) if T[i][e] > 0]
            if not rows:
                raise ValueError("the LP is unbounded")
            l = min(rows, key=lambda i: (rhs[i] / T[i][e], B[i]))
            pivot(l, e)

    if m and min(rhs) < 0:
        aux = n + m
        N.append(aux)
        for row in T:
            row.append(F(-1))
        obj = [F(0)] * n + [F(-1)]
        l = min(range(m), key=lambda i: (rhs[i], B[i]))
        pivot(l, len(N) - 1)
        run()
        if val < 0:
            return None
        if aux in B:
            l = B.index(aux)
            nz = [j for j in range(len(N)) if T[l][j] != 0 and N[j] != aux]
            if nz:
                pivot(l, nz[0])
            else:
                del T[l], rhs[l], B[l]
                m -= 1
        e = N.index(aux)
        N.pop(e)
        for row in T:
            row.pop(e)
        obj = [F(0)] * len(N)
        val = F(0)
        for x in range(n):
            if x in N:
                obj[N.index(x)] += c[x]
            else:
                i = B.index(x)
                val += c[x] * rhs[i]
                for j in range(len(N)):
                    obj[j] -= c[x] * T[i][j]
    else:
        obj = [F(x) for x in c]
    run()
    x = [F(0)] * n
    for i, var in enumerate(B):
        if var < n:
            x[var] = rhs[i]
    return val, x


def sdc_schedule(n, edges, lat, dly, kind, limits, period, latency_bound=None, weights=None, extra=()):
    """Schedule by the SDC method. Returns a list of start steps, or None when the system is infeasible.

    weights[v] is the cost per step of s[v] (default 1, which gives ASAP-like schedules).
    With nonnegative weights the least solution is returned. Otherwise an LP is solved,
    which needs latency_bound so that the LP is bounded.
    """
    cons, upper = build_constraints(n, edges, lat, dly, kind, limits, period, latency_bound, extra)  # @line L1
    if cons is None:
        return None
    w = [1] * n if weights is None else list(weights)
    least = least_solution(n, cons)                               # @line L9
    if least is None or (upper is not None and any(least[v] > upper[v] for v in range(n))):
        return None
    if all(x >= 0 for x in w):                                    # @line L10
        return least
    if upper is None:
        raise ValueError("negative weights need a latency bound")
    A, b = [], []                                                 # @line L11
    for (u, v, c) in cons:
        row = [0] * n
        row[u] += 1
        row[v] -= 1
        A.append(row)
        b.append(-c)
    for v in range(n):
        row = [0] * n
        row[v] = 1
        A.append(row)
        b.append(upper[v])
    res = lp_max([-x for x in w], A, b)
    if res is None:
        return None
    _, x = res
    if any(xi.denominator != 1 for xi in x):
        raise AssertionError("a vertex of a totally unimodular system was not integral")
    return [int(xi) for xi in x]


def latency(lat: list[int], s: list[int]) -> int:
    return max((s[v] + occ(lat, v) for v in range(len(s))), default=0)


def is_valid(n, edges, lat, dly, kind, limits, period, s, latency_bound=None) -> bool:
    """Check a schedule directly against the model, without difference constraints."""
    if any(x < 0 for x in s):
        return False
    if any(s[v] < s[u] + lat[u] for (u, v) in edges):
        return False
    if latency_bound is not None and latency(lat, s) > latency_bound:
        return False
    order = topological_order(n, edges)
    arrive = [0] * n
    for v in order:
        if lat[v] == 0:
            arrive[v] = dly[v] + max([arrive[u] for (u, x) in edges if x == v and lat[u] == 0 and s[u] == s[v]],
                                     default=0)
            if arrive[v] > period:
                return False
    for k, c in limits.items():
        busy: dict = {}
        for v in range(n):
            if kind[v] == k:
                for j in range(s[v], s[v] + occ(lat, v)):
                    busy[j] = busy.get(j, 0) + 1
        if any(x > c for x in busy.values()):
            return False
    return True
