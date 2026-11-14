# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/symmetric-feasible-sequence-pair/. The authors are listed in prov/RFE075.jsonl.

"""Symmetric-feasible sequence pairs and a symmetric packing of them.

Cells are 0 .. n - 1 with widths w and heights h. A sequence pair is two
permutations gp (Gamma+) and gm (Gamma-) of the cells. One symmetric set with
a vertical axis is a dict sym: each cell of the group maps to its partner, and a
self-symmetric cell maps to itself. Cells not in sym are free.

Relations (as on the sequence-pair page): u is left of v if u is before v in
both sequences; u is below v if u is after v in gp and before v in gm.
"""

from fractions import Fraction


def positions(seq: list) -> dict:
    return {c: i for i, c in enumerate(seq)}


def is_symmetric_feasible(gp: list, gm: list, sym: dict) -> bool:
    """Balasa and Lampaert's condition: for distinct x, y in the group,
    pos+(x) < pos+(y) if and only if pos-(sym y) < pos-(sym x)."""
    pp, pm = positions(gp), positions(gm)
    g = list(sym)
    return all((pp[x] < pp[y]) == (pm[sym[y]] < pm[sym[x]]) for x in g for y in g if x != y)


def repair(gp: list, gm: list, sym: dict) -> list:
    """Return a new gm that keeps the slots of the group cells and of the free
    cells, and refills the group slots in the only order that the condition
    allows: the mirrors of the group cells, in the reverse order of gp."""
    forced = [sym[x] for x in reversed([c for c in gp if c in sym])]
    it = iter(forced)
    return [next(it) if c in sym else c for c in gm]


def _simplex_min(c: list, rows: list):
    """Minimize c.x subject to rows (a, sense, b) with sense in '<=', '=', '>=', and x >= 0.
    Exact two-phase simplex in Fraction with Bland's rule. Returns (value, x) or None when
    infeasible. The callers here always have a bounded objective."""
    n, m = len(c), len(rows)
    ns = sum(1 for _, sense, _ in rows if sense != "=")
    N = n + ns + m
    T, basis, s = [], [], n
    for i, (a, sense, b) in enumerate(rows):
        row = [Fraction(0)] * (N + 1)
        for j in range(n):
            row[j] = Fraction(a[j])
        if sense != "=":
            row[s] = Fraction(1 if sense == "<=" else -1)
            s += 1
        row[N] = Fraction(b)
        if row[N] < 0:
            row = [-v for v in row]
        row[n + ns + i] = Fraction(1)
        T.append(row)
        basis.append(n + ns + i)

    def pivot(r: int, col: int) -> None:
        pv = T[r][col]
        T[r] = [v / pv for v in T[r]]
        for i in range(len(T)):
            if i != r and T[i][col] != 0:
                f = T[i][col]
                T[i] = [a - f * b for a, b in zip(T[i], T[r])]
        basis[r] = col

    def run(cost: list, allowed: range) -> None:
        while True:
            enter = None
            for j in allowed:
                if j not in basis and cost[j] - sum(cost[basis[i]] * T[i][j] for i in range(len(T))) < 0:
                    enter = j
                    break
            if enter is None:
                return
            best = None
            for i in range(len(T)):
                if T[i][enter] > 0:
                    ratio = T[i][N] / T[i][enter]
                    if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]):
                        best = (ratio, i)
            if best is None:
                raise ArithmeticError("unbounded linear program")
            pivot(best[1], enter)

    run([0] * (n + ns) + [1] * m, range(N))
    if sum(T[i][N] for i in range(len(T)) if basis[i] >= n + ns) != 0:
        return None
    for i in range(len(T) - 1, -1, -1):  # drive the artificial variables out
        if basis[i] >= n + ns:
            j = next((j for j in range(n + ns) if T[i][j] != 0), None)
            if j is None:
                del T[i], basis[i]  # a redundant row
            else:
                pivot(i, j)
    run(list(c) + [0] * (N - n), range(n + ns))
    x = [Fraction(0)] * n
    for i, b in enumerate(basis):
        if b < n:
            x[b] = T[i][N]
    return sum(Fraction(ci) * xi for ci, xi in zip(c, x)), x


def sym_pack(gp: list, gm: list, w: list, h: list, sym: dict):
    """A placement with the group mirrored about one vertical axis, that keeps
    every relation of the sequence pair, with the least width and the least
    height among such placements. Returns None if the pair is not
    symmetric-feasible."""
    n = len(gp)
    if not is_symmetric_feasible(gp, gm, sym):  # @line L1
        return None
    pp, pm = positions(gp), positions(gm)
    left = [(u, v) for u in range(n) for v in range(n) if pp[u] < pp[v] and pm[u] < pm[v]]  # @line L2
    below = [(u, v) for u in range(n) for v in range(n) if pp[u] > pp[v] and pm[u] < pm[v]]
    node = {u: min(u, sym.get(u, u)) for u in range(n)}  # @line L3: a pair is one node
    succ: dict = {node[u]: [] for u in range(n)}
    indeg = {k: 0 for k in succ}
    for u, v in below:
        succ[node[u]].append((u, node[v]))
        indeg[node[v]] += 1
    order, stack = [], [k for k in succ if indeg[k] == 0]  # @line L4: Kahn's order
    while stack:
        k = stack.pop()
        order.append(k)
        for _, t in succ[k]:
            indeg[t] -= 1
            if indeg[t] == 0:
                stack.append(t)
    assert len(order) == len(succ), "the merged vertical graph has a cycle"
    ynode = {k: Fraction(0) for k in succ}
    for k in order:  # @line L5: longest paths
        for u, t in succ[k]:
            ynode[t] = max(ynode[t], ynode[k] + h[u])
    y = [ynode[node[u]] for u in range(n)]
    # x: variables x_0 .. x_{n-1}, X (the axis), W (the width); minimize W
    nv = n + 2
    X, W = n, n + 1
    rows = []

    def row(coef: dict, sense: str, b) -> None:
        a = [0] * nv
        for k, v in coef.items():
            a[k] += v
        rows.append((a, sense, b))

    for u, v in left:  # @line L6
        row({v: 1, u: -1}, ">=", w[u])
    for u in range(n):
        row({W: 1, u: -1}, ">=", w[u])
    for u, v in sym.items():
        if u == v:
            row({u: 2, X: -2}, "=", -w[u])  # center of u on the axis
        elif u < v:
            row({u: 1, v: 1, X: -2}, "=", -w[u])  # centers mirrored about the axis
    res = _simplex_min([0] * n + [0, 1], rows)  # @line L7
    if res is None:
        raise ArithmeticError("no symmetric x placement; this contradicts Balasa and Lampaert's theorem")
    width, sol = res
    x = sol[:n]
    height = max((y[u] + h[u] for u in range(n)), default=Fraction(0))
    return {"x": x, "y": y, "axis": sol[X], "width": width, "height": height}  # @line L8
