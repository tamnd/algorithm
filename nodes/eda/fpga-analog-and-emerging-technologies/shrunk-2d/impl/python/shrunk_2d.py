# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/shrunk-2d/. The authors are listed in prov/BTYXM7.jsonl.

"""Shrunk-2D: a two-tier gate-level 3D flow built on a 2D placer.

A design has n cells with widths w[i] and heights h[i], a square die of
side W, and nets. A net is a pair (cells, pads): a list of cell indices and
a list of fixed pad points (x, y) on the die.

The flow scales every cell, pad and the die by s = 1/sqrt(2), places the
shrunk design with a 2D placer, gives each cell back its original size,
cuts the die into k x k bins, and splits the cells of every bin between
tier 0 and tier 1 with a Fiduccia-Mattheyses pass that keeps the area of
the two tiers balanced inside each bin. Every cut net gets one inter-tier
via (MIV) at the center of its bounding box.

The placer here is a small stand-in for the commercial tool of the paper:
a quadratic placement with the clique net model, solved by Gauss-Seidel,
followed by spreading by rank. Both steps commute with scaling, which is
the property that the flow uses. There is no legalization into rows, no
routing, no memory handling and no clock tree.
"""

import math

SCALE = 1.0 / math.sqrt(2.0)


def shrink(widths, heights, nets, die, s=SCALE):
    """Scale cell sizes, pads and die by s (the metal pitch would scale too)."""
    w = [x * s for x in widths]
    h = [y * s for y in heights]
    new_nets = [(list(cs), [(px * s, py * s) for px, py in pads]) for cs, pads in nets]
    return w, h, new_nets, die * s


def quadratic_place(n, nets, die, tol=1e-13, max_iter=20000):
    """Clique-model quadratic placement, then spread by rank over the die."""
    nbr = [dict() for _ in range(n)]
    anchor = [[0.0, 0.0, 0.0] for _ in range(n)]  # weight, sum wx, sum wy
    for cells, pads in nets:
        p = len(cells) + len(pads)
        if p < 2:
            continue
        wt = 1.0 / (p - 1)
        for a in cells:
            for b in cells:
                if a != b:
                    nbr[a][b] = nbr[a].get(b, 0.0) + wt
            for px, py in pads:
                anchor[a][0] += wt
                anchor[a][1] += wt * px
                anchor[a][2] += wt * py
    x = [die / 2.0] * n
    y = [die / 2.0] * n
    for _ in range(max_iter):
        delta = 0.0
        for i in range(n):
            tw = anchor[i][0] + sum(nbr[i].values())
            if tw == 0.0:
                continue
            nx = (anchor[i][1] + sum(wt * x[j] for j, wt in nbr[i].items())) / tw
            ny = (anchor[i][2] + sum(wt * y[j] for j, wt in nbr[i].items())) / tw
            delta = max(delta, abs(nx - x[i]), abs(ny - y[i]))
            x[i], y[i] = nx, ny
        if delta <= tol * die:
            break
    return spread_by_rank(x, die), spread_by_rank(y, die)


def spread_by_rank(coord, die):
    """Put the cell of rank r at (r + 0.5) / n of the die side."""
    n = len(coord)
    order = sorted(range(n), key=lambda i: (round(coord[i] / die, 9), i))
    out = [0.0] * n
    for r, i in enumerate(order):
        out[i] = (r + 0.5) * die / n
    return out


def hpwl(xs, ys, nets):
    total = 0.0
    for cells, pads in nets:
        px = [xs[c] for c in cells] + [p[0] for p in pads]
        py = [ys[c] for c in cells] + [p[1] for p in pads]
        if len(px) >= 2:
            total += max(px) - min(px) + max(py) - min(py)
    return total


def make_bins(xs, ys, die, k):
    size = die / k
    return [min(int(x / size), k - 1) * k + min(int(y / size), k - 1) for x, y in zip(xs, ys)]


def bin_limits(areas, bins, eps):
    """Allowed |area(tier 0) - area(tier 1)| in each bin.

    As in the balance rule of Fiduccia and Mattheyses, each tier may be off
    half the bin area by the largest cell, so the limit on the difference is
    twice the largest cell area, or eps times the bin area if that is more.
    """
    total, biggest = {}, {}
    for a, b in zip(areas, bins):
        total[b] = total.get(b, 0.0) + a
        biggest[b] = max(biggest.get(b, 0.0), a)
    return {b: max(eps * total[b], 2.0 * biggest[b]) for b in total}


