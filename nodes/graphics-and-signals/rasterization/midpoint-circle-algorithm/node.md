---
tag: MR2G6P
kind: algorithm
slug: midpoint-circle-algorithm
name: Midpoint circle algorithm
aliases:
- Bresenham circle algorithm
area: graphics-and-signals/rasterization
level: intro
summary: Draw a circle of integer radius by computing one octant with an integer decision variable at midpoints and mirroring it eight ways.
solves: [circle-rasterization]
model: word-ram
complexity:
  vars: {r: the radius in pixels}
  time: {worst: Θ(r), best: Θ(r)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, integer_only: true, incremental: true}
history:
  year: 1977
  people: [Jack E. Bresenham, M. L. V. Pitteway]
  note: Pitteway gave a midpoint method for ellipses and hyperbolas on plotters in 1967, and Bresenham an integer circle algorithm in 1977.
prereqs: [circle-rasterization, bresenham-line-algorithm]
see_also: [midpoint-ellipse-algorithm, ellipse-rasterization, wu-line-algorithm, integer-square-root, pixel]
sources:
  - paper: doi:10.1145/359423.359432
    title: Jack E. Bresenham, A linear algorithm for incremental digital display of circular arcs, Communications of the ACM 20(2), 100 to 106 (1977)
    locator: the whole paper (an algorithm with sign tests and additions only, which picks the step pattern closest to the circle)
  - paper: "M. L. V. Pitteway, Algorithm for drawing ellipses or hyperbolae with a digital plotter, The Computer Journal 10(3), 282 to 289 (1967)"
    locator: the decision by the sign of the conic equation at the point between the two candidate moves
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.3, Scan Converting Circles (eight-way symmetry and the midpoint circle algorithm with integer arithmetic)
---

