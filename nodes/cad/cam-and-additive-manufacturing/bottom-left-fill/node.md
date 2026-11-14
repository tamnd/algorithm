---
tag: 28CHNP
kind: algorithm
slug: bottom-left-fill
name: Bottom-left fill heuristic
aliases:
- bottom-left heuristic
area: cad/cam-and-additive-manufacturing
level: core
summary: Places each part in turn at the lowest, then leftmost, position where it fits, often found with no-fit polygons. It is a base for nesting heuristics.
solves: [nesting-problem, strip-packing]
model: real-ram
complexity:
  vars: {n: number of rectangles}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n)"}
properties: {deterministic: true, recursive: false, exact: true, online: true}
history:
  year: 1980
  people: [Brenda S. Baker, Edward G. Coffman Jr., Ronald L. Rivest, Bernard Chazelle]
  note: Baker, Coffman and Rivest defined the bottom-left rule for rectangles and proved the ratio 3 for decreasing widths. Chazelle gave an O(n^2) implementation in 1983. Later authors took the rule to polygons with no-fit polygons.
prereqs: [strip-packing, nesting-problem, no-fit-polygon]
see_also: [rectangle-packing, bin-packing, first-fit-decreasing, minkowski-sum, polygon-with-holes, genetic-algorithm, simulated-annealing, local-search]
sources:
  - paper: doi:10.1137/0209064
    title: Brenda S. Baker, Edward G. Coffman Jr. and Ronald L. Rivest, Orthogonal packings in two dimensions, SIAM Journal on Computing 9(4), 1980, 846 to 855
    locator: the bottom-left rule, the bound of 3 times the optimum for decreasing widths, and the orders for which the rule is arbitrarily bad
  - paper: doi:10.1109/TC.1983.1676307
    title: Bernard Chazelle, The bottomn-left bin-packing heuristic, an efficient implementation, IEEE Transactions on Computers C-32(8), 1983, 697 to 707
    locator: the O(n^2) time and linear space implementation for rectangles (the title has this spelling in print)
  - paper: "Stefan Jakobs, On genetic algorithms for the packing of polygons, European Journal of Operational Research 88(1), 1996, 165 to 181"
    locator: the sliding bottom-left rule (down, then left, repeated) and the genetic search over the order
  - paper: "E. Hopper and B. C. H. Turton, An empirical investigation of meta-heuristic and heuristic algorithms for a 2D packing problem, European Journal of Operational Research 128(1), 2001, 34 to 57"
    locator: the comparison of the sliding BL rule and the bottom-left fill rule, alone and inside genetic search, simulated annealing and naive evolution
  - paper: doi:10.1016/S0377-2217(02)00131-5
    title: Kathryn A. Dowsland, Subodh Vaid and William B. Dowsland, An algorithm for polygon placement using a bottom-left strategy, European Journal of Operational Research 141(2), 2002, 371 to 381
    locator: the bottom-left position of a polygon, holes included, from no-fit polygons
  - paper: "Edmund K. Burke, Robert S. R. Hellier, Graham Kendall and Glenn Whitwell, A new bottom-left-fill heuristic algorithm for the two-dimensional irregular packing problem, Operations Research 54(3), 2006, 587 to 601"
    locator: bottom-left fill of polygons with lines and arcs by direct overlap resolution, with a search over the order
  - paper: doi:10.4230/LIPIcs.STACS.2026.54
    title: Stefan Hougardy and Bart Zondervan, A 13/6-approximation for strip packing via the bottom-left algorithm, STACS 2026, LIPIcs, article 54
    locator: a new order of the rectangles for which the bottom-left rule has ratio 13/6
---

