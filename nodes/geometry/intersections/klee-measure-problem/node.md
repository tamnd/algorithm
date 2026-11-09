---
tag: JDZW0X
kind: problem
slug: klee-measure-problem
name: Klee's measure problem
aliases:
- union-volume-of-boxes
- measure of a union of boxes
area: geometry/intersections
level: advanced
summary: Compute the volume of the union of n axis-parallel boxes in d dimensions; Θ(n log n) for d of 1 and 2, and O(n^(d/2)) for d of 3 or more.
prereqs: [area-of-union-of-rectangles, interval-union-length]
see_also: [overmars-yap-algorithm, segment-tree, sweep-line-technique, rectangle-intersection-reporting, coordinate-compression, algebraic-decision-tree, axis-aligned-bounding-box, orthogonal-range-reporting]
sources:
  - paper: doi:10.2307/2318871
    title: Victor Klee, Can the measure of the union of intervals be computed in less than O(n log n) steps?, American Mathematical Monthly 84(4), 1977
    locator: the question for n intervals on the line, and the remark on the same problem for boxes in higher dimensions
  - paper: doi:10.1145/359545.359553
    title: Michael L. Fredman and Bruce Weide, On the complexity of computing the measure of the union of intervals, Communications of the ACM 21(7), 1978
    locator: the Omega(n log n) lower bound for the union length of n intervals in the linear decision tree model
  - paper: doi:10.1016/0196-6774(81)90027-4
    title: Jan van Leeuwen and Derick Wood, The measure problem for rectangular ranges in d-space, Journal of Algorithms 2(3), 1981
    locator: the sweep with segment trees in the plane and the recursive method for d dimensions with less space
  - paper: doi:10.1137/0220065
    title: Mark H. Overmars and Chee-Keng Yap, New upper bounds in Klee's measure problem, SIAM Journal on Computing 20(6), 1991
    locator: the O(n^(d/2) log n) time bound for d of 3 or more by a partition of space into trellis cells
  - paper: doi:10.1109/FOCS.2013.51
    title: Timothy M. Chan, Klee's measure problem made easy, FOCS 2013
    locator: the O(n^(d/2)) algorithm for d of 3 or more by a simplified divide and conquer, and the faster bounds for special cases
---

Klee's measure problem asks for the volume of the union of $n$ axis-parallel boxes in $\mathbb{R}^d$. Overlaps must be counted once, so the sum of the volumes is not the answer, and inclusion and exclusion has $2^n$ terms. Victor Klee asked in 1977 whether the one-dimensional case, the total length of a union of intervals, needs $\Omega(n \log n)$ time; Fredman and Weide proved that it does. In the plane a sweep with a segment tree takes $O(n \log n)$ time, and for $d \ge 3$ the best bound is $O(n^{d/2})$, found by Overmars and Yap up to a log factor and by Chan in 2013.

## In plain words

You have many rectangles on a sheet of paper, and they overlap. You want the total area that they cover. Adding up the areas of the rectangles counts the overlaps two or more times, so it gives too much. The same question in three or more dimensions is about boxes and their volume.

On a line the rectangles become intervals, and you sort the end points and walk from left to right. In the plane you sweep a vertical line across the rectangles and keep track of how much of the line is covered. In higher dimensions the problem gets much harder, and the best methods cut space into cells where the boxes look simple.

## Definition

**Input.** $n$ boxes $B_i = [a_{i,1}, b_{i,1}] \times \dots \times [a_{i,d}, b_{i,d}]$ in $\mathbb{R}^d$, with $a_{i,j} \le b_{i,j}$.

**Output.** The $d$-dimensional volume $\operatorname{vol}\big(\bigcup_{i=1}^n B_i\big)$.

**Notation.** $d$ is a fixed dimension, and the bounds hide factors that depend only on $d$. For $d = 1$ the boxes are intervals, and for $d = 2$ they are rectangles.

**Model.** The [real RAM](/real-ram/) for the upper bounds; the lower bound holds in the [algebraic decision tree](/algebraic-decision-tree/) model. With integer coordinates the volume is an exact integer.

## Variants

- **Length of a union of intervals.** The case $d = 1$, solved by sorting; see [interval union length](/interval-union-length/).
- **Area of a union of rectangles.** The case $d = 2$, solved by a sweep; see [area of union of rectangles](/area-of-union-of-rectangles/).
- **Perimeter and contour.** The perimeter of the union of rectangles and the boundary polygons, also by a sweep in $O(n \log n)$, plus the output size for the contour.
- **Depth and coverage.** The largest number of boxes over one point, or the volume covered at least $k$ times; the methods for the measure adapt to these.
- **Special boxes.** Cubes, unit cubes, and boxes with a common corner have faster algorithms. Boxes that all contain a common corner of the space give the hypervolume indicator of multi-objective optimization.
- **Discrete version.** Count the grid points in the union, or the weighted union over a grid; with [coordinate compression](/coordinate-compression/) this is the same problem.

## Examples