The midpoint circle algorithm draws a circle of integer radius $r$ about an integer center. It computes the pixels of one octant, one column at a time, with an integer decision variable that tells on which side of the circle the midpoint between the two candidate pixels lies, and it mirrors each pixel to the other seven octants. It solves [circle rasterization](/circle-rasterization/) with only integer additions and sign tests, in $\Theta(r)$ time, and each pixel is the one nearest to the circle in its column. It is the circle form of [Bresenham's line algorithm](/bresenham-line-algorithm/), and the [midpoint ellipse algorithm](/midpoint-ellipse-algorithm/) extends it.

## In plain words

A circle looks the same if you flip it left to right, top to bottom, or across a diagonal. So you only need to draw one eighth of it, the part from the top going right until the curve reaches the diagonal, and copy each square you fill to seven other places.

In that eighth, the curve falls slowly, never more than one row per column. So in each new column there are two choices: stay on the same row, or go down one row. Look at the point half way between the two candidate squares. If that point is inside the circle, the curve passes above it, and you stay. If it is outside, you go down. A whole number tracks how far that half-way point is inside or outside, and it changes by a simple amount at each column.

## The problem

The input is an integer center $(x_c, y_c)$ and an integer radius $r \ge 0$. A pixel is a point sample at its center, here at the integer point $(i, j)$; with centers at $(i + \tfrac12, j + \tfrac12)$, as in Direct3D and OpenGL, give the center in those units and nothing else changes. Let $F(x, y) = x^2 + y^2 - r^2$, which is negative inside the circle and positive outside. On the arc with $0 \le x \le y$, the slope is between 0 and $-1$, so each column has one pixel. The output for this arc is the pixel $(x, y)$ with $y$ nearest to $(r^2 - x^2)^{1/2}$ for each column $x$ from 0 to the diagonal, and the output for the circle is this arc mapped by the eight symmetries $(x, y) \mapsto (\pm x, \pm y), (\pm y, \pm x)$ and moved by $(x_c, y_c)$. The cost model is the [word RAM](/word-ram/) with integers.

## The algorithm

```pseudo id=main
MIDPOINT-CIRCLE(xc, yc, r)                ▷ integer center and radius, r ≥ 0
L1  x ← 0, y ← r, d ← 1 − r
L2  while x ≤ y do
L3      PLOT-8(xc, yc, x, y)
L4      if d < 0 then d ← d + 2x + 3          ▷ the midpoint is inside: stay on row y
L5      else d ← d + 2(x − y) + 5, y ← y − 1   ▷ the midpoint is outside: go down
L6      x ← x + 1

PLOT-8(xc, yc, x, y)
    PLOT(xc ± x, yc ± y) and PLOT(xc ± y, yc ± x), for all four choices of the signs
```

The pass at column $x$ has plotted $(x, y)$, and it decides the pixel of column $x + 1$: it is $(x + 1, y)$ or $(x + 1, y - 1)$. The midpoint between these two candidates is $(x + 1, y - \tfrac12)$. The decision variable is $d = F(x + 1, y - \tfrac12) - \tfrac14 = (x + 1)^2 + y^2 - y - r^2$, an integer. Since $F$ at the midpoint is an integer plus $\tfrac14$, it is never zero, and $d < 0$ exactly when the midpoint is inside. Line L1 is the value at $x = 0$, $y = r$: $1 + r^2 - r - r^2 = 1 - r$. When $x$ grows by one, $(x + 1)^2$ grows by $2x + 3$ (line L4). When $y$ also drops by one, $y^2 - y$ drops by $2y - 2$, which gives line L5. The loop stops after the diagonal $x = y$.

## Example

Draw the circle of radius $r = 10$ about the origin. The value $d$ in pass $x$ decides the pixel of column $x + 1$, by the sign of $F$ at the midpoint $(x + 1, y - \tfrac12)$.

| pass $x$ | pixel plotted | $d$ at line L4 | exact height in column $x + 1$ | decision |
|---|---|---|---|---|
| 0 | (0, 10) | −9 | 9.9499 | stay |
| 1 | (1, 10) | −6 | 9.7980 | stay |
| 2 | (2, 10) | −1 | 9.5394 | stay |
| 3 | (3, 10) | 6 | 9.1652 | down |
| 4 | (4, 9) | −3 | 8.6603 | stay |
| 5 | (5, 9) | 8 | 8.0000 | down |
| 6 | (6, 8) | 5 | 7.1414 | down |
| 7 | (7, 7) | 6 | 6.0000 | down, then $x = 8 > y = 6$ and stop |

The octant has 8 pixels. In pass 2, $d = -1$: the midpoint $(3, 9.5)$ has $F = -\tfrac34$, and the exact height $9.5394$ is just above it. The eight copies give $8 \times 8 = 64$ plots. The pixels $(0, \pm 10)$ and $(\pm 10, 0)$ come from two octants each, and so do the four images of $(7, 7)$, so the circle has $64 - 4 - 4 = 56$ different pixels.

## Correctness

The [loop invariant](/loop-invariant/) at line L2 has two parts: $d = (x + 1)^2 + y^2 - y - r^2$, and if $x \le y$ then $|y - (r^2 - x^2)^{1/2}| < \tfrac12$. The first part follows from the updates of lines L4 and L5. For the second part, the sign of $d$ tells whether the exact height in column $x + 1$ is above or below $y - \tfrac12$. In this octant the circle falls by at most one row per column, and a short argument with $Y(x)^2 - Y(x + 1)^2 = 2x + 1$ shows that the exact height is never below $y - \tfrac32$ while the loop goes on. So the chosen row is the nearest. A tie would need $(2y + 1)^2 = 4(r^2 - x^2)$, an odd number equal to an even number, so ties never occur for an integer radius. The last pixel of the octant has $y - x \in \{0, 1\}$, so the eight copies meet. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The value $y - x$ starts at $r$ and drops by at least one per pass, so the loop of line L2 runs at most $r + 1$ times. In fact the octant ends near $x = r/\sqrt2$, so it has about $r/\sqrt2 + 1$ pixels. Each pass does a constant number of additions, one sign test and eight PLOT operations. So the time is $\Theta(r)$ in each case, and the extra space is $\Theta(1)$. The circle has about $8 r/\sqrt2 = 4\sqrt2\, r \approx 5.66 r$ pixels: 564 for $r = 100$ and 5656 for $r = 1000$. Each algorithm must write these pixels, so the bound is optimal up to a constant factor.

The decision variable satisfies $-2r < d < 2r + 2$ at each test, and $|d| \le 4r + 5$ after the last update. So $d$ needs only about $\log_2 r + 4$ bits, and the algorithm never computes $r^2$ or another square: it is exact for each radius that fits in the integers.

## Properties

- **Exact.** Integers only, no rounding, the same pixels on each machine.
- **Nearest pixel in each column of the octant.** By the proof, and with no ties for an integer radius.
- **The same pixels as the smallest residual.** Of the two candidates $y$ and $y - 1$, the algorithm also picks the one with the smaller residual $|x^2 + y^2 - r^2|$. Indeed $F(x, y) + F(x, y - 1) = 2F(x, y - \tfrac12) + \tfrac12 = 2d + 1$ is odd, so it is never zero, and its sign gives both the midpoint test and the comparison of the two residuals.
- **8-connected and symmetric.** Consecutive pixels of the octant differ by one column and at most one row, and the output is the same under the eight symmetries of the square grid.
- **Pixels on the axes and diagonals plotted twice.** PLOT-8 plots the pixels with $x = 0$ or $x = y$ two times.

## Variants and improvements

- **Second-order differences.** The increments $2x + 3$ and $2(x - y) + 5$ are themselves updated by constant amounts, so a version with two more variables uses only additions of constants.
- **Half-integer centers or radii.** For a center at a pixel corner or a radius $r + \tfrac12$, scale all coordinates by 2. The decision variable stays an integer, but ties can then occur, and a tie rule is needed.
- **Filled disks.** Draw the horizontal span from $(x_c - x, y_c + y)$ to $(x_c + x, y_c + y)$ for each octant pixel and its mirror images. Each row must be drawn one time only.
- **Arcs.** Clip the octant runs to the angles of the arc. Bresenham's 1977 paper treats circular arcs.
- **Ellipses.** The [midpoint ellipse algorithm](/midpoint-ellipse-algorithm/) has no eight-way symmetry, only four-way, and splits each quadrant at slope $-1$.
- **Antialiased circles.** Wu's 1991 paper also gives a circle generator with two pixels per column; see [Wu's line algorithm](/wu-line-algorithm/).

