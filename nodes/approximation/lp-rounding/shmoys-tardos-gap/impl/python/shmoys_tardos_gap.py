# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shmoys-tardos-gap/. The authors are listed in prov/6ZNFNM.jsonl.

from fractions import Fraction
from typing import Sequence

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
    width = first_ar + n_ar
    _run(t, basis, [Fraction(0)] * first_ar + [Fraction(1)] * n_ar, width)
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


def min_cost_job_matching(n_jobs: int, n_slots: int, edges: Sequence[tuple[int, int, Number]]):
    """Minimum cost matching that covers every job, by successive shortest paths.

    edges holds (job, slot, cost). Returns a list slot_of_job, or None if no matching covers
    all jobs. Bellman-Ford on the residual graph, O(n_jobs * V * E) time.
    """
    adj = [[] for _ in range(n_jobs)]
    for j, s, w in edges:
        adj[j].append((s, Fraction(w)))
    job_of_slot = [-1] * n_slots
    slot_of_job = [-1] * n_jobs
    for root in range(n_jobs):
        dist_job = [None] * n_jobs
        dist_slot = [None] * n_slots
        prev_slot = [-1] * n_slots
        dist_job[root] = Fraction(0)
        changed = True
        while changed:
            changed = False
            for j in range(n_jobs):
                if dist_job[j] is None:
                    continue
                for s, w in adj[j]:
                    if slot_of_job[j] == s:
                        continue
                    d = dist_job[j] + w
                    if dist_slot[s] is None or d < dist_slot[s]:
                        dist_slot[s], prev_slot[s] = d, j
                        changed = True
            for s in range(n_slots):
                j = job_of_slot[s]
                if j >= 0 and dist_slot[s] is not None:
                    w = next(w for t_, w in adj[j] if t_ == s)
                    d = dist_slot[s] - w
                    if dist_job[j] is None or d < dist_job[j]:
                        dist_job[j] = d
                        changed = True
        free = [s for s in range(n_slots) if job_of_slot[s] < 0 and dist_slot[s] is not None]
        if not free:
            return None
        s = min(free, key=lambda u: (dist_slot[u], u))
        while True:
            j = prev_slot[s]
            old = slot_of_job[j]
            slot_of_job[j], job_of_slot[s] = s, j
            if j == root:
                break
            s = old
    return slot_of_job


def shmoys_tardos_gap(p: Sequence[Sequence[Number]], c: Sequence[Sequence[Number]], t: Number):
    """Shmoys-Tardos rounding for the generalized assignment problem.

    p[i][j] and c[i][j] are the time and the cost of job j on machine i, both >= 0, and t > 0
    is the target makespan. Returns None if the LP with makespan t is infeasible. Otherwise
    returns (assign, lp_value, x): assign[j] is the machine of job j, the total cost is at most
    lp_value, and each machine i gets load at most t + max p[i][j] over the jobs j with
    x[i][j] > 0. Time: one LP with m n variables plus a matching on n jobs and at most n + m slots.
    """
    m, n = len(p), len(p[0])
    t = Fraction(t)
    var = [(i, j) for i in range(m) for j in range(n) if p[i][j] <= t]
    idx = {v: k for k, v in enumerate(var)}
    rows = []
    for j in range(n):
        rows.append(([1 if v[1] == j else 0 for v in var], "=", 1))
    for i in range(m):
        rows.append(([p[v[0]][v[1]] if v[0] == i else 0 for v in var], "<=", t))
    if any(all(p[i][j] > t for i in range(m)) for j in range(n)):
        return None
    sol = lp_min([c[i][j] for i, j in var], rows)  # @line L1
    if sol is None:  # @line L2
        return None
    lp_value, xv = sol
    x = [[xv[idx[(i, j)]] if (i, j) in idx else Fraction(0) for j in range(n)] for i in range(m)]
    slots, edges = [], []
    for i in range(m):  # @line L3
        k_i = -(-sum(x[i]) // 1)  # @line L4
        order = sorted((j for j in range(n) if x[i][j] > 0), key=lambda j: (-p[i][j], j))
        s, room = 0, Fraction(1)
        base = len(slots)
        slots.extend((i, q) for q in range(int(k_i)))
        for j in order:  # @line L5
            rest = x[i][j]
            while rest > 0:
                take = min(rest, room)
                edges.append((j, base + s, c[i][j]))  # @line L6
                rest -= take
                room -= take
                if room == 0 and s + 1 < k_i:
                    s, room = s + 1, Fraction(1)
    slot_of_job = min_cost_job_matching(n, len(slots), edges)  # @line L7
    assign = [slots[slot_of_job[j]][0] for j in range(n)]  # @line L8
    return assign, lp_value, x  # @line L9
