---
tag: SK1EM1
kind: definition
slug: polygon-with-holes
name: Polygon with holes
aliases:
- polygon with holes
- multiply connected polygon
- polygonal domain
area: geometry/polygons
level: core
summary: A polygonal region bounded by an outer boundary and one or more interior boundaries (holes).
prereqs: [simple-polygon]
see_also: [polygon-with-holes-triangulation, polygon-orientation, shoelace-formula, point-in-polygon, polygon-clipping, art-gallery-problem, euclidean-shortest-path, planar-subdivision]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, polygons with holes, and the count of triangles in a triangulation of a polygon with holes
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 3, Exercises (triangulating a polygon with holes, and the number of triangles n + 2h − 2)
  - url: https://www.rfc-editor.org/rfc/rfc7946
    title: H. Butler and others, The GeoJSON Format, RFC 7946, 2016
    locator: Section 3.1.6, Polygon (an exterior ring and interior rings, with exterior rings counterclockwise and holes clockwise)
---

A polygon with holes is a region of the plane bounded by one outer [simple polygon](/simple-polygon/) and $h \ge 0$ inner simple polygons, the holes, that lie inside it and do not touch each other or the outer boundary. It is the shape of a floor plan with pillars, a country with lakes, or a letter such as A or B. Its boundary has $h + 1$ separate closed curves, so it is connected but, for $h \ge 1$, not simply connected: a loop around a hole cannot shrink to a point inside the region. Many algorithms for simple polygons extend to it, and some problems, such as guarding and shortest paths, become harder.

## Definition

Let $P_0$ be a simple polygon and $H_1, \ldots, H_h$ simple polygons with

1. $H_j \subset \operatorname{int} P_0$ for each $j$, where $H_j$ denotes the closed region of the hole;
2. $H_j \cap H_k = \emptyset$ for $j \ne k$.

The **polygon with holes** is the closed region

$$Q = P_0 \setminus \bigcup_{j=1}^{h} \operatorname{int} H_j.$$

Its boundary is $\partial Q = \partial P_0 \cup \partial H_1 \cup \cdots \cup \partial H_h$, a union of $h + 1$ disjoint closed curves, the **contours** or **rings**. The number of vertices is $n = n_0 + n_1 + \cdots + n_h$, where $n_j$ is the number of vertices of contour $j$. For $h = 0$ this is a simple polygon.

**Orientation convention.** The outer contour is listed counterclockwise and each hole clockwise. Then the region lies to the left of every directed edge, and the [signed areas](/shoelace-formula/) add up: $\operatorname{area}(Q) = A(P_0) + \sum_j A(H_j)$, where each $A(H_j)$ is negative. Some formats use the opposite convention, and a reader should check the signs rather than trust the order.

**Theorem.** Every triangulation of $Q$ whose triangles have their corners at vertices of $Q$ has exactly $t = n + 2h - 2$ triangles and $n + 3h - 3$ diagonals.

*Proof.* Add up interior angles. At the vertices of $P_0$ the angles of $Q$ are the interior angles of $P_0$, with sum $(n_0 - 2)\pi$ by the angle sum of a simple polygon. At a vertex of $H_j$ the angle of $Q$ is $2\pi$ minus the interior angle of $H_j$, so these sum to $2\pi n_j - (n_j - 2)\pi = (n_j + 2)\pi$. In total the angles of $Q$ sum to $(n_0 - 2 + \sum_{j \ge 1} (n_j + 2))\pi = (n + 2h - 2)\pi$. The triangles have no corner other than vertices of $Q$, and at each vertex their angles fill the angle of $Q$, so the angles of the $t$ triangles also sum to this; each triangle contributes $\pi$. For the diagonals, each triangle has three sides, each of the $n$ boundary edges is a side of one triangle and each diagonal of two, so $3t = n + 2d$ and $d = n + 3h - 3$. $\square$

Such a triangulation exists for every polygon with holes ([polygon with holes triangulation](/polygon-with-holes-triangulation/)), for example by joining each hole to the outer contour with a diagonal and triangulating the resulting weakly simple polygon.

**Degenerate input.** Some data formats also allow a hole that touches the outer contour or another hole at a single point. The definition above forbids it; such a region can be split at the touching point or handled as a weakly simple polygon.

## Examples and non-examples

- **A square frame.** The outer square $(0,0), (4,0), (4,4), (0,4)$ with the clockwise hole $(1,1), (1,3), (3,3), (3,1)$ has $n = 8$, $h = 1$ and area $16 - 4 = 12$. Every triangulation has $8 + 2 - 2 = 8$ triangles and $8 + 3 - 3 = 8$ diagonals.
- **Two holes.** The rectangle $(0,0), (6,0), (6,3), (0,3)$ with the holes $(1,1), (1,2), (2,2), (2,1)$ and $(4,1), (4,2), (5,2), (5,1)$ has $n = 12$, $h = 2$, area $18 - 1 - 1 = 16$, and every triangulation has 14 triangles.
- **No holes.** A simple polygon is the case $h = 0$; the formula gives $n - 2$ triangles.
- **Non-example: a hole outside.** A "hole" that does not lie inside $P_0$ removes nothing and breaks condition 1; it is a separate polygon, as in a multipolygon.
- **Non-example: overlapping holes.** Two holes that overlap break condition 2. Their union is one hole, with a contour found by [polygon union](/polygon-union/).
- **Non-example: an island in a lake.** A polygon inside a hole is not part of $Q$. The region with the island is a set of two polygons with holes, one of them inside the hole of the other.

## Related definitions

- **[Simple polygon](/simple-polygon/).** The case $h = 0$, and the type of each contour.
- **[Polygon orientation](/polygon-orientation/).** The convention of the outer and inner contours.
- **[Point in polygon](/point-in-polygon/).** For a polygon with holes, count the crossings of a ray with all contours together; the point is in $Q$ exactly when the total is odd.
- **[Polygon with holes triangulation](/polygon-with-holes-triangulation/).** Triangulating $Q$ in $O(n \log n)$ time; the holes make $\Omega(n \log n)$ necessary in the algebraic decision tree model.
- **[Art gallery problem](/art-gallery-problem/).** With holes, $\lfloor (n + h)/3 \rfloor$ point guards are always enough and sometimes necessary.
- **[Euclidean shortest path](/euclidean-shortest-path/).** Shortest paths in a polygon with holes may pass on either side of a hole, so they are found with a visibility graph or a continuous Dijkstra rather than by the funnel of a simple polygon.
- **[Planar subdivision](/planar-subdivision/).** A polygon with holes is one face of a planar subdivision, with $h + 1$ boundary components.

## References
