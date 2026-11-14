# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/corner-stitching/. The authors are listed in prov/452WNT.jsonl.
"""Corner stitching (Ousterhout 1984) on a bounded world with integer coordinates.

The world is the half-open rectangle [X0, X1) x [Y0, Y1). It is cut into
half-open tiles [x0, x1) x [y0, y1), and every point of the world lies in
exactly one tile. A tile is solid or space. Space tiles are kept in the
canonical form of maximal horizontal strips:

  (H) no two space tiles share a vertical edge, and
  (V) no two space tiles with the same x-span share a horizontal edge.

Each tile has four stitches, defined by the point that the target tile
contains (e is a small positive number):

  bl: the tile that contains (x0, y0 - e)   (bottom neighbour at the left end)
  lb: the tile that contains (x0 - e, y0)   (left neighbour at the bottom end)
  tr: the tile that contains (x1 - e, y1)   (top neighbour at the right end)
  rt: the tile that contains (x1, y1 - e)   (right neighbour at the top end)

A stitch that would leave the world is None. Ousterhout stores only the
lower left corner of a tile and reads x1 and y1 from rt and tr. This code
stores all four coordinates, which is simpler to read and changes no
algorithm.
"""


class Tile:
    __slots__ = ("x0", "y0", "x1", "y1", "solid", "bl", "lb", "tr", "rt", "alive")

    def __init__(self, x0, y0, x1, y1, solid=False):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.solid = solid
        self.bl = self.lb = self.tr = self.rt = None
        self.alive = True

    def rect(self):
        return (self.x0, self.y0, self.x1, self.y1)

    def __repr__(self):
        kind = "solid" if self.solid else "space"
        return f"Tile({self.x0}, {self.y0}, {self.x1}, {self.y1}, {kind})"


def _space(t):
    return t is not None and not t.solid


