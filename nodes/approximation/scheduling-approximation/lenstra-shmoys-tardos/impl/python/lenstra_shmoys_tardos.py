# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/lenstra-shmoys-tardos/. The authors are listed in prov/0P56MZ.jsonl.

from fractions import Fraction

INF = None  # a job that cannot run on a machine has time INF


def _phase_one(rows, rhs, basis, art):
    """Minimize the sum of the artificial columns with Bland's rule.

    rows and rhs describe equality constraints with rhs >= 0, and basis[r] is a
    unit column of row r. Returns the values of all columns at the final basic
    solution, or None if the minimum is positive (no feasible point).
    """
    ncol = len(rows[0])
    obj = [Fraction(0)] * ncol
    val = Fraction(0)
    for k in art:
        obj[k] = Fraction(1)
    for r, b in enumerate(basis):
        if b in art:
            obj = [obj[k] - rows[r][k] for k in range(ncol)]
            val -= rhs[r]
    while True:
        enter = next((k for k in range(ncol) if obj[k] < 0), None)
        if enter is None:
            break
        best = None
        for r in range(len(rows)):
            a = rows[r][enter]
            if a > 0:
                key = (rhs[r] / a, basis[r])
                if best is None or key < best[0]:
                    best = (key, r)
        r = best[1]  # bounded: the artificial sum is at least 0
        piv = rows[r][enter]
        rows[r] = [v / piv for v in rows[r]]
        rhs[r] = rhs[r] / piv
        for q in range(len(rows)):
            f = rows[q][enter]
            if q != r and f != 0:
                rows[q] = [rows[q][k] - f * rows[r][k] for k in range(ncol)]
                rhs[q] -= f * rhs[r]
        f = obj[enter]
        obj = [obj[k] - f * rows[r][k] for k in range(ncol)]
        val -= f * rhs[r]
        basis[r] = enter
    if val != 0:
        return None
    x = [Fraction(0)] * ncol
    for r, b in enumerate(basis):
        x[b] = rhs[r]
    return x


def lp_vertex(p, T):
    """Return a vertex x of LP(T) as a dict {(i, j): value}, or None if LP(T) is empty.

    LP(T): sum over i of x[i, j] = 1 for each job j, sum over j of p[i][j] x[i, j] <= T
    for each machine i, x >= 0, and x[i, j] = 0 when p[i][j] is INF or above T.
    """
    m, n = len(p), len(p[0])
    edges = [(i, j) for i in range(m) for j in range(n) if p[i][j] is not INF and p[i][j] <= T]
    ne = len(edges)
    ncol = ne + m + n  # x columns, then slacks of the machine rows, then artificials of the job rows
    rows, rhs, basis = [], [], []
    for j in range(n):
        row = [Fraction(0)] * ncol
        for k, (_, jj) in enumerate(edges):
            if jj == j:
                row[k] = Fraction(1)
        row[ne + m + j] = Fraction(1)
        rows.append(row)
        rhs.append(Fraction(1))
        basis.append(ne + m + j)
    for i in range(m):
        row = [Fraction(0)] * ncol
        for k, (ii, j) in enumerate(edges):
            if ii == i:
                row[k] = Fraction(p[i][j])
        row[ne + i] = Fraction(1)
        rows.append(row)
        rhs.append(Fraction(T))
        basis.append(ne + i)
    x = _phase_one(rows, rhs, basis, set(range(ne + m, ncol)))
    if x is None:
        return None
    return {e: x[k] for k, e in enumerate(edges) if x[k] != 0}


def least_feasible_T(p):
    """Binary search for the least integer T such that LP(T) is feasible. Times are integers."""
    n = len(p[0])
    best = [min(p[i][j] for i in range(len(p)) if p[i][j] is not INF) for j in range(n)]
    lo, hi = max(best, default=0), sum(best)  # LP(sum) holds the fastest-machine schedule
    while lo < hi:
        mid = (lo + hi) // 2
        if lp_vertex(p, mid) is None:
            lo = mid + 1
        else:
            hi = mid
    return lo


def round_vertex(x, n, m):
    """Round a vertex of LP(T) to an assignment: integral jobs stay, fractional jobs get a matching."""
    sigma = [None] * n
    for (i, j), v in x.items():
        if v == 1:
            sigma[j] = i  # @line L3
    jadj = {j: set() for j in range(n) if sigma[j] is None}
    madj = {i: set() for i in range(m)}
    for (i, j), v in x.items():  # @line L4
        if v != 1:
            jadj[j].add(i)
            madj[i].add(j)

    def remove(i, j):
        """Assign job j to machine i, then delete both from the graph."""
        sigma[j] = i
        for ii in jadj.pop(j):
            madj[ii].discard(j)
        for jj in madj.pop(i):
            jadj[jj].discard(i)

    while jadj:  # @line L5
        leaf = next((i for i, js in madj.items() if len(js) == 1), None)  # @line L6
        if leaf is not None:
            remove(leaf, next(iter(madj[leaf])))  # @line L7
            continue
        j0 = min(jadj)  # @line L8
        if len(jadj[j0]) != 2:  # with no machine leaf, a pseudoforest has only cycles left
            raise ValueError("the support is not a pseudoforest")
        remove(min(jadj[j0]), j0)  # @line L9
    return sigma


def lenstra_shmoys_tardos(p):
    """2-approximation for makespan on unrelated machines.

    p[i][j] is the integer time of job j on machine i, or INF if j cannot run on i.
    Every job must have a finite time somewhere. Returns (sigma, T) where sigma[j]
    is the machine of job j and T <= OPT is the least integer with LP(T) feasible.
    Each machine load is at most T + max p[i][j] over the fractional edges, so at most 2T.
    """
    m = len(p)
    n = len(p[0]) if m else 0
    if n == 0:
        return [], 0
    T = least_feasible_T(p)  # @line L1
    x = lp_vertex(p, T)  # @line L2
    return round_vertex(x, n, m), T  # @line L10
