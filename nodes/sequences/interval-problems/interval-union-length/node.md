---
tag: 65GCGD
kind: problem
slug: interval-union-length
name: Interval union length
aliases:
- Klee's measure problem in one dimension
- Total covered length of intervals
area: sequences/interval-problems
level: core
summary: Compute the total length of the union of a set of intervals.
prereqs: [interval-merging, sorting-problem]
see_also: [sweep-union-length, interval-merging-sort, klee-measure-problem, area-of-union-of-rectangles, maximum-overlap, segment-tree, algebraic-decision-tree]
sources:
  - paper: "Victor Klee, Can the measure of the union of intervals [a_i, b_i] be computed in less than O(n log n) steps?, American Mathematical Monthly 84(4) (1977), pages 284 to 285"
    locator: the question and the O(n log n) sorting algorithm
  - paper: "Michael L. Fredman and Bruce Weide, On the complexity of computing the measure of the union of intervals [a_i, b_i], Communications of the ACM 21(7) (1978), pages 540 to 544, doi:10.1145/359545.359553"
    locator: the Omega(n log n) lower bound in the linear decision tree model
  - url: https://cp-algorithms.com/geometry/length-of-segments-union.html
    title: cp-algorithms, Length of the union of segments
    locator: the sweep over sorted end points with a counter
---

