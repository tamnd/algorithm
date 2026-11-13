---
tag: NCXHRX
kind: definition
slug: bezier-patch
name: Bezier patch
aliases:
- tensor-product Bezier surface
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The surface sum P_ij B_i^m(u) B_j^n(v) on [0, 1]^2 with a grid of (m + 1)(n + 1) control points. Its edges are Bezier curves, and de Casteljau in each direction evaluates it.
prereqs: [bezier-curve, tensor-product-surface]
see_also: [bezier-triangle, coons-patch, de-casteljau-algorithm, bernstein-polynomials, convex-hull-property, nurbs, surface-tessellation, surface-from-control-mesh]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 14, Tensor Product Patches (the de Casteljau algorithm for patches, derivatives, the twist, degree elevation and subdivision), and Chapter 16, Composite Surfaces
  - book: isbn:9783540437611
    title: Hartmut Prautzsch, Wolfgang Boehm and Marco Paluszny, Bezier and B-Spline Techniques, Springer, 2002
    locator: Chapter 9, Tensor product surfaces (Bezier representation, de Casteljau algorithm, derivatives and subdivision)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Chapter 1, Curve and Surface Basics (tensor product surfaces, and Bezier surfaces as products of Bernstein bases)
---

A Bézier patch of degree $(m, n)$ is the surface $S(u, v) = \sum_{i=0}^m \sum_{j=0}^n P_{ij} B_i^m(u) B_j^n(v)$ on the unit square, where the $P_{ij}$ are a grid of $(m + 1)(n + 1)$ [control points](/control-points/) and $B_i^m$ are the [Bernstein polynomials](/bernstein-polynomials/). It is the [tensor product](/tensor-product-surface/) of two [Bézier curves](/bezier-curve/): each row of the net is a curve in $v$, and the points of the rows at a fixed $v$ are the control points of a curve in $u$. The patch passes through its four corner points, its edges are the Bézier curves of the boundary rows and columns, and it lies in the convex hull of the net. The bicubic patch, with 16 control points, is the usual case in CAD and in GPU tessellation.

## Definition

Let $m, n \ge 0$ and let $P_{ij} \in \mathbb{R}^3$ for $0 \le i \le m$, $0 \le j \le n$. The Bézier patch with the control net $(P_{ij})$ is

$$S(u, v) = \sum_{i=0}^{m} \sum_{j=0}^{n} P_{ij}\, B_i^m(u)\, B_j^n(v), \qquad B_i^m(u) = \binom{m}{i} u^i (1 - u)^{m-i}, \qquad (u, v) \in [0, 1]^2.$$

The index $i$ runs along $u$ and $j$ along $v$. Each coordinate of $S$ is a polynomial of degree at most $m$ in $u$ and at most $n$ in $v$. Because the products $B_i^m(u) B_j^n(v)$ are a basis of that space, every such polynomial surface has exactly one net of degree $(m, n)$.

The patch has these properties. Each one is the curve property applied in both directions.

