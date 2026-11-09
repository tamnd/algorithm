---
tag: 680M9T
kind: theorem
slug: triangulation-counting-theorem
name: Triangulation counting theorem
aliases:
- Euler counting for triangulations
area: geometry/triangulations
level: intro
summary: A triangulation of n points with h hull vertices has 2n-2-h triangles and 3n-3-h edges.
prereqs: [triangulation, euler-formula, convex-polygon]
see_also: [triangulation-of-point-set, polygon-triangulation, maximal-planar-graph, delaunay-triangulation, edge-flip, catalan-triangulation-theorem]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Section 9.1, Theorem 9.1 (2n - 2 - k triangles and 3n - 3 - k edges, with k the number of points on the convex hull boundary)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.2 (n - 2 triangles in a polygon triangulation) and Chapter 4 (Euler's formula); to be checked
---

The triangulation counting theorem says that the size of a triangulation of a point set does not depend on which triangulation is chosen. If $n$ points have $h$ of them on the boundary of their convex hull, every triangulation has exactly $2n - h - 2$ triangles and $3n - h - 3$ edges. The numbers follow from adding up angles, or from [Euler's formula](/euler-formula/). They show that triangulations are sparse, with fewer than $3n$ edges, and that a flip, which trades one edge for another, keeps the counts fixed.

## Statement

Let $S$ be a set of $n$ points in the plane, not all on one line, and let $h$ be the number of points of $S$ on the boundary of the convex hull $\mathrm{conv}(S)$. This counts the hull's corners **and** the points of $S$ in the relative interiors of hull edges. Let $T$ be a [triangulation](/triangulation/) of $S$: triangles with corners in $S$ that meet edge to edge, cover $\mathrm{conv}(S)$, and use every point of $S$ as a corner.

**Theorem.** $T$ has exactly $t = 2n - h - 2$ triangles and $e = 3n - h - 3$ edges.

For a point set in convex position with no three collinear, $h = n$, which gives $n - 2$ triangles and $2n - 3$ edges, the counts for a triangulated convex polygon.

## In plain words

Scatter some points on a table and wrap a rubber band around them. Connect the points with straight lines into triangles, using every point, until no more lines fit without crossing. However you draw the lines, you always get the same number of triangles and the same number of lines. The numbers depend only on how many points there are and how many of them touch the rubber band. Points inside make more triangles than points on the band.

## Proof

**Triangles, by angles.** Add up all angles of all triangles in $T$. Each triangle contributes $\pi$, so the sum is $t \pi$. Now group the angles by their corner point $p \in S$.

1. *Every angle sits at a point of $S$, and the angles at $p$ fill the region near $p$ without overlap.* The triangles cover $\mathrm{conv}(S)$ with disjoint interiors. A small disk around $p$ meets only triangles that contain $p$, and since $p$ is not in the relative interior of any triangle or edge (it is a corner of some triangle, and triangles meet edge to edge), every triangle containing $p$ has $p$ as a corner. So the angles at $p$ add up to the angle of $\mathrm{conv}(S)$ at $p$.
2. *Interior points.* If $p$ is in the interior of $\mathrm{conv}(S)$, the angles at $p$ add up to $2\pi$. There are $n - h$ such points.
3. *Boundary points.* Let the hull have $k$ corners. The angles at the corners add up to $(k - 2)\pi$, the angle sum of a convex $k$-gon. Each of the $h - k$ other boundary points lies inside a hull edge, where the angle is $\pi$. So the boundary points contribute $(k - 2)\pi + (h - k)\pi = (h - 2)\pi$.

Hence $t\pi = 2\pi(n - h) + (h - 2)\pi$, and $t = 2n - h - 2$.

**Edges, by sides.** Each triangle has 3 sides, which gives $3t$ triangle-edge incidences. An edge on the hull boundary lies in one triangle, and every other edge lies in two (on each side of an interior edge, the region near its midpoint is covered, and by edge-to-edge meeting the triangle on that side has the whole edge as a side). The hull boundary is a cycle through all $h$ boundary points, made of $h$ edges of $T$. So $3t = 2e - h$, and
$$e = \frac{3t + h}{2} = \frac{6n - 3h - 6 + h}{2} = 3n - h - 3.$$

**Check by Euler's formula.** The triangulation is a connected plane graph with $V = n$ vertices, $E = e$ edges and $F = t + 1$ faces (the triangles and the outer face). Then $V - E + F = n - (3n - h - 3) + (2n - h - 1) = 2$, as [Euler's formula](/euler-formula/) requires. $\blacksquare$

## Consequences

- **All triangulations of $S$ have the same size.** So an [edge flip](/edge-flip/), which removes one edge and adds one, maps triangulations to triangulations of the same size, and the number of edges in a triangulation tells nothing about which triangulation it is.
- **Sparsity.** Since $h \ge 3$, every triangulation has at most $2n - 5$ triangles and $3n - 6$ edges. This bounds the size of the [Delaunay triangulation](/delaunay-triangulation/), and by duality the number of Voronoi vertices and edges.
- **Maximal planar graphs.** When $h = 3$, the triangulation, outer face included, is a [maximal planar graph](/maximal-planar-graph/) with $3n - 6$ edges.
- **Polygons.** A triangulation of a simple polygon with $n$ vertices has $n - 2$ triangles and $n - 3$ diagonals, by the same angle argument with the interior angle sum $(n - 2)\pi$. A polygon with $n$ vertices and $k$ holes gives $n + 2k - 2$ triangles.
- **Output size.** Algorithms that output a triangulation, such as [triangulation of a point set](/triangulation-of-point-set/), produce $\Theta(n)$ edges, so the output does not dominate their running time.
- **Steiner points.** Adding a point inside a triangle adds 2 triangles and 3 edges; adding one on a hull edge adds 1 triangle and 2 edges.

## Tightness

The formulas are exact equalities, so the only question is the range of $h$. The count is largest when $h = 3$, giving $2n - 5$ triangles (for example, three hull corners and $n - 3$ points inside), and smallest when $h = n$, giving $n - 2$ triangles (points in convex position).

The hypothesis that $h$ counts **all** boundary points matters. Take $S = \{(0,0), (1,0), (2,0), (1,1)\}$. The hull is a triangle with 3 corners, but $(1,0)$ lies inside a hull edge, so $h = 4$. Every triangulation must use $(1,0)$ as a corner, which forces the two triangles $(0,0), (1,0), (1,1)$ and $(1,0), (2,0), (1,1)$: $t = 2 = 2 \cdot 4 - 4 - 2$ and $e = 5 = 3 \cdot 4 - 4 - 3$. With $h = 3$ the formula would claim 3 triangles. Under the convention that a triangulation may skip points (De Loera, Rambau and Santos), the counts are no longer fixed: a convex quadrilateral with one interior point has triangulations with 2 triangles (skipping the point) and with 4 (using it).

The hypothesis that the points are not all on one line is needed: then the hull is a segment and there is no triangle at all.

## History

The counts are a direct consequence of Euler's formula for planar graphs (Euler 1758; the polyhedral formula $V - E + F = 2$). For polygon triangulations the count $n - 2$ is classical. The formulation with the hull size used in computational geometry appears as Theorem 9.1 in the textbook of de Berg, Cheong, van Kreveld and Overmars, where it bounds the size of the Delaunay triangulation.

## References
