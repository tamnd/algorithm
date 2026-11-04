# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/kd-b-tree/. The authors are listed in prov/TMRMPW.jsonl.

from typing import Optional

INF = float("inf")
Point = tuple[int, int]
Vec = tuple[float, float]


class Page:
    """A page of the tree with the region [lo, hi), half-open on each axis.

    A point page (leaf) has children None and holds points. A region page has
    a list of child pages whose regions partition its own region.
    """

    __slots__ = ("lo", "hi", "points", "children")

    def __init__(self, lo: Vec, hi: Vec, children: Optional[list["Page"]] = None) -> None:
        self.lo, self.hi = lo, hi
        self.points: list[Point] = []
        self.children = children

    def holds(self, p: Point) -> bool:
        return all(self.lo[a] <= p[a] < self.hi[a] for a in range(2))

    def meets(self, lo: Point, hi: Point) -> bool:
        """Whether the region meets the closed box [lo, hi]."""
        return all(self.lo[a] <= hi[a] and lo[a] < self.hi[a] for a in range(2))


def _with(v: Vec, a: int, x: float) -> Vec:
    return (x, v[1]) if a == 0 else (v[0], x)


def split_page(u: Page, a: int, v: float) -> tuple[Page, Page]:
    """Cut the page u by the line x_a = v, which crosses its region, into two pages.

    The children that cross the line are cut too, down to the point pages:
    these are the forced splits of the k-d-B tree.
    """
    left = Page(u.lo, _with(u.hi, a, v))
    right = Page(_with(u.lo, a, v), u.hi)
    if u.children is None:
        left.points = [p for p in u.points if p[a] < v]
        right.points = [p for p in u.points if p[a] >= v]
        return left, right
    left.children, right.children = [], []
    for c in u.children:
        if c.hi[a] <= v:
            left.children.append(c)
        elif c.lo[a] >= v:
            right.children.append(c)
        else:
            cl, cr = split_page(c, a, v)
            left.children.append(cl)
            right.children.append(cr)
    return left, right


