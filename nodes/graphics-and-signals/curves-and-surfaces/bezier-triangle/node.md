---
tag: 6DPB5V
kind: definition
slug: bezier-triangle
name: Bezier triangle
aliases:
- triangular Bezier patch
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The surface sum P_ijk B_ijk^n(r, s, t) over i + j + k = n on a triangle in barycentric coordinates, with (n + 1)(n + 2)/2 control points and a triangular de Casteljau algorithm.
prereqs: [bezier-curve, bernstein-polynomials, parametric-surface]
see_also: [bezier-patch, tensor-product-surface, de-casteljau-algorithm, convex-hull-property, stars-and-bars, loop-subdivision, surface-from-control-mesh, surface-tessellation]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 17, Bezier Triangles (barycentric coordinates, the de Casteljau algorithm, derivatives, degree elevation and subdivision), and Chapter 18, Practical Aspects of Bezier Triangles
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Chapter 10, Bezier representation of triangular patches, with Section 10.4, The de Casteljau algorithm (page 146), and Section 10.5, Derivatives (page 147), and Chapter 11, Bezier techniques for triangular patches
  - paper: doi:10.1016/0167-8396(86)90016-6
    title: Gerald Farin, Triangular Bernstein-Bezier patches, Computer Aided Geometric Design 3(2), 83-127 (1986)
    locator: the survey of the triangular form, its history from de Casteljau, the algorithm, derivatives and smooth joins
  - paper: doi:10.1145/364338.364387
    title: Alex Vlachos, Jorg Peters, Chas Boyd and Jason L. Mitchell, Curved PN triangles, Proceedings of the 2001 Symposium on Interactive 3D Graphics, 159-166
    locator: the cubic Bezier triangle built from the three vertex positions and normals of a mesh triangle, with a separate quadratic normal patch
---

A Bézier triangle of degree $n$ is a polynomial surface over a triangle, written in barycentric coordinates $(r, s, t)$ with $r + s + t = 1$. It has one control point $P_{ijk}$ for each triple of nonnegative integers with $i + j + k = n$, so $(n + 1)(n + 2)/2$ control points: 3, 6, 10 and 15 for degrees 1 to 4. The basis is the trivariate Bernstein basis of total degree $n$, so the patch keeps the corner, edge, convex hull and de Casteljau properties of the [Bézier curve](/bezier-curve/). Unlike a [Bézier patch](/bezier-patch/), it is not a tensor product: it covers a triangle without a collapsed edge, which is why triangle meshes in CAD and in GPU tessellation use it.

## Definition

Fix a triangle $T$ in the parameter plane with vertices $A_1, A_2, A_3$. Each point $p$ of the plane has unique barycentric coordinates $(r, s, t)$ with $p = r A_1 + s A_2 + t A_3$ and $r + s + t = 1$; $p$ is in $T$ exactly when $r, s, t \ge 0$. For $n \ge 0$ and $i + j + k = n$, the Bernstein polynomials of total degree $n$ are

$$B_{ijk}^n(r, s, t) = \frac{n!}{i!\, j!\, k!}\, r^i s^j t^k.$$

The Bézier triangle with the control points $P_{ijk} \in \mathbb{R}^3$ is

$$S(r, s, t) = \sum_{i + j + k = n} P_{ijk}\, B_{ijk}^n(r, s, t), \qquad r + s + t = 1,\ r, s, t \ge 0.$$

The number of indices is the number of ways to write $n$ as an ordered sum of three nonnegative integers, $\binom{n + 2}{2} = (n + 1)(n + 2)/2$ (see [stars and bars](/stars-and-bars/)). This is the dimension of the space of polynomials of total degree at most $n$ in two variables, so every such polynomial surface over $T$ has exactly one control net of degree $n$. The net is drawn as a triangular grid: $P_{n00}$, $P_{0n0}$, $P_{00n}$ at the corners and $P_{ijk}$ at the domain point $(i A_1 + j A_2 + k A_3)/n$.

The patch has these properties.

