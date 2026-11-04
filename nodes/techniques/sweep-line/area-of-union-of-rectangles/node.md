---
tag: 5B1BEQ
kind: problem
slug: area-of-union-of-rectangles
name: Area of union of rectangles
aliases:
- union of rectangles
- rectangle union area
area: techniques/sweep-line
level: core
summary: Compute the area covered by the union of n axis-parallel rectangles.
prereqs: [sweep-line-technique, coordinate-compression]
see_also: [rectangle-union-sweep, klee-measure-problem, segment-tree, rectangle-intersection-detection, skyline-problem, algebraic-decision-tree]
sources:
  - paper: "M. L. Fredman and B. Weide, On the complexity of computing the measure of the union of intervals, Communications of the ACM 21(7) (1978), doi:10.1145/359545.359553"
    locator: pages 540 to 544 (the Omega(n log n) lower bound in the decision tree model with linear comparisons)
  - paper: "V. Klee, Can the measure of the union of intervals be computed in less than O(n log n) steps?, The American Mathematical Monthly 84(4) (1977), doi:10.1080/00029890.1977.11994336"
    locator: pages 284 to 285
  - paper: "J. L. Bentley, Algorithms for Klee's rectangle problems, unpublished notes, Computer Science Department, Carnegie Mellon University (1977)"
    locator: the O(n log n) sweep in the plane and O(n^(d-1) log n) in d dimensions
  - paper: "T. M. Chan, Klee's measure problem made easy, 54th IEEE Symposium on Foundations of Computer Science (2013), doi:10.1109/FOCS.2013.51"
    locator: pages 410 to 419 (the O(n^(d/2)) bound for d at least 3, and a survey of earlier bounds)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction
    locator: Chapter 8, The Geometry of Rectangles (measure and perimeter of a union of rectangles)
---

The area of union of rectangles problem asks for the area that $n$ axis-parallel rectangles cover together, with each point counted once however many rectangles cover it. It is the planar case of [Klee's measure problem](/klee-measure-problem/). It takes $\Theta(n \log n)$ time: [Bentley's sweep](/rectangle-union-sweep/) gives the upper bound, and Fredman and Weide's bound for the one-dimensional case gives the lower bound in a decision tree model with linear tests.

## In plain words

Lay some rectangular sheets of paper on a table. They may overlap. How much of the table do they cover? Adding the areas of the sheets counts the overlaps more than once. Subtracting the overlaps of pairs, then adding back the triple overlaps, and so on, gets out of hand quickly.

A better way is to cut the table into narrow vertical strips at each left or right edge of a sheet. Inside one strip, the sheets cover the same heights all the way across, so the covered area of the strip is the strip width times the covered height. The work is then to keep the covered height up to date as you move from strip to strip. A tree over the sorted heights does this fast, and the whole job costs about as much as sorting.

## Definition

**Input.** A list of $n \ge 0$ rectangles $R_i = [a_i, b_i] \times [c_i, d_i]$ with real coordinates, $a_i \le b_i$ and $c_i \le d_i$.

**Output.** The area of their union,

$$\mu\Big(\bigcup_{i=1}^{n} R_i\Big) = \int_{-\infty}^{\infty} \Big|\bigcup_{i \,:\, a_i \le x \le b_i} [c_i, d_i]\Big| \, dx,$$

where $\mu$ is the area (Lebesgue measure) and $|\cdot|$ is length. The equality is Fubini's theorem: the area is the integral of the length of the vertical section at $x$. Open and closed rectangles give the same area, because their boundaries have area 0.

**Inclusion and exclusion.** The area also equals $\sum_{\emptyset \ne S \subseteq \{1, \ldots, n\}} (-1)^{|S|+1} \mu\big(\bigcap_{i \in S} R_i\big)$, and each intersection of rectangles is a rectangle or empty. This formula has $2^n - 1$ terms, so it is useful only for very small $n$ or as a check.

## Variants

- **Length of a union of intervals.** The one-dimensional case: $\big|\bigcup_i [a_i, b_i]\big|$. Sort the intervals by left end and merge them in one pass: $O(n \log n)$ time.
- **Klee's measure problem.** The volume of a union of $n$ boxes in $\mathbb{R}^d$. See [Klee's measure problem](/klee-measure-problem/).
- **Perimeter of the union.** The length of the boundary of the union. A sweep with a segment tree also solves it in $O(n \log n)$ time.
- **Coverage at least $k$.** The area of the set of points covered by at least $k$ rectangles. For $k = 1$ this is the union.
- **Maximum depth.** The largest number of rectangles that share a point. A sweep with a segment tree for range add and range maximum gives it in $O(n \log n)$ time.
- **Grid cells.** With integer coordinates and unit cells, count the cells covered. This is the same number as the area.
- **Rectangles on a baseline.** If each $c_i = 0$, the union is the region under the [skyline](/skyline-problem/), and its area is the integral of the skyline function.

