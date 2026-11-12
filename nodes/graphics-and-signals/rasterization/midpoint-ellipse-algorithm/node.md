---
tag: VKBD4R
kind: algorithm
slug: midpoint-ellipse-algorithm
name: Midpoint ellipse algorithm
aliases:
- Bresenham ellipse algorithm
area: graphics-and-signals/rasterization
level: intro
summary: Draw an axis-aligned ellipse with integer semi-axes in two regions per quadrant, split where the slope is -1, with integer midpoint decisions.
solves: [ellipse-rasterization]
model: word-ram
complexity:
  vars: {a: the semi-axis along x, b: the semi-axis along y}
  time: {worst: Θ(a + b), best: Θ(a + b)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, integer_only: true, incremental: true}
history:
  year: 1984
  people: [Jerry R. Van Aken, M. L. V. Pitteway]
  note: Pitteway gave the midpoint decision for conics on plotters in 1967, and Van Aken an ellipse algorithm with two regions per quadrant in 1984.
prereqs: [ellipse-rasterization, midpoint-circle-algorithm]
see_also: [circle-rasterization, bresenham-line-algorithm, integer-overflow, pixel]
sources:
  - paper: doi:10.1109/MCG.1984.275994
    title: Jerry R. Van Aken, An efficient ellipse-drawing algorithm, IEEE Computer Graphics and Applications 4(9), 24 to 35 (1984)
    locator: the whole paper (the midpoint ellipse algorithm with integer decision variables and a change of region where the slope is -1)
  - paper: "M. L. V. Pitteway, Algorithm for drawing ellipses or hyperbolae with a digital plotter, The Computer Journal 10(3), 282 to 289 (1967)"
    locator: the decision by the sign of the conic equation at the point between the two candidate moves
  - paper: doi:10.1145/130881.130892
    title: M. Douglas McIlroy, Getting raster ellipses right, ACM Transactions on Graphics 11(3), 259 to 275 (1992)
    locator: the whole paper (which pixels a raster ellipse should have, and incremental programs that give them)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.4, Scan Converting Ellipses (the midpoint ellipse algorithm with two regions)
---

The midpoint ellipse algorithm draws the axis-aligned ellipse with integer semi-axes $a$ and $b$ about an integer center. It splits each quadrant at the point where the slope of the curve is $-1$: above that point it takes one pixel per column, below it one pixel per row, and each choice is the sign of an integer decision variable at the midpoint between the two candidate pixels. It solves [ellipse rasterization](/ellipse-rasterization/) with integer additions and sign tests in $\Theta(a + b)$ time, and it extends the [midpoint circle algorithm](/midpoint-circle-algorithm/), which has eight-way symmetry where the ellipse has only four.

## In plain words

An ellipse looks the same if you flip it left to right or top to bottom, so you draw one quarter and copy it three times. Start at the top. Near the top the curve is flat, so you move one column to the right at each step and decide whether to stay on the row or go down one row. Near the right end the curve is steep, so you move down one row at each step and decide whether to stay in the column or go right one column.

Each decision looks at the point half way between the two candidate squares and asks whether it is inside or outside the curve. A whole number tracks the answer and changes by a simple amount at each step. You change from the first kind of step to the second when the curve becomes steeper than a diagonal.

## The problem

The input is an integer center $(x_c, y_c)$ and integer semi-axes $a, b \ge 0$. A pixel is a point sample at its center, here at the integer point $(i, j)$; with centers at $(i + \tfrac12, j + \tfrac12)$, give the center in those units. Let

$$F(x, y) = b^2 x^2 + a^2 y^2 - a^2 b^2,$$

which is negative inside the ellipse $x^2/a^2 + y^2/b^2 = 1$ and positive outside. In the first quadrant, region 1 is the part where the slope is between 0 and $-1$, and region 2 the part where it is steeper. The gradient of $F$ is $(2b^2 x, 2a^2 y)$, so region 1 is where $b^2 x < a^2 y$. The output is a chain of pixels from $(0, b)$ to $(a, 0)$, one per column in region 1 and one per row in region 2, mapped by the four symmetries $(x, y) \mapsto (\pm x, \pm y)$ and moved by $(x_c, y_c)$. The cost model is the [word RAM](/word-ram/) with integers.

## The algorithm

The decision variables are $4F$ at the midpoints, so they are integers.

```pseudo id=main
MIDPOINT-ELLIPSE(xc, yc, a, b)               ▷ integer center and semi-axes, a, b ≥ 0
L1  x ← 0, y ← b, d1 ← 4b² − 4a²b + a²
L2  PLOT-4(xc, yc, x, y)
L3  while a²(2y − 1) > 2b²(x + 1) do         ▷ region 1: one pixel per column
L4      if d1 < 0 then d1 ← d1 + 4b²(2x + 3)                  ▷ midpoint inside: stay on row y
L5      else d1 ← d1 + 4b²(2x + 3) − 8a²(y − 1), y ← y − 1   ▷ midpoint outside: go down
L6      x ← x + 1, PLOT-4(xc, yc, x, y)
L7  d2 ← b²(2x + 1)² + 4a²(y − 1)² − 4a²b²
L8  while y > 0 do                           ▷ region 2: one pixel per row
L9      if d2 < 0 then d2 ← d2 + 8b²(x + 1) + 4a²(3 − 2y), x ← x + 1   ▷ midpoint inside: go right
L10     else d2 ← d2 + 4a²(3 − 2y)                                     ▷ midpoint outside: stay in column x
L11     y ← y − 1, PLOT-4(xc, yc, x, y)
L12 while x < a do x ← x + 1, PLOT-4(xc, yc, x, 0)     ▷ the tip of a flat ellipse

PLOT-4(xc, yc, x, y)
    PLOT(xc ± x, yc ± y), for all four choices of the signs
```

