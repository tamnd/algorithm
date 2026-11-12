---
tag: V3ZHMG
kind: algorithm
slug: offline-orthogonal-range-counting
name: Offline orthogonal range counting
aliases:
- sweep-line range counting with Fenwick tree
- batched orthogonal range counting
- offline 2D range counting
area: geometry/range-searching
level: core
summary: Sort the queries and points by one coordinate, sweep, and update a Fenwick tree on the other coordinate.
solves: [orthogonal-range-counting, dominance-counting]
model: real-ram
complexity:
  vars: {n: the number of points, q: the number of query boxes}
  time: {total: O((n + q) log(n + q)) worst case}
  space: {total: O(n + q) worst case}
properties: {online: false, deterministic: true, recursive: false, static: true}
history:
  year: 1980
  people: [Jon Louis Bentley, Peter M. Fenwick]
  note: Bentley solved batched dominance (ECDF) counting by sweeping and divide and conquer; Fenwick's 1994 tree became the usual counter for the sweep.
prereqs: [orthogonal-range-counting, fenwick-tree, sweep-line-technique]
see_also: [dominance-counting, coordinate-compression, offline-query-processing, inversion-count-with-fenwick-tree, range-tree, persistent-segment-tree, merge-sort-tree, wavelet-tree]
sources:
  - paper: doi:10.1145/358841.358850
    title: Jon Louis Bentley, Multidimensional divide-and-conquer, Communications of the ACM 23(4), 1980, pages 214 to 229
    locator: the all-points ECDF (dominance counting) problem solved in batch in O(n log^(d-1) n) time
  - paper: doi:10.1002/spe.4380240306
    title: Peter M. Fenwick, A new data structure for cumulative frequency tables, Software, Practice and Experience 24(3), 1994, pages 327 to 336
    locator: the binary indexed tree with O(log m) update and prefix sum (DOI to be checked)
  - paper: doi:10.1137/1.9781611973075.15
    title: Timothy M. Chan and Mihai Pătraşcu, Counting inversions, offline orthogonal range counting, and related problems, Proceedings of the 21st ACM-SIAM Symposium on Discrete Algorithms (SODA), 2010, pages 161 to 173
    locator: offline counting of n points and n boxes in O(n sqrt(log n)) time on the word RAM (DOI to be checked)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2 (orthogonal range counting, offline bounds)
---

Offline orthogonal range counting answers $q$ box-counting queries on $n$ points in the plane when all the boxes are known before any answer is needed. It sweeps a vertical line from left to right, inserts each point into a [Fenwick tree](/fenwick-tree/) indexed by the rank of its $y$-coordinate, and reads the number of points with $y \in [y_1, y_2]$ twice per box: just before the line reaches $x_1$, and just after it passes $x_2$. The difference is the count. The whole batch takes $O((n + q) \log (n + q))$ time and $O(n + q)$ space in the worst case, against $O(n \log n)$ space for an online [range tree](/range-tree/).

## In plain words

To count the points inside a rectangle, count the points between its bottom and top edges that lie to the left of its right edge, and subtract those that lie to the left of its left edge. What remains are exactly the points between the left and right edges.

If all the rectangles are known in advance, one pass from left to right gives all these numbers. Walk over the points in left-to-right order and drop each one into a tally sorted by height. Each time the walk reaches the left edge of a rectangle, read how many points of the tally are between its bottom and top and remember that number; when it passes the right edge, read again and take the difference. A tally that can add one point and count a band of heights quickly makes the whole pass fast.

## The problem

**Notation.** $P$ is a multiset of $n$ points in the plane ($d = 2$), $p = (p_x, p_y)$ a point, and $Q_1, \dots, Q_q$ the closed query boxes $Q_i = [x_1, x_2] \times [y_1, y_2]$. $Y$ is the sorted list of the distinct $y$-coordinates of $P$, with $m = |Y| \le n$. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used. The model is the [real RAM](/real-ram/): coordinates are only compared, and the counters are integers.

**Input.** $P$ and the list of boxes, all at once.

**Output.** For every $i$, the number $|P \cap Q_i|$, with each copy of a repeated point counted.

