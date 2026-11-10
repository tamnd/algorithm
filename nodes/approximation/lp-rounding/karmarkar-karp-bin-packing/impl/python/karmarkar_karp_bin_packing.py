# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/karmarkar-karp-bin-packing/. The authors are listed in prov/P2QGMB.jsonl.

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


def covering_lp(cols: Sequence[Sequence[int]], b: Sequence[int]):
    """Minimize sum x_C subject to sum_C cols[C][k] x_C >= b[k] and x >= 0, exactly.

    Two-phase simplex with Bland's rule. Returns (value, x) for a basic optimal solution, so x
    has at most len(b) nonzero entries. The LP must be feasible.
    """
    n, m = len(cols), len(b)
    t = []
    for k in range(m):
        t.append([Fraction(col[k]) for col in cols] + [Fraction(-1 if q == k else 0) for q in range(m)]
                 + [Fraction(1 if q == k else 0) for q in range(m)] + [Fraction(b[k])])
    basis = [n + m + k for k in range(m)]
    first_ar = n + m
    _run(t, basis, [Fraction(0)] * first_ar + [Fraction(1)] * m, first_ar + m)
    if any(basis[i] >= first_ar and t[i][-1] != 0 for i in range(m)):
        raise ValueError("the covering LP is infeasible")
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
    cost = [Fraction(1)] * n + [Fraction(0)] * m
    _run(t, basis, cost, first_ar)
    x = [Fraction(0)] * n
    for i, j in enumerate(basis):
        if j < n:
            x[j] = t[i][-1]
    return sum(x, Fraction(0)), x


def configurations(sizes: Sequence[Fraction]) -> list[tuple[int, ...]]:
    """All nonzero vectors a >= 0 of integers with sum a[k] sizes[k] <= 1.

    There is no bound a[k] <= count[k]: that bound would make the LP of the leftover items
    larger than the fractional parts of x, and the rounding argument would fail.
    """
    out = []

    def rec(k: int, room: Fraction, a: list[int]) -> None:
        if k == len(sizes):
            if any(a):
                out.append(tuple(a))
            return
        q = 0
        while q * sizes[k] <= room:
            a.append(q)
            rec(k + 1, room - q * sizes[k], a)
            a.pop()
            q += 1

    rec(0, Fraction(1), [])
    return out


def config_lp(sizes: Sequence[Number]):
    """The configuration LP (Gilmore-Gomory) of a list of sizes. Returns (value, configs, x, kinds)."""
    kinds = sorted(set(Fraction(s) for s in sizes), reverse=True)
    counts = [sum(1 for s in sizes if Fraction(s) == v) for v in kinds]
    configs = configurations(kinds)
    value, x = covering_lp(configs, counts)
    return value, configs, x, kinds


def first_fit(sizes: Sequence[Fraction], items: Sequence[int], bins: list[list[int]], loads: list[Fraction]) -> None:
    for it in items:
        for k in range(len(bins)):
            if loads[k] + sizes[it] <= 1:
                bins[k].append(it)
                loads[k] += sizes[it]
                break
        else:
            bins.append([it])
            loads.append(sizes[it])


def geometric_grouping(sizes: Sequence[Fraction], items: Sequence[int], k: int = 4):
    """Karmarkar-Karp geometric grouping. Returns (rounded, discarded).

    Class l holds the items with size in (2^-(l+1), 2^-l]. In each class, sort by size and cut
    into groups of k * 2^l items; the first group is discarded, and every other item is rounded
    up to the largest size in its group. rounded maps each kept item to its rounded size.
    """
    classes: dict[int, list[int]] = {}
    for it in items:
        lev = 0
        while sizes[it] <= Fraction(1, 2 ** (lev + 1)):
            lev += 1
        classes.setdefault(lev, []).append(it)
    rounded: dict[int, Fraction] = {}
    discarded: list[int] = []
    for lev, group_items in classes.items():
        group_items.sort(key=lambda it: (-sizes[it], it))
        q = k * 2 ** lev
        discarded += group_items[:q]
        for start in range(q, len(group_items), q):
            group = group_items[start:start + q]
            for it in group:
                rounded[it] = sizes[group[0]]
    return rounded, discarded


def karmarkar_karp_bin_packing(sizes: Sequence[Number], k: int = 4, trace: list | None = None) -> list[list[int]]:
    """Karmarkar-Karp bin packing with geometric grouping (1982).

    sizes[i] in (0, 1]. Returns a list of bins, each a list of item indices, with at most
    OPT + O(log^2 OPT) bins. k is the grouping parameter; k >= 4 halves the size of the
    remaining instance in each round, and the loop ends for every k >= 1 because each round
    discards at least one item. If trace is a list, each round appends
    (size_of_J, lp_of_J, lp_of_rounded, bins_packed, size_discarded, lp_of_rest).
    The LP is solved exactly over all configurations, so this is for small inputs only.
    """
    sizes = [Fraction(s) for s in sizes]
    if any(not 0 < s <= 1 for s in sizes):
        raise ValueError("sizes must be in (0, 1]")
    total = sum(sizes, Fraction(0))
    if not sizes:
        return []
    g = min(Fraction(1, 2), 1 / total)  # @line L1
    rest = [i for i in range(len(sizes)) if sizes[i] >= g]
    small = [i for i in range(len(sizes)) if sizes[i] < g]
    bins: list[list[int]] = []
    loads: list[Fraction] = []
    dropped: list[int] = []
    while rest:  # @line L2
        rounded, discarded = geometric_grouping(sizes, rest, k)  # @line L3
        dropped += discarded
        kept = sorted(rounded)
        packed: set[int] = set()
        if kept:
            value, configs, x, kinds = config_lp([rounded[i] for i in kept])  # @line L4
            pool = {v: [i for i in kept if rounded[i] == v] for v in kinds}
            before = len(bins)
            for conf, xc in zip(configs, x):
                for _ in range(xc.numerator // xc.denominator):  # @line L5
                    b = []
                    for q, v in zip(conf, kinds):
                        for _ in range(q):
                            if pool[v]:
                                b.append(pool[v].pop())
                    if b:
                        bins.append(b)
                        loads.append(sum((sizes[i] for i in b), Fraction(0)))
                        packed.update(b)
        rest_next = [i for i in kept if i not in packed]  # @line L6
        if trace is not None:
            lp_j = config_lp([sizes[i] for i in rest])[0]
            lp_r = value if kept else Fraction(0)
            lp_n = config_lp([sizes[i] for i in rest_next])[0] if rest_next else Fraction(0)
            trace.append((sum((sizes[i] for i in rest), Fraction(0)), lp_j, lp_r,
                          len(bins) - before if kept else 0, sum((sizes[i] for i in discarded), Fraction(0)), lp_n))
        rest = rest_next
    first_fit(sizes, sorted(dropped, key=lambda i: (-sizes[i], i)), bins, loads)  # @line L7
    first_fit(sizes, small, bins, loads)  # @line L8
    return bins  # @line L9
