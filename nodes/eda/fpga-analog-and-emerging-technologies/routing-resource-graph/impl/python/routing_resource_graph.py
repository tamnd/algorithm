# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/routing-resource-graph/. The authors are listed in prov/4ASKQ1.jsonl.

"""Routing resource graph of a small island-style FPGA.

The array has nx * ny logic blocks at (x, y), 1 <= x <= nx, 1 <= y <= ny.
Each block has one output pin and `pins` input pins. Each channel piece has
W tracks, and every wire segment has length 1. A node is a pin, a source, a
sink or a track segment, and each node has capacity 1. A directed edge is a
switch that can drive the head from the tail.

Node keys:
  ("SOURCE", x, y), ("OPIN", x, y), ("IPIN", x, y, p), ("SINK", x, y, p),
  ("CHANX", x, y, t) for 1 <= x <= nx, 0 <= y <= ny (above row y),
  ("CHANY", x, y, t) for 0 <= x <= nx, 1 <= y <= ny (right of column x).
"""

from collections import deque
from typing import Optional

# The four sides of a switch block, and its six pairs of sides.
PAIRS = [("T", "R"), ("T", "B"), ("T", "L"), ("R", "B"), ("R", "L"), ("B", "L")]


def track_map(pattern: str, a: str, b: str, t: int, w: int) -> int:
    """Track on side b that the switch block joins to track t on side a.

    (a, b) is one of PAIRS. Each map is a permutation of range(w).
    """
    if pattern == "subset":
        return t
    if pattern == "universal":
        # Pairs of tracks {2q, 2q + 1}; the turns T-R and B-L swap inside a pair.
        if (a, b) in (("T", "R"), ("B", "L")) and t < 2 * (w // 2):
            return t ^ 1
        return t
    if pattern == "turning":
        # An illustrative pattern in which turns change the track.
        if (a, b) in (("T", "B"), ("R", "L")):
            return t
        if (a, b) in (("T", "R"), ("B", "L")):
            return (t + 1) % w
        return w - 1 - t
    raise ValueError("unknown pattern " + pattern)


class RoutingResourceGraph:
    """A directed graph of the routing resources, built once, then read."""

    def __init__(
        self,
        nx: int,
        ny: int,
        w: int,
        pins: int,
        fc_in: int,
        fc_out: int,
        pattern: str = "universal",
    ) -> None:
        if not (1 <= fc_in <= w and 1 <= fc_out <= w):
            raise ValueError("need 1 <= fc <= W")
        self.nx, self.ny, self.w, self.pins = nx, ny, w, pins
        self.fc_in, self.fc_out, self.pattern = fc_in, fc_out, pattern
        self.keys: list[tuple] = []
        self.index: dict[tuple, int] = {}
        self.out: list[list[int]] = []
        self._build()

    # Building blocks.

    def _add_node(self, key: tuple) -> int:
        self.index[key] = len(self.keys)
        self.keys.append(key)
        self.out.append([])
        return self.index[key]

    def _add_edge(self, a: tuple, b: tuple) -> None:
        self.out[self.index[a]].append(self.index[b])

    def _side_channel(self, x: int, y: int, side: int, t: int) -> tuple:
        """Track t of the channel piece on side 0 top, 1 right, 2 bottom, 3 left of block (x, y)."""
        if side == 0:
            return ("CHANX", x, y, t)
        if side == 1:
            return ("CHANY", x, y, t)
        if side == 2:
            return ("CHANX", x, y - 1, t)
        return ("CHANY", x - 1, y, t)

    def _sb_sides(self, i: int, j: int) -> dict[str, tuple]:
        """The channel pieces that meet at switch block (i, j), by side, as key prefixes."""
        sides = {}
        if j + 1 <= self.ny:
            sides["T"] = ("CHANY", i, j + 1)
        if j >= 1:
            sides["B"] = ("CHANY", i, j)
        if i >= 1:
            sides["L"] = ("CHANX", i, j)
        if i + 1 <= self.nx:
            sides["R"] = ("CHANX", i + 1, j)
        return sides

    def _build(self) -> None:
        nx, ny, w, pins = self.nx, self.ny, self.w, self.pins
        blocks = [(x, y) for y in range(1, ny + 1) for x in range(1, nx + 1)]
        for x, y in blocks:  # @line L1
            self._add_node(("SOURCE", x, y))
            self._add_node(("OPIN", x, y))
            self._add_edge(("SOURCE", x, y), ("OPIN", x, y))
            for p in range(pins):
                self._add_node(("IPIN", x, y, p))
                self._add_node(("SINK", x, y, p))
                self._add_edge(("IPIN", x, y, p), ("SINK", x, y, p))
        for t in range(w):  # @line L2
            for y in range(ny + 1):
                for x in range(1, nx + 1):
                    self._add_node(("CHANX", x, y, t))
            for x in range(nx + 1):
                for y in range(1, ny + 1):
                    self._add_node(("CHANY", x, y, t))
        for x, y in blocks:  # @line L3
            for side in range(4):
                for t in range(self.fc_out):
                    self._add_edge(("OPIN", x, y), self._side_channel(x, y, side, t))
        for x, y in blocks:  # @line L4
            for p in range(pins):
                for j in range(self.fc_in):
                    t = (p + j) % w
                    self._add_edge(self._side_channel(x, y, p % 4, t), ("IPIN", x, y, p))
        for i in range(nx + 1):  # @line L5
            for j in range(ny + 1):
                sides = self._sb_sides(i, j)
                for a, b in PAIRS:
                    if a in sides and b in sides:
                        for t in range(w):
                            u = sides[a] + (t,)
                            v = sides[b] + (track_map(self.pattern, a, b, t, w),)
                            self._add_edge(u, v)
                            self._add_edge(v, u)

    # Queries.

    def num_nodes(self) -> int:
        return len(self.keys)

    def num_edges(self) -> int:
        return sum(len(o) for o in self.out)

    def node(self, key: tuple) -> int:
        return self.index[key]

    def edges(self) -> set[tuple[int, int]]:
        return {(u, v) for u in range(len(self.out)) for v in self.out[u]}

    def check_invariant(self) -> None:
        """Raise AssertionError if the graph breaks the rules of its node kinds."""
        allowed = {
            "SOURCE": {"OPIN"},
            "OPIN": {"CHANX", "CHANY"},
            "CHANX": {"CHANX", "CHANY", "IPIN"},
            "CHANY": {"CHANX", "CHANY", "IPIN"},
            "IPIN": {"SINK"},
            "SINK": set(),
        }
        es = self.edges()
        assert len(es) == self.num_edges(), "parallel edge"
        for u, v in es:
            ku, kv = self.keys[u][0], self.keys[v][0]
            assert kv in allowed[ku], (self.keys[u], self.keys[v])
            if ku in ("CHANX", "CHANY") and kv in ("CHANX", "CHANY"):
                assert (v, u) in es, "a switch between tracks must work both ways"
        for k, i in self.index.items():
            assert self.keys[i] == k

    # Routing of one net on the graph.

    def route_net(
        self, source: int, sinks: list[int], used: set[int]
    ) -> Optional[tuple[set[int], list[tuple[int, int]]]]:
        """Grow a tree from source to every sink through nodes not in used.

        Returns (nodes, edges) of the tree, or None when some sink cannot be
        reached. The caller adds the nodes to used to reserve them.
        """
        if source in used:
            return None
        tree = {source}  # @line L6
        tree_edges: list[tuple[int, int]] = []
        for k in sinks:  # @line L7
            if k in tree:
                continue
            pred: dict[int, int] = {}
            seen = set(tree)
            queue = deque(sorted(tree))
            found = False
            while queue and not found:  # @line L8
                u = queue.popleft()
                for v in self.out[u]:
                    if v in seen or v in used:
                        continue
                    seen.add(v)
                    pred[v] = u
                    if v == k:
                        found = True
                        break
                    queue.append(v)
            if not found:  # @line L9
                return None
            v = k  # @line L10
            while v not in tree:
                u = pred[v]
                tree_edges.append((u, v))
                tree.add(v)
                v = u
        return tree, tree_edges  # @line L11

    def route_all(
        self, nets: list[tuple[int, list[int]]]
    ) -> list[Optional[tuple[set[int], list[tuple[int, int]]]]]:
        """Route the nets one after the other; a net that fails gets None."""
        used: set[int] = set()
        result = []
        for source, sinks in nets:
            r = self.route_net(source, sinks, used)
            if r is not None:
                used |= r[0]
            result.append(r)
        return result


def expected_counts(nx: int, ny: int, w: int, pins: int, fc_in: int, fc_out: int) -> tuple[int, int]:
    """Closed forms for the number of nodes and of directed edges."""
    nb = nx * ny
    segments = w * (nx * (ny + 1) + ny * (nx + 1))
    nodes = nb * (2 + 2 * pins) + segments
    sb = 0
    for i in range(nx + 1):
        for j in range(ny + 1):
            s = (i >= 1) + (i <= nx - 1) + (j >= 1) + (j <= ny - 1)
            sb += w * s * (s - 1)
    edges = nb * (1 + pins) + nb * 4 * fc_out + nb * pins * fc_in + sb
    return nodes, edges
