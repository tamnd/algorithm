---
tag: KBCKNR
kind: problem
slug: orthogonal-segment-intersection
name: Orthogonal segment intersection
aliases: [horizontal and vertical segment intersection, horizontal-vertical-segment-intersection, rectilinear segment intersection]
area: geometry/intersections
level: core
summary: Report every pair of a horizontal and a vertical segment that meet, among n axis-parallel segments; a sweep with a one-dimensional range query solves it in Θ(n log n + k) time.
prereqs: [all-segment-intersections, orthogonal-range-reporting]
see_also: [orthogonal-segment-intersection-sweep, rectangle-intersection-reporting, bentley-ottmann-algorithm, segment-tree, range-tree, fenwick-tree, interval-union-length, element-distinctness]
sources:
  - paper: doi:10.1109/TC.1979.1675432
    title: Jon L. Bentley and Thomas A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9), 1979, 643-647
    locator: the rectilinear case (reporting in O(n log n + k) time and counting in O(n log n) time)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 8, The Geometry of Rectangles (intersections of orthogonal segments)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 10, More Geometric Data Structures (interval trees and segment trees, with windowing queries on axis-parallel segments)
---

Orthogonal segment intersection asks for every pair of a horizontal and a vertical segment that meet, in a set of $n$ axis-parallel segments. It is the special case of [reporting all segment intersections](/all-segment-intersections/) that appears in circuit layout and in the geometry of rectangles. Since the order of horizontal segments by height never changes, a sweep needs no crossing events, and the [orthogonal segment intersection sweep](/orthogonal-segment-intersection-sweep/) reports the $k$ pairs in optimal $\Theta(n \log n + k)$ time with only comparisons of coordinates.

## In plain words

Think of a street map where every street runs east-west or north-south. Which pairs of streets cross or touch?

A north-south street meets an east-west street when the east-west street is at a height inside the range of the north-south one and the north-south street is at a position inside the range of the east-west one. So the question is about intervals and points on two axes, and no arithmetic is needed beyond comparisons. Sweeping a line from west to east and keeping the active east-west streets sorted by height, each north-south street asks which active heights fall in its range. That is a sorted-list search plus one step per answer.

## Definition

**Input.** A list $H$ of horizontal segments $h = [x_1(h), x_2(h)] \times \{y(h)\}$ and a list $V$ of vertical segments $v = \{x(v)\} \times [y_1(v), y_2(v)]$, closed, with $n = |H| + |V|$. End points can be equal, and segments of length zero are allowed.

**Output.** Every pair $(h, v) \in H \times V$ with $x_1(h) \le x(v) \le x_2(h)$ and $y_1(v) \le y(h) \le y_2(v)$. These are exactly the pairs that meet, at the point $(x(v), y(h))$. The number of pairs is $k \le |H| \cdot |V|$.

