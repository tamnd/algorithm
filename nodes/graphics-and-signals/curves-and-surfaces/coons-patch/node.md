---
tag: JG5HXQ
kind: definition
slug: coons-patch
name: Coons patch
aliases:
- bilinearly blended Coons patch
area: graphics-and-signals/curves-and-surfaces
level: advanced
summary: The surface through four boundary curves that meet at the corners. It is the sum of the two ruled surfaces between opposite curves minus the bilinear patch of the corners.
prereqs: [parametric-surface, bilinear-interpolation]
see_also: [ruled-surface, bezier-patch, tensor-product-surface, tensor-product-interpolation, mesh-generation, surface-from-control-mesh, bezier-curve, parametric-continuity]
sources:
  - book: isbn:9781558607378
    title: Gerald Farin, Curves and Surfaces for CAGD, A Practical Guide, fifth edition, Morgan Kaufmann, 2002
    locator: Chapter 22, Coons Patches (the bilinearly blended patch, the Boolean sum, the discrete form on Bezier boundaries, and the bicubically blended patch)
  - book: isbn:9783540615453
    title: Les Piegl and Wayne Tiller, The NURBS Book, second edition, Springer, 1997
    locator: Section 10.6, Coons Surfaces (the bilinearly blended Coons surface as a NURBS surface from compatible boundary curves)
  - paper: doi:10.1137/0708019
    title: William J. Gordon, Blending-Function Methods of Bivariate and Multivariate Interpolation and Approximation, SIAM Journal on Numerical Analysis 8(1), 158-177 (1971)
    locator: the projectors of univariate interpolation, their Boolean sum, and the interpolation of a function on the whole boundary of a rectangle
---

A Coons patch fills the region bounded by four curves. Given curves $c_0(u)$, $c_1(u)$, $d_0(v)$, $d_1(v)$ that form a closed loop, it builds a surface $S(u, v)$ on the unit square with $S(u, 0) = c_0(u)$, $S(u, 1) = c_1(u)$, $S(0, v) = d_0(v)$ and $S(1, v) = d_1(v)$. The formula adds the two [ruled surfaces](/ruled-surface/) between opposite curves and subtracts the [bilinear patch](/bilinear-interpolation/) of the four corners, which both ruled surfaces contain. Steven Coons gave the construction in his 1967 MIT Project MAC report "Surfaces for Computer-Aided Design of Space Forms" (MAC-TR-41). It is the simplest answer to the question "which surface has these four edges", and it is used in CAD, in hole filling, and as transfinite interpolation in structured [mesh generation](/mesh-generation/).

## Definition

Let $c_0, c_1 : [0, 1] \to \mathbb{R}^3$ and $d_0, d_1 : [0, 1] \to \mathbb{R}^3$ be continuous curves that meet at four corners:

$$c_0(0) = d_0(0) = P_{00}, \quad c_0(1) = d_1(0) = P_{10}, \quad c_1(0) = d_0(1) = P_{01}, \quad c_1(1) = d_1(1) = P_{11}.$$

These four equations are the compatibility conditions. The bilinearly blended Coons patch is

$$S(u, v) = \underbrace{(1 - v)\, c_0(u) + v\, c_1(u)}_{R_v} + \underbrace{(1 - u)\, d_0(v) + u\, d_1(v)}_{R_u} - \underbrace{\big[(1 - u)(1 - v) P_{00} + u(1 - v) P_{10} + (1 - u) v P_{01} + uv P_{11}\big]}_{B}$$

for $(u, v) \in [0, 1]^2$. $R_v$ is the ruled surface between $c_0$ and $c_1$, $R_u$ the ruled surface between $d_0$ and $d_1$, and $B$ the bilinear patch of the corners. The name comes from the blending functions $1 - t$ and $t$, which are linear in each variable.

**The boundary property.** $S$ matches all four curves exactly. Proof for the edge $v = 0$: there $R_v = c_0(u)$, $R_u = (1 - u) d_0(0) + u\, d_1(0) = (1 - u) P_{00} + u P_{10}$, and $B = (1 - u) P_{00} + u P_{10}$. So $R_u - B = 0$ and $S(u, 0) = c_0(u)$. The other three edges are the same computation with the roles of the curves exchanged. $\square$

