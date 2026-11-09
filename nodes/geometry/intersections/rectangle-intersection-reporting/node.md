---
tag: 4VFM9M
kind: problem
slug: rectangle-intersection-reporting
name: Rectangle intersection reporting
aliases: [rectangle-overlap-reporting, reporting intersecting rectangles, box overlap reporting]
area: geometry/intersections
level: core
summary: Report every pair of overlapping axis-parallel rectangles among n rectangles; a sweep with an interval tree, or edge crossings plus point enclosure, solves it in Θ(n log n + k) time.
prereqs: [orthogonal-segment-intersection, rectangle-intersection-detection, axis-aligned-bounding-box, interval-tree]
see_also: [orthogonal-segment-intersection-sweep, rectangle-intersection-sweep, segment-tree, interval-overlap-query, area-of-union-of-rectangles, klee-measure-problem, collision-detection, bounding-volume-hierarchy]
sources:
  - paper: doi:10.1109/TC.1980.1675628
    title: Jon L. Bentley and Derick Wood, An optimal worst case algorithm for reporting intersections of rectangles, IEEE Transactions on Computers C-29(7), 1980, 571-577
    locator: the O(n log n + k) algorithm, by segment intersection for crossing edges and a segment tree for containment
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 8, The Geometry of Rectangles (intersection of rectangles and the related problems)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 10, Sections 10.1 and 10.3 (interval trees and segment trees, the structures used by the sweep)
  - paper: doi:10.1016/0196-6774(81)90027-4
    title: Jan van Leeuwen and Derick Wood, The measure problem for rectangular ranges in d-space, Journal of Algorithms 2(3), 1981, 282-300
    locator: rectangle problems in d dimensions solved by sweeping with segment trees
---

Rectangle intersection reporting asks for every pair of overlapping rectangles among $n$ axis-parallel rectangles in the plane. Two rectangles overlap exactly when their $x$-intervals overlap and their $y$-intervals overlap, so the problem is about intervals on two axes. A sweep over $x$ that keeps the $y$-intervals of the active rectangles in an [interval tree](/interval-tree/) reports the $k$ pairs in $\Theta(n \log n + k)$ time, which is optimal; Bentley and Wood (1980) gave the first optimal method, by [orthogonal segment intersection](/orthogonal-segment-intersection/) plus point enclosure.

## In plain words

You have many rectangular boxes drawn on a page, all with sides parallel to the edges of the page. Which pairs of boxes overlap?

Two boxes overlap when their shadows on the bottom edge overlap and their shadows on the side edge also overlap. Sweep a line from left to right. A box is active while the line is over it. When a new box starts, every active box already overlaps it from left to right, so you only need the active boxes whose side shadows overlap the side shadow of the new box. A good search structure for intervals finds these quickly, with a little work for each pair found.

## Definition

**Input.** A list of $n$ closed axis-parallel rectangles $r_i = [a_i, b_i] \times [c_i, d_i]$ with $a_i \le b_i$ and $c_i \le d_i$. Rectangles of zero width or height are allowed.

**Output.** Every pair $\{i, j\}$, $i \ne j$, with $r_i \cap r_j \ne \emptyset$, which holds if and only if $a_i \le b_j$, $a_j \le b_i$, $c_i \le d_j$ and $c_j \le d_i$. The number of pairs is $k$.

**Closed or open.** With closed rectangles, two rectangles that share only a side or a corner overlap. Many applications use open rectangles, where touching does not count; this changes $\le$ to $<$ in the test and the tie order of the events in a sweep.

**Model.** Only comparisons of coordinates are needed, so the result is exact for any ordered number type. Lower bounds use the [algebraic decision tree](/algebraic-decision-tree/).

## Variants

- **Detection.** Decide whether any two rectangles overlap: [rectangle intersection detection](/rectangle-intersection-detection/), in $\Theta(n \log n)$ time with the [rectangle intersection sweep](/rectangle-intersection-sweep/).
- **Edge crossings only.** Report pairs whose boundaries cross; this is [orthogonal segment intersection](/orthogonal-segment-intersection/) on the $4n$ edges.
- **Containment pairs.** Report the pairs where one rectangle contains another; a point-enclosure problem for the corners.
- **Red-blue.** Report overlaps between a red set and a blue set only, for example between the parts of two layers of a chip.
- **Union and measure.** The [area of a union of rectangles](/area-of-union-of-rectangles/), and in $d$ dimensions the [Klee measure problem](/klee-measure-problem/), need no pairs and have their own sweeps.
- **Boxes in $d$ dimensions.** Report overlapping pairs of axis-parallel boxes in $\mathbb{R}^d$; with a sweep and segment trees nested $d - 1$ levels, $O(n \log^{d-1} n + k)$ time.
- **Online version.** Keep a set of rectangles under insertions and deletions and report the overlaps of a query rectangle: an [interval tree](/interval-tree/) for one axis with a second level, or a [range tree](/range-tree/) on the corners.