class Plane:
    """A corner stitched plane over the world [x0, x1) x [y0, y1)."""

    def __init__(self, x0, y0, x1, y1):
        if not (x0 < x1 and y0 < y1):
            raise ValueError("empty world")
        t = Tile(x0, y0, x1, y1)
        self.world = (x0, y0, x1, y1)
        self.tiles = {t}
        self.hint = t

    # ------------------------------------------------------------ neighbours

    def top_neighbors(self, t):
        """Tiles that touch the top edge of t, from right to left."""
        out, u = [], t.tr
        while u is not None and u.x1 > t.x0:
            out.append(u)
            u = u.lb
        return out

    def right_neighbors(self, t):
        """Tiles that touch the right edge of t, from top to bottom."""
        out, u = [], t.rt
        while u is not None and u.y1 > t.y0:
            out.append(u)
            u = u.bl
        return out

    def bottom_neighbors(self, t):
        """Tiles that touch the bottom edge of t, from left to right."""
        out, u = [], t.bl
        while u is not None and u.x0 < t.x1:
            out.append(u)
            u = u.rt
        return out

    def left_neighbors(self, t):
        """Tiles that touch the left edge of t, from bottom to top."""
        out, u = [], t.lb
        while u is not None and u.y0 < t.y1:
            out.append(u)
            u = u.tr
        return out

    # ------------------------------------------------------------ point find

    def point_find(self, x, y, start=None):
        """The tile that contains the point (x, y), by walking the stitches."""
        X0, Y0, X1, Y1 = self.world
        if not (X0 <= x < X1 and Y0 <= y < Y1):
            raise ValueError("point outside the world")
        t = start if start is not None and start.alive else self.hint
        while True:  # @line L1
            while y < t.y0:  # @line L2
                t = t.bl
            while y >= t.y1:  # @line L3
                t = t.tr
            if x < t.x0:  # @line L4
                t = t.lb
            elif x >= t.x1:  # @line L5
                t = t.rt
            else:  # @line L6
                self.hint = t
                return t

    # ------------------------------------------------------------ area search

    def area_search(self, ax0, ay0, ax1, ay1):
        """A solid tile that meets the area [ax0, ax1) x [ay0, ay1), or None."""
        t = self.point_find(ax0, ay1 - 1)  # @line A1
        while True:
            if t.solid:  # @line A2
                return t
            if t.x1 < ax1:  # @line A3
                return self.point_find(t.x1, min(t.y1, ay1) - 1, t)
            if t.y0 <= ay0:  # @line A4
                return None
            t = self.point_find(ax0, t.y0 - 1, t)  # @line A5

    def enumerate_area(self, ax0, ay0, ax1, ay1):
        """Every tile that meets the area, each once, with no marks."""
        out = []
        t = self.point_find(ax0, ay1 - 1)  # @line E1
        while True:
            stack = [t]  # @line E2
            while stack:
                u = stack.pop()
                out.append(u)  # @line E6
                if u.x1 >= ax1:  # @line E7
                    continue
                w = u.rt  # @line E8
                low = max(u.y0, ay0)
                while w is not None and w.y1 > low:
                    if w.y0 < ay1 and max(w.y0, ay0) >= u.y0:  # @line E9
                        stack.append(w)
                    w = w.bl
            if t.y0 <= ay0:  # @line E3
                return out
            t = self.point_find(ax0, t.y0 - 1, t)  # @line E4

    # ------------------------------------------------------------ split and merge

    def _split_h(self, t, y):
        """Cut t at height y. t keeps the lower part; the upper part is returned."""
        top = t.y1
        u = Tile(t.x0, y, t.x1, top, t.solid)
        u.tr, u.rt, u.bl = t.tr, t.rt, t
        w = t.lb
        while w is not None and w.y1 <= y:
            w = w.tr
        u.lb = w
        w = t.rt
        while w is not None and w.y0 >= y:
            w.lb = u  # right neighbours above the cut
            w = w.bl
        t_rt = w
        w = t.tr
        while w is not None and w.x1 > t.x0:
            if w.bl is t:
                w.bl = u
            w = w.lb
        w = u.lb
        while w is not None and w.y0 < top:
            if w.rt is t:
                w.rt = u
            w = w.tr
        t.tr, t.rt, t.y1 = u, t_rt, y
        self.tiles.add(u)
        return u

    def _split_v(self, t, x):
        """Cut t at abscissa x. t keeps the left part; the right part is returned."""
        right = t.x1
        u = Tile(x, t.y0, right, t.y1, t.solid)
        u.rt, u.tr, u.lb = t.rt, t.tr, t
        w = t.bl
        while w is not None and w.x1 <= x:
            w = w.rt
        u.bl = w
        w = t.tr
        while w is not None and w.x0 >= x:
            w.bl = u  # top neighbours right of the cut
            w = w.lb
        t_tr = w
        w = t.rt
        while w is not None and w.y1 > t.y0:
            if w.lb is t:
                w.lb = u
            w = w.bl
        w = u.bl
        while w is not None and w.x0 < right:
            if w.tr is t:
                w.tr = u
            w = w.rt
        t.rt, t.tr, t.x1 = u, t_tr, x
        self.tiles.add(u)
        return u

    def _merge_v(self, lo, hi):
        """Join hi, which lies on lo with the same x-span, into lo."""
        w = hi.tr
        while w is not None and w.x1 > hi.x0:
            if w.bl is hi:
                w.bl = lo
            w = w.lb
        w = hi.rt
        while w is not None and w.y1 > hi.y0:
            if w.lb is hi:
                w.lb = lo
            w = w.bl
        w = hi.lb
        while w is not None and w.y0 < hi.y1:
            if w.rt is hi:
                w.rt = lo
            w = w.tr
        lo.tr, lo.rt, lo.y1 = hi.tr, hi.rt, hi.y1
        self._kill(hi)

    def _merge_h(self, le, ri):
        """Join ri, right of le with the same y-span, into le."""
        w = ri.tr
        while w is not None and w.x1 > ri.x0:
            if w.bl is ri:
                w.bl = le
            w = w.lb
        w = ri.bl
        while w is not None and w.x0 < ri.x1:
            if w.tr is ri:
                w.tr = le
            w = w.rt
        w = ri.rt
        while w is not None and w.y1 > ri.y0:
            if w.lb is ri:
                w.lb = le
            w = w.bl
        le.rt, le.tr, le.x1 = ri.rt, ri.tr, ri.x1
        self._kill(ri)

    def _kill(self, t):
        t.alive = False
        self.tiles.discard(t)
        if self.hint is t:
            self.hint = next(iter(self.tiles))

    def _settle(self, t):
        """Merge the space tile t with space tiles of the same x-span above and below."""
        while t.alive and not t.solid:
            u = t.tr
            if _space(u) and u.x0 == t.x0 and u.x1 == t.x1:
                self._merge_v(t, u)
                continue
            d = t.bl
            if _space(d) and d.x0 == t.x0 and d.x1 == t.x1:
                self._merge_v(d, t)
                t = d
                continue
            return

    # ------------------------------------------------------------ insert and delete

    def insert(self, ax0, ay0, ax1, ay1):
        """Make the area, which must be all space, one new solid tile."""
        X0, Y0, X1, Y1 = self.world
        if not (X0 <= ax0 < ax1 <= X1 and Y0 <= ay0 < ay1 <= Y1):
            raise ValueError("bad rectangle")
        if self.area_search(ax0, ay0, ax1, ay1) is not None:  # @line I1
            raise ValueError("area is not empty")
        t = self.point_find(ax0, ay1 - 1)  # @line I2
        if t.y1 > ay1:
            self._split_h(t, ay1)
        t = self.point_find(ax0, ay0)  # @line I3
        if t.y0 < ay0:
            self._split_h(t, ay0)
        column, t = [], self.point_find(ax0, ay1 - 1)  # @line I4
        while True:
            column.append(t)
            if t.y0 <= ay0:
                break
            t = self.point_find(ax0, t.y0 - 1, t)
        sides, middles = [], []
        for s in column:  # @line I5
            if s.x0 < ax0:
                m = self._split_v(s, ax0)
                sides.append(s)
            else:
                m = s
            if m.x1 > ax1:
                sides.append(self._split_v(m, ax1))
            m.solid = True
            middles.append(m)
        new = middles[-1]  # @line I6
        for m in reversed(middles[:-1]):
            self._merge_v(new, m)
        for s in sides:  # @line I7
            self._settle(s)
        self.hint = new
        return new

    def delete(self, d):
        """Turn the solid tile d into space and restore the canonical form."""
        if not (d.alive and d.solid):
            raise ValueError("not a live solid tile")
        d.solid = False  # @line D1
        c, top = d.y0, d.y1
        for w in self.left_neighbors(d) + self.right_neighbors(d):  # @line D2
            if not w.solid:
                if w.y0 < c:
                    w = self._split_h(w, c)
                if w.y1 > top:
                    self._split_h(w, top)
        cuts = set()  # @line D3
        for w in self.left_neighbors(d) + self.right_neighbors(d):
            if not w.solid:
                cuts.update(h for h in (w.y0, w.y1) if c < h < top)
        cuts = sorted(cuts)
        pieces, t = [], d  # @line D4
        for h in cuts:
            u = self._split_h(t, h)
            pieces.append(t)
            t = u
        pieces.append(t)
        side = []  # @line D5
        for p in pieces:
            for w in self.left_neighbors(p) + self.right_neighbors(p):
                if not w.solid and w not in side:
                    side.append(w)
        for w in side:
            for h in cuts:
                if w.y0 < h < w.y1:
                    w = self._split_h(w, h)
        rows = []
        for p in pieces:  # @line D6
            le = p.lb
            if _space(le) and le.y0 == p.y0 and le.y1 == p.y1:
                self._merge_h(le, p)
                p = le
            ri = p.rt
            if _space(ri) and ri.y0 == p.y0 and ri.y1 == p.y1:
                self._merge_h(p, ri)
            rows.append(p)
        for p in rows:  # @line D7
            self._settle(p)
