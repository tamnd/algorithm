---
tag: 0ZN18F
kind: problem
slug: line-rasterization
name: Line rasterization
aliases:
- line drawing
- line scan conversion
area: graphics-and-signals/rasterization
level: intro
summary: Choose the pixels that represent a line segment between two endpoints, for example the pixel nearest to the segment in each column, with a rule for ties.
model: word-ram
complexity:
  vars: {n: "the change on the major axis, max(|x1 - x0|, |y1 - y0|)"}
  time: {worst: Θ(n)}
prereqs: [pixel]
see_also: [bresenham-line-algorithm, digital-differential-analyzer, wu-line-algorithm, amanatides-woo-traversal, line-clipping, circle-rasterization, triangle-rasterization, viewport-transform]
sources:
  - paper: doi:10.1147/sj.41.0025
    title: Jack E. Bresenham, Algorithm for computer control of a digital plotter, IBM Systems Journal 4(1), 25 to 30 (1965)
    locator: the statement of the problem for a plotter that moves in eight directions, and the choice of the point nearest to the line
  - paper: doi:10.1109/T-C.1974.223845
    title: Azriel Rosenfeld, Digital straight line segments, IEEE Transactions on Computers C-23(12), 1264 to 1269 (1974)
    locator: the digitization of a segment and the chord property that characterizes digital straight segments
  - paper: "Jack E. Bresenham, Ambiguities in incremental line rastering, IEEE Computer Graphics and Applications 7(5), 31 to 43 (1987)"
    locator: the cases where the exact line passes half way between two pixels, and the choice that makes a line the same in both directions
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.2, Scan Converting Lines
---

