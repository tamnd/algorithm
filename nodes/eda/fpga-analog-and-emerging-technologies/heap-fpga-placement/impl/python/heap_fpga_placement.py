# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/heap-fpga-placement/. The authors are listed in prov/5EREMJ.jsonl.

"""HeAP-style analytical placement for a heterogeneous FPGA.

The grid has nx columns and ny rows. Column x has the type col_type[x], such as
"L" for logic, "M" for memory or "D" for DSP, and every site in it has that
type. Movable block i has the type types[i]. Fixed pads have real positions.
A net is a list of terminals: ("b", i) for movable block i, ("p", j) for pad j.

Each iteration solves a quadratic wirelength model (clique net model, solved
by conjugate gradients), spreads the blocks of each type over the sites of
that type by recursive partitioning, and pulls the blocks toward their spread
sites with anchors of growing weight. The best legal placement is kept.
"""

import itertools
from typing import Optional

Pos = tuple[float, float]


def hpwl(nets, loc: list[Pos], pads: list[Pos]) -> float:
    total = 0.0
    for net in nets:
        pts = [loc[i] if k == "b" else pads[i] for k, i in net]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        total += (max(xs) - min(xs)) + (max(ys) - min(ys))
    return total


def build_system(n: int, nets, pads: list[Pos], anchors: Optional[list[Pos]], anchor_w: float, eps: float):
    """The matrix and the two right-hand sides of the clique model, as dicts of dicts."""
    a: list[dict[int, float]] = [dict() for _ in range(n)]
    bx = [0.0] * n
    by = [0.0] * n

    def add_diag(i: int, w: float) -> None:
        a[i][i] = a[i].get(i, 0.0) + w

    for net in nets:
        if len(net) < 2:
            continue
        w = 1.0 / (len(net) - 1)
        for (k1, i1), (k2, i2) in itertools.combinations(net, 2):
            if k1 == "b" and k2 == "b":
                if i1 == i2:
                    continue
                add_diag(i1, w)
                add_diag(i2, w)
                a[i1][i2] = a[i1].get(i2, 0.0) - w
                a[i2][i1] = a[i2].get(i1, 0.0) - w
            elif k1 == "b" or k2 == "b":
                i, j = (i1, i2) if k1 == "b" else (i2, i1)
                add_diag(i, w)
                bx[i] += w * pads[j][0]
                by[i] += w * pads[j][1]
    for i in range(n):
        target, w = (anchors[i], anchor_w) if anchors is not None else (None, 0.0)
        if eps > 0:
            add_diag(i, eps)
        if target is not None:
            add_diag(i, w)
            bx[i] += w * target[0]
            by[i] += w * target[1]
    return a, bx, by


def matvec(a: list[dict[int, float]], v: list[float]) -> list[float]:
    return [sum(w * v[j] for j, w in row.items()) for row in a]


def conjugate_gradient(a, b: list[float], x0: list[float], tol: float = 1e-12, max_iter: int = 1000) -> list[float]:
    x = list(x0)
    r = [bi - ai for bi, ai in zip(b, matvec(a, x))]
    p = list(r)
    rr = sum(v * v for v in r)
    for _ in range(max_iter):
        if rr <= tol * tol:
            break
        ap = matvec(a, p)
        step = rr / sum(pi * api for pi, api in zip(p, ap))
        x = [xi + step * pi for xi, pi in zip(x, p)]
        r = [ri - step * api for ri, api in zip(r, ap)]
        rr_new = sum(v * v for v in r)
        p = [ri + (rr_new / rr) * pi for ri, pi in zip(r, p)]
        rr = rr_new
    return x


def solve_quadratic(n, nets, pads, anchors, anchor_w, center: Pos, x0: list[Pos], eps: float = 1e-3) -> list[Pos]:
    """Minimize the clique-model quadratic wirelength plus anchor terms, in x and in y."""
    a, bx, by = build_system(n, nets, pads, anchors, anchor_w, eps)
    bx = [v + eps * center[0] for v in bx]
    by = [v + eps * center[1] for v in by]
    xs = conjugate_gradient(a, bx, [p[0] for p in x0])
    ys = conjugate_gradient(a, by, [p[1] for p in x0])
    return list(zip(xs, ys))


