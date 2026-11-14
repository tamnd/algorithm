# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/multilevel-hypergraph-partitioning/. The authors are listed in prov/FYFXXW.jsonl.

import random
from fractions import Fraction
from typing import Optional, Sequence


def cut_weight(nets: Sequence[Sequence[int]], netw: Sequence[int], side: Sequence[int]) -> int:
    """Total weight of the nets with pins on both sides."""
    return sum(w for e, w in zip(nets, netw) if len({side[v] for v in e}) == 2)


def fm_refine(
    n: int,
    nets: Sequence[Sequence[int]],
    netw: Sequence[int],
    vw: Sequence[int],
    side: Sequence[int],
    lo: int,
    hi: int,
) -> list[int]:
    """Fiduccia-Mattheyses passes with vertex weights and net weights.

    The weight of side 0 stays in [lo, hi] at every step. Each pass moves
    every free vertex at most once, always the free vertex of largest gain
    whose move keeps the balance (ties: the smaller number), and then keeps
    the best prefix. Passes repeat while the best prefix has positive gain.
    The vertex of largest gain is found by a scan, and each move scans the
    pins of its nets, so a pass costs O(n^2 + sum of |e|^2 over the nets),
    instead of O(n + P) for P pins with the gain buckets of FM.
    """
    side = list(side)
    vnets: list[list[int]] = [[] for _ in range(n)]
    for i, e in enumerate(nets):
        for v in e:
            vnets[v].append(i)
    while True:
        cnt = [[0, 0] for _ in nets]
        for i, e in enumerate(nets):
            for v in e:
                cnt[i][side[v]] += 1
        gain = [0] * n
        for v in range(n):
            s = side[v]
            for i in vnets[v]:
                if cnt[i][s] == 1:
                    gain[v] += netw[i]
                if cnt[i][1 - s] == 0:
                    gain[v] -= netw[i]
        locked = [False] * n
        w0 = sum(vw[v] for v in range(n) if side[v] == 0)
        moves: list[int] = []
        total, best_total, best_k = 0, 0, 0
        while True:
            pick = -1
            for v in range(n):
                if locked[v]:
                    continue
                nw0 = w0 - vw[v] if side[v] == 0 else w0 + vw[v]
                if lo <= nw0 <= hi and (pick < 0 or gain[v] > gain[pick]):
                    pick = v
            if pick < 0:
                break
            v, f = pick, side[pick]
            t = 1 - f
            locked[v] = True
            for i in vnets[v]:
                e, w = nets[i], netw[i]
                if cnt[i][t] == 0:
                    for u in e:
                        if not locked[u]:
                            gain[u] += w
                elif cnt[i][t] == 1:
                    for u in e:
                        if side[u] == t and not locked[u]:
                            gain[u] -= w
                cnt[i][f] -= 1
                cnt[i][t] += 1
                if cnt[i][f] == 0:
                    for u in e:
                        if not locked[u]:
                            gain[u] -= w
                elif cnt[i][f] == 1:
                    for u in e:
                        if side[u] == f and u != v and not locked[u]:
                            gain[u] += w
            total += gain[v]
            side[v] = t
            w0 += -vw[v] if f == 0 else vw[v]
            moves.append(v)
            if total > best_total:
                best_total, best_k = total, len(moves)
        for v in moves[best_k:]:
            side[v] = 1 - side[v]
        if best_total <= 0:
            return side


def coarsen(
    n: int,
    nets: Sequence[Sequence[int]],
    netw: Sequence[int],
    vw: Sequence[int],
    cap: int,
    rng: random.Random,
    scheme: str = "hec",
    side: Optional[Sequence[int]] = None,
) -> tuple[list[int], int, list[list[int]], list[int], list[int]]:
    """One coarsening level by hyperedge coarsening ("hec") or edge coarsening ("ec").

    hec visits the nets in order of non-increasing weight, then non-decreasing
    size, with random order among ties, and merges all pins of a net if none
    of them is merged yet. ec visits the vertices in random order and merges
    each unmerged vertex with the unmerged vertex that shares the largest sum
    of w(e)/(|e| - 1) over common nets. No coarse vertex weighs more than cap.
    If side is given, only vertices on the same side merge (restricted
    coarsening for V-cycles). Coarse nets are the images of the nets; nets
    with one coarse pin are dropped and equal coarse nets are merged with
    their weights added.

    Returns (cmap, k, coarse nets, coarse net weights, coarse vertex weights).
    """
    cmap = [-1] * n
    k = 0
    if scheme == "hec":
        order = list(range(len(nets)))
        rng.shuffle(order)
        order.sort(key=lambda i: (-netw[i], len(nets[i])))
        for i in order:
            e = nets[i]
            if len(e) < 2 or any(cmap[v] >= 0 for v in e):
                continue
            if sum(vw[v] for v in e) > cap:
                continue
            if side is not None and len({side[v] for v in e}) > 1:
                continue
            for v in e:
                cmap[v] = k
            k += 1
    elif scheme == "ec":
        vnets: list[list[int]] = [[] for _ in range(n)]
        for i, e in enumerate(nets):
            for v in e:
                vnets[v].append(i)
        order = list(range(n))
        rng.shuffle(order)
        for v in order:
            if cmap[v] >= 0:
                continue
            score: dict[int, Fraction] = {}
            for i in vnets[v]:
                e = nets[i]
                for u in e:
                    if u == v or cmap[u] >= 0 or vw[u] + vw[v] > cap:
                        continue
                    if side is not None and side[u] != side[v]:
                        continue
                    score[u] = score.get(u, Fraction(0)) + Fraction(netw[i], len(e) - 1)
            if score:
                u = max(score, key=lambda u: (score[u], -u))
                cmap[u] = k
            cmap[v] = k
            k += 1
    else:
        raise ValueError("scheme must be 'hec' or 'ec'")
    for v in range(n):
        if cmap[v] < 0:
            cmap[v] = k
            k += 1
    merged: dict[tuple[int, ...], int] = {}
    for e, w in zip(nets, netw):
        ce = tuple(sorted({cmap[v] for v in e}))
        if len(ce) >= 2:
            merged[ce] = merged.get(ce, 0) + w
    cvw = [0] * k
    for v in range(n):
        cvw[cmap[v]] += vw[v]
    return cmap, k, [list(e) for e in merged], list(merged.values()), cvw


