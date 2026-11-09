---
tag: 1KXJYH
kind: problem
slug: common-tangents-two-circles
name: Common tangents of two circles
aliases: [common tangents to two circles, bitangents of two circles, tangent lines of two circles]
area: geometry/intersections
level: core
summary: Find all lines tangent to two given circles; there are 0, 1, 2, 3 or 4 of them, or infinitely many, and each is found from one quadratic equation for its unit normal.
prereqs: [circle-line-intersection, line-representation, point-to-line-distance]
see_also: [circle-circle-intersection, line-line-intersection, quadratic-formula, minkowski-sum, convex-hull, rotating-calipers, floating-point-arithmetic, in-circle-test]
sources:
  - url: https://cp-algorithms.com/geometry/tangents-to-two-circles.html
    title: cp-algorithms, Finding common tangents to two circles
    locator: the whole article (the reduction to a line at distances r1 and r2 from two points, the four sign cases and the degenerate cases)
  - book: isbn:9780521649766
    title: Joseph O'Rourke, Computational Geometry in C, second edition, Cambridge University Press, 1998
    locator: Chapter 1 and Chapter 7 (lines, distances and tangents from a point used by the primitives)
---

The common tangents of two circles are the lines that touch both circles. Two circles with centers $c_1, c_2$ and radii $r_1, r_2$ have four common tangents if they are apart, three if they touch from outside, two if they cross, one if they touch from inside, none if one lies strictly inside the other, and infinitely many if they are equal. Each tangent is a line at signed distance $\pm r_1$ from $c_1$ and $\pm r_2$ from $c_2$, so the problem reduces to a quadratic equation for the unit normal of the line, and the answer comes from the distance $d = |c_1 c_2|$ compared with $|r_1 - r_2|$ and $r_1 + r_2$.

## In plain words

Put two coins on a table and lay a ruler so that it touches both coins. If the coins are apart, there are four ways: two with both coins on the same side of the ruler, and two that pass between the coins. If the coins overlap, only the two outer ways are left. If one coin is inside the other, there is no way at all.

A ruler touches a coin exactly when the distance from the coin's center to the ruler equals the coin's radius. So you look for lines with given distances to two points. You choose for each coin on which side of the ruler it lies, and each choice gives at most two lines.

## Definition

**Input.** Two circles $C_1 = (c_1, r_1)$ and $C_2 = (c_2, r_2)$ with $r_1, r_2 \ge 0$. A circle of radius zero is a point, and then the tangents are the lines through that point that touch the other circle.

**Output.** All lines $\ell$ with $\operatorname{dist}(c_1, \ell) = r_1$ and $\operatorname{dist}(c_2, \ell) = r_2$, with their tangent points on each circle. A line is given as $a x + b y + c = 0$ with $a^2 + b^2 = 1$, so that $a x + b y + c$ is the signed distance of $(x, y)$ from the line.

**Outer and inner tangents.** A tangent is *outer* (or direct) if both circles lie on the same side of it, and *inner* (or transverse) if it separates them. The outer tangents meet at the external center of similarity, and the inner tangents meet at the internal center of similarity on the segment $c_1 c_2$, which divides it in the ratio $r_1 : r_2$.

**Notation.** $d = |c_2 - c_1|$. With signs $\sigma_1, \sigma_2 \in \{+1, -1\}$, a line with $a c_{1x} + b c_{1y} + c = \sigma_1 r_1$ and $a c_{2x} + b c_{2y} + c = \sigma_2 r_2$ is tangent to both. Same signs give outer tangents, and opposite signs give inner ones.

## Variants

- **Count only.** The number of common tangents depends only on $d$, $|r_1 - r_2|$ and $r_1 + r_2$: 4 if $d > r_1 + r_2$; 3 if $d = r_1 + r_2$; 2 if $|r_1 - r_2| < d < r_1 + r_2$; 1 if $d = |r_1 - r_2| > 0$; 0 if $d < |r_1 - r_2|$; infinitely many if $d = 0$ and $r_1 = r_2 > 0$. With integer input, these are exact comparisons of $d^2$ with $(r_1 \pm r_2)^2$.
- **Tangents from a point.** If $r_2 = 0$, the problem is the tangents from the point $c_2$ to $C_1$: two if $c_2$ is outside, one if it is on $C_1$, none if it is inside.
- **Tangents of two convex polygons.** The common tangents of two convex polygons, used to merge two convex hulls, are found by [rotating calipers](/rotating-calipers/) or binary search; the circle case is the smooth version.
- **Belt problem.** The length of a belt around two pulleys uses the outer tangents (open belt) or the inner tangents (crossed belt).

## Examples

**Four tangents with rational numbers.** Let $C_1$ have center $(0, 0)$ and radius $1$, and $C_2$ center $(10, 0)$ and radius $7$. Then $d = 10 > r_1 + r_2 = 8$, so there are four tangents.

