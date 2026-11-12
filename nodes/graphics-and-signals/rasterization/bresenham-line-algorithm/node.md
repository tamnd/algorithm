---
tag: VSRX7E
kind: algorithm
slug: bresenham-line-algorithm
name: Bresenham's line algorithm
aliases:
- midpoint line algorithm
- Bresenham line drawing
area: graphics-and-signals/rasterization
level: intro
summary: Draw a line segment between two integer pixels. Step along the major axis and choose the nearest pixel on the minor axis with integer additions and a sign test.
solves: [line-rasterization]
model: word-ram
complexity:
  vars: {n: "the number of pixels drawn, max(|x1 - x0|, |y1 - y0|) + 1"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, integer_only: true, incremental: true, reversible: false}
history:
  year: 1965
  people: [Jack E. Bresenham]
  note: Bresenham published the algorithm in 1965 in the IBM Systems Journal, for the control of an incremental digital plotter.
prereqs: [line-rasterization, loop-invariant]
see_also: [digital-differential-analyzer, wu-line-algorithm, midpoint-circle-algorithm, line-clipping, amanatides-woo-traversal, pixel]
sources:
  - paper: doi:10.1147/sj.41.0025
    title: Jack E. Bresenham, Algorithm for computer control of a digital plotter, IBM Systems Journal 4(1), 25 to 30 (1965)
    locator: the whole paper (the integer error term and the choice between the two plotter moves at each step)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.2, Scan Converting Lines (the basic incremental algorithm and the midpoint line algorithm)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2015
    locator: Chapter 8, Section 8.1, Rasterization (line drawing with the implicit line equation and the midpoint test)
  - paper: "Jack E. Bresenham, Ambiguities in incremental line rastering, IEEE Computer Graphics and Applications 7(5), 31 to 43 (1987)"
    locator: the cases where the error term is zero, the reversal of a line, and the effect of clipping and of fractional endpoints
  - paper: doi:10.1145/357311.357312
    title: Robert F. Sproull, Using program transformations to derive line-drawing algorithms, ACM Transactions on Graphics 1(4), 259 to 273 (1982)
    locator: the derivation of Bresenham's algorithm from the algorithm that rounds the exact line
---

Bresenham's line algorithm draws a line segment between two integer [pixels](/pixel/) on a raster grid. It takes one step at a time along the axis of the larger change, and on the other axis it picks the pixel nearest to the exact line, with only integer additions and the sign test of an error term. It solves [line rasterization](/line-rasterization/) in time proportional to the number of pixels, and its output has no rounding error. It is the base of most software line drawing, and its idea extends to the [midpoint circle algorithm](/midpoint-circle-algorithm/).

## In plain words

Draw a line on graph paper from one square to another square, where the line goes more across than up. Go one column at a time from left to right. In each column you must fill one square, and the only choice is to stay on the same row or to go up one row. Fill the square whose center is nearer to the true line.

To make this choice without fractions, keep one whole number that tells how far the true line is above or below the point half way between the two candidate squares. Each column adds a fixed amount to this number. When it becomes positive, go up one row and subtract a second fixed amount. The method uses only adding, subtracting and the test "is it positive", so it is fast and always gives the same answer on every machine.

## The problem

The input is two pixels $(x_0, y_0)$ and $(x_1, y_1)$ with integer coordinates. A pixel is a point sample at its center, not a little square, and this page puts the center of pixel $(i, j)$ at the integer point $(i, j)$. With the Direct3D and OpenGL convention, where the center is at $(i + \tfrac12, j + \tfrac12)$, shift the endpoints by $\tfrac12$ and nothing else changes. Let $d_x = |x_1 - x_0|$ and $d_y = |y_1 - y_0|$. The axis with the larger change is the *major axis*, and the other one is the *minor axis*. The output is the sequence of pixels with one pixel for each integer value on the major axis from the start to the end, and on the minor axis the integer nearest to the exact segment at that value. When the segment passes exactly half way between two pixels, a tie rule decides. This algorithm gives the tie to the pixel nearer to the start. The cost model is the [word RAM](/word-ram/) with integers.

## The algorithm

Let $m$ be the change on the major axis and $n$ the change on the minor axis, so $0 \le n \le m$. The error term $e$ is an integer.

```pseudo id=main
BRESENHAM-LINE(x0, y0, x1, y1)              ▷ integer endpoints
L1  dx ← |x1 − x0|, dy ← |y1 − y0|
L2  sx ← (1 if x1 ≥ x0 else −1), sy ← (1 if y1 ≥ y0 else −1)
L3  if dx ≥ dy then (m, n) ← (dx, dy) else (m, n) ← (dy, dx)
L4  e ← 2n − m, x ← x0, y ← y0
L5  for i ← 0 to m do
L6      PLOT(x, y)
L7      if e > 0 then                        ▷ the line passes beyond the midpoint
L8          step the minor axis: y ← y + sy if dx ≥ dy, else x ← x + sx
L9          e ← e − 2m
L10     e ← e + 2n
L11     step the major axis: x ← x + sx if dx ≥ dy, else y ← y + sy
```

