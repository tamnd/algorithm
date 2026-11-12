---
tag: VS80AE
kind: algorithm
slug: scanline-polygon-fill
name: Scanline polygon fill
aliases:
- scan-line fill
area: graphics-and-signals/rasterization
level: core
summary: Fill a polygon one pixel row at a time. Keep the edges that cross the row sorted by x, and fill between crossings that the fill rule selects.
solves: [polygon-scan-conversion]
model: real-ram
complexity:
  vars: {n: the number of polygon edges, H: the image height, I: the number of crossings of edges with row center lines, K: the number of pairs of edges that intersect, P: the number of filled pixels}
  time: {worst: O(n log n + H + I + K + P)}
  space: {extra: O(n + H)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1967
  people: [Chris Wylie, Gordon Romney, David Evans, Alan Erdahl]
  note: Wylie, Romney, Evans and Erdahl drew shaded polygons in scan line order at the University of Utah in 1967. The edge table and the active edge table became the textbook form of the fill.
prereqs: [polygon-scan-conversion, even-odd-fill-rule, nonzero-winding-rule]
see_also: [active-edge-table, stencil-buffer, triangle-rasterization, watkins-scanline-algorithm, sweep-line-technique, insertion-sort, digital-differential-analyzer, region-filling]
sources:
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Section 3.6, Filling Polygons (the spans between crossings, the rules for vertices and horizontal edges, the edge table and the active edge table)
  - paper: "Gregory Ackland and Neil H. Weste, The edge flag algorithm, a fill method for raster scan displays, IEEE Transactions on Computers C-30(1), 41 to 48 (1981)"
    locator: the comparison of the sorted edge list fill with the edge flag fill
  - paper: "Chris Wylie, Gordon Romney, David Evans and Alan Erdahl, Half-tone perspective drawings by computer, AFIPS Fall Joint Computer Conference, 1967"
    locator: the computation of polygon images in scan line order
  - book: isbn:9780201379228
    title: Adobe Systems, PostScript Language Reference, third edition, Addison-Wesley, 1999
    locator: Section 4.5.2, Filling (the two fill rules that the spans follow)
---

Scanline polygon fill solves [polygon scan conversion](/polygon-scan-conversion/) one row of pixels at a time. For each row it keeps the polygon edges that cross the center line of the row in an [active edge table](/active-edge-table/), sorted by the $x$ of the crossing. It then fills the pixels between crossings that the [even-odd fill rule](/even-odd-fill-rule/) or the [nonzero winding rule](/nonzero-winding-rule/) selects. With exact arithmetic it fills exactly the pixels whose shifted centers are inside, and its cost is $O(n \log n + H + I + K + P)$, which depends on the edge crossings as well as on the filled pixels.

## In plain words

Look at the image one row at a time, from top to bottom. A row is a horizontal line through the middles of its pixels. The outline of the shape crosses this line at a few points. Sort these points from left to right.

Walk along the row from the left. Each time you pass a crossing, you change from outside to inside, or the other way. With the even-odd rule you just switch at each crossing. With the nonzero rule you keep a count that goes up or down, by the direction of the outline, and you are inside when the count is not zero. Color the pixels between the crossings where you are inside.

From one row to the next, each crossing moves by a fixed step, and the order of the crossings almost never changes. So you update the list and do not build it again.

## The problem

The image has $W$ columns and $H$ rows. Pixel $(i, j)$ has its center at $(i + 1/2, j + 1/2)$, as in OpenGL and Direct3D 10, and $y$ grows downward. A pixel is a point sample, not a little square. The input is a polygon as a list of closed rings with integer or rational vertices, and a fill rule. Pixel $(i, j)$ must be filled exactly when its center, shifted by $(\varepsilon, \varepsilon^2)$ for a tiny $\varepsilon > 0$, is inside under the rule. This tie rule fills a center on a left or top edge and not one on a right or bottom edge, as the [top-left fill rule](/top-left-fill-rule/) does. See [polygon scan conversion](/polygon-scan-conversion/).

The model is the [real RAM](/real-ram/) with exact rational arithmetic; the implementation keeps every $x$ as a Python fraction, so each decision is exact.

## The algorithm

An edge from $a$ to $b$ with $y_a \ne y_b$ has a top end point and a bottom end point, and a direction $d = +1$ if it goes down and $d = -1$ if it goes up. It is active on row $j$ when $y_{\text{top}} \le j + 1/2 < y_{\text{bot}}$. This half-open rule counts a vertex on a center line once, and it never makes a horizontal edge active. The active rows are $j_0 \le j < j_1$, with $j_0 = \lceil y_{\text{top}} - 1/2 \rceil$ and $j_1 = \lceil y_{\text{bot}} - 1/2 \rceil$.

```pseudo id=main
SCANLINE-FILL(rings, W, H, rule)
L1  ET[0 .. H − 1] ← empty buckets                       ▷ the edge table
L2  for each edge (a, b) of each ring with ya ≠ yb do
L3      d ← +1 if ya < yb else −1; top, bot ← the end points in order of y
L4      j0 ← ⌈top.y − 1/2⌉, j1 ← ⌈bot.y − 1/2⌉; Δ ← (bot.x − top.x) / (bot.y − top.y)
L5      f ← max(j0, 0); if f < min(j1, H) then add (j1, top.x + (f + 1/2 − top.y) Δ, Δ, d) to ET[f]
        sort each bucket by x, then by Δ
L6  AET ← empty list                                     ▷ the active edge table
L7  for j ← 0 to H − 1 do
L8      remove from AET each edge with j1 ≤ j
L9      sort AET by x with insertion sort
L10     merge ET[j] into AET
L11     w ← 0; for k ← 1 to |AET| − 1 do
            w ← w + 1 (even-odd) or w + d_k (nonzero)
            if w is odd (even-odd) or w ≠ 0 (nonzero) then
                fill the pixels i of row j with ⌈x_k − 1/2⌉ ≤ i < ⌈x_{k+1} − 1/2⌉
L12     for each edge in AET do x ← x + Δ
```

The span on line L11 holds the columns $i$ with $x_k \le i + 1/2 < x_{k+1}$. So a center on the left crossing is filled and a center on the right crossing is not, which is the tie rule. Two equal crossings give an empty span and need no special case. Rows above the image start an edge at row 0 on line L5, and line L11 clamps each span to $0 \le i < W$, so the fill clips itself to the image.

## Example

Fill the five-point star with the vertices $(5, 0)$, $(8, 10)$, $(0, 4)$, $(10, 4)$, $(2, 10)$ on an 11 by 11 image. The edge table has two edges in bucket 0, from the top tip, and two in bucket 4, from the two edges that end at $(0, 4)$ and $(10, 4)$. The edge from $(0, 4)$ to $(10, 4)$ is horizontal and never active.

| Row $j$ | Sorted crossings $(x, d)$ | Even-odd spans | Nonzero spans |
|---|---|---|---|
| 4 | $(2/3, -1)$, $(73/20, -1)$, $(127/20, +1)$, $(28/3, +1)$ | $[1, 4)$, $[6, 9)$ | $[1, 9)$ |
| 5 | $(2, -1)$, $(67/20, -1)$, $(133/20, +1)$, $(8, +1)$ | $[2, 3)$, $[7, 8)$ | $[2, 8)$ |
| 6 | $(61/20, -1)$, $(10/3, -1)$, $(20/3, +1)$, $(139/20, +1)$ | none | $[3, 7)$ |

At row 4, the nonzero sum after each crossing is $-1$, $-2$, $-1$, so all three intervals are filled and they join into one span. Under the even-odd rule the count 2 in the middle is even, and the middle is empty. Between rows 5 and 6 the edges cross each other inside the star: the crossing $10/3$ passes $61/20$, and $20/3$ passes $139/20$. The insertion sort on line L9 makes exactly these two moves. At row 6 the two odd intervals are both shorter than the gap between two pixel centers, so the even-odd rule fills nothing in this row although it finds four crossings. The full picture is on the page of [polygon scan conversion](/polygon-scan-conversion/).

## Correctness

At row $j$, the active edge table holds exactly the edges with $y_{\text{top}} \le j + 1/2 < y_{\text{bot}}$, each with its exact crossing $x$, in sorted order. The shifted row $y = j + 1/2 + \varepsilon^2$ meets exactly these edges, at points that are not vertices. An edge crosses it to the left of the shifted center $(i + 1/2 + \varepsilon, \dots)$ exactly when its crossing $x$ is at most $i + 1/2$. So the crossings of a ray from the shifted center to the left are the first $r$ active edges, where $x_r \le i + 1/2 < x_{r+1}$. Their count gives the parity, and their signed sum gives the winding number up to one fixed sign. Line L11 fills pixel $i$ exactly when the rule holds for this prefix. The full proof is below.

## Complexity

Lines L1 to L5 take $O(n + H)$ time, and the sort of the buckets takes $O(n \log n)$ time. In the loop, row $j$ costs $O(1 + A_j)$ for lines L8, L10 and L12, where $A_j$ is the number of active edges, plus the moves of the insertion sort, plus the filled pixels. The sum of $A_j$ over all rows is $I$, the number of crossings of edges with center lines. The values of two active edges change linearly from row to row, so a pair of edges is out of order at most once, and only when the two edges cross between two center lines or meet on one. So the insertion sort makes at most $K$ moves in total, where $K$ is the number of pairs of edges that intersect. The total time is $O(n \log n + H + I + K + P)$, and the extra space is $O(n + H)$.

For a simple polygon, two edges meet only at a shared vertex, so $K \le n$, and the time is $O(n \log n + H + I + P)$. For a polygon that crosses itself, $K$ can be $\Theta(n^2)$.

A bound of $O(n \log n + \text{total span length})$ is sometimes given for this method, but it is not right in general. The terms $H$ and $I$ do not depend on the filled pixels: a polygon made of thin slivers between pixel centers can have $I = \Theta(nH)$ and fill no pixel, as row 6 of the example shows on a small scale. The term $K$ counts the reordering of edges that cross.

## Properties

- With exact arithmetic, the result is exactly the set of pixels whose shifted centers are inside. Two polygons that share an edge fill each pixel on the edge once, never twice and never zero times.
- The same loop serves both fill rules. The even-odd rule ignores the directions $d$, and the nonzero rule uses them.
- It handles concave polygons, holes, several rings and self-intersections with no special case.
- The output is in row order, left to right, which suits a frame buffer that is stored row by row.
- It is a sweep in $y$ over the edges, an instance of the [sweep line technique](/sweep-line-technique/): the edge table is the event queue and the active edge table is the sweep status.

## Variants and improvements

- **Integer stepping.** With integer vertices, each crossing $x$ is an integer plus a fraction with denominator $\Delta y$. A program can keep the numerator as an integer error term and step it like Bresenham's line method, so the fill stays exact without fractions.
- **Convex polygons.** Each row has one span, between the left chain and the right chain of the polygon, so the method needs no sort and no table.
- **Edge flags.** The edge flag method of Ackland and Weste marks the pixels where edges cross each row in a buffer, then fills each row by one pass of a flag from left to right. It avoids the sorted list at the cost of a full pass over each row.
- **Hidden surfaces.** The [Watkins scanline algorithm](/watkins-scanline-algorithm/) keeps the active edges of many polygons and also resolves depth along each span.
- **Coverage.** For [antialiasing](/antialiasing/), a renderer can accumulate the exact area of the polygon in each pixel along the row, in place of a point sample.

## When to use it

Use it to fill general polygons on a CPU: concave shapes, holes and self-intersecting paths, as in vector graphics, fonts and maps. It does work in proportion to the crossings and the filled pixels, not to the bounding box. For triangles on parallel hardware, the edge function tests of [triangle rasterization](/triangle-rasterization/) are simpler. On a GPU, the [stencil buffer](/stencil-buffer/) fills general paths without sorting edges. To fill a region of an image that is given by its pixels, use [region filling](/region-filling/).

## Pitfalls

- **Vertices on a center line.** If an edge counts at both of its end points, a vertex on a center line is counted twice and the parity breaks for the rest of the row. The half-open rule $y_{\text{top}} \le y < y_{\text{bot}}$ counts each vertex once. A local minimum or maximum on the line is then counted 0 or 2 times, which is right.
- **Horizontal edges.** They must not enter the table. Their end points are handled by the edges next to them.
- **Rounding of spans.** Rounding $x_k$ to the nearest integer, in place of $\lceil x_k - 1/2 \rceil$, breaks the tie rule, and shared edges then get pixels twice or not at all.
- **Floating-point drift.** In [IEEE 754](/ieee-754/) arithmetic, adding a rounded $\Delta$ on each row lets $x$ drift, as in the [digital differential analyzer](/digital-differential-analyzer/). A pixel center near an edge then lands on the wrong side, and long edges are hit most. Use exact fractions or integer error terms, or compute $x$ from the end points on each row.
- **Inserting new edges.** New edges must go into their sorted place by a merge. Appending them and sorting again by insertion sort costs up to the length of the table for each new edge, which loses the bound.
- **Thin parts vanish.** A part of the polygon that lies between pixel centers fills no pixel. This is right for point sampling. When every touched pixel is needed, use [conservative rasterization](/conservative-rasterization/).

## Implementations

## History

Wylie, Romney, Evans and Erdahl computed images of polygons in scan line order at the University of Utah in 1967, and scan line methods for hidden surfaces followed, such as the method of Watkins in 1970. The fill of polygons with a sorted edge table and an active edge table is the form that textbooks such as Newman and Sproull and Foley and his coauthors give. Ackland and Weste gave the edge flag method in 1981 as a fill for raster displays with simple hardware.

## References