Interval union length asks for the total length of the union of $n$ intervals on the real line, where the parts covered by several intervals count once. It is the one-dimensional case of [Klee's measure problem](/klee-measure-problem/). A sort of the $2n$ end points and one sweep solve it in $O(n \log n)$ time, and Fredman and Weide proved that $\Omega(n \log n)$ is necessary in the linear decision tree model. The answer does not depend on whether the end points are open or closed, but the count of covered integer points does.

## In plain words

Several painters paint parts of a long fence. Each painter tells you where they started and where they stopped. Some parts were painted by two or three painters. You want to know how many meters of fence have paint, and each meter counts once, however many painters worked on it.

Adding up the lengths of all the painted parts counts the overlaps too many times. Instead, walk along the fence from left to right and keep track of how many painters are working at the place where you stand. Each stretch where at least one painter is working counts, and each stretch where nobody is working does not.

## Definition

**Input.** A finite list of $n$ intervals $I_j$ with real end points $l_j \le r_j$, $1 \le j \le n$. Each $I_j$ may be closed $[l_j, r_j]$, open $(l_j, r_j)$ or half-open; the types may differ between intervals.

**Output.** The Lebesgue measure of the union,

$$ L = \lambda\Bigl(\bigcup_{j=1}^{n} I_j\Bigr) = \int_{-\infty}^{\infty} \mathbf{1}\bigl[c(x) \ge 1\bigr]\,dx, \qquad c(x) = \bigl|\{\, j : x \in I_j \,\}\bigr|. $$

The function $c$ is the *coverage*. A finite set of points has measure zero, so the type of each end point does not change $L$: $[1, 3] \cup [3, 5]$ and $(1, 3) \cup (3, 5)$ both have $L = 4$. A point interval $[x, x]$ adds 0. Equivalently, $L$ is the sum of the lengths of the components that [interval merging](/interval-merging/) returns.

**Discrete form.** For closed intervals of integers, the number of covered integers is

$$ N = \bigl|\{\, z \in \mathbb{Z} : z \in [l_j, r_j] \text{ for some } j \,\}\bigr|, $$

and here the type matters: $N$ for $[1, 3], [3, 5]$ is 5, not 6 and not 4. The reduction is $N = \lambda\bigl(\bigcup_j [l_j, r_j + 1)\bigr)$, since each covered integer $z$ owns the unit piece $[z, z + 1)$.

## Variants

- **Coverage at least $k$.** The measure of $\{x : c(x) \ge k\}$, the length covered by at least $k$ intervals. The same sweep solves it with the test $c \ge k$ instead of $c \ge 1$.
- **Exactly $k$, or a histogram.** The length covered exactly $k$ times, for each $k$, in one sweep.
- **Clipped to a window.** The length of the union inside a query range $[a, b]$; clip each interval first.
- **Dynamic.** Intervals are inserted and deleted, and the length is asked after each change. A [segment tree](/segment-tree/) over the sorted coordinates, where each node keeps a cover count and the covered length of its range, does each change in $O(\log n)$ time. This is the inner structure of the [area of a union of rectangles](/area-of-union-of-rectangles/).
- **Higher dimensions.** For boxes in $\mathbb{R}^d$ this is [Klee's measure problem](/klee-measure-problem/), which is much harder for $d \ge 3$.

## Examples

**Overlaps, touching and a point.** For $[1, 4], [7, 9], [2, 5], [9, 12], [8, 9], [14, 14]$ the union is $[1, 5] \cup [7, 12] \cup [14, 14]$, so

$$ L = (5 - 1) + (12 - 7) + 0 = 9, $$

while the sum of the lengths is $3 + 2 + 3 + 3 + 1 + 0 = 12$. The overlap $[2, 4]$ is counted once, the touching pair $[7, 9]$ and $[9, 12]$ joins without a gap, and the point $[14, 14]$ adds nothing.

**Open, closed and integers.** $L([1, 3] \cup [3, 5]) = L((1, 3) \cup (3, 5)) = 4$. As integer intervals, $[1, 3]$ and $[3, 5]$ cover $\{1, 2, 3, 4, 5\}$, so $N = 5$, and $[1, 3]$ and $[4, 5]$ also give $N = 5$ while $L = 2 + 1 = 3$.

**At least twice.** In the first example the length covered at least twice is $(4 - 2) + (9 - 8) = 3$: the pieces $[2, 4]$ and $[8, 9]$.

## Known algorithms

- **[Sweep for union length](/sweep-union-length/).** Sort the $2n$ end points and walk through them with a counter of open intervals; add each gap where the counter is positive. $O(n \log n)$ time, $O(n)$ space.
- **[Merge, then add](/interval-merging-sort/).** Merge the intervals by sorting by left end, then add the lengths of the components. $O(n \log n)$ time, and it sorts only $n$ keys.
- **Integer coordinates.** With integer end points in a range of size $O(n)$, sort with a counting sort, or add $+1$ and $-1$ to a difference array and take prefix sums, for $O(n + U)$ time where $U$ is the size of the range.
- **Dynamic segment tree.** $O(\log n)$ per insertion or deletion of an interval, when the coordinates are known in advance.

## Bounds

**Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/) plus subtractions and additions of coordinates, by the sweep.

**Lower bound.** Klee asked in 1977 whether the measure can be found in fewer than $O(n \log n)$ steps. Fredman and Weide (1978) answered no: in the linear decision tree model, where each test compares a linear function of the end points with 0, computing $L$ needs $\Omega(n \log n)$ tests in the worst case. So the sort-based algorithms are optimal in that model. A related $\Omega(n \log n)$ bound in the [algebraic decision tree](/algebraic-decision-tree/) model follows from element distinctness, for the count of components on the [interval merging](/interval-merging/) page.

## Reductions

- **To interval merging.** $L$ is the sum of the component lengths, $O(n)$ extra time.
- **Discrete to continuous.** The number of integers covered by closed integer intervals is the measure of the half-open intervals $[l_j, r_j + 1)$.
- **Inner step of the area of a union of rectangles.** A vertical sweep over $n$ rectangles keeps the union length of the active $y$-intervals, so the 2D area costs $O(n)$ union length queries, each in $O(\log n)$ time with the dynamic segment tree.

## Applications

- **Coverage of a genome or a timeline.** The number of bases covered by at least one read, or the total time during which at least one machine was busy.
- **Billing and monitoring.** Total time during which at least one session of a user was active, counting overlapping sessions once.
- **Geometry.** The one-dimensional step of the area and perimeter of a union of rectangles, and of the [skyline problem](/skyline-problem/).

## References
