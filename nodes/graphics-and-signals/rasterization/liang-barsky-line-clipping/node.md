---
tag: CW3RQ3
kind: algorithm
slug: liang-barsky-line-clipping
name: Liang-Barsky line clipping
area: graphics-and-signals/rasterization
level: core
summary: Clip a segment P + t(Q - P) to a rectangle by four inequalities in t. The inside part is the interval from the last entry to the first exit.
solves: [line-clipping]
model: real-ram
complexity:
  vars: {n: the number of segments}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1984
  people: [You-Dong Liang, Brian A. Barsky]
  note: Liang and Barsky published the method in ACM Transactions on Graphics in 1984. Cyrus and Beck gave the general form for convex windows in 1978.
prereqs: [line-clipping]
see_also: [cohen-sutherland-line-clipping, polygon-window-clipping, linear-programming-problem, half-plane-intersection, sutherland-hodgman, ieee-754]
sources:
  - paper: doi:10.1145/357332.357333
    title: You-Dong Liang and Brian A. Barsky, A new concept and method for line clipping, ACM Transactions on Graphics 3(1), 1 to 22 (1984)
    locator: the parameter form of the four inequalities, the entering and leaving parameters, and the three-dimensional form
  - paper: doi:10.1016/0097-8493(78)90021-3
    title: Mike Cyrus and Jay Beck, Generalized two- and three-dimensional clipping, Computers and Graphics 3(1), 23 to 28 (1978)
    locator: the clipping of a segment against a convex polygon or polyhedron by one inequality for each face normal
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.12, Clipping Lines (the parametric line clipping of Cyrus and Beck, and the form of Liang and Barsky for an upright rectangle)
  - paper: doi:10.1145/37401.37432
    title: Tina M. Nicholl, D. T. Lee and Robin A. Nicholl, An efficient new algorithm for 2-D line clipping, its development and analysis, Computer Graphics 21(4), 253 to 262 (1987)
    locator: the comparison of the operation counts of the Cohen-Sutherland, Liang-Barsky and new methods
---

Liang-Barsky line clipping solves [line clipping](/line-clipping/) against an axis-aligned rectangle in the parameter of the segment. It writes the segment as $P + t\,(Q - P)$ for $t \in [0, 1]$, and each side of the window gives one inequality $t\,a \le b$. The inside part is the interval from the largest entering parameter to the smallest leaving parameter, so the method needs at most four divisions and never computes a point that it throws away. It is the case of a rectangle of the Cyrus-Beck method for convex windows.

## In plain words

Walk along the segment from its start to its end, and keep a clock that goes from 0 to 1. Each side of the window has a moment when you cross its line. At some lines you go from the outside to the inside, and at others you go from the inside to the outside.

You are in the window only after you are inside all four side lines. So the visible part starts at the latest moment that you go in, or at 0. It ends at the earliest moment that you go out, or at 1. If the latest moment in comes after the earliest moment out, you are never inside all four at once, and nothing is visible.

You only compare moments. You compute the two end points once, at the end.

## The problem

The input is a segment from $P$ to $Q$ and a window $W = [x_{\min}, x_{\max}] \times [y_{\min}, y_{\max}]$. The output is $\overline{PQ} \cap W$: nothing, one point or one segment, in the direction from $P$ to $Q$. The window is closed. See [line clipping](/line-clipping/).

The model is the [real RAM](/real-ram/) with exact rational arithmetic; the implementation uses Python integers and fractions, so each comparison of parameters is exact. The window is in continuous coordinates. When the result is drawn, the pixels are point samples at the centers $(i + 1/2, j + 1/2)$, as in the OpenGL and Direct3D 10 rules.

## The algorithm

Let $d_x = x_Q - x_P$ and $d_y = y_Q - y_P$. The point $P + t\,(Q - P)$ is inside the left side when $x_P + t d_x \ge x_{\min}$, which is $t \cdot (-d_x) \le x_P - x_{\min}$. The four sides give four pairs $(a, b)$ in the same way.

```pseudo id=main
LIANG-BARSKY(P, Q, W)                      ▷ W = [xmin, xmax] × [ymin, ymax]
L1  t0 ← 0, t1 ← 1
L2  pairs (a, b) ← (−dx, xP − xmin), (dx, xmax − xP), (−dy, yP − ymin), (dy, ymax − yP)
L3  for each pair (a, b) do                ▷ the side holds when t · a ≤ b
L4      if a = 0 then (if b < 0 then return empty)       ▷ parallel to the side and outside it
L5      else if a < 0 then t0 ← max(t0, b / a)           ▷ the segment enters here
L6      else t1 ← min(t1, b / a)                         ▷ the segment leaves here
L7      if t0 > t1 then return empty
L8  return (t0, t1)
L9  the output is the segment from P + t0 (Q − P) to P + t1 (Q − P)
```

When $a < 0$, the value $t\,a$ falls as $t$ grows, so the segment comes from the outside of that side into its inside, and $b / a$ is the entering parameter. When $a > 0$ it is the leaving parameter. When $a = 0$ the segment is parallel to the side, and $b$ alone says whether it is inside or outside that side. Line L7 can stop the loop early, as soon as the interval is empty.

## Example

Clip the segment from $P = (-3, -1)$ to $Q = (13, 11)$ against $W = [0, 10]^2$, so $d_x = 16$ and $d_y = 12$.

| Side | $a$ | $b$ | $b / a$ | Kind | $[t_0, t_1]$ after it |
|---|---|---|---|---|---|
| left | $-16$ | $-3$ | $3/16$ | enters | $[3/16, 1]$ |
| right | $16$ | $13$ | $13/16$ | leaves | $[3/16, 13/16]$ |
| bottom | $-12$ | $-1$ | $1/12$ | enters | $[3/16, 13/16]$ |
| top | $12$ | $11$ | $11/12$ | leaves | $[3/16, 13/16]$ |

