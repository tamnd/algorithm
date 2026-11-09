---
tag: XQG3E1
kind: algorithm
slug: point-to-segment-distance
name: Distance from a point to a segment
aliases:
- point-segment distance
- distance to a line segment
area: geometry/proximity
level: intro
summary: Algorithm that computes the shortest distance from a point to a segment by comparing the projection with the endpoints.
model: real-ram
complexity:
  vars: {d: the dimension}
  time: {worst: Θ(d)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, recursive: false}
prereqs: [point-to-line-distance, euclidean-distance, dot-product]
see_also: [point-projection-and-reflection, hausdorff-distance, frechet-distance, alt-godau-algorithm, polygon-simplification, segment-intersection-detection]
sources:
  - book: isbn:9781558605947
    title: Philip J. Schneider and David H. Eberly, Geometric Tools for Computer Graphics, Morgan Kaufmann, 2003
    locator: Chapter 6, Distance in 2D, Section 6.1 (point to line, ray and segment, by clamping the projection parameter)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 33, Section 33.1 (cross and dot products of segments, computed without division)
  - paper: doi:10.1142/S0218195995000064
    title: Helmut Alt and Michael Godau, Computing the Fréchet distance between two polygonal curves, International Journal of Computational Geometry and Applications 5(1-2), 1995
    locator: the free space of a point against a segment (the points of a segment within distance eps of a point form one interval)
---

The distance from a point $p$ to a segment $ab$ is the smallest distance from $p$ to a point of the segment. Project $p$ on the line through $a$ and $b$. If the projection falls inside the segment, the answer is the [distance to the line](/point-to-line-distance/); otherwise it is the distance to the nearer end point. The test needs only the sign of a [dot product](/dot-product/) and one comparison, so with integer coordinates the squared distance is an exact fraction and no root is taken before the result is reported.

## In plain words

You stand near a straight fence of fixed length and want to touch it with the shortest walk. Imagine the fence going on forever and drop the shortest path onto it. If that path lands on the real fence, you are done: walk straight there. If it lands past one end of the fence, the real fence is not there, and the closest part of the fence is that end post. So walk to the end post.

Two quick tests tell you which case you are in. One test checks whether you are behind the first post, and the other checks whether you are past the second post. Both tests use only multiplications and additions. Keep the result squared, and whole-number coordinates give an exact answer.

## The problem

**Input.** Points $a$, $b$ and $p$ in $\mathbb{R}^2$ (or $\mathbb{R}^d$) with integer or rational coordinates. The segment $ab = \{a + t(b - a) : 0 \le t \le 1\}$ may be a single point when $a = b$.

**Output.** The squared distance $\delta^2 = \min_{0 \le t \le 1} \|p - (a + t(b - a))\|^2$ as an exact rational, and the closest point $c$ of the segment, where the minimum is reached. The distance is $\delta = \sqrt{\delta^2}$.

We write $u = b - a$, $w = p - a$, $u \cdot w$ for the dot product and $u \times w = u_x w_y - u_y w_x$ for the cross product.

## The algorithm

```pseudo id=main
POINT-SEGMENT-DISTANCE-SQUARED(p, a, b)    ▷ squared distance from p to the segment ab
L1  u ← b − a
L2  w ← p − a
L3  s ← w · u                                ▷ s ≤ 0: the projection is at or before a
L4  if s ≤ 0 then return (w · w, a)
L5  D ← u · u                                ▷ D > 0 here, because s > 0 forces u ≠ 0
L6  if s ≥ D then return (‖p − b‖², b)      ▷ the projection is at or after b
L7  c ← u × w
L8  return (c² / D, a + (s / D) · u)         ▷ the projection is inside the segment
```

The projection of $p$ on the line has parameter $t^* = s / D$. Line L4 handles $t^* \le 0$ and line L6 handles $t^* \ge 1$, both without a division. Line L8 is the [point-line distance](/point-to-line-distance/) in its cross product form. When $a = b$, $u = 0$ and $s = 0$, so line L4 returns the point distance $\|p - a\|^2$ and line L5 never divides by zero. In $\mathbb{R}^d$, replace line L8 by $\|w\|^2 - s^2 / D$.

## Example

Take $a = (1, 1)$ and $b = (7, 9)$, so $u = (6, 8)$ and $D = 100$. The table follows four query points through the algorithm.

| $p$ | $w$ | $s = w \cdot u$ | case | $\delta^2$ | closest point |
| --- | --- | --- | --- | --- | --- |
| $(8, 2)$ | $(7, 1)$ | $50$ | L8, $t^* = 1/2$ | $(-50)^2 / 100 = 25$ | $(4, 5)$ |
| $(2, 7)$ | $(1, 6)$ | $54$ | L8, $t^* = 27/50$ | $28^2 / 100 = 196/25$ | $(106/25, 133/25)$ |
| $(10, 12)$ | $(9, 11)$ | $142$ | L6, $s \ge 100$ | $3^2 + 3^2 = 18$ | $(7, 9)$ |
| $(-2, 0)$ | $(-3, -1)$ | $-26$ | L4, $s \le 0$ | $9 + 1 = 10$ | $(1, 1)$ |