def spread(blocks: list[int], sites: list[tuple[int, int]], pos: list[Pos], out: dict[int, tuple[int, int]]) -> None:
    """Recursive partitioning: split the sites in two along the longer side, and the blocks in order with them."""
    if not blocks:
        return
    if len(sites) == 1:
        out[blocks[0]] = sites[0]
        return
    xs = {s[0] for s in sites}
    ys = {s[1] for s in sites}
    axis = 0 if max(xs) - min(xs) >= max(ys) - min(ys) else 1
    sites = sorted(sites, key=lambda s: (s[axis], s[1 - axis]))
    cut = len(sites) // 2
    # keep sites with the same coordinate on one side when that leaves both sides nonempty
    lo = [s for s in sites if s[axis] < sites[cut][axis]]
    if lo:
        cut = len(lo)
    c1, c2 = cut, len(sites) - cut
    order = sorted(blocks, key=lambda b: (pos[b][axis], pos[b][1 - axis], b))
    m = len(order)
    k = (2 * m * c1 + c1 + c2) // (2 * (c1 + c2))  # m * c1 / (c1 + c2), rounded half up
    k = max(m - c2, min(c1, k))
    spread(order[:k], sites[:cut], pos, out)
    spread(order[k:], sites[cut:], pos, out)


def heap_place(nx: int, ny: int, col_type: list[str], types: list[str], pads: list[Pos], nets, iters: int = 20, alpha: float = 0.05):
    """Returns (best legal placement, its HPWL, the HPWL of each iteration)."""
    n = len(types)
    sites_of: dict[str, list[tuple[int, int]]] = {}
    for x in range(nx):
        for y in range(ny):
            sites_of.setdefault(col_type[x], []).append((x, y))
    for t in set(types):
        if types.count(t) > len(sites_of.get(t, [])):
            raise ValueError(f"more blocks of type {t} than sites")
    center = ((nx - 1) / 2, (ny - 1) / 2)
    pos = solve_quadratic(n, nets, pads, None, 0.0, center, [center] * n)  # @line L1
    best: Optional[list[Pos]] = None  # @line L2
    best_cost = float("inf")
    history = []
    for k in range(1, iters + 1):  # @line L3
        out: dict[int, tuple[int, int]] = {}
        for t, sites in sites_of.items():  # @line L4
            spread([i for i in range(n) if types[i] == t], sites, pos, out)
        legal = [(float(out[i][0]), float(out[i][1])) for i in range(n)]
        cost = hpwl(nets, legal, pads)  # @line L5
        history.append(cost)
        if cost < best_cost:
            best, best_cost = legal, cost
        weight = alpha * k  # @line L6
        pos = solve_quadratic(n, nets, pads, legal, weight, center, pos)  # @line L7
    assert best is not None
    return best, best_cost, history  # @line L8


def exhaustive_min_hpwl(nx, ny, col_type, types, pads, nets) -> float:
    """Least HPWL over all legal placements: each type permuted over its own sites."""
    sites_of: dict[str, list[tuple[int, int]]] = {}
    for x in range(nx):
        for y in range(ny):
            sites_of.setdefault(col_type[x], []).append((x, y))
    groups = {t: [i for i in range(len(types)) if types[i] == t] for t in set(types)}
    keys = sorted(groups)
    best = float("inf")
    for choice in itertools.product(*(itertools.permutations(sites_of[t], len(groups[t])) for t in keys)):
        loc: list[Pos] = [(0.0, 0.0)] * len(types)
        for t, sites in zip(keys, choice):
            for i, s in zip(groups[t], sites):
                loc[i] = (float(s[0]), float(s[1]))
        best = min(best, hpwl(nets, loc, pads))
    return best
