---
tag: RBTG43
kind: concept
slug: tensor-product-surface
name: Tensor-product surface
aliases:
- tensor product patch
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: A surface sum P_ij f_i(u) g_j(v) over a rectangular grid of control points, with a curve basis in each direction. It is a curve whose control points move along curves.
prereqs: [parametric-surface, tensor-product-interpolation]
see_also: [bezier-patch, b-spline, nurbs, de-casteljau-algorithm, de-boor-algorithm, bilinear-interpolation, bezier-triangle, partition-of-unity]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 14, Tensor Product Patches (bilinear patches, Bezier patches, the de Casteljau algorithm in both directions, derivatives and B-spline surfaces)
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Chapter 9, Tensor product surfaces
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 3, B-spline Curves and Surfaces (tensor product B-spline surfaces), and Section 8.2, Bilinear Surfaces
---

A tensor-product surface takes two curve bases, one in $u$ and one in $v$, and multiplies them. With bases $f_0, \dots, f_m$ and $g_0, \dots, g_n$ and a rectangular grid of $(m + 1)(n + 1)$ control points $P_{ij}$, the surface is $S(u, v) = \sum_i \sum_j P_{ij} f_i(u) g_j(v)$. [Bézier patches](/bezier-patch/), B-spline surfaces and [NURBS](/nurbs/) surfaces are all of this type, and almost every curve algorithm carries over to them by running it once in each direction. This page is about the surface representation. The page [tensor-product interpolation](/tensor-product-interpolation/) is about the numerical method that fits such a product to values on a grid.

## In plain words

Take a curve design system and use it twice. First pick a few curves that run across the surface in one direction, each from its own row of control points. Then, for each position along these curves, take the points they reach and use them as the control points of a new curve in the other direction. The new curves sweep out the surface. The order does not matter: running the rows first or the columns first gives the same surface. So the surface keeps the good properties of the curve system, such as staying inside the hull of its control points, and every curve tool, such as fast point evaluation or splitting, works on surfaces by doing it in one direction and then in the other.

## The idea

**Definition.** Let $f_0, \dots, f_m$ be functions of $u$ and $g_0, \dots, g_n$ functions of $v$, on intervals $I$ and $J$. The tensor-product surface with the control points $P_{ij} \in \mathbb{R}^3$ is

$$S(u, v) = \sum_{i=0}^{m} \sum_{j=0}^{n} P_{ij}\, f_i(u)\, g_j(v), \qquad (u, v) \in I \times J.$$

In matrix form, $S(u, v) = F(u)^{\mathsf T} P\, G(v)$ for each coordinate, where $F = (f_0, \dots, f_m)$, $G = (g_0, \dots, g_n)$ and $P$ is the $(m + 1) \times (n + 1)$ matrix of that coordinate of the control points. The functions $f_i(u) g_j(v)$ form the product basis. When the $f_i$ are independent and the $g_j$ are independent, the $(m + 1)(n + 1)$ products are independent, so every surface in the span has exactly one control net.

**A curve of curves.** Group the double sum by rows:

$$S(u, v) = \sum_{i=0}^{m} Q_i(v)\, f_i(u), \qquad Q_i(v) = \sum_{j=0}^{n} P_{ij}\, g_j(v).$$

For a fixed $v$ the surface curve $u \mapsto S(u, v)$ is a curve in the $u$ basis with the control points $Q_0(v), \dots, Q_m(v)$, and each $Q_i$ moves along a curve in the $v$ basis. Grouping by columns gives the same surface. This symmetry is the whole method: an algorithm for curves applied to the rows, then to the resulting points, gives the algorithm for the surface.

**What the surface inherits.** Each statement follows from the matching property of the two bases.

1. **Affine invariance.** If $\sum_i f_i = 1$ and $\sum_j g_j = 1$ ([partition of unity](/partition-of-unity/)), then $\sum_{i,j} f_i g_j = 1$, so an affine map of the control points maps the surface in the same way.
2. **Convex hull.** If also $f_i \ge 0$ and $g_j \ge 0$, then $S(u, v)$ is a convex combination of the $P_{ij}$, so the surface lies in their [convex hull](/convex-hull-property/).
3. **Boundary curves.** If $f_i(a) = 1$ for $i = 0$ and 0 otherwise at the end $a$ of $I$, as for Bernstein and clamped B-spline bases, then $S(a, v) = \sum_j P_{0j} g_j(v)$: the boundary is the curve of the first row of the net.
4. **Derivatives.** $S_u = \sum_{i,j} P_{ij} f_i'(u) g_j(v)$, so a partial derivative is again a tensor-product surface, with the derivative basis in one direction. Mixed partials come from both.
5. **Local control.** With B-spline bases each $f_i g_j$ is zero outside a rectangle of knot spans, so moving $P_{ij}$ changes only that rectangle of the surface.

