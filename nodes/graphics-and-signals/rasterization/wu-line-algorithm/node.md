---
tag: ZEVX63
kind: algorithm
slug: wu-line-algorithm
name: Wu's line algorithm
aliases:
- Xiaolin Wu line algorithm
- anti-aliased line drawing
area: graphics-and-signals/rasterization
level: advanced
summary: Draw an antialiased line with two pixels per column, whose intensities come from the fractional part of the exact height, kept in an integer accumulator.
solves: [line-rasterization]
model: word-ram
complexity:
  vars: {n: "the change on the major axis, max(|x1 - x0|, |y1 - y0|)"}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: false, integer_only: true, incremental: true, antialiased: true}
history:
  year: 1991
  people: [Xiaolin Wu]
  note: Wu presented the method at SIGGRAPH 1991, with an antialiased circle generator of the same kind.
prereqs: [bresenham-line-algorithm, antialiasing]
see_also: [digital-differential-analyzer, supersampling-antialiasing, reconstruction-filter, alpha-blending, gamma-correction, pixel]
sources:
  - paper: doi:10.1145/122718.122734
    title: Xiaolin Wu, An efficient antialiasing technique, Computer Graphics (Proceedings of SIGGRAPH 91) 25(4), 143 to 152 (1991)
    locator: the antialiased line generator and its integer error accumulator
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, the section on antialiasing (unweighted and weighted area sampling of a line of width one pixel)
  - book: isbn:9781576101742
    title: Michael Abrash, Michael Abrash's Graphics Programming Black Book, Coriolis Group Books, 1997
    locator: the chapter on Wu antialiasing (an implementation with a 16-bit error accumulator)
---

Wu's line algorithm draws an antialiased line segment with two [pixels](/pixel/) in each column, whose intensities add up to one and come from the fractional part of the exact height of the line. It keeps this fractional part in an integer accumulator, and the carry out of the accumulator tells when to move up one row, as the error term does in [Bresenham's algorithm](/bresenham-line-algorithm/). Xiaolin Wu published it in 1991 as a fast way to [antialias](/antialiasing/) lines. Its weights are a tent filter of width two pixels across the line in each column.

## In plain words

An ordinary line drawing fills one square per column, and a shallow line then looks like a staircase. Wu's method fills two squares per column, the one just below the true line and the one just above it, and shares one unit of ink between them. If the true line passes near the lower square, the lower square gets most of the ink. If it passes in the middle, each gets half.

The share depends on how far the line is above the lower square. The method keeps this distance as a whole number that grows by a fixed amount at each column. When the number passes its maximum, it wraps around and the pair of squares moves up one row. So the method has the speed of an ordinary integer line drawing, and the line looks smooth.

## The problem

The input is two pixels $(x_0, y_0)$ and $(x_1, y_1)$ with integer coordinates, and the output is a set of pixels with intensities in $[0, 1]$. A pixel is a point sample at its center, here at the integer point $(i, j)$; with centers at $(i + \tfrac12, j + \tfrac12)$, shift the endpoints. In column $x$, let $Y$ be the exact height of the segment. The target intensity of pixel $(x, j)$ is the tent weight $\max(0, 1 - |j - Y|)$: a linear [reconstruction filter](/reconstruction-filter/) of width two pixels, in the column direction. The intensities are linear light, not [sRGB](/gamma-correction/) values, and the program that draws the line blends the color $c$ over the old value $b$ as $b + a(c - b)$ for an intensity $a$. The cost model is the [word RAM](/word-ram/).

## The algorithm

The main program handles the first octant, $x_0 < x_1$ and $0 \le y_1 - y_0 \le x_1 - x_0$. The other octants follow by the exchange of the axes and changes of sign, as for Bresenham's algorithm. The accumulator $D$ is a $w$-bit unsigned integer, and $D / 2^w$ is the fractional part of the height.

