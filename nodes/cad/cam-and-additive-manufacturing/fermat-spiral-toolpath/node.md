---
tag: RPHNQ4
kind: algorithm
slug: fermat-spiral-toolpath
name: Connected Fermat spiral toolpath
aliases:
- Fermat spiral infill
area: cad/cam-and-additive-manufacturing
level: research
summary: Zhao and coauthors' fill that covers a layer with Fermat spirals joined into one continuous path, which avoids the many starts and stops of contour filling.
solves: [toolpath-planning]
model: real-ram
complexity:
  vars: {n: number of contours of the rectangle}
  time: {worst: "O(n)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 2016
  people: [Haisen Zhao, Fanglin Gu, Qi-Xing Huang, Jorge Garcia, Yong Chen, Changhe Tu, Bedrich Benes, Hao Zhang, Daniel Cohen-Or, Baoquan Chen]
  note: Zhao and coauthors presented connected Fermat spirals at SIGGRAPH 2016 as a fill pattern for layered fabrication that is one continuous path per connected region.
prereqs: [contour-parallel-toolpath, offset-curve]
see_also: [infill-pattern, direction-parallel-toolpath, slicing-for-additive-manufacturing, medial-axis, distance-transform, hamiltonian-path, polygon-with-holes]
sources:
  - paper: doi:10.1145/2897824.2925958
    title: Haisen Zhao, Fanglin Gu, Qi-Xing Huang, Jorge Garcia, Yong Chen, Changhe Tu, Bedrich Benes, Hao Zhang, Daniel Cohen-Or and Baoquan Chen, Connected Fermat spirals for layered fabrication, ACM Transactions on Graphics 35(4), Article 100, 2016
    locator: the construction of a Fermat spiral from the iso-contours of a spiralable region, and the connection of the spirals of all regions into one path
  - book: isbn:978-3-030-56126-0
    title: Ian Gibson, David Rosen, Brent Stucker and Mahyar Khorasani, Additive Manufacturing Technologies, 3rd edition, Springer, 2021
    locator: the discussion of contour and raster fill paths for extrusion processes
---

A connected Fermat spiral toolpath fills one layer of a printed part with a single continuous path. Zhao and coauthors (2016) built it from the iso-contours of the distance to the boundary, the same curves that a [contour-parallel toolpath](/contour-parallel-toolpath/) prints as separate closed loops. A Fermat spiral links every second contour into an inward spiral and the other contours into an outward spiral, and joins the two at the center. Both ends of the path then lie on the outer contour, next to each other, so the spiral of one region can be linked to the spirals of the regions around it. A contour fill with $n$ loops needs $n$ starts and stops of the nozzle. A Fermat spiral needs one. This page gives the construction on a rectangle, with exact offsets, and proves that the path is simple, stays inside, and covers the rectangle. The general method of the paper, for any region, is described in words only.

## In plain words

Draw nested rectangles inside a rectangle, one bead width apart. A printer could print each one as a closed loop, but then it must stop, lift, move and start again for every loop, and each start leaves a mark.

Instead, cut every loop open at one place on its bottom side. Join loop 1 to loop 3, loop 3 to loop 5, and so on, with short vertical pieces that pass through the cuts of the loops in between. This gives a spiral that goes in. Join loops 2, 4, 6 in the same way. That spiral comes back out. Connect the two spirals at the middle. The nozzle now goes in along one spiral and comes out along the other, and it ends right next to where it started.

## The problem

The input is a rectangle $[0, W] \times [0, H]$ with $W \ge H$ and a bead width $w > 0$. The output is a path for the nozzle, a polyline. A good fill path is simple (it does not cross or touch itself), stays at least $w/2$ from the boundary so that the bead stays inside, and leaves no gap and no overlap between beads. A fill path for a region in a layer is a case of [toolpath planning](/toolpath-planning/).

The contours are the curves at distance $d_i = (i - \tfrac12)\,w$ from the boundary, for $i = 1, \dots, n$, where $n$ is the number of such $i$ with $d_i < H/2$. In a rectangle, the contour at distance $d$ is the rectangle $[d, W - d] \times [d, H - d]$. With a square bead of side $w$ centered on the path, contour $i$ covers the frame of points whose distance to the boundary is between $(i - 1)w$ and $iw$.

## The algorithm

Let $X$ be the abscissa of the links. Write $c_j = X - jw$. Contour $i$ is cut open on its bottom side between $c_i$ and $c_{i-2}$, a gap of length $2w$, except the innermost contour, which has the gap from $c_{n-1}$ to $c_{n-2}$.

```pseudo id=main
FERMAT-RECTANGLE(W, H, w, X)
L1  n ← number of i ≥ 1 with (i − 1/2)w < H/2
L2  if n < 2 or not (2n − 3/2)w < X < W − 3w/2 then fail
L3  for i ← 1 to n do
L4      d ← (i − 1/2)w
L5      s ← (c_(i−2), d)                          ▷ start of the open contour
L6      e ← (c_i, d) if i < n, else (c_(n−1), d)  ▷ end of the open contour
L7      R_i ← s, (W − d, d), (W − d, H − d), (d, H − d), (d, d), e
L8  A ← R_1 R_3 R_5 ...                ▷ the inward spiral
L9  B ← R_2 R_4 R_6 ...                ▷ the outward spiral, before reversal
L10 P ← A followed by B reversed       ▷ the segment between them is the center join
L11 append (X, w/2) to P               ▷ the exit, back to contour 1
L12 return P
```

Each open contour $R_i$ goes counterclockwise from its start $s$ to its end $e$. In line L8, the end $(c_i, d_i)$ of $R_i$ and the start $(c_i, d_{i+2})$ of $R_{i+2}$ have the same abscissa, so consecutive contours of $A$ are joined by a vertical link at $x = c_i$ of length $2w$. That link crosses the bottom side of contour $i + 1$ at $c_i$, which is the middle of the gap of contour $i + 1$. Line L9 does the same for the even contours. Line L10 joins the last points of $A$ and $B$, which are the ends of contours $n - 1$ and $n$ and lie on the vertical line $x = c_{n-1}$. Line L11 adds a last vertical piece from the start of contour 2 down through the gap of contour 1.

The bounds of line L2 make every piece fit. The end of contour $n$ must lie right of its left side, $c_{n-1} > d_n$, which is $X > (2n - \tfrac32)w$. The start of each contour must lie left of its right side, $c_{i-2} < W - d_i$, which is $X < W - \tfrac32 w$ for every $i$. A valid $X$ exists if and only if $W > 2nw$. A square with $W = H = 2nw$ has no valid $X$ in this form. The code of this page rejects it.

## Example

Take $W = 6$, $H = 4$, $w = 1$ and $X = \tfrac72$. Line L1 gives $n = 2$ (with $d_1 = \tfrac12$ and $d_2 = \tfrac32 < 2$), and line L2 needs $\tfrac52 < X < \tfrac92$.

| line | value |
|---|---|
| L5 to L7, $i = 1$ | $R_1$: $(\tfrac92, \tfrac12)$, $(\tfrac{11}2, \tfrac12)$, $(\tfrac{11}2, \tfrac72)$, $(\tfrac12, \tfrac72)$, $(\tfrac12, \tfrac12)$, $(\tfrac52, \tfrac12)$ |
| L5 to L7, $i = 2$ | $R_2$: $(\tfrac72, \tfrac32)$, $(\tfrac92, \tfrac32)$, $(\tfrac92, \tfrac52)$, $(\tfrac32, \tfrac52)$, $(\tfrac32, \tfrac32)$, $(\tfrac52, \tfrac32)$ |
| L8, L9 | $A = R_1$, $B = R_2$ |
| L10 | $R_1$, then $(\tfrac52, \tfrac32)$, $(\tfrac32, \tfrac32)$, $(\tfrac32, \tfrac52)$, $(\tfrac92, \tfrac52)$, $(\tfrac92, \tfrac32)$, $(\tfrac72, \tfrac32)$ |
| L11 | $(\tfrac72, \tfrac12)$ |

The path has 13 points and length 23. It starts at $(\tfrac92, \tfrac12)$ and ends at $(\tfrac72, \tfrac12)$, one bead width to the left. The center join is the segment from $(\tfrac52, \tfrac12)$ up to $(\tfrac52, \tfrac32)$. A square bead of side 1 along the path covers area $23 \cdot 1 + 1 = 24 = W H$, and the covered region is the whole rectangle, so there is no gap and no overlap. Printed as two closed contour loops, the same layer needs two starts. Printed as this path, it needs one.

For $W = 10$, $H = 7$ and $w = 1$, line L1 gives $n = 3$. The path has length 65, and the beads leave a strip of area $(10 - 6)(7 - 6) = 4$ at the center uncovered, because the height is not an even multiple of $w$. A contour fill with the same contours leaves the same strip.

## Correctness

Four facts hold for every input that passes line L2. The full proof is below.

- **Simple.** Every segment is horizontal or vertical. The contours are nested rectangles $w$ apart. A vertical link at $c_i$ spans the heights $d_i$ to $d_{i+2}$, and so it meets only contours $i$, $i + 1$ and $i + 2$. It meets contour $i + 1$ inside its gap, because $c_{i-1} > c_i > c_{i+1}$. The links are at different abscissas $c_1, \dots, c_{n-2}$, the center join is at $c_{n-1}$, and the exit is at $c_0$, inside the gap of contour 1. So no two segments meet except consecutive ones at their shared point.
- **Inside.** Every point has both coordinates at least $w/2$ from the boundary, so a bead of width $w$ stays inside the rectangle.
- **Ends on the boundary.** The path starts at $(c_{-1}, w/2)$ and ends at $(c_0, w/2)$, both on contour 1, at distance $w$.
- **Coverage.** The square beads cover the whole rectangle except the core of points at distance more than $nw$ from the boundary, which has area $(W - 2nw)\,\max(0, H - 2nw)$. The gap of contour $i$ is filled by the link at $c_{i-1}$ for $2 \le i \le n - 1$, by the exit for $i = 1$, and needs nothing for $i = n$, because its length is $w$.

The length is $L = 2n(W + H) - 4wn^2 - w$: the perimeters of the contours, minus the gaps, plus the links, the join and the exit. If $H = 2nw$, the bead area $Lw + w^2$ equals $WH$, and the beads cover the rectangle with no overlap. If $H < 2nw$, the two long sides of contour $n$ are closer than $w$, and the beads there overlap. These are properties of the construction on this page, proved for rectangles. This page makes no coverage claim for general regions.

## Complexity

The path has $6n + 1$ points, and each is found in $O(1)$ time, so the time and the extra space are $O(n)$, with $n < H/(2w) + \tfrac12$. The tests check simplicity by comparing all pairs of segments, which is $O(n^2)$ and is not part of the algorithm.

For a general region, the cost of the method of Zhao and coauthors is dominated by the computation of the iso-contours of the distance field and by the smoothing and optimization steps. The paper does not state a single bound for the whole pipeline, and this page does not give one.

## Properties

- **One path.** The layer is printed with one start and one stop, against one per contour for a contour fill.
- **Spacing.** Two parallel passes side by side are $w$ apart, except the two long sides of the innermost contour, which are $H - 2d_n$ apart. The tests check this on squares and rectangles. The proof page does not prove it.
- **Both ends outside.** The two ends lie on the outer contour, one bead width apart. A spiral can be opened there and spliced into a neighbor path.
- **Follows the boundary.** Like a contour fill, every pass is parallel to the boundary, so the outer surface is printed by a contour, not by the ends of raster lines.
- **Few sharp turns on smooth regions.** On a smooth region, the spirals turn as gently as the contours. On a rectangle, the corners stay.
- **Exact.** With rational input, every point is rational, and every claim above is checked exactly.

## Variants and improvements

- **General regions.** For a region with holes or several lobes, the contours of the distance field change topology: a contour splits into two, or two merge. Zhao and coauthors split the region at these events into spiralable parts, each with nested contours, fill each part with a Fermat spiral, and connect the spirals into one path by a traversal of the tree of parts. Each connection opens a spiral at its two ends on the boundary and routes it through the neighbor. This page does not implement that pipeline.
- **Smoothing.** The paper smooths the path and adjusts the spacing to reduce sharp turns and gaps between beads. Those steps are not part of this page.
- **Single spiral.** A plain spiral links contour $i$ to contour $i + 1$ and ends at the center. It is also one path, but its end is inside, so it cannot be linked to a neighbor without a jump.
- **Other fills.** A [direction-parallel toolpath](/direction-parallel-toolpath/) uses parallel lines joined end to end. It is simpler and gives the same pattern in every region, but it meets the boundary at the end of every line. See [infill pattern](/infill-pattern/) for the sparse fills used inside parts.

## When to use it

Use a connected Fermat spiral when the number of starts and stops matters, for example on extrusion printers where each start and stop leaves a mark or a weak spot, and when the fill should follow the boundary. Use a raster fill when the region is very thin or very complex, or when the slicer must be simple and fast. The claims of the paper about print quality are measured on test prints. The claims on this page are proved for rectangles only.

## Pitfalls

- **Spacing near the links.** The pieces next to the links are short when $X$ is close to a bound of line L2. A piece of length much less than $w$ makes a tight U-turn, where real beads overlap. Choose $X$ near the middle of the interval.
- **Even and odd heights.** If $H$ is not an even multiple of $w$, the center has a gap or an overlap. Adjust $w$ slightly, as the paper adjusts the spacing, or accept the error.
- **Squares.** A square of side $a$ works in this form only if $2nw < a \le (2n + 1)w$, for example $a = 7$ or $a = 9$ with $w = 1$. A square of side $2nw$ has no valid link position. Use a different place for the links, or change $w$ slightly.
- **The exit fills a gap.** Contour 1 has a gap of $2w$, and only the exit passes through it. If the exit is left out, a square of side $w$ next to the start stays empty.
- **Floating-point offsets.** For general regions, offsets in floating point can make two contours touch or cross. Snap the result and check for self-intersection.

## Implementations

## History

Zhao, Gu, Huang, Garcia, Chen, Tu, Benes, Zhang, Cohen-Or and Chen presented connected Fermat spirals for layered fabrication at SIGGRAPH 2016, in ACM Transactions on Graphics. The name comes from the Fermat spiral $r^2 = a^2 \theta$, which has two arms that wind into the center and meet there. Earlier fill paths for printing and for pocket milling were contour loops or zigzag lines.

## References
