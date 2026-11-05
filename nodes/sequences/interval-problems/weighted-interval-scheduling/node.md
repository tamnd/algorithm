---
tag: 549YPB
kind: problem
slug: weighted-interval-scheduling
name: Weighted interval scheduling
aliases:
- Maximum-weight independent set of an interval graph
area: sequences/interval-problems
level: core
summary: Choose non-overlapping intervals of maximum total weight.
prereqs: [activity-selection, optimal-substructure]
see_also: [weighted-interval-dp, activity-selection, earliest-finish-time-first, k-machine-interval-scheduling, maximum-independent-set, dag-dynamic-programming, online-interval-scheduling, knapsack-problem]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 6.1, Weighted Interval Scheduling, A Recursive Procedure, and Section 6.2, Principles of Dynamic Programming, Memoization or Iteration over Subproblems
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), pages 80 to 86"
    locator: the element distinctness lower bound used in the Bounds section
  - paper: doi:10.1016/0166-218X(87)90037-0
    title: "Esther M. Arkin and Ellen B. Silverberg, Scheduling jobs with fixed start and end times, Discrete Applied Mathematics 18(1) (1987), pages 1 to 8"
    locator: the weighted problem on k machines, solved by a minimum cost flow
---

Weighted interval scheduling gives each of $n$ intervals a weight and asks for a set of pairwise disjoint intervals of largest total weight. With all weights equal it is [activity selection](/activity-selection/), which a greedy solves, but no greedy rule is correct for general weights, and the standard method is the [dynamic program](/weighted-interval-dp/) $\mathrm{OPT}(j) = \max(\mathrm{OPT}(j - 1), w_j + \mathrm{OPT}(p(j)))$ over the intervals sorted by right end, in $O(n \log n)$ time. In graph terms it is the maximum weight independent set problem on an interval graph, which is NP-hard on general graphs. Whether two intervals that share an end point may both be chosen depends on the end point type, and it changes the optimum.

## In plain words

You own one room and receive offers to rent it. Each offer names a start time, an end time and a price. Two offers that overlap cannot both be accepted. You want to earn as much as possible.

Taking the offer that ends first, or the one that pays most, can be wrong. A long offer that pays well may block two short ones that together pay more, and the other way around.

The trick is to sort the offers by end time and decide for each one: either skip it, or take it and add the best plan for the offers that end before it starts. Whether an offer that starts at 10 fits after one that ends at 10 depends on whether times include their end moment.

## Definition

**Input.** Intervals $I_1, \ldots, I_n$, $I_j = \langle l_j, r_j \rangle$, all of one type, with weights $w_j > 0$. Closed intervals have $l_j \le r_j$; half-open and open intervals have $l_j < r_j$.

**Compatibility.** Two intervals are *compatible* when they are disjoint. For $I_i$ with $l_i \le l_j$:

| type | $I_i$ and $I_j$ compatible if and only if |
|---|---|
| closed $[l, r]$ | $r_i < l_j$ |
| half-open $[l, r)$ | $r_i \le l_j$ |
| open $(l, r)$ | $r_i \le l_j$ |

So intervals that touch, $r_i = l_j$, are compatible for half-open and open intervals and not for closed ones. *Proof.* For closed intervals, the point $l_j$ lies in $I_j$, and it lies in $I_i$ if and only if $l_j \le r_i$, since $l_i \le l_j$; if $r_i < l_j$, every point of $I_i$ is below every point of $I_j$. For half-open and open intervals, if $r_i \le l_j$, every point of $I_i$ is less than $r_i \le l_j$, and every point of $I_j$ is at least $l_j$. If $r_i > l_j$, the points just above $l_j$ and below $\min(r_i, r_j)$ lie in both. $\square$

**Output.** A set $A \subseteq \{1, \ldots, n\}$ of pairwise compatible intervals that maximizes $w(A) = \sum_{j \in A} w_j$, or just the value $w(A)$.

**Weights.** An interval with $w_j \le 0$ never helps, since removing it from a feasible set keeps it feasible, so we assume $w_j > 0$.

**As a graph problem.** In the interval graph, with a vertex per interval and an edge between intervals that meet, a compatible set is an [independent set](/independent-set/). So the problem is [maximum weight independent set](/maximum-independent-set/) on interval graphs, given by their intervals.

## Variants

