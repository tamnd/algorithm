---
tag: C3P34G
kind: definition
slug: in-circle-test
name: In-circle test
aliases:
- incircle test
- incircle predicate
- InCircle
area: geometry/voronoi-and-delaunay
level: core
summary: Geometric predicate deciding whether a point lies inside a triangle's circumcircle.
prereqs: [circumcircle, orientation-test]
see_also: [empty-circle-property, local-delaunay-criterion, paraboloid-lifting-map, lawson-flip-algorithm, bowyer-watson-algorithm, regular-triangulation, general-position-delaunay, delaunay-triangulation]
sources:
  - paper: doi:10.1145/282918.282923
    title: L. Guibas and J. Stolfi, Primitives for the manipulation of general subdivisions and the computation of Voronoi diagrams, ACM Transactions on Graphics 4(2), 1985
    locator: the InCircle predicate, its determinant form and its use as the only geometric test besides the orientation test
  - paper: "J. R. Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 1997, 305-363"
    locator: the exact and adaptive evaluation of the orientation and in-circle determinants
  - book: isbn:9781584887300
    title: S.-W. Cheng, T. K. Dey and J. R. Shewchuk, Delaunay Mesh Generation, CRC Press, 2013
    locator: Chapter 2 (the in-circle predicate and the lifting map)
---

The in-circle test takes three points $a$, $b$, $c$ in counterclockwise order and a fourth point $d$, and says whether $d$ is strictly inside, on, or strictly outside the [circumcircle](/circumcircle/) of $abc$. It is the sign of a $3 \times 3$ determinant whose entries are polynomials of degree at most $2$ in the coordinates, so on integer input it is computed exactly with integers. Together with the [orientation test](/orientation-test/), it is the only geometric decision that Delaunay algorithms need: the [empty circle property](/empty-circle-property/), the [local Delaunay criterion](/local-delaunay-criterion/), the [Lawson flip algorithm](/lawson-flip-algorithm/) and the [Bowyer-Watson algorithm](/bowyer-watson-algorithm/) all reduce to it.

## Definition

Notation: points are $p = (x, y)$, $P$ is a set of $n$ points with $h$ on its hull boundary, $|p|^2 = x^2 + y^2$, and $\mathrm{orient}(a, b, c)$ is the sign of $D(a, b, c) = (b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x)$, positive when $a, b, c$ turn counterclockwise. For points $a$, $b$, $c$, $d$ let

$$I(a, b, c, d) = \det \begin{pmatrix} a_x - d_x & a_y - d_y & |a - d|^2 \\ b_x - d_x & b_y - d_y & |b - d|^2 \\ c_x - d_x & c_y - d_y & |c - d|^2 \end{pmatrix}.$$

The **in-circle test** $\mathrm{incircle}(a, b, c, d)$ is the sign of $I(a, b, c, d)$. The same number is the $4 \times 4$ determinant with rows $(p_x, p_y, |p|^2, 1)$ for $p = a, b, c, d$, up to the sign of the row order; subtracting the row of $d$ from the others and expanding along the last column gives the $3 \times 3$ form.

**The identity.** If $\mathrm{orient}(a, b, c) \ne 0$, with circumcenter $o$ and circumradius $R$,

$$I(a, b, c, d) = D(a, b, c) \left( R^2 - |d - o|^2 \right).$$

*Proof.* Let $f(q) = 2 o \cdot q + R^2 - |o|^2$. It is affine, and $f(q) - |q|^2 = R^2 - |q - o|^2$, so $f = |\cdot|^2$ at $a$, $b$, $c$. The third entry of the row of $a$ is $|a|^2 - |d|^2 - 2 d \cdot (a - d)$. Subtracting $-2 d_x$ times the first column and $-2 d_y$ times the second leaves $|a|^2 - |d|^2$. Since $|a|^2 = f(a)$ and $f(a) - f(d) = 2 o \cdot (a - d)$, the entry is $2 o \cdot (a - d) + (f(d) - |d|^2)$; subtracting $2 o_x$ times the first column and $2 o_y$ times the second leaves $f(d) - |d|^2$ in every row. The determinant is then $(f(d) - |d|^2)$ times the determinant with rows $(a - d, 1)$, $(b - d, 1)$, $(c - d, 1)$, which is $D(a, b, c)$. $\square$