def _greedy_fill(k: int, cvw: Sequence[int], lo: int, hi: int, rng: random.Random) -> list[int]:
    """Random greedy bisection: add vertices to side 0 in random order until its weight reaches lo."""
    order = list(range(k))
    rng.shuffle(order)
    side, w0 = [1] * k, 0
    for v in order:
        if w0 >= lo:
            break
        if w0 + cvw[v] <= hi:
            side[v] = 0
            w0 += cvw[v]
    return side


def _down_and_up(
    n: int,
    nets: list[list[int]],
    netw: list[int],
    vw: list[int],
    lo: int,
    hi: int,
    cap: int,
    coarsest: int,
    rng: random.Random,
    scheme: str,
    trials: int,
    side: Optional[list[int]],
) -> list[int]:
    levels = []  # (cmap, graph of the finer level)
    cur = (n, nets, netw, vw)
    while cur[0] > coarsest:  # @line L2
        cmap, k, cn, cw, cv = coarsen(*cur, cap, rng, scheme, side)  # @line L3
        if k == cur[0]:
            break
        levels.append((cmap, cur))
        cur = (k, cn, cw, cv)
        if side is not None:
            proj = [0] * k
            for v, c in enumerate(cmap):
                proj[c] = side[v]
            side = proj
        if k > 0.9 * levels[-1][1][0]:  # @line L4
            break
    k, cn, cw, cv = cur
    if side is None:
        best, best_cut = None, None
        for _ in range(max(1, trials)):  # @line L5
            s = fm_refine(k, cn, cw, cv, _greedy_fill(k, cv, lo, hi, rng), lo, hi)  # @line L6
            c = cut_weight(cn, cw, s)
            if best_cut is None or c < best_cut:
                best, best_cut = s, c
        side = best  # @line L7
    else:
        side = fm_refine(k, cn, cw, cv, side, lo, hi)
    for cmap, (fn, fnets, fnetw, fvw) in reversed(levels):  # @line L8
        side = [side[cmap[v]] for v in range(fn)]  # @line L9
        side = fm_refine(fn, fnets, fnetw, fvw, side, lo, hi)  # @line L10
    return side


def multilevel_hypergraph_partitioning(
    n: int,
    nets: Sequence[Sequence[int]],
    lo: int,
    hi: int,
    rng: random.Random,
    netw: Optional[Sequence[int]] = None,
    vw: Optional[Sequence[int]] = None,
    scheme: str = "hec",
    coarsest: int = 8,
    trials: int = 4,
    vcycles: int = 1,
    cap: Optional[int] = None,
) -> list[int]:
    """Bisect a hypergraph by the multilevel scheme of hMETIS.

    Vertices are 0 .. n-1 with weights vw (default 1), nets are lists of
    distinct vertices with weights netw (default 1). The weight of side 0 must
    end in [lo, hi]. Coarsening stops at coarsest vertices, or when a level
    removes less than a tenth of the vertices. The coarsest hypergraph gets
    trials random greedy bisections, each refined by FM, and the best is
    projected back with FM refinement at each level. Then vcycles V-cycles
    coarsen again inside the two sides and refine on the way up. Coarse
    vertices weigh at most cap, by default max(1, hi - lo), so that a
    balanced start always exists.

    Returns side[v] in {0, 1}. Cost: O(P log P) per coarsening level by hec
    (O(sum of |e|^2) by ec), and O(n_l^2 + sum of |e|^2) per FM pass on a
    level with n_l vertices.
    """
    netw = [1] * len(nets) if netw is None else list(netw)
    vw = [1] * n if vw is None else list(vw)
    if not 0 <= lo <= hi <= sum(vw):
        raise ValueError("need 0 <= lo <= hi <= total vertex weight")
    if cap is None:
        cap = max(1, hi - lo)
    if cap > hi - lo + 1 or max(vw, default=0) > cap:
        raise ValueError("need max vertex weight <= cap <= hi - lo + 1")
    net_list = [sorted(set(e)) for e in nets]  # @line L1
    side = _down_and_up(n, net_list, netw, vw, lo, hi, cap, coarsest, rng, scheme, trials, None)
    for _ in range(vcycles):  # @line L11
        side = _down_and_up(n, net_list, netw, vw, lo, hi, cap, coarsest, rng, scheme, trials, side)  # @line L12
    return side  # @line L13
