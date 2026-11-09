---
tag: DRDMDB
kind: problem
slug: polygon-area
name: Polygon area
aliases:
- area of a simple polygon
- area of a polygon
- polygon area computation
area: geometry/polygons
level: intro
summary: Compute the area enclosed by a simple polygon given its vertices.
prereqs: [polygon, simple-polygon]
see_also: [shoelace-formula, picks-theorem, polygon-triangulation, polygon-orientation, polygon-with-holes, polygon-union, winding-number-algorithm, oriented-triangle-area]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.3, Area of polygon (the area from a triangulation, then from a fan of signed triangles, and the code)
  - paper: doi:10.1080/07468342.1986.11972974
    title: Bart Braden, The surveyor's area formula, The College Mathematics Journal 17(4), 326 to 337 (1986)
    locator: the whole article (the formula, its proof by Green's theorem, and its history)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1, the signed area of a triangle as a determinant
---

The polygon area problem asks for the area of the region enclosed by a [simple polygon](/simple-polygon/), given its vertices in order around the boundary. It has an exact answer in $\Theta(n)$ time: the [shoelace formula](/shoelace-formula/) adds the signed areas of the triangles that one fixed point makes with the edges, and on integer coordinates twice the area is an integer. The problem is a base step of many others, from [polygon orientation](/polygon-orientation/) and centroids to the areas of unions and intersections, and its variants for self-intersecting polygons and polygons with holes have answers that depend on how the region is defined.

## In plain words

You are given the corners of a field, in order around its edge, and you want its area. Cutting the field into triangles and adding their areas works, but finding a good cut is work.

A simpler way picks one fixed point, makes a triangle from that point and each side of the field, and adds the triangle areas with a sign: positive when the side goes one way around the point, negative when it goes back. The parts outside the field cancel, and what is left is exactly the field. Each triangle costs two multiplications, so the work is one step per corner.

## Definition

**Input.** A simple polygon $P = (v_0, \ldots, v_{n-1})$, $v_i = (x_i, y_i) \in \mathbb{R}^2$, in either orientation, with edges $v_i v_{i+1}$ and indices mod $n$.

**Output.** The area $\operatorname{area}(P) = \iint_{R} 1\, dx\, dy$ of the closed region $R$ bounded by $P$, which exists by the [Jordan curve theorem](/jordan-curve-theorem/). The **signed area** is $+\operatorname{area}(P)$ for a counterclockwise and $-\operatorname{area}(P)$ for a clockwise vertex order.

**Model.** The [real RAM](/real-ram/), with exact additions and multiplications of coordinates. With integer coordinates of absolute value at most $M$, twice the area is an integer of absolute value at most $8 M^2$, every partial sum has absolute value at most $2 n M^2$, and integer arithmetic is exact.

**The identity behind the problem.** For every polygon,

$$\frac12 \sum_{i=0}^{n-1} (x_i\, y_{i+1} - x_{i+1}\, y_i) = \iint w_P(q)\, dq,$$

where $w_P(q)$ is the [winding number](/winding-number-algorithm/) of the boundary around $q$. For a simple polygon, $w_P$ is $\pm 1$ inside and 0 outside, so the left side is the signed area. The proof, by a fan of signed triangles from the origin and by Green's theorem, is on the [shoelace formula](/shoelace-formula/) page.

## Variants

- **Signed area.** Return the area with the sign of the orientation; this is what the shoelace formula computes, and its sign solves [polygon orientation](/polygon-orientation/).
- **Polygon with holes.** For a [polygon with holes](/polygon-with-holes/) the area is the area of the outer contour minus the areas of the holes. With the outer contour counterclockwise and the holes clockwise, it is the sum of the signed areas of all contours.
- **Self-intersecting polygons.** The boundary no longer encloses one region. The shoelace sum gives the integral of the winding number, which counts a region twice where the boundary winds twice and cancels regions of opposite winding. The area of the region under a fill rule, $\{w_P \ne 0\}$ or $\{w_P \text{ odd}\}$, is a different quantity and needs the arrangement of the edges, for example by [Vatti clipping](/vatti-clipping/) of the polygon with itself followed by the shoelace formula.
- **Union and intersection.** The area of a union of polygons is the [polygon union](/polygon-union/) problem; for axis-parallel rectangles it is the [area of union of rectangles](/area-of-union-of-rectangles/).
- **Lattice polygons.** For a polygon with integer vertices, [Pick's theorem](/picks-theorem/) relates the area to lattice points: $\operatorname{area} = I + B/2 - 1$, with $I$ interior and $B$ boundary lattice points.
- **Moments.** The centroid and the moments of inertia come from the same fan of triangles, weighting each triangle by its own centroid or moment.
- **Curved boundaries.** For a region bounded by arcs or splines, Green's theorem $\operatorname{area} = \oint x\, dy$ still applies edge by edge, with an integral over each curved piece.

## Examples

- **A right triangle.** $(0,0), (4,0), (0,3)$: the shoelace sum is $0 + 12 + 0 = 12$, so the area is 6.
- **A concave pentagon.** $(0,0), (6,0), (6,4), (3,1), (0,4)$: the terms are $0, 24, -6, 12, 0$, with sum 30, so the area is 15. This is the $6 \times 4$ rectangle minus the notch, the triangle $(6,4), (3,1), (0,4)$ of area 9. Pick's theorem agrees: $B = 6 + 4 + 3 + 3 + 4 = 20$ boundary lattice points, $I = 6$ interior ones, and $6 + 10 - 1 = 15$.
- **Clockwise order.** The same pentagon listed as $(0,4), (3,1), (6,4), (6,0), (0,0)$ gives the sum $-30$: signed area $-15$, area 15.
- **A square with a hole.** The outer square $(0,0), (4,0), (4,4), (0,4)$ with signed area 16 and the hole $(1,1), (1,3), (3,3), (3,1)$ with signed area $-4$ give the area 12.
- **A bowtie.** $(0,0), (2,2), (2,0), (0,2)$ is not simple. Its shoelace sum is 0, since the two triangles of area 1 wind in opposite directions, but the region it covers has area 2.

## Known algorithms

| algorithm | time | idea |
| --- | --- | --- |
| [shoelace formula](/shoelace-formula/) | $\Theta(n)$ | half the sum of the cross products $v_i \times v_{i+1}$ |
| triangulate, then add triangle areas | $O(n \log n)$ or $O(n^2)$ in practice, $O(n)$ in theory | [polygon triangulation](/polygon-triangulation/) or [ear clipping](/ear-clipping/), then $n - 2$ [triangle areas](/oriented-triangle-area/) |
| trapezoids | $\Theta(n)$ | $\frac12 \sum (x_{i+1} - x_i)(y_{i+1} + y_i)$, the signed trapezoids between each edge and the x axis; expanding it gives minus the shoelace sum |
| [Pick's theorem](/picks-theorem/) | needs the lattice point counts | for lattice polygons; used more often in the other direction, to count interior points from the area |
| raster counting | grows with the resolution | [scanline fill](/scanline-polygon-fill/) of a pixel grid; approximate |

The shoelace formula is the method used in practice: one pass, two multiplications per vertex, no special cases, and exact on integers.

## Bounds

- **Upper bound.** $O(n)$ time and $O(1)$ extra space on the real RAM, by the shoelace formula. The algorithm reads the vertices once, in order, so it also works on a stream.
- **Lower bound.** $\Omega(n)$: every coordinate must be read. Take a convex polygon in which no two vertices share an x or a y coordinate. The terms of the shoelace sum that contain $v_i$ add up to $v_i \times (v_{i+1} - v_{i-1})$, so moving $v_i$ right by a small $\delta$ keeps the polygon simple and changes the area by $\frac12 \delta\, |y_{i+1} - y_{i-1}| \ne 0$. An algorithm that never reads $x_i$ gives the same answer on both polygons, so it is wrong on one of them; the same holds for $y_i$.
- **Exactness.** On integer input the answer is half an integer, computed with numbers of size $O(n M^2)$; on floating-point input the sum can lose all relative accuracy when the area is small compared to the coordinates, and translating the polygon so that a vertex is at the origin first reduces the error.

## Reductions

- **Orientation to area.** The orientation of a simple polygon is the sign of its signed area. It can also be found without the area, by one [orientation test](/orientation-test/) at the lowest-leftmost vertex.
- **Clipping and union to area.** The area of $P \cap Q$, $P \cup Q$ or $P \setminus Q$ is the area of the output of [polygon clipping](/polygon-clipping/), summed over the output contours with their signs.
- **Area of a polygon with holes to areas of simple polygons.** Sum the signed areas of the contours.

## Applications

- **Surveying and maps.** The area of a land parcel from the coordinates of its corners is the original use of the formula, and GIS software computes areas of map polygons this way, after projecting them to a plane.
- **Geometry kernels.** Areas give orientations, centroids and moments for physics engines and CAD systems.
- **Image analysis.** The area of a contour traced from a binary image, for example by marching squares.
- **Validation.** A polygon with area 0, or a hole with the wrong sign, is often a sign of bad input data.

## References
