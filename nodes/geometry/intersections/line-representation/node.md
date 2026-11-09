---
tag: M1G12D
kind: concept
slug: line-representation
name: Line representation
aliases: [line equation forms, representations of a line, forms of a line]
area: geometry/intersections
level: intro
summary: The ways to describe a line in the plane, as a general equation, normal form, slope and intercept, point and direction, two points or homogeneous coordinates, and exact conversions between them.
prereqs: [point-and-vector, cross-product]
see_also: [line-equation-from-segment, line-line-intersection, point-to-line-distance, half-plane-intersection, orientation-test, dot-product, line-arrangement, segment-intersection-point]
sources:
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1 (the left-of test from the signed area of a triangle) and Chapter 7, Section 7.2 (segment intersection with the parametric form of a line)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 8, Section 8.2, Duality (the slope-intercept form y = mx - b and the dual point (m, b))
  - url: https://cp-algorithms.com/geometry/segment-to-line.html
    title: cp-algorithms, Finding the equation of a line for a segment
    locator: the general form Ax + By + C = 0 from two points and its normalization in the integer and the real case
---

A line in the plane can be written in several forms: the general equation $A x + B y + C = 0$, the normal form with a unit normal, the slope-intercept form $y = m x + b$, a point with a direction, two points, or a triple of homogeneous coordinates. Each form is good for some tasks and bad for others. The general form handles every line, including vertical ones, and with integer input it stays in integers; the point-direction form is natural for segments and rays; the normal form gives distances directly. Algorithms on lines need fast and exact conversions between them, and a canonical form to decide whether two descriptions give the same line.

## In plain words

There are many ways to tell someone where a straight line is. You can name two points on it. You can name one point and the direction in which the line goes. You can say how steep it is and where it crosses the vertical axis, which fails for a line that goes straight up. Or you can give a rule that a point must satisfy to lie on the line, such as "twice the first coordinate plus the second equals five".

All these ways describe the same thing, and you can change from one to another with a few multiplications. The rule form is the most useful in programs, because it works for every line and because the sign of the rule tells on which side of the line a point is.

## The idea

**Notation.** Points are $p = (p_x, p_y)$, $\operatorname{cross}(u, v) = u_x v_y - u_y v_x$ and $u \cdot v = u_x v_x + u_y v_y$ are the [cross product](/cross-product/) and the [dot product](/dot-product/).

**General form.** $\ell = \{(x, y) : A x + B y + C = 0\}$ with $(A, B) \ne (0, 0)$. The vector $n = (A, B)$ is a normal of $\ell$ and $(-B, A)$ is a direction. The triple is defined up to a nonzero factor: $(A, B, C)$ and $(\lambda A, \lambda B, \lambda C)$ give the same line. The value $f(p) = A p_x + B p_y + C$ is positive on one side of $\ell$, negative on the other and zero on it, so the general form also describes the two closed half-planes $f \ge 0$ and $f \le 0$.

**Normal form.** If $A^2 + B^2 = 1$, then $f(p)$ is the signed distance from $p$ to $\ell$. The Hesse normal form writes this as $x \cos \theta + y \sin \theta = \rho$, with the angle $\theta$ of the normal and the distance $\rho \ge 0$ from the origin. Normalizing needs a square root, so it is not exact with rational input; for the distance alone, $|f(p)| / \sqrt{A^2 + B^2}$ is enough (see [point-to-line distance](/point-to-line-distance/)).

**Slope-intercept form.** $y = m x + b$ with $m = -A / B$ and $b = -C / B$, for $B \ne 0$. It cannot describe vertical lines, and $m$ becomes large and inaccurate for steep lines. Its strength is that $(m, b)$ is a point: [point-line duality](/line-arrangement-construction/) maps the line $y = m x - b$ to the point $(m, b)$.

**Point and direction.** $\ell = \{p + t d : t \in \mathbb{R}\}$ with a point $p$ and a direction $d \ne 0$. It also gives an orientation: the side to the left of $d$ is where $\operatorname{cross}(d, x - p) > 0$. Restricting $t$ to $[0, 1]$ gives the segment from $p$ to $p + d$, and $t \ge 0$ gives a ray. The [half-plane intersection](/half-plane-intersection-deque/) code uses this form.

**Two points.** $\ell$ through $p \ne q$. This is the point-direction form with $d = q - p$, and the general form has $A = p_y - q_y$, $B = q_x - p_x$, $C = -(A p_x + B p_y) = \operatorname{cross}(p, q)$; the [line equation from a segment](/line-equation-from-segment/) page derives it. Then $A x + B y + C = \operatorname{cross}(q - p, x - p)$, the [orientation test](/orientation-test/) of $p, q, x$.