In region 1 the pass at $(x, y)$ chooses between $(x + 1, y)$ and $(x + 1, y - 1)$, and $d_1 = 4F(x + 1, y - \tfrac12)$. Line L1 is this value at $(0, b)$. The updates of lines L4 and L5 are the changes of $4F$ when the midpoint moves by one column, or by one column and one row. Line L3 is the test $b^2 X < a^2 Y$ at the midpoint $(X, Y) = (x + 1, y - \tfrac12)$, times 2. In region 2 the pass at $(x, y)$ chooses between $(x, y - 1)$ and $(x + 1, y - 1)$, and line L7 starts $d_2 = 4F(x + \tfrac12, y - 1)$ from the last pixel of region 1. Line L12 completes row 0 when region 1 or region 2 reaches it before column $a$.

## Example

Draw the ellipse with $a = 8$ and $b = 5$ about the origin. In region 1 the test of line L3 compares $a^2(2y - 1)$ with $2b^2(x + 1)$, and the exact height in column $x + 1$ is $Y = 5(1 - (x+1)^2/64)^{1/2}$.

| pass at | $d_1$ | test of line L3 | exact $Y$ in column $x + 1$ | new pixel |
|---|---|---|---|---|
| (0, 5) | −1116 | 576 > 50 | 4.9608 | (1, 5) |
| (1, 5) | −816 | 576 > 100 | 4.8412 | (2, 5) |
| (2, 5) | −316 | 576 > 150 | 4.6351 | (3, 5) |
| (3, 5) | 384 | 576 > 200 | 4.3301 | (4, 4) |
| (4, 4) | −764 | 448 > 250 | 3.9031 | (5, 4) |
| (5, 4) | 336 | 448 > 300 | 3.3072 | (6, 3) |
| (6, 3) | | 320 < 350, so region 2 | | |

In region 2 the exact column in row $y - 1$ is $X = 8(1 - (y-1)^2/25)^{1/2}$.

| pass at | $d_2$ | exact $X$ in row $y - 1$ | new pixel |
|---|---|---|---|
| (6, 3) | −1151 | 7.3321 | (7, 2) |
| (7, 2) | −519 | 7.8384 | (8, 1) |
| (8, 1) | 825 | 8.0000 | (8, 0) |

The quadrant has 10 pixels, and each is the nearest pixel in its column (region 1) or row (region 2). The four copies give 40 plots, and the pixels $(0, \pm 5)$ and $(\pm 8, 0)$ come from two quadrants each, so the ellipse has 36 different pixels.

## Correctness

The decision variables satisfy $d_1 = 4F(x + 1, y - \tfrac12)$ at line L3 and $d_2 = 4F(x + \tfrac12, y - 1)$ at line L8, so each choice is the sign of $F$ at the midpoint of the two candidates. For integer $a, b \ge 1$, no midpoint is on the ellipse: the equation $F = 0$ at such a point leads to a Pythagorean triple with an even hypotenuse. So no ties occur. The loop of line L3 never starts at column $a$ (a short argument with the inequality of the arithmetic and geometric means), region 2 never passes column $a$, and so the program ends at $(a, 0)$ after at most $a + b$ passes, with each step to an 8-neighbor.

The midpoint rule keeps the nearest pixel from one column to the next while the curve falls by less than one row per column, and in the same way for rows in region 2. So the pixels of region 1 are the nearest in their columns up to the column where the curve becomes steep, and the pixels of region 2 are the nearest in their rows from the first row where they meet the nearest pixel. Near the switch, the result can differ from the nearest pixels; see Properties. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Each pass adds 1 to $x$ or subtracts 1 from $y$ or both, so there are at most $a + b$ passes, each with a constant number of additions and multiplications by constants, one sign test and four PLOT operations. The time is $\Theta(a + b)$ in each case, and the extra space is $\Theta(1)$. Region 1 has about $a^2/(a^2 + b^2)^{1/2}$ pixels and region 2 about $b^2/(a^2 + b^2)^{1/2}$, so the ellipse has about $4(a^2 + b^2)^{1/2}$ pixels: 3200 for $a = 640$, $b = 480$, and 4472 for $a = 1000$, $b = 500$.

The products $a^2$, $b^2$, $4a^2b^2$ and the terms of lines L5, L7 and L9 can be computed once, or the increments can be kept as variables that change by $8b^2$ and $8a^2$ per step. The decision variables are of the order of $a^2 b^2$, so they need about $2\log_2 a + 2\log_2 b + 4$ bits.

