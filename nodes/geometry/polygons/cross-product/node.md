---
tag: EB0SYP
kind: definition
slug: cross-product
name: Cross product
aliases:
- two-dimensional cross product
- 2D cross product
- perp dot product
- wedge product of two vectors
area: geometry/polygons
level: intro
summary: Product of two vectors giving the signed area of their parallelogram, used to find orientation and turn direction.
prereqs: [point-and-vector]
see_also: [dot-product, orientation-test, oriented-triangle-area, shoelace-formula, geometry-primitives, determinant, segment-intersection-detection, angular-sort]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 33.1, Line-segment properties (the cross product as a determinant, the turn test and the segment intersection test)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1, Section 1.3, Area of Polygon (the cross product, the signed area of a triangle and the Left predicate)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 1 (the determinant that gives the signed area of a triangle and the turn of three points)
---

The cross product of two vectors in the plane is the number $u \times v = u_x v_y - u_y v_x$, the determinant of the 2 by 2 matrix with columns $u$ and $v$. Its absolute value is the area of the parallelogram spanned by $u$ and $v$, and its sign says whether $v$ points to the left of $u$ (positive) or to the right (negative). Applied to $u = q - p$ and $v = r - p$ it gives the [orientation test](/orientation-test/) and the [oriented area of a triangle](/oriented-triangle-area/), the predicate that most planar algorithms are built on.

## Definition

Points are $p = (x, y)$ and vectors are differences of points, as on [point and vector](/point-and-vector/). For $u, v \in \mathbb{R}^2$,

$$u \times v = \det \begin{pmatrix} u_x & v_x \\ u_y & v_y \end{pmatrix} = u_x v_y - u_y v_x .$$

It is the $z$-component of the three-dimensional cross product $(u_x, u_y, 0) \times (v_x, v_y, 0)$, whose other two components are $0$. Some texts call it the *perp dot product*, because $u \times v = u^{\perp} \cdot v$ with $u^{\perp} = (-u_y, u_x)$, the vector $u$ turned by $90°$ counterclockwise.

**Algebraic properties.** For all vectors $u, v, w$ and reals $c$:

- antisymmetric: $u \times v = -(v \times u)$, so $u \times u = 0$;
- bilinear: $(c u + w) \times v = c\,(u \times v) + w \times v$;
- $u \times v = 0$ if and only if $u$ and $v$ are parallel (one is a multiple of the other, or one is zero).

**The angle formula.** Let $\theta \in (-\pi, \pi]$ be the signed angle that turns the direction of $u$ to the direction of $v$, positive for a counterclockwise turn. For nonzero $u, v$,

$$u \times v = |u|\,|v| \sin\theta .$$

*Proof.* Write $u = |u|(\cos\alpha, \sin\alpha)$ and $v = |v|(\cos\beta, \sin\beta)$. Then $u \times v = |u||v|(\cos\alpha \sin\beta - \sin\alpha\cos\beta) = |u||v|\sin(\beta - \alpha)$, and $\beta - \alpha$ equals $\theta$ up to a multiple of $2\pi$. $\square$

**Area.** The parallelogram with sides $u$ and $v$ has base $|u|$ and height $|v||\sin\theta|$, so its area is $|u \times v|$. The triangle $p, q, r$ has area $\frac12 |(q - p) \times (r - p)|$.

**Orientation.** For three points,

$$\operatorname{orient}(p, q, r) = \operatorname{sign}\big((q - p) \times (r - p)\big) \in \{-1, 0, +1\}.$$

The value is $+1$ when $p, q, r$ make a counterclockwise (left) turn, $-1$ for a clockwise (right) turn, and $0$ when the three points are collinear. The expression is a polynomial of degree 2 in the coordinates. By the antisymmetry it changes sign under a swap of two points, and it does not change under a cyclic shift: $\operatorname{orient}(p, q, r) = \operatorname{orient}(q, r, p)$.

**Exactness.** With integer coordinates of absolute value below $B$, the value is an integer of absolute value at most $8B^2$, and its sign is exact. In floating point the two products can be almost equal, and the rounded difference can have the wrong sign for almost collinear points. The [orientation test](/orientation-test/) page shows such inputs, and [Shewchuk's expansion arithmetic](/shewchuk-expansion-sum/) gives an exact sign with float input.

## Examples and non-examples

**A worked example.** For $u = (3, 4)$ and $v = (4, 1)$: $u \times v = 3 \cdot 1 - 4 \cdot 4 = -13$. The parallelogram has area 13. The sign is negative, so $v$ is clockwise from $u$. With $p = (2, 1)$, $q = (5, 5)$ and $r = (6, 2)$, where $u = q - p$ and $v = r - p$, the triangle $pqr$ is clockwise and has area $13/2$. The swapped order $p, r, q$ gives $+13$, a counterclockwise triangle.

**Collinear points.** For $p = (0, 0)$, $q = (2, 1)$ and $r = (6, 3)$: $(2, 1) \times (6, 3) = 6 - 6 = 0$. The value $0$ does not say whether $r$ is between $p$ and $q$. That needs the [dot product](/dot-product/) test.

**Segment intersection.** Two segments $ab$ and $cd$ cross at one point inside both, with no endpoint on the other segment, if and only if $\operatorname{orient}(a, b, c)$ and $\operatorname{orient}(a, b, d)$ are nonzero with opposite signs, and $\operatorname{orient}(c, d, a)$ and $\operatorname{orient}(c, d, b)$ are nonzero with opposite signs. A zero value is the degenerate case of an endpoint on the other line, and [segment intersection detection](/segment-intersection-detection/) treats it separately.

**Sorting by angle without trigonometry.** To sort vectors by their angle around the origin, split the plane into two half-planes (for example $y > 0$, or $y = 0$ and $x > 0$, against the rest) and compare two vectors in the same half by the sign of $u \times v$. This is exact for integer input, while `atan2` rounds. See [angular sort](/angular-sort/).

**Non-example: the cross product of two points.** $p \times q$ for points depends on the origin. The sum $\sum_i p_i \times p_{i+1}$ in the [shoelace formula](/shoelace-formula/) is an exception: over a closed polygon the terms that depend on the origin cancel, so the total is the same for any origin.

**Non-example: the three-dimensional cross product.** In space, $u \times v$ is a vector perpendicular to both $u$ and $v$, not a number. The planar cross product is only its third component, for vectors in the plane $z = 0$.

## Related definitions

- [Dot product](/dot-product/): the companion product, $|u||v|\cos\theta$. Together, $(u \cdot v)^2 + (u \times v)^2 = |u|^2|v|^2$.
- [Orientation test](/orientation-test/): the sign of $(q - p) \times (r - p)$.
- [Oriented triangle area](/oriented-triangle-area/): half of $(q - p) \times (r - p)$, with its sign.
- [Determinant](/determinant/): the cross product is the 2 by 2 case; the orientation test in $d$ dimensions is a $(d+1)$ by $(d+1)$ determinant.
- [Shoelace formula](/shoelace-formula/): the signed area of a polygon as a sum of cross products.
- [Point and vector](/point-and-vector/): the objects that the product takes.

## References
