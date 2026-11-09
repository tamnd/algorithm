---
tag: Z9MKHN
kind: problem
slug: polygon-clipping
name: Polygon clipping
aliases:
- polygon boolean operations
- polygon intersection and union
- polygon-boolean-operations
- polygon set operations
area: geometry/polygons
level: core
summary: Compute the union, intersection or difference of two polygons, possibly non-convex.
prereqs: [simple-polygon, polygon-with-holes, segment-intersection-point]
see_also: [sutherland-hodgman, weiler-atherton-algorithm, greiner-hormann-algorithm, vatti-clipping, convex-polygon-intersection, polygon-union, polygon-window-clipping, line-clipping]
sources:
  - paper: doi:10.1145/274363.274364
    title: Günther Greiner and Kai Hormann, Efficient clipping of arbitrary polygons, ACM Transactions on Graphics 17(2), 71 to 83 (1998)
    locator: the problem statement for arbitrary polygons, the comparison with Sutherland-Hodgman, Weiler-Atherton and Vatti, and the treatment of degenerate intersections
  - paper: doi:10.1145/129902.129906
    title: Bala R. Vatti, A generic solution to polygon clipping, Communications of the ACM 35(7), 56 to 63 (1992)
    locator: the sweep-line clipping of arbitrary polygons with holes and self-intersections, for intersection, union, difference and exclusive or
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, the overlay of two planar subdivisions by a plane sweep and its use for Boolean operations on polygons
---

Polygon clipping asks for the intersection, union or difference of two polygons, the **subject** $P$ and the **clip** polygon $Q$, as a set of output polygons. When $Q$ is convex, as a window on the screen, the problem is easy and [Sutherland-Hodgman](/sutherland-hodgman/) cuts $P$ by one edge line of $Q$ after another. For general polygons the boundaries can cross many times, the result can fall into several pieces and can have holes, and the algorithms trace the boundaries through their crossing points ([Weiler-Atherton](/weiler-atherton-algorithm/), [Greiner-Hormann](/greiner-hormann-algorithm/)) or sweep a line over the plane ([Vatti](/vatti-clipping/)). With $n$ and $m$ vertices and $k$ boundary crossings, the output has $\Theta(n + m + k)$ vertices, which is $\Theta(n m)$ in the worst case, and the hard part in practice is not the time bound but degenerate input: shared edges, vertices on edges, and touching corners.

## In plain words

Lay two paper shapes on a table, one on top of the other. You may want the part where they overlap, the outline of both together, or the first shape with the second one cut out of it. Each answer is again a set of shapes.

If the second shape is a plain window with no dents, you can cut the first shape along each side of the window in turn and keep the inside part. If both shapes have dents, their outlines can cross many times. Then you find all the crossings, and walk along the outlines, switching from one outline to the other at each crossing, so that you trace exactly the edge of the answer. The answer can come out as several separate pieces, or as a piece with a hole.

## Definition

**Input.** Two polygons $P$ and $Q$, each given as one or more closed vertex lists (contours), with $n$ vertices in $P$ and $m$ in $Q$, and an operation: intersection $P \cap Q$, union $P \cup Q$, difference $P \setminus Q$, or exclusive or $P \triangle Q$. In the basic version $P$ and $Q$ are [simple polygons](/simple-polygon/), identified with their closed regions; general versions allow [holes](/polygon-with-holes/), several outer contours, and self-intersecting contours with a fill rule.

**Output.** The regularized result: the closure of the interior of the set operation, given as a set of contours, each outer contour counterclockwise and each hole clockwise. Regularization discards parts of dimension less than two, such as a shared edge in $P \cap Q$ or a single touching point.

**Model.** The [real RAM](/real-ram/). Crossing points of two edges are rational in the input coordinates (see [segment intersection point](/segment-intersection-point/)), so on integer input every predicate can be decided exactly, but the output coordinates need about twice the input precision in numerator and denominator.

