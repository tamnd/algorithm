---
tag: GET9EH
kind: problem
slug: polygon-scan-conversion
name: Polygon scan conversion
aliases:
- polygon filling
- scan conversion of polygons
area: graphics-and-signals/rasterization
level: core
summary: Find the pixels of a W by H grid whose centers lie inside a polygon under a fill rule, with a tie rule for centers on edges.
model: real-ram
complexity:
  vars: {n: the number of polygon edges, w: the image width, h: the image height}
  time: {worst: O(w h n)}
prereqs: [polygon, pixel, point-in-polygon]
see_also: [scanline-polygon-fill, even-odd-fill-rule, nonzero-winding-rule, triangle-rasterization, top-left-fill-rule, region-filling, polygon-window-clipping, stencil-buffer]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.5, Filling Rectangles, Section 3.6, Filling Polygons, and Section 19.5, Filling Algorithms
  - book: isbn:9780201379228
    title: Adobe Systems, PostScript Language Reference, third edition, Addison-Wesley, 1999
    locator: Section 4.5.2, Filling (the nonzero winding number rule and the even-odd rule), and Section 4.5.3, Insideness Testing
  - url: https://svgwg.org/svg2-draft/painting.html
    title: Scalable Vector Graphics (SVG) 2, Chapter 13, Painting
    locator: Section 13.4.2, Winding rule, the fill-rule property
  - paper: "Gregory Ackland and Neil H. Weste, The edge flag algorithm, a fill method for raster scan displays, IEEE Transactions on Computers C-30(1), 41 to 48 (1981)"
    locator: the fill of polygons on a raster by edge flags along each scan line
---

Polygon scan conversion asks which pixels of a raster image a polygon covers. A pixel is a point sample at its center, and it is covered when its center is inside the polygon under a fill rule, with a tie rule for centers that lie on an edge. The two fill rules in use are the [even-odd fill rule](/even-odd-fill-rule/) and the [nonzero winding rule](/nonzero-winding-rule/), and they differ only for polygons that cross themselves or have rings that overlap. The main method is [scanline polygon fill](/scanline-polygon-fill/), which works one row of pixels at a time.

## In plain words

A screen is a grid of small dots. To draw a filled shape, you must decide for each dot whether it is part of the shape. Look at the exact middle of the dot. If the middle is inside the shape, color the dot.

Two questions need a firm answer. First, when the outline of a shape crosses itself, which parts are inside? There are two common rules, and they give different pictures. Second, when the middle of a dot lies exactly on the outline, is the dot in or out? Two shapes that share a side must not both color the dots on that side, and they must not both skip them.

## Definition

The image has $W$ columns and $H$ rows of pixels. Pixel $(i, j)$ has its center at $c_{ij} = (i + 1/2, j + 1/2)$, with $0 \le i < W$, $0 \le j < H$, and $y$ grows downward, so row 0 is the top row. The centers are those of OpenGL and Direct3D 10; the downward $y$ axis is that of Direct3D, while OpenGL window coordinates have $y$ up. A pixel is a point sample at $c_{ij}$, not a little square: the problem asks about points, not about the area that a pixel square shares with the polygon.

The input is a polygon $P$ as a list of closed rings of vertices, with integer or rational coordinates, and a fill rule. For a point $x$ off the boundary, let $w(x)$ be the [winding number](/winding-number-algorithm/) of $P$ around $x$. The point is inside under the even-odd rule when $w(x)$ is odd, and inside under the nonzero rule when $w(x) \ne 0$.

A center on an edge needs a tie rule. This page uses the rule of a small shift: pixel $(i, j)$ is covered when the point $c_{ij} + (\varepsilon, \varepsilon^2)$ is inside for all small enough $\varepsilon > 0$. The shifted point lies on no line through two vertices, so it is never on the boundary. The rule means that a center on a left edge or a top edge is covered, and a center on a right edge or a bottom edge is not. This is the [top-left fill rule](/top-left-fill-rule/) of triangle rasterization.

The output is the set of covered pixels, most often as spans: for each row $j$, a list of column ranges $[i_0, i_1)$.

**Partition property.** If polygons $P_1, \dots, P_k$ cover a region with no overlap, sharing only edges, each pixel center in the interior of the region is covered by exactly one of them. The reason is that the shifted center is off every edge, so it lies in the inside of exactly one polygon. A center on the outer boundary of the region is covered by at most one, and by none if it is on a right or a bottom edge.

**Exact and floating-point arithmetic.** The decisions are signs of expressions in the vertex coordinates, so with integer or rational input they can be exact. Many renderers snap vertices to a fixed grid of subpixel steps, so that the decisions are integer tests. With [IEEE 754](/ieee-754/) floating point, a crossing $x$ that is computed by repeated addition of the slope drifts, as in the [digital differential analyzer](/digital-differential-analyzer/). A center near an edge can then fall on the wrong side, and two polygons that share an edge can both cover a pixel, or both miss it.

