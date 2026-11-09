---
tag: 6722KQ
kind: algorithm
slug: overmars-yap-algorithm
name: Overmars-Yap algorithm
aliases:
- overmars-yap
- trellis partition for Klee's measure problem
area: geometry/intersections
level: research
summary: Solve Klee's measure problem in O(n^(d/2) log n) time for d of 3 or more by cutting space into cells where all boxes are piles, whose union, a trellis, has a closed-form volume.
solves: [klee-measure-problem]
model: real-ram
complexity:
  vars: {n: the number of boxes, d: the dimension}
  time: {worst: O(n^(d/2) log n)}
  space: {extra: O(n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1988
  people: [Mark H. Overmars, Chee-Keng Yap]
  note: Overmars and Yap presented the trellis partition at FOCS 1988 and in SIAM Journal on Computing in 1991, improving the O(n^(d-1) log n) sweep bound for d of 3 or more; Chan removed the log factor in 2013.
prereqs: [klee-measure-problem, area-of-union-of-rectangles, interval-union-length]
see_also: [segment-tree, sweep-line-technique, coordinate-compression, orthogonal-range-reporting, axis-aligned-bounding-box, rectangle-intersection-reporting]
sources:
  - paper: doi:10.1137/0220065
    title: Mark H. Overmars and Chee-Keng Yap, New upper bounds in Klee's measure problem, SIAM Journal on Computing 20(6), 1991
    locator: piles and trellises, the measure of a trellis, the partition of space into O(n^(d/2)) cells, and the O(n^(d/2) log n) time and O(n) space bounds
  - paper: doi:10.1109/FOCS.2013.51
    title: Timothy M. Chan, Klee's measure problem made easy, FOCS 2013
    locator: the simplified divide and conquer that gives O(n^(d/2)) time, and its comparison with the Overmars-Yap partition
  - paper: doi:10.1016/0196-6774(81)90027-4
    title: Jan van Leeuwen and Derick Wood, The measure problem for rectangular ranges in d-space, Journal of Algorithms 2(3), 1981
    locator: the earlier sweep-based bounds that the trellis method improves
---

The Overmars-Yap algorithm computes the volume of the union of $n$ axis-parallel boxes in $\mathbb{R}^d$, the [Klee measure problem](/klee-measure-problem/), in $O(n^{d/2} \log n)$ time and $O(n)$ space for $d \ge 3$. Its key observation is that a box which covers a cell in all coordinates but one is a *pile*, and the union of piles in a cell, a *trellis*, has a volume given by a product formula. The algorithm cuts space into cells so that inside every cell all boxes are piles or cover the cell, and it adds up the trellis volumes. Overmars and Yap built a partition with $O(n^{d/2})$ cells that has this property, which beat the $O(n^{d-1} \log n)$ of the plain sweep.

## In plain words

You want the volume covered by many overlapping boxes. Cut space into small rooms. In some rooms a box fills the whole room, and then the room is fully covered. In other rooms each box that enters goes all the way through the room in every direction but one, like a wall that is as wide and tall as the room. Such walls in a room form a lattice, and the space they leave free is easy to measure: in each direction, the free part is the part of the room that no wall of that direction touches, and the free space is the product of these parts.

So the method keeps cutting rooms until every room is of one of these two easy kinds. The skill is in cutting so that the number of rooms stays small.

## The problem

**Input.** $n$ boxes $B_i = \prod_{j=1}^{d} [a_{i,j}, b_{i,j}]$ in $\mathbb{R}^d$.

**Output.** $\operatorname{vol}\big(\bigcup_i B_i\big)$.

**Notation.** A *cell* is a box $C = \prod_j [\ell_j, h_j]$, and $|C_j| = h_j - \ell_j$. A box $B$ *covers* $C$ if $C \subseteq B$. It is a *$j$-pile* of $C$ if $B \cap C$ has positive volume and $B$ covers $C$ in every coordinate except $j$, but not in coordinate $j$. For the $j$-piles of $C$, $U_j$ is the length of the union of their $j$-intervals inside $[\ell_j, h_j]$. A boundary value of $B$ in coordinate $j$ is *inner* for $C$ if it lies strictly between $\ell_j$ and $h_j$.

**Model.** The [real RAM](/real-ram/); the implementation uses exact integers and `Fraction`s.

## The algorithm

```pseudo id=main
MEASURE(C, S)                                ▷ cell C, boxes S; start with the bounding box
L1  S ← {B ∩ C : B ∈ S and vol(B ∩ C) > 0}
L2  if some B ∈ S covers C then return vol(C)
L3  if every B ∈ S is a pile of C then         ▷ the boxes form a trellis in C
L4      U_j ← length of ∪ {B_j : B ∈ S a j-pile}, for j = 1..d
L5      return vol(C) − ∏_j (|C_j| − U_j)
L6  choose j and an inner value m of a box of S that is not a pile
L7  cut C at x_j = m into C⁻ and C⁺
L8  return MEASURE(C⁻, S) + MEASURE(C⁺, S)
```

Line L5 is the trellis formula: a point of $C$ is outside every pile exactly when, for each $j$, its coordinate $x_j$ avoids the union of the $j$-pile intervals, so the free part of $C$ is a product of $d$ sets of lengths $|C_j| - U_j$. Line L6 is where the methods differ. Overmars and Yap fix a partition of space in advance, built from the box boundaries in a balanced way, so that there are $O(n^{d/2})$ cells, each box is a pile in all but few of the cells it meets, and a sweep in one coordinate maintains the trellis measures with $O(\log n)$ work per change. The implementation uses a simple rule instead: it tries the coordinate $\text{depth} \bmod d$ first and cuts at the lower median of the inner values of the boxes that are not piles. Both rules give the same exact answer; the time bound holds for the Overmars-Yap partition.

## Example

$R_1 = [0, 4] \times [0, 2]$ and $R_2 = [2, 6] \times [1, 3]$, with the start cell $[0, 6] \times [0, 3]$ and the median rule:

| cell | boxes in the cell after L1 | kind | value |
| --- | --- | --- | --- |
| $[0, 6] \times [0, 3]$ | $R_1$, $R_2$, both not piles | cut at $x = 2$ (L6) | |
| $[0, 2] \times [0, 3]$ | $R_1 \to [0, 2] \times [0, 2]$, a 2-pile | trellis: $6 - (2 - 0)(3 - 2)$ | $4$ |
| $[2, 6] \times [0, 3]$ | $R_1 \to [2, 4] \times [0, 2]$ not a pile; $R_2$ a 2-pile | cut at $y = 2$ (L6) | |
| $[2, 6] \times [0, 2]$ | $R_1$ a 1-pile $[2, 4]$; $R_2$ a 2-pile $[1, 2]$ | trellis: $8 - (4 - 2)(2 - 1)$ | $6$ |
| $[2, 6] \times [2, 3]$ | $R_2$ covers the cell | covered | $4$ |

The total is $4 + 6 + 4 = 14$, which equals $8 + 8 - 2$, the two areas minus the overlap $[2, 4] \times [1, 2]$. In the first cut the inner values in $x$ of the boxes that are not piles are $2$ and $4$, and the lower median is $2$; in the right cell only $R_1$ is not a pile, and the depth is $1$, so the rule cuts in $y$ at its inner value $2$. With the third rectangle $[1, 3] \times [-1, 4]$ the same code gives $19$, as on the problem page.

## Correctness

Let $U = \bigcup_i B_i$. The cut of line L7 splits $C$ into two cells whose common face has volume $0$, so $\operatorname{vol}(U \cap C) = \operatorname{vol}(U \cap C^-) + \operatorname{vol}(U \cap C^+)$, which is line L8. Line L1 drops only sets of volume $0$ and parts outside $C$. Line L2 is right because $U \cap C = C$. In line L5, a box that is a $j$-pile and also a $k$-pile with $k \ne j$ covers $C$, which line L2 excludes, so each pile has one coordinate, and the trellis formula holds. Every box that is neither a pile nor covering has inner values in at least two coordinates, so line L6 finds a cut, and the number of distinct inner values drops in both children, so the recursion ends. The full proof is in the proof file.

## Complexity

For the Overmars-Yap partition the time is $O(n^{d/2} \log n)$ and the space is $O(n)$ for $d \ge 3$. Their analysis bounds the number of cells by $O(n^{d/2})$ and runs a sweep over one coordinate through the cells of a partition of the other coordinates, keeping each trellis measure in a search structure so that each insertion or deletion of a pile costs $O(\log n)$. For the median rule of the implementation, the depth is at most $2 d n$, since each cut removes one of at most $2n$ inner values per coordinate, and each cell costs $O(d\, n \log n)$; the number of cells is not bounded by $O(n^{d/2})$ in general.

## Properties

- **Exact.** All quantities are sums and products of coordinate differences, so integer input gives the exact integer volume.
- **Local.** Each cell needs only the boxes that meet it, which also gives a natural parallel version.
- **Any cut rule is correct.** Correctness needs only that each cut uses an inner value of a box that is not a pile; the rule affects only the running time.
- **Low space.** The sweep version of Overmars and Yap uses $O(n)$ space, which is less than the grid method.

## Variants and improvements

- **Chan's simplification.** Chan (2013) uses a plain divide and conquer that cuts at weighted medians and simplifies the boxes that become slabs in a cell, which gives $O(n^{d/2})$ time, removing the log factor, with a much simpler analysis.
- **Depth and coverage.** The same cell approach adapts to the largest depth of the boxes and to the volume covered at least $k$ times.
- **Special boxes.** For cubes, unit cubes and boxes with a common corner, the partition idea leads to faster bounds.
- **Grid method.** Without a partition, [coordinate compression](/coordinate-compression/) and a scan of all $(2n)^d$ cells give $O(n^d)$ time, which is the brute force of the tests.

## When to use it

Use the trellis method for the union volume in three or more dimensions when $n$ is large and an $O(n^{d-1} \log n)$ sweep is too slow. In the plane use the [segment tree sweep](/area-of-union-of-rectangles/) instead. For small $n$ in any dimension, the grid method or inclusion and exclusion over few boxes is simpler, and for boxes in high dimension with many overlaps, randomized estimation of the volume by sampling is often the practical choice.

## Pitfalls

- **Counting a box twice in line L5.** A box that covers the cell is a pile in every coordinate; line L2 must handle it before the trellis formula, or it adds to all $U_j$ at once.
- **A cut at a non-inner value in line L6.** A cut at the cell boundary gives an empty child and the same cell again, so the recursion does not end.
- **Cutting on piles.** The inner values of piles do not need cuts; cutting on them only multiplies the cells.
- **Flat boxes in line L1.** Boxes of volume $0$ add nothing but can be inner values forever; drop them.
- **Overlapping intervals in line L4.** $U_j$ is the length of the union of the pile intervals, not their sum.

## Implementations

## History

Klee asked in 1977 about the one-dimensional case, and the sweep with segment trees gave $O(n^{d-1} \log n)$ for $d \ge 2$ by the work of Bentley and of van Leeuwen and Wood. Overmars and Yap introduced piles, trellises and the balanced partition at FOCS 1988, with the journal version in 1991, and obtained $O(n^{d/2} \log n)$ time and $O(n)$ space. Chan improved the bound to $O(n^{d/2} 2^{O(\log^* n)})$ in 2010 and to $O(n^{d/2})$ in 2013, with a simpler divide and conquer.

## References