```pseudo id=main
WU-LINE(x0, y0, x1, y1, w)                   ▷ first octant, integer endpoints
L1  dx ← x1 − x0, dy ← y1 − y0
L2  d ← ⌊dy · 2^w / dx + 1/2⌋                   ▷ the slope in units of 2^(−w)
L3  D ← 0, y ← y0
L4  PLOT(x0, y0, 1), PLOT(x1, y1, 1)
L5  for x ← x0 + 1 to x1 − 1 do
L6      D ← D + d
L7      if D ≥ 2^w then D ← D − 2^w, y ← y + 1      ▷ the carry of a w-bit register
L8      PLOT(x, y, 1 − D / 2^w)
L9      PLOT(x, y + 1, D / 2^w)
```

Line L2 is the only division, done one time. In a $w$-bit register, line L7 is the overflow of the addition of line L6: the carry is the test, and the wrap is the subtraction. After the update of column $x_0 + i$, the pair $(y, D)$ holds the value $y + D/2^w = y_0 + i d / 2^w$, the height computed with the rounded slope. Line L8 gives the lower pixel the weight $1 - D/2^w$, and line L9 gives the upper pixel the weight $D/2^w$. With $q$-bit intensities, a program takes the top $q$ bits of $D$ as the upper weight. Keeping the remainder over $d_x$ in place of $D$ (add $d_y$, and wrap at $d_x$) gives the exact form of the method, which has no error at all.

## Example

Draw the segment from $(0, 0)$ to $(5, 2)$ with $w = 8$. Then $d_x = 5$, $d_y = 2$ and $d = \lfloor 2 \cdot 256 / 5 + \tfrac12 \rfloor = \lfloor 102.9 \rfloor = 102$, while the exact slope is $0.4 \cdot 256 = 102.4$. The endpoints $(0, 0)$ and $(5, 2)$ get intensity 1.

| column $x$ | exact $Y$ | exact weights | $D$ after line L7 | $y$ | weights of lines L8, L9 |
|---|---|---|---|---|---|
| 1 | 0.4 | (1,0): 0.6, (1,1): 0.4 | 102 | 0 | 154/256 = 0.6016, 102/256 = 0.3984 |
| 2 | 0.8 | (2,0): 0.2, (2,1): 0.8 | 204 | 0 | 52/256 = 0.2031, 204/256 = 0.7969 |
| 3 | 1.2 | (3,1): 0.8, (3,2): 0.2 | 306 − 256 = 50 | 1 | 206/256 = 0.8047, 50/256 = 0.1953 |
| 4 | 1.6 | (4,1): 0.4, (4,2): 0.6 | 152 | 1 | 104/256 = 0.4063, 152/256 = 0.5938 |

In column 3, the sum $204 + 102 = 306$ overflows the 8-bit register, so the pair moves up to rows 1 and 2. The largest error is $0.00625$ in column 4, below the bound $4 / 2^9 \approx 0.0078$ of the next section.

## Correctness

The invariant of the loop of line L5, after line L7 of column $x_0 + i$, is

$$y \cdot 2^w + D = y_0 \cdot 2^w + i\,d, \qquad 0 \le D < 2^w.$$

So $y$ is the integer part and $D/2^w$ the fractional part of $\hat Y = y_0 + i d/2^w$, and the two weights are exactly the tent weights of $\hat Y$; each column gets total weight 1. The tent weight is a 1-Lipschitz function of the height, and $|d/2^w - d_y/d_x| \le 2^{-(w+1)}$, so each weight differs from the exact tent weight of the line by at most $i / 2^{w+1} < d_x / 2^{w+1}$. With $q$-bit intensities, $d_x \le 2^{w-q}$ keeps the error below half a step. The exact form gives the tent weights with no error. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The loop of line L5 runs $n - 1$ times for $n = d_x$, and each pass does one addition, one test, at most one subtraction and two PLOT operations. So the time is $\Theta(n)$ in each case, with $2n$ pixels written, and the extra space is $\Theta(1)$. Each PLOT is a read, a blend and a write of the [frame buffer](/frame-buffer/), and in practice this costs more than the loop. The accumulator needs $w$ bits, and $d$ needs $w + 1$ bits only for the diagonal, where $d = 2^w$.

