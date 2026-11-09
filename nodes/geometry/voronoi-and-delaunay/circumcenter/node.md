---
tag: HRFDPQ
kind: definition
slug: circumcenter
name: Circumcenter
area: geometry/voronoi-and-delaunay
level: intro
summary: Center of a triangle's circumcircle; it is the Voronoi vertex of the triangle's three sites.
prereqs: [circumcircle, euclidean-distance]
see_also: [in-circle-test, voronoi-diagram, delaunay-triangulation, voronoi-delaunay-duality, largest-empty-circle, minimum-enclosing-circle, determinant]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Sections 7.1 and 9.2 (Voronoi vertices as centers of empty circles through three sites, and the Delaunay triangles)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 5 (Voronoi vertices and the circumcircles of Delaunay triangles)
---

The circumcenter of a triangle $abc$ is the point at the same distance from its three vertices. It is the center of the [circumcircle](/circumcircle/), and it is the point where the perpendicular bisectors of the three sides meet. If $abc$ is a triangle of the [Delaunay triangulation](/delaunay-triangulation/) of a point set, its circumcenter is a vertex of the [Voronoi diagram](/voronoi-diagram/) of that set, and each Voronoi vertex arises in this way.

## Definition

Let $a$, $b$, $c$ be three points of the plane that are not on one line, so that $\mathrm{orient}(a, b, c) \ne 0$. The **circumcenter** $o$ of $abc$ is the unique point with

$$|o - a| = |o - b| = |o - c|,$$

and this common distance $R$ is the **circumradius**. With $b' = b - a$, $c' = c - a$ and $D = 2 (b'_x c'_y - b'_y c'_x)$, which is twice the signed area of the parallelogram and is not zero,

$$o = a + \left( \frac{c'_y |b'|^2 - b'_y |c'|^2}{D},\ \frac{b'_x |c'|^2 - c'_x |b'|^2}{D} \right).$$

The formula follows from the two linear equations $2 b' \cdot (o - a) = |b'|^2$ and $2 c' \cdot (o - a) = |c'|^2$, which say that $o$ is on the perpendicular bisectors of $ab$ and $ac$; Cramer's rule solves them. For integer coordinates, $o$ has rational coordinates with denominator $D$, so it can be computed exactly with fractions. Three points on one line have no circumcenter: $D = 0$ and the bisectors are parallel.

The position of $o$ depends on the angles of the triangle: $o$ is strictly inside the triangle when all angles are acute, at the midpoint of the longest side when one angle is right, and strictly outside, beyond the longest side, when one angle is obtuse.

## Examples and non-examples

- **Right triangle.** For $(0,0), (4,0), (0,3)$, $D = 24$ and $o = (2, 3/2)$, the midpoint of the hypotenuse, with $R = 5/2$.
- **Acute triangle.** For $(0,0), (6,0), (3,5)$, $o = (3, 8/5)$, inside the triangle, with $R^2 = 289/25$.
- **Obtuse triangle.** For $(0,0), (4,0), (1,1)$, $D = 8$ and $o = (2, -1)$, outside the triangle, below the long side; $R^2 = 5$, and indeed $(1 - 2)^2 + (1 + 1)^2 = 5$.
- **A Voronoi vertex.** The three sites $(0,5)$, $(3,4)$, $(-4,3)$ have circumcenter $(0,0)$. No other site is given, so the circle of radius $5$ is empty and $(0,0)$ is the one vertex of their Voronoi diagram, where the three Voronoi edges meet.
- **Non-example: collinear points.** $(0,0), (1,1), (3,3)$ have $D = 0$ and no circumcenter. Their Voronoi diagram has two parallel edges and no vertex.
- **Non-example: not a Voronoi vertex.** If a fourth site lies strictly inside the circle, the circumcenter of the first three is nearer to that site, so it is not a vertex of the Voronoi diagram of all four.

## Related definitions

- The [circumcircle](/circumcircle/) is the circle with center $o$ and radius $R$.
- The [in-circle test](/in-circle-test/) decides on which side of the circumcircle a fourth point lies, without computing $o$.
- A **Voronoi vertex** is a point at the same distance from three or more sites, with no site nearer; it is the circumcenter of every [Delaunay](/delaunay-triangulation/) triangle of those sites, by the [duality](/voronoi-delaunay-duality/).
- The center of the [largest empty circle](/largest-empty-circle/) among points, when it is not on the boundary of the region, is a circumcenter of a Delaunay triangle.
- The [minimum enclosing circle](/minimum-enclosing-circle/) has as center either the midpoint of two points or the circumcenter of three.
- In $d$ dimensions, $d + 1$ affinely independent points have a circumcenter, the center of their circumsphere, found by the same linear system with $d$ equations.

## References
