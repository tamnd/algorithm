# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/min-cut-placement/. The authors are listed in prov/S0NJTB.jsonl.

import random
from collections import deque
from fractions import Fraction
from typing import Sequence

Point = tuple[int, int]


def hpwl(pos: Sequence[Point], nets: Sequence[Sequence[int]]) -> int:
    """Total half-perimeter wirelength; pins sit at the cell or pad position (no pin offsets)."""
    total = 0
    for e in nets:
        xs = [pos[p][0] for p in e]
        ys = [pos[p][1] for p in e]
        total += max(xs) - min(xs) + max(ys) - min(ys)
    return total


def fm_with_fixed(
    k: int,
    nets: Sequence[Sequence[int]],
    fixed: dict[int, int],
    side: Sequence[int],
    lo: int,
    hi: int,
) -> list[int]:
    """Fiduccia-Mattheyses passes on vertices 0 .. k-1 plus fixed vertices.

    fixed maps the extra vertex ids (k and up) to their side; they never move
    and do not count for the balance. A tentative move may take the number of
    free vertices on side 0 one step outside [lo, hi], but only a prefix that
    ends inside [lo, hi] is applied, so exact balance (lo = hi) still allows
    swaps. The vertex of largest gain is found by a scan.
    """
    total = k + len(fixed)
    side = list(side) + [0] * len(fixed)
    for v, s in fixed.items():
        side[v] = s
    vnets: list[list[int]] = [[] for _ in range(total)]
    for i, e in enumerate(nets):
        for v in e:
            vnets[v].append(i)
    while True:
        cnt = [[0, 0] for _ in nets]
        for i, e in enumerate(nets):
            for v in e:
                cnt[i][side[v]] += 1
        gain = [0] * total
        for v in range(k):
            s = side[v]
            for i in vnets[v]:
                gain[v] += (cnt[i][s] == 1) - (cnt[i][1 - s] == 0)
        locked = [False] * k + [True] * len(fixed)
        c0 = sum(1 for v in range(k) if side[v] == 0)
        moves: list[int] = []
        run, best_run, best_k = 0, 0, 0
        while True:
            pick = -1
            for v in range(k):
                if locked[v]:
                    continue
                nc0 = c0 - 1 if side[v] == 0 else c0 + 1
                if lo - 1 <= nc0 <= hi + 1 and (pick < 0 or gain[v] > gain[pick]):
                    pick = v
            if pick < 0:
                break
            v, f = pick, side[pick]
            t = 1 - f
            locked[v] = True
            for i in vnets[v]:
                e = nets[i]
                if cnt[i][t] == 0:
                    for u in e:
                        if not locked[u]:
                            gain[u] += 1
                elif cnt[i][t] == 1:
                    for u in e:
                        if side[u] == t and not locked[u]:
                            gain[u] -= 1
                cnt[i][f] -= 1
                cnt[i][t] += 1
                if cnt[i][f] == 0:
                    for u in e:
                        if not locked[u]:
                            gain[u] -= 1
                elif cnt[i][f] == 1:
                    for u in e:
                        if side[u] == f and u != v and not locked[u]:
                            gain[u] += 1
            run += gain[v]
            side[v] = t
            c0 += -1 if f == 0 else 1
            moves.append(v)
            if lo <= c0 <= hi and run > best_run:
                best_run, best_k = run, len(moves)
        for v in moves[best_k:]:
            side[v] = 1 - side[v]
        if best_run <= 0:
            return side[:k]