1. **Corners and edges.** $S(0, 0) = P_{00}$, $S(1, 0) = P_{m0}$, $S(0, 1) = P_{0n}$, $S(1, 1) = P_{mn}$. The edge $S(u, 0) = \sum_i P_{i0} B_i^m(u)$ is the Bézier curve of the row $j = 0$, and the same holds for the other three edges. The inner control points do not change the edges. Two patches that share a boundary row of control points share that edge exactly.
2. **Partial derivatives.** With the forward differences $\Delta^{1,0} P_{ij} = P_{i+1,j} - P_{ij}$ and $\Delta^{0,1} P_{ij} = P_{i,j+1} - P_{ij}$,
$$S_u = m \sum_{i=0}^{m-1} \sum_{j=0}^{n} \Delta^{1,0} P_{ij}\, B_i^{m-1}(u) B_j^n(v), \qquad S_v = n \sum_{i=0}^{m} \sum_{j=0}^{n-1} \Delta^{0,1} P_{ij}\, B_i^m(u) B_j^{n-1}(v).$$
Proof: differentiate the $u$ factor with the curve rule $\frac{d}{du} \sum_i Q_i B_i^m = m \sum_i (Q_{i+1} - Q_i) B_i^{m-1}$ for each fixed $j$. Higher partials repeat this. In general $\partial^{r+s} S / \partial u^r \partial v^s$ is the patch of degree $(m - r, n - s)$ with the net $\frac{m!}{(m-r)!} \frac{n!}{(n-s)!} \Delta^{r,s} P_{ij}$.
3. **Tangent plane and twist at a corner.** $S_u(0, 0) = m (P_{10} - P_{00})$ and $S_v(0, 0) = n (P_{01} - P_{00})$, so the tangent plane at $P_{00}$ is the plane of $P_{00}, P_{10}, P_{01}$ when these are not on a line. The twist is $S_{uv}(0, 0) = mn\,(P_{11} - P_{10} - P_{01} + P_{00})$. It is zero when the first quad of the net is a parallelogram.
4. **Affine invariance and convex hull.** The products $B_i^m(u) B_j^n(v)$ are nonnegative on $[0, 1]^2$ and sum to 1. So an affine map of the net maps the patch in the same way, and every point of the patch is a convex combination of the control points (see the [convex hull property](/convex-hull-property/)). Each derivative net from property 2 bounds its derivative in the same way, which gives bounds for [tessellation](/surface-tessellation/).
5. **Subdivision.** The [de Casteljau](/de-casteljau-algorithm/) split of every row at $u = u_0$ (here the "rows" are the lines of fixed $j$) gives the nets of the parts on $[0, u_0] \times [0, 1]$ and $[u_0, 1] \times [0, 1]$. A split in $v$ works the same way.
6. **Degree elevation.** Elevating each line of fixed $j$ from degree $m$ to $m + 1$ gives the same surface with a net of degree $(m + 1, n)$.
7. **No exact quadrics.** A polynomial patch cannot represent a piece of a sphere or of a circular cylinder exactly, for the same reason that a Bézier curve cannot represent a circle arc. A rational patch can; see [NURBS](/nurbs/).

### Evaluation

The point is computed by the curve algorithm in two passes. This is correct because $S(u, v) = \sum_i B_i^m(u) \left( \sum_j P_{ij} B_j^n(v) \right)$: the inner sum is the Bézier curve of row $i$ at $v$, which the curve algorithm computes, and the outer sum is the Bézier curve of these $m + 1$ points at $u$.

```pseudo id=main
PATCH-POINT(P[0..m][0..n], u, v)
L1  if n ≤ m then                                  ▷ start along the lower degree
L2      for i ← 0 to m do
L3          Q_i ← DE-CASTELJAU(P_i0, ..., P_in, v)  ▷ row i is a curve of degree n in v
L4      return DE-CASTELJAU(Q_0, ..., Q_m, u)
L5  else
L6      for j ← 0 to n do
L7          R_j ← DE-CASTELJAU(P_0j, ..., P_mj, u)  ▷ column j is a curve of degree m in u
L8      return DE-CASTELJAU(R_0, ..., R_n, v)
```

The cost model is the real RAM, and the unit is one linear interpolation of two points of $\mathbb{R}^3$ (three multiplications and six additions). The curve algorithm of degree $k$ does $k(k + 1)/2$ interpolations. Lines L2 to L4 do $(m + 1)\,n(n + 1)/2 + m(m + 1)/2$, and lines L6 to L8 do the same with $m$ and $n$ swapped. The first count is no larger than the second when $n \le m$, and smaller when $0 < n < m$, so the test on line L1 picks the cheaper order. This is an exact count per point, the same for every input: 30 interpolations for a bicubic patch. The extra memory is $O(m + n)$ points if line L3 reuses one array.

There is also a two-dimensional form of the algorithm. Each step replaces every $2 \times 2$ block of neighbours by its bilinear blend at $(u, v)$, which turns a net of size $(a + 1) \times (b + 1)$ into one of size $a \times b$. After $\min(m, n)$ steps one line of points is left, and a curve step finishes. For $m = n$ the last net is a single point. This form costs more (42 interpolations for a bicubic patch, since each blend takes three), but its last $2 \times 2$ net gives the tangent plane: if $m = n$, the last four points $b_{00}, b_{10}, b_{01}, b_{11}$ give $S_u = n\,[(1 - v)(b_{10} - b_{00}) + v (b_{11} - b_{01})]$ and the similar formula for $S_v$.

## Examples and non-examples