## Examples

**Three rectangles.** $R_1 = [1, 4] \times [1, 3]$ (area 6), $R_2 = [2, 6] \times [2, 5]$ (area 12) and $R_3 = [5, 7] \times [0, 2]$ (area 4). Only $R_1 \cap R_2 = [2, 4] \times [2, 3]$ has positive area, 2. The area of the union is $6 + 12 + 4 - 2 = 20$. The area covered at least twice is 2. The union's boundary has length 24. The table of the strips is on the page of [the sweep](/rectangle-union-sweep/).

**A cross.** $[0, 10] \times [4, 5]$ and $[4, 5] \times [0, 10]$ have area 10 each and share the unit square $[4, 5] \times [4, 5]$. The union has area 19.

**Nested and equal.** $[0, 10] \times [0, 10]$ and $[2, 3] \times [2, 3]$ give 100. Two copies of the same rectangle give its area once.

**Intervals.** The union of $[1, 3]$, $[2, 5]$ and $[7, 8]$ is $[1, 5] \cup [7, 8]$, of length 5.

## Known algorithms

- **Inclusion and exclusion.** $O(2^n n)$ time. Only for tiny inputs.
- **Grid over compressed coordinates.** [Compress](/coordinate-compression/) the $x$- and $y$-coordinates to at most $2n$ values each, and mark the grid cells that each rectangle covers. This is $O(n^3)$ time with direct marking, or $O(n^2)$ time and space with a two-dimensional difference array. Simple and exact, and a good test oracle.
- **Sweep with a sorted list per strip.** Sweep over $x$, and at each strip compute the covered length by sorting and merging the active $y$-intervals: $O(n^2 \log n)$ time, or $O(n^2)$ if the active intervals are kept sorted.
- **[Bentley's rectangle union sweep](/rectangle-union-sweep/).** Sweep over $x$ with a [segment tree](/segment-tree/) over the compressed $y$-coordinates that keeps the covered length: $O(n \log n)$ time and $O(n)$ space.

## Bounds

**Upper bound.** $O(n \log n)$ worst-case time on a [real RAM](/real-ram/), by Bentley's sweep (1977).

**Lower bound.** Fredman and Weide (1978) proved that computing the length of a union of $n$ intervals needs $\Omega(n \log n)$ steps in the worst case in the decision tree model, even when each test compares two linear functions of the interval ends. The planar problem contains the one-dimensional one: the rectangles $[a_i, b_i] \times [0, 1]$ have a union of area $\big|\bigcup_i [a_i, b_i]\big|$. So the planar problem has the same lower bound in that model, and $\Theta(n \log n)$ is tight. Klee (1977) had asked whether the one-dimensional problem can be solved in fewer than $O(n \log n)$ steps; this lower bound answers his question in that model.

**Higher dimensions.** For $d \ge 3$, the best known algorithm takes $O(n^{d/2})$ time (Chan 2013), and no matching lower bound is known. See [Klee's measure problem](/klee-measure-problem/).

## Reductions

- **From the length of a union of intervals**, in $O(n)$ time, as above.
- **To Klee's measure problem** in any dimension $d \ge 2$, by giving each rectangle the extent $[0, 1]$ in each extra dimension.
- **Coverage depth and union.** The union area is the area where the depth is at least 1. A structure that keeps, for each part of the line, the number of rectangles that cover it solves both. Bentley's sweep keeps only whether the count is positive, in a form that needs no lazy updates.

## Applications

- **Chip layout.** The total area of a layer of a circuit layout is the area of a union of rectangles, and so is the area of the parts that two layers share.
- **Maps and images.** The area covered by a set of bounding boxes, for example of buildings or of detected objects, and the coverage of a region by sensors with rectangular range.
- **Databases.** The volume of a union of query boxes, in the analysis of range queries.
- **Programming contests.** The planar union area, the perimeter and the "covered at least $k$ times" variants are standard exercises for the segment tree sweep.

## References
