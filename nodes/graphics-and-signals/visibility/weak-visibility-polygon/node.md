---
tag: 2V5SZ2
kind: problem
slug: weak-visibility-polygon
name: Weak visibility polygon
aliases:
- weak visibility region
area: graphics-and-signals/visibility
level: advanced
summary: Given a simple polygon and a segment in it, compute the points that some point of the segment sees. The region has O(n) vertices and takes O(n) time after a triangulation.
prereqs: [visibility-polygon, simple-polygon]
see_also: [visibility-polygon, lee-visibility-polygon-algorithm, polygon-kernel, euclidean-shortest-path-in-polygon, funnel-algorithm, chazelle-polygon-triangulation, shadow-determination, art-gallery-problem]
sources:
  - paper: doi:10.1109/TC.1981.1675729
    title: David Avis and Godfried T. Toussaint, An optimal algorithm for determining the visibility of a polygon from an edge, IEEE Transactions on Computers C-30(12), 1981, pages 910 to 914
    locator: the definitions of complete, strong and weak visibility from an edge, and the linear test for weak visibility
  - paper: doi:10.1016/0734-189X(86)90044-7
    title: D. T. Lee and A. K. Lin, Computing the visibility polygon from an edge, Computer Vision, Graphics, and Image Processing 34(1), 1986, pages 1 to 19
    locator: the whole paper (two scans of the boundary, O(n log n) time)
  - paper: doi:10.1007/BF01840360
    title: Leonidas Guibas, John Hershberger, Daniel Leven, Micha Sharir and Robert E. Tarjan, Linear-time algorithms for visibility and shortest path problems inside triangulated simple polygons, Algorithmica 2, 1987, pages 209 to 233
    locator: the shortest path trees from the two endpoints and the weak visibility polygon in linear time after triangulation
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 8, Section 8.1 (the three kinds of edge visibility), Section 8.3 (the edge visibility polygon and the earlier algorithms), Section 8.6 (segment obstacles and the n^4 bound), Section 8.7 (the shortest path tree method)
  - paper: doi:10.1007/BF02574703
    title: Bernard Chazelle, Triangulating a simple polygon in linear time, Discrete and Computational Geometry 6(3), 1991, pages 485 to 524
    locator: the linear triangulation that makes the shortest path tree method linear in total
---

