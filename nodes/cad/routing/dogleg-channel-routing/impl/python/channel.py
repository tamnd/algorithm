# SPDX-License-Identifier: MIT
# Shared helper of the rt3 cad pages of https://algorithm.tamnd.com/. The authors are listed in prov/.

"""A two-layer channel in the reserved-layer model, and a checker for routings.

A channel is given by two lists, top and bottom, of the same length n.
top[c - 1] is the net of the pin at the top of column c, and bottom[c - 1]
the net at the bottom; 0 means no pin. Columns are numbered 1 to n.

A routing in T tracks is a list of wires. Tracks are numbered 1 to T from
the top. Row 0 is the top edge of the channel and row T + 1 the bottom edge.
  ("H", net, track, c1, c2)  a trunk on layer H, on one track, from column c1 to c2
  ("V", net, column, r1, r2) a branch on layer V, in one column, from row r1 to r2
Two wires of the same net that share a grid point on the same layer are
joined. An H wire and a V wire of the same net that share a grid point are
joined by a via.
"""

from typing import Dict, List, Sequence, Tuple

Wire = Tuple[str, int, int, int, int]


def pins_of(top: Sequence[int], bottom: Sequence[int]) -> Dict[int, List[Tuple[int, str]]]:
    """Map each net to its pins (column, "T" or "B"), in column order."""
    pins: Dict[int, List[Tuple[int, str]]] = {}
    for c, (a, b) in enumerate(zip(top, bottom), start=1):
        if a:
            pins.setdefault(a, []).append((c, "T"))
        if b:
            pins.setdefault(b, []).append((c, "B"))
    return pins


def intervals(top: Sequence[int], bottom: Sequence[int]) -> Dict[int, Tuple[int, int]]:
    """Map each net to its interval (leftmost pin column, rightmost pin column)."""
    return {x: (p[0][0], p[-1][0]) for x, p in pins_of(top, bottom).items()}


def local_density(top: Sequence[int], bottom: Sequence[int], c: int) -> int:
    """Number of nets whose interval holds column c."""
    return sum(1 for l, r in intervals(top, bottom).values() if l <= c <= r)


def density(top: Sequence[int], bottom: Sequence[int]) -> int:
    """Channel density: the largest local density over all columns."""
    return max((local_density(top, bottom, c) for c in range(1, len(top) + 1)), default=0)


def vcg_edges(top: Sequence[int], bottom: Sequence[int]) -> List[Tuple[int, int]]:
    """Edges (a, b) of the vertical constraint graph: a is on top and b at the bottom of a column."""
    edges = set()
    for a, b in zip(top, bottom):
        if a and b and a != b:
            edges.add((a, b))
    return sorted(edges)


def realize(top: Sequence[int], bottom: Sequence[int], pieces: Dict[object, Tuple[int, int, int]],
            track: Dict[object, int], ntracks: int) -> List[Wire]:
    """Turn a track for each piece (net, left column, right column) into wires.

    A piece is a trunk. At each pin column c of a net, one branch runs from the
    pin to every track of the pieces of that net whose interval holds c.
    """
    wires: List[Wire] = []
    for p, (net, l, r) in pieces.items():
        wires.append(("H", net, track[p], l, r))
    for net, pins in pins_of(top, bottom).items():
        for c, side in pins:
            rows = [track[p] for p, (x, l, r) in pieces.items() if x == net and l <= c <= r]
            rows.append(0 if side == "T" else ntracks + 1)
            wires.append(("V", net, c, min(rows), max(rows)))
    return wires


def check_routing(top: Sequence[int], bottom: Sequence[int], ntracks: int, wires: Sequence[Wire],
                  extra_columns: int = 0) -> List[str]:
    """Return a list of problems with the routing. An empty list means a legal routing.

    Checks: every wire is inside the channel; no grid point of a layer holds two
    nets (no short); the edge rows are touched only at the pins of the same net;
    each pin is reached; the wires and pins of each net are connected.
    """
    n = len(top)
    last_col = n + extra_columns
    probs: List[str] = []
    owner: Dict[Tuple[str, int, int], int] = {}
    cells: Dict[Tuple[str, int, int], List[int]] = {}
    for i, (layer, net, a, b, c) in enumerate(wires):
        if layer == "H":
            t, c1, c2 = a, min(b, c), max(b, c)
            if not 1 <= t <= ntracks or c1 < 1 or c2 > last_col:
                probs.append(f"wire {i} leaves the channel")
                continue
            pts = [("H", x, t) for x in range(c1, c2 + 1)]
        else:
            col, r1, r2 = a, min(b, c), max(b, c)
            if not 1 <= col <= last_col or r1 < 0 or r2 > ntracks + 1:
                probs.append(f"wire {i} leaves the channel")
                continue
            pts = [("V", col, y) for y in range(r1, r2 + 1)]
        for pt in pts:
            if pt in owner and owner[pt] != net:
                probs.append(f"short between nets {owner[pt]} and {net} at {pt}")
            owner.setdefault(pt, net)
            cells.setdefault(pt, []).append(i)
    pins = pins_of(top, bottom)
    pin_points = {}
    for net, ps in pins.items():
        for c, side in ps:
            pin_points[("V", c, 0 if side == "T" else ntracks + 1)] = net
    for pt, net in owner.items():
        if pt[0] == "V" and pt[2] in (0, ntracks + 1) and pin_points.get(pt) != net:
            probs.append(f"net {net} touches the channel edge at {pt} without a pin")
    for pt, net in pin_points.items():
        if owner.get(pt) != net:
            probs.append(f"pin of net {net} at {pt} is not reached")
    if probs:
        return probs
    parent = list(range(len(wires)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        parent[find(x)] = find(y)

    for pt, ws in cells.items():
        for w in ws[1:]:
            union(ws[0], w)
        if pt[0] == "H":
            other = cells.get(("V", pt[1], pt[2]))
            if other and owner[("V", pt[1], pt[2])] == owner[pt]:
                union(ws[0], other[0])
    for net, ps in pins.items():
        roots = {find(cells[pt][0]) for pt, x in pin_points.items() if x == net}
        if len(roots) != 1:
            probs.append(f"net {net} is not connected")
    return probs


def tracks_used(wires: Sequence[Wire]) -> int:
    """The largest track number used by an H wire."""
    return max((w[2] for w in wires if w[0] == "H"), default=0)