**Intervals.** $[1, 3], [2, 5], [6, 7]$: after sorting, $[1, 3]$ and $[2, 5]$ merge to $[1, 5]$, so the union length is $4 + 1 = 5$, while the sum of lengths is $6$.

**Rectangles.** $R_1 = [0, 4] \times [0, 2]$, $R_2 = [2, 6] \times [1, 3]$ and $R_3 = [1, 3] \times [-1, 4]$, with areas $8 + 8 + 10 = 26$. The distinct $x$-values $0, 1, 2, 3, 4, 6$ cut the plane into vertical slabs, and in each slab the covered length of the sweep line is a union of intervals:

| slab | boxes over the slab | covered $y$-length | area |
| --- | --- | --- | --- |
| $[0, 1]$ | $R_1$ | $2$ | $2$ |
| $[1, 2]$ | $R_1, R_3$ | $5$ | $5$ |
| $[2, 3]$ | $R_1, R_2, R_3$ | $5$ | $5$ |
| $[3, 4]$ | $R_1, R_2$ | $3$ | $3$ |
| $[4, 6]$ | $R_2$ | $2$ | $4$ |

The union has area $19$, which a brute-force count over the $5 \times 5$ grid of compressed cells confirms.

## Known algorithms

**Inclusion and exclusion.** $\sum_{\emptyset \ne S} (-1)^{|S| + 1} \operatorname{vol}(\bigcap_{i \in S} B_i)$, since an intersection of boxes is a box. This is exact but takes $O(2^n d)$ time.

**Grid.** After [coordinate compression](/coordinate-compression/) there are fewer than $(2n)^d$ cells, and a cell is covered or not; marking takes $O(n^{d+1})$ time naively, or $O(n^d)$ with prefix sums of the box counts.

**Sorting for $d = 1$.** Sort the $2n$ end points and walk with a counter of open intervals, in $O(n \log n)$ time.

**Sweep for $d = 2$.** Bentley (1977) sweeps a vertical line and keeps the covered length in a [segment tree](/segment-tree/) over the compressed $y$-values; each node stores a cover count and the covered length of its range, and each event updates $O(\log n)$ nodes. The total is $O(n \log n)$ time and $O(n)$ space.

**Sweep and recursion for $d \ge 3$.** Sweeping one coordinate and solving the $(d-1)$-dimensional problem at each event gives $O(n^{d-1} \log n)$ time; van Leeuwen and Wood (1981) reduced the space of this approach.

**Trellis partition.** [Overmars and Yap](/overmars-yap-algorithm/) (1991) partition space into $O(n^{d/2})$ cells such that inside each cell every box that meets it, but does not contain it, is a slab in one coordinate; the union of such boxes in a cell, called a trellis, has a measure that is easy to compute. With a sweep over one coordinate this gives $O(n^{d/2} \log n)$ time and $O(n)$ space.

**Chan's simplification.** Chan (2013) replaces the partition by a simpler divide and conquer with a weight-balanced cut and simplification of the boxes in each piece, which gives $O(n^{d/2})$ time for $d \ge 3$.

## Bounds

For $d = 1$, Fredman and Weide (1978) proved $\Omega(n \log n)$ in the linear decision tree model. The union of the intervals $[x_i, x_i + 1]$ has length $n$ exactly when $|x_i - x_j| \ge 1$ for all $i \ne j$, and this set of inputs has $n!$ connected components, one for each order of the $x_i$, as in the proof for [element distinctness](/element-distinctness/). The bound extends to the algebraic decision tree by Ben-Or's theorem, and to every $d \ge 1$ by taking boxes of unit width in the other coordinates. So the problem is $\Theta(n \log n)$ for $d = 1$ and $d = 2$. For $d \ge 3$ the gap between $\Omega(n \log n)$ and $O(n^{d/2})$ is open; Chan showed by a reduction from the clique problem that the problem is W[1]-hard when $d$ is part of the input, so a bound of the form $f(d) \cdot n^{c}$ with a fixed $c$ is unlikely.

## Reductions

- **From the unit gap problem.** "Are $n$ numbers pairwise at distance at least $1$?" is the question whether the union of $[x_i, x_i + 1]$ has length $n$, which gives the lower bound.
- **To a sweep of $(d - 1)$-dimensional problems.** The volume is the integral over $x_1$ of the $(d-1)$-dimensional measure of the cross section, which is constant between consecutive events.
- **To union of orthants.** The hypervolume indicator is the special case where all boxes share one corner.
- **To depth problems.** Volume covered at least once is $\operatorname{vol}(\text{space}) - \operatorname{vol}(\text{depth } 0)$, so measure and depth algorithms often share their structure.

## Applications

- **VLSI and layout.** The area covered by a set of rectangular masks or cells, and the contour of the covered region.
- **Databases.** The volume covered by a set of range queries, used for selectivity and caching.
- **Multi-objective optimization.** The hypervolume indicator measures the quality of a set of solutions by the volume of the union of boxes they dominate.
- **Image processing.** The area of a union of bounding boxes in an image, for example of detected objects.

## References