Take the first octant, where $x_1 \ge x_0$, $y_1 \ge y_0$ and $d_y \le d_x$. After $i$ steps, the pixel is $(x_0 + i, y_0 + k)$, and the next column $x_0 + i + 1$ has two candidates, $y_0 + k$ and $y_0 + k + 1$. The midpoint between them is at height $y_0 + k + \tfrac12$. The implicit line function $F(x, y) = 2\big(d_y (x - x_0) - d_x (y - y_0)\big)$ is zero on the line, positive below it and negative above it. At the midpoint it is

$$e = F\big(x_0 + i + 1,\ y_0 + k + \tfrac12\big) = 2 d_y (i + 1) - d_x (2k + 1).$$

This is the error term of line L7. If $e > 0$, the midpoint is below the line, so the upper pixel is nearer, and line L8 steps up. Each step of $x$ adds $2 d_y$ to $F$ (line L10), and each step of $y$ subtracts $2 d_x$ (line L9). The factor 2 removes the $\tfrac12$ of the midpoint, so all values are integers. Line L4 is the value for $i = 0$, $k = 0$. When $e = 0$, the line passes through the midpoint, and the algorithm does not step: this is the tie rule. This view of $e$ as the line function at a midpoint is the *midpoint line algorithm* of the textbooks; it makes the same decisions as Bresenham's error term. The other seven octants use the same steps with the signs $s_x$, $s_y$, and with the axes exchanged when $d_y > d_x$.

## Example

Draw the segment from $(0, 0)$ to $(8, 3)$. So $m = 8$, $n = 3$, $2n = 6$, $2m = 16$, and $e$ starts at $6 - 8 = -2$. The exact height is $y = 3x/8$. The value of $e$ in pass $i$ decides the pixel of column $i + 1$.

| pass $i$ | pixel plotted | $e$ at line L7 | exact $y$ in column $i + 1$ | decision |
|---|---|---|---|---|
| 0 | (0, 0) | −2 | 0.375 | stay |
| 1 | (1, 0) | 4 | 0.75 | step up |
| 2 | (2, 1) | −6 | 1.125 | stay |
| 3 | (3, 1) | 0 | 1.5 | tie: stay |
| 4 | (4, 1) | 6 | 1.875 | step up |
| 5 | (5, 2) | −4 | 2.25 | stay |
| 6 | (6, 2) | 2 | 2.625 | step up |
| 7 | (7, 3) | −8 | 3 | stay |
| 8 | (8, 3) | −2 | | end |

The pixels are $(0,0), (1,0), (2,1), (3,1), (4,1), (5,2), (6,2), (7,3), (8,3)$. In column 4 the exact line is at $1.5$, half way between rows 1 and 2, and $e = 0$ gives the tie to row 1, the row nearer to the start.

## Correctness

In the first octant, let $k_i$ be the row offset of pass $i$. The [loop invariant](/loop-invariant/) at line L6 is

$$k_i = \left\lceil \frac{i\,n}{m} - \frac12 \right\rceil, \qquad e = 2n(i + 1) - m(2k_i + 1).$$

The integer $\lceil v - \tfrac12 \rceil$ is the integer nearest to $v$, with a tie to the lower one, so pass $i$ plots the nearest pixel to the exact height $y_0 + i n / m$. The invariant holds after line L4. Because the slope $n/m$ is at most 1, the exact height grows by at most 1 per column, so the next row is $k_i$ or $k_i + 1$, and the sign of $e$ tells which one. The last pass plots $(x_1, y_1)$. The full proof, with the bound $-2m < e \le 2m$, is in [the correctness proof](proofs/correctness.md).

## Complexity

The loop of line L5 runs $m + 1$ times, and each pass does a constant number of additions, one comparison and one PLOT. So the time is $\Theta(n)$ for $n = m + 1$ pixels, in the best and in the worst case. Each algorithm for this problem writes $n$ pixels, so no algorithm is faster by more than a constant factor. The extra space is $\Theta(1)$: the six integers $m$, $n$, $e$, $x$, $y$ and $i$.

The error term stays in $-2m < e \le 2m$. So with $w$-bit signed integers the algorithm is exact for each line with $2m < 2^{w-1}$, for example $m < 2^{14} = 16384$ with 16-bit integers. The coordinates need the same range. No multiplication is necessary: $2n$ and $2m$ are shifts, computed one time.

## Properties

