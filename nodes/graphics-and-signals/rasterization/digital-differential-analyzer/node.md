---
tag: QJ39WT
kind: algorithm
slug: digital-differential-analyzer
name: Digital differential analyzer (DDA) line algorithm
aliases:
- DDA line algorithm
area: graphics-and-signals/rasterization
level: intro
summary: Draw a line segment by adding a fixed floating-point increment to each coordinate at each step and rounding the result to the nearest pixel.
solves: [line-rasterization]
model: floating-point-model
complexity:
  vars: {n: "the change on the major axis, max(|x1 - x0|, |y1 - y0|)"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, integer_only: false, incremental: true}
prereqs: [line-rasterization, floating-point-model]
see_also: [bresenham-line-algorithm, wu-line-algorithm, amanatides-woo-traversal, ieee-754, machine-epsilon, kahan-summation]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.2, Scan Converting Lines (the basic incremental algorithm, which adds the slope at each step and rounds)
  - book: "William M. Newman and Robert F. Sproull, Principles of Interactive Computer Graphics, McGraw-Hill, 1973"
    locator: the chapter on line drawing (the digital differential analyzer)
  - book: isbn:9781482229394
    title: Steve Marschner and Peter Shirley, Fundamentals of Computer Graphics, fourth edition, CRC Press, 2015
    locator: Chapter 8, Section 8.1, Rasterization (line drawing by incremental evaluation)
  - book: isbn:9780898715217
    title: Nicholas J. Higham, Accuracy and Stability of Numerical Algorithms, second edition, SIAM, 2002
    locator: Chapter 4, Summation (the error bound of recursive summation, which is the drift of the DDA)
---

The digital differential analyzer (DDA) line algorithm draws a line segment by adding a fixed increment to each coordinate at each step and rounding the result to the nearest [pixel](/pixel/). The increment is the change of the segment divided by the number of steps, so one coordinate moves by exactly one pixel per step and the other by the slope. It solves [line rasterization](/line-rasterization/) in time proportional to the number of pixels. In floating point, each addition rounds, the rounding errors add up along the line, and a pixel can differ from the pixel of the exact line.

## In plain words

To walk along a straight line on graph paper, decide how many steps to take: one step for each square along the longer direction. Work out how far the line moves in each direction during one step. Then start at the first point, and at each step add these two amounts to your position and fill the square that contains your position.

This is easy to write and easy to change, for example to also blend a color along the line. Its weak point is the adding. A computer stores the step amounts with a tiny rounding error, and each addition rounds again. Over a long line the small errors add up, and the position can end up on the wrong side of a square boundary.

## The problem

The input is two pixels $(x_0, y_0)$ and $(x_1, y_1)$ with integer coordinates. A pixel is a point sample at its center, and this page puts the center of pixel $(i, j)$ at $(i, j)$; with centers at $(i + \tfrac12, j + \tfrac12)$, as in Direct3D and OpenGL, shift the endpoints and nothing else changes. The output has one pixel for each integer value on the major axis (the axis of the larger change), and on the minor axis the integer nearest to the exact segment. The DDA rounds half up: it maps $v$ to $\lfloor v + \tfrac12 \rfloor$. The cost model is the [floating-point model](/floating-point-model/) with [IEEE 754](/ieee-754/) binary64 or binary32 numbers and round to nearest.

## The algorithm

The values $x$, $y$, $\Delta x$ and $\Delta y$ are floating-point numbers, and $\mathrm{fl}$ marks a rounded operation.

```pseudo id=main
DDA-LINE(x0, y0, x1, y1)                    ▷ integer endpoints
L1  n ← max(|x1 − x0|, |y1 − y0|)
L2  if n = 0 then PLOT(x0, y0) and return
L3  Δx ← fl((x1 − x0) / n), Δy ← fl((y1 − y0) / n)
L4  x ← x0, y ← y0
L5  for i ← 0 to n do
L6      PLOT(⌊fl(x + 1/2)⌋, ⌊fl(y + 1/2)⌋)
L7      x ← fl(x + Δx), y ← fl(y + Δy)
```

