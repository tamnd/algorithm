---
tag: 6165MC
kind: concept
slug: polygon-kernel
name: Kernel of a polygon
aliases:
- kernel
- kernel of a simple polygon
- polygon kernel
area: geometry/polygons
level: core
summary: The set of points from which the whole polygon is visible; the intersection of its interior-side half-planes.
prereqs: [star-shaped-polygon, simple-polygon, half-plane-intersection]
see_also: [star-shaped-polygon, half-plane-intersection-deque, art-gallery-problem, visibility-polygon, convex-polygon, sutherland-hodgman, point-in-convex-polygon, mesh-generation]
sources:
  - paper: doi:10.1145/322139.322142
    title: D. T. Lee and F. P. Preparata, An optimal algorithm for finding the kernel of a polygon, Journal of the ACM 26(3), 415 to 421 (1979)
    locator: the whole paper (the kernel as an intersection of half-planes, and the O(n) algorithm that keeps the kernel of a growing chain)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.5, the kernel of a plane polygon
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 4, Section 4.2, half-plane intersection in O(n log n) time
---

The kernel of a [simple polygon](/simple-polygon/) $P$ is the set of points of $P$ from which every point of $P$ is visible, along a segment that stays inside $P$. It is the intersection of the $n$ closed half-planes on the inner side of the edges of $P$, so it is convex, and it is empty, a point, a segment or a convex polygon with at most $n$ edges. The polygon is [star-shaped](/star-shaped-polygon/) exactly when its kernel is not empty. A general [half-plane intersection](/half-plane-intersection/) finds the kernel in $O(n \log n)$ time; Lee and Preparata showed in 1979 that the order of the edges along the boundary allows $O(n)$, which is optimal.

## In plain words

Imagine the polygon is a room, and you stand at one spot inside it. If you can see every corner of the room without leaving that spot, the spot is in the kernel. In a room with no corners that point inward, every spot works. Each wall that bends inward hides part of the room from some spots.

Each wall splits the floor into the side facing into the room and the side behind it. A spot sees everything exactly when it is in front of every wall at once, on the inner side of each wall's line. So the kernel is what remains after cutting away, for each wall, everything behind the line of that wall. Cutting with straight lines always leaves a convex piece, or nothing.

## The idea

Let $P$ be a simple polygon with vertices $v_0, \ldots, v_{n-1}$ in counterclockwise order and edges $e_i = v_i v_{i+1}$, identified with its closed region. For each edge let $H_i = \{z : \mathrm{orient}(v_i, v_{i+1}, z) \ge 0\}$ be the closed half-plane to the left of $e_i$, the side of the interior. The kernel is

$$\ker P = \{z \in P : zq \subseteq P \text{ for all } q \in P\}.$$

**Theorem.** $\ker P = H_0 \cap H_1 \cap \cdots \cap H_{n-1}$.

*Proof.* We use one fact about simple polygons: near a point $q$ in the relative interior of an edge $e_i$, a small disk around $q$ is split by the line of $e_i$, the open half on the left of $e_i$ lies in $\operatorname{int} P$, and the open half on the right lies outside $P$.

($\subseteq$) Let $z \in \ker P$ and suppose $z \notin H_i$, so $z$ is strictly to the right of the line of $e_i$. Take $q$ in the relative interior of $e_i$. The points of the segment $zq$ close to $q$ are strictly right of the line of $e_i$ and close to $q$, so they lie outside $P$. Then $zq \not\subseteq P$, a contradiction.

($\supseteq$) Let $z \in \bigcap_i H_i$ and $q \in P$, and suppose the segment from $q$ to $z$ leaves $P$. The set of its points in $P$ is closed, so there is a last point $x$ such that the segment from $q$ to $x$ lies in $P$ and points just after $x$ toward $z$ are outside $P$. Then $x \in \partial P$. If $x$ is in the relative interior of an edge $e_i$, the segment passes from the closed left side of $e_i$ to the open right side there, and since it is not contained in the line of $e_i$, it crosses that line at $x$ and stays strictly to the right of it afterward; so $z \notin H_i$. If $x$ is a vertex $v_i$, the direction $z - x$ points out of the polygon at $v_i$. At a convex vertex the polygon near $v_i$ is $H_{i-1} \cap H_i$ near $v_i$, and at a reflex vertex it is $H_{i-1} \cup H_i$; in both cases a direction leaving it is strictly outside $H_{i-1}$ or $H_i$, so $z$ is strictly right of the line of $e_{i-1}$ or of $e_i$. Each case contradicts $z \in \bigcap_i H_i$. So $zq \subseteq P$ for every $q \in P$. The same argument with any $q \in P$ shows $z \in P$, so $z \in \ker P$. $\square$

**Consequences.**

- The kernel is convex, as an intersection of half-planes, and it is closed. It is not empty exactly when $P$ is star-shaped.
- The kernel of a [convex polygon](/convex-polygon/) is the polygon itself, since then $P = \bigcap_i H_i$.
- If $P$ has no reflex vertex, it is convex and the kernel is $P$. With exactly one reflex vertex $v$, the kernel contains $v$: extending the two edges at $v$ into the interior cuts $P$ into pieces without reflex vertices, which are convex and all contain $v$.
- On integer input, the kernel's vertices are intersections of two edge lines, with rational coordinates of denominator at most a constant times the square of the coordinates, and every test is an exact [orientation test](/orientation-test/).

