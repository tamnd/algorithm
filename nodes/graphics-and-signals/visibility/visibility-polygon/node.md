---
tag: 7YW9NV
kind: problem
slug: visibility-polygon
name: Visibility polygon
aliases:
- star-shaped visibility polygon
- visibility region
- visibility region of a point in polygon
area: graphics-and-signals/visibility
level: core
summary: Given a polygon and a point in it, compute the region of points that the point sees. The region is a star-shaped polygon with O(n) vertices, found in O(n) time for a simple polygon.
prereqs: [simple-polygon, star-shaped-polygon]
see_also: [lee-visibility-polygon-algorithm, weak-visibility-polygon, star-shaped-polygon, polygon-kernel, art-gallery-problem, visibility-graph-of-polygon, rotational-sweep, terrain-visibility]
sources:
  - paper: doi:10.1016/0734-189X(83)90065-8
    title: D. T. Lee, Visibility of a simple polygon, Computer Vision, Graphics, and Image Processing 22(2), 1983, pages 207 to 221
    locator: the problem for a point in a simple polygon and the linear scan
  - paper: doi:10.1016/0196-6774(81)90019-5
    title: Hossam ElGindy and David Avis, A linear algorithm for computing the visibility polygon from a point, Journal of Algorithms 2(2), 1981, pages 186 to 197
    locator: the whole paper (the first linear algorithm for a point in a simple polygon)
  - paper: doi:10.1007/BF01937271
    title: Barry Joe and R. B. Simpson, Corrections to Lee's visibility polygon algorithm, BIT 27(4), 1987, pages 458 to 473
    locator: the polygons that wind around the viewpoint and the corrected linear algorithm
  - paper: doi:10.1007/BF01840436
    title: Takao Asano, Tetsuo Asano, Leonidas Guibas, John Hershberger and Hiroshi Imai, Visibility of disjoint polygons, Algorithmica 1, 1986, pages 49 to 63
    locator: the visibility polygon of a point among disjoint polygons, by an angular sweep
  - paper: doi:10.1016/S0925-7721(01)00070-0
    title: Prosenjit Bose, Anna Lubiw and J. Ian Munro, Efficient visibility queries in simple polygons, Computational Geometry 23(3), 2002, pages 313 to 335
    locator: the query version (preprocess the polygon, then report the visibility polygon of a query point)
---