Bottom-left fill (BLF) is a greedy placement rule for packing parts into a strip or a sheet. It takes the parts one at a time in a given order, and puts each one at the feasible position that is lowest, and among the lowest ones, leftmost. A position is feasible when the part stays inside the strip and does not overlap a part placed earlier. Positions in holes between earlier parts count, and this is the "fill" in the name. For rectangles the rule is the bottom-left rule of Baker, Coffman and Rivest (1980), who proved that with the rectangles sorted by decreasing width the strip height is at most 3 times the optimum. For polygons the feasible positions come from [no-fit polygons](/no-fit-polygon/). BLF is a heuristic for the [nesting problem](/nesting-problem/) and for [strip packing](/strip-packing/). Most solvers for the nesting problem use it as the decoder of a search over part orders. This page covers the hole-filling rule. The older sliding rule of Jakobs (1996), which moves a part down and left until it is stuck, is a different rule, and the page names it where the two differ.

## In plain words

You must cut a list of shapes from a long roll of sheet metal of fixed width, and use as little of the roll as you can.

Take the shapes in the order of the list. For each shape, look for the lowest place on the roll where it fits without touching the inside of a shape you have already placed. If there are several such places at the same height, take the one most to the left. Put the shape there and go to the next one.

The rule can put a small shape into a gap that is closed on all sides, below a shape that was placed earlier. A rule that only pushes the shape down and to the left cannot reach such a gap.

The rule never moves a shape again, so the order of the list decides how good the result is.

## The problem

The strip is $[0, W] \times [0, \infty)$. The input is a list of rectangles $R_1, \dots, R_n$ with widths $0 < w_i \le W$ and heights $h_i > 0$, and the output is a lower left corner $(x_i, y_i)$ for each. Rectangles may not rotate. Two placed rectangles overlap when their interiors meet. Touching edges and corners are allowed. The goal of strip packing is the least height $\max_i (y_i + h_i)$. BLF does not solve that goal. It gives each rectangle the position that is least in the [lexicographic order](/lexicographic-order/) of $(y, x)$ among the feasible positions, given the rectangles before it. The polygon case is in Variants.

## The algorithm