So for counterclockwise $a, b, c$: $\mathrm{incircle} > 0$ when $d$ is strictly inside the circle, $= 0$ on it, and $< 0$ strictly outside. For clockwise $a, b, c$ the signs are reversed. In the [lifting map](/paraboloid-lifting-map/) view, $f(d) - |d|^2$ is the height of the plane through the lifted $a$, $b$, $c$ above the lifted $d$: inside the circle means below the plane.

**Properties.**

- **Exactness.** On integers with absolute value at most $M$, the entries have absolute value at most $2M$ and $8M^2$, so $|I| \le 6 \cdot 2M \cdot 2M \cdot 8M^2 = 192 M^4$. Integer arithmetic of this size gives the exact sign; Python integers have no limit.
- **Symmetry.** $I$ does not change under a cyclic shift of $a, b, c$, changes sign under a swap of two of them, and does not change under translation of all four points.
- **Collinear $a$, $b$, $c$.** Then $I(a, b, c, d) = 0$ exactly when $d$ is on their line, since the lifted points of $a$, $b$, $c$ then span a vertical plane. Off the line the sign tells the side, but which side is positive depends on the order of $a$, $b$, $c$ on the line. Algorithms call the test only on triangles that are not flat, or treat this case on its own.
- **Weights.** Replacing $|p|^2$ in the third column by $|p|^2 - w_p$ gives the power test of the [regular triangulation](/regular-triangulation/).

## Examples and non-examples

- **Inside.** For $a = (0,0)$, $b = (6,0)$, $c = (3,5)$, $d = (3,2)$: the rows are $(-3, -2, 13)$, $(3, -2, 13)$, $(0, 3, 9)$ and $I = 342 > 0$. By the identity, $D = 30$, the circumcenter is $(3, \frac{8}{5})$, $R^2 = \frac{289}{25}$ and $|d - o|^2 = \frac{4}{25}$, so $I = 30 \cdot \frac{285}{25} = 342$.
- **Outside.** For the same triangle and $d = (6,4)$: the rows are $(-6, -4, 52)$, $(0, -4, 16)$, $(-3, 1, 10)$ and $I = -96 < 0$; here $|d - o|^2 = \frac{369}{25}$ and $30 \cdot \frac{-80}{25} = -96$.
- **On the circle.** For $(0,0), (4,0), (4,3)$ and $d = (0,3)$, the four corners of a rectangle, $I = 0$. A Delaunay code must accept either diagonal of such a quadrilateral; see [general position](/general-position-delaunay/).
- **Non-example: clockwise input.** For $a = (0,0)$, $b = (3,5)$, $c = (6,0)$ and $d = (3,2)$, the value is $-342$ although $d$ is inside. Codes that do not fix the orientation first get the answer backwards.
- **Non-example: floating point.** For points that are nearly cocircular, the rounded determinant can have the wrong sign, and a flip algorithm can then loop or produce crossing edges. Exact integers or adaptive exact arithmetic avoid this.

## Related definitions

- [Orientation test](/orientation-test/): the sign of $D(a, b, c)$, the $2 \times 2$ analogue; $I$ is the orientation test of the lifted points in space.
- [Empty circle property](/empty-circle-property/): $\mathrm{incircle}(a, b, c, q) \le 0$ for every point $q$ of the set.
- [Local Delaunay criterion](/local-delaunay-criterion/): the in-circle test across a single edge.
- **In-sphere test**: the $(d+1) \times (d+1)$ analogue for $d + 2$ points in $d$ dimensions, used by the [higher-dimensional Delaunay triangulation](/higher-dimensional-delaunay/).

## References