**Not every surface is a tensor product.** The product of two polynomial bases of degrees $m$ and $n$ spans the polynomials of degree at most $m$ in $u$ and at most $n$ in $v$, a space of dimension $(m + 1)(n + 1)$. The polynomials of total degree at most $n$ form a different space, of dimension $(n + 1)(n + 2)/2$, on a triangular domain. That space is the [Bézier triangle](/bezier-triangle/). For $n = 3$ the counts are 16 and 10 control points. A rectangular grid also has a fixed topology, a disk with four corners, so a closed surface or one with an $n$-sided region needs several patches joined along their edges; see [smooth surface from a control mesh](/surface-from-control-mesh/).

**Cost of a point.** In the Bernstein basis the curve version of [de Casteljau](/de-casteljau-algorithm/) costs $k(k + 1)/2$ linear interpolations for degree $k$. Running it on the $m + 1$ rows (degree $n$ in $v$) and then once on the result (degree $m$ in $u$) costs

$$(m + 1)\,\frac{n(n + 1)}{2} + \frac{m(m + 1)}{2}$$

interpolations of points. The other order costs the same with $m$ and $n$ swapped. The difference of the two is $m n (n - m) / 2$, so the order that starts along the lower degree is cheaper, and the two are equal when $m = n$ or when one of the degrees is 0. These are exact operation counts per point, the same for every input. For B-splines the same scheme runs the [de Boor algorithm](/de-boor-algorithm/) in each direction.

## Examples

- **The bilinear patch.** With $m = n = 1$ and the linear Bernstein basis $1 - t, t$, the surface $S = (1 - u)(1 - v) P_{00} + u(1 - v) P_{10} + (1 - u) v P_{01} + uv P_{11}$ is the [bilinear interpolant](/bilinear-interpolation/) of the four corners. With the corners $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(1, 1, 1)$ it is the saddle $z = xy$ over the unit square. Every $u$-curve and every $v$-curve is a straight line, so the patch is also a [ruled surface](/ruled-surface/) in two ways.
- **A biquadratic Bézier patch.** The net with $P_{ij} = (i, j, z_{ij})$, where $z_{ij}$ is 0 at the corners, 1 at the edge midpoints and 4 at the center, is worked on the [Bézier patch](/bezier-patch/) page. The rows at $v = 1/2$ give the points $(0, 1, 1/2)$, $(1, 1, 5/2)$, $(2, 1, 1/2)$, and the curve through these gives $S(1/2, 1/2) = (1, 1, 3/2)$. Columns first gives the same point.
- **Operation counts.** A bicubic patch ($m = n = 3$) costs $4 \cdot 6 + 6 = 30$ interpolations per point in either order. A patch of degree $(3, 1)$ costs $4 \cdot 1 + 6 = 10$ along $v$ first and $2 \cdot 6 + 1 = 13$ along $u$ first.
- **Mixed bases.** A cylinder over a cubic profile curve is the tensor product of a cubic Bernstein basis in $u$ and the linear basis $1 - v, v$ in $v$, with the net made of the profile's control points and a translated copy.
- **Tensor-product B-spline surface.** With cubic B-spline bases over knot vectors in $u$ and $v$, a net of $(m + 1)(n + 1)$ points gives a surface with continuous second derivatives. If the net is a regular grid of a quad mesh, this is the limit surface of [Catmull-Clark subdivision](/catmull-clark-subdivision/) away from the extraordinary vertices.
- **Non-example: the Coons patch.** A bilinearly blended [Coons patch](/coons-patch/) is built from four boundary curves, not from a net. It is a tensor-product polynomial patch only when the four curves are polynomials; then it equals a Bézier patch whose net the Coons formula gives.
- **Non-example: the Bézier triangle.** Its basis $\binom{n}{i,j,k} r^i s^j t^k$ with $i + j + k = n$ is not a product of a basis in one variable and a basis in another.

## Where it is used

- [Bézier patch](/bezier-patch/): the tensor product of two Bernstein bases. [B-spline](/b-spline/) and [NURBS](/nurbs/) surfaces: the tensor products of B-spline bases, the standard surfaces of CAD file formats.
- [De Casteljau](/de-casteljau-algorithm/) and [de Boor](/de-boor-algorithm/) algorithms: the curve evaluators that surface evaluation runs in each direction. Knot insertion and subdivision work on each row of the net in the same way.
- [Tensor-product interpolation](/tensor-product-interpolation/) and [bilinear interpolation](/bilinear-interpolation/): the same product construction used to fit values on a grid.
- [Surface tessellation](/surface-tessellation/): the rectangular parameter domain gives a natural grid of sample points, and the product structure gives bounds on the second derivatives from the control net.
- [Smooth surface from a control mesh](/surface-from-control-mesh/): how several tensor-product patches, or subdivision, cover surfaces that one grid cannot.

## References