**Homogeneous coordinates.** The point $(x, y)$ becomes $(x : y : 1)$ and the line becomes $(A : B : C)$, with incidence $A x + B y + C \cdot 1 = 0$. The line through two points is the cross product in $\mathbb{R}^3$ of their homogeneous coordinates, and the intersection point of two lines is the cross product of their coefficient triples. Parallel lines meet in a point $(x : y : 0)$ at infinity, so there is no special case.

**Conversions.**

| from | to | formula |
| --- | --- | --- |
| two points $p, q$ | general | $A = p_y - q_y$, $B = q_x - p_x$, $C = \operatorname{cross}(p, q)$ |
| point $p$, direction $d$ | general | $A = -d_y$, $B = d_x$, $C = d_y p_x - d_x p_y$ |
| general | point and direction | $d = (-B, A)$, $p = -C (A, B) / (A^2 + B^2)$, the point next to the origin |
| general, $B \ne 0$ | slope-intercept | $m = -A / B$, $b = -C / B$ |
| general | normal form | divide by $\sqrt{A^2 + B^2}$ |

**Canonical form.** To test whether two descriptions give the same line, or to use lines as keys of a hash table, bring them to one form. With integer coefficients, divide $(A, B, C)$ by $\gcd(|A|, |B|, |C|)$ and multiply by $-1$ if $A < 0$, or if $A = 0$ and $B < 0$. Then two integer triples describe the same line exactly when their canonical forms are equal. Without normalizing, test $A_1 B_2 = A_2 B_1$, $A_1 C_2 = A_2 C_1$ and $B_1 C_2 = B_2 C_1$.

**Exactness.** With integer points of absolute value at most $U$, the two-point form gives $|A|, |B| \le 2U$ and $|C| \le 2U^2$, and every later test, such as the side of a point or the intersection of two lines, is a polynomial in these numbers. So the general form, the point-direction form and the homogeneous form are exact in integer or rational arithmetic. The normal form and the slope-intercept form of a vertical line are not.

## Examples

**One line in all forms.** The line through $p = (1, 2)$ and $q = (4, 6)$:

| form | description |
| --- | --- |
| two points | $(1, 2)$ and $(4, 6)$ |
| point and direction | $(1, 2) + t (3, 4)$ |
| general | $-4 x + 3 y - 2 = 0$, canonical $4 x - 3 y + 2 = 0$ |
| normal form | $\frac{4}{5} x - \frac{3}{5} y + \frac{2}{5} = 0$, the origin is at distance $2/5$ |
| slope-intercept | $y = \frac{4}{3} x + \frac{2}{3}$ |
| homogeneous | $(4 : -3 : 2)$ |

The point $(0, 0)$ gives $4 \cdot 0 - 3 \cdot 0 + 2 = 2 > 0$, so it lies on the positive side of $4 x - 3 y + 2 = 0$; in the oriented general form from $p$ to $q$, $-4 x + 3 y - 2$, it is negative, so the origin is to the right of the direction from $p$ to $q$.

**A vertical line.** $x = 3$ is $1 \cdot x + 0 \cdot y - 3 = 0$, or $(3, 0) + t (0, 1)$, but it has no slope-intercept form.

**Same line, other numbers.** $(2, 4, -6)$ and $(-1, -2, 3)$ both have the canonical form $(1, 2, -3)$, the line $x + 2y = 3$.

## Where it is used

- **Intersections.** The [intersection of two lines](/line-line-intersection/) is a $2 \times 2$ linear system in the general form, solved by Cramer's rule; [segment intersection](/segment-intersection-point/) uses the point-direction form with parameters in $[0, 1]$.
- **Half-planes and clipping.** [Half-plane intersection](/half-plane-intersection/) and polygon clipping need lines with an orientation, given by the general form or by a point and a direction.
- **Distances and circles.** The normal form gives the distance to a line, used by [circle-line intersection](/circle-line-intersection/) and [common tangents of two circles](/common-tangents-two-circles/).
- **Duality and arrangements.** The slope-intercept form maps lines to points and back for [arrangements](/line-arrangement/) and the convex hull trick.
- **Hough transform.** Image analysis detects lines by voting in the $(\theta, \rho)$ parameters of the Hesse normal form, which covers every line, vertical or not, with bounded parameters.
- **Projective geometry and graphics.** Homogeneous coordinates make "join" and "meet" of points and lines the same cross product and remove the parallel case.

## References
