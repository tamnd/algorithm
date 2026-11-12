---
tag: 5HYJ1C
kind: problem
slug: circle-rasterization
name: Circle rasterization
aliases:
- circle drawing
area: graphics-and-signals/rasterization
level: intro
summary: Choose the pixels that represent a circle outline, usually the pixel nearest to the circle in each column of one octant, copied by the eight symmetries of the grid.
model: word-ram
complexity:
  vars: {r: the radius in pixels}
  time: {worst: Θ(r)}
prereqs: [pixel, line-rasterization]
see_also: [midpoint-circle-algorithm, ellipse-rasterization, midpoint-ellipse-algorithm, integer-square-root, wu-line-algorithm, antialiasing]
sources:
  - paper: doi:10.1145/359423.359432
    title: Jack E. Bresenham, A linear algorithm for incremental digital display of circular arcs, Communications of the ACM 20(2), 100 to 106 (1977)
    locator: the statement of the problem for circular arcs on a raster or plotter grid, and the choice of the move that keeps the residual of the circle equation smallest
  - paper: "M. L. V. Pitteway, Algorithm for drawing ellipses or hyperbolae with a digital plotter, The Computer Journal 10(3), 282 to 289 (1967)"
    locator: curves given by a quadratic equation on a plotter that moves in eight directions
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 3, Section 3.3, Scan Converting Circles (eight-way symmetry and the methods that compute y from x)
---

Circle rasterization asks for the set of pixels that represents a circle on a pixel grid. In the usual form the center and the radius $r$ are integers, and the answer is, on the arc where the circle is closer to flat than to upright, the pixel nearest to the circle in each column, copied to the rest of the circle by the eight symmetries of the square grid. The answer has about $4\sqrt2\, r \approx 5.66\, r$ pixels, and the [midpoint circle algorithm](/midpoint-circle-algorithm/) gives it with integer additions only. Other forms ask for a filled disk, an arc, a thick ring or an antialiased outline.

## In plain words

A screen is a grid of small dots, and a circle passes between most of them. You must decide which dots to light so that the result looks like a round outline of the right size.

Near the top of the circle the outline is flat, so you light one dot in each column, the one nearest to the outline. Near the sides it is steep, so you light one dot in each row instead. A circle looks the same when you flip it across the middle or across a diagonal. So you need to decide only one eighth of the dots, and the flips give the rest.

## Definition

The input is a center $(x_c, y_c)$ and a radius $r \ge 0$, all integers. A [pixel](/pixel/) is a point sample, and here pixel $(i, j)$ is the point $(i, j)$; with the centers at $(i + \tfrac12, j + \tfrac12)$, give the center of the circle in those units. Take the center at the origin; the answer for $(x_c, y_c)$ is the same set moved by $(x_c, y_c)$.

**The octant.** For a column $x$ with $0 \le x \le r$, let $\hat y(x)$ be the integer nearest to $(r^2 - x^2)^{1/2}$, the height of the circle in that column. The octant is the set of the pixels $(x, \hat y(x))$ for the columns $x = 0, 1, 2, \dots$ with $x \le \hat y(x)$. On this arc the slope of the circle is between 0 and $-1$, so one pixel per column is enough for an 8-connected chain.

**No ties.** A tie would need $r^2 - x^2 = (k + \tfrac12)^2 = k^2 + k + \tfrac14$ for an integer $k$, which is not an integer. So for an integer center and radius no tie rule is needed, and the answer is unique.

**The circle.** The output is the image of the octant under the eight maps $(x, y) \mapsto (\pm x, \pm y)$ and $(x, y) \mapsto (\pm y, \pm x)$, as a set, so the pixels on the axes and on the diagonals appear once. By symmetry the result is also the pixel nearest to the circle in each row where the circle is steep. It is an 8-connected closed curve, and the last pixel of the octant has $\hat y - x \in \{0, 1\}$, so the octant meets its mirror image across the diagonal.

The model is the [word RAM](/word-ram/) with integers of about $2 \log_2 r$ bits if $r^2$ is computed, and fewer for incremental methods.

## Variants

