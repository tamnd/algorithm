# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/deferred-merge-embedding/. The authors are listed in prov/RDEGA7.jsonl.
"""Deferred-merge embedding (DME) for a zero-skew tree under linear delay.

The delay of a path is its wire length. Sinks are points (x, y). A topology
is a sink index or a pair of topologies. In the rotated coordinates
u = x + y, v = x - y the L1 distance is the L-infinity distance, so a merging
segment (a Manhattan arc) is an axis-parallel segment and a tilted
rectangular region (TRR) is an axis-parallel rectangle. A region is stored
as (ulo, uhi, vlo, vhi). All arithmetic is exact with Fractions.
"""

from fractions import Fraction


class Node:
    def __init__(self, kids=(), sink=None):
        self.kids = list(kids)  # child Nodes
        self.sink = sink
        self.ms = None  # merging region in (u, v)
        self.t = Fraction(0)  # delay from any point of ms to every sink below
        self.edge = Fraction(0)  # wire length from the parent to this node
        self.pt = None  # embedded point (x, y)


def rotate(p):
    return (Fraction(p[0]) + p[1], Fraction(p[0]) - p[1])


def unrotate(q):
    return ((q[0] + q[1]) / 2, (q[0] - q[1]) / 2)


def gap(a_lo, a_hi, b_lo, b_hi):
    return max(Fraction(0), b_lo - a_hi, a_lo - b_hi)


def dist(r1, r2):
    """L-infinity distance between two rectangles (L1 in the plane)."""
    return max(gap(r1[0], r1[1], r2[0], r2[1]), gap(r1[2], r1[3], r2[2], r2[3]))


def trr(r, e):
    return (r[0] - e, r[1] + e, r[2] - e, r[3] + e)


def meet(r1, r2):
    out = (max(r1[0], r2[0]), min(r1[1], r2[1]), max(r1[2], r2[2]), min(r1[3], r2[3]))
    assert out[0] <= out[1] and out[2] <= out[3]
    return out


def clamp(q, r):
    return (min(max(q[0], r[0]), r[1]), min(max(q[1], r[2]), r[3]))


def build(sinks, topo):
    if isinstance(topo, tuple):
        return Node([build(sinks, topo[0]), build(sinks, topo[1])])
    return Node(sink=topo)


def bottom_up(node, sinks):
    """Phase 1: merging regions and edge lengths, from the leaves up."""
    if node.sink is not None:  # @line L1
        u, v = rotate(sinks[node.sink])
        node.ms, node.t = (u, u, v, v), Fraction(0)  # @line L2
        return
    a, b = node.kids
    bottom_up(a, sinks)  # @line L3
    bottom_up(b, sinks)
    d = dist(a.ms, b.ms)  # @line L4
    if abs(a.t - b.t) <= d:  # @line L5
        a.edge = (d + b.t - a.t) / 2
        b.edge = d - a.edge
    elif a.t > b.t:  # @line L6
        a.edge, b.edge = Fraction(0), a.t - b.t
    else:
        a.edge, b.edge = b.t - a.t, Fraction(0)
    node.ms = meet(trr(a.ms, a.edge), trr(b.ms, b.edge))  # @line L7
    node.t = a.t + a.edge  # @line L8


def top_down(node, parent_q):
    """Phase 2: embed each node at the point of its region nearest the parent."""
    q = clamp(parent_q, node.ms)  # @line L10
    node.pt = unrotate(q)
    for k in node.kids:  # @line L11
        top_down(k, q)


def dme(sinks, topo, source=None):
    """Return the root of the embedded zero-skew tree. The root goes to the
    point of its region nearest to source (or its lowest corner)."""
    root = build(sinks, topo)
    bottom_up(root, sinks)
    start = rotate(source) if source is not None else (root.ms[0], root.ms[2])
    top_down(root, start)  # @line L9
    return root


def wirelength(node):
    return sum(k.edge + wirelength(k) for k in node.kids)


def l1(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])