## Properties

- **Exact.** Integers only, no rounding, the same pixels on each machine.
- **No ties for integer semi-axes.** The test $d < 0$ or $d \le 0$ gives the same pixels, because no midpoint is on the ellipse.
- **A monotone 8-connected chain.** Each step moves right, down or diagonally, from $(0, b)$ to $(a, 0)$, and the four copies meet at the ends of the axes.
- **Four-way symmetric only.** The output is the same under $(x, y) \mapsto (\pm x, \pm y)$. For $a \ne b$ there is no diagonal symmetry.
- **Not always the nearest pixel at the switch.** The test of line L3 is at the midpoint, not on the curve, and region 2 starts from the last pixel of region 1, so the pixels near the switch can be one pixel inside the nearest ones. For $a = 8$, $b = 7$ the quadrant is (0, 7), (1, 7), (2, 7), (3, 6), (4, 6), (5, 5), (6, 4), (7, 3), (8, 2), (8, 1), (8, 0): the switch comes at (5, 5), and the nearest pixels in column 6 and row 4 are (6, 5) and (7, 4), not (6, 4).
- **For $a = b$, not the midpoint circle.** For $a = b = 4$ the quadrant goes from (2, 3) to (3, 2), but the [midpoint circle algorithm](/midpoint-circle-algorithm/) also plots (3, 3), the nearest pixel in column 3.

## Variants and improvements

- **Exact pixels near the switch.** McIlroy (1992) studies which pixels a raster ellipse should contain and gives incremental programs that produce them.
- **One loop for both regions.** A version that tests at each step both the move in $x$ and the move in $y$ needs no switch test. Alois Zingl's 2012 report on rasterizing curves uses this form for ellipses, rotated ellipses and Bézier curves.
- **Second-order differences.** The increments of lines L4, L5, L9 and L10 change by constants, so a version with more variables uses only additions.
- **General conics.** Pitteway's 1967 method applies the same midpoint test to the equation of a general conic, for ellipses and hyperbolas.
- **Filled ellipses.** Draw the span from $(x_c - x, y_c \pm y)$ to $(x_c + x, y_c \pm y)$ for the largest $x$ of each row. Each row must be drawn one time only.
- **Half-integer centers or semi-axes.** Scale all coordinates by 2. The decision variables stay integers, but midpoints can then lie on the curve, and a tie rule is needed.

## When to use it

Use the midpoint ellipse algorithm to draw aliased axis-aligned ellipses in software, when the center and the semi-axes are integers and the result must be the same on each machine. For a rotated ellipse, use a general conic method or approximate the curve by a polygon and draw it with [Bresenham's line algorithm](/bresenham-line-algorithm/). For a smooth ellipse, use an antialiased method or [supersampling](/supersampling-antialiasing/). Where each pixel must be the nearest one, use a corrected version such as McIlroy's.

## Pitfalls

- **32-bit integers.** The term $4a^2b^2$ of line L7 is $6.4 \cdot 10^9$ for $a = b = 200$, which does not fit in 32 bits, and the overflow changes the signs of the decisions. Use 64-bit integers, which are enough for $a$ and $b$ below 16384, or [check for overflow](/integer-overflow/).
- **No line L12.** The common textbook form stops when $y$ reaches 0. For a flat ellipse, region 1 can reach row 0 before column $a$: for $a = 15$, $b = 1$ it reaches $(13, 0)$, and without line L12 the pixels $(\pm 14, 0)$ and $(\pm 15, 0)$ are missing.
- **The ellipse routine for circles.** With $a = b$ the output is not the same as the output of the midpoint circle algorithm, as the case $a = b = 4$ shows. Use the circle algorithm for circles.
- **Plotting the ends of the axes two times.** PLOT-4 in lines L2, L11 and L12 plots $(0, \pm b)$ and $(\pm a, 0)$ from two quadrants. With XOR drawing or [alpha blending](/alpha-blending/), these pixels change twice. Plot two copies, not four, of the pixels with $x = 0$ or $y = 0$.
- **The region test at the pixel.** Writing the test of line L3 as $a^2 y > b^2 x$ at the current pixel in place of the midpoint moves the switch. For $a = 1$, $b = 8$ the changed program stays in region 1 for one more pass and plots $(1, 7)$ in place of the nearest pixel $(0, 7)$.

## Implementations

## History

M. L. V. Pitteway published in 1967 an algorithm that draws ellipses and hyperbolas with a digital plotter, choosing each move by the sign of the conic equation at the point between the two candidate moves. Jerry R. Van Aken published "An efficient ellipse-drawing algorithm" in IEEE Computer Graphics and Applications in 1984. It uses integer decision variables at midpoints and changes from steps in $x$ to steps in $y$ where the slope of the curve is $-1$. In 1985 Van Aken and Novak extended the method to other curves in ACM Transactions on Graphics. In 1992 M. Douglas McIlroy analysed the errors of such programs and showed how to get the raster ellipse right. Textbooks such as Foley, van Dam, Feiner and Hughes present the two-region form of this page.

## References