The proof uses each compatibility condition: if, say, $d_0(0) \ne c_0(0)$ with $P_{00} = c_0(0)$, then $S(u, 0) = c_0(u) + (1 - u)(d_0(0) - c_0(0))$, which misses $c_0$ everywhere except at $u = 1$. So the curves must close up before the patch is built.

**The Boolean sum.** Write $\mathcal P_1 F = (1 - u) F(0, v) + u F(1, v)$ and $\mathcal P_2 F = (1 - v) F(u, 0) + v F(u, 1)$ for the two linear interpolation operators on functions of $(u, v)$. Each one matches $F$ on two opposite edges only. Their product $\mathcal P_1 \mathcal P_2 F$ is the bilinear interpolant of the four corners. The Coons patch is the Boolean sum

$$S = (\mathcal P_1 \oplus \mathcal P_2) F = \mathcal P_1 F + \mathcal P_2 F - \mathcal P_1 \mathcal P_2 F,$$

applied to any $F$ with the given boundary. Gordon (1971) studied these sums in general: if $\mathcal P_1$ and $\mathcal P_2$ commute and are projectors, then $\mathcal P_1 \oplus \mathcal P_2$ is a projector that matches $F$ wherever either one does. This view gives the variants below by changing the univariate interpolation in each direction.

**Bézier boundaries.** Let $c_0, c_1$ be [Bézier curves](/bezier-curve/) of degree $m$ with control points $a_i$ and $b_i$, and $d_0, d_1$ Bézier curves of degree $n$ with control points $c_j$ and $d_j$, with $m, n \ge 1$ and matching corners. Then $S$ is the [Bézier patch](/bezier-patch/) of degree $(m, n)$ with the net

$$P_{ij} = \left(1 - \tfrac{j}{n}\right) a_i + \tfrac{j}{n}\, b_i + \left(1 - \tfrac{i}{m}\right) c_j + \tfrac{i}{m}\, d_j - \left[\left(1 - \tfrac{i}{m}\right)\left(1 - \tfrac{j}{n}\right) P_{00} + \tfrac{i}{m}\left(1 - \tfrac{j}{n}\right) P_{10} + \left(1 - \tfrac{i}{m}\right) \tfrac{j}{n} P_{01} + \tfrac{i}{m} \tfrac{j}{n} P_{11}\right].$$

Proof: by linear precision, $1 - v = \sum_j (1 - j/n) B_j^n(v)$ and $v = \sum_j (j/n) B_j^n(v)$, and $\sum_j B_j^n(v) = 1$. So $(1 - v)\, c_0(u) = \sum_{i,j} (1 - j/n)\, a_i\, B_i^m(u) B_j^n(v)$, and each of the other seven terms becomes a double Bernstein sum in the same way. Adding the coefficients of $B_i^m(u) B_j^n(v)$ gives $P_{ij}$. $\square$ If the opposite curves have different degrees, elevate the lower one first. The boundary rows of this net are the curve control points, as they must be.

### Evaluation

```pseudo id=main
COONS-POINT(c0, c1, d0, d1, u, v)
L1  if c0(0) ≠ d0(0) or c0(1) ≠ d1(0) or c1(0) ≠ d0(1) or c1(1) ≠ d1(1) then error
L2  P00, P10, P01, P11 ← c0(0), c0(1), c1(0), c1(1)
L3  R_v ← (1 − v) c0(u) + v c1(u)                       ▷ ruled between c0 and c1
L4  R_u ← (1 − u) d0(v) + u d1(v)                       ▷ ruled between d0 and d1
L5  B ← (1 − u)(1 − v) P00 + u(1 − v) P10 + (1 − u) v P01 + uv P11
L6  return R_v + R_u − B
```

The cost of a point is four curve evaluations and a combination of eight points. In the real RAM model, with Bézier boundaries of degrees $m$ and $n$ evaluated by de Casteljau, lines L3 and L4 cost $m(m + 1) + n(n + 1)$ linear interpolations and lines L5 and L6 a constant. For bicubic boundaries this is 24 interpolations, against 30 for the equal [Bézier patch](/bezier-patch/) evaluated from its net. The corner values of line L2 can be cached for all points of a patch.