- **Unit weights.** All $w_j = 1$: [activity selection](/activity-selection/), solved by the [earliest finish time](/earliest-finish-time-first/) greedy in $O(n \log n)$ time.
- **$k$ machines.** Choose intervals of largest weight that can be split among $k$ machines, so that no point lies in more than $k$ chosen intervals: [k-machine interval scheduling](/k-machine-interval-scheduling/). Arkin and Silverberg solve it by a minimum cost flow.
- **Online.** The intervals arrive in order of start and each must be accepted or rejected at once: [online interval scheduling](/online-interval-scheduling/).
- **Circular arcs.** Arcs of a circle in place of intervals, for daily repeating schedules. The arcs through a fixed point of the circle all meet, so an optimal set uses at most one of them. Trying each of them, or none, and cutting the circle there gives at most $n + 1$ instances on a line.
- **Counting and listing.** The number of optimal sets, or all of them, follows from the same recurrence, with counts in place of values.

## Examples

Take six intervals with end points and weights

| interval | $a$ | $b$ | $c$ | $d$ | $e$ | $f$ |
|---|---|---|---|---|---|---|
| end points | $(0, 3)$ | $(3, 6)$ | $(1, 5)$ | $(5, 8)$ | $(6, 9)$ | $(8, 10)$ |
| weight | 2 | 4 | 5 | 3 | 4 | 2 |

Four pairs touch: $a$ and $b$ at 3, $b$ and $e$ at 6, $c$ and $d$ at 5, and $d$ and $f$ at 8.

- *As closed intervals*, no touching pair is compatible. The optimum is $\{c, e\}$, with weight $5 + 4 = 9$.
- *As half-open intervals*, the chains $a, b, e$ and $c, d, f$ are compatible, and both have weight 10, the optimum. Open intervals give the same answer.

**Greedy rules fail.** Earliest finish time on the closed intervals takes $a$, then $d$, the first one that starts after 3, and then nothing, since $f$ touches $d$ at 8: weight 5, against 9. Largest weight first on the half-open intervals takes $c$, then $e$, and then nothing else fits: weight 9, against 10.

**Edge cases.** One interval: take it. All intervals pairwise overlapping: take the heaviest one. All intervals pairwise disjoint: take all of them.

## Known algorithms

- **[Weighted interval DP](/weighted-interval-dp/).** Sort by right end, compute for each $j$ the number $p(j)$ of intervals that end in time for $I_j$ by [binary search](/binary-search/), and fill $\mathrm{OPT}(j) = \max(\mathrm{OPT}(j - 1), w_j + \mathrm{OPT}(p(j)))$. $O(n \log n)$ time, $O(n)$ space, and an optimal set by tracing back. This is the algorithm of Kleinberg and Tardos, Section 6.1.
- **Sorted input.** If the intervals are given sorted both by left end and by right end, the $p(j)$ come from one merge of the two lists in $O(n)$ time, and the whole algorithm is linear.
- **Longest path in a DAG.** Make a node for each end point and for each interval an edge from its left end to its right end of length $w_j$, plus edges of length 0 from each end point to the next one in sorted order, with the touching rule deciding the order of equal values. A longest path is an optimal schedule; see [DAG dynamic programming](/dag-dynamic-programming/).
- **Brute force.** Try all $2^n$ subsets, for testing.

## Bounds

**Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/), with $O(n)$ space, and $O(n)$ time after sorting.

**Lower bound.** In the [algebraic decision tree](/algebraic-decision-tree/) model, $\Omega(n \log n)$ operations are needed, even with unit weights. Given numbers $x_1, \ldots, x_n$, take the closed point intervals $[x_j, x_j]$ with weight 1. Two of them are compatible if and only if their numbers differ, so the optimum is the number of distinct values, and it equals $n$ if and only if all numbers are distinct. This decides [element distinctness](/element-distinctness/), which needs $\Omega(n \log n)$ operations by Ben-Or's theorem.

## Reductions

- **From activity selection.** Unit weights.
- **To maximum weight independent set.** The interval graph, as above. The general problem is NP-hard, and interval graphs are one of the classes where structure, here the order of the right ends, makes it easy.
- **To longest path in a DAG.** As in the Known algorithms section.
- **To minimum cost flow.** The $k$-machine version, and so the case $k = 1$, is a minimum cost flow on a path of end points, by Arkin and Silverberg.

## Applications

- **Renting a resource.** Accept the most valuable bookings for a room, a vehicle, a telescope or a machine.
- **Selecting bids.** Choose among offers for time slots, such as advertising slots, where each offer is an interval and a price.
- **Gene finding and sequence analysis.** Choose a highest scoring set of non-overlapping candidate regions, such as local alignments or exons, along a sequence.
- **Teaching dynamic programming.** It is the first example in Kleinberg and Tardos, because the greedy rules fail and the recurrence has only two cases.

## References
