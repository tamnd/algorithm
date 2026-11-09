---
tag: 3WEVWQ
kind: definition
slug: star-shaped-polygon
name: Star-shaped polygon
aliases:
- star polygon
- star-shaped region
area: geometry/polygons
level: intro
summary: A polygon that has at least one point from which every point of the interior is visible.
prereqs: [simple-polygon, convex-set]
see_also: [polygon-kernel, convex-polygon, art-gallery-problem, visibility-polygon, angular-sort, point-in-convex-polygon, monotone-polygon, half-plane-intersection]
sources:
  - paper: doi:10.1145/322139.322142
    title: D. T. Lee and F. P. Preparata, An optimal algorithm for finding the kernel of a polygon, Journal of the ACM 26(3), 415 to 421 (1979)
    locator: the definition of the kernel and of a star-shaped polygon, and the O(n) kernel algorithm
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 7, Section 7.2.5, the kernel of a plane polygon (star-shaped polygons and the Lee-Preparata algorithm)
  - book: isbn:9780195039658
    title: Joseph O'Rourke, Art Gallery Theorems and Algorithms, Oxford University Press, 1987
    locator: Chapter 1, a polygon can be guarded by one guard exactly when it is star-shaped
---

A star-shaped polygon is a [simple polygon](/simple-polygon/) that contains a point $z$ from which the whole polygon is visible: for every point $q$ of the polygon, the segment from $z$ to $q$ stays inside. The set of all such points $z$ is the [kernel](/polygon-kernel/) of the polygon, a convex set, and the polygon is star-shaped exactly when its kernel is not empty. Every [convex polygon](/convex-polygon/) is star-shaped, with the kernel equal to the whole polygon, and the outline of a star is the usual example of a star-shaped polygon that is not convex. In the language of the [art gallery problem](/art-gallery-problem/), a polygon is star-shaped exactly when one guard can see all of it.

## Definition

Let $P$ be a simple polygon, identified with its closed region. Two points $p, q \in P$ **see each other** if the segment $pq$ lies in $P$; the segment may run along the boundary. $P$ is **star-shaped** if there is a point $z \in P$ that sees every point of $P$. The **kernel** of $P$ is

$$\ker P = \{z \in P : zq \subseteq P \text{ for all } q \in P\},$$

so $P$ is star-shaped if and only if $\ker P \ne \emptyset$. The same definition applies to any subset of the plane; a set is star-shaped with respect to $z$ if it contains the segments from $z$ to all its points. A [convex set](/convex-set/) is one that is star-shaped with respect to each of its points.

In counterclockwise order, $\ker P$ is the intersection of the $n$ closed half-planes to the left of the directed edges of $P$; the proof is on the [kernel](/polygon-kernel/) page. So the kernel is a convex polygon, a segment, a point or empty, and it is found in $O(n)$ time.

**Theorem.** If $z$ lies in the interior of $\ker P$, every ray from $z$ meets $\partial P$ in exactly one point. Consequently, the vertices of $P$, in boundary order, are sorted by their angle around $z$.

*Proof.* Let $\rho$ be a ray from $z$. The set $P \cap \rho$ is compact and contains, with each of its points $q$, the whole segment $zq$, so it is a segment $[z, q^*]$. The point $q^*$ is on $\partial P$. Take a point $x = (1 - \lambda) z + \lambda q$ with $q \in P$ and $0 \le \lambda < 1$, and a disk $D$ of radius $\varepsilon$ around $z$ inside $\ker P$. Each point of $D$ sees $q$, so the segments from $D$ to $q$ cover the disk of radius $(1 - \lambda)\varepsilon$ around $x$, and $x$ is an interior point of $P$. So every point of $[z, q^*)$ is interior, and $q^*$ is the only boundary point on $\rho$. As $\rho$ turns once around $z$, its boundary point moves once around $\partial P$ in the same direction, which gives the angular order of the vertices. $\square$

If $z$ is in the kernel but on its boundary, a ray from $z$ can run along an edge, and the theorem holds with this exception.

**Degenerate input.** The kernel can be a single segment or a single point; the polygon is then star-shaped, but no point sees the whole polygon from its interior, and the angular order around a kernel point can have ties.

## Examples and non-examples

- **Convex polygons.** Every convex polygon is star-shaped, and its kernel is the whole polygon.
- **A concave pentagon.** $(0,0), (6,0), (6,4), (3,1), (0,4)$ is star-shaped. Its kernel is the triangle $(2,0), (4,0), (3,1)$, bounded by the lines of the two edges at the reflex vertex $(3,1)$ and by the bottom edge.
- **A four-pointed star.** $(0,0), (2,1), (4,0), (3,2), (4,4), (2,3), (0,4), (1,2)$, with area 8, is star-shaped. Its kernel is the octagon $(2,1), (\frac83, \frac43), (3,2), (\frac83, \frac83), (2,3), (\frac43, \frac83), (1,2), (\frac43, \frac43)$, with area $\frac83$.
- **An L-shape.** $(0,0), (2,0), (2,1), (1,1), (1,2), (0,2)$ is star-shaped with the unit square $[0,1]^2$ as its kernel.
- **A Z-shape with a thin kernel.** $(0,0), (2,0), (2,1), (3,1), (3,2), (1,2), (1,1), (0,1)$ is star-shaped, but its kernel is only the segment from $(1,1)$ to $(2,1)$.
- **Non-example: a U-shape.** $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ is not star-shaped: the inner edges of the two prongs need $x \ge 2$ and $x \le 1$, so the kernel is empty. No point sees the tops of both prongs.
- **Non-example: a spiral.** A polygon shaped like a corridor that coils around a center has an empty kernel: no point sees both ends of the corridor.

## Related definitions

- **[Kernel of a polygon](/polygon-kernel/).** The set of points that see the whole polygon, and how to compute it.
- **[Convex polygon](/convex-polygon/).** The polygons whose kernel is the whole polygon.
- **[Art gallery problem](/art-gallery-problem/).** The fewest guards that see a polygon; the answer is 1 exactly for star-shaped polygons.
- **[Visibility polygon](/visibility-polygon/).** The part of a polygon seen from one point; $P$ is star-shaped with respect to $z$ when the visibility polygon of $z$ is all of $P$.
- **[Monotone polygon](/monotone-polygon/).** Another class of simple polygons with an order on the boundary, here by a direction instead of by angle; neither class contains the other.
- **[Point in convex polygon](/point-in-convex-polygon/).** The binary search on angles used there works for a star-shaped polygon from any interior kernel point, by the theorem above.

## References