| kind | sides of the line | line | tangent point on $C_1$ | tangent point on $C_2$ |
| --- | --- | --- | --- | --- |
| outer | same | $3x + 4y + 5 = 0$ | $(-3/5, -4/5)$ | $(29/5, -28/5)$ |
| outer | same | $3x - 4y + 5 = 0$ | $(-3/5, 4/5)$ | $(29/5, 28/5)$ |
| inner | opposite | $4x + 3y - 5 = 0$ | $(4/5, 3/5)$ | $(22/5, -21/5)$ |
| inner | opposite | $4x - 3y - 5 = 0$ | $(4/5, -3/5)$ | $(22/5, 21/5)$ |

For the line $3x + 4y + 5 = 0$ with unit normal $(3/5, 4/5)$, the signed distance of $(0, 0)$ is $5/5 = 1$ and that of $(10, 0)$ is $35/5 = 7$, so the line touches both circles from the same side. The tangent point on a circle is its center minus the signed distance times the unit normal. The two outer tangents meet at $(-5/3, 0)$, the external center of similarity, and the two inner ones at $(5/4, 0)$, which divides the segment from $(0, 0)$ to $(10, 0)$ in the ratio $1 : 7$.

**Crossing circles.** For $C_1 = ((0,0), 2)$ and $C_2 = ((3, 0), 2)$, $d = 3 < 4$, so only the two outer tangents $y = 2$ and $y = -2$ exist.

**Nested circles.** For $C_1 = ((0,0), 5)$ and $C_2 = ((1, 0), 1)$, $d = 1 < 4 = r_1 - r_2$, so there is no common tangent.

## Known algorithms

**The quadratic for the normal.** Move $c_1$ to the origin and put $(\Delta x, \Delta y) = c_2 - c_1$. For a sign pair, let $r = \sigma_2 r_2 - \sigma_1 r_1$. A unit normal $(a, b)$ of a tangent must satisfy $a \Delta x + b \Delta y = r$ and $a^2 + b^2 = 1$. With $z = \Delta x^2 + \Delta y^2 = d^2$ and $D = z - r^2$:

- if $D < 0$, there is no tangent of this kind;
- otherwise $a = (r \Delta x \mp \Delta y \sqrt{D}) / z$ and $b = (r \Delta y \pm \Delta x \sqrt{D}) / z$, which gives one line for $D = 0$ and two for $D > 0$, and then $c = \sigma_1 r_1 - (a c_{1x} + b c_{1y})$.

The sign pairs $(\sigma_1, \sigma_2)$ and $(-\sigma_1, -\sigma_2)$ give the same lines, so two pairs suffice: $(+, +)$ for the outer and $(+, -)$ for the inner tangents. The whole computation takes $O(1)$ time and one square root per kind.

**Exactness.** With integer centers and radii, the case analysis (the signs of $D$ for the two kinds, and $z = 0$) is exact in integers. The lines themselves contain $\sqrt{D}$, so they are exact only in an extension of the rational numbers, or as floating-point approximations computed after the exact case decision.

**Geometric construction.** The classic construction draws the circle with center $c_1$ and radius $r_1 \pm r_2$, takes the tangents from $c_2$ to it, and moves them by $r_2$. It gives the same lines.

## Bounds

The problem has constant size: $O(1)$ arithmetic operations and at most two square roots. The interesting questions are numerical. When $D$ is close to zero, the two tangents of a kind are close, and a floating-point computation can report two lines, one line or none. Deciding the case from exact integer comparisons first avoids this.

## Reductions

- **To two distances from a line.** A line is tangent to a circle exactly when the [distance](/point-to-line-distance/) from the center to the line equals the radius. So the problem is to find lines at given signed distances from two points.
- **To tangents from a point.** Shrink $C_2$ to its center and grow or shrink $C_1$ by $r_2$: the outer tangents become tangents from $c_2$ to the circle of radius $|r_1 - r_2|$ around $c_1$, and the inner tangents become tangents to the circle of radius $r_1 + r_2$. This is a [Minkowski sum](/minkowski-sum/) of the circles with a disk.
- **To circle-line intersection.** The tangent points from a point $c$ to a circle $C$ are the [intersection of $C$](/circle-line-intersection/) with the polar line of $c$, or with the circle on the diameter from $c$ to the center of $C$.

## Applications

- **Convex hull of disks.** The boundary of the convex hull of a set of disks consists of arcs and outer common tangents.
- **Shortest paths around circular obstacles.** A shortest path among disks runs along outer and inner common tangents and arcs; the visibility graph of the disks uses all common tangents.
- **Belts, pulleys and cams.** The length and the contact points of belts.
- **Computer graphics and CAD.** Fillets and smooth connections between two round shapes, and the outline of a stroke with round caps.

## References
