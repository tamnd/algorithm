---
tag: 2SWPQV
kind: definition
slug: edge-function
name: Edge function
aliases:
- half-space function
- signed area function
area: graphics-and-signals/rasterization
level: advanced
summary: "The affine function E(p) = (b - a) x (p - a) of a directed edge: twice the signed area of (a, b, p), so its sign gives the side of p."
prereqs: [oriented-triangle-area, orientation-test, cross-product]
see_also: [top-left-fill-rule, pineda-rasterization, triangle-rasterization, point-to-line-distance, half-plane-intersection, watertight-ray-triangle-intersection, shewchuk-expansion-sum, integer-overflow]
sources:
  - paper: doi:10.1145/378456.378457
    title: Juan Pineda, A parallel algorithm for polygon rasterization, Computer Graphics (SIGGRAPH 88 Proceedings) 22(4), 17 to 20, 1988
    locator: the whole paper (the edge function, its incremental evaluation, and the inside test as the conjunction of three edge tests)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2016
    locator: Chapter 8, Section 8.1.2, Triangle Rasterization (barycentric coordinates of pixel centers from the edge line equations)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, CRC Press, 2018
    locator: Chapter 23, Section 23.1, Rasterization (edge functions and triangle setup)
  - paper: doi:10.1145/258694.258723
    title: Marc Olano and Trey Greer, Triangle scan conversion using 2D homogeneous coordinates, Proceedings of the ACM SIGGRAPH/Eurographics Workshop on Graphics Hardware, 89 to 95, 1997
    locator: the whole paper (edge functions in homogeneous screen coordinates, without a divide)
  - paper: doi:10.1007/PL00009321
    title: Jonathan Richard Shewchuk, Adaptive precision floating-point arithmetic and fast robust geometric predicates, Discrete and Computational Geometry 18(3), 1997
    locator: the sections on the orientation predicate (exact sign of the same determinant)
  - url: https://fgiesen.wordpress.com/2013/02/08/triangle-rasterization-in-practice/
    title: Fabian Giesen, Triangle rasterization in practice, The ryg blog, 2013
    locator: the sections on integer edge functions, subpixel precision and the fill rule bias
---

An edge function is the affine function $E_{ab}(p) = (b - a) \times (p - a)$ of a point $p$ in the plane, for a directed edge from $a$ to $b$. Its value is twice the [oriented area](/oriented-triangle-area/) of the triangle $(a, b, p)$, so its sign is the [orientation test](/orientation-test/) of $a$, $b$ and $p$: zero on the line through $a$ and $b$, positive on its left side and negative on its right side. A triangle is the set where its three edge functions have the same sign, so a [triangle rasterizer](/triangle-rasterization/) tests a pixel center with three edge functions. Because the function is affine, one step to the next pixel adds a constant, which is the base of [Pineda rasterization](/pineda-rasterization/).

## Definition

Let $a = (a_x, a_y)$ and $b = (b_x, b_y)$ be two different points of $\mathbb{R}^2$. The **edge function** of the directed edge $ab$ is the map $E_{ab} : \mathbb{R}^2 \to \mathbb{R}$,

$$E_{ab}(p) = (b_x - a_x)(p_y - a_y) - (b_y - a_y)(p_x - a_x) = A\,p_x + B\,p_y + C,$$

with the edge constants

$$A = a_y - b_y, \qquad B = b_x - a_x, \qquad C = a_x b_y - a_y b_x .$$

The first form is the 2D [cross product](/cross-product/) $(b - a) \times (p - a)$, that is, the determinant with rows $b - a$ and $p - a$. A triangle $T = (v_0, v_1, v_2)$ has three edge functions, each named after the vertex opposite the edge:

$$E_0 = E_{v_1 v_2}, \qquad E_1 = E_{v_2 v_0}, \qquad E_2 = E_{v_0 v_1} .$$

Let $S$ be the signed area of $T$, so $2S = E_{v_0 v_1}(v_2)$. The direction of the axes changes only the names of the sides. In screen coordinates with $y$ down, a positive $E_{ab}(p)$ puts $p$ on the right of $ab$ as seen on the screen. The rest of this page uses the algebra, which does not depend on the direction of the axes.

The function has these properties. Each one has a short proof.

