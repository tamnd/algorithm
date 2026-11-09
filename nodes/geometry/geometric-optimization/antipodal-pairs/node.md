---
tag: MCZ09J
kind: concept
slug: antipodal-pairs
name: Antipodal pairs
aliases:
- antipodal points
- antipodal vertex pairs
- antipodal pair
area: geometry/geometric-optimization
level: core
summary: Two vertices of a convex polygon are antipodal if parallel supporting lines pass through them. A convex n-gon has at most floor(3n/2) such pairs, and rotating calipers lists them in O(n) time.
prereqs: [convex-polygon, supporting-hyperplane, orientation-test]
see_also: [rotating-calipers, polygon-diameter, polygon-width, farthest-pair, minimum-area-enclosing-rectangle, maximum-area-inscribed-triangle, minimum-width-annulus, support-function]
sources:
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 4, the diameter of a convex polygon (antipodal pairs, the bound of 3n/2 pairs, and the linear-time enumeration)
  - paper: "Michael Ian Shamos, Computational Geometry, PhD thesis, Yale University, 1978"
    locator: the diameter of a convex polygon by enumeration of antipodal pairs
  - paper: "Godfried T. Toussaint, Solving geometric problems with the rotating calipers, Proceedings of IEEE MELECON 1983, Athens"
    locator: the rotating calipers as a generator of antipodal pairs and its applications
  - paper: doi:10.1109/34.6790
    title: Michael E. Houle and Godfried T. Toussaint, Computing the width of a set, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(5), 1988
    locator: the width as the minimum over antipodal vertex and edge pairs
---

Two points of a [convex polygon](/convex-polygon/) are *antipodal* if two distinct parallel lines pass through them and the whole polygon lies between the two lines. A convex polygon with $n$ vertices has between $n$ and $\lfloor 3n/2 \rfloor$ antipodal vertex pairs, and the [rotating calipers](/rotating-calipers/) list all of them in $O(n)$ time. The farthest pair, the width, the smallest enclosing rectangle and several other extreme measures are attained at antipodal pairs, which is why so many polygon problems reduce to one walk around the polygon.

## In plain words

Hold a convex shape between the two jaws of a caliper, so that both jaws touch it. The two points where the jaws touch are a pair of opposite points. Turn the shape slowly. The touching points move from corner to corner, and each new contact gives a new pair. After half a turn the jaws have swapped places and every pair has appeared.

Each corner of the shape is touched by each jaw for a while, so the number of pairs is about the number of corners. When two sides are parallel, both jaws lie flat against a side at the same moment, and this adds extra pairs. So the count is at least the number of corners and at most one and a half times that number.

## The idea

**Notation.** $P$ is a convex polygon with vertices $p_0, \ldots, p_{n-1}$ in counterclockwise order, $n \ge 3$, with no three vertices collinear; indices are modulo $n$. A point is $p = (x, y)$, and $\mathrm{orient}(p, q, r)$ is the sign of the cross product $(q - p) \times (r - p)$. A *supporting line* of $P$ is a line that meets $P$ and has $P$ on one side.

**Definition.** Vertices $p_i \ne p_j$ are *antipodal* if there are two distinct parallel supporting lines $\ell_i \ni p_i$ and $\ell_j \ni p_j$. Equivalently, there is a unit vector $u$ with

$$\langle u, p_i \rangle = \max_k \langle u, p_k \rangle \quad\text{and}\quad \langle u, p_j \rangle = \min_k \langle u, p_k \rangle .$$

In terms of the *normal cone* $N_i = \{u : \langle u, p_i - p_k \rangle \ge 0 \text{ for all } k\}$, the closed cone between the outer normals of the two edges at $p_i$, the pair is antipodal iff $N_i \cap (-N_j) \ne \{0\}$. This gives an exact test with integer arithmetic: two cones of angle less than $\pi$ meet iff one contains a boundary ray of the other, and "the ray $v$ lies in the cone spanned by $a$ then $b$" is $a \times v \ge 0$ and $v \times b \ge 0$.

An edge and a vertex are antipodal if the line of the edge and a parallel line through the vertex support $P$; two edges are antipodal if they are parallel.

**Theorem (the number of pairs).** Let $t$ be the number of pairs of parallel edges of $P$. Then $P$ has exactly $n + t$ antipodal vertex pairs. Since each edge is parallel to at most one other edge, $t \le \lfloor n/2 \rfloor$, so the number is between $n$ and $\lfloor 3n/2 \rfloor$, and both ends are attained.