## Properties

- **Constant weight per column.** The two weights of a column add up to 1. So a line with slope $s$ gets weight 1 per column and $1/(1 + s^2)^{1/2}$ per unit of length: a diagonal line is about $1/\sqrt2 \approx 0.71$ times as bright as a horizontal line of the same color.
- **A tent filter, not area coverage.** The weights are the linear interpolation between the two nearest pixel centers in the column. They are not the area of a little square covered by a thick line. A pixel is a point sample, and the tent is one reconstruction filter among many.
- **Integer only.** The loop uses only integer additions and a carry test.
- **Integer endpoints.** This version draws the endpoints at full intensity. Lines with subpixel endpoints need the endpoint variant below.
- **Not exact in fixed point.** The rounded slope moves the computed height by up to $d_x / 2^{w+1}$ at the end of the line, so a weight can be wrong by that much, and the pair of rows can change one column earlier or later than in the exact form.

## Variants and improvements

- **Exact accumulator.** Wrap the accumulator at $d_x$ in place of $2^w$. The weights are then exactly $D/d_x$, at the cost of a division per weight (or a table) to turn $D/d_x$ into a $q$-bit intensity.
- **Subpixel endpoints.** The common version for real endpoints rounds each endpoint to the nearest column, and scales the weights of the two end columns by the part of the pixel that the segment covers in the $x$ direction. The inner loop is the same.
- **Gamma-aware blending.** A table maps each weight to the value to write, so that the blend is done in linear light. See [gamma correction](/gamma-correction/).
- **Circles.** Wu's paper also gives an antialiased circle generator built on the same idea.
- **Filtered lines with a wider kernel.** Methods that weight three or more pixels per column with a better filter look smoother, and cost more per pixel.
- **Supersampling.** [Supersampling](/supersampling-antialiasing/) and [multisampling](/multisample-antialiasing/) antialias all primitives the same way, at the cost of more samples per pixel.

## When to use it

Use Wu's algorithm to draw smooth thin lines in software, for example in a plotting library, a map, a vector editor or a game without hardware antialiasing. It costs little more than [Bresenham's algorithm](/bresenham-line-algorithm/), because the extra work is the second pixel and the blend. Use Bresenham's algorithm when the output has only two colors or must be exact pixels. Use [supersampling](/supersampling-antialiasing/) or a coverage method for thick lines, for lines that cross, or when the line must look the same at every slope.

## Pitfalls

- **Blending in sRGB.** Writing $b + a(c - b)$ with sRGB-encoded $b$ and $c$ makes the line look beaded, because a weight of 0.5 does not give half the light. Convert to linear light before line L8 and line L9, or use a gamma table.
- **Overwriting in place of blending.** Line L8 and line L9 must blend with the old pixel. Writing $a \cdot c$ over a non-black background, or over another line, leaves dark gaps where lines cross. Use [alpha blending](/alpha-blending/).
- **The diagonal in a $w$-bit register.** For $d_y = d_x$, line L2 gives $d = 2^w$, which does not fit in $w$ bits and wraps to 0, so the line comes out horizontal. Draw the diagonal (and the horizontal and vertical lines) as special cases, or give $d$ one more bit.
- **Too few accumulator bits.** With $w = 8$ and a line of 1000 pixels, the height at the end can be wrong by up to about 2 pixels, because $1000/2^9 \approx 1.95$. Choose $w$ with $2^w \ge d_x 2^q$ in line L2.
- **The second pixel off the image.** Line L9 writes row $y + 1$, which can be outside the frame buffer when the line runs along its last row. Clip each PLOT, or clip the line first.

## Implementations

## History

Xiaolin Wu presented the method at SIGGRAPH 1991 in the paper "An efficient antialiasing technique". The paper gives antialiased line and circle generators that need less integer arithmetic than Bresenham's algorithm, and it shows that they give the same images as an earlier method of Fujimoto and Iwata at a fraction of the cost. Michael Abrash gives a fixed-point implementation with a 16-bit accumulator in his Graphics Programming Black Book.

## References