1. **Partition of unity and convex hull.** By the multinomial theorem $\sum_{i+j+k=n} B_{ijk}^n = (r + s + t)^n = 1$, and each $B_{ijk}^n \ge 0$ on $T$. So the patch is affinely invariant and lies in the [convex hull](/convex-hull-property/) of its control points.
2. **Corners and edges.** $S(1, 0, 0) = P_{n00}$, and the same at the other two corners. On the edge $t = 0$ only the terms with $k = 0$ remain, and $B_{ij0}^n(r, s, 0) = \binom{n}{i} r^i s^j$ with $s = 1 - r$. So the edge is the Bézier curve of degree $n$ with the control points $P_{n00}, P_{n-1,1,0}, \dots, P_{0n0}$. Two triangles that share a boundary row of control points meet along that curve.
3. **Linear precision.** $\sum_{i+j+k=n} \frac{i}{n} B_{ijk}^n = r$, by the same differentiation of $(r + s + t)^n$ that proves it for curves. So if $P_{ijk} = (i A_1 + j A_2 + k A_3)/n$, the patch is the identity map of the triangle.
4. **The de Casteljau algorithm.** Let $P_{ijk}^0 = P_{ijk}$ and, for $\ell = 1, \dots, n$ and $i + j + k = n - \ell$,
$$P_{ijk}^\ell = r\, P_{i+1,j,k}^{\ell-1} + s\, P_{i,j+1,k}^{\ell-1} + t\, P_{i,j,k+1}^{\ell-1}.$$
Then $S(r, s, t) = P_{000}^n$. Proof: by induction on $\ell$, $S = \sum_{i+j+k=n-\ell} P_{ijk}^\ell B_{ijk}^{n-\ell}$, because the recurrence $B_{ijk}^{n} = r B_{i-1,j,k}^{n-1} + s B_{i,j-1,k}^{n-1} + t B_{i,j,k-1}^{n-1}$ moves one factor $r$, $s$ or $t$ from each basis function into the points.
5. **Derivatives.** A direction in the domain has barycentric form $d = (d_1, d_2, d_3)$ with $d_1 + d_2 + d_3 = 0$. The derivative along $d$ is
$$D_d S = n \sum_{i+j+k=n-1} (d_1 P_{i+1,j,k} + d_2 P_{i,j+1,k} + d_3 P_{i,j,k+1})\, B_{ijk}^{n-1},$$
and also $D_d S = n\,(d_1 P_{100}^{n-1} + d_2 P_{010}^{n-1} + d_3 P_{001}^{n-1})$ from the last level but one of the algorithm. So the three points of level $n - 1$ span the tangent plane at $S(r, s, t)$, as the last two points of the curve algorithm span the tangent.
6. **Subdivision.** Let $p$ be the domain point of $(r, s, t)$. The part of the patch over the subtriangle with corners $p, A_2, A_3$ is the Bézier triangle with the control points $Q_{ijk} = P_{0jk}^{i}$ for $i + j + k = n$: from each level $i$ of the algorithm, the points with first index 0. These points form one face of the pyramid of all levels, and the other two faces give the parts over $(A_1, p, A_3)$ and $(A_1, A_2, p)$.

### Evaluation

```pseudo id=main
TRIANGLE-POINT(P_ijk for i + j + k = n, r, s, t)
L1  b_ijk ← P_ijk for all i + j + k = n                 ▷ level 0, the control net
L2  for ℓ ← 1 to n do
L3      for each (i, j, k) with i + j + k = n − ℓ do
L4          b_ijk ← r b_(i+1)jk + s b_i(j+1)k + t b_ij(k+1)  ▷ level ℓ from level ℓ − 1
L5  return b_000
```

The cost model is the real RAM, and the unit is one blend of three points of $\mathbb{R}^3$. Level $\ell$ has $(n - \ell + 1)(n - \ell + 2)/2$ points, so lines L2 to L4 do

$$\sum_{\ell=1}^{n} \frac{(n - \ell + 1)(n - \ell + 2)}{2} = \sum_{q=1}^{n} \frac{q(q + 1)}{2} = \frac{n(n + 1)(n + 2)}{6}$$

blends, which is $\Theta(n^3)$ per point, against $\Theta(n^2)$ for a curve of degree $n$. The count is exact and the same for every input: 1, 4, 10 and 20 blends for degrees 1 to 4. To store the levels in place, sweep the indices so that each $b$ is read before it is overwritten, or keep two levels.

## Examples and non-examples

