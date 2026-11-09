---
tag: SGBK99
kind: algorithm
slug: circle-line-intersection
name: Circle-line intersection
aliases:
- Intersection of a circle and a line
- line-circle intersection
area: geometry/intersections
level: intro
summary: Find the 0, 1 or 2 points where a line meets a circle, from the foot of the perpendicular from the center and the half-length of the chord.
model: real-ram
complexity:
  vars: {U: the largest absolute value of an input number}
  time: {worst: O(1)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1637
  people: [René Descartes]
  note: Descartes, in La Géométrie of 1637, solved quadratic equations by cutting a circle with a line, which is this computation read backwards; the exact case test by the sign of one integer is standard in robust geometry code.
prereqs: [line-representation, point-to-line-distance]
see_also: [circle-circle-intersection, line-line-intersection, segment-intersection-point, common-tangents-two-circles, quadratic-formula, collision-detection, floating-point-arithmetic, line-clipping]
sources:
  - url: https://cp-algorithms.com/geometry/circle-line-intersection.html
    title: cp-algorithms, Circle-Line Intersection
    locator: the move of the center to the origin, the foot of the perpendicular (-A C / (A^2 + B^2), -B C / (A^2 + B^2)), the comparison of C^2 with r^2 (A^2 + B^2), and the two points at distance d along the line
  - book: isbn:9781558607323
    title: Christer Ericson, Real-Time Collision Detection, Morgan Kaufmann, 2005
    locator: Chapter 5, Section 5.3.2, Intersecting ray or segment against sphere (the same quadratic in the ray parameter, and the early exit by the sign of the discriminant)
---

Circle-line intersection finds the common points of a line $A x + B y + C = 0$ and a circle with center $c$ and radius $r$. The algorithm drops a perpendicular from $c$ to the line: its foot $h$ is the point of the line nearest to $c$, and the line meets the circle in two points, one point or no point as the distance $|c h|$ is less than, equal to or more than $r$. The two points are $h \pm t u$, where $u$ is the unit direction of the line and $t = \sqrt{r^2 - |c h|^2}$ is half the length of the chord. The case test is the sign of one integer when the input is integer, so it is exact, and only the final coordinates need a square root.

## In plain words

Draw a circle and a straight line. The line can miss the circle, touch it at one point, or cut through it at two points. To find out which, walk from the center of the circle straight toward the line, at a right angle. The spot where you reach the line is the closest point of the line to the center.

If that spot is farther away than the radius, the line misses. If it is exactly at the radius, the line touches the circle there. If it is closer, the line cuts the circle at two points, the same distance to the left and to the right of that spot. The theorem of Pythagoras gives that distance.

## The problem

**Input.** A circle with integer center $c = (c_x, c_y)$ and integer radius $r \ge 0$, and a line $\ell : A x + B y + C = 0$ with integers and $(A, B) \ne (0, 0)$, all of absolute value at most $U$.

**Output.** The set $\ell \cap \{p : |p - c| = r\}$, which has $0$, $1$ or $2$ points.

**Notation.** $N = A^2 + B^2$ and $e = A c_x + B c_y + C$, the value of the line equation at the center. The distance from $c$ to $\ell$ is $|e| / \sqrt{N}$ (see [distance to a line](/point-to-line-distance/)). $D = r^2 N - e^2$, so that $D / N = r^2 - e^2 / N$ is the squared half-length of the chord; the sign of $D$ decides the case.

**Model.** The [real RAM](/real-ram/). The implementation uses exact integers and `Fraction`s, and it returns each point as $h + s \sqrt{D}$ with rational $h$ and $s$, so that no rounding happens.

## The algorithm

```pseudo id=main
CIRCLE-LINE(c, r, A, B, C)
L1  if (A, B) = (0, 0) then error "not a line"
L2  N ← A² + B², e ← A·c_x + B·c_y + C
L3  h ← (c_x − e·A / N, c_y − e·B / N)         ▷ foot of the perpendicular
L4  D ← r²·N − e²                               ▷ sign of r² − dist(c, ℓ)²
L5  if D < 0 then return ∅
L6  if D = 0 then return {h}                    ▷ tangent
L7  u ← (−B, A) / N, return {h + √D·u, h − √D·u}
```

Line L3 moves from $c$ along the normal $(A, B)$ by the amount that makes the line equation zero. Line L4 compares the squared distance $e^2 / N$ with $r^2$ after a multiplication by $N > 0$, so its sign is exact on integers. In line L7, $\sqrt{D} \cdot |u| = \sqrt{D} / \sqrt{N} = \sqrt{r^2 - e^2 / N}$ is half the chord. The implementation keeps $\sqrt{D}$ symbolic: a point is the triple $(h, u, D)$, and it is a rational point exactly when $D$ is a perfect square.

## Example

Circle with center $(0, 0)$ and $r = 5$, against three lines, and one circle with center $(1, 1)$:

| circle | line | $N$ | $e$ | $h$ (L3) | $D$ (L4) | answer |
| --- | --- | --- | --- | --- | --- | --- |
| $(0, 0), 5$ | $x + y - 7 = 0$ | 2 | $-7$ | $(7/2, 7/2)$ | $50 - 49 = 1$ | $(3, 4)$ and $(4, 3)$ |
| $(0, 0), 5$ | $3x + 4y - 25 = 0$ | 25 | $-25$ | $(3, 4)$ | $625 - 625 = 0$ | tangent at $(3, 4)$ |
| $(0, 0), 5$ | $x - 6 = 0$ | 1 | $-6$ | $(6, 0)$ | $25 - 36 < 0$ | none |
| $(1, 1), 5$ | $3x + 4y - 2 = 0$ | 25 | $5$ | $(2/5, 1/5)$ | $625 - 25 = 600$ | $(2/5, 1/5) \pm \sqrt{600}\,(-4, 3)/25$ |

In the first row $u = (-1/2, 1/2)$ and $\sqrt{D} = 1$, so the points are $(7/2 - 1/2, 7/2 + 1/2) = (3, 4)$ and $(4, 3)$. In the last row the center has distance $5/5 = 1$ from the line, the half chord is $\sqrt{25 - 1} = 2\sqrt{6}$, and the points $(2/5 \mp 8\sqrt{6}/5,\ 1/5 \pm 6\sqrt{6}/5)$ are irrational.

## Correctness

The point $h$ of line L3 is on $\ell$: $A h_x + B h_y + C = e - e (A^2 + B^2) / N = 0$. The vector $c - h = e (A, B) / N$ is normal to $\ell$, so $h$ is the foot of the perpendicular and $|c - h|^2 = e^2 / N$. Each point $p$ of $\ell$ is $p = h + t w$ with $w = (-B, A) / \sqrt{N}$ a unit direction of $\ell$, and by Pythagoras $|p - c|^2 = e^2 / N + t^2$. So $p$ is on the circle if and only if $t^2 = r^2 - e^2 / N = D / N$. This has no real solution for $D < 0$, the one solution $t = 0$ for $D = 0$, and the two solutions $t = \pm \sqrt{D / N}$ for $D > 0$; these are lines L5, L6 and L7, since $\sqrt{D / N}\, w = \sqrt{D}\, (-B, A) / N = \sqrt{D}\, u$. The full proof is in the proof file.

## Complexity

The algorithm does a constant number of arithmetic operations and at most one square root, so it takes $O(1)$ time and $\Theta(1)$ extra space. On integers of absolute value at most $U$, $N \le 2U^2$, $|e| \le 3U^2$ and $|D| \le 9 U^4$, so the case test needs integers about four times as wide as the input.

## Properties

- **Exact case test.** The answer "0, 1 or 2 points" is the sign of the integer $D$; no tolerance is needed.
- **No special cases.** Vertical lines ($B = 0$), horizontal lines, a line through the center ($e = 0$) and a point circle ($r = 0$) all go through the same lines.
- **One square root.** Only the coordinates of the two points need $\sqrt{D}$, and the foot $h$ is always rational.
- **Symmetric output.** The two points are symmetric about $h$, which is the midpoint of the chord.

## Variants and improvements

- **Parametric form.** For a line $p + t d$, substitute into $|x - c|^2 = r^2$ and solve the quadratic $|d|^2 t^2 + 2 (p - c) \cdot d\, t + |p - c|^2 - r^2 = 0$ with the [quadratic formula](/quadratic-formula/). This gives the parameters directly, which ray casting needs.
- **Segment or ray against a circle.** Keep the roots $t$ in $[0, 1]$ or $[0, \infty)$. For a pure yes or no test, compare the distance from $c$ to the segment with $r$ instead.
- **Sphere and line in 3D.** The same foot-of-perpendicular argument works with $h$ the projection of $c$ on the line.
- **Two circles.** Subtracting the two circle equations gives the radical line, and [circle-circle intersection](/circle-circle-intersection/) becomes this algorithm.
- **Numerically stable roots.** In floating point, compute the root of larger magnitude first and the other from the product of the roots, to avoid cancellation.

## When to use it

Use it for ray casting against circles and spheres, for clipping a line to a circular window, for the points where a robot path crosses a safety radius, and as the inner step of circle-circle intersection and of tangent constructions. When only the number of points matters, compute the sign of $D$ alone; when the points feed an exact algorithm, keep them in the form $h \pm \sqrt{D} u$.

## Pitfalls

- **A tolerance in line L4.** Comparing a floating-point distance with $r$ by `abs(dist - r) < eps` makes tangent lines unstable and makes the result depend on the scale; use the exact sign of $D$ on integers or rationals.
- **Dividing by $\sqrt{N}$ too early.** Normalizing the line to unit length before line L3 brings in a square root and rounding into the case test; keep $N$ and divide only in lines L3 and L7.
- **Forgetting the center.** The cp-algorithms formulas assume the center at the origin; for a general center, line L2 must use $e = A c_x + B c_y + C$, not $C$.
- **Two equal points.** For $D = 0$ line L7 would return $h$ twice; line L6 must return one point, or a caller that counts crossings counts the tangent twice.

## Implementations

## History

The intersection of a line and a circle is as old as ruler-and-compass geometry: Euclid's Elements, Book III, treats chords and tangents of a circle. Descartes, in La Géométrie of 1637, used the cut of a circle by a line to construct the roots of quadratic equations, and the computation here is the same quadratic. The exact test by the sign of $r^2 N - e^2$ is the standard form in robust computational geometry code.

## References