## Examples and non-examples

- **A worked patch.** Take the four quadratic boundaries $c_0$: $(0, 0, 0), (1, 0, 1), (2, 0, 0)$; $c_1$: $(0, 2, 0), (1, 2, 1), (2, 2, 0)$; $d_0$: $(0, 0, 0), (0, 1, 1), (0, 2, 0)$; $d_1$: $(2, 0, 0), (2, 1, 1), (2, 2, 0)$. They are the edges of the worked [Bézier patch](/bezier-patch/) example. At the center, $c_0(1/2) = (1, 0, 1/2)$, $c_1(1/2) = (1, 2, 1/2)$, $d_0(1/2) = (0, 1, 1/2)$, $d_1(1/2) = (2, 1, 1/2)$, so $R_v = R_u = (1, 1, 1/2)$, $B = (1, 1, 0)$, and $S(1/2, 1/2) = (1, 1, 1)$. The Bézier patch with the same edges and inner control point $(1, 1, 4)$ has its center at $(1, 1, 3/2)$. The net formula gives the inner control point $P_{11} = (1, 1, 2)$, and with it the Bézier patch center is $(1, 1, 1)$, which is the Coons value.
- **Straight edges.** If all four curves are the straight segments between the corners, then $R_v = R_u = B$ and $S = B$: the Coons patch of a skew quadrilateral is its bilinear patch. With the corners $(0, 0, 0)$, $(1, 0, 0)$, $(0, 1, 0)$, $(1, 1, 1)$ it is the saddle $z = xy$.
- **Ruled surfaces are reproduced.** If $d_0$ and $d_1$ are straight segments, then $R_u = B$ and $S = R_v$, the ruled surface between $c_0$ and $c_1$. If they are not straight, $R_v$ alone matches $c_0$ and $c_1$ but gives the segment $(1 - v) P_{00} + v P_{01}$ on the edge $u = 0$ instead of $d_0$. The correction $R_u - B$ is exactly what moves that edge onto $d_0$.
- **Transfinite interpolation of a grid.** In structured mesh generation the four sides of a region are given as point lists of equal size on opposite sides. The same formula with $u = i/M$ and $v = j/N$ gives the inner grid points, which interpolate the sides exactly. For mildly curved sides the grid is usually good, but for strongly curved or concave sides the cells can fold over, and the formula itself gives no guarantee against this.
- **Non-example: incompatible curves.** Four curves that do not meet at the corners give a surface that misses at least one of them; see the computation after the boundary property. No patch of the form above can fix this.
- **Non-example: smooth joins.** Two Coons patches that share a boundary curve meet along it with no gap, but in general with a crease. The tangent across the edge $u = 0$ is $S_u(0, v) = d_1(v) - d_0(v) + (1 - v)\, c_0'(0) + v\, c_1'(0) - (P_{10} - P_{00})(1 - v) - (P_{11} - P_{01}) v$, which depends on the opposite curve $d_1$, not only on data along the shared edge. So the patch gives [continuity](/parametric-continuity/) of position only. The bicubically blended Coons patch uses cubic Hermite blending functions and prescribed cross-boundary derivatives to join patches with continuous tangent planes.

## Related definitions

- [Ruled surface](/ruled-surface/) and [bilinear interpolation](/bilinear-interpolation/): the three parts of the formula.
- [Bézier patch](/bezier-patch/) and [tensor-product surface](/tensor-product-surface/): a Coons patch of polynomial boundaries is a tensor-product polynomial patch, with the net given above. A tensor-product patch needs its whole net; a Coons patch needs only the boundary.
- [Tensor-product interpolation](/tensor-product-interpolation/): interpolates values at grid points. The Coons patch interpolates on whole curves, which is why such methods are called transfinite.
- [Smooth surface from a control mesh](/surface-from-control-mesh/): networks of patches over a mesh, where Coons-type constructions fill faces from their edge curves.
- [Mesh generation](/mesh-generation/): structured grids by transfinite interpolation of the boundary.

## References