The output is the segment from $P + \frac{3}{16}(16, 12) = (0, 5/4)$ to $P + \frac{13}{16}(16, 12) = (10, 35/4)$. [Cohen-Sutherland line clipping](/cohen-sutherland-line-clipping/) needs four cuts for the same segment, each with one division, and it throws two of the four points away. Here two of the four ratios do not change the interval, and the two points are computed once.

Now clip the segment from $(-2, 8)$ to $(3, 14)$, with $d_x = 5$ and $d_y = 6$. The left side gives $t_0 = 2/5$, the right side $12/5$, which does not change $t_1 = 1$, and the bottom side $-4/3$, which does not change $t_0$. The top side gives $t_1 = 1/3$. Now $t_0 = 2/5 > 1/3 = t_1$, so line L7 rejects the segment: it leaves the top side before it enters the left side.

## Correctness

By the four pairs, a point $P + t\,(Q - P)$ is in $W$ exactly when $t\,a \le b$ for all four pairs. Each pair allows all $t$, no $t$, a half-line $t \ge b/a$, or a half-line $t \le b/a$. The loop keeps the invariant that $[t_0, t_1]$ is the intersection of $[0, 1]$ with the sets of the pairs seen so far. So after the four pairs, $[t_0, t_1]$ is exactly the set of inside parameters, and when it is empty, line L4 or line L7 returns. The full proof is below.

## Complexity

The loop runs four times, with at most four divisions and eight comparisons. Line L9 adds at most four multiplications. So each segment takes $O(1)$ time, $n$ segments take $\Theta(n)$ time, and the extra space is $\Theta(1)$. A program can keep each candidate as the pair $(b, a)$ and compare two candidates by cross multiplication; then only the two final divisions remain.

## Properties

- It computes at most two output points, and only for segments that are not rejected.
- It does not depend on the order of the four sides; any order gives the same interval.
- A segment that is fully inside still costs four ratios. [Cohen-Sutherland line clipping](/cohen-sutherland-line-clipping/) accepts it with two codes and no division.
- With exact arithmetic the result is exact, and $t_0 = t_1$ gives the single point where a segment touches a corner.
- The output keeps the direction from $P$ to $Q$.

## Variants and improvements

- **Cyrus-Beck.** For a convex window with $m$ sides, side $k$ has an inner normal $n_k$ and a point $p_k$. The side holds when $t\,(-n_k \cdot d) \le n_k \cdot (P - p_k)$, which has the same form $t\,a \le b$. The loop then runs $m$ times, so a segment costs $O(m)$ time. Liang-Barsky is the case where the normals are the four axis directions, so each $a$ and $b$ is a single subtraction.
- **Three dimensions.** A box gives six pairs, and the loop is the same. Liang and Barsky also give the form for the view volume in homogeneous coordinates.
- **Polygons.** Liang and Barsky gave a polygon clipping method in 1983, which uses the entering and leaving parameters of each edge and adds the corners of the window where the polygon turns around one. For the problem see [polygon window clipping](/polygon-window-clipping/).
- **Nicholl-Lee-Nicholl.** The method of 1987 finds the region of one end point first and then tests only the sides that the segment can cross. It does fewer operations on average for two dimensions.
- **As a linear program.** The method solves a [linear program](/linear-programming-problem/) in one variable: the minimum and the maximum of $t$ under the constraints of a [half-plane intersection](/half-plane-intersection/).

## When to use it

Use it when many segments cross the window, or when the window is a convex polygon or a box in three dimensions, through the Cyrus-Beck form. It is also the natural form when the segment parameter is needed later, for example to cut a texture coordinate or a color at the same $t$. When most segments are fully inside or fully outside one side, the outcode tests of [Cohen-Sutherland line clipping](/cohen-sutherland-line-clipping/) are cheaper. For the Boolean operations of two polygons, see [polygon clipping](/polygon-clipping/) in geometry.

## Pitfalls

- **Test $a = 0$ first.** In [IEEE 754](/ieee-754/) arithmetic, $b / 0$ is $\pm\infty$, and the signs of the comparisons then often come out right. But $0 / 0$ is NaN when the segment lies on the line of a side, and $\max$ and $\min$ with NaN give results that depend on the order of the arguments. Line L4 handles $a = 0$ before any division.
- **Strict test on line L7.** The test is $t_0 > t_1$. With $t_0 \ge t_1$, a segment that touches the window at one corner, such as the segment from $(-5, 5)$ to $(5, 15)$ at $(0, 10)$, is rejected.
- **Rounded end points.** In floating point, $P + 1 \cdot (Q - P)$ can differ from $Q$, and a computed point can be a little outside the window. Return $P$ or $Q$ itself when $t_0 = 0$ or $t_1 = 1$, and set the coordinate of the side that gave $t_0$ or $t_1$ to the exact boundary value.
- **Signs of the pairs.** Each pair must read as "inside when $t\,a \le b$". If one sign is wrong, the method takes the outside of that side, and the error shows only for segments that cross it.

## Implementations

## History

Mike Cyrus and Jay Beck gave the parameter method for convex polygons and convex polyhedra in 1978. You-Dong Liang and Brian A. Barsky gave the form for an upright rectangle and box in "A new concept and method for line clipping" in ACM Transactions on Graphics in 1984. They had earlier given a polygon clipping method in the Communications of the ACM in 1983. In 1987, Nicholl, Lee and Nicholl compared the operation counts of the Cohen-Sutherland and Liang-Barsky methods and gave a faster method for two dimensions.

## References
