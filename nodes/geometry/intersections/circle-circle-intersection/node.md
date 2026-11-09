---
tag: 4EXW3T
kind: problem
slug: circle-circle-intersection
name: Circle-circle intersection
aliases:
- Intersection of two circles
- two-circle intersection
area: geometry/intersections
level: intro
summary: Find the common points of two circles; subtracting the two equations gives the radical line, and the problem becomes a circle-line intersection with 0, 1 or 2 points.
prereqs: [circle-line-intersection]
see_also: [common-tangents-two-circles, line-line-intersection, quadratic-formula, collision-detection, bentley-ottmann-algorithm, floating-point-arithmetic, point-to-line-distance]
sources:
  - url: https://cp-algorithms.com/geometry/circle-circle-intersection.html
    title: cp-algorithms, Circle-Circle Intersection
    locator: the move of the first center to the origin, the radical line A = -2 x2, B = -2 y2, C = x2^2 + y2^2 + r1^2 - r2^2, and the special case of equal centers
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 4, Section 4.3.1, Sphere-sphere intersection (the overlap test by the squared distance of the centers against the squared sum of the radii)
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers 28(9), 1979
    locator: the sweep for many curves that meet in a bounded number of points, which covers the intersections of n circles
---

Circle-circle intersection asks for the common points of two circles in the plane. Two distinct circles meet in at most two points, and the case depends only on the distance $d$ of the centers and the two radii: two points if $|r_1 - r_2| < d < r_1 + r_2$, one point of tangency if $d$ equals the sum or the difference and $d > 0$, no point otherwise, and the whole circle if the circles are equal. Subtracting the two circle equations removes the squared terms and leaves the equation of a line, the radical line, so the points are the [circle-line intersection](/circle-line-intersection/) of either circle with that line. With integer input, the case test is the sign of integers and is exact.

## In plain words

Two rings drawn on paper can cross at two points, touch at one point, or not meet at all; one ring can also lie inside the other without touching. If the two rings are the same ring, they share every point.

To decide which case you have, measure the distance between the two centers and compare it with the sum and the difference of the two radii. To find the crossing points, use a trick: both crossing points lie on one straight line, which you get by subtracting the rule of one circle from the rule of the other. Then you only need to cut one circle with that line, which is a known and simple job.

## Definition

**Input.** Two circles $\Gamma_i = \{p : |p - c_i| = r_i\}$ for $i = 1, 2$, with centers $c_i \in \mathbb{R}^2$ and radii $r_i \ge 0$, usually with integer data.

**Output.** The set $\Gamma_1 \cap \Gamma_2$: no point, one point, two points, or the report "equal circles" when $\Gamma_1 = \Gamma_2$.

**Notation.** $v = c_2 - c_1$ and $d^2 = |v|^2$. After the move $c_1 = (0, 0)$ and $c_2 = (x_2, y_2)$, the radical line is

$$ \ell : A x + B y + C = 0, \qquad A = -2 x_2, \quad B = -2 y_2, \quad C = x_2^2 + y_2^2 + r_1^2 - r_2^2 . $$

**Model.** The [real RAM](/real-ram/). With integer input, $d^2$, $(r_1 \pm r_2)^2$ and the coefficients of $\ell$ are integers, so the case test is exact; the points need one square root.

## Variants

- **Decision only.** "Do the two disks overlap?" is $d^2 \le (r_1 + r_2)^2$, one comparison of integers; "do the two circles meet?" adds $d^2 \ge (r_1 - r_2)^2$.
- **Disks instead of circles.** The intersection of two disks is a lens bounded by two arcs; its area has a closed form from the two chord angles.
- **Spheres in 3D.** Two spheres meet in a circle in the radical plane, a point, or nothing, by the same distance test.
- **Many circles.** Report all intersection points of $n$ circles. There are at most $n (n - 1)$, and a sweep over $x$-monotone arcs reports them, as for segments in [Bentley-Ottmann](/bentley-ottmann-algorithm/).
- **Tangent lines.** The [common tangents of two circles](/common-tangents-two-circles/) come from the same distance and radius comparisons.

## Examples

