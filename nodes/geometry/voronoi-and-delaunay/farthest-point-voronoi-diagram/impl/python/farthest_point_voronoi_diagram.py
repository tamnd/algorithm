# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/farthest-point-voronoi-diagram/. The authors are listed in prov/0J56YS.jsonl.

from fractions import Fraction

Point = tuple[int, int]
FPoint = tuple[Fraction, Fraction]


def orient(a: Point, b: Point, c: Point) -> int:
    """Sign of (b - a) x (c - a): 1 for a left turn, -1 for a right turn, 0 when collinear."""
    d = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    return (d > 0) - (d < 0)


def incircle(a: Point, b: Point, c: Point, d: Point) -> int:
    """For a, b, c counterclockwise: 1 if d is strictly inside their circumcircle, 0 on it, -1 outside."""
    adx, ady = a[0] - d[0], a[1] - d[1]
    bdx, bdy = b[0] - d[0], b[1] - d[1]
    cdx, cdy = c[0] - d[0], c[1] - d[1]
    det = ((adx * adx + ady * ady) * (bdx * cdy - cdx * bdy)
           + (bdx * bdx + bdy * bdy) * (cdx * ady - adx * cdy)
           + (cdx * cdx + cdy * cdy) * (adx * bdy - bdx * ady))
    return (det > 0) - (det < 0)


def circumcenter(a: Point, b: Point, c: Point) -> FPoint:
    """Exact circumcenter of three points that are not collinear."""
    bx, by = b[0] - a[0], b[1] - a[1]
    cx, cy = c[0] - a[0], c[1] - a[1]
    d = 2 * (bx * cy - by * cx)
    return (a[0] + Fraction(cy * (bx * bx + by * by) - by * (cx * cx + cy * cy), d),
            a[1] + Fraction(bx * (cx * cx + cy * cy) - cx * (bx * bx + by * by), d))


def strict_hull(points: list[Point]) -> list[Point]:
    """Vertices of the convex hull in counterclockwise order, without points inside hull edges."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list[Point] = []
    upper: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


class FarthestPointVoronoiDiagram:
    """The farthest-point Voronoi diagram of a set of integer sites.

    Only the vertices of the convex hull have a nonempty cell. The dual triangulation of the hull vertices
    (the farthest-point Delaunay triangulation) is found by flips from a fan: an edge is flipped while the
    opposite vertex lies strictly outside the circumcircle of the triangle. Vertices are exact; edges are
    {frozenset({p, q}): (end, end)} with None for an end at infinity, as for the nearest-point diagram.
    insert marks the diagram as stale; the next query rebuilds it.
    Cost: build O(n log n + h^2) with these flips (O(n log n) with the algorithm of Shamos and Hoey or a
    randomized method); farthest(q) O(h); space O(n).
    """

    def __init__(self, points: list[Point] = ()) -> None:
        self.sites: list[Point] = []
        self.stale = True
        for p in points:
            self.insert(p)

    def insert(self, p: Point) -> bool:
        """Add the site p; return False if it is already a site."""
        if p in self.sites:
            return False
        self.sites.append(p)
        self.stale = True
        return True

    def _build(self) -> None:
        hull = strict_hull(self.sites)  # @line L1
        self.hull = hull
        self.tris: list[tuple[int, int, int]] = []
        self._edges: dict[frozenset, tuple] = {}
        h = len(hull)
        if h == 2:
            self._edges[frozenset(hull)] = (None, None)
        if h >= 3:
            edge: dict[tuple[int, int], tuple[int, int, int]] = {}
            for k in range(1, h - 1):  # @line L2
                t = (0, k, k + 1)
                edge[(0, k)] = edge[(k, k + 1)] = edge[(k + 1, 0)] = t
            stack = [e for e in edge if (e[1], e[0]) in edge]  # @line L3
            while stack:  # @line L4
                a, b = stack.pop()
                if (a, b) not in edge or (b, a) not in edge:
                    continue
                t1, t2 = edge[(a, b)], edge[(b, a)]
                c = next(v for v in t1 if v not in (a, b))
                d = next(v for v in t2 if v not in (a, b))
                if incircle(hull[a], hull[b], hull[c], hull[d]) < 0:  # @line L5
                    for x, y, z in (t1, t2):
                        del edge[(x, y)], edge[(y, z)], edge[(z, x)]
                    for t in ((a, d, c), (d, b, c)):
                        x, y, z = t
                        edge[(x, y)] = edge[(y, z)] = edge[(z, x)] = t
                    stack += [(a, d), (d, b), (b, c), (c, a)]  # @line L6
            self.tris = sorted(set(edge.values()))
            center = {t: circumcenter(hull[t[0]], hull[t[1]], hull[t[2]]) for t in self.tris}  # @line L7
            for (u, v), t in edge.items():  # @line L8
                t2 = edge.get((v, u))
                if t2 is None:
                    ends = (center[t], None)  # a ray toward the inside of the hull edge u -> v
                elif u < v and center[t] != center[t2]:
                    ends = tuple(sorted((center[t], center[t2])))
                else:
                    continue
                self._edges[frozenset((hull[u], hull[v]))] = ends
            self._vertices = sorted(set(center.values()))
        else:
            self._vertices = []
        self.stale = False

    def vertices(self) -> list[FPoint]:
        """The vertices of the diagram, sorted."""
        if self.stale:
            self._build()
        return list(self._vertices)

    def edges(self) -> dict[frozenset, tuple]:
        """The edges of positive length, keyed by the pair of sites."""
        if self.stale:
            self._build()
        return dict(self._edges)

    def sites_with_cells(self) -> list[Point]:
        """The sites with a nonempty cell: the hull vertices, counterclockwise."""
        if self.stale:
            self._build()
        return list(self.hull)

    def farthest(self, q: tuple) -> Point:
        """A site farthest from q (exact), found among the hull vertices."""
        if self.stale:
            self._build()
        return max(self.hull, key=lambda s: (s[0] - q[0]) ** 2 + (s[1] - q[1]) ** 2)
