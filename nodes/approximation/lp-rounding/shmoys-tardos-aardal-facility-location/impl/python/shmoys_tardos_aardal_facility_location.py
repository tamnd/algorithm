# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shmoys-tardos-aardal-facility-location/. The authors are listed in prov/C5BW1S.jsonl.

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
    """Minimize c.x subject to rows (a, sense, b), sense in '<=', '>=', '=', and x >= 0.

    Exact two-phase simplex with Bland's rule. Returns (value, x) or None if infeasible.
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


def ufl_lp(f: Sequence[Number], c: Sequence[Sequence[Number]]):
    """The LP relaxation of uncapacitated facility location. Returns (value, x, y)."""
    m, n = len(f), len(c[0])
    nv = m * n + m  # x[i][j] is variable i * n + j, y[i] is variable m * n + i
    cost = [c[i][j] for i in range(m) for j in range(n)] + list(f)
    rows = []
    for j in range(n):
        rows.append(([1 if v < m * n and v % n == j else 0 for v in range(nv)], "=", 1))
    for i in range(m):
        for j in range(n):
            a = [0] * nv
            a[i * n + j], a[m * n + i] = 1, -1
            rows.append((a, "<=", 0))
    value, z = lp_min(cost, rows)
    x = [[z[i * n + j] for j in range(n)] for i in range(m)]
    return value, x, z[m * n:]


def alpha_point(x: Sequence[Sequence[Fraction]], c: Sequence[Sequence[Number]], j: int, alpha: Fraction) -> Fraction:
    """g_j(alpha): the least g with sum of x_ij over c_ij <= g at least alpha."""
    total = Fraction(0)
    for i in sorted(range(len(x)), key=lambda i: c[i][j]):
        if x[i][j] > 0:
            total += x[i][j]
            if total >= alpha:
                return Fraction(c[i][j])
    raise ValueError("alpha must be in (0, 1]")


def cluster(f, c, x, alpha: Fraction):
    """Filter at alpha, then cluster. Returns (opened, assign, g)."""
    m, n = len(f), len(c[0])
    g = [alpha_point(x, c, j, alpha) for j in range(n)]  # @line L3
    near = [{i for i in range(m) if x[i][j] > 0 and c[i][j] <= g[j]} for j in range(n)]
    left = set(range(n))  # @line L4
    opened: list[int] = []
    assign = [-1] * n
    while left:
        j = min(left, key=lambda k: (g[k], k))  # @line L5
        i = min(near[j], key=lambda q: (f[q], q))  # @line L6
        opened.append(i)
        for k in sorted(left):
            if near[k] & near[j]:
                assign[k] = i  # @line L7
                left.discard(k)
    return opened, assign, g


def shmoys_tardos_aardal(f: Sequence[Number], c: Sequence[Sequence[Number]], alphas=None):
    """LP rounding for metric uncapacitated facility location (Shmoys, Tardos and Aardal 1997).

    f[i] is the opening cost of facility i and c[i][j] the cost to connect client j to i; c must
    be a metric. For each alpha in alphas (default: every breakpoint of the filtering in (0, 1]),
    filter the LP solution at alpha and cluster; keep the cheapest result. The default gives
    cost at most 3 / (1 - e^-3) < 3.16 times the LP value; a single alpha gives at most
    F / alpha + 3 C / (1 - alpha). Returns (opened, assign, lp_value, alpha).
    """
    m, n = len(f), len(c[0])
    lp_value, x, _ = ufl_lp(f, c)  # @line L1
    if alphas is None:
        alphas = set()
        for j in range(n):
            total = Fraction(0)
            for i in sorted(range(m), key=lambda i: c[i][j]):
                total += x[i][j]
                if 0 < total <= 1:
                    alphas.add(total)
    best = None
    for alpha in sorted(alphas):  # @line L2
        opened, assign, _ = cluster(f, c, x, Fraction(alpha))
        value = sum(f[i] for i in opened) + sum(c[assign[j]][j] for j in range(n))
        if best is None or value < best[0]:  # @line L8
            best = (value, opened, assign, Fraction(alpha))
    return best[1], best[2], lp_value, best[3]  # @line L9