**Degenerate input.** No general position is assumed. Points may share coordinates with each other and with box sides. A box with $x_1 > x_2$ or $y_1 > y_2$ is empty and gets $0$.

## The algorithm

```pseudo id=main
OFFLINE-RANGE-COUNT(P, Q_1 .. Q_q)
L1  Y ← the sorted distinct y-coordinates of P; the rank of y is its position in Y, from 1
L2  E ← one POINT event (p_x, rank of p_y) per point; for each nonempty box Q_i, an OPEN event at x1 and a CLOSE event at x2, each with r1 = #{y ∈ Y : y < y1} and r2 = #{y ∈ Y : y ≤ y2}
L3  sort E by x, and at equal x put OPEN before POINT before CLOSE
L4  F ← a Fenwick tree of size m with all counts 0; for each event e of E in order do
L5      if e is a POINT event then F.ADD(rank, 1)
L6      else c ← F.PREFIX(r2) − F.PREFIX(r1); ans_i ← ans_i − c for OPEN, ans_i ← ans_i + c for CLOSE
L7  return ans_1, ..., ans_q
```

- **Line L1** is [coordinate compression](/coordinate-compression/): the Fenwick tree only needs the order of the $y$-values.
- **Line L2.** $r_1$ and $r_2$ come from a lower bound and an upper bound [binary search](/binary-search/) in $Y$, so the ranks $r_1 + 1, \dots, r_2$ are exactly the $y$-values in $[y_1, y_2]$.
- **Line L3** settles ties on the sweep line. An OPEN event at $x_1$ must see the points with $p_x < x_1$, so it comes before the points with $p_x = x_1$; a CLOSE event at $x_2$ must see the points with $p_x \le x_2$, so it comes after them.
- **Line L6** reads the number of inserted points with $y \in [y_1, y_2]$ by two prefix sums.

## Example

The points are $(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)$, and the boxes are $Q_1 = [3, 7] \times [2, 6]$ and $Q_2 = [6, 9] \times [1, 6]$. Here $Y = (1, 2, 3, 4, 6, 7, 8)$, so $Q_1$ reads the ranks $2$ to $5$ and $Q_2$ the ranks $1$ to $5$.

| $x$ | events in order | points inserted so far with $y$ in $[2, 6]$ / in $[1, 6]$ | effect |
|---|---|---|---|
| 2 | POINT $(2,3)$ | | |
| 3 | OPEN $Q_1$, POINT $(3,8)$ | $Q_1$ reads $1$: $(2,3)$ | $ans_1 = -1$ |
| 4 | POINT $(4,7)$ | | |
| 5 | POINT $(5,4)$ | | |
| 6 | OPEN $Q_2$, POINT $(6,6)$ | $Q_2$ reads $2$: $(2,3), (5,4)$ | $ans_2 = -2$ |
| 7 | POINT $(7,2)$, CLOSE $Q_1$ | $Q_1$ reads $4$: $(2,3), (5,4), (6,6), (7,2)$ | $ans_1 = 3$ |
| 8 | POINT $(8,1)$ | | |
| 9 | POINT $(9,6)$, CLOSE $Q_2$ | $Q_2$ reads $6$: all but $(4,7)$ and $(3,8)$ | $ans_2 = 4$ |

The answers are $3$ and $4$: $Q_1$ holds $(5,4), (6,6), (7,2)$, and $Q_2$ holds $(6,6), (7,2), (8,1), (9,6)$. The points $(6,6)$, $(7,2)$ and $(9,6)$ lie on box boundaries.

## Correctness

**Key invariant.** When the sweep processes an OPEN event at $x_1$, the Fenwick tree holds one count for each point with $p_x < x_1$, and when it processes a CLOSE event at $x_2$, one count for each point with $p_x \le x_2$. So $ans_i = |\{p : p_x \le x_2, y_1 \le p_y \le y_2\}| - |\{p : p_x < x_1, y_1 \le p_y \le y_2\}|$, which is $|P \cap Q_i|$ because the first set contains the second when $x_1 \le x_2$. The full proof is in [the correctness proof](proofs/correctness/).

