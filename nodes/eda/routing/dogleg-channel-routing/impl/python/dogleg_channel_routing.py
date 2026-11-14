# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dogleg-channel-routing/. The authors are listed in prov/SJ43AX.jsonl.

"""The dogleg channel router in the reserved two-layer model.

Each net is cut at its pin columns into pieces, called subnets. A net with
pins in k distinct columns gives k - 1 pieces, and two pieces of the same net
meet at a pin column. Each piece is a trunk on one track, so a net can change
track (a dogleg) at a pin column. The pieces are placed with the left-edge
rule, under the vertical constraints between pieces.
"""

from typing import Dict, List, Optional, Sequence, Tuple

from channel import pins_of, realize

Piece = Tuple[int, int]  # (net, index of the piece within the net)


def split_nets(top: Sequence[int], bottom: Sequence[int]) -> Dict[Piece, Tuple[int, int, int]]:
    """Cut each net at its pin columns. Returns piece -> (net, left column, right column)."""
    pieces: Dict[Piece, Tuple[int, int, int]] = {}
    for net, pins in pins_of(top, bottom).items():
        cols = sorted({c for c, _ in pins})
        for i in range(len(cols) - 1):
            pieces[(net, i)] = (net, cols[i], cols[i + 1])
    return pieces


def piece_vcg(top: Sequence[int], bottom: Sequence[int],
              pieces: Dict[Piece, Tuple[int, int, int]]) -> List[Tuple[Piece, Piece]]:
    """Edges (p, q): in some column, net(p) has the top pin, net(q) the bottom pin, and both pieces hold the column."""
    edges = set()
    for c, (a, b) in enumerate(zip(top, bottom), start=1):
        if a and b and a != b:
            above = [p for p, (x, l, r) in pieces.items() if x == a and l <= c <= r]
            below = [q for q, (x, l, r) in pieces.items() if x == b and l <= c <= r]
            for p in above:
                for q in below:
                    edges.add((p, q))
    return sorted(edges)


def left_edge_pieces(pieces: Dict[Piece, Tuple[int, int, int]],
                     edges: Sequence[Tuple[Piece, Piece]]) -> Optional[Dict[Piece, int]]:
    """Constrained left-edge on pieces. Two pieces of the same net may meet at a column on one track."""
    parents: Dict[Piece, List[Piece]] = {p: [] for p in pieces}
    for p, q in edges:
        parents[q].append(p)
    order = sorted(pieces, key=lambda p: (pieces[p][1], p))  # @line L1
    track: Dict[Piece, int] = {}
    t = 0  # @line L2
    unplaced = list(order)
    while unplaced:  # @line L3
        t += 1  # @line L4
        last, last_net = None, None
        now = []
        for p in unplaced:  # @line L5
            net, l, r = pieces[p]
            free = last is None or l > last or (l == last and net == last_net)
            if free and all(track.get(u, t) < t for u in parents[p]):  # @line L6
                track[p] = t  # @line L7
                last, last_net = r, net
                now.append(p)
        unplaced = [p for p in unplaced if p not in track]  # @line L8
        if not now:  # @line L9
            return None
    return track  # @line L10


def dogleg_route(top: Sequence[int], bottom: Sequence[int]):
    """Route a channel with doglegs at pin columns.

    Returns (number of tracks, track of each piece, wires), or None if the
    vertical constraints between pieces have a cycle.
    """
    pieces = split_nets(top, bottom)
    track = left_edge_pieces(pieces, piece_vcg(top, bottom, pieces))
    if track is None:
        return None
    t = max(track.values(), default=0)
    return t, track, realize(top, bottom, pieces, track, t)


if __name__ == "__main__":
    print(dogleg_route([1, 1, 2], [2, 0, 1])[:2])
