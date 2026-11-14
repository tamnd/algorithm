# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/greedy-channel-router/. The authors are listed in prov/N38E4M.jsonl.

"""A greedy channel router after Rivest and Fiduccia, in the reserved two-layer model.

The router scans the channel one column at a time, from left to right. In
each column it brings the pins into the channel, joins the tracks of nets
that are split over two or more tracks, moves nets toward the side of their
next pin, and frees the track of each net that is finished. A net may
change track in any column (a jog). If a net is still split after the last
column, the router goes on in extension columns to the right of the channel.

This is the version of the page. Range reduction is left out, and a pin
that cannot enter gets a new track at the edge of its own side.
"""

from typing import Dict, List, Optional, Sequence, Tuple

from channel import density, pins_of

TOP, BOTTOM = "T", "B"


def greedy_route(top: Sequence[int], bottom: Sequence[int]):
    """Route a channel. Returns (number of tracks, wires, number of extension columns)."""
    n = len(top)
    pins = pins_of(top, bottom)
    order: List[int] = list(range(density(top, bottom)))  # @line L1
    next_id = len(order)
    occ: Dict[int, Optional[int]] = {t: None for t in order}
    start: Dict[int, int] = {}
    h_wires: List[Tuple[int, int, int, int]] = []  # (net, track id, c1, c2)
    v_wires: List[Tuple[int, int, object, object]] = []  # (net, column, end, end); an end is a track id, TOP or BOTTOM

    def new_track(side: str) -> int:
        nonlocal next_id
        t = next_id
        next_id += 1
        if side == TOP:
            order.insert(0, t)
        else:
            order.append(t)
        occ[t] = None
        return t

    def free(t: int, c: int) -> None:
        h_wires.append((occ[t], t, start[t], c))
        occ[t] = None

    def next_pin(x: int, c: int) -> Optional[str]:
        later = [s for col, s in pins[x] if col > c]
        if not later:
            return None
        first = min(col for col, s in pins[x] if col > c)
        sides = [s for col, s in pins[x] if col == first]
        return TOP if TOP in sides else BOTTOM

    def tracks_of(x: int) -> List[int]:
        return [t for t in order if occ[t] == x]

    c = 1
    while c <= n or any(v is not None for v in occ.values()):  # @line L2
        a = top[c - 1] if c <= n else 0
        b = bottom[c - 1] if c <= n else 0
        # Step 1: bring the pins in.  @line L3
        i = next((t for t in order if occ[t] in (None, a)), None) if a else None
        j = next((t for t in reversed(order) if occ[t] in (None, b)), None) if b else None
        if a and b and a != b:
            if i is not None and j is not None and order.index(i) < order.index(j):
                pass
            else:
                up = order.index(i) + 1 if i is not None else len(order) + 2
                down = len(order) - order.index(j) if j is not None else len(order) + 2
                if up <= down and i is not None:
                    j = None
                elif j is not None:
                    i = None
        if a and i is None:
            i = new_track(TOP)
        if b and j is None:
            j = new_track(BOTTOM)
        for x, t, end in ((a, i, TOP), (b, j, BOTTOM)):
            if x:
                if occ[t] is None:
                    occ[t], start[t] = x, c
                v_wires.append((x, c, end, t))
        pos = {t: k for k, t in enumerate(order)}
        used: List[Tuple[int, int, int]] = []  # V use in this column: (low position, high position, net)
        if a:
            used.append((-1, pos[i], a))
        if b:
            used.append((pos[j], len(order), b))

        def clear(lo: int, hi: int, x: int) -> bool:
            return all(y == x or h < lo or hi < l for l, h, y in used)

        # Step 2: join split nets, shortest jog first.  @line L4
        jogs = []
        for x in sorted({v for v in occ.values() if v is not None}):
            ts = tracks_of(x)
            for p, q in zip(ts, ts[1:]):
                jogs.append((pos[q] - pos[p], pos[p], x, p, q))
        group = {t: t for t in order}

        def find(t: int) -> int:
            while group[t] != t:
                t = group[t]
            return t

        for _, _, x, p, q in sorted(jogs):
            if clear(pos[p], pos[q], x):
                used.append((pos[p], pos[q], x))
                v_wires.append((x, c, p, q))
                group[find(p)] = find(q)
        just_freed = set()
        for x in sorted({v for v in occ.values() if v is not None}):
            sets: Dict[int, List[int]] = {}
            for t in tracks_of(x):
                sets.setdefault(find(t), []).append(t)
            side = next_pin(x, c)
            for ts in sets.values():
                keep = ts[-1] if side == BOTTOM else ts[0]
                for t in ts:
                    if t != keep:
                        free(t, c)
                        just_freed.add(t)
        # Step 4: move nets toward the side of their next pin.  @line L5
        for x in sorted({v for v in occ.values() if v is not None}):
            ts = tracks_of(x)
            side = next_pin(x, c)
            if len(ts) != 1 or side is None:
                continue
            p = ts[0]
            step = -1 if side == TOP else 1
            best = None
            k = pos[p] + step
            while 0 <= k < len(order) and clear(min(k, pos[p]), max(k, pos[p]), x):
                t = order[k]
                if occ[t] is None and t not in just_freed and t not in (i, j):
                    best = t
                k += step
            if best is not None:
                used.append((min(pos[p], pos[best]), max(pos[p], pos[best]), x))
                v_wires.append((x, c, p, best))
                occ[best], start[best] = x, c
                free(p, c)
                just_freed.add(p)
        # Step 5: free the track of each finished net.  @line L6
        for x in sorted({v for v in occ.values() if v is not None}):
            ts = tracks_of(x)
            if len(ts) == 1 and next_pin(x, c) is None:
                free(ts[0], c)
        c += 1  # @line L7
    last_col = c - 1
    used_ids = [t for t in order if any(w[1] == t for w in h_wires)]  # @line L8
    row = {t: k + 1 for k, t in enumerate(used_ids)}
    T = len(used_ids)

    def to_row(end) -> int:
        if end == TOP:
            return 0
        if end == BOTTOM:
            return T + 1
        return row[end]

    wires = [("H", x, row[t], c1, c2) for x, t, c1, c2 in h_wires]
    wires += [("V", x, col, to_row(e1), to_row(e2)) for x, col, e1, e2 in v_wires]
    return T, wires, max(0, last_col - n)  # @line L9


if __name__ == "__main__":
    print(greedy_route([1, 2], [2, 1]))
