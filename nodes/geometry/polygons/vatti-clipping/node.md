---
tag: AT6FZP
kind: algorithm
slug: vatti-clipping
name: Vatti clipping algorithm
aliases:
- Vatti algorithm
- Vatti polygon clipping
- scanbeam clipping
area: geometry/polygons
level: advanced
summary: Sweep-based boolean operations on general polygons, including self-intersecting and holed ones.
solves: [polygon-clipping]
model: real-ram
complexity:
  vars: {n: the total number of input vertices, k: the number of edge crossings}
  time: {worst: O((n + k) n log n)}
  space: {extra: O((n + k) n)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1992
  people: [Bala R. Vatti]
  note: Published as a generic solution to polygon clipping, for arbitrary subject and clip polygons, with output as polygons or as trapezoids.
prereqs: [polygon, sweep-line-technique, winding-number-algorithm, segment-intersection-point]
see_also: [polygon-clipping, polygon-union, weiler-atherton-algorithm, greiner-hormann-algorithm, sutherland-hodgman, bentley-ottmann-algorithm, scanline-polygon-fill, polygon-with-holes]
sources:
  - paper: doi:10.1145/129902.129906
    title: Bala R. Vatti, A generic solution to polygon clipping, Communications of the ACM 35(7), 56 to 63 (1992)
    locator: the whole paper (scanbeams, local minima, left and right bounds, intersections within a scanbeam, and trapezoid output)
  - paper: doi:10.1145/274363.274364
    title: Günther Greiner and Kai Hormann, Efficient clipping of arbitrary polygons, ACM Transactions on Graphics 17(2), 71 to 83 (1998)
    locator: Section 1, introduction (comparison with Vatti's algorithm)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 2, line segment intersection and the plane sweep (the sweep of the active edges and the crossing events)
---

Vatti's algorithm computes boolean operations, intersection, union, difference and exclusive or, of two general [polygons](/polygon/): each may have several contours, holes, and self-intersections, and a fill rule (even-odd or nonzero) says which points each one covers. It sweeps a horizontal line upward. The heights of the vertices cut the plane into scanbeams; inside one scanbeam every edge runs from bottom to top, and the edge crossings inside it are found by sorting the active edges by their $x$ at the bottom and at the top. Between consecutive crossing heights the order of the edges is fixed, and walking the edges from left to right gives the winding numbers of both polygons in every gap, so the result in that strip is a set of trapezoids. Vatti's paper links the trapezoid sides into output contours during the sweep; the implementation here emits the trapezoids and links their boundaries afterwards.

## In plain words

Slice the picture into thin horizontal bands, cutting at every corner of either shape and at every point where two edges cross. Inside one band no corner and no crossing remains, so every edge is a straight slanted line from the bottom of the band to its top, and the edges keep their left-to-right order.

Walk across the band from left to right. Each edge you pass changes a counter for its shape, which tells you whether you are inside that shape. Combine the two answers with the operation you want, for example inside both for the intersection. The pieces of the band where the answer is yes are trapezoids. Stack the trapezoids of all bands, and trace around the outside of the stack to get the outline of the result.

## The problem

The input is two sets of closed contours, the subject $S$ and the clip $C$, with $n$ vertices in all; contours may cross themselves and each other, and edges may overlap. A fill rule, nonzero or even-odd, decides from the winding number $w_S(q)$ whether $q$ is in $S$, and the same for $C$. An operation combines the two memberships: $\wedge$ (intersection), $\vee$ (union), $a \wedge \neg b$ (difference) or $\oplus$ (exclusive or). The output is a list of closed contours whose winding numbers add up to 1 at every point of the result and to 0 elsewhere, off the input edges.

Notation: $x_e(y)$ is the $x$-coordinate of the non-horizontal edge $e$ at height $y$, and $w_e$ is $+1$ for an edge directed downward and $-1$ for one directed upward, the change of the winding number from left to right across it. No general position is needed; the cases where several edges meet at one point or overlap are handled by the same rules.

## The algorithm

```pseudo id=main
VATTI(S, C, op, rule)
L1  Y ← the sorted distinct y-coordinates of all vertices
L2  for each scanbeam [y0, y1] between consecutive values of Y do
L3      A ← the non-horizontal edges that span it, sorted by (x(y0), x(y1))
L4      insertion-sort A by x(y1); at each swap of two edges record the height where they cross
L5      for each sub-beam [ya, yb] between consecutive recorded heights do
L6          walk A in its order at mid-height, group equal edges, and add w_e to w_S or w_C
L7          a span opens where op(fill(w_S), fill(w_C)) becomes true and closes where it becomes false
L8  emit the sides of every span trapezoid: the right side upward, the left side downward
L9  at every cut height emit the horizontal pieces where the coverage just above and just below differ
L10 link the directed pieces into closed contours and return them
```

- **Line L3.** Edges that span the beam are exactly the edges that meet its interior, because no vertex lies strictly inside the beam. Horizontal edges never span a beam; they only affect the coverage at their own height, which line L9 recovers.
- **Line L4.** Two edges cross strictly inside the beam exactly when their order at the bottom and at the top is reversed, and insertion sort swaps each reversed pair exactly once. So the swaps list all crossings in the beam. This is how Vatti's paper finds the intersections in a scanbeam.
- **Line L7.** Spans are the maximal runs of gaps where the result holds. A group of edges with the result on both sides is passed over, so shared edges and overlaps cause no extra boundary.
- **Lines L8 and L9.** The right side goes up and the left side goes down, so the result is on the left. A horizontal piece where only the band above is covered goes east, and one where only the band below is covered goes west. Together these are the boundaries of all the trapezoids, with the shared horizontal parts canceled.
- **Line L10.** At every point as many pieces start as end, so following unused pieces always closes a contour. Vertices where the contour goes straight on are removed.

## Example

Let $S$ be the U shape $(0,0), (6,0), (6,6), (4,6), (4,2), (2,2), (2,6), (0,6)$ and $C$ the bar $(-1,4), (7,4), (7,5), (-1,5)$. The vertex heights $0, 2, 4, 5, 6$ give four scanbeams, and there are no crossings inside them, so each scanbeam is one sub-beam. In the beam $4 \le y \le 5$ the active edges, from left to right, are $x = -1$ (bar, downward), $x = 0$ (U, downward), $x = 2$ (U, upward), $x = 4$ (U, downward), $x = 6$ (U, upward) and $x = 7$ (bar, upward).

| gap | $(-1, 0)$ | $(0, 2)$ | $(2, 4)$ | $(4, 6)$ | $(6, 7)$ |
|---|---|---|---|---|---|
| $w_S$, $w_C$ | 0, 1 | 1, 1 | 0, 1 | 1, 1 | 0, 1 |
| intersection | no | yes | no | yes | no |
| union | yes | yes | yes | yes | yes |
| exclusive or | yes | no | yes | no | yes |

So in this beam the intersection has the spans $[0, 2]$ and $[4, 6]$, the union has one span $[-1, 7]$, the difference has none, and the exclusive or has three. For the union, the beam $2 \le y \le 4$ has the spans $[0, 2]$ and $[4, 6]$, and the beam $0 \le y \le 2$ has $[0, 6]$. At the height $y = 2$ the coverage below is $[0, 6]$ and above it is $[0, 2] \cup [4, 6]$, so line L9 emits the westward piece from $(4, 2)$ to $(2, 2)$: the bottom of the hole. Linking gives two contours, the outer boundary with 16 vertices and area 36, and the clockwise hole $(2,2), (2,4), (4,4), (4,2)$ of signed area $-4$. The areas of the four results are 4, 32, 24 and 28.

The fill rule matters for a self-intersecting input. The pentagram $(0,10), (-6,-8), (10,3), (-10,3), (6,-8)$ has winding number 2 in its central pentagon. Intersected with a large square under the nonzero rule, the result is the whole star; under the even-odd rule the central pentagon is left out, and the result is the five points of the star.

## Correctness

**Theorem.** For every point $q$ off the input edges, the total winding number of the output contours at $q$ is 1 if $\mathrm{op}(\mathrm{fill}(w_S(q)), \mathrm{fill}(w_C(q)))$ holds and 0 otherwise.

The proof is in [proofs/correctness.md](proofs/correctness.md). Inside a sub-beam no two active edges cross, so their left-to-right order is fixed. A ray from a point to the left crosses exactly the active edges to its left, and the ray count of the [winding number](/winding-number-algorithm/) shows that the running sums of line L6 are the winding numbers of $S$ and $C$ in each gap. So the result inside the sub-beam is the union of the span trapezoids, which are disjoint. The emitted pieces add up, as a chain of directed segments, to the sum of the counterclockwise boundaries of all trapezoids, so at every point as many pieces start as end, and linking closes them into contours. A horizontal ray from a point at a height that is not a cut height crosses only trapezoid sides, so the total winding number of the output there is the number of trapezoids that contain the point, which is the indicator of the result.

## Complexity

- **This version.** There are fewer than $n$ scanbeams, and $O(n + k)$ sub-beams in all. Each scanbeam collects and sorts its active edges in $O(n \log n)$ time, and the insertion sort adds $O(1)$ per crossing. Each sub-beam sorts the at most $n$ active edges and walks them, in $O(n \log n)$ time, and emits $O(n)$ trapezoid sides. So the time is $O((n + k) n \log n)$ and the output before linking has $O((n + k) n)$ pieces. The linking is linear in the number of pieces with a hash map.
- **The original.** Vatti's algorithm keeps the active edge list sorted from one scanbeam to the next and builds the output contours during the sweep, so only edges at a vertex or a crossing are touched, and the trapezoid sides inside long runs of an edge are never created one by one.
- **With a search tree.** If the active edges are kept in a balanced search tree and the crossings are found as in the [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/), by testing only edges that become adjacent, each vertex and each crossing costs $O(\log n)$, and the winding numbers change only in the gaps next to the event. That gives $O((n + k) \log n)$ time for the sweep.
- **Lower bound.** The output can have $\Theta(k)$ vertices, since every crossing of two boundaries can be a vertex of the result, and $k$ can be $\Theta(n^2)$.

## Properties

- **General input.** Self-intersecting contours, holes, several contours per operand, shared edges and touching vertices are all handled, without perturbation.
- **Fill rules.** Even-odd and nonzero are both supported by changing one test. Other rules, such as positive winding, change only the function fill.
- **Four operations from one sweep.** The operation enters only through the test of line L7.
- **Trapezoid output.** The spans of line L7 are a decomposition of the result into trapezoids with horizontal tops and bottoms. Vatti's paper offers this as an output form, useful for scan conversion; see [scanline polygon fill](/scanline-polygon-fill/).
- **Exact.** With integer or rational input, all crossing heights and coordinates are rational, and all decisions are exact comparisons.

## Variants and improvements

- **Contours during the sweep.** Vatti's own algorithm starts a pair of left and right bounds at each local minimum of the result, extends them edge by edge as the sweep passes vertices and crossings, and joins them into a contour at each local maximum. This avoids the trapezoid sides and the separate linking pass.
- **Several polygons.** Union of many polygons runs the same sweep with one winding number per input, or with one total winding number and the rule $w \ne 0$ for a nonzero union. See [polygon union](/polygon-union/).
- **Offsetting and Minkowski sums.** Libraries that implement Vatti's algorithm, such as the Clipper library of Angus Johnson, also use it to clean up offset polygons and [Minkowski sums](/minkowski-sum/): those are built as unions of many overlapping pieces under the nonzero rule.
- **Walking methods.** For two simple polygons in general position, [Weiler-Atherton](/weiler-atherton-algorithm/) and [Greiner-Hormann](/greiner-hormann-algorithm/) walk the boundaries instead, in time linear in the size of the input plus the crossings, after the crossings are found.

## When to use it

Use a Vatti-style sweep when the input is general: polygons with holes, self-intersections, shared edges, or many contours at once, and when a fill rule defines the regions. This is the usual situation in GIS, CAD and font processing, and the reason that robust clipping libraries are built on it. For two simple polygons in general position, a walking method is simpler; for a convex window, [Sutherland-Hodgman](/sutherland-hodgman/) is enough.

## Pitfalls

- **Horizontal edges.** They never span a scanbeam and carry no winding change across a horizontal line, but they bound the result. Leaving them out of the output loses the top and bottom of every region; here line L9 recovers them from the coverage above and below.
- **Ties in the edge order.** Edges that meet at a vertex have equal $x$ at one end of the beam. Sorting by $x$ at the bottom with ties broken by $x$ at the top, and testing reversal strictly, keeps touching edges from being counted as crossings.
- **Crossings found only between neighbors.** Testing only adjacent edges at the bottom of a beam misses crossings between edges that become adjacent later in the beam. The insertion sort finds all reversed pairs, not just the adjacent ones.
- **Contours that touch.** At a point where the result touches itself, two contours meet, and the linking may join them into one contour that passes through the point twice. The winding numbers are still right; code that needs simple contours must split them at repeated vertices. The exclusive or of the example comes out as one such contour.
- **Floating point.** The order of edges at a crossing height computed in floating point can disagree with the order used to find the crossing, which breaks the left-to-right walk. Exact rational arithmetic, or a snap rounding step as in practical libraries, avoids that.

## Implementations

The Python version keeps Vatti's scanbeams and the insertion sort for crossings, computes the spans with the winding numbers of both operands, emits trapezoid sides and horizontal pieces, and links them into contours, all in exact rational arithmetic. The tests check the U and bar example for all four operations, the pentagram under both fill rules, shared edges, shared corners, identical inputs, empty and degenerate contours, a polygon with a hole, and 160 pairs of random self-intersecting multi-contour inputs: the total signed area against an exact slab measure of the result region, and the total winding number at rational sample points.

## History

Bala Vatti published the algorithm in 1992. Earlier methods, such as [Sutherland-Hodgman](/sutherland-hodgman/) and [Weiler-Atherton](/weiler-atherton-algorithm/), needed a convex window or polygons in general position; Vatti's sweep handles arbitrary subject and clip polygons with the same code and can produce trapezoids for scan conversion. It is the basis of widely used clipping libraries.

## References