**What is not included.** Two horizontal segments on one line can overlap, and so can two vertical ones. These pairs are a one-dimensional interval problem on each line: sort the segments of the line by left end and report overlaps with the active ones, in $O(m \log m + k')$ time for $m$ segments and $k'$ pairs. Most texts leave them out.

**Model.** The [real RAM](/real-ram/), or any model with comparisons of coordinates; no arithmetic is needed, so the solution is exact for integers, rationals and floating-point numbers alike. Lower bounds use the [algebraic decision tree](/algebraic-decision-tree/).

## Variants

- **Counting.** Compute $k$ only, in $O(n \log n)$ time for any $k$: replace each range report by a range count, two prefix sums in a [Fenwick tree](/fenwick-tree/).
- **Detection.** Decide whether $k > 0$, in $O(n \log n)$ time.
- **Segments in a fixed set of directions.** For segments in $c$ directions, shear the plane for each pair of directions and run the method $O(c^2)$ times.
- **Rectangles.** Report the pairs of overlapping axis-parallel rectangles: [rectangle intersection reporting](/rectangle-intersection-reporting/). Their crossing edges are an instance of this problem.
- **Windowing queries.** Preprocess $H$ so that a query rectangle or a query vertical segment reports the horizontal segments it meets; this is the data-structure version, solved with [segment trees](/segment-tree/) or [interval trees](/interval-tree/) plus a [range tree](/range-tree/) in $O(\log^2 n + k)$ time per query.
- **Higher dimensions.** Report the pairs of axis-parallel boxes that meet, or of axis-parallel segments in $\mathbb{R}^d$.

## Examples

**Eight segments.** Take $h_0$: $y = 1$, $x \in [0, 6]$; $h_1$: $y = 3$, $x \in [2, 9]$; $h_2$: $y = 5$, $x \in [1, 4]$; $h_3$: $y = 3$, $x \in [7, 8]$, and $v_0$: $x = 2$, $y \in [0, 4]$; $v_1$: $x = 5$, $y \in [2, 6]$; $v_2$: the point $(8, 3)$; $v_3$: $x = 0$, $y \in [2, 9]$. The output is the $k = 5$ pairs $(h_0, v_0)$, $(h_1, v_0)$, $(h_1, v_1)$, $(h_1, v_2)$ and $(h_3, v_2)$. The pair $(h_1, v_0)$ meets at the end point $(2, 3)$ of $h_1$, a T-junction, and $v_2$ touches $h_1$ inside and $h_3$ at its right end. The [sweep](/orthogonal-segment-intersection-sweep/) page traces the events.

**Grid.** $m$ horizontal segments $[0, m] \times \{i\}$ and $m$ vertical segments $\{j\} \times [0, m]$ for $0 \le i, j < m$ give $k = m^2 = n^2/4$ pairs, so the $\Theta(k)$ output term can dominate.

**No pair.** If every vertical segment lies above all horizontal ones, $k = 0$, and the sweep takes $O(n \log n)$ time.

## Known algorithms

| algorithm | time | space | idea |
| --- | --- | --- | --- |
| all pairs | $\Theta(\lvert H \rvert \cdot \lvert V \rvert)$ | $O(1)$ | two comparisons per pair |
| [orthogonal sweep](/orthogonal-segment-intersection-sweep/) (Bentley and Ottmann, 1979) | $\Theta(n \log n + k)$ | $\Theta(n)$ | sweep in $x$, active horizontals ordered by $y$, a range query per vertical |
| [Bentley-Ottmann](/bentley-ottmann-algorithm/) on the same input | $O((n + k) \log n)$ | $O(n)$ | the general sweep; crossings become events |
| sort and distribute, divide and conquer | $O(n \log n + k)$ | $O(n)$ | split by $x$ and match the pieces that span a slab |

The sweep is the standard solution. Its status can be a [balanced binary search tree](/balanced-binary-search-tree/) with linked leaves, a [skip list](/skip-list/), or, since all $y$ values are known in advance, a [Fenwick tree](/fenwick-tree/) over the compressed $y$ values with a linked list of the used values, as in the implementation on the sweep page.

## Bounds

- **Lower bound.** $\Omega(n \log n + k)$ in the algebraic decision tree model. The $\Omega(k)$ part is the output. The $\Omega(n \log n)$ part holds even on inputs with $k = n$, by the reduction from [element distinctness](/element-distinctness/) below.
- **Upper bound.** $O(n \log n + k)$ time and $O(n)$ space, by the sweep.
- **Integer coordinates.** On a word RAM with coordinates in $\{1, \dots, U\}$, the comparisons can be replaced by integer sorting and a predecessor structure, and the $\Omega(n \log n)$ lower bound does not apply.

## Reductions

- **From element distinctness.** For numbers $x_1, \dots, x_n$, take the horizontal segments $h_i = [x_i, x_i] \times \{0\}$, of length zero, and the vertical segments $v_i = \{x_i\} \times [0, 1]$. Then $h_i$ meets $v_j$ exactly when $x_i = x_j$, so $k = n$ if the numbers are distinct and $k > n$ otherwise. An algorithm that reports or counts the pairs decides element distinctness, in $O(n)$ extra time.
- **To the general problem.** Every orthogonal instance is an instance of [all segment intersections](/all-segment-intersections/), but the general algorithms pay for arithmetic and for crossing events that this case does not need.
- **Inside rectangle reporting.** Two rectangles overlap if and only if an edge of one crosses an edge of the other, or one contains a corner of the other. So [rectangle intersection reporting](/rectangle-intersection-reporting/) is this problem plus point enclosure.

## Applications

- **VLSI design rule checks.** Wires on a chip run in two directions, and the check finds wires of one layer that touch.
- **Floor plans and maps.** Walls and streets in grid layouts.
- **Rectangle problems.** The sweep is the main step of rectangle intersection reporting and a model for the [area of a union of rectangles](/area-of-union-of-rectangles/).
- **Windowing in GIS.** Clip a map of axis-parallel features to a rectangular window.

## References