class KdBTree:
    """A two-dimensional k-d-B tree with B points per point page and M entries per region page.

    Invariant: the regions of the children of a region page partition its
    region, each point lies in the region of its point page, every point page
    is at the same depth, point pages hold at most B points, and region pages
    hold between 1 and M children. Pages may be underfull, even empty.
    """

    def __init__(self, leaf_capacity: int = 2, fanout: int = 3) -> None:
        if leaf_capacity < 1 or fanout < 2:
            raise ValueError("need leaf_capacity >= 1 and fanout >= 2")
        self.B, self.M = leaf_capacity, fanout
        self.root = Page((-INF, -INF), (INF, INF))
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def _path(self, p: Point) -> list[Page]:
        path = [self.root]
        while path[-1].children is not None:
            path.append(next(c for c in path[-1].children if c.holds(p)))  # type: ignore[union-attr]
        return path

    def __contains__(self, p: Point) -> bool:
        return (int(p[0]), int(p[1])) in self._path(p)[-1].points

    def _leaf_plane(self, u: Page) -> tuple[int, float]:
        """A line through the median of the distinct coordinates on the axis of larger spread."""
        best = None
        for a in range(2):
            d = sorted({p[a] for p in u.points})
            if len(d) >= 2:
                key = (-(d[-1] - d[0]), a)
                if best is None or key < best[0]:
                    best = (key, a, d[len(d) // 2])
        assert best is not None, "a full page of distinct points differs on some axis"
        return best[1], best[2]

    def _region_plane(self, u: Page) -> tuple[int, float]:
        """The line at a child boundary that balances the halves, then cuts the fewest children."""
        kids = u.children or []
        best = None
        for a in range(2):
            for v in sorted({c.lo[a] for c in kids if c.lo[a] > u.lo[a]}):
                left = sum(1 for c in kids if c.lo[a] < v)
                right = sum(1 for c in kids if c.hi[a] > v)
                if left <= self.M and right <= self.M:
                    key = (max(left, right), left + right, a, v)
                    if best is None or key < best:
                        best = key
        assert best is not None, "a guillotine partition always has a cut that splits no child"
        return best[2], best[3]

    def insert(self, p: Point) -> bool:
        """Add p. Returns False if p was stored."""
        p = (int(p[0]), int(p[1]))
        path = self._path(p)  # @line L1
        leaf = path[-1]
        if p in leaf.points:
            return False
        leaf.points.append(p)  # @line L2
        self.size += 1
        i = len(path) - 1
        while i >= 0:  # @line L3
            u = path[i]
            full = len(u.points) > self.B if u.children is None else len(u.children) > self.M
            if not full:  # @line L4
                break
            a, v = self._leaf_plane(u) if u.children is None else self._region_plane(u)  # @line L5
            left, right = split_page(u, a, v)  # @line L6
            if i == 0:  # @line L7
                self.root = Page((-INF, -INF), (INF, INF), [left, right])
                break
            parent = path[i - 1]
            k = parent.children.index(u)  # type: ignore[union-attr]
            parent.children[k : k + 1] = [left, right]  # type: ignore[index]  # @line L8
            i -= 1  # @line L9
        return True

    def delete(self, p: Point) -> bool:
        """Remove p from its point page. Pages are not merged."""
        p = (int(p[0]), int(p[1]))
        leaf = self._path(p)[-1]  # @line L14
        if p not in leaf.points:
            return False
        leaf.points.remove(p)  # @line L15
        self.size -= 1
        return True

    def range_search(self, lo: Point, hi: Point) -> list[Point]:
        """The points in the closed box [lo, hi]."""
        out: list[Point] = []
        stack = [self.root]
        while stack:  # @line L10
            u = stack.pop()
            if not u.meets(lo, hi):  # @line L11
                continue
            if u.children is None:  # @line L12
                out.extend(q for q in u.points if lo[0] <= q[0] <= hi[0] and lo[1] <= q[1] <= hi[1])
            else:
                stack.extend(u.children)  # @line L13
        return out

    def height(self) -> int:
        h, u = 0, self.root
        while u.children is not None:
            u, h = u.children[0], h + 1
        return h

    def leaves(self) -> list[Page]:
        out, stack = [], [self.root]
        while stack:
            u = stack.pop()
            if u.children is None:
                out.append(u)
            else:
                stack.extend(reversed(u.children))
        return out

    def points(self) -> list[Point]:
        return [q for leaf in self.leaves() for q in leaf.points]

    def check_invariant(self) -> None:
        assert self.root.lo == (-INF, -INF) and self.root.hi == (INF, INF)
        depths: set[int] = set()
        total = 0
        stack: list[tuple[Page, int]] = [(self.root, 0)]
        while stack:
            u, d = stack.pop()
            assert all(u.lo[a] < u.hi[a] for a in range(2)), "empty region"
            if u.children is None:
                depths.add(d)
                assert len(u.points) <= self.B, "point page overflow"
                assert all(u.holds(q) for q in u.points), "point outside its page"
                total += len(u.points)
                continue
            assert 1 <= len(u.children) <= self.M, "region page has a wrong size"
            area_ok = True
            for c in u.children:
                assert all(u.lo[a] <= c.lo[a] and c.hi[a] <= u.hi[a] for a in range(2)), "child outside"
                stack.append((c, d + 1))
            kids = u.children
            for i in range(len(kids)):
                for j in range(i + 1, len(kids)):
                    x, y = kids[i], kids[j]
                    overlap = all(max(x.lo[a], y.lo[a]) < min(x.hi[a], y.hi[a]) for a in range(2))
                    assert not overlap, "child regions overlap"
            # cover: the lower left corner of each cell of the grid of child boundaries lies in one child
            xs = sorted({c.lo[0] for c in kids} | {c.hi[0] for c in kids if c.hi[0] < u.hi[0]} | {u.lo[0]})
            ys = sorted({c.lo[1] for c in kids} | {c.hi[1] for c in kids if c.hi[1] < u.hi[1]} | {u.lo[1]})
            for x in xs:
                for y in ys:
                    probe = (x if x > -INF else -(10**18), y if y > -INF else -(10**18))
                    n = sum(1 for c in kids if all(c.lo[a] <= probe[a] < c.hi[a] for a in range(2)))
                    area_ok = area_ok and n == 1
            assert area_ok, "child regions do not cover the page"
        assert len(depths) <= 1, "point pages at different depths"
        assert total == self.size == len(set(self.points())), "size is wrong"