## Complexity

- **Sorting.** $Y$ and the $n + 2q$ events are sorted in $O((n + q) \log (n + q))$ time, and line L2 does $2q$ binary searches in $Y$, $O(q \log n)$.
- **Sweep.** $n$ ADD operations and $4q$ PREFIX operations on a Fenwick tree of size $m \le n$, each $O(\log n)$.
- **Total.** $O((n + q) \log (n + q))$ time and $O(n + q)$ space, in the worst case.
- **Word RAM.** Chan and Pătraşcu (2010) count $n$ points in $n$ boxes in $O(n \sqrt{\log n})$ time; see [orthogonal range counting](/orthogonal-range-counting/).

## Properties

- **Offline.** All boxes must be known before the sweep. The answers come out in sweep order, not in input order.
- **Linear space.** Only the event list and a Fenwick tree are kept, unlike the $O(n \log n)$ of an online [range tree](/range-tree/) or [persistent segment tree](/persistent-segment-tree/).
- **Works for any group.** Replacing the count $1$ by a weight from an abelian group, with subtraction, gives offline range sums; a semigroup without inverses does not allow line L6.

## Variants and improvements

- **Dominance counting.** For $(-\infty, x] \times (-\infty, y]$ only the CLOSE event is needed, and one prefix sum; see [dominance counting](/dominance-counting/). Counting inversions of a permutation is the case where the points are $(i, \pi(i))$; see [inversion counting with a Fenwick tree](/inversion-count-with-fenwick-tree/).
- **Higher dimensions.** Bentley's multidimensional divide and conquer reduces $d$-dimensional offline dominance counting to $(d-1)$-dimensional sweeps and runs in $O(n \log^{d-1} n)$ time with linear space.
- **Online counterparts.** If the boxes arrive one at a time, a [persistent segment tree](/persistent-segment-tree/) on the sweep, a [merge sort tree](/merge-sort-tree/), a [wavelet tree](/wavelet-tree/) or a [range tree](/range-tree/) answers each in $O(\log n)$ or $O(\log^2 n)$ time with $O(n \log n)$ space; see [offline query processing](/offline-query-processing/) for the general trade.
- **Sweeping the other way.** Sweeping by $y$ with a Fenwick tree on $x$-ranks is the same algorithm with the coordinates swapped.

## When to use it

Use the sweep when the boxes are known in advance and only counts or group sums are wanted, as in batch analytics, counting inversions, and competitive programming. It is the simplest correct method and uses linear memory. If points must be reported, or queries come online, use a [range tree](/range-tree/) or a [kd-tree](/kd-tree-range-search/) instead.

## Pitfalls

- **Wrong order of events at equal $x$.** If POINT events at $x_1$ come before the OPEN event, the points on the left side of the box are subtracted, and the count misses them. If the CLOSE event comes before POINT events at $x_2$, the points on the right side are missed. Line L3 fixes the order.
- **Strict and non-strict ranks.** $r_1$ must count the $y$-values $< y_1$ and $r_2$ those $\le y_2$; using $\le$ for $r_1$ drops the points on the bottom side.
- **Compressing only the point coordinates and looking up box sides by equality.** Box sides need not be point coordinates, so their ranks come from binary search, not from a dictionary of point values.
- **Empty boxes.** A box with $x_1 > x_2$ has its CLOSE before its OPEN, and the difference is negative. Skip such boxes, and boxes with $y_1 > y_2$, as line L2 does.

## Implementations

## History

Bentley's 1980 paper on multidimensional divide and conquer treated the all-points empirical cumulative distribution function (ECDF) problem, which is batched dominance counting, by sweeping and recursion on the dimension. The sweep with a Fenwick tree became standard after Fenwick's 1994 paper on cumulative frequency tables, which gave a compact counter with logarithmic updates and prefix sums. Chan and Pătraşcu (2010) showed that $n$ offline counting queries can be answered in $O(n \sqrt{\log n})$ time on the word RAM, below the $\Omega(\log n / \log \log n)$ per-query bound for online static structures of near-linear space.

## References