## Examples

**Four rectangles.** Take $r_0 = [0, 4] \times [0, 3]$, $r_1 = [2, 6] \times [1, 5]$, $r_2 = [1, 2] \times [1, 2]$ and $r_3 = [5, 7] \times [4, 6]$. The overlapping pairs are $\{0, 1\}$, where edges cross, $\{0, 2\}$, where $r_2$ lies inside $r_0$ and no edges cross, $\{1, 2\}$, which touch along the side $x = 2$, and $\{1, 3\}$, whose sides cross near their corners. The pairs $\{0, 3\}$ and $\{2, 3\}$ do not overlap, so $k = 4$. The pair $\{0, 2\}$ shows why edge crossings alone are not enough.

**Quadratic output.** $n$ rectangles that all contain the point $(0, 0)$ give $k = \binom{n}{2}$.

**No pair.** $n$ unit squares placed side by side with gaps give $k = 0$; the sweep takes $O(n \log n)$ time and the test of all pairs takes $\Theta(n^2)$.

## Known algorithms

| algorithm | time | space | idea |
| --- | --- | --- | --- |
| all pairs | $\Theta(n^2)$ | $O(1)$ | four comparisons per pair |
| Bentley and Wood, 1980 | $\Theta(n \log n + k)$ | $O(n \log n)$ | crossing edges by the [orthogonal sweep](/orthogonal-segment-intersection-sweep/), containment by point enclosure in a [segment tree](/segment-tree/) |
| sweep with an [interval tree](/interval-tree/) | $\Theta(n \log n + k)$ | $\Theta(n)$ | at the left side of a rectangle, report the active $y$-intervals that overlap its own, then insert it |
| sort and scan on one axis | $O(n \log n + k')$ | $O(n)$ | report the $k' \ge k$ pairs whose $x$-intervals overlap, then filter by $y$; simple but not output-sensitive in $k$ |
| [bounding volume hierarchy](/bounding-volume-hierarchy/) or uniform grid | no good worst case | $O(n)$ | used in practice for many objects of similar size |

The interval-tree sweep is the usual method. The events are the left and right sides, sorted by $x$, with left sides before right sides at equal $x$ for closed rectangles. At a left side $[c, d]$, the interval tree reports all stored intervals $[c', d']$ with $c' \le d$ and $c \le d'$ in $O(\log n + m)$ time for $m$ answers.

## Bounds

- **Lower bound.** $\Omega(n \log n + k)$ in the algebraic decision tree model: $\Omega(k)$ for the output, and $\Omega(n \log n)$ even for detection, by a reduction from [element distinctness](/element-distinctness/).
- **Upper bound.** $O(n \log n + k)$ time and $O(n)$ space, by the interval-tree sweep.
- **Integer coordinates.** On a word RAM with small integer coordinates, the sort and the interval structure can be replaced by faster integer structures.

## Reductions

- **Overlap means crossing or containment.** Two rectangles overlap if and only if a side of one meets a side of the other, or one contains a corner of the other; Bentley and Wood use this split.
- **From element distinctness.** For numbers $x_1, \dots, x_n$, the degenerate rectangles $[x_i, x_i] \times [0, 1]$ overlap exactly when two numbers are equal.
- **To orthogonal range searching.** The pair $r_i, r_j$ overlaps exactly when the point $(a_j, b_j, c_j, d_j)$ lies in the 4-dimensional orthant $a \le b_i$, $b \ge a_i$, $c \le d_i$, $d \ge c_i$; so each rectangle is one query of [orthogonal range reporting](/orthogonal-range-reporting/) in four dimensions.

## Applications

- **Collision detection, broad phase.** [Axis-aligned bounding boxes](/axis-aligned-bounding-box/) of moving objects are tested for overlap, and only the overlapping pairs go to an exact test; see [collision detection](/collision-detection/).
- **VLSI design rule checks.** Find overlapping or too-close parts of a chip layout, after growing each rectangle by the minimum distance.
- **Databases and GIS.** A spatial join of two tables of bounding boxes reports the pairs of overlapping boxes.
- **Windowing systems.** Find which windows on a screen overlap.

## References
