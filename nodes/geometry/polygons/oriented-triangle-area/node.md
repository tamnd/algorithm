---
tag: PA94WX
kind: concept
slug: oriented-triangle-area
name: Oriented area of a triangle
aliases:
- signed area of a triangle
- signed triangle area
- Area2
area: geometry/polygons
level: intro
summary: Signed area of a triangle computed from the cross product of two edge vectors, whose sign gives the orientation of its vertices.
prereqs: [cross-product]
see_also: [orientation-test, shoelace-formula, polygon-area, polygon-orientation, picks-theorem, point-to-line-distance, determinant, geometry-primitives]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.3, Area of Polygon (the determinant form of twice the signed area, Area2, and the sum of triangle areas from a fixed point)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1 (the 3 by 3 determinant whose value is twice the signed area of a triangle, and its use as the turn test)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.1 (the left-turn test as the sign of a determinant)
---

The oriented (signed) area of a triangle $p, q, r$ is $A(p, q, r) = \frac12 (q - p) \times (r - p)$, half the [cross product](/cross-product/) of two edge vectors. Its absolute value is the usual area, and its sign is positive when the vertices are in counterclockwise order, negative when they are clockwise, and zero when they are collinear. The sign is the [orientation test](/orientation-test/), the sum over a fan of triangles gives the area of a polygon by the [shoelace formula](/shoelace-formula/), and the ratios of such areas are barycentric coordinates.

## In plain words

Draw a triangle and walk around it, from the first corner to the second, to the third and back. If the inside of the triangle is on your left all the time, you walk counterclockwise and the area gets a plus sign. If it is on your right, the area gets a minus sign. If the three corners are on one straight line, there is no inside and the area is zero. The formula needs only a few multiplications and subtractions of the coordinates, and no square roots or angles. With whole-number corners it gives the exact value, which is always a whole number or a half.

## The idea

**Notation.** Points are $p = (x, y)$, and $\operatorname{orient}(p, q, r)$ is the sign of $(q - p) \times (r - p)$, as on [point and vector](/point-and-vector/). We write

$$2A(p, q, r) = (q - p) \times (r - p) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x).$$

Programs compute $2A$, which is an integer for integer input, and divide by 2 only at the end, if at all.

**The determinant form.** Subtracting the first column from the other two does not change a determinant, so

$$2A(p, q, r) = \det \begin{pmatrix} 1 & 1 & 1 \\ p_x & q_x & r_x \\ p_y & q_y & r_y \end{pmatrix}.$$

This form shows that $A$ is unchanged by a translation and by a cyclic shift of the three points, and that it changes sign when two points are swapped.

**Additivity.** For any point $o$,

$$A(p, q, r) = A(o, p, q) + A(o, q, r) + A(o, r, p).$$

*Proof.* Bilinearity of $\times$ gives $(p - o) \times (q - o) = p \times q + o \times p - o \times q$. Add the three such terms for the pairs $(p, q)$, $(q, r)$, $(r, p)$. The terms with $o$ sum to $o \times (p - q + q - r + r - p) = 0$, so the total is $p \times q + q \times r + r \times p$. The same computation with $o = p$ shows that $2A(p, q, r)$ also equals $p \times q + q \times r + r \times p$. $\square$

With $o$ outside the triangle, some of the three terms are negative, and the signs cancel the area outside. The same identity for a polygon $v_0, \ldots, v_{n-1}$ and $o$ at the origin is the [shoelace formula](/shoelace-formula/): $2A = \sum_i v_i \times v_{i+1}$.

**Barycentric coordinates.** Let $A(p, q, r) \ne 0$. Each point $x$ of the plane is the affine combination $x = \lambda_p p + \lambda_q q + \lambda_r r$ with

$$\lambda_p = \frac{A(x, q, r)}{A(p, q, r)}, \quad \lambda_q = \frac{A(p, x, r)}{A(p, q, r)}, \quad \lambda_r = \frac{A(p, q, x)}{A(p, q, r)},$$

and $\lambda_p + \lambda_q + \lambda_r = 1$ by additivity with $o = x$. The point $x$ is inside the closed triangle if and only if all three are $\ge 0$, on its boundary if one is $0$ and the others are $\ge 0$, and at a vertex if two are $0$. Only the signs of the three numerators matter for this test, so it is exact with integer input.

**Height and distance.** The area is half the base times the height, so the distance from $r$ to the line through $p \ne q$ is $|2A(p, q, r)| / |q - p|$. This is the base of the [point-to-line distance](/point-to-line-distance/).

**Half-integers.** If $p, q, r$ have integer coordinates, $2A$ is an integer, so $A$ is a multiple of $\frac12$. [Pick's theorem](/picks-theorem/) explains which half-integer it is from the lattice points in and on the triangle.

## Examples

**A clockwise triangle.** For $p = (2, 1)$, $q = (5, 5)$ and $r = (6, 2)$: $2A = 3 \cdot 1 - 4 \cdot 4 = -13$. The triangle is clockwise with area $13/2$. In the order $p, r, q$ it is counterclockwise, with $2A = 13$.

**Barycentric coordinates.** Use the counterclockwise order $P = (2, 1)$, $Q = (6, 2)$, $R = (5, 5)$, with $2A(P, Q, R) = 13$, and the point $x = (4, 3)$. The three numerators are $2A(x, Q, R) = 5$, $2A(P, x, R) = 2$ and $2A(P, Q, x) = 6$, all positive, so $x$ is inside. The coordinates are $\frac{5}{13}, \frac{2}{13}, \frac{6}{13}$, they sum to 1, and $\frac{5}{13}(2,1) + \frac{2}{13}(6,2) + \frac{6}{13}(5,5) = (4, 3)$.

**Points outside and on the boundary.** For $x = (6, 6)$ the numerators are $-4, 1, 16$: the negative one says that $x$ is beyond the edge $QR$. For $x = (4, 1)$ they are $7, 8, -2$: $x$ is beyond the edge $PQ$. For $x = R = (5, 5)$ they are $0, 0, 13$: two zeros mean a vertex.

**Any reference point.** With $o = (100, -7)$, far outside the triangle, $2A(o, P, Q) + 2A(o, Q, R) + 2A(o, R, P) = 13$, the same as $2A(P, Q, R)$.

**Distance.** The distance from $r = (6, 2)$ to the line through $p = (2, 1)$ and $q = (5, 5)$ is $13 / 5 = 2.6$.

## Where it is used

- The [orientation test](/orientation-test/) is the sign of $A$. It is the predicate of [Graham scan](/graham-scan/), [Andrew's monotone chain](/andrew-monotone-chain/), [segment intersection](/segment-intersection-detection/) and [ear clipping](/ear-clipping/).
- The [shoelace formula](/shoelace-formula/) and [polygon area](/polygon-area/) sum the oriented areas of a fan of triangles, and the sign of the total gives the [polygon orientation](/polygon-orientation/).
- [Point in convex polygon](/point-in-convex-polygon/) and the [crossing number algorithm](/crossing-number-algorithm/) use the sign of $A$ to decide on which side of an edge a point lies.
- [Pick's theorem](/picks-theorem/) relates the area of a lattice polygon to its lattice points.
- The [in-circle test](/in-circle-test/) is the analogous determinant one degree higher, for four points.

## References