**General position.** The basic algorithms assume that no vertex of one polygon lies on an edge of the other and that no two edges of different polygons overlap. Degenerate input is handled by perturbing the vertices symbolically, by snapping and merging, or by a sweep that classifies each edge piece by its winding numbers, as discussed below.

Let $k$ be the number of crossing points of an edge of $P$ with an edge of $Q$.

## Variants

- **Clipping by a window.** $Q$ is an axis-parallel rectangle or a convex polygon. This is [polygon window clipping](/polygon-window-clipping/) in rasterization, solved by [Sutherland-Hodgman](/sutherland-hodgman/) in $O(n m^2)$ time, which is $O(n)$ for a rectangle; clipping a set of segments instead of a polygon is [line clipping](/line-clipping/).
- **Two convex polygons.** The intersection is convex and is found in $O(n + m)$ time by walking both boundaries ([convex polygon intersection](/convex-polygon-intersection/)).
- **Two simple polygons.** The general case for [Weiler-Atherton](/weiler-atherton-algorithm/) and [Greiner-Hormann](/greiner-hormann-algorithm/).
- **Many polygons.** The [union of many polygons](/polygon-union/), the overlay of two maps, and polygons with self-intersections under the [even-odd](/even-odd-fill-rule/) or [nonzero](/nonzero-winding-rule/) fill rule, handled by sweep algorithms such as [Vatti](/vatti-clipping/).
- **Area only.** When only the area of the result is needed, the [polygon area](/polygon-area/) of the output is the answer; for rectangles it is the [area of union of rectangles](/area-of-union-of-rectangles/).
- **Offsetting and Minkowski sums.** Growing a polygon by a disk or a convex shape is a union of many simple pieces, so it is solved with the same machinery; see [Minkowski sum](/minkowski-sum/).

## Examples

All polygons are counterclockwise.

- **Two overlapping squares.** $P = (0,0), (2,0), (2,2), (0,2)$ and $Q = (1,1), (3,1), (3,3), (1,3)$. The boundaries cross at $k = 2$ points, $(2,1)$ and $(1,2)$. The intersection is the unit square $(1,1), (2,1), (2,2), (1,2)$ with area 1, the union is the octagon $(0,0), (2,0), (2,1), (3,1), (3,3), (1,3), (1,2), (0,2)$ with area 7, and $P \setminus Q$ is the L-shape $(0,0), (2,0), (2,1), (1,1), (1,2), (0,2)$ with area 3.
- **A result in two pieces.** $P$ is the U-shape $(0,0), (3,0), (3,3), (2,3), (2,1), (1,1), (1,3), (0,3)$ with area 7, and $Q$ is the strip $(0,2), (3,2), (3,3), (0,3)$ with area 3. Then $P \cap Q$ is two unit squares, $[0,1] \times [2,3]$ and $[2,3] \times [2,3]$, with total area 2. Sutherland-Hodgman, which outputs one vertex list, would join them by an edge of zero width along the top.
- **A union with a hole.** For the same $P$ and $Q$, the strip closes the gap between the prongs, and $P \cup Q$ is the square $[0,3]^2$ with the hole $[1,2] \times [1,2]$: area $9 - 1 = 8 = 7 + 3 - 2$.
- **A degenerate case.** $P = [0,2]^2$ and $Q = [2,4] \times [0,2]$ share the edge $x = 2$. The intersection is the segment, which the regularized operation discards, so $P \cap Q$ is empty and $P \cup Q$ is the rectangle $[0,4] \times [0,2]$. A crossing-based method sees no proper crossings here and needs special rules to merge the two squares.

## Known algorithms

