---
tag: J9VDA4
kind: problem
slug: maximum-overlap
name: Maximum overlap
aliases:
- Maximum depth of an interval family
- Maximum number of simultaneously active intervals
area: sequences/interval-problems
level: intro
summary: Find the largest number of intervals that share a common point.
prereqs: [sorting-problem, total-order]
see_also: [sweep-maximum-overlap, interval-partitioning, interval-coloring-depth-theorem, helly-property-intervals, interval-stabbing-query, maximum-clique, element-distinctness-lower-bound]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, the subsection on interval partitioning (the depth of a set of intervals)
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 8, Interval Graphs (maximal cliques of an interval graph and the points of the line)
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), pages 80 to 86"
    locator: the element distinctness lower bound used in the Bounds section
---

Maximum overlap asks for the largest number of intervals, among $n$ given intervals, that contain one common point, and for such a point. This number is the *depth* of the family. It is the number of resources that [interval partitioning](/interval-partitioning/) needs, and, by the [Helly property](/helly-property-intervals/), the size of a [maximum clique](/maximum-clique/) of the interval graph. A sort of the end points and a counter solve it in $O(n \log n)$ time. Whether intervals that only touch count as overlapping decides the answer, so the end point type is part of the input.

## In plain words

A web server logs, for each visitor, the moment the visit started and the moment it ended. What was the largest number of visitors on the site at one time, and when did it happen?

Picture each visit as a bar on a time line. Run your finger along the line. At each moment, count the bars above your finger. The answer is the largest count you see.

One detail changes the answer: if one visit ends at 10:00 and another starts at 10:00, were both on the site at 10:00? If the end moment belongs to the visit, yes, and the two count together. If it does not, they never overlap.

## Definition

**Input.** A finite family of $n$ nonempty intervals $I_1, \ldots, I_n$ of $\mathbb{R}$ (or of a [total order](/total-order/)), with end points $l_j \le r_j$. The type of each interval is given: closed $[l_j, r_j]$, half-open $[l_j, r_j)$ with $l_j < r_j$, or open $(l_j, r_j)$ with $l_j < r_j$.

**Output.** The depth

$$ d = \max_{x \in \mathbb{R}} c(x), \qquad c(x) = \bigl|\{\, j : x \in I_j \,\}\bigr|, $$

and a witness point $x^*$ with $c(x^*) = d$. For $n = 0$, $d = 0$.

**Where the maximum is.** The coverage $c$ changes only at end points, so the maximum exists. For closed and half-open intervals it is reached at some left end. Let $c(x) = d$, and let $l^*$ be the largest left end among the intervals that contain $x$. Each such interval $I_j$ has $l_j \le l^* \le x$, and $x$ is in $I_j$, so $x$ is not past its right end, and $I_j$ also contains $l^*$; hence $c(l^*) \ge d$. For open intervals the maximum is reached on an open gap just to the right of a left end.

**Touching end points.** For two intervals that meet at one point $t$:

| intervals | $c(t)$ | overlap? |
|---|---|---|
| $[1, 3]$ and $[3, 5]$ | 2 | yes |
| $[1, 3)$ and $[3, 5)$ | 1 | no |
| $(1, 3)$ and $(3, 5)$ | 0 | no |

## Variants

- **Only the number.** Return $d$ without a witness. This is the "minimum number of platforms" or "meeting rooms" count.
- **Weighted overlap.** Each interval has a weight $w_j \ge 0$, and the goal is $\max_x \sum_{j : x \in I_j} w_j$. The same sweep adds $w_j$ instead of 1.
- **All maximal points.** Report every maximal segment of the line where $c(x) = d$.
- **Dynamic.** Insert and delete intervals and ask for $d$ after each change. A [segment tree](/segment-tree/) over the coordinates with range add and global maximum does each change in $O(\log n)$ time.
- **Query at a point.** The value $c(x)$ at one given $x$ is an [interval stabbing query](/interval-stabbing-query/) that counts instead of reporting.
- **Circular arcs.** On a circle, the depth is still found by a sweep, but it no longer equals the number of colors needed.

## Examples

**Closed intervals.** $[1, 3], [2, 5], [3, 4], [5, 8], [6, 7], [8, 9], [7, 10]$ have depth $d = 3$. The point 3 lies in $[1, 3], [2, 5], [3, 4]$; the points 7 and 8 also have coverage 3.

**The same numbers as half-open intervals.** $[1, 3), [2, 5), [3, 4), [5, 8), [6, 7), [8, 9), [7, 10)$ have depth $d = 2$. At 3 the interval $[1, 3)$ has ended, at 7 the interval $[6, 7)$ has ended, and at 8 the interval $[5, 8)$ has ended. So one family of numbers gives two different answers.

**Point intervals.** $[4, 4], [4, 4], [4, 4]$ has depth 3 at the point 4. As half-open or open intervals these are empty and are not allowed.

**Edge cases.** One interval has depth 1. $n$ pairwise disjoint intervals have depth 1. $n$ intervals that all contain one point have depth $n$.

## Known algorithms

- **[Sweep for maximum overlap](/sweep-maximum-overlap/).** Sort the $2n$ end points, with the tie rule set by the type, and keep a counter; the largest value is $d$. $O(n \log n)$ time and $O(n)$ space.
- **Two sorted arrays.** Sort the left ends and the right ends separately and merge them with two pointers. Same bound, no event objects.
- **Difference array.** For integer coordinates in a range of size $U$, add $+1$ and $-1$ in an array and take prefix sums. $O(n + U)$ time.
- **[Greedy partitioning](/interval-partitioning-greedy/).** The number of resources it opens is $d$, so it also finds the depth, with an assignment, in $O(n \log n)$ time.

## Bounds

**Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/), by the sweep.

**Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, even to decide whether $d \ge 2$. Given numbers $x_1, \ldots, x_n$, form the closed point intervals $[x_j, x_j]$. Then $d \ge 2$ if and only if two numbers are equal. So an algorithm for maximum overlap decides [element distinctness](/element-distinctness/) with $O(n)$ extra work, and Ben-Or's bound for element distinctness ([lower bound page](/element-distinctness-lower-bound/)) applies.

**Value.** $1 \le d \le n$ for $n \ge 1$, and both ends are reached.

## Reductions

- **Maximum clique of an interval graph.** In the interval graph (one vertex per interval, an edge for each intersecting pair), a set of intervals is a clique if and only if they share a point, by the [Helly property](/helly-property-intervals/). So $d$ is the clique number $\omega$.
- **Fewest resources.** By the [interval coloring depth theorem](/interval-coloring-depth-theorem/), $d$ is also the chromatic number of the interval graph, so the depth is the answer to the counting form of [interval partitioning](/interval-partitioning/).
- **From element distinctness.** As in the Bounds section, in $O(n)$ time.

## Applications

- **Capacity planning.** The number of gates, platforms, rooms or servers needed when the times are fixed.
- **Peak load.** The largest number of concurrent sessions, calls or open connections in a log.
- **Register pressure.** In straight-line code, the largest number of live variables at one point is the depth of the live ranges, and it is a lower bound on the number of registers without spills.
- **Genomics.** The largest read depth at one position of a chromosome.

## References