def min_cut_placement(
    n: int,
    nets: Sequence[Sequence[int]],
    pads: Sequence[Point],
    width: int,
    height: int,
    rng: random.Random,
    terminal_propagation: bool = True,
) -> list[Point]:
    """Place n unit cells on the sites (x, y), 0 <= x < width, 0 <= y < height.

    Pin ids 0 .. n-1 are cells and n + j is the fixed pad at pads[j]. Regions
    are cut in breadth-first order across their longer side, through the
    middle, and the cells of each region are bisected by FM in proportion to
    the site counts, within one cell. With terminal propagation, every net
    with pins outside the region gets a fixed terminal on the side of the cut
    where those pins are (pads at their position, other cells at the center
    of their current region); a net with outside pins on both sides is always
    cut and is left out, and pins exactly on the cut line are ignored.

    Returns the site of each cell. Cost: at most ceil(log2 width) +
    ceil(log2 height) levels of regions; building the subnetlists of a level
    costs O(sum of |e|^2 over the nets), and an FM pass in a region of k
    cells costs O(k^2 + sum of |e|^2 over its nets) with the scan.
    """
    if n > width * height:
        raise ValueError("more cells than sites")
    est: list[tuple[Fraction, Fraction]] = [(Fraction(width - 1, 2), Fraction(height - 1, 2))] * n
    pos: list[Point] = [(-1, -1)] * n
    pin_nets: list[list[int]] = [[] for _ in range(n)]
    for i, e in enumerate(nets):
        for p in e:
            if p < n:
                pin_nets[p].append(i)
    queue = deque([(0, width, 0, height, list(range(n)))])  # @line L1
    while queue:  # @line L2
        x0, x1, y0, y1, cells = queue.popleft()  # @line L3
        if not cells:
            continue
        if x1 - x0 == 1 and y1 - y0 == 1:  # @line L4
            pos[cells[0]] = (x0, y0)
            continue
        vertical = x1 - x0 >= y1 - y0  # @line L5
        if vertical:
            xm = x0 + (x1 - x0) // 2
            line = Fraction(2 * xm - 1, 2)
            sub = [(x0, xm, y0, y1), (xm, x1, y0, y1)]
        else:
            ym = y0 + (y1 - y0) // 2
            line = Fraction(2 * ym - 1, 2)
            sub = [(x0, x1, y0, ym), (x0, x1, ym, y1)]
        caps = [(b[1] - b[0]) * (b[3] - b[2]) for b in sub]
        local = {c: j for j, c in enumerate(cells)}
        k = len(cells)
        fixed: dict[int, int] = {}
        sub_nets: list[list[int]] = []
        seen: set[int] = set()
        for c in cells:  # @line L6
            for i in pin_nets[c]:
                if i in seen:
                    continue
                seen.add(i)
                inner = sorted({local[p] for p in nets[i] if p < n and p in local})
                if terminal_propagation:
                    sides = set()
                    for p in nets[i]:
                        if p < n and p in local:
                            continue
                        q = (Fraction(pads[p - n][0]), Fraction(pads[p - n][1])) if p >= n else est[p]
                        coord = q[0] if vertical else q[1]
                        if coord != line:
                            sides.add(0 if coord < line else 1)
                    if len(sides) == 2:
                        continue
                    if sides:
                        s = sides.pop()
                        term = k + s
                        fixed[term] = s
                        inner.append(term)
                if len(inner) >= 2:
                    sub_nets.append(inner)
        # The two terminal ids k and k + 1 must both exist for fm_with_fixed.
        fixed.setdefault(k, 0)
        fixed.setdefault(k + 1, 1)
        t = round(Fraction(k * caps[0], caps[0] + caps[1]))  # @line L7
        lo, hi = max(k - caps[1], t - 1, 0), min(caps[0], t + 1, k)
        start = [0] * t + [1] * (k - t)
        rng.shuffle(start)
        side = fm_with_fixed(k, sub_nets, fixed, start, lo, hi)  # @line L8
        for s in (0, 1):  # @line L9
            group = [cells[j] for j in range(k) if side[j] == s]
            bx0, bx1, by0, by1 = sub[s]
            for c in group:
                est[c] = (Fraction(bx0 + bx1 - 1, 2), Fraction(by0 + by1 - 1, 2))
            queue.append((bx0, bx1, by0, by1, group))
    return pos  # @line L10