Two facts make the search finite. The lowest feasible height is $0$ or the top edge of a placed rectangle: at any other height the rectangle can move down a little. For a fixed height, the rectangles that meet the open band $(y, y + h)$ block the $x$ positions in the open intervals $(x' - w, x' + w')$, and a scan from the left in the order of $x'$ finds the least free $x$.

```pseudo id=main
BLF(W, R)                          ▷ strip width W, rectangles R[1..n] = (w, h)
L1  P ← empty list                                  ▷ placed (x', y', w', h')
L2  for each (w, h) in R, in order do
L3      Y ← {0} ∪ {y' + h' : (x', y', w', h') ∈ P}, in increasing order
L4      for each y ∈ Y do
L5          x ← 0
L6          for each (x', y', w', h') ∈ P with y' < y + h and y' + h' > y, by increasing x' do
L7              if x' ≥ x + w then break             ▷ the gap before this one is wide enough
L8              x ← max(x, x' + w')
L9          if x + w ≤ W then
L10             append (x, y, w, h) to P and go to the next rectangle
L11 return P
```

Line L3 lists the candidate heights. Line L6 keeps the rectangles of the band, the only ones that can block a position at height $y$. Line L7 stops as soon as the rectangle at $x$ ends before the next blocker starts. Line L8 moves $x$ to the right edge of a blocker. At the largest candidate height the band is empty, so line L9 succeeds there and every rectangle is placed.

**Exact arithmetic.** Every test is a comparison of sums of input numbers. With integer or rational sizes the result is exact, and the positions are themselves sums of sizes. With floating point sizes, a sum such as $0.1 + 0.2$ can compare wrong with $0.3$, so a rectangle that fits exactly into a gap can be rejected, or two rectangles can overlap by a rounding error. Use integers in a fixed unit, or exact rationals. The degenerate cases are part of the input: a rectangle as wide as the strip, a rectangle that fits a gap exactly, and edges that touch are all handled by the strict inequalities of line L6 and the non-strict ones of lines L7 and L9.

## Example

Take $W = 10$ and the rectangles $(2, 4)$, $(6, 1)$, $(2, 4)$, $(10, 2)$, $(5, 3)$ as (width, height), in this order.

| rectangle | candidate heights $Y$ | what happens | position |
|---|---|---|---|
| $R_1 = (2, 4)$ | $\{0\}$ | empty strip | $(0, 0)$ |
| $R_2 = (6, 1)$ | $\{0, 4\}$ | $y = 0$: $R_1$ moves $x$ to 2, and $2 + 6 \le 10$ | $(2, 0)$ |
| $R_3 = (2, 4)$ | $\{0, 1, 4\}$ | $y = 0$: $R_1$ gives $x = 2$, $R_2$ gives $x = 8$, and $8 + 2 \le 10$ | $(8, 0)$ |
| $R_4 = (10, 2)$ | $\{0, 1, 4\}$ | $y = 0$ and $y = 1$: $R_1$ blocks, so $x \ge 2$ and $x + 10 > 10$. $y = 4$: empty band | $(0, 4)$ |
| $R_5 = (5, 3)$ | $\{0, 1, 4, 6\}$ | $y = 0$: $x$ goes to 2, 8, 10, fails. $y = 1$: band $(1, 4)$ holds $R_1$ and $R_3$ only, $R_1$ gives $x = 2$, then $R_3$ starts at $8 \ge 2 + 5$ | $(2, 1)$ |

$R_4$ is a lid on the two posts $R_1$ and $R_3$, so the region $[2, 8] \times [1, 4]$ is a closed hole. $R_5$ goes into it. The final height is 6. The total area is 57, so no packing is lower than $5.7$. A sliding rule that starts $R_5$ above the lid and pushes it down and left cannot reach the hole. It stops on top of $R_4$ at $(0, 6)$, and the packing is then 9 high.

## Correctness

Feasible positions form a closed set, so a lexicographically least one exists. If its height $y^*$ were neither 0 nor a top edge, moving the rectangle down by a small amount would keep it feasible, because only a rectangle whose top edge is in the gap could block the move. So $y^*$ is in the list of line L3. For a fixed height the scan of lines L5 to L8 keeps two facts: $x$ is at or right of the right edge of every blocker seen so far, and every smaller $x$ is blocked by one of them. When the scan stops, $x$ is the least $x$ that nothing blocks, and line L9 checks the right wall. Trying the heights in increasing order gives the least $y$, and then the least $x$. The full proof is in proofs/correctness.md.

## Complexity

For the $i$-th rectangle, line L3 has at most $i$ heights, and lines L6 to L8 scan at most $i - 1$ rectangles per height, after one sort of $P$ by $x'$. So one placement takes $O(i^2)$ time, and all of them take $\sum_i O(i^2) = O(n^3)$ time. The extra space is $O(n)$. Chazelle (1983) keeps the free space as a structure of empty regions and places all $n$ rectangles in $O(n^2)$ time and linear space. These bounds are for the rule itself. They say nothing about the height it reaches.

For polygons with at most $m$ vertices each, the cost is dominated by the [no-fit polygons](/no-fit-polygon/) and their arrangement. A placement must look at all pairs of edges of up to $i - 1$ no-fit polygons, so a simple implementation is quadratic in the total number of their edges per part.

## Properties

What is proved:

- **Lexicographic optimality per part.** Each rectangle gets the least feasible $(y, x)$ given the earlier ones. This is not optimality of the packing.
- **Ratio 3 for decreasing widths.** If the rectangles are sorted by decreasing width, the height is at most $3\,\mathrm{OPT}$ (Baker, Coffman and Rivest 1980). For other orders, such as increasing widths, the ratio is not bounded by any constant.
- **No order is always optimal.** Brown (1980) gave instances where no order of the rectangles lets BL reach the optimum. Hougardy and Zondervan (STACS 2026) found an order with ratio $13/6$, the first order that beats 3 since 1980.
- **Online in the order.** A part is placed without looking at the parts after it.
- **Exact.** With integer or rational sizes, positions and tests are exact.

What is only measured: the quality of BLF inside a search over orders, for example by a [genetic algorithm](/genetic-algorithm/) or [simulated annealing](/simulated-annealing/). Hopper and Turton (2001) and Burke, Hellier, Kendall and Whitwell (2006) report densities on benchmark sets from the literature. These are empirical results. They carry no bound.

## Variants and improvements

- **Sliding bottom-left (Jakobs 1996).** Start the part at the top right, then move it down as far as it goes, then left as far as it goes, and repeat until it cannot move. The result is a position that is locally stuck. It need not be the lowest one, and it cannot enter a closed hole. Hopper and Turton (2001) call this rule BL and the hole-filling rule of this page BLF.
- **Polygons with no-fit polygons.** For a part $B$ with reference point $r$, the feasible positions are the points of the inner-fit polygon of the sheet that are in the interior of no [no-fit polygon](/no-fit-polygon/) of $B$ with a placed part. The least point in $(y, x)$ is a vertex of this region: a vertex of a no-fit polygon or of the inner-fit polygon, or a crossing of two of their edges. Dowsland, Vaid and Dowsland (2002) compute this position, holes included. The predicates are [orientation tests](/orientation-test/) and [segment intersection](/segment-intersection-detection/) tests, and in exact arithmetic the crossing points are rationals.
- **Rotations.** Many nesting codes allow a few fixed angles, for example the multiples of 90 degrees, and keep the best position over the angles. Each angle needs its own no-fit polygons.
- **Direct overlap resolution.** Burke, Hellier, Kendall and Whitwell (2006) do not build no-fit polygons. They move the part from a start position and resolve overlaps with the placed parts edge by edge, also for arcs.
- **Order search.** The rule is a decoder. A search over the order of the parts, by [local search](/local-search/), a genetic algorithm or simulated annealing, calls it once per candidate order. Sorting by decreasing width, height or area gives the usual start.
- **Raster version.** On a grid of pixels, the parts and the sheet are bitmaps, and a scan of the cells finds the first cell where the part fits. It is easy and robust, but its precision is the cell size.

## When to use it

Use BLF when parts arrive in a fixed order, or as the inner step of a search over orders, in sheet metal, wood, glass, textile and laser cutting. It is simple, exact with integer coordinates, and it fills holes that simpler rules leave. If you need a guaranteed height for rectangles, use a method with a proved bound, as on the [strip packing](/strip-packing/) page. If the parts are rectangles that must be cut with straight cuts across the sheet, the packing must be a guillotine packing, and BLF does not respect that (see [guillotine cuts](/guillotine-cut-technique/)).

## Pitfalls

- **Sliding is not filling.** Code that pushes a part down and left finds a stuck position, not the lowest feasible one. In the example the sliding rule puts $R_5$ at height 6 instead of 1, and the packing is 9 high instead of 6.
- **The order matters most.** With increasing widths the height can be arbitrarily far from the optimum. Sort first, or search over orders.
- **Floating point gaps.** A part that fits a gap exactly can be rejected, or it can overlap a neighbour by $10^{-15}$. Use integer units or exact rationals for the tests, and floats only for display.
- **Touching versus overlapping.** The overlap test must use the interiors. A closed-set test rejects parts that only touch and leaves a thin gap at every edge.
- **Candidates for polygons.** The least position of a polygon is often at a crossing of edges of two different no-fit polygons. A code that tests only the vertices of each no-fit polygon misses it.
- **Holes in no-fit polygons.** A no-fit polygon of a part with a cavity can have holes. They are feasible regions, and a code that keeps only the outer boundary loses them.

## Implementations

## History

Baker, Coffman and Rivest defined the bottom-left rule for rectangles in a strip in 1980, as part of the first worst-case analysis of two-dimensional packing heuristics, and proved the bound 3 for decreasing widths. Chazelle gave an $O(n^2)$ implementation in 1983. In the 1990s the rule moved to irregular shapes in operations research. Jakobs (1996) used the sliding rule inside a genetic algorithm, and Liu and Teng (1999) improved the sliding moves. Hopper and Turton (2001) compared the sliding rule with the hole-filling rule. Dowsland, Vaid and Dowsland (2002) computed the bottom-left position of polygons, holes included, with no-fit polygons, and Burke, Hellier, Kendall and Whitwell (2006) gave a hole-filling rule for parts with lines and arcs. In 2025 Hougardy and Zondervan found the first order of the rectangles with a better ratio than 3.

## References