**Computing the kernel.**

- **By half-plane intersection.** The kernel is the intersection of $n$ half-planes, computed in $O(n \log n)$ time by sorting the half-planes by angle and running the deque method of [half-plane intersection](/half-plane-intersection-deque/). This is also optimal for half-planes in arbitrary order.
- **By Lee and Preparata, in $O(n)$.** The edges of a simple polygon come in boundary order, and their directions are almost sorted. The algorithm starts at a reflex vertex and keeps the intersection $K_i = H_0 \cap \cdots \cap H_i$ for the chain $e_0, \ldots, e_i$, a convex region that may be unbounded, as a doubly linked list of its boundary. It also keeps two pointers $F_i$ and $L_i$ to the vertices of $K_i$ where the two tangent lines from $v_{i+1}$ touch $K_i$. Adding $e_{i+1}$ cuts $K_i$ by one line: the cut is found by scanning from $F_i$ or $L_i$, the cut-off vertices are deleted, and the tangent pointers move forward. Each vertex of $K$ is deleted at most once, and an argument about the total turning of the boundary bounds the forward motion of the pointers, so the whole run takes $O(n)$ time. The algorithm stops early when $K_i$ becomes empty.
- **Lower bound.** Every algorithm must read all coordinates: moving one vertex of a convex polygon inward makes it reflex and changes the kernel. So $\Omega(n)$, and Lee and Preparata's bound is optimal.

**Degenerate input.** Collinear consecutive edges give equal half-planes and change nothing. A kernel that is a single point or a segment is still a kernel; the polygon is star-shaped, but only weakly so, with no point that sees $P$ from the interior of the kernel.

## Examples

All examples are in counterclockwise order. The kernels were computed by intersecting the edge half-planes exactly.

| polygon | vertices | kernel | kernel area |
| --- | --- | --- | --- |
| concave pentagon | $(0,0), (6,0), (6,4), (3,1), (0,4)$ | triangle $(2,0), (4,0), (3,1)$ | 1 |
| L-shape | $(0,0), (2,0), (2,1), (1,1), (1,2), (0,2)$ | the square $[0,1]^2$ | 1 |
| four-pointed star | $(0,0), (2,1), (4,0), (3,2), (4,4), (2,3), (0,4), (1,2)$ | octagon $(2,1), (\frac83, \frac43), (3,2), (\frac83, \frac83), (2,3), (\frac43, \frac83), (1,2), (\frac43, \frac43)$ | $\frac83$ |
| Z-shape | $(0,0), (2,0), (2,1), (3,1), (3,2), (1,2), (1,1), (0,1)$ | the segment from $(1,1)$ to $(2,1)$ | 0 |
| U-shape | $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ | empty | |

- **The pentagon.** The reflex vertex $(3,1)$ has the edges from $(6,4)$ and to $(0,4)$. Their half-planes are $x - y \ge 2$ and $x + y \le 4$; with $y \ge 0$ from the bottom edge they cut out the triangle. The other edges, $x \le 6$ and $x \ge 0$, do not touch it.
- **The star.** The kernel has all four reflex vertices $(2,1), (3,2), (2,3), (1,2)$ as corners. Each of its other four corners is the meeting point of the lines of two edges at neighboring reflex vertices, such as $(\frac83, \frac43)$, where the line $y = x/2$ of the edge from $(0,0)$ to $(2,1)$ meets the line $y = 2x - 4$ of the edge from $(3,2)$ to $(4,4)$.
- **The U-shape.** The inner edge from $(2,3)$ to $(2,1)$ needs $x \ge 2$, and the inner edge from $(1,1)$ to $(1,3)$ needs $x \le 1$. No point satisfies both, and indeed no point sees the tops of both prongs.

## Where it is used

- **[Star-shaped polygons](/star-shaped-polygon/).** A polygon is star-shaped exactly when its kernel is not empty, and a point of the kernel's interior is a center from which the boundary is a single-valued function of the angle.
- **[Art gallery problem](/art-gallery-problem/).** One guard sees the whole polygon exactly when it stands in the kernel, so testing whether one guard suffices is computing the kernel.
- **[Visibility polygon](/visibility-polygon/).** The kernel is the set of points whose visibility polygon is all of $P$.
- **[Point in convex polygon](/point-in-convex-polygon/).** The binary search on angles around a center works for a star-shaped polygon when the center is a point of the kernel's interior, giving $O(\log n)$ queries after $O(n)$ preprocessing.
- **[Sutherland-Hodgman](/sutherland-hodgman/).** Clipping by each edge's half-plane in turn computes the subject intersected with $\bigcap_i H_i$. For a convex clip polygon this is the intersection with the clip polygon; for a concave one it is the intersection with its kernel, which is why the method is wrong for concave clip polygons.
- **[Mesh generation](/mesh-generation/).** When a mesh vertex is moved to smooth a triangulation, its triangles keep their orientation exactly when the new position lies in the interior of the kernel of the polygon formed by its neighbors.

## References