def initial_split(areas, bins):
    """In each bin, largest cell first, to the tier with less area."""
    side = [0] * len(areas)
    load = {}
    for i in sorted(range(len(areas)), key=lambda i: (-areas[i], i)):
        l0, l1 = load.get(bins[i], (0.0, 0.0))
        if l0 <= l1:
            side[i], l0 = 0, l0 + areas[i]
        else:
            side[i], l1 = 1, l1 + areas[i]
        load[bins[i]] = (l0, l1)
    return side


def bin_diffs(areas, bins, side):
    diff = {}
    for a, b, s in zip(areas, bins, side):
        diff[b] = diff.get(b, 0.0) + (a if s == 0 else -a)
    return diff


def cut_nets(nets, side):
    return [e for e, (cells, _) in enumerate(nets) if len({side[c] for c in cells}) == 2]


def fm_split(areas, bins, nets, side, eps=0.1, max_passes=20):
    """Fiduccia-Mattheyses with the balance checked in each bin."""
    n = len(areas)
    side = list(side)
    limit = bin_limits(areas, bins, eps)
    cell_nets = [[] for _ in range(n)]
    for e, (cells, _) in enumerate(nets):
        for c in cells:
            cell_nets[c].append(e)
    for _ in range(max_passes):
        count = [[0, 0] for _ in nets]
        for e, (cells, _) in enumerate(nets):
            for c in cells:
                count[e][side[c]] += 1
        diff = bin_diffs(areas, bins, side)
        locked = [False] * n
        moves, gains = [], []

        def gain(v):
            g, s = 0, side[v]
            for e in cell_nets[v]:
                if len(nets[e][0]) < 2:
                    continue
                if count[e][s] == 1:
                    g += 1
                if count[e][1 - s] == 0:
                    g -= 1
            return g

        while True:
            best, best_g = -1, None
            for v in range(n):  # @line L7
                if locked[v]:
                    continue
                d = diff[bins[v]] + (-2 * areas[v] if side[v] == 0 else 2 * areas[v])
                if abs(d) > limit[bins[v]] + 1e-12:
                    continue
                g = gain(v)
                if best_g is None or g > best_g:
                    best, best_g = v, g
            if best < 0:
                break
            v = best
            s = side[v]
            for e in cell_nets[v]:
                count[e][s] -= 1
                count[e][1 - s] += 1
            diff[bins[v]] += -2 * areas[v] if s == 0 else 2 * areas[v]
            side[v] = 1 - s
            locked[v] = True
            moves.append(v)
            gains.append(best_g)
        run, best_sum, best_k = 0, 0, 0
        for k, g in enumerate(gains):  # @line L8
            run += g
            if run > best_sum:
                best_sum, best_k = run, k + 1
        for v in moves[best_k:]:
            side[v] = 1 - side[v]
        if best_sum <= 0:  # @line L9
            break
    return side


def shrunk_2d(widths, heights, nets, die, k=2, eps=0.1):
    n = len(widths)
    sw, sh, snets, sdie = shrink(widths, heights, nets, die)  # @line L1
    xs, ys = quadratic_place(n, snets, sdie)  # @line L2
    areas = [w * h for w, h in zip(widths, heights)]  # @line L3
    bins = make_bins(xs, ys, sdie, k)  # @line L4
    side = initial_split(areas, bins)  # @line L5
    side = fm_split(areas, bins, snets, side, eps)  # @line L6
    mivs = []
    for e in cut_nets(snets, side):  # @line L10
        cells, pads = snets[e]
        px = [xs[c] for c in cells] + [p[0] for p in pads]
        py = [ys[c] for c in cells] + [p[1] for p in pads]
        mivs.append((e, (max(px) + min(px)) / 2.0, (max(py) + min(py)) / 2.0))
    return {"x": xs, "y": ys, "die": sdie, "bins": bins, "side": side, "mivs": mivs,  # @line L11
            "hpwl": hpwl(xs, ys, snets)}