The visibility polygon of a point $q$ in a polygon $P$ is the set of points of $P$ that $q$ sees, where $q$ sees $p$ if the segment $qp$ stays inside $P$. The problem is to compute its boundary. The answer is always a [star-shaped polygon](/star-shaped-polygon/) with $q$ in its kernel, which is where the alias "star-shaped visibility polygon" comes from. For a [simple polygon](/simple-polygon/) with $n$ vertices it has $O(n)$ vertices and can be found in $O(n)$ time, by [Lee's algorithm](/lee-visibility-polygon-algorithm/) as corrected by Joe and Simpson. With holes or with free segments as obstacles, the best time is $\Theta(n \log n)$. The visibility polygon is the basic step of guard problems ([art gallery problem](/art-gallery-problem/)), of the [visibility graph](/visibility-graph-of-polygon/), and of many motion planning methods. It is a 2D, exact relative of the 3D questions elsewhere in this area: [hidden-surface removal](/hidden-surface-removal/) asks for the parts of a scene that an eye sees, and [terrain visibility](/terrain-visibility/) asks for the parts of a height field. Visibility from a whole segment instead of a point is the [weak visibility polygon](/weak-visibility-polygon/).

## In plain words

Stand somewhere in a room with straight walls and no doors. Some parts of the room you can see, and some parts are behind a corner. The parts you can see form a region of the floor. Its border is made of pieces of the walls that you see, and of straight edges along your lines of sight past the corners, where the shadow of a corner begins. The problem is to find this region exactly. Since you see each point of the region along a straight line, the region has no part that is hidden from where you stand.

## Definition

**Input.** A polygon $P$, simple or with holes, with $n$ vertices in total and rational coordinates, taken as a closed region, and a point $q \in P$.

**Visibility.** A point $p \in P$ is *visible* from $q$ if the closed segment $qp$ lies in $P$. The segment may touch the boundary, for example it may pass through a reflex vertex.

**Output.** The visibility polygon $V(q) = \{ p \in P : qp \subseteq P \}$, as the list of the vertices of its boundary in angular order around $q$.

**Structure.** $V(q)$ is star-shaped and $q$ is in its kernel, since for $p \in V(q)$ the whole segment $qp$ is in $V(q)$. In particular $V(q)$ has no holes, even when $P$ has holes. Each vertex of $V(q)$ is a vertex of $P$, or a *shadow point*, where the ray from $q$ through a vertex $v$ of $P$ grazes $v$ and goes on to hit an edge behind it. Each vertex of $P$ gives at most one shadow point, so $V(q)$ has at most $2n$ vertices. The edges of $V(q)$ are parts of edges of $P$, and *windows*, the segments from a vertex to its shadow point.

## Variants

- **Simple polygon.** The case with no holes. Linear time is possible because the boundary order of $P$ gives the angular order of the visible parts almost for free ([Lee's algorithm](/lee-visibility-polygon-algorithm/)).
- **Polygon with holes, or segments in the plane.** The obstacles are $h$ holes, or $n$ disjoint segments. The boundary order no longer helps, and an angular sweep around $q$ is the standard method ([rotational sweep](/rotational-sweep/)).
- **Query version.** Preprocess $P$ once, then report $V(q)$ for many query points $q$, in time that depends on the size $k$ of the answer (Bose, Lubiw and Munro 2002).
- **Weak visibility.** The set of points seen from some point of a segment $e$, the [weak visibility polygon](/weak-visibility-polygon/).
- **Limited views.** A view cone or a range limit, as for a camera or a sensor, clips $V(q)$ by a wedge or a disk.
- **Visibility on a terrain.** The 2.5D analogue is the viewshed of a viewer above a height field ([terrain visibility](/terrain-visibility/)).
- **The whole polygon.** Deciding whether $V(q) = P$ for some $q$ is deciding whether $P$ is star-shaped, which is the [kernel](/polygon-kernel/) problem.

## Examples

**An L-shaped room.** Let $P = (0,0), (6,0), (6,2), (2,2), (2,6), (0,6)$, the union of the rectangles $[0,6] \times [0,2]$ and $[0,2] \times [0,6]$, with area 20 and the reflex vertex $(2,2)$.

- For $q = (4,1)$, the ray from $q$ through $(2,2)$ has the direction $(-2, 1)$ and hits the left wall $x = 0$ at $(0, 3)$. So $V(q) = (2,2), (0,3), (0,0), (6,0), (6,2)$, with area 13. The window from $(2,2)$ to $(0,3)$ is the edge of the shadow, and the upper arm above it is hidden.
- For $q = (1,5)$, the ray through $(2,2)$ has the direction $(1, -3)$ and hits the floor $y = 0$ at $(8/3, 0)$. So $V(q) = (0,6), (0,0), (8/3, 0), (2,2), (2,6)$.
- For $q = (1,1)$, the point is in the kernel $[0,2] \times [0,2]$, and $V(q) = P$.

**A room with a pillar.** Let $P$ be the square $[0,6]^2$ with the square hole $[2,4]^2$, and $q = (1,1)$. The hole has the two silhouette corners $(4,2)$ and $(2,4)$ as seen from $q$. The ray through $(4,2)$ has the direction $(3,1)$ and hits $x = 6$ at $(6, 8/3)$, and the ray through $(2,4)$ has the direction $(1,3)$ and hits $y = 6$ at $(8/3, 6)$. So

$$V(q) = (0,0), (6,0), (6, 8/3), (4,2), (2,2), (2,4), (8/3, 6), (0,6),$$

a star-shaped polygon with no hole. The shadow of the pillar is the region behind it, between the two windows.

## Known algorithms

| polygon | algorithm | time | notes |
|---|---|---|---|
| any | ray to each vertex, nearest hit by brute force | $O(n^2)$ | a reference method for tests |
| any, or segments | angular sweep around $q$ with a balanced search tree of the edges hit by the ray ([rotational sweep](/rotational-sweep/); Asano and others 1986) | $O(n \log n)$ | optimal when holes are allowed |
| simple | ElGindy and Avis (1981) | $O(n)$ | the first linear method; Joe and Simpson show inputs that wind around $q$ where it fails |
| simple | [Lee (1983)](/lee-visibility-polygon-algorithm/), corrected by Joe and Simpson (1987) | $O(n)$ | one scan of the boundary with a stack |
| simple, many queries | Bose, Lubiw and Munro (2002) | $O(\log n + k)$ per query | after a polynomial preprocessing step |

The brute-force method sends a ray from $q$ to each vertex $v$, tests it against all edges, and keeps the nearest hit and, if $v$ is grazed, the hit behind $v$. Sorting the points by angle then gives $V(q)$.

## Bounds

- **Output size.** $V(q)$ has at most $2n$ vertices, by the count of shadow points above, and it can have $\Theta(n)$. So $\Omega(n)$ time is needed, and Lee's algorithm is optimal for simple polygons.
- **With holes.** $\Omega(n \log n)$ comparisons are needed in the algebraic decision tree model, by the reduction from sorting below, and the angular sweep matches it.
- **Exact arithmetic.** With integer input, each shadow point is the crossing of a line through $q$ and a vertex with an edge, so its coordinates are rationals whose sizes are a constant times the input size. The tests on this page and in the implementation of Lee's algorithm use exact rationals.

## Reductions

- **From sorting, with holes.** Given distinct numbers $x_1, \dots, x_m$, map them to angles in a small range, put a short segment (or a thin triangular hole) at distance 1 from $q$ at each angle, short enough that they do not hide each other, and put all of it in a large square. Each obstacle is visible, and $V(q)$ lists them in angular order, which is the sorted order of the $x_i$.
- **To ray shooting.** $V(q)$ is fixed by the first hit of the rays from $q$ through the vertices of $P$ and just past them. So any ray shooting structure for $P$ gives an algorithm with $O(n)$ queries.
- **Guarding.** A set $G$ of guards sees $P$ if and only if $\bigcup_{g \in G} V(g) = P$, so guard problems for a fixed candidate set reduce to the union of visibility polygons ([art gallery problem](/art-gallery-problem/)). The [visibility graph](/visibility-graph-of-polygon/) of $P$ joins each vertex $v$ to the vertices on the boundary of $V(v)$.

## Applications

- **Guards, cameras and sensors.** The area that one guard or one camera covers in a floor plan is its visibility polygon.
- **Motion planning and shortest paths.** Shortest paths among polygonal obstacles turn only at vertices that see each other, so visibility polygons build the visibility graph.
- **Games and lighting in 2D.** The lit area of a point light in a 2D level, and the area that a player sees, are visibility polygons. This is how "fog of war" and 2D shadows are often drawn.
- **Robot exploration.** A robot with a range finder sees its visibility polygon, and exploration methods choose the next position from it.

## References
