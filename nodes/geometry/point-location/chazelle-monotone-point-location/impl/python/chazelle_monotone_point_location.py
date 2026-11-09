# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/chazelle-monotone-point-location/. The authors are listed in prov/VJCF98.jsonl.

"""Point location in a monotone subdivision: the chain method with fractional cascading.

Input: the segments of a regular planar straight-line graph. Segments meet only at shared end
points. All comparisons of points use the lexicographic order, which is the x-order after the
symbolic shear (x, y) -> (x + eps y, y); so no two vertices share an x and no edge is vertical.
Regular means: every vertex other than the first and the last has an edge to a smaller vertex
and an edge to a larger vertex.

Build:
  1. Order the edges at each vertex from bottom to top, trace the faces, and number the f
     bounded faces 1 .. f in a topological order of the relation "directly below". Chain j is
     the upper boundary of the faces 1 .. j together with the outer part below the graph. An
     edge with face a below it and face b above it (0 and f + 1 for the outer face) is in the
     chains lo(e) = a .. hi(e) = b - 1.
  2. Chain j is node j + 1 of an implicit balanced search tree on the keys 1 .. 2^k - 1. Edge e
     is stored once, at the node of its range with the most trailing zeros, which is the
     highest node of the range in the tree.
  3. Fractional cascading: the augmented list A(m) of a node holds its own edges and every
     second element of the augmented lists of its children, with a pointer from each element to
     its own predecessor (nat) and to its place in each child list (down).

Query: one binary search in A(root), then one or two steps per level down the tree.

A query returns one of
    ("vertex", p)                q is the vertex p
    ("edge", i)                  q is in the relative interior of segment i
    ("face", above, below)       the segments directly above and below q (None if there is none)
"""

import heapq
from bisect import bisect_left
from functools import cmp_to_key

Point = tuple[int, int]


def orient(p: Point, q: Point, r: Point) -> int:
    """Twice the signed area of p, q, r: positive for a counterclockwise turn."""
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def normalize(s):
    a, b = s
    return (a, b) if a < b else (b, a)


def top_node(lo: int, hi: int) -> int:
    """The key in [lo, hi] (keys >= 1) with the most trailing zeros."""
    h = ((lo - 1) ^ hi).bit_length() - 1
    return (hi >> h) << h


