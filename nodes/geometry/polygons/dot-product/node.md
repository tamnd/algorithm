---
tag: 1WSK55
kind: definition
slug: dot-product
name: Dot product
aliases:
- scalar product
- inner product of two vectors
area: geometry/polygons
level: intro
summary: Scalar product of two vectors, equal to the product of their lengths and the cosine of the angle between them.
prereqs: [point-and-vector]
see_also: [cross-product, point-projection-and-reflection, point-to-segment-distance, oriented-triangle-area, geometry-primitives, accurate-dot-product, vector-rotation]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.1, Line-segment properties (vectors, and the on-segment test used with the cross product)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Sections 1.3 to 1.5 (vector arithmetic in the area code, and the test of Section 1.5 for a collinear point between two endpoints)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 1, Section 1.2, Degeneracies and Robustness
---

The dot product of two vectors $u = (u_x, u_y)$ and $v = (v_x, v_y)$ is the number $u \cdot v = u_x v_x + u_y v_y$. It equals $|u|\,|v| \cos\theta$, where $\theta$ is the angle between the vectors, so its sign tells whether the angle is acute, right or obtuse, without a square root or a cosine. With the [cross product](/cross-product/), which gives the sine, it is one of the two basic [geometry primitives](/geometry-primitives/) on [points and vectors](/point-and-vector/).

## Definition

Points are $p = (x, y)$ and vectors are differences of points, as on [point and vector](/point-and-vector/). For vectors $u, v \in \mathbb{R}^2$,

$$u \cdot v = u_x v_x + u_y v_y .$$

**Algebraic properties.** For all vectors $u, v, w$ and reals $c$:

- symmetric: $u \cdot v = v \cdot u$;
- bilinear: $(c u + w) \cdot v = c\,(u \cdot v) + w \cdot v$;
- positive definite: $u \cdot u = u_x^2 + u_y^2 = |u|^2 \ge 0$, with equality only for $u = 0$.

**The angle formula.** For nonzero $u$ and $v$, with $\theta \in [0, \pi]$ the angle between them,

$$u \cdot v = |u|\,|v| \cos\theta .$$

*Proof.* By bilinearity and symmetry, $|u - v|^2 = (u - v) \cdot (u - v) = |u|^2 + |v|^2 - 2\,u \cdot v$. The triangle with sides $u$, $v$ and $u - v$ has the angle $\theta$ between the sides of length $|u|$ and $|v|$, so the law of cosines gives $|u - v|^2 = |u|^2 + |v|^2 - 2|u||v|\cos\theta$. Compare the two equations. If $u$ and $v$ are parallel the triangle is flat, and the formula follows from $v = c u$ directly: both sides equal $c|u|^2$. $\square$

**Consequences.** For nonzero $u, v$:

- $u \cdot v > 0$ if and only if $\theta < 90°$; $u \cdot v = 0$ if and only if $u \perp v$; $u \cdot v < 0$ if and only if $\theta > 90°$.
- Cauchy-Schwarz: $|u \cdot v| \le |u|\,|v|$.
- Lagrange's identity in the plane: $(u \cdot v)^2 + (u \times v)^2 = |u|^2 |v|^2$, where $u \times v = u_x v_y - u_y v_x$. Expand both sides: the cross terms $2u_xv_xu_yv_y$ and $-2u_xv_yu_yv_x$ cancel, and the rest is $(u_x^2 + u_y^2)(v_x^2 + v_y^2)$.
- Projection: the point of the line through $a$ with direction $u \ne 0$ that is nearest to $p$ is $a + \frac{(p - a) \cdot u}{u \cdot u}\, u$. The parameter is a ratio of integers when the input is integer, so it is exact as a `Fraction`.

**Exactness.** With integer coordinates the dot product is an integer and its sign is exact. With coordinates of absolute value below $B$, the dot product of two differences of points has absolute value at most $8B^2$. In floating point, the sum of two products can cancel, and the sign of a small result is not reliable; [compensated dot products](/accurate-dot-product/) or exact arithmetic fix this.

## Examples and non-examples

**A worked example.** For $u = (3, 4)$ and $v = (4, 1)$: $u \cdot v = 12 + 4 = 16 > 0$, so the angle is acute. With $|u| = 5$ and $|v| = \sqrt{17}$, $\cos\theta = 16 / (5\sqrt{17})$ and $\theta \approx 39.09°$. The cross product is $3 \cdot 1 - 4 \cdot 4 = -13$, and Lagrange's identity holds: $16^2 + 13^2 = 425 = 25 \cdot 17$.

**Perpendicular vectors.** $(3, 4) \cdot (-4, 3) = -12 + 12 = 0$. Rotating a vector by $90°$ counterclockwise maps $(x, y)$ to $(-y, x)$, and the result is always perpendicular to the original.

**A projection.** The projection of $v = (4, 1)$ on the line through the origin with direction $u = (3, 4)$ has parameter $16/25$, so it is the point $(48/25, 64/25)$.

**The between test.** Let $a = (0, 0)$ and $b = (4, 2)$. A point $p$ on the line $ab$ lies on the closed segment $ab$ if and only if $(p - a) \cdot (p - b) \le 0$, because the two vectors then point in opposite directions or one is zero. For $p = (2, 1)$ the value is $-5$, so $p$ is on the segment. For $p = (6, 3)$ and $p = (-2, -1)$ it is $15$, so these points are on the line but outside the segment. For the endpoint $p = (4, 2)$ it is $0$.

**Non-example: the dot product of two points.** $p \cdot q$ for points changes when the origin moves, so it has no geometric meaning. Only the dot product of two differences of points does.

**Non-example: the test without the collinearity check.** The test $(p - a) \cdot (p - b) \le 0$ alone says that $p$ is in the closed disk with diameter $ab$, not that $p$ is on the segment. The point $(2, 2)$ gives $(2, 2) \cdot (-2, 0) = -4$ but is not on the segment from $(0,0)$ to $(4,2)$. The test needs $\operatorname{orient}(a, b, p) = 0$ first.

## Related definitions

- [Cross product](/cross-product/): the companion product, $|u||v|\sin\theta$ with a sign, which gives the turn direction and the signed area.
- [Point and vector](/point-and-vector/): the objects that the product takes.
- [Point projection and reflection](/point-projection-and-reflection/) and [point-to-segment distance](/point-to-segment-distance/): direct uses of the projection formula.
- [Vector rotation](/vector-rotation/): a rotation keeps all dot products.
- [Accurate dot product](/accurate-dot-product/) and [compensated dot product](/dot2-compensated-dot-product/): the dot product in floating point with a small error bound.

## References