## Variants

- **Triangles only.** GPUs scan convert triangles, which are convex and have three edges. See [triangle rasterization](/triangle-rasterization/).
- **Convex polygons.** Each row then has one span, between a left edge and a right edge.
- **Coverage.** In [antialiasing](/antialiasing/), the output is a value in $[0, 1]$ for each pixel, from many samples or from exact area. This is a different problem from the point sample of this page.
- **Conservative rasterization.** The output is every pixel whose square the polygon touches, or only the pixels whose squares are fully inside. See [conservative rasterization](/conservative-rasterization/).
- **Paths with curves.** Fonts and vector images use curves. A renderer first flattens the curves into a polygon with a stated tolerance.
- **Region filling.** The input is a set of pixels and a seed pixel, not a polygon. That is [region filling](/region-filling/), a different problem.

## Examples

Take the five-point star with the vertices $(5, 0)$, $(8, 10)$, $(0, 4)$, $(10, 4)$ and $(2, 10)$, in this order, on an 11 by 11 image. The ring crosses itself. The five tips have winding number 1 (up to sign), and the pentagon in the middle has winding number 2. A `#` is a covered pixel, and row 0 is at the top.

```text
even-odd       nonzero
...........    ...........
...........    ...........
....##.....    ....##.....
....##.....    ....##.....
.###..###..    .########..
..#....#...    ..######...
...........    ...####....
...####....    ...####....
..##..##...    ..##..##...
..#....#...    ..#....#...
...........    ...........
```

The rules agree on the tips and differ on the middle. Rows 0 and 1 are empty for both: the top tip at the center line $y = 1/2$ runs from $x = 4.85$ to $x = 5.15$, and no pixel center lies between. Row 6 is empty under the even-odd rule for the same reason: the center line $y = 6.5$ crosses the star edges near $x = 3.05$, $3.33$, $6.67$ and $6.95$, and both odd intervals are thinner than one pixel.

**Shared edges.** The square with corners $(1, 1)$ and $(5, 4)$ covers the 12 pixels with $1 \le i < 5$ and $1 \le j < 4$. Cut it along its diagonal into two triangles. Each of the 12 pixels is covered by exactly one of the two triangles, also the pixels whose centers lie near the diagonal.

**Holes.** An 8 by 8 square with an inner 4 by 4 square as a second ring has a hole under the even-odd rule, in either direction of the inner ring. Under the nonzero rule it has a hole only when the inner ring goes the other way around.

## Known algorithms

- [Scanline polygon fill](/scanline-polygon-fill/) sorts the edges by their first row, keeps the edges that cross the current row in an [active edge table](/active-edge-table/), and fills the spans between crossings. Its cost is $O(n \log n + H + I + K + P)$, where $I$ is the number of crossings of edges with center lines, $K$ the number of pairs of edges that cross, and $P$ the number of covered pixels.
- Edge functions test each pixel center in a bounding box against the edge lines, which suits triangles and parallel hardware. See [edge function](/edge-function/) and [Pineda rasterization](/pineda-rasterization/).
- The edge flag method of Ackland and Weste (1981) marks the crossings in a buffer and then fills each row by one pass of a flag from left to right.
- The [stencil buffer](/stencil-buffer/) fills a polygon of any shape in two passes: it counts the windings at each pixel with a fan of triangles, then it covers the pixels with a nonzero count.
- The direct method tests each pixel center with a point in polygon test, the [crossing number algorithm](/crossing-number-algorithm/) or the [winding number algorithm](/winding-number-algorithm/), in $O(WHn)$ time.

## Bounds

The output can have $\Theta(WH)$ pixels, so a list of pixels costs $\Omega(n + P)$ time. As spans, the output can be much smaller than $P$. The direct method takes $O(WHn)$ time. The cost of the scanline method depends on $I$, which is not bounded by $P$: a polygon of thin slivers between pixel centers crosses many center lines and covers no pixel.

## Reductions

- Each pixel is one [point in polygon](/point-in-polygon/) query at a shifted center, so the problem reduces to $WH$ such queries.
- Each row is a one-dimensional problem: sort the crossings of the edges with the center line, then mark the intervals that the fill rule selects.
- [Polygon window clipping](/polygon-window-clipping/) to the image rectangle before scan conversion changes no pixel, because each pixel center is inside the image.

## Applications

- Fonts: TrueType outlines use the nonzero rule, and PostScript and PDF offer both rules.
- Vector graphics: the SVG `fill-rule` property and the canvas fill of web browsers select nonzero or even-odd.
- The fill of polygons in maps, chip layouts and 2D games, and the first step of [polygon shading](/polygon-shading/).

## References
