# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/liaison-graph/. The authors are listed in prov/RHWBG9.jsonl.
"""The liaison graph of an assembly of axis-aligned boxes.

A node is a part. A liaison joins two parts that share a face patch of
positive area (a contact), or two parts that the designer joins on purpose
(a fastener). A set of parts is stored as a bit mask.
"""


def contact(a, b):
    """Return (k, s, area) if boxes a and b share a planar patch of positive area.

    The boxes are (x0, y0, z0, x1, y1, z1) with disjoint interiors. The
    contact normal from a to b is s times e_k.
    """
    for k in range(3):  # @line L7
        if a[k + 3] == b[k]:  # @line L8
            s = 1
        elif b[k + 3] == a[k]:
            s = -1
        else:
            continue
        area = 1
        for m in range(3):  # @line L9
            if m == k:
                continue
            w = min(a[m + 3], b[m + 3]) - max(a[m], b[m])
            if w <= 0:
                area = 0
                break
            area *= w
        if area > 0:
            return (k, s, area)
    return None  # @line L10


class LiaisonGraph:
    def __init__(self, n):
        self.n = n
        self.adj = [0] * n          # adj[i]: bit mask of the neighbours of i
        self.label = {}             # (i, j) with i < j -> data of the liaison

    def add_liaison(self, i, j, data):
        if i == j:
            raise ValueError("a liaison joins two different parts")
        if i > j:
            i, j = j, i
        self.adj[i] |= 1 << j
        self.adj[j] |= 1 << i
        self.label[(i, j)] = data

    def neighbours(self, i):
        return [j for j in range(self.n) if self.adj[i] >> j & 1]

    def liaisons(self):
        return sorted(self.label)

    def neighbourhood(self, mask):
        """N(S): the parts outside mask that share a liaison with a part of mask."""
        out = 0
        m = mask
        while m:
            low = m & -m
            out |= self.adj[low.bit_length() - 1]
            m ^= low
        return out & ~mask

    def cut(self, mask):
        """The liaisons with exactly one end in mask."""
        return [(i, j) for (i, j) in self.liaisons()
                if (mask >> i & 1) != (mask >> j & 1)]  # @line L13

    def is_connected(self, mask):
        """True if mask is nonempty and its parts form one connected piece."""
        if mask == 0:
            return False
        reach = mask & -mask  # @line L11
        while True:
            grow = (reach | self.neighbourhood(reach)) & mask
            if grow == reach:
                return reach == mask  # @line L12
            reach = grow

    def connected_subsets(self, within=None):
        """Each connected subset of within (default: all parts) once."""
        full = (1 << self.n) - 1 if within is None else within
        out = []

        def grow(s, banned):
            out.append(s)  # @line L14
            cand = self.neighbourhood(s) & full & ~banned  # @line L15
            while cand:  # @line L16
                w = cand & -cand
                grow(s | w, banned)  # @line L17
                banned |= w
                cand ^= w

        banned = ~full  # @line L18
        m = full
        while m:  # @line L19
            v = m & -m
            grow(v, banned)  # @line L20
            banned |= v
            m ^= v
        return out


def build(boxes):
    """The contact liaisons of a list of boxes, found by a sweep along x."""
    g = LiaisonGraph(len(boxes))
    order = sorted(range(len(boxes)), key=lambda i: boxes[i][0])  # @line L1
    active = []
    for i in order:  # @line L2
        x0 = boxes[i][0]
        active = [j for j in active if boxes[j][3] >= x0]  # @line L3
        for j in active:  # @line L4
            a, b = (j, i) if j < i else (i, j)
            c = contact(boxes[a], boxes[b])
            if c is not None:  # @line L5
                g.add_liaison(a, b, ("contact",) + c)
        active.append(i)  # @line L6
    return g
