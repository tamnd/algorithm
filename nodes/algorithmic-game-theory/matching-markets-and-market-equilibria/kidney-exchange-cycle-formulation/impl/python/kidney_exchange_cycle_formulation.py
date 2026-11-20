# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kidney-exchange-cycle-formulation/. The authors are listed in prov/HATF0Q.jsonl.

from fractions import Fraction
from typing import Iterable, Optional

from agtlp import lp_max

Cycle = tuple[int, ...]


def short_cycles(n: int, succ: list[list[int]], L: int, alive: Optional[set[int]] = None) -> list[Cycle]:
    """Every directed cycle with at most L vertices, each listed once from its smallest vertex.

    O(n * d^(L-1)) time for maximum out-degree d.
    """
    alive = set(range(n)) if alive is None else alive
    out: list[Cycle] = []

    def extend(path: list[int], on: set[int]) -> None:
        s, v = path[0], path[-1]
        for u in succ[v]:
            if u == s:
                out.append(tuple(path))
            elif u > s and u in alive and u not in on and len(path) < L:
                path.append(u)
                on.add(u)
                extend(path, on)
                on.discard(u)
                path.pop()

    for s in sorted(alive):
        extend([s], {s})
    return out


def _master(cols: list[Cycle], weight: dict[Cycle, int], verts: list[int]):
    """Solve max sum w_c x_c subject to sum of x_c over the columns at v <= 1, x >= 0."""
    if not cols:
        return [], Fraction(0), {v: Fraction(0) for v in verts}
    row = {v: k for k, v in enumerate(verts)}
    A = [[0] * len(cols) for _ in verts]
    for j, c in enumerate(cols):
        for v in c:
            A[row[v]][j] = 1
    status, x, value, dual = lp_max([weight[c] for c in cols], A, [1] * len(verts))
    assert status == "optimal"
    return x, value, {v: dual[row[v]] for v in verts}


def kidney_exchange(
    n: int, arcs: Iterable[tuple[int, int]], L: int, w: Optional[dict[tuple[int, int], int]] = None
) -> tuple[int, list[Cycle], dict]:
    """Maximum weight packing of vertex-disjoint cycles with at most L vertices.

    This is the cycle formulation of Abraham, Blum and Sandholm (2007), solved by branch and
    price: each node solves the LP relaxation by column generation, with exact pricing by
    enumeration of the short cycles and the LP duals, and branches on a fractional cycle
    (take it, or forbid it). Pairs are 0, ..., n - 1, an arc (i, j) means that the donor of
    pair i can give to the patient of pair j, and w gives integer arc weights (default 1, so
    the value is the number of transplants). Returns (value, cycles, stats), with stats the
    root LP bound and the number of nodes. The worst case is exponential (the problem is
    NP-hard for L >= 3); each LP is solved exactly in Fraction.
    """
    arcs = list(arcs)
    w = {a: 1 for a in arcs} if w is None else w
    succ: list[list[int]] = [[] for _ in range(n)]
    for i, j in arcs:
        if i != j:
            succ[i].append(j)

    def weight_of(c: Cycle) -> int:
        return sum(w[(c[k], c[(k + 1) % len(c)])] for k in range(len(c)))

    weight: dict[Cycle, int] = {}
    best, best_set = 0, []  # @line L1
    stack = [((), frozenset(), [])]  # @line L2  (fixed cycles, forbidden cycles, columns)
    stats = {"nodes": 0, "root_lp": None}
    while stack:  # @line L3
        fixed, forbidden, cols = stack.pop()  # @line L4
        stats["nodes"] += 1
        used = {v for c in fixed for v in c}
        verts = [v for v in range(n) if v not in used]
        cands = [c for c in short_cycles(n, succ, L, set(verts)) if c not in forbidden]
        for c in cands:
            if c not in weight:
                weight[c] = weight_of(c)
        cols = [c for c in cols if c not in forbidden and not used.intersection(c)]
        while True:
            x, value, y = _master(cols, weight, verts)  # @line L5
            have = set(cols)
            new = [c for c in cands if c not in have and weight[c] - sum(y[v] for v in c) > 0]  # @line L6
            if not new:  # @line L7
                break
            cols = cols + new
        if stats["root_lp"] is None:
            stats["root_lp"] = value
        base = sum(weight[c] for c in fixed)
        if base + (value.numerator // value.denominator) <= best:  # @line L8
            continue
        frac = [(x[j], c) for j, c in enumerate(cols) if 0 < x[j] < 1]
        if not frac:  # @line L9
            best = base + int(value)
            best_set = list(fixed) + [c for j, c in enumerate(cols) if x[j] == 1]
            continue
        c = max(frac)[1]  # @line L10
        stack.append((fixed, forbidden | {c}, [d for d in cols if d != c]))  # @line L11
        stack.append((fixed + (c,), forbidden, [d for d in cols if not set(d).intersection(c)]))
    return best, sorted(best_set), stats  # @line L12