Line rasterization asks for the set of pixels that represents a line segment on a pixel grid. The common form takes two integer endpoints and asks, in each column that the segment crosses, for the pixel nearest to the segment, or in each row for a steep segment, with a fixed rule for the case where two pixels are equally near. The answer has one pixel for each step on the major axis, so it has $n + 1$ pixels for $n = \max(|x_1 - x_0|, |y_1 - y_0|)$, and the classic integer solution is [Bresenham's line algorithm](/bresenham-line-algorithm/). Other forms ask for every pixel that the segment touches, or for pixels with intensities that hide the stairs.

## In plain words

A screen is a grid of small dots, and a straight line between two dots usually passes between the dots, not through them. You must decide which dots to light so that the result looks like the line.

For a line that is closer to flat than to upright, light one dot in each column, the one nearest to the true line. For a steep line, light one dot in each row. Sometimes the line passes exactly half way between two dots, and then you need a fixed rule to choose one. Without such a rule, the same line can come out differently when it is drawn from the other end.

## Definition

The input is two pixels $P_0 = (x_0, y_0)$ and $P_1 = (x_1, y_1)$ with integer coordinates. A [pixel](/pixel/) is a point sample, and here pixel $(i, j)$ is the point $(i, j)$; with the centers at $(i + \tfrac12, j + \tfrac12)$ of OpenGL and Direct3D, the integer endpoints are pixel centers and nothing changes. Let $d_x = x_1 - x_0$, $d_y = y_1 - y_0$ and $n = \max(|d_x|, |d_y|)$. The segment is $x$-major if $|d_x| \ge |d_y|$ and $y$-major otherwise.

**Nearest pixel on the major axis.** For an $x$-major segment with $d_x \ne 0$, the exact height in column $x$, for $x$ between $x_0$ and $x_1$, is

$$Y(x) = y_0 + \frac{d_y}{d_x}\,(x - x_0).$$

The output is the set of the $n + 1$ pixels $(x, y)$ where $y$ is the integer nearest to $Y(x)$. A tie happens when $Y(x)$ is an integer plus $\tfrac12$, which needs $2 d_y (x - x_0) / d_x$ to be an odd integer, so $d_x$ must be even. A tie rule chooses one of the two pixels: toward the start, toward the end, always down, always up, and so on. A $y$-major segment uses the same definition with the axes exchanged, and $P_0 = P_1$ gives one pixel.

**Properties of the answer.** Consecutive pixels differ by one on the major axis and by at most one on the other axis, so the set is 8-connected and has no pixel that could be left out without a gap. Each pixel is within $\tfrac12$ of the segment along the minor axis. The output is the same up to symmetry when the segment is reflected in an axis or a diagonal, if the tie rule is reflected too. A tie rule that does not depend on the direction, such as "always round half down", gives the same pixels from $P_0$ to $P_1$ and from $P_1$ to $P_0$; the rule "toward the start" does not.

**Digital straight segments.** Rosenfeld called a set of pixels a digital straight segment if it is the nearest-pixel digitization of some segment, and showed that these are exactly the 8-connected sets with the chord property: each point of a segment between two of its pixels is less than one unit, in the maximum norm, from a pixel of the set. In such a set, for an $x$-major segment that is not horizontal, the runs of pixels on the same row, other than the two runs at the ends, have only two lengths, $\lfloor |d_x| / |d_y| \rfloor$ and $\lceil |d_x| / |d_y| \rceil$.

The model is the [word RAM](/word-ram/) with integers of $O(\log n)$ bits more than the coordinates. The output is a list of pixels or a set of writes to a [frame buffer](/frame-buffer/).

## Variants

- **The diamond exit rule.** OpenGL and Direct3D rasterize aliased lines by a rule that gives the pixels whose small diamond around the center the segment leaves. For segments with integer endpoints, most pixels are the nearest pixels, but the rule decides the ends and the ties in its own way, so that two segments that join at a point do not both draw it.
- **Supercover.** The output is every pixel whose unit square the segment touches. It is 4-connected, and it is the answer for line of sight on a grid map and for the cells that a ray crosses. [Amanatides-Woo traversal](/amanatides-woo-traversal/) gives these cells in order.
- **Real endpoints.** The endpoints are real numbers, for example after the [viewport transform](/viewport-transform/) and [line clipping](/line-clipping/). The answer is still the nearest pixel in each column, now for the columns whose centers are between the endpoints.
- **Antialiased lines.** The output gives each pixel an intensity, for example from a filter of the distance to the segment, so that the line looks smooth. [Wu's line algorithm](/wu-line-algorithm/) is one answer with two pixels per column.
- **Thick lines and polylines.** A line of width $w$ is the region within $w/2$ of the segment, with caps at the ends and joins between the segments of a polyline. It is a polygon fill problem; see [polygon scan conversion](/polygon-scan-conversion/).
- **Lines in three dimensions.** The same nearest rule picks one voxel per step on the major of three axes.

## Examples

| segment | output | comment |
|---|---|---|
| (0, 0) to (6, 0) | (0, 0), (1, 0), ..., (6, 0) | 7 pixels, horizontal |
| (0, 0) to (5, 5) | (0, 0), (1, 1), ..., (5, 5) | 6 pixels, diagonal |
| (0, 0) to (8, 3) | (0, 0), (1, 0), (2, 1), (3, 1), (4, 1) or (4, 2), (5, 2), (6, 2), (7, 3), (8, 3) | a tie in column 4 |
| (0, 0) to (3, 8) | (0, 0), (0, 1), (1, 2), (1, 3), (1, 4) or (2, 4), (2, 5), (2, 6), (3, 7), (3, 8) | $y$-major, the reflection of the previous row |
| (0, 0) to (7, 2) | (0, 0), (1, 0), (2, 1), (3, 1), (4, 1), (5, 1), (6, 2), (7, 2) | no tie, because $d_x$ is odd |

In the third row the exact heights in the columns 0 to 8 are $0, 0.375, 0.75, 1.125, 1.5, 1.875, 2.25, 2.625, 3$. Column 4 is a tie. Bresenham's algorithm with ties toward the start gives $(4, 1)$, and the [DDA](/digital-differential-analyzer/) with rounding half up gives $(4, 2)$. Both are correct answers for their tie rules. In the last row the runs on rows 0, 1 and 2 have lengths 2, 4 and 2, and the run lengths of the inner rows are $\lfloor 7/2 \rfloor = 3$ or $\lceil 7/2 \rceil = 4$; the runs at the ends are cut by the endpoints.

## Known algorithms

- The [digital differential analyzer](/digital-differential-analyzer/) adds the slope to a floating-point height at each step and rounds it. It is simple, but the rounding error grows along the line, and it can choose the wrong pixel at a tie or on a long line.
- [Bresenham's line algorithm](/bresenham-line-algorithm/) (1965) uses only integer additions and a sign test per step, and it gives exactly the nearest pixel in each column, with a fixed tie rule.
- [Wu's line algorithm](/wu-line-algorithm/) (1991) gives antialiased lines with two pixels per column, with an integer accumulator.
- [Amanatides-Woo traversal](/amanatides-woo-traversal/) (1987) gives the supercover of a segment or a ray, cell by cell.
- Run-length methods compute the length of each horizontal run in one step from the run pattern, and methods with two or more pixels per step take the next few pixels from a small table of patterns. They give the same pixels with fewer decisions.

## Bounds

The output of the nearest-pixel form has exactly $n + 1$ pixels, so each algorithm that lists them takes $\Omega(n)$ time, and Bresenham's algorithm takes $\Theta(n)$ time with $O(1)$ integer operations per pixel and $O(1)$ extra space. If the output may be a list of horizontal runs for an $x$-major segment, it has $|d_y| + 1$ runs, and run-length methods list them in $O(|d_y| + 1)$ steps. The integers involved have $O(\log n)$ bits more than the coordinates.

## Reductions

- **Symmetry.** Each segment reduces to one with $0 \le d_y \le d_x$ by an exchange of the axes and changes of sign, so an algorithm for the first octant solves all eight.
- **A floor formula.** With the tie rule "round half down", the pixel in column $x_0 + k$ of a segment in the first octant has the row $y_0 + \lceil (2k d_y - d_x) / (2 d_x) \rceil$. So the problem is the evaluation of a floor or ceiling of a linear function at each integer, the same function that appears in sums of floors.
- **Continued fractions.** The pattern of runs is a word in two letters that the [continued fraction](/continued-fraction/) of $d_y / d_x$ describes, and the path of $d_y / d_x$ in the [Stern-Brocot tree](/stern-brocot-tree/) gives the same pattern. The [Euclidean algorithm](/euclidean-algorithm/) on $d_x$ and $d_y$ computes it.

## Applications

- The [graphics pipeline](/graphics-pipeline/) draws wireframes, outlines and debug lines after [line clipping](/line-clipping/) and the [viewport transform](/viewport-transform/).
- Plotting libraries, CAD programs, user interfaces and map viewers draw lines in software, often antialiased.
- Pen plotters, laser cutters and machines with stepper motors move one step at a time in eight directions; Bresenham's 1965 paper was written for such a plotter.
- [Polygon scan conversion](/polygon-scan-conversion/) and [triangle rasterization](/triangle-rasterization/) walk the edges of a shape with the same kind of incremental step.
- Games and robots on grid maps test line of sight with the supercover form.

## References