1. **Zero set and sides.** $(A, B) = (-(b_y - a_y),\ b_x - a_x)$ is the vector $b - a$ turned by a quarter turn, so $(A, B) \ne (0, 0)$. The set $E_{ab} = 0$ is the line through $a$ and $b$, because $E_{ab}$ is affine, is not constant, and is zero at $a$ and at $b$. The sets $E_{ab} > 0$ and $E_{ab} < 0$ are the two open half-planes of that line, and $(A, B)$ is a normal vector that points into the positive one.
2. **Signed distance.** $E_{ab}(p) / \lVert b - a \rVert$ is the signed distance from $p$ to the line, because $\lVert (A, B) \rVert = \lVert b - a \rVert$ (see [point-to-line distance](/point-to-line-distance/)).
3. **Antisymmetry.** $E_{ba} = -E_{ab}$, because swapping $a$ and $b$ negates $A$, $B$ and $C$.
4. **Incremental evaluation.** $E_{ab}(p + (d_x, d_y)) = E_{ab}(p) + A\,d_x + B\,d_y$. A step of one pixel to the right adds $A$, and a step of one pixel down adds $B$.
5. **Constant sum.** $E_0(p) + E_1(p) + E_2(p) = 2S$ for each $p$. *Proof.* The sum is affine. Its linear part is $\sum (A_k, B_k)$, and the three terms $(a_y - b_y, b_x - a_x)$ over the cycle $v_1 v_2, v_2 v_0, v_0 v_1$ cancel. So the sum is constant. At $p = v_0$, $E_1(v_0) = E_2(v_0) = 0$, and $E_0(v_0) = (v_2 - v_1) \times (v_0 - v_1) = 2S$, because the oriented area does not change under a cyclic shift of the vertices. $\square$
6. **Barycentric coordinates.** If $S \ne 0$, then $\lambda_k(p) = E_k(p) / (2S)$ for $k = 0, 1, 2$ are the barycentric coordinates of $p$: $\lambda_0 + \lambda_1 + \lambda_2 = 1$ and $p = \lambda_0 v_0 + \lambda_1 v_1 + \lambda_2 v_2$. *Proof.* The sum is 1 by property 5. The map $p \mapsto \sum_k \lambda_k(p) v_k$ is affine, and $\lambda_k(v_j)$ is 1 if $j = k$ and 0 otherwise, so the map is the identity at the three vertices. An affine map of the plane is fixed by its values at three points that are not on one line, so it is the identity. $\square$ The closed triangle is the set of points with $\lambda_k \ge 0$ for all $k$, that is, the set where each $E_k$ is zero or has the sign of $S$.
7. **Exact in integers.** Let the coordinates of $a$, $b$ and $p$ be integers in $[-2^{q-1}, 2^{q-1} - 1]$. Each difference has absolute value at most $2^q - 1$, so $|E_{ab}(p)| \le 2(2^q - 1)^2 < 2^{2q+1}$. A signed integer of $2q + 2$ binary digits holds the value exactly, and so does each value of the incremental steps of property 4 at points in the same range.

Rasterizers apply property 7 to snapped vertices. A pixel is a point sample at its center, not a little square. With centers at $i + \tfrac12$, as in the Direct3D 10 and OpenGL rules, and $2^s$ subpixel steps per pixel, the center of pixel $i$ is the integer $2^s i + 2^{s-1}$ in subpixel units. The Direct3D rasterizer uses 16.8 fixed point, which is $s = 8$, so 256 steps per pixel. For pixel coordinates in $[-2^{k-1}, 2^{k-1})$, the subpixel coordinates have $q = k + s$ binary digits. A 32-bit $E$ is then safe only for $q \le 15$, which with $s = 8$ is a range of 128 pixels. With $k = 12$ (pixels $-2048$ to $2047$) and $s = 8$, $E$ needs 42 binary digits, so implementations use 64-bit integers or a smaller range per tile. In this range the test "is $E > 0$, $E = 0$ or $E < 0$" has no rounding at all, so the [top-left fill rule](/top-left-fill-rule/) can decide the case $E = 0$.

## Examples and non-examples

**A right triangle.** Take $v_0 = (1, 1)$, $v_1 = (9, 1)$ and $v_2 = (1, 9)$. Then $2S = E_{v_0 v_1}(v_2) = 8 \cdot 8 - 0 \cdot 0 = 64$. The edge constants are:

| edge | from, to | $A$ | $B$ | $C$ |
| --- | --- | --- | --- | --- |
| $E_0$ | $v_1 \to v_2$ | $-8$ | $-8$ | $80$ |
| $E_1$ | $v_2 \to v_0$ | $8$ | $0$ | $-8$ |
| $E_2$ | $v_0 \to v_1$ | $0$ | $8$ | $-8$ |