- **The smallest residual.** Bresenham's 1977 paper chooses, among the candidate moves, the pixel with the smallest $|x^2 + y^2 - r^2|$. For an integer radius this gives the same pixels as the nearest pixel in each column; the [midpoint circle algorithm](/midpoint-circle-algorithm/) page shows why.
- **4-connected circles.** Some plotters and some grid uses need a curve that moves only along the axes. Each quadrant is then a chain of exactly $2r$ steps, one in $x$ or one in $y$ at a time, so the circle has $8r$ pixels for $r \ge 1$.
- **Real center and radius.** A center between pixels or a radius such as $r + \tfrac12$ allows ties, and the definition then needs a tie rule. Scaling all coordinates by 2 keeps the arithmetic in integers.
- **Filled disks.** The output is the set of pixels with $x^2 + y^2 \le r^2$, or the set with $x^2 + y^2 \le r^2 + r$, which are the pixels at a distance less than $r + \tfrac12$ from the center. It is a set of horizontal spans, one per row. The number of pixels is about $\pi r^2$; the error of this estimate is the subject of the Gauss circle problem in number theory.
- **Arcs and sectors.** The output is the part of the circle between two angles, with a rule for the pixels at the end angles.
- **Thick circles.** The output is the set of pixels in a ring $r_1^2 \le x^2 + y^2 \le r_2^2$, drawn as spans.
- **Antialiased circles.** Each pixel gets an intensity from its distance to the circle, as in the circle generator of Wu's 1991 paper; see [Wu's line algorithm](/wu-line-algorithm/) and [antialiasing](/antialiasing/).

## Examples

| $r$ | octant | pixels in the circle |
|---|---|---|
| 0 | (0, 0) | 1 |
| 1 | (0, 1) | 4 |
| 2 | (0, 2), (1, 2) | 12 |
| 3 | (0, 3), (1, 3), (2, 2) | 16 |
| 7 | (0, 7), (1, 7), (2, 7), (3, 6), (4, 6), (5, 5) | 40 |
| 10 | (0, 10), (1, 10), (2, 10), (3, 10), (4, 9), (5, 9), (6, 8), (7, 7) | 56 |

For $r = 1$ the circle is the four pixels next to the center, and for $r = 3$ the octant ends on the diagonal at (2, 2). For $r = 7$ the true circle meets the diagonal at $x = 7/\sqrt2 \approx 4.95$, but the octant has a pixel in column 5: the height there is $24^{1/2} \approx 4.90$, so the nearest pixel is (5, 5) and it is on the diagonal. Without it the circle would have a gap between (4, 6) and (6, 4). The filled disk of radius 10 has 317 pixels, against $\pi \cdot 100 \approx 314.2$.

## Known algorithms

- The [midpoint circle algorithm](/midpoint-circle-algorithm/) (Bresenham 1977, after Pitteway 1967) computes the octant with an integer decision variable and integer additions, and mirrors it.
- The direct method computes $\hat y(x)$ in each column with an [integer square root](/integer-square-root/). It gives the same pixels at a higher cost per pixel.
- The parametric method plots $(r \cos\theta, r \sin\theta)$ for steps of $\theta$. With a step that is too large it leaves gaps, with a smaller step it plots pixels more than once, and with floating point it can disagree with the exact answer.
- A polygon with many sides, drawn by [line rasterization](/line-rasterization/), approximates the circle. It is common in pipelines that draw only lines and triangles.
- The [midpoint ellipse algorithm](/midpoint-ellipse-algorithm/) with equal semi-axes also draws a circle, but its switch between the two regions does not always give the nearest pixels.

## Bounds

The octant has about $r/\sqrt2 + 1$ pixels, so the circle has $\Theta(r)$ pixels, and each algorithm that lists them takes $\Omega(r)$ time. The midpoint circle algorithm takes $\Theta(r)$ time with $O(1)$ operations per pixel and $O(1)$ extra space. A filled disk has $\Theta(r^2)$ pixels but only $2r + 1$ spans, so it takes $\Theta(r)$ time as a list of spans.

## Reductions

- **Symmetry.** The eight symmetries reduce the circle to the octant, and a filled disk to the spans given by the octant and its mirror images.
- **Integer square roots.** The pixel in column $x$ is $(x, k)$ or $(x, k + 1)$ for $k = \lfloor (r^2 - x^2)^{1/2} \rfloor$, and it is $(x, k + 1)$ exactly when $r^2 - x^2 > k^2 + k$. So the problem reduces to one [integer square root](/integer-square-root/) per column.
- **Ellipses.** A circle is an ellipse with equal semi-axes, so each definition of [ellipse rasterization](/ellipse-rasterization/) contains a definition for circles. With unequal pixel spacing in $x$ and $y$, a circle on the screen is an ellipse in pixel units.

## Applications

- User interfaces and plotting libraries draw circles for markers, buttons, dials and radio buttons.
- CAD programs, map viewers and drawing programs show circles and arcs, and pen plotters and machines with stepper motors cut them with steps in eight directions.
- Games and simulations draw ranges, selection rings and explosions, and test which grid cells lie within a distance of a point.
- Image processing makes circular masks and structuring elements from filled disks.

## References