class MonotoneLocator:
    def __init__(self, segments) -> None:
        segs = [normalize(s) for s in segments]
        self.segs = segs
        verts = sorted({p for s in segs for p in s})
        if not segs:
            raise ValueError("no segments")
        self.vertices = set(verts)
        out = {v: [] for v in verts}
        inn = {v: [] for v in verts}
        for i, (a, b) in enumerate(segs):
            out[a].append(i)
            inn[b].append(i)
        first, last = verts[0], verts[-1]
        for v in verts[1:-1]:
            if not out[v] or not inn[v]:
                raise ValueError("the graph is not regular at %r" % (v,))
        self.first, self.last = first, last

        def below_out(v):
            # two edges leaving v to the right: i is below j if j turns counterclockwise from i
            return cmp_to_key(lambda i, j: 0 if i == j else (-1 if orient(v, segs[i][1], segs[j][1]) > 0 else 1))

        def below_in(v):
            return cmp_to_key(lambda i, j: 0 if i == j else (-1 if orient(v, segs[i][0], segs[j][0]) < 0 else 1))

        for v in verts:
            out[v].sort(key=below_out(v))
            inn[v].sort(key=below_in(v))

        # step 1: the faces, a bottom-to-top order of the faces, and the chain ranges
        ccw = {v: [segs[i][1] for i in out[v]] + [segs[i][0] for i in reversed(inn[v])] for v in verts}
        where = {v: {u: k for k, u in enumerate(ccw[v])} for v in verts}
        face = {}
        nfaces = 0
        for a, b in segs:  # @line L1
            for h in ((a, b), (b, a)):
                if h in face:
                    continue
                while h not in face:  # trace the face on the left of the half-edge h
                    face[h] = nfaces
                    u, v = h
                    around = ccw[v]
                    h = (v, around[where[v][u] - 1])  # the next edge clockwise from u around v
                nfaces += 1
        outer = face[(segs[out[first][0]][1], first)]  # left of the reversed lowest edge at v_1
        lower_face = [face[(b, a)] for a, b in segs]
        upper_face = [face[(a, b)] for a, b in segs]
        f = nfaces - 1  # bounded faces
        succ = [[] for _ in range(nfaces)]
        indeg = [0] * nfaces
        leftmost = [None] * nfaces
        for i, (a, b) in enumerate(segs):
            dn, up = lower_face[i], upper_face[i]
            for x in (dn, up):
                if leftmost[x] is None or a < leftmost[x]:
                    leftmost[x] = a
            if dn != outer and up != outer:
                if dn == up:
                    raise RuntimeError("an edge with one bounded face on both sides")
                succ[dn].append(up)
                indeg[up] += 1
        index = [0] * nfaces
        ready = [(leftmost[x], x) for x in range(nfaces) if x != outer and indeg[x] == 0]
        heapq.heapify(ready)
        count = 0
        while ready:  # @line L2
            _, x = heapq.heappop(ready)
            count += 1
            index[x] = count  # faces 1 .. f from bottom to top, ties by leftmost vertex
            for y in succ[x]:
                indeg[y] -= 1
                if indeg[y] == 0:
                    heapq.heappush(ready, (leftmost[y], y))
        if count != f:
            raise RuntimeError("the relation below has a cycle")
        lo = [0] * len(segs)
        hi = [0] * len(segs)
        for i in range(len(segs)):  # @line L3
            lo[i] = 0 if lower_face[i] == outer else index[lower_face[i]]
            hi[i] = (f + 1 if upper_face[i] == outer else index[upper_face[i]]) - 1
        self.lo, self.hi = lo, hi
        self.weight = [hi[i] - lo[i] + 1 for i in range(len(segs))]
        self.faces = f
        self.chains = f + 1  # chain j is the upper boundary of the outer part below and faces 1 .. j

        # step 2: the implicit tree and the edge lists
        k = self.chains.bit_length()
        self.size = (1 << k) - 1
        self.root = 1 << (k - 1)
        L = [[] for _ in range(self.size + 1)]
        for i in range(len(segs)):  # @line L4
            L[top_node(lo[i] + 1, hi[i] + 1)].append(i)
        for m in range(1, self.size + 1):
            L[m].sort(key=lambda i: segs[i][0])  # the edges of one chain: disjoint x-ranges
        self.L = L
        self.Lkeys = [[segs[i][0] for i in L[m]] for m in range(self.size + 1)]

        # step 3: fractional cascading, from the leaves up
        self.A = [None] * (self.size + 1)  # keys of A(m); index 0 of the arrays below is a sentinel
        self.nat = [None] * (self.size + 1)
        self.down = [None] * (self.size + 1)  # (left pointers, right pointers)
        for level in range(k):  # @line L5
            step = 1 << level
            for m in range(step, self.size + 1, 2 * step):
                own = [(segs[i][0], 1, idx) for idx, i in enumerate(L[m])]
                kids = []
                if level > 0:
                    half = step >> 1
                    for c in (m - half, m + half):
                        kids += [(key, 0, -1) for key in self.A[c][1::2]]  # every second element
                merged = sorted(own + kids)
                keys = [key for key, _, _ in merged]
                nat = [-1]
                for key, native, idx in merged:
                    nat.append(idx if native else nat[-1])
                self.A[m] = keys
                self.nat[m] = nat
                if level > 0:
                    pointers = []
                    for c in (m - half, m + half):
                        ck = self.A[c]
                        ptr = [0]
                        j = 0
                        for key in keys:
                            while j < len(ck) and ck[j] <= key:
                                j += 1
                            ptr.append(j)  # the number of child keys <= key, the position in the child array
                        pointers.append(ptr)
                    self.down[m] = tuple(pointers)
        self.steps = 0

    def storage(self) -> int:
        """The number of entries in all augmented lists."""
        return sum(len(a) for a in self.A[1:])

    def _spanning(self, m: int, pos: int, q: Point):
        """The edge of L(m) that spans q, given the predecessor position pos in A(m)."""
        idx = self.nat[m][pos]
        if idx < 0:
            return None
        i = self.L[m][idx]
        return i if q < self.segs[i][1] else None

    def locate(self, q: Point, cascade: bool = True):
        self.steps = 0
        if q in self.vertices:
            return ("vertex", q)
        if not (self.first < q < self.last):
            return ("face", None, None)
        segs = self.segs
        m = self.root
        low_edge = high_edge = None  # the spanning edges of the chains known to be below and above q
        pos = bisect_left(self.A[m], q)  # @line L6
        while True:
            j = m - 1
            if j >= self.chains:
                above = False  # a node with no chain: everything is below it
            else:
                if cascade:
                    e = self._spanning(m, pos, q)
                else:
                    idx = bisect_left(self.Lkeys[m], q) - 1
                    e = self.L[m][idx] if idx >= 0 and q < segs[self.L[m][idx]][1] else None
                if e is None:  # @line L7
                    # the edge of chain j at q is stored higher up; it is low_edge or high_edge
                    above = low_edge is not None and self.hi[low_edge] >= j
                else:
                    a, b = segs[e]
                    o = orient(a, b, q)  # @line L8
                    self.steps += 1
                    if o == 0:
                        return ("edge", e)
                    above = o > 0
                    if above:
                        low_edge = e
                    else:
                        high_edge = e
            if m & 1:
                break
            half = (m & -m) >> 1
            child = m + half if above else m - half  # @line L9
            if cascade:
                p = self.down[m][1 if above else 0][pos]
                ck = self.A[child]
                while p < len(ck) and ck[p] < q:
                    p += 1
                    self.steps += 1
                pos = p
            m = child
        return ("face", high_edge, low_edge)