For $p = (10, 12)$ the distance to the line would be $|6 \cdot 11 - 8 \cdot 9| / 10 = 0.6$, much less than the true $\sqrt{18} \approx 4.24$, because the foot on the line is beyond $b$.

## Correctness

For $t \in \mathbb{R}$ let $g(t) = \|w - t u\|^2$. If $u \ne 0$, $g$ is a quadratic with positive leading coefficient $D$ and minimizer $t^* = s / D$, so it decreases on $(-\infty, t^*]$ and increases on $[t^*, \infty)$. Its minimum on $[0, 1]$ is therefore at $\mathrm{clamp}(t^*) = \min(1, \max(0, t^*))$. The tests $s \le 0$ and $s \ge D$ are the tests $t^* \le 0$ and $t^* \ge 1$ multiplied by $D > 0$. In the middle case $g(t^*)$ is the squared distance to the line, which equals $c^2 / D$ by Lagrange's identity. If $u = 0$ the segment is the point $a$ and line L4 returns its squared distance. The full proof is in the correctness proof below.

## Complexity

The algorithm does a fixed number of operations: two dot products, one cross product, at most one division, and at most one more squared distance. It takes $\Theta(1)$ time in the plane and $\Theta(d)$ time in $\mathbb{R}^d$ on the [real RAM](/real-ram/), with $\Theta(1)$ extra space. With integer coordinates of absolute value at most $M$, the cases L4 and L6 return integers of at most $8M^2$, and the case L8 returns a fraction whose numerator is at most $64 M^4$.

## Properties

- **Exact.** Each step is a ring or field operation on rationals. The branch tests compare integers when the input is integer.
- **Continuous in $p$.** The three formulas agree on the boundaries of the cases: at $s = 0$, $c^2/D = \|w\|^2$ because $w$ is orthogonal to $u$, and similarly at $s = D$.
- **Convex distance function.** $p \mapsto \delta(p)$ is the distance to a convex set, so it is a convex function. The set of points within distance $\varepsilon$ of the segment is a stadium: a rectangle with two half discs.
- **The other way round.** For a fixed point and $\varepsilon$, the points of the segment within distance $\varepsilon$ of the point form one interval of parameters $t$ (possibly empty). This is the free interval of a cell edge in the [Alt-Godau algorithm](/alt-godau-algorithm/).

## Variants and improvements

- **Ray.** Drop line L6: the minimum over $t \ge 0$ is at $\max(0, t^*)$.
- **Segment to segment.** Two segments in the plane are at distance 0 when they intersect ([segment intersection test](/segment-intersection-detection/)). Otherwise their distance is the minimum of the four distances from an end point of one to the other segment.
- **Point to polyline or polygon boundary.** Take the minimum over all segments, which is $O(m)$ for $m$ segments. Comparing the returned fractions is exact.
- **Points against many segments.** For many queries, use a [Voronoi diagram](/voronoi-diagram/) of the segments or a spatial index such as a [kd-tree](/kd-tree/) over the segments.

## When to use it

Use it for every bounded object: polylines, polygon edges, collision tests, the error of a [polyline simplification](/polygon-simplification/), and the inner loops of the [Hausdorff](/hausdorff-distance/) and [Fréchet](/frechet-distance/) distances between curves. Use the [point-line distance](/point-to-line-distance/) only when the line is really infinite.

## Pitfalls

- **Using the line formula for a segment.** Returning $c^2/D$ in every case, as in the example with $p = (10, 12)$, underestimates the distance. Lines L4 and L6 must come before line L8.
- **Clamping after a float division.** Computing `t = s / D` in floats and then comparing `t <= 0` is safe in sign but can misplace a point near the end of the segment when $s$ and $D$ are large. Compare $s$ with $0$ and with $D$ as in lines L4 and L6, without dividing.
- **Dividing by zero on a degenerate segment.** Code that computes $D$ and divides before it tests $s$ fails when $a = b$. In the order of the pseudocode, $s > 0$ implies $D > 0$.
- **Comparing roots.** As for all distances, compare the squared values; see [Euclidean distance](/euclidean-distance/).

## Implementations

## History

The clamped projection is a standard construction of analytic geometry and of computer graphics. Schneider and Eberly give it with the case analysis of lines L4 and L6 in their chapter on distances in two dimensions. Alt and Godau use its interval form, the points of a segment near a point, as the building block of the free space diagram for the [Fréchet distance](/frechet-distance/).

## References