| algorithm | input | time | notes |
| --- | --- | --- | --- |
| [Sutherland-Hodgman](/sutherland-hodgman/), 1974 | any $P$, convex $Q$ | $O(m (n + m))$ for convex $P$, at most $O(n m^2)$ | one output list; disconnected pieces are joined by zero-width edges |
| [convex polygon intersection](/convex-polygon-intersection/), 1982 | convex $P$ and $Q$ | $O(n + m)$ | walks both boundaries in step |
| [Weiler-Atherton](/weiler-atherton-algorithm/), 1977 | simple $P$ and $Q$, with holes | $O(n m + k \log k)$ | tags crossings as entering or leaving, then traces; fails on vertices on edges without extra rules |
| [Greiner-Hormann](/greiner-hormann-algorithm/), 1998 | any closed contours, even-odd rule | $O(n m + k \log k)$ | doubly linked lists with entry and exit flags; degenerate vertices are perturbed, or handled by the 2019 extension of Foster, Hormann and Popa |
| [Vatti](/vatti-clipping/), 1992 | many contours, holes, self-intersections | sweep over all edges and crossings | local minima and bounds; fill rules decided by winding counts; basis of the Clipper library |
| overlay by plane sweep (de Berg et al.) | planar subdivisions | $O((n + m + k) \log (n + m))$ | [Bentley-Ottmann](/bentley-ottmann-algorithm/) on all edges, then each face is labeled by whether it is in $P$ and in $Q$ |

The $O(n m)$ term in Weiler-Atherton and Greiner-Hormann comes from testing every edge pair for a crossing; replacing that step by a sweep makes them output-sensitive.

## Bounds

- **Output size.** The result has at most $n + m + 2k$ vertices, and $k \le n m$. Two combs show that $\Theta(n m)$ is reached: one with $\Theta(n)$ thin horizontal teeth and one with $\Theta(m)$ thin vertical teeth, laid over each other, meet in $\Theta(n m)$ small squares, so $P \cap Q$ has $\Theta(n m)$ separate pieces.
- **Lower bound.** Any algorithm must at least write the output, so $\Omega(n + m + k)$ time; with the comb example this gives $\Omega(n m)$ in the worst case, and the $O(n m)$ algorithms are optimal in that sense.
- **Output-sensitive upper bound.** The plane sweep gives $O((n + m + k) \log (n + m))$, which is much faster when $k$ is small, as in most practical inputs.
- **Convex inputs.** $\Theta(n + m)$, since the intersection of two convex polygons has at most $n + m$ vertices.

## Reductions

- **Difference and exclusive or to intersection and union.** $P \setminus Q = P \cap \overline{Q}$, where the complement $\overline{Q}$ is obtained by reversing the orientation of $Q$; Weiler-Atherton and Greiner-Hormann implement this by inverting the entering and leaving flags. $P \triangle Q = (P \setminus Q) \cup (Q \setminus P)$.
- **Clipping to segment intersection.** All crossing-based methods first solve [segment intersection](/all-segment-intersections/) between the edges of $P$ and of $Q$, the red-blue version of the problem.
- **Clipping to overlay.** The overlay of the two boundaries is a [planar subdivision](/planar-subdivision/); every Boolean operation is a selection of its faces, and the output contours are the boundaries between selected and unselected faces.
- **Union of many polygons.** Can be done by repeated two-polygon unions, or in one sweep, which avoids the blow-up of intermediate results; see [polygon union](/polygon-union/).

## Applications

- **Rendering.** Clipping polygons against the view window or the view volume before rasterization, and hidden surface removal, the original use of Weiler-Atherton.
- **GIS.** Overlay of map layers, for example land parcels with flood zones, is intersection and union of many polygons with holes.
- **CAD and manufacturing.** Constructive solid geometry in the plane, cutting patterns, and tool paths by offsetting.
- **Printed circuit boards and chip layout.** Design rule checks and the union of copper areas are Boolean operations on large sets of rectilinear polygons.
- **Games and robotics.** Navigation meshes and [configuration space](/configuration-space/) obstacles are built from unions and differences of polygons.

## References
