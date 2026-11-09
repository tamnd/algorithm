---
tag: E9KW5N
kind: definition
slug: triangulation
name: Triangulation
aliases:
- Planar triangulation
- Maximal planar subdivision
area: geometry/triangulations
level: intro
summary: A subdivision of a region or point set into triangles that meet edge to edge.
prereqs: [planar-subdivision, convex-polygon, simple-polygon]
see_also: [triangulation-of-point-set, polygon-triangulation, triangulation-counting-theorem, delaunay-triangulation, constrained-triangulation, maximal-planar-graph, tetrahedralization, edge-flip]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Section 9.1, Triangulations of Planar Point Sets (maximal planar subdivisions and Theorem 9.1), and Chapter 3, Section 3.1 (triangulations of polygons)
  - book: isbn:9783642129704
    title: Jesús A. De Loera, Jörg Rambau and Francisco Santos, Triangulations, Structures for Algorithms and Applications, Springer, 2010
    locator: Chapter 2 (definitions of triangulations of point configurations) and Chapter 3 (the planar case); chapter numbers to be checked
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.2 (triangulations of polygons by diagonals)
---

A triangulation cuts a region of the plane into triangles that fit together edge to edge: two triangles share a whole edge, a single corner, or nothing. The two most common inputs are a [simple polygon](/simple-polygon/), whose triangles use only the polygon's vertices, and a finite point set, whose triangles fill the convex hull and use the points as corners. In both cases the triangulation can be seen as a [planar subdivision](/planar-subdivision/) that cannot get any more edges without crossings.

## Definition

Let $S$ be a finite set of points in the plane, not all on one line. A **triangulation of $S$** is a set $T$ of triangles such that:

1. the corners of every triangle are points of $S$, and every triangle has positive area;
2. any two triangles of $T$ intersect in a common edge, a common corner, or not at all (the triangles are **edge to edge**);
3. the union of the triangles is the convex hull $\mathrm{conv}(S)$;
4. every point of $S$ is a corner of some triangle.

Conditions 2 and 4 together mean that no point of $S$ lies in the relative interior of an edge or a triangle. An equivalent definition (de Berg et al.): a triangulation of $S$ is a **maximal planar subdivision** with vertex set $S$, that is, a set of segments between points of $S$ that do not cross and do not pass through other points of $S$, such that no further segment can be added. The faces of such a maximal subdivision inside the convex hull are triangles. Some authors, notably De Loera, Rambau and Santos, drop condition 4 and allow points of $S$ to be skipped; this page follows the computational geometry convention that uses all points.

A **triangulation of a simple polygon** $P$ is a triangulation in the same sense whose triangles have corners among the vertices of $P$ and whose union is $P$ instead of the convex hull. Its edges are the polygon edges and a maximal set of non-crossing diagonals. The general notion for a region with prescribed edges is a [constrained triangulation](/constrained-triangulation/).

As a graph, the vertices and edges of a triangulation form a plane graph whose bounded faces are triangles. If $S$ has $n$ points and $h$ of them lie on the boundary of the convex hull, it has $2n - h - 2$ triangles and $3n - h - 3$ edges, by the [triangulation counting theorem](/triangulation-counting-theorem/). A triangulation of a polygon with $n$ vertices has $n - 2$ triangles. In graph theory, a **planar triangulation** is a [maximal planar graph](/maximal-planar-graph/): a plane graph in which every face, including the outer face, is a triangle. A triangulation of a point set is a maximal planar graph exactly when its convex hull is a triangle.

## Examples and non-examples

- **A square with its center.** For $S = \{(0,0), (2,0), (2,2), (0,2), (1,1)\}$, the four triangles from the center to each side form a triangulation. Here $n = 5$, $h = 4$, so there are $2 \cdot 5 - 4 - 2 = 4$ triangles and $3 \cdot 5 - 4 - 3 = 8$ edges: four on the hull and four spokes.
- **Not a triangulation: a skipped point.** The two triangles $(0,0), (2,0), (2,2)$ and $(0,0), (2,2), (0,2)$ cover the square, but the point $(1,1)$ lies on their shared edge and is not a corner. This breaks condition 4. The edge from $(0,0)$ to $(2,2)$ passes through a point of $S$, so the subdivision is not a maximal planar subdivision of $S$ either.
- **Not a triangulation: a T-junction.** Cut the square $(0,0), (2,0), (2,2), (0,2)$ along its diagonal from $(0,0)$ to $(2,2)$. Keep the lower triangle $(0,0), (2,0), (2,2)$ whole, and split the upper one at the midpoint $m = (1,1)$ of the diagonal into $(0,0), m, (0,2)$ and $m, (2,2), (0,2)$. The lower triangle and $(0,0), m, (0,2)$ meet in the segment from $(0,0)$ to $m$, which is a whole edge of one but only half an edge of the other. The pieces do not meet edge to edge. Splitting the lower triangle at $m$ as well repairs this and gives the square with its center from the first example.
- **A convex polygon.** A convex $n$-gon with no three vertices collinear has $C_{n-2}$ triangulations, where $C_k$ is the $k$-th [Catalan number](/catalan-triangulation-theorem/); a square has 2 and a convex hexagon has 14.
- **Delaunay triangulation.** Among the triangulations of a point set, the [Delaunay triangulation](/delaunay-triangulation/) is the one whose triangles have empty circumcircles. It exists for every point set not all on a line.
- **Collinear points.** If all points of $S$ lie on one line, the convex hull is a segment, and there is no triangle of positive area. Such sets have no triangulation in this sense.

## Related definitions

- [Triangulation of a point set](/triangulation-of-point-set/) and [polygon triangulation](/polygon-triangulation/): the two problems of computing a triangulation.
- [Triangulation counting theorem](/triangulation-counting-theorem/): the numbers of triangles and edges.
- [Edge flip](/edge-flip/) and [flip graph](/flip-graph/): moving between triangulations of the same point set.
- [Constrained triangulation](/constrained-triangulation/): triangulations that must contain given segments.
- [Steiner points](/steiner-points/): extra vertices that are not in the input.
- [Tetrahedralization](/tetrahedralization/): the three-dimensional analogue, made of tetrahedra.
- [Maximal planar graph](/maximal-planar-graph/) and [outerplanar graph](/outerplanar-graph/): the graphs of point set and polygon triangulations.
- [Regular triangulation](/regular-triangulation/): triangulations obtained by projecting a lifted convex hull, which include the Delaunay triangulation.

## References
