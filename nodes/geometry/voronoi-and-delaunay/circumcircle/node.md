---
tag: AXRMV3
kind: definition
slug: circumcircle
name: Circumcircle
aliases:
- circumscribed circle
- circumdisk
area: geometry/voronoi-and-delaunay
level: intro
summary: The unique circle passing through the three vertices of a triangle.
prereqs: [euclidean-distance, orientation-test]
see_also: [circumcenter, in-circle-test, empty-circle-property, delaunay-triangulation, paraboloid-lifting-map, minimum-enclosing-circle, general-position-delaunay]
sources:
  - book: isbn:9783540779735
    title: M. de Berg, O. Cheong, M. van Kreveld and M. Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Section 9.2 (the empty circle characterization of Delaunay triangles and edges)
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 2 (circumcircles, circumdisks, the in-circle predicate and the lifting map)
---

The circumcircle of a triangle is the circle that passes through its three vertices. Every three points that are not on one line have exactly one such circle. Its center is the [circumcenter](/circumcenter/), and its radius is the circumradius. Circumcircles are the central object of Delaunay triangulations: a triangulation is a [Delaunay triangulation](/delaunay-triangulation/) when no point lies strictly inside the circumcircle of any of its triangles, the [empty circle property](/empty-circle-property/).

## Definition

Let $a$, $b$, $c$ be points of the plane with $\mathrm{orient}(a, b, c) \ne 0$. The **circumcircle** of $abc$ is the circle

$$C(a, b, c) = \{z : |z - o| = R\},$$

where $o$ is the circumcenter and $R = |o - a|$ the circumradius. The **open circumdisk** is $\{z : |z - o| < R\}$; a point in it is **strictly inside** the circumcircle. The circle is unique: a circle through $a$, $b$, $c$ has its center at the same distance from the three points, so on the perpendicular bisectors of $ab$ and $ac$, and these two lines meet in exactly one point because $ab$ and $ac$ are not parallel.

Two formulas are useful.

- **Radius from the sides.** With side lengths $|bc| = \ell_a$, $|ca| = \ell_b$, $|ab| = \ell_c$ and area $K$, $R = \ell_a \ell_b \ell_c / (4K)$. By the law of sines, $R = \ell_a / (2 \sin \angle a)$.
- **Determinant form.** A point $z$ is on the circle through $a$, $b$, $c$ exactly when

$$\det \begin{pmatrix} a_x & a_y & a_x^2 + a_y^2 & 1 \\ b_x & b_y & b_x^2 + b_y^2 & 1 \\ c_x & c_y & c_x^2 + c_y^2 & 1 \\ z_x & z_y & z_x^2 + z_y^2 & 1 \end{pmatrix} = 0.$$

The sign of this determinant tells inside from outside; this is the [in-circle test](/in-circle-test/). Seen through the [paraboloid lifting map](/paraboloid-lifting-map/), the circle is the projection of the intersection of the paraboloid $w = x^2 + y^2$ with the plane through the three lifted points.

**Inscribed angles.** For a chord $ab$ of the circle and points $c$, $d$ on the same side of the line $ab$, the angle $\angle acb$ is the same for $c$ on the circle, larger for $c$ strictly inside, and smaller for $c$ strictly outside. This fact (Thales and the inscribed angle theorem) is the key step in the proof of the [max-min angle property](/delaunay-max-min-angle/).

## Examples and non-examples

- **Integer data.** For $(0,0), (6,0), (3,5)$ the circumcircle has center $(3, 8/5)$ and squared radius $289/25$. The point $(3,2)$ is inside, since $(3-3)^2 + (2 - 8/5)^2 = 4/25 < 289/25$; the point $(6,4)$ is outside.
- **Four points on one circle.** The corners of the rectangle $(0,0), (4,0), (4,3), (0,3)$ lie on the circle with center $(2, 3/2)$ and radius $5/2$. Any three of them have the same circumcircle, and the fourth is on it, not inside. So both diagonals give a Delaunay triangulation of the rectangle; see [general position](/general-position-delaunay/).
- **The 12 integer points with $x^2 + y^2 = 25$.** Every triangle on three of them has the circumcircle $x^2 + y^2 = 25$. Such sets are used to test Delaunay codes on degenerate input.
- **Non-example: collinear points.** $(0,0), (1,0), (2,0)$ have no circumcircle. As a limit, the circle through $a$, $b$ and $c$ becomes the line through them when $c$ moves onto that line.
- **Non-example: the smallest enclosing circle.** The circumcircle of an obtuse triangle is not its smallest enclosing circle; the circle with the longest side as diameter is smaller and still holds the triangle. See [minimum enclosing circle](/minimum-enclosing-circle/).

## Related definitions

- [Circumcenter](/circumcenter/): the center of the circumcircle.
- [In-circle test](/in-circle-test/): the predicate that compares a point with a circumcircle.
- [Empty circle property](/empty-circle-property/): no input point strictly inside the circumcircle of any triangle.
- **Diametral circle** of a segment $uv$: the circle with $uv$ as diameter. It is the smallest circle through $u$ and $v$ and defines the [Gabriel graph](/gabriel-graph/).
- **Circumsphere**: the sphere through the $d + 1$ vertices of a simplex in $d$ dimensions, used by the [higher-dimensional Delaunay triangulation](/higher-dimensional-delaunay/).

## References