- **A biquadratic patch, worked.** Take $m = n = 2$ and $P_{ij} = (i, j, z_{ij})$ with $z = 0$ at the four corners, $z = 1$ at the four edge midpoints $P_{10}, P_{01}, P_{21}, P_{12}$, and $z = 4$ at the center $P_{11}$. The $x$ and $y$ coordinates are $i$ and $j$, so by linear precision $x = 2u$ and $y = 2v$. Lines L2 and L3 at $v = 1/2$ give the row points $Q_0 = (0, 1, 1/2)$, $Q_1 = (1, 1, 5/2)$, $Q_2 = (2, 1, 1/2)$; for row 1 the $z$ value is $(1 + 2 \cdot 4 + 1)/4 = 5/2$. Line L4 at $u = 1/2$ gives $S(1/2, 1/2) = (1, 1, 3/2)$, and at $u = 1/4$ it gives $\frac{9}{16} Q_0 + \frac{6}{16} Q_1 + \frac{1}{16} Q_2 = (1/2, 1, 5/4)$.
- **Derivatives of the same patch.** At $(1/2, 1/2)$ property 2 gives $S_u = (2, 0, 0)$, $S_v = (0, 2, 0)$ and $S_{uv} = 0$, so the point is a horizontal tangent plane at the top. The second differences in $i$ are $-2, -6, -2$ for $j = 0, 1, 2$ (for $j = 1$: $1 - 2 \cdot 4 + 1$), so $S_{uu}(1/2, 1/2) = 2\,(-2 \cdot \frac14 - 6 \cdot \frac12 - 2 \cdot \frac14)\,e_z = (0, 0, -8)$. At $(1/4, 1/2)$, $S_{vv} = 2\,(-2 \cdot \frac{9}{16} - 6 \cdot \frac{6}{16} - 2 \cdot \frac{1}{16})\,e_z = (0, 0, -7)$.
- **The bilinear patch.** For $m = n = 1$ the patch is the [bilinear interpolant](/bilinear-interpolation/) of its four corners. The corners $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(1, 1, 1)$ give $z = xy$, a hyperbolic paraboloid. Its twist is $P_{11} - P_{10} - P_{01} + P_{00} = (0, 0, 1)$.
- **A plane.** If $P_{ij} = A + \frac{i}{m} U + \frac{j}{n} V$, then $S(u, v) = A + uU + vV$, the parallelogram spanned by $U$ and $V$. Any net on a plane gives a patch in that plane, by the convex hull property, but only this net gives the linear parametrization.
- **Collapsed edge.** If $P_{00} = P_{10} = \dots = P_{m0}$, the edge $v = 0$ is a single point. The patch is then a triangle-shaped surface, but $S_u = 0$ along that edge, so the parametrization is singular there and the normal must be found by a limit. A [Bézier triangle](/bezier-triangle/) gives triangular patches without this problem.
- **Non-example: the inner points are not on the surface.** In the worked example, $P_{11} = (1, 1, 4)$, but the patch over $(1, 1)$ is at height $3/2$. The patch interpolates only its corners. To make a patch pass through a grid of points, solve the [tensor-product interpolation](/tensor-product-interpolation/) problem for the net.
- **Non-example: four curves are not enough.** The four boundary curves fix only the boundary rows of the net. The inner points are free, so many patches share the same boundary. The [Coons patch](/coons-patch/) is one canonical choice: for the boundary of the worked example it gives the center control point $(1, 1, 2)$ in place of $(1, 1, 4)$.

## Related definitions

- [Bézier curve](/bezier-curve/) and [de Casteljau algorithm](/de-casteljau-algorithm/): the curve form and the evaluator that the patch uses in each direction.
- [Tensor-product surface](/tensor-product-surface/): the general product construction. With B-spline bases it gives [B-spline](/b-spline/) and [NURBS](/nurbs/) surfaces, whose pieces are Bézier patches.
- [Bézier triangle](/bezier-triangle/): the Bernstein form of total degree $n$ on a triangle, with $(n + 1)(n + 2)/2$ control points instead of $(n + 1)^2$.
- [Coons patch](/coons-patch/): a surface from four boundary curves. For Bézier boundaries it is a Bézier patch with a net given by a formula.
- [Surface tessellation](/surface-tessellation/) and [smooth surface from a control mesh](/surface-from-control-mesh/): turning patches into triangles, and building patch networks from meshes.

## References