Line L1 takes one step for each pixel of the major axis. Line L3 makes the increments: one of them is $\pm 1$, and the other is the slope, with $|\Delta| \le 1$. So the major coordinate moves by exactly one pixel per step, and the minor coordinate by at most one pixel, and the pixels are 8-connected. Line L6 rounds half up. In exact arithmetic, step $i$ is at the point $(x_0, y_0) + \tfrac{i}{n}(x_1 - x_0, y_1 - y_0)$ of the segment, and the pixel is that point rounded. In floating point, line L3 rounds the slope, and each addition of line L7 rounds again. The error of $y$ after $i$ steps is the error of a recursive sum of $i$ terms, so it grows with $i$.

The name comes from the digital differential analyzer, a kind of computer that solved differential equations by the repeated addition of small increments. The line DDA integrates $dy/dx = \Delta y / \Delta x$ in the same way.

## Example

Draw the segment from $(0, 0)$ to $(8, 3)$. Then $n = 8$, $\Delta x = 1$ and $\Delta y = 0.375$. The value $0.375 = 3/8$ is exact in binary, so here no addition rounds.

| step $i$ | $x$ | $y$ | $y + \tfrac12$ | pixel |
|---|---|---|---|---|
| 0 | 0 | 0 | 0.5 | (0, 0) |
| 1 | 1 | 0.375 | 0.875 | (1, 0) |
| 2 | 2 | 0.75 | 1.25 | (2, 1) |
| 3 | 3 | 1.125 | 1.625 | (3, 1) |
| 4 | 4 | 1.5 | 2 | (4, 2) |
| 5 | 5 | 1.875 | 2.375 | (5, 2) |
| 6 | 6 | 2.25 | 2.75 | (6, 2) |
| 7 | 7 | 2.625 | 3.125 | (7, 3) |
| 8 | 8 | 3 | 3.5 | (8, 3) |