## When to use it

Use the midpoint circle algorithm to draw aliased circles in software or in a plotter, when the center and the radius are integers and the pixels must be exact. A parametric method that computes $(r\cos\theta, r\sin\theta)$ needs floating point, trigonometric functions and a choice of step, and it can leave gaps or plot a pixel twice. A method that computes $(r^2 - x^2)^{1/2}$ for each column needs an [integer square root](/integer-square-root/) per pixel, and it gives the same pixels at a higher cost. Use an antialiased method for smooth circles, and a span fill for disks.

## Pitfalls

- **Testing $d \le 0$ in line L4.** For an integer radius this gives the same pixels, because the midpoint value is never zero. With a scaled or half-integer radius, ties occur, and the two tests then give different circles.
- **The diagonal with the wrong loop test.** Writing `while x < y` in line L2 drops the pixel on the diagonal when $x = y$, for example $(7, 7)$ for $r = 10$, and leaves four gaps in the circle.
- **Plotting the octant boundaries two times.** With XOR drawing or [alpha blending](/alpha-blending/), the pixels on the axes and the diagonals of line L3 change twice. Plot $x = 0$ and $x = y$ with four copies, not eight.
- **The radius as a float.** A radius such as 10.5 makes $d$ in line L1 a fraction, and the test of line L4 then has rounding problems. Scale by 2 or round the radius first.

## Implementations

## History

M. L. V. Pitteway published in 1967 an algorithm that draws ellipses and hyperbolas with a digital plotter. It chooses each step by the sign of the conic equation at the point between the two candidate moves, the idea of line L4. In 1977 Jack E. Bresenham published an integer algorithm for circular arcs that uses only sign tests, additions and subtractions, and picks the step pattern closest to the true circle. Textbooks such as Foley, van Dam, Feiner and Hughes present the circle in the midpoint form of this page.

## References