**Two points.** $c_1 = (0, 0)$, $r_1 = 5$ and $c_2 = (6, 0)$, $r_2 = 5$. Then $A = -12$, $B = 0$, $C = 36 + 25 - 25 = 36$, so $\ell : x = 3$, and the circle $x^2 + y^2 = 25$ meets it at $(3, 4)$ and $(3, -4)$. Here $|r_1 - r_2| = 0 < d = 6 < 10$.

**External tangency.** $c_1 = (0, 0)$, $r_1 = 5$ and $c_2 = (9, 12)$, $r_2 = 10$. Then $d = 15 = r_1 + r_2$; the radical line is $-18 x - 24 y + 225 + 25 - 100 = 0$, that is $3 x + 4 y - 25 = 0$, which touches the first circle at $(3, 4)$.

**No point.** $c_1 = (0, 0)$, $r_1 = 5$ and $c_2 = (1, 0)$, $r_2 = 1$: $d = 1 < r_1 - r_2 = 4$, so the small circle lies inside the large one. The radical line $-2 x + 1 + 25 - 1 = 0$ is $x = 12.5$, outside both circles.

**Equal centers.** $c_1 = c_2$ gives $A = B = 0$; the circles are equal if $r_1 = r_2$ and disjoint otherwise.

## Known algorithms

**Radical line.** Move $c_1$ to the origin. If $c_1 = c_2$, answer "equal" or "none" from the radii. Otherwise compute $A, B, C$ as above and return the circle-line intersection of $x^2 + y^2 = r_1^2$ with $\ell$, moved back by $c_1$. This takes $O(1)$ operations and one square root. The circle-line step decides the case by the sign of $r_1^2 (A^2 + B^2) - C^2$, which equals $4 d^2 r_1^2 - (d^2 + r_1^2 - r_2^2)^2$; this factors as $\big((r_1 + r_2)^2 - d^2\big)\big(d^2 - (r_1 - r_2)^2\big)$, so it is the distance test in another form.

**Along the center line.** The chord of the two points is perpendicular to $v$. Its midpoint is $m = c_1 + a\, v / d$ with $a = (d^2 + r_1^2 - r_2^2) / (2 d)$, and the half chord is $\sqrt{r_1^2 - a^2}$. The points are $m \pm \sqrt{r_1^2 - a^2}\, v^{\perp} / d$. This is the same computation, with the distance $a$ from $c_1$ to the radical line made explicit.

**Exact representation.** With integer data, the midpoint $m$ is rational and the points are $m \pm \sqrt{Q} \cdot w$ with an integer $Q$ and a rational vector $w$, as in the circle-line implementation, so an exact program keeps the square root symbolic.

## Bounds

The problem has constant size, so $O(1)$ arithmetic operations are enough, and one square root is needed in general, since the points can be irrational: $c_1 = (0, 0)$, $r_1 = 2$, $c_2 = (2, 0)$, $r_2 = 2$ give $(1, \pm \sqrt{3})$. The case test is the sign of a polynomial of degree $4$ in the input, the product above, so an exact program needs integers about four times as wide as the input. For $n$ circles, $n (n - 1)$ points can occur, so reporting all of them takes $\Omega(n^2)$ time in the worst case.

## Reductions

- **To circle-line intersection.** Subtracting the equations $|p|^2 = r_1^2$ and $|p - c_2|^2 = r_2^2$ gives the linear equation of the radical line, and $\Gamma_1 \cap \Gamma_2 = \Gamma_1 \cap \ell$ when $c_1 \ne c_2$.
- **From two-circle tangency.** The tangent cases, and the [common tangents](/common-tangents-two-circles/), are the boundary cases $d = r_1 \pm r_2$ of the same test.
- **To a distance test.** "Do two disks overlap" is "is $d \le r_1 + r_2$", the basis of circle and sphere [collision detection](/collision-detection/).

## Applications

- **Trilateration.** A position from the distances to two known points is the intersection of two circles; a third circle picks one of the two points, as in GPS and in sensor networks.
- **Collision detection.** Circles and spheres are the cheapest bounding shapes, and the overlap test is one comparison of squared lengths.
- **Mechanism design.** The joint of a two-bar linkage with known bar lengths is an intersection of two circles, which gives the two "elbow" positions.
- **Geometric constructions.** Ruler-and-compass steps such as the perpendicular bisector and the equilateral triangle on a segment use the two points of two circles.

## References