At step 4 the line is at $1.5$, half way between two rows, and the DDA rounds up to row 2. [Bresenham's algorithm](/bresenham-line-algorithm/) gives the tie to row 1. All other pixels are the same.

Two cases show the rounding error.

- **A tie that falls the other way.** For $(0, 0)$ to $(14, 1)$, $\Delta y = \mathrm{fl}(1/14)$, and seven additions in binary64 give $0.4999999999999999$, not $0.5$. So step 7 plots $(7, 0)$, but rounding the exact value $\tfrac12$ half up gives $(7, 1)$.
- **Drift off a tie.** For $(0, 0)$ to $(353, 337)$ in binary32, $\Delta y = 0.954674243927002$, while the exact slope is $0.95467422\ldots$. After 342 additions, $y = 326.5$, but the exact height is $337 \cdot 342/353 \approx 326.4986$. So binary32 plots $(342, 327)$, and the exact line rounds to $(342, 326)$. Binary64 gives $(342, 326)$.

## Correctness

In exact arithmetic, step $i$ plots the point of the segment at the fraction $i/n$ of its length, rounded half up. The first pixel is $(x_0, y_0)$, the last is $(x_1, y_1)$, and consecutive pixels differ by at most one in each coordinate. In floating point, the major coordinate stays exact, because it is a sum of integers. For the minor coordinate, let $u$ be the unit roundoff and $M$ the largest absolute value of an endpoint coordinate. Then the error after $i$ steps is at most $i\,u\,(M + \tfrac52)$. The exact value of $y + \tfrac12$ is a fraction with denominator $2n$, so off a tie it is at least $\tfrac1{2n}$ from each integer. So if

$$2n(n + 1)\,u\,\left(M + \tfrac52\right) < 1,$$

the floating-point DDA plots the same pixel as the exact line at each step that is not a tie, and one of the two nearest pixels at a tie. For binary64 this holds for lines with $n \le 2^{16}$ and coordinates up to $2^{16}$. For binary32 it holds only up to about 200. The proofs are in [the correctness proof](proofs/correctness.md).

## Complexity

The loop of line L5 runs $n + 1$ times for $n + 1$ pixels, and each pass does two additions, two additions of $\tfrac12$, two floors and one PLOT. So the time is $\Theta(n)$ in each case, and the extra space is $\Theta(1)$. Line L3 has two divisions, done one time. Each algorithm must write the $n + 1$ pixels, so the DDA is optimal up to a constant factor. On old hardware, the conversion from float to integer in line L6 was the slow part, which is one reason for the integer methods.

## Properties

- **Not exact.** The pixels depend on the float format and on the order of the operations. Binary32 and binary64 can give different pixels on the same segment.
- **Ties are not predictable.** At a tie the rounded sum can fall on either side, so the tie rule of the exact algorithm (round half up) is not kept.
- **Not reversible.** A segment and its reverse can differ at ties, and with drift they can differ elsewhere too.
- **8-connected.** The major coordinate is exact and the minor coordinate moves by at most one pixel per step.
- **Easy to extend.** Any value that changes linearly along the line (a color, a depth, a texture coordinate) gets its own increment and its own addition in line L7.

## Variants and improvements

- **Recompute instead of add.** Compute $c_0 + i\,(c_1 - c_0)/n$ at each step, or the exact integer $\lfloor (2 c_0 n + 2 i (c_1 - c_0) + n) / (2n) \rfloor$. The error then does not grow with $i$, at the cost of a multiplication (and a division) per step.
- **Fixed-point DDA.** Keep $y$ as an integer in units of $2^{-f}$ (for example a 16.16 format). Each addition is then exact, but the increment is rounded one time, so the drift after $i$ steps is at most $i \cdot 2^{-f-1}$. Choose $f$ with $n \cdot 2^{-f-1}$ below the gap $\tfrac1{2n}$, that is $2^{f} > n^2$, to get the exact pixels off the ties.
- **The integer form.** Keep the fractional part of $y$ as an exact integer numerator over $2n$ and test it against the half. This is [Bresenham's algorithm](/bresenham-line-algorithm/), which has no error at all.
- **Two pixels per step.** Use the fractional part of $y$ as an intensity, and plot the two nearest pixels: this is [Wu's line algorithm](/wu-line-algorithm/).
- **Grid traversal.** The [Amanatides and Woo traversal](/amanatides-woo-traversal/) is often also called a DDA. It steps through each cell of a grid that a ray crosses, with one step on one axis at a time, so it gives a 4-connected set of cells, not one pixel per column. It is a different algorithm for a different output.

## When to use it

Use the DDA when the line is short, binary64 is available, and the exact pixels at ties do not matter, or when the same loop must also interpolate colors or depths. Use [Bresenham's algorithm](/bresenham-line-algorithm/) when the pixels must be exact and the same on each machine, when only integers are available, or when the line is long. Use [Wu's algorithm](/wu-line-algorithm/) for smooth lines.

## Pitfalls

- **Python round in line L6.** `round` in Python rounds half to even, so `round(0.5)` is 0 and `round(2.5)` is 2. Line L6 must use `floor(v + 0.5)`.
- **Truncation in line L6.** `int(v + 0.5)` in C or Python truncates toward zero, so for $v = -0.7$ it gives 0, not $-1$. Use `floor`.
- **Integer division in line L3.** In C, `(x1 - x0) / n` with integer operands gives 0 for a shallow line. Convert to floating point before the division.
- **Zero length.** Without line L2, a segment with equal endpoints divides by zero in line L3.
- **Binary32 on long lines.** A float32 DDA can move pixels off the ties after a few hundred steps. Use binary64, recompute from $i$, or use the integer form.

## Implementations

## History

The name comes from the digital differential analyzer, a computer that solved differential equations by adding small increments at each step. Line drawing by adding the slope at each step appears in the early graphics textbooks, for example Newman and Sproull in 1973. Foley, van Dam, Feiner and Hughes give it as the basic incremental algorithm, before the integer midpoint algorithm.

## References