The weak visibility polygon of a segment $e$ in a polygon $P$ is the set of points of $P$ that are seen from at least one point of $e$. The problem is to compute it. The segment is usually an edge of $P$, and the region is what a light tube along $e$ lights. It differs from the [visibility polygon](/visibility-polygon/) of a point in two ways. It is not star-shaped in general, and it is not the union of the visibility polygons of the two endpoints of $e$, because a point can be hidden from both ends and still be seen from the middle. For a [simple polygon](/simple-polygon/) with $n$ vertices it has $O(n)$ vertices. The best algorithm takes $O(n)$ time after a triangulation, so $O(n)$ in total with [Chazelle's triangulation](/chazelle-polygon-triangulation/). Among segment obstacles the region can have $\Theta(n^4)$ vertices. In graphics, [shadow determination](/shadow-determination/) asks the same kind of question for area lights in 3D scenes, mostly by sampling. This page is the exact 2D problem for a light along a segment: the points outside the weak visibility polygon are in full shadow.

## In plain words

Put a long light tube along one wall of a room. A point of the floor is lit if it can see at least one part of the tube. The lit part of the room is the weak visibility region. A point does not need to see the whole tube, and it does not need to see either end of it. A point in a narrow alcove across from the middle of the tube may see only the middle, and it is still lit. The parts of the room that see no part of the tube are dark. The problem is to find the exact border between the lit part and the dark part.

## Definition

**Input.** A simple polygon $P$ with $n$ vertices and rational coordinates, taken as a closed region, and a segment $e = ab$ in $P$. In the standard form, $e$ is an edge of $P$.

**Visibility.** A point $p$ sees a point $x$ if the closed segment $px$ lies in $P$, as for the [visibility polygon](/visibility-polygon/). Write $V(x)$ for the visibility polygon of $x$.

**Three kinds of visibility from $e$** (Avis and Toussaint 1981).

- A point $p$ is *completely visible* from $e$ if $p$ sees every point of $e$.
- $P$ is *strongly visible* from $e$ if some point of $e$ sees all of $P$, that is, $e$ meets the [kernel](/polygon-kernel/) of $P$.
- A point $p$ is *weakly visible* from $e$ if $p$ sees at least one point of $e$. $P$ is weakly visible from $e$ if every point of $P$ is.

**Output.** The weak visibility polygon

$$V(e) = \{ p \in P : p \text{ sees some point of } e \} = \bigcup_{x \in e} V(x),$$

as the list of the vertices of its boundary in order.

**Structure.** $V(e)$ is connected, since each $V(x)$ contains $x$ and $e$ is connected. In a simple polygon it is a simple polygon. Its boundary is made of parts of edges of $P$ and of *windows*. Each window starts at a reflex vertex $u$ of $P$ and cuts off a pocket of $P$ that no point of $e$ sees. The window lies on the last ray from $e$ that grazes $u$, so its line passes through $u$ and through an endpoint of $e$ or a second reflex vertex that blocks the view of $e$ from $u$. The pockets that the windows cut off are disjoint, and each pocket holds at least one vertex of $P$, so there are at most $n$ windows and $V(e)$ has $O(n)$ vertices.

## Variants

- **Completely visible region.** The set of points that see all of $e$. If $p$ sees $a$ and $b$, the triangle $pab$ lies in $P$ because $P$ has no holes, so $p$ sees all of $e$. Thus this region is $V(a) \cap V(b)$, and it takes $O(n)$ time from two runs of [Lee's algorithm](/lee-visibility-polygon-algorithm/).
- **Decision version.** Decide whether $P$ is weakly visible from $e$, that is, whether $V(e) = P$. Avis and Toussaint (1981) solved this in $O(n)$ time.
- **Strong visibility.** Decide whether some point of $e$ sees all of $P$. This is whether $e$ meets the kernel, which the linear kernel algorithm decides ([kernel](/polygon-kernel/)).
- **A segment inside $P$.** The segment $e$ can be a diagonal or any segment in $P$. A chord splits $P$ into two parts, and the problem splits into one problem for each part.
- **Segment obstacles or holes.** With $n$ segments as obstacles, $V(e)$ can be unbounded and have holes, and it can have $\Theta(n^4)$ vertices (O'Rourke, Section 8.6).
- **Weakly visible polygons as a class.** Some guard and path problems are studied on the special class of polygons that are weakly visible from an edge, and the decision version tells whether an input is in this class.

## Examples

**A hall with three alcoves.** Let $P$ be the hall $[0,10] \times [0,2]$ with three alcoves of height 3 on top: $[0,1] \times [2,5]$ at the left, $[9/2, 11/2] \times [2,5]$ in the middle and $[9,10] \times [2,5]$ at the right. In order, its vertices are

$$(0,0), (4,0), (6,0), (10,0), (10,5), (9,5), (9,2), (11/2,2), (11/2,5), (9/2,5), (9/2,2), (1,2), (1,5), (0,5).$$

The floor is split at $(4,0)$ and $(6,0)$, so that $e$ from $a = (4,0)$ to $b = (6,0)$ is an edge. The area of $P$ is 29.

- **The left alcove.** Light enters it past the reflex vertex $(1,2)$. Of all the rays from $e$ that pass $(1,2)$, the ray from $a$ is the steepest. It has the direction $(-3,2)$ and hits the wall $x = 0$ at $(0, 8/3)$. So the part of the alcove above the window from $(1,2)$ to $(0,8/3)$ is dark. The right alcove is the mirror image, with the window from $(9,2)$ to $(10,8/3)$ on the ray from $b$.
- **The middle alcove.** The ray from $a$ through $(9/2,2)$ hits the top $y = 5$ at $(21/4, 5)$, so $a$ lights only the part of the top to the right of it. In the same way $b$ lights only the part to the left of $(19/4, 5)$. The point $(5,5)$ is seen from neither end. But each point $(x, y)$ of the middle alcove sees the point $(x, 0)$ of $e$ straight below it, since $9/2 \le x \le 11/2$. So the whole middle alcove is lit.

The weak visibility polygon is

$$V(e) = (0,0), (10,0), (10, 8/3), (9,2), (11/2,2), (11/2,5), (9/2,5), (9/2,2), (1,2), (0, 8/3),$$

with area $71/3$. The point $(5,5)$ shows that $V(e) \ne V(a) \cup V(b)$. The completely visible region is

$$V(a) \cap V(b) = (0,0), (10,0), (10, 12/5), (9,2), (11/2,2), (5,4), (9/2,2), (1,2), (0, 12/5),$$

with area $107/5$. Here $(0, 12/5)$ is where the ray from $b$ through $(1,2)$ hits the left wall, and $(5,4)$ is where the rays from $a$ through $(9/2,2)$ and from $b$ through $(11/2,2)$ cross. With $e$ as a linear light, the points outside $V(e)$ are in full shadow, the points of $V(e)$ outside $V(a) \cap V(b)$ are in partial shadow, and the rest are in full light.

**Weak visibility without a kernel.** Take the same room, but let $e$ be the whole floor from $(0,0)$ to $(10,0)$. Each point of $P$ sees the point of the floor straight below it, so $P$ is weakly visible from $e$. But no point sees both top corners $(0,5)$ and $(10,5)$, so the kernel of $P$ is empty, and $P$ is not strongly visible from any segment.

## Known algorithms

| problem | algorithm | time | notes |
|---|---|---|---|
| test one point $p$ | compute $V(p)$ by [Lee's algorithm](/lee-visibility-polygon-algorithm/) and test if it meets $e$ | $O(n)$ per point | a reference method for tests |
| completely visible region | $V(a) \cap V(b)$ | $O(n)$ | two visibility polygons and one intersection |
| is $P$ weakly visible from $e$ | Avis and Toussaint (1981) | $O(n)$ | decision only |
| $V(e)$ | ElGindy (1985) | $O(n \log n)$ | split into monotone pieces |
| $V(e)$ | Lee and Lin (1986) | $O(n \log n)$ | two scans of the boundary in opposite directions, a binary search on a stack at some steps |
| $V(e)$ | Chazelle and Guibas (1985) | $O(n \log n)$ | a dual space of rays and divide and conquer |
| $V(e)$ | Guibas, Hershberger, Leven, Sharir and Tarjan (1987) | $O(n)$ after a triangulation | [shortest path](/euclidean-shortest-path-in-polygon/) trees from $a$ and $b$, then one traversal of the boundary |
| $V(e)$ among segments | Suri and O'Rourke (1985) | $O(n^4)$ | optimal by the bound below |

O'Rourke's book of 1987 also gives a plane sweep as a fourth $O(n \log n)$ method, and it describes the shortest path tree method with the $O(n \log \log n)$ triangulation of Tarjan and Van Wyk. With Chazelle's linear triangulation of 1991, the same method takes $O(n)$ in total.

## Bounds

- **Simple polygon.** $V(e)$ has $O(n)$ vertices, by the count of windows above, and it can have $\Theta(n)$. So $\Theta(n)$ time is the answer, and the shortest path tree method with a linear triangulation reaches it.
- **Segment obstacles.** There are $n$ segments in the plane such that $V(e)$ has $\Theta(n^4)$ vertices (O'Rourke, Section 8.6). The construction makes $\Theta(n^2)$ rays from $e$ that cross in $\Theta(n^4)$ points of the boundary. An $O(n^4)$ algorithm matches the bound.
- **Contrast with a point.** For a point the bound with obstacles is $O(n)$ vertices and $\Theta(n \log n)$ time ([visibility polygon](/visibility-polygon/)). The jump to $n^4$ comes from the fact that the region seen from a segment is a union of infinitely many visibility polygons.

## Reductions

- **Complete visibility to point visibility.** The completely visible region is $V(a) \cap V(b)$, as shown in the variants.
- **Strong visibility to the kernel.** $P$ is strongly visible from $e$ exactly when $e$ meets the kernel of $P$, and the kernel is an intersection of $n$ half planes.
- **Weak visibility to shortest paths.** Take a point $p$ in general position. The shortest paths from $p$ to $a$ and to $b$, with $e$, bound a funnel, and the two paths bend away from each other ([funnel algorithm](/funnel-algorithm/)). Then $p$ sees a point of $e$ exactly when the two paths leave $p$ along different edges, so that $p$ is the tip of the funnel. Guibas and others use the shortest path trees from $a$ and from $b$ to apply this test to all the vertices of $P$ in one traversal.
- **To the union of point visibility polygons.** $V(e)$ is the union of $V(x)$ over $x \in e$. Sampling finitely many $x$ gives only an inner approximation, as the point $(5,5)$ in the example shows for the two endpoints.

## Applications

- **Lighting.** A light tube along a wall lights exactly $V(e)$, and the completely visible region is the part in full light. This gives the exact umbra and penumbra of a linear light in a 2D scene.
- **Guards that move.** A guard that walks along a segment sees $V(e)$ during the walk. Guard problems with edge guards ask for a set of edges whose weak visibility polygons cover $P$ ([art gallery problem](/art-gallery-problem/)).
- **Robots and sensors.** A robot that moves along a straight path and senses the whole time sees the weak visibility polygon of its path.
- **Other visibility problems.** The shortest path trees and the hourglass test that Guibas and others use for $V(e)$ also solve other visibility and shortest path problems in a triangulated polygon in linear time, as the title of their paper says.

## References