- **Exact.** All values are integers, so there is no rounding error, and each machine gives the same pixels. A floating-point [DDA](/digital-differential-analyzer/) does not have this property.
- **Nearest pixel.** In each step of the major axis, the pixel is the one nearest to the line. In a fixed column, the distance to the line is the vertical distance times a constant, so the pixel is also nearest in Euclidean distance.
- **8-connected.** Consecutive pixels differ by one step on the major axis and by zero or one step on the minor axis.
- **Runs.** In the first octant with $n \ge 1$, the pixels of row $y_0 + k$ are the columns $i$ with $k - \tfrac12 < i n/m \le k + \tfrac12$, an interval of length $m/n$. So each run that is not the first or the last has $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ pixels, and no run has more than $\lceil m/n \rceil$.
- **Not reversible.** The tie rule depends on the direction. The segment from $(0, 0)$ to $(4, 1)$ gives $(0,0), (1,0), (2,0), (3,1), (4,1)$, but from $(4, 1)$ to $(0, 0)$ it gives $(4,1), (3,1), (2,1), (1,0), (0,0)$. They differ at $x = 2$.
- **Brightness depends on the slope.** A line gets $m + 1$ pixels for a length of $(m^2 + n^2)^{1/2}$, so a diagonal line has about $1/\sqrt2$ of the pixels per unit length of a horizontal line, and looks thinner.

## Variants and improvements

- **Tie toward the end.** Write $e \ge 0$ in line L7. This rounds ties up in the first octant. Both rules give the nearest pixel; they differ only at ties.
- **Reversible lines.** Always draw from the endpoint with the smaller $x$ (or a fixed tie rule that depends on the octant, not on the direction), so that a line and its reverse give the same pixels. Bresenham's 1987 paper studies these choices.
- **Clipped lines.** To start at a column $x_c$ inside the segment, compute $k$ and $e$ from the invariant with one division, then run the loop. The clipped line then has the same pixels as the full line. Clipping the segment in real numbers and rounding the new endpoints can move the pixels. See [line clipping](/line-clipping/).
- **Subpixel endpoints.** With endpoints on a grid of $2^s$ subpixel steps per pixel, multiply the line function by $2^s$. The error term then starts at a value that depends on the fractional parts of the endpoints, and it stays an integer.
- **Multi-step and run-slice versions.** Decide two pixels per test, or use the run property to draw a whole run of $\lfloor m/n \rfloor$ or $\lceil m/n \rceil$ pixels per test.
- **Antialiased lines.** [Wu's line algorithm](/wu-line-algorithm/) draws two pixels per column with intensities from the same kind of integer error term.
- **All cells that the segment crosses.** A 4-connected walk that visits each grid cell the segment meets is a different output. The [Amanatides and Woo traversal](/amanatides-woo-traversal/) computes it for rays in a voxel grid.

## When to use it

Use Bresenham's algorithm to draw aliased lines in software when the endpoints are integers or fixed-point values, and the result must be exact and the same on all machines, for example in a plotter, a CNC controller, a pixel editor, a line-of-sight test on a tile map, or a test reference for a renderer. The floating-point [DDA](/digital-differential-analyzer/) is shorter to write, but it can round differently on different machines and it drifts on long lines. Use [Wu's algorithm](/wu-line-algorithm/) or [supersampling](/supersampling-antialiasing/) when the line must look smooth. On a GPU, the hardware draws lines with its own rules (the diamond-exit rule of OpenGL and Direct3D), which can differ from Bresenham's pixels at ties.

## Pitfalls

- **No swap for steep lines.** Without the test of line L3, a line with $d_y > d_x$ gets one pixel per column and has gaps. Line L3 must make the axis with the larger change the major axis.
- **A changed tie rule.** Writing $e \ge 0$ in line L7, when a test or another program expects $e > 0$, changes the pixels at each tie. Choose one rule and use it everywhere.
- **Erasing by drawing the reverse.** Drawing from $(x_1, y_1)$ to $(x_0, y_0)$ to erase a line drawn the other way leaves pixels at the ties. Sort the endpoints first.
- **The shared vertex of a polyline.** Drawing each segment of a polyline with both endpoints plots each inner vertex two times, which is wrong with XOR drawing or with [alpha blending](/alpha-blending/). Use `for i ← 0 to m − 1` in line L5 for each segment, and plot the last vertex one time.
- **Overflow.** The error term needs $2m < 2^{w-1}$ in line L4 and line L9. With 16-bit integers, a line longer than 16383 pixels overflows; use a wider type or clip first.

## Implementations

## History

Jack E. Bresenham worked at IBM, and he published the algorithm in 1965 in the IBM Systems Journal, as a method to control a digital plotter whose pen moves in one of eight directions per step. The paper decides each move with an integer error term, the term of line L7. Robert Sproull showed in 1982 that the algorithm follows from the simple algorithm that rounds the exact line, by a sequence of program transformations. In 1987 Bresenham wrote about the ambiguities of the method: the ties, the reversal of a line, and the effect of clipping and of fractional endpoints.

## References
