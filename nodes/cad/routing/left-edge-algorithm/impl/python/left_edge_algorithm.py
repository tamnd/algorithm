# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/left-edge-algorithm/. The authors are listed in prov/NN5MVW.jsonl.

"""The left-edge channel router, with the vertical constraints of the reserved two-layer model.

Each net gets one trunk on one track (no doglegs). Tracks are filled one at a
time from the top. Within a track, the nets are tried in the order of their
left ends, and a net is placed when it does not overlap the last net on the
track and all its parents in the vertical constraint graph are on higher tracks.
"""

from typing import Dict, List, Optional, Sequence, Tuple

from channel import intervals, realize, vcg_edges


def left_edge(spans: Dict[int, Tuple[int, int]], edges: Sequence[Tuple[int, int]]) -> Optional[Dict[int, int]]:
    """Assign a track (1 = top) to each net. spans maps a net to (left, right).

    edges are the vertical constraints (a, b): a must be on a higher track than b.
    Returns None when the constraints have a cycle.
    """
    parents: Dict[int, List[int]] = {x: [] for x in spans}
    for a, b in edges:
        parents[b].append(a)
    order = sorted(spans, key=lambda x: (spans[x][0], x))  # @line L1
    track: Dict[int, int] = {}
    t = 0  # @line L2
    unplaced = list(order)
    while unplaced:  # @line L3
        t += 1  # @line L4
        last = None
        now = []
        for x in unplaced:  # @line L5
            free = last is None or spans[x][0] > last
            if free and all(track.get(p, t) < t for p in parents[x]):  # @line L6
                track[x] = t  # @line L7
                last = spans[x][1]
                now.append(x)
        unplaced = [x for x in unplaced if x not in track]  # @line L8
        if not now:  # @line L9
            return None
    return track  # @line L10


def left_edge_route(top: Sequence[int], bottom: Sequence[int]):
    """Route a channel with the left-edge algorithm.

    Returns (number of tracks, track of each net, wires), or None if the
    vertical constraint graph has a cycle.
    """
    spans = intervals(top, bottom)
    track = left_edge(spans, vcg_edges(top, bottom))
    if track is None:
        return None
    t = max(track.values(), default=0)
    pieces = {x: (x, l, r) for x, (l, r) in spans.items()}
    return t, track, realize(top, bottom, pieces, track, t)


if __name__ == "__main__":
    top = [1, 0, 2, 1, 3, 0, 4, 0]
    bottom = [0, 2, 0, 3, 0, 4, 0, 3]
    print(left_edge_route(top, bottom)[:2])