At $p = (3, 3)$ the values are $E_0 = -24 - 24 + 80 = 32$, $E_1 = 24 - 8 = 16$ and $E_2 = 24 - 8 = 16$. Their sum is $64 = 2S$, as property 5 says. The barycentric coordinates are $(\tfrac12, \tfrac14, \tfrac14)$, and $\tfrac12 (1, 1) + \tfrac14 (9, 1) + \tfrac14 (1, 9) = (3, 3)$. One step right to $(4, 3)$ adds $(A_0, A_1, A_2) = (-8, 8, 0)$ and gives $(24, 24, 16)$.

**A point on an edge.** At $p = (5, 5)$, $E_0 = -40 - 40 + 80 = 0$, so $p$ is on the edge $v_1 v_2$, and the barycentric coordinates are $(0, \tfrac12, \tfrac12)$. The sign alone cannot say whether this triangle or its neighbor across $v_1 v_2$ owns $p$. The [top-left fill rule](/top-left-fill-rule/) decides it.

**Signed distance.** $E_0(3, 3) = 32$ and $\lVert v_2 - v_1 \rVert = 8\sqrt2$, so the distance from $(3, 3)$ to the line $x + y = 10$ is $32 / (8\sqrt2) = 2\sqrt2 \approx 2.828$, which is $|3 + 3 - 10| / \sqrt2$.

**Non-example: the edge function in floating point.** Take $a = (3.6, 1.5)$, $b = (0.8, 6.1)$ and $p = (1.36, 5.18)$, as [IEEE 754](/ieee-754/) binary64 numbers. In decimal, $p = a + 0.8\,(b - a)$ is on the line. The stored binary values are not, and the exact value of $E_{ab}(p)$ for them is about $-2.04 \times 10^{-16}$. The formula of the definition, evaluated in binary64, gives $E_{ab}(p) = 1.78 \times 10^{-15}$, with the wrong sign, and $E_{ba}(p) = 4.44 \times 10^{-16}$. So the computed values are not negatives of each other, and both triangles that share the edge $ab$ find $p$ strictly inside. The pixel is drawn twice. The other order of failure, where both values are negative, leaves a pixel out, which shows as a crack. The cause is [catastrophic cancellation](/catastrophic-cancellation/) in the difference of two nearly equal products, after the rounding of the inputs and of the differences. A [fused multiply-add](/fused-multiply-add/) removes the rounding of one product, but not the rounding of $b - a$ and $p - a$, so it does not fix the sign alone. The fixes that make the sign exact are integer coordinates (property 7), or an exact predicate such as Shewchuk's orientation test, which uses [error-free transformations](/error-free-transformations/) and [expansion sums](/shewchuk-expansion-sum/) and runs a fast [interval](/interval-arithmetic/) style filter first.

**Non-example: not a distance.** $E_{ab}$ is a distance only when $\lVert b - a \rVert = 1$. Hardware does not normalize it, because the sign and the ratios $E_k / 2S$ do not need it.

**Non-example: a degenerate edge.** If $a = b$, then $E_{ab}$ is zero everywhere and gives no half-plane. If $T$ has $S = 0$, the three edge functions do not define barycentric coordinates, and a rasterizer draws no pixel for $T$.

**Non-example: screen barycentrics are not surface barycentrics.** After a perspective projection, the ratios $E_k / 2S$ of the projected triangle are not the barycentric coordinates of the 3D point that projects to $p$. [Perspective-correct interpolation](/perspective-correct-interpolation/) gives the relation.

## Related definitions

- [Oriented triangle area](/oriented-triangle-area/) and the [orientation test](/orientation-test/): $E_{ab}(p)$ is the oriented area of $(a, b, p)$ times 2, and its sign is the orientation test. This page adds the affine form, the edge constants, the incremental steps and the use in rasterization.
- [Top-left fill rule](/top-left-fill-rule/): the rule for a pixel center where an edge function is zero.
- [Pineda rasterization](/pineda-rasterization/): evaluates the three edge functions at all pixel centers of a bounding box by property 4. [Conservative rasterization](/conservative-rasterization/) moves the constant $C$ by half a pixel along the normal.
- [Half-plane intersection](/half-plane-intersection/): a triangle is the intersection of the three half-planes $E_k \ge 0$ when $S > 0$.
- Homogeneous edge functions: Olano and Greer write the edge function as a linear function of the homogeneous screen point $(x, y, w)$, so a rasterizer can test triangles that cross the plane $w = 0$ without a divide. The edge constants are then the cross products of pairs of vertices in homogeneous form.
- [Watertight ray-triangle intersection](/watertight-ray-triangle-intersection/) and the [Plücker test](/plucker-ray-triangle-test/): ray tracing tests that solve a different problem, a 3D ray against a triangle. The watertight test shears the scene so that the ray is the $z$ axis, and then computes 2D edge functions of the projected triangle at the origin, with the same tie problem on shared edges.

## References
