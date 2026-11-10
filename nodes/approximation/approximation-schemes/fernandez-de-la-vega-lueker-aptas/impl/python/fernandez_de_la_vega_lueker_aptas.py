# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/fernandez-de-la-vega-lueker-aptas/. The authors are listed in prov/SZNNHA.jsonl.

"""The Fernandez de la Vega-Lueker APTAS: linear grouping, the configuration LP and greedy small items.

The LP is solved exactly with fractions by the simplex method on its dual. This is for small instances only."""

from fractions import Fraction
from itertools import product
from math import ceil, floor
from typing import Optional, Sequence


def exact_pack(sizes: Sequence[Fraction]) -> list[list[int]]:
    """An optimal packing (lists of indices) by dynamic programming over the counts of each distinct size."""
    types = sorted(set(sizes), reverse=True)
    pos = {s: i for i, s in enumerate(types)}
    pools: list[list[int]] = [[] for _ in types]
    for j, s in enumerate(sizes):
        pools[pos[s]].append(j)
    count = [len(q) for q in pools]
    configs = [c for c in product(*(range(ci + 1) for ci in count))
               if any(c) and sum(ci * s for ci, s in zip(c, types)) <= 1]
    best: dict[tuple[int, ...], int] = {}
    pick: dict[tuple[int, ...], tuple[int, ...]] = {}
    for v in product(*(range(ci + 1) for ci in count)):
        if not any(v):
            best[v] = 0
            continue
        b = None
        for c in configs:
            if all(a <= w for a, w in zip(c, v)):
                r = best[tuple(w - a for w, a in zip(v, c))] + 1
                if b is None or r < b:
                    b, pick[v] = r, c
        best[v] = b
    bins, v = [], tuple(count)
    while any(v):
        c = pick[v]
        bins.append([pools[i].pop() for i, a in enumerate(c) for _ in range(a)])
        v = tuple(w - a for w, a in zip(v, c))
    return bins


def configuration_lp(types: Sequence[Fraction], demand: Sequence[int]) -> tuple[list[tuple[int, ...]], list[Fraction], Fraction]:
    """Solve min sum x_C subject to sum_C a_C x_C >= demand, x >= 0, over all configurations C of the sizes types.

    Return (configurations, a basic optimal x, the optimum). The simplex runs on the dual
    max demand.y subject to a_C.y <= 1, y >= 0, with Bland's rule; x is read from the final objective row."""
    d = len(types)
    configs = [c for c in product(*(range(int(1 // t) + 1) for t in types))
               if any(c) and sum(a * t for a, t in zip(c, types)) <= 1]
    r = len(configs)
    # tableau rows: one per configuration; columns: y_1..y_d, slack_1..slack_r, right-hand side
    rows = [[Fraction(a) for a in c] + [Fraction(int(i == q)) for i in range(r)] + [Fraction(1)]
            for q, c in enumerate(configs)]
    obj = [Fraction(-w) for w in demand] + [Fraction(0)] * r + [Fraction(0)]
    basis = [d + q for q in range(r)]
    while True:
        enter = next((j for j in range(d + r) if obj[j] < 0), None)
        if enter is None:
            break
        ratios = [(rows[q][-1] / rows[q][enter], basis[q], q) for q in range(r) if rows[q][enter] > 0]
        _, _, leave = min(ratios)
        piv = rows[leave][enter]
        rows[leave] = [v / piv for v in rows[leave]]
        for q in range(r):
            if q != leave and rows[q][enter] != 0:
                f = rows[q][enter]
                rows[q] = [a - f * b for a, b in zip(rows[q], rows[leave])]
        f = obj[enter]
        obj = [a - f * b for a, b in zip(obj, rows[leave])]
        basis[leave] = enter
    x = [obj[d + q] for q in range(r)]
    return configs, x, obj[-1]


def fernandez_de_la_vega_lueker_aptas(sizes: Sequence, eps, exact_limit: Optional[int] = None,
                                      stats: Optional[dict] = None) -> list[list[int]]:
    """Pack sizes in (0, 1] into unit bins with at most (1 + eps) OPT + 1 bins, for 0 < eps <= 1."""
    s = [Fraction(v) for v in sizes]
    delta = Fraction(eps) / 2  # @line L1
    large = sorted((j for j in range(len(s)) if s[j] >= delta), key=lambda j: -s[j])  # @line L2
    n1 = len(large)
    if exact_limit is None:
        exact_limit = ceil(2 / delta ** 4)
    info = {"large": n1, "K": 0, "d": 0, "lp": None, "lp_bins": 0}
    if n1 < exact_limit:  # @line L3
        bins = [[large[i] for i in b] for b in exact_pack([s[j] for j in large])]
    else:
        k_group = max(1, floor(delta * delta * n1))  # @line L4  (at least 1 when n1 >= 2 / delta^4)
        groups = [large[a:a + k_group] for a in range(0, n1, k_group)]
        rounded = [s[g[0]] for g in groups[1:]]  # @line L5
        types = sorted(set(rounded), reverse=True)
        pools: dict[Fraction, list[int]] = {t: [] for t in types}
        for g, t in zip(groups[1:], rounded):
            pools[t].extend(g)
        demand = [len(pools[t]) for t in types]
        configs, x, z = configuration_lp(types, demand)  # @line L6
        bins = []
        for c, xc in zip(configs, x):  # @line L7
            for _ in range(ceil(xc)):
                bins.append([pools[t].pop() for t, a in zip(types, c) for _ in range(a) if pools[t]])
        bins = [b for b in bins if b] + [[j] for j in groups[0]]  # @line L8
        info.update(K=k_group, d=len(types), lp=z, lp_bins=sum(ceil(v) for v in x),
                    support=sum(1 for v in x if v > 0))
    load = [sum(s[j] for j in b) for b in bins]
    for j in range(len(s)):  # @line L9
        if s[j] >= delta:
            continue
        i = next((i for i in range(len(bins)) if load[i] + s[j] <= 1), None)
        if i is None:
            bins.append([])
            load.append(Fraction(0))
            i = len(bins) - 1
        bins[i].append(j)
        load[i] += s[j]
    if stats is not None:
        stats.update(info)
    return bins  # @line L10