*Proof.* The cones $N_0, \ldots, N_{n-1}$ cover the circle of directions, have disjoint interiors, and each is a closed arc of angle less than $\pi$ that ends at the outer normals of two consecutive edges. The cones $-N_0, \ldots, -N_{n-1}$ do the same. So the $2n$ outer normals $\pm \nu_k$ of the edges cut the circle into arcs, and on the interior of each arc both the maximizing vertex $i$ and the minimizing vertex $j$ are constant. If $\nu_k = -\nu_m$ for parallel edges $k, m$, two cut points coincide, so there are $2n - 2t$ distinct cut points and $2n - 2t$ arcs. Each arc gives an ordered pair $(i, j)$ with $N_i \cap (-N_j)$ of positive angle. Different arcs give different ordered pairs, because $N_i \cap (-N_j)$ is a convex cone, hence one arc. The arc at $u$ and the arc at $-u$ give $(i, j)$ and $(j, i)$, so the arcs give $n - t$ unordered pairs. Other antipodal pairs have $N_i \cap (-N_j)$ equal to a single ray. A single ray in two closed arcs with disjoint interiors is a common end point, so the ray is a normal $\nu_k$ with $-\nu_k$ also a normal: a pair of parallel edges $p_a p_{a+1}$ and $p_b p_{b+1}$. At $u = \nu_k$ the maximizers are $p_a, p_{a+1}$ and the minimizers are $p_b, p_{b+1}$. Of the four cross pairs, two lie on the arcs next to the ray, and the other two (the "diagonals" of the trapezoid) meet only at the ray. So each pair of parallel edges adds exactly 2 new unordered pairs, which gives $n - t + 2t = n + t$. $\square$

**How the calipers find them.** Start with the vertex of smallest $y$ and the vertex of largest $y$, which are antipodal for $u = (0, 1)$. Rotate $u$ counterclockwise. At each step compare the angles of the next edge at the two contact vertices, with one [orientation test](/orientation-test/) of the two edge vectors, and advance the contact whose edge makes the smaller angle; if the edges are parallel, report the two diagonal pairs and advance both. Each step reports one pair, and after half a turn each contact has advanced about $n/2$ times, so the walk takes $O(n)$ time and reports each pair once. See [rotating calipers](/rotating-calipers/) for the template.

**Point sets.** For a finite point set, antipodal pairs are defined on its [convex hull](/convex-hull/). So for $n$ points the pairs come from an $O(n \log n)$ hull followed by an $O(h)$ walk, where $h$ is the number of hull vertices.

## Examples

**A pentagon with no parallel edges.** $P = (0, 0), (4, 0), (5, 3), (3, 5), (0, 4)$. Here $t = 0$, so there are $n = 5$ antipodal pairs:

$$\{(0,0),(5,3)\},\ \{(0,0),(3,5)\},\ \{(4,0),(3,5)\},\ \{(4,0),(0,4)\},\ \{(5,3),(0,4)\}.$$

The pair $(0, 0), (4, 0)$ is not antipodal: they are neighbors on one edge, and any line through one of them that supports $P$ has the other on its supporting side. The two farthest pairs, at squared distance 34, are both in the list, as the [polygon diameter](/polygon-diameter/) theorem requires.

**A hexagon with three parallel pairs.** $P = (0, 0), (4, 0), (6, 2), (6, 4), (2, 4), (0, 2)$ is centrally symmetric, so $t = 3$ and it has $6 + 3 = 9 = \lfloor 3 \cdot 6 / 2 \rfloor$ antipodal pairs, the maximum. For the horizontal pair of edges, $u = (0, 1)$ makes $(2, 4)$ and $(6, 4)$ maximal and $(0, 0)$ and $(4, 0)$ minimal, and all four cross pairs are antipodal. Just before this direction the pair is $\{(6, 4), (0, 0)\}$ and just after it is $\{(2, 4), (4, 0)\}$. The diagonal pairs $\{(0, 0), (2, 4)\}$ and $\{(4, 0), (6, 4)\}$ are antipodal only for this single direction.

**A non-example.** In a square with vertices $(0, 0), (1, 0), (1, 1), (0, 1)$, every pair of vertices is antipodal, including the neighbors $(0, 0)$ and $(1, 0)$: the vertical lines $x = 0$ and $x = 1$ support the square. This is the case $t = 2$, $n + t = 6 = \binom{4}{2}$. In a triangle every pair is antipodal and $n + t = 3$.

## Where it is used

- **[Polygon diameter](/polygon-diameter/) and [farthest pair](/farthest-pair/).** The farthest pair of a convex polygon is an antipodal pair, so the diameter takes $O(n)$ time after the hull.
- **[Polygon width](/polygon-width/).** The width is attained by an antipodal edge and vertex pair.
- **[Minimum-area enclosing rectangle](/minimum-area-enclosing-rectangle/).** Four calipers at right angles; one side lies on an edge.
- **[Maximum-area inscribed triangle](/maximum-area-inscribed-triangle/) and [minimum-width annulus](/minimum-width-annulus/).** Both use walks of the same kind.
- **Distances between two convex polygons.** The largest distance between two convex polygons and the merge of two hulls use antipodal pairs taken across the two polygons.
- **The [support function](/support-function/).** For a direction $u$, the maximizing vertex is the contact of one caliper; antipodal pairs list where the support function and its opposite change vertex.

## References
