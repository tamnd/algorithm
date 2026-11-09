# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/quad-edge-data-structure/. The authors are listed in prov/77AC3G.jsonl.
"""The quad-edge data structure of Guibas and Stolfi.

Every undirected edge is a group of four directed edges e = 4q + r, r in 0..3.
r = 0 and r = 2 are the two directions of the primal edge, r = 1 and r = 3 are
the two directions of the dual edge. Each directed edge stores its Onext link
(the next edge counterclockwise around its origin) and its origin data.
"""


class QuadEdge:
    def __init__(self):
        self.nxt = []      # Onext of every directed edge
        self.data = []     # origin vertex of primal edges (None for dual ones)
        self.alive = []    # one flag per quad-edge

    # ---- the edge algebra --------------------------------------------------
    @staticmethod
    def rot(e):
        return (e & ~3) | ((e + 1) & 3)  # @line L1

    @staticmethod
    def sym(e):
        return e ^ 2  # @line L1

    @staticmethod
    def rot_inv(e):
        return (e & ~3) | ((e + 3) & 3)  # @line L1

    def onext(self, e):
        return self.nxt[e]  # @line L2

    def oprev(self, e):
        return self.rot(self.nxt[self.rot(e)])  # @line L2

    def lnext(self, e):
        return self.rot(self.nxt[self.rot_inv(e)])  # @line L2

    def rnext(self, e):
        return self.rot_inv(self.nxt[self.rot(e)])

    def dnext(self, e):
        return self.sym(self.nxt[self.sym(e)])

    def org(self, e):
        return self.data[e]

    def dest(self, e):
        return self.data[self.sym(e)]

    # ---- the two primitives ------------------------------------------------
    def make_edge(self, a=None, b=None):
        q = len(self.alive)  # @line L3
        e = 4 * q
        self.nxt.extend([e, e + 3, e + 2, e + 1])  # @line L4
        self.data.extend([a, None, b, None])
        self.alive.append(True)
        return e  # @line L5

    def splice(self, a, b):
        alpha = self.rot(self.nxt[a])  # @line L6
        beta = self.rot(self.nxt[b])
        self.nxt[a], self.nxt[b] = self.nxt[b], self.nxt[a]  # @line L7
        self.nxt[alpha], self.nxt[beta] = self.nxt[beta], self.nxt[alpha]  # @line L8

    # ---- derived operations ------------------------------------------------
    def connect(self, a, b):
        """New edge from Dest(a) to Org(b), inside the face left of a and b."""
        e = self.make_edge(self.dest(a), self.org(b))  # @line L9
        self.splice(e, self.lnext(a))  # @line L10
        self.splice(self.sym(e), b)  # @line L11
        return e

    def delete_edge(self, e):
        self.splice(e, self.oprev(e))  # @line L12
        self.splice(self.sym(e), self.oprev(self.sym(e)))  # @line L13
        self.alive[e >> 2] = False

    def flip(self, e):
        """Replace e, the diagonal of the two faces at it, by the other diagonal."""
        a = self.oprev(e)  # @line L14
        b = self.oprev(self.sym(e))
        self.splice(e, a)  # @line L15
        self.splice(self.sym(e), b)
        self.splice(e, self.lnext(a))  # @line L16
        self.splice(self.sym(e), self.lnext(b))
        self.data[e] = self.dest(a)  # @line L17
        self.data[self.sym(e)] = self.dest(b)

    # ---- traversal ---------------------------------------------------------
    def edges(self):
        """One directed primal edge per live quad-edge."""
        return [4 * q for q, ok in enumerate(self.alive) if ok]

    def faces(self):
        """The faces as lists of directed edges, each face traced by Lnext."""
        seen = set()
        out = []
        for q, ok in enumerate(self.alive):
            if not ok:
                continue
            for e in (4 * q, 4 * q + 2):
                if e in seen:
                    continue
                cycle = []
                f = e
                while f not in seen:  # @line L18
                    seen.add(f)
                    cycle.append(f)
                    f = self.lnext(f)
                out.append(cycle)
        return out

    def vertex_ring(self, e):
        """The directed edges with the same origin as e, counterclockwise."""
        ring = [e]
        f = self.nxt[e]
        while f != e:
            ring.append(f)
            f = self.nxt[f]
        return ring


def polygon(qe, points):
    """Build the boundary cycle of a polygon given counterclockwise.

    Returns the directed edge from points[0] to points[1]; the polygon interior
    is the face to its left.
    """
    n = len(points)
    first = qe.make_edge(points[0], points[1])
    last = first
    for i in range(1, n - 1):
        e = qe.make_edge(points[i], points[i + 1])
        qe.splice(qe.sym(last), e)
        last = e
    qe.connect(last, first)
    return first


def fan(qe, base):
    """Triangulate the convex face left of base by diagonals from Org(base)."""
    b = base
    while qe.lnext(qe.lnext(qe.lnext(b))) != b:
        e = qe.connect(qe.lnext(b), b)
        b = qe.sym(e)
    return base


def insert_in_face(qe, e, p):
    """Join a new vertex p, inside the face left of e, to every corner of it.

    The face must be star-shaped from p, for example a triangle containing p.
    Returns the new edge from Org(e) to p.
    """
    base = qe.make_edge(qe.org(e), p)
    qe.splice(base, e)
    start = base
    while True:
        base = qe.connect(e, qe.sym(base))
        e = qe.oprev(base)
        if qe.lnext(e) == start:
            return start