- **A quadratic, worked.** Take $n = 2$ with $P_{200} = (0, 0, 0)$, $P_{020} = (2, 0, 0)$, $P_{002} = (0, 2, 0)$ at the corners and $P_{110} = (1, 0, 1)$, $P_{011} = (1, 1, 1)$, $P_{101} = (0, 1, 1)$ at the edge midpoints. The $x$ and $y$ coordinates follow linear precision, so $x = 2s$ and $y = 2t$, and $z = 2(rs + st + tr)$; in the plane this is the paraboloid $z = x + y - (x^2 + xy + y^2)/2$ over the triangle with corners $(0, 0)$, $(2, 0)$, $(0, 2)$. At the centroid $(1/3, 1/3, 1/3)$, line L4 gives the level 1 points $P_{100}^1 = (1/3, 1/3, 2/3)$, $P_{010}^1 = (4/3, 1/3, 2/3)$, $P_{001}^1 = (1/3, 4/3, 2/3)$, and the second round gives $S = (2/3, 2/3, 2/3)$. The derivative along $d = (-1, 1, 0)$ is $2\,(P_{010}^1 - P_{100}^1) = (2, 0, 0)$, and along $(-1, 0, 1)$ it is $(0, 2, 0)$: the tangent plane is horizontal, so the centroid is the top of the paraboloid. At $(1/2, 1/4, 1/4)$ the patch gives $(1/2, 1/2, 5/8)$, and the paraboloid at $x = y = 1/2$ gives the same height: $1/2 + 1/2 - (1/4 + 1/4 + 1/4)/2 = 5/8$.
- **Degree 1.** A linear Bézier triangle is the flat triangle of its three control points. A [polygon mesh](/polygon-mesh/) made of triangles is a network of linear Bézier triangles.
- **PN triangles.** Vlachos, Peters, Boyd and Mitchell (2001) replace each flat triangle of a mesh by a cubic Bézier triangle (10 control points). The corners are the three vertices; the two inner points of each edge are the points at one third and two thirds of the edge, projected onto the tangent planes given by the vertex normals; and the center point is chosen from these. The patches meet with a common boundary curve but in general not with a common tangent plane, so the paper interpolates the normals with a separate quadratic patch for shading.
- **Non-example: a collapsed tensor-product patch.** The map $(u, v) \mapsto (r, s, t) = (1 - u,\ u(1 - v),\ uv)$ sends the square onto the triangle and the edge $u = 0$ to the corner $A_1$. Composing it with a Bézier triangle of degree $n$ gives a [Bézier patch](/bezier-patch/) of degree $(n, n)$ with $(n + 1)^2$ control points, one whole boundary row of which is the single point $P_{n00}$. The surface is the same set, but the parametrization is singular along that edge ($S_v = 0$ there), and the net has $(n + 1)^2$ points instead of $(n + 1)(n + 2)/2$.
- **Non-example: points outside the triangle.** The formula is a polynomial and has values for every $(r, s, t)$ with $r + s + t = 1$. With a negative coordinate the weights are not all nonnegative, so the point need not be in the convex hull of the net. For the quadratic above, $(r, s, t) = (-1, 1, 1)$ gives $z = 2(-1 + 1 - 1) = -2$, below every control point.
- **Non-example: a tensor product of two curve bases.** For $m + n \ge 1$ the span of the products $B_i^m(u) B_j^n(v)$ is never the space of polynomials of total degree at most some $N$. If $m, n \ge 1$, it holds $u^m v^n$ of total degree $m + n$ but not $u^{m+n}$. If $n = 0$, it holds no polynomial in $v$ at all.

## Related definitions

- [Bézier curve](/bezier-curve/) and [Bernstein polynomials](/bernstein-polynomials/): the univariate form. Each edge of a Bézier triangle is a Bézier curve.
- [Bézier patch](/bezier-patch/) and [tensor-product surface](/tensor-product-surface/): the rectangular form with $(m + 1)(n + 1)$ control points and de Casteljau in each direction.
- [De Casteljau algorithm](/de-casteljau-algorithm/): the curve algorithm. The triangular version replaces each linear interpolation of two points by a barycentric blend of three.
- [Loop subdivision](/loop-subdivision/): on a regular triangle mesh its limit is a box spline surface of total degree 4, so each regular face corresponds to a quartic Bézier triangle (15 control points).
- [Smooth surface from a control mesh](/surface-from-control-mesh/) and [surface tessellation](/surface-tessellation/): building triangle patch networks from meshes, and turning patches back into triangles.

## References
