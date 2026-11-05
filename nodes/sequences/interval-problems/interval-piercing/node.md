---
tag: D900VD
kind: problem
slug: interval-piercing
name: Interval piercing
aliases:
- Interval stabbing (minimum points)
- Hitting set of intervals
- Minimum arrows to burst balloons
area: sequences/interval-problems
level: core
summary: Find the fewest points that hit every interval.
prereqs: [interval-covering, greedy-algorithm, activity-selection]
see_also: [interval-piercing-greedy, earliest-finish-time-first, hitting-set, helly-property-intervals, interval-stabbing-query, maximum-independent-set, perfect-graph, interval-covering]
sources:
  - url: https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/
    title: LeetCode 452, Minimum Number of Arrows to Burst Balloons
    locator: the problem statement (closed intervals; an arrow at x bursts a balloon when x_start <= x <= x_end)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling (the earliest finish time greedy for a largest set of disjoint intervals)
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 8, Interval Graphs (interval graphs are perfect, so the clique cover number equals the independence number)
  - paper: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), pages 80 to 86"
    locator: the element distinctness lower bound used in the Bounds section
  - paper: "Robert J. Fowler, Michael S. Paterson and Steven L. Tanimoto, Optimal packing and covering in the plane are NP-complete, Information Processing Letters 12(3) (1981), pages 133 to 137"
    locator: the NP-completeness of covering points by unit squares, the planar form of piercing
---

Interval piercing asks for the fewest points such that every interval of a family contains at least one of them. It is the [hitting set](/hitting-set/) problem for intervals of a line, and unlike the general hitting set problem it is easy: a greedy that puts a point at the earliest right end of an interval not yet hit solves it in $O(n \log n)$ time. The least number of points equals the largest number of pairwise disjoint intervals, a min-max theorem that the greedy proves. Touching matters: the closed intervals $[1, 3]$ and $[3, 5]$ share the point 3, so one point pierces both, while $[1, 3)$ and $[3, 5)$ are disjoint and need two.

## In plain words

Balloons are tied along a wall, and each one spans a stretch of the wall. An arrow shot straight up from one spot bursts every balloon above that spot. How few arrows burst all balloons?

Look at the balloon whose stretch ends first. Some arrow must hit it, and the best place for that arrow is the last spot of that balloon, because every other spot of it hits fewer of the balloons that are still left. Shoot there, remove every balloon it burst, and repeat with the balloon that now ends first.

The balloons that start each round are far apart: no two of them share a spot. So no plan can use fewer arrows than the plan you found.

## Definition

**Input.** A finite family of nonempty intervals $I_1, \ldots, I_n$ of $\mathbb{R}$ with $I_j = \langle l_j, r_j \rangle$, all of one type: closed with $l_j \le r_j$, or half-open or open with $l_j < r_j$.

**Output.** A set $P \subset \mathbb{R}$ of least size $\tau$ such that $P \cap I_j \ne \emptyset$ for every $j$. The number $\tau$ is the *piercing number* of the family.

**Packing number.** Let $\nu$ be the largest number of pairwise disjoint intervals in the family. Each point lies in at most one of $\nu$ disjoint intervals, so $\tau \ge \nu$.

**Min-max theorem.** For every finite family of intervals, $\tau = \nu$. The greedy proves it: it places points at the right ends $p_1 < p_2 < \cdots < p_m$ of intervals $J_1, \ldots, J_m$, where each $J_{i+1}$ was not hit by $p_i$. For closed intervals that means $J_{i+1}$ starts after $p_i$, which is the right end of $J_i$, so $J_1, \ldots, J_m$ are pairwise disjoint and $m \le \nu \le \tau \le m$. The [greedy page](/interval-piercing-greedy/) proves the same for the other types.

**Touching end points.**

| intervals | pierced by one point? | $\tau$ |
|---|---|---|
| $[1, 3]$, $[3, 5]$ | yes, by 3 | 1 |
| $[1, 3)$, $[3, 5)$ | no, they are disjoint | 2 |
| $(1, 3)$, $(3, 5)$ | no | 2 |
| $[2, 5]$, $[5, 5]$ | yes, by 5 | 1 |

For half-open and open intervals there is no rightmost point, so the greedy point is "just left of $r$", and a concrete point must be chosen inside all the intervals of its group.

## Variants

- **Points from a given set.** The points must come from a finite candidate set $Q$. The greedy takes the largest candidate that is at most the earliest right end and still at least the left end of that interval; if there is none, there is no solution.
- **Each interval needs $k$ points.** Choose the fewest points such that each interval $I_j$ contains at least $k_j$ of them. With the candidate points fixed, it is still an integer program with an interval matrix, so the linear programming method below solves it in polynomial time.
- **Weighted points.** Each candidate point has a cost; minimize the total cost. A dynamic program over the candidates sorted from left to right solves it in polynomial time.
- **Circular arcs.** Pierce arcs of a circle. A point of an optimal solution can be moved clockwise to the first right end of an arc that contains it, and it still hits the same arcs. So trying each right end as the first point, and running the line greedy on the arcs it misses, which do not wrap around it, gives an $O(n^2)$ algorithm after sorting.
- **Boxes in the plane.** Piercing axis-parallel rectangles, even unit squares, with the fewest points is NP-hard, by the result of Fowler, Paterson and Tanimoto on covering points with unit squares. The line case is easy because a point either lies left of an interval, inside it, or right of it.
- **Counting form of the dual.** The packing number $\nu$ alone is the answer to [activity selection](/activity-selection/).

## Examples

**One family, three types.** Take the end point pairs $(1, 4), (2, 3), (3, 6), (5, 7), (6, 8), (8, 9), (9, 10)$.

- *Closed.* The points $3, 7, 9$ pierce all: 3 hits $[1, 4], [2, 3], [3, 6]$, 7 hits $[5, 7], [6, 8]$, and 9 hits $[8, 9], [9, 10]$. The disjoint intervals $[2, 3], [5, 7], [8, 9]$ show that 3 points are needed. Two of the hits, of $[3, 6]$ by 3 and of $[9, 10]$ by 9, are touches.
- *Half-open.* Now $[2, 3), [3, 6), [6, 8), [8, 9), [9, 10)$ are pairwise disjoint, so $\tau \ge 5$, and the points $2, 5, 6, 8, 9$ pierce all intervals. So $\tau = 5$.
- *Open.* The same five intervals are disjoint as open intervals, and $2.5, 5.5, 7, 8.5, 9.5$ pierce all, so $\tau = 5$.

**Nested intervals.** $[0, 6], [1, 5], [2, 4]$ have a common point, so $\tau = 1$, for any type.

**Point intervals.** For closed point intervals $[x_1, x_1], \ldots, [x_n, x_n]$, $\tau$ is the number of distinct values among the $x_j$.

## Known algorithms

- **[Interval piercing greedy](/interval-piercing-greedy/).** Sort by right end; whenever an interval is not hit by the last point, place a new point at its right end (just left of it, for half-open and open intervals). $O(n \log n)$ time.
- **Earliest finish time first.** [This greedy](/earliest-finish-time-first/) for activity selection chooses the same intervals $J_1, \ldots, J_m$, and its right ends are the piercing points; one run gives both the packing and the piercing.
- **Linear programming.** The constraint matrix, with a row per interval and a column per candidate point, has consecutive ones in each row, so it is totally unimodular, and the LP optimum is integral. This explains why the weighted variant is polynomial.
- **Brute force.** Try sets of right ends in order of size; for closed intervals the right ends are enough candidates. $O(2^n n)$ time.

## Bounds

**Upper bound.** $O(n \log n)$ time in the [comparison model](/comparison-model/), and $O(n)$ time when the intervals come sorted by right end.

**Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, to compute $\tau$. For closed point intervals $[x_j, x_j]$, $\tau = n$ if and only if the $x_j$ are distinct, so computing $\tau$ decides [element distinctness](/element-distinctness/) with $O(n)$ extra work, and Ben-Or's bound ([lower bound page](/element-distinctness-lower-bound/)) applies.

**Value.** $1 \le \tau \le n$ for $n \ge 1$. $\tau = 1$ exactly when all the intervals share a point, which by the [Helly property](/helly-property-intervals/) happens exactly when every two of them meet.

## Reductions

- **Clique cover of an interval graph.** The intervals that contain one point form a clique of the interval graph, and by the Helly property every clique has a common point. So $\tau$ is the clique cover number $\theta$ and $\nu$ is the independence number $\alpha$. The theorem $\tau = \nu$ is $\theta = \alpha$, which holds because interval graphs are [perfect](/perfect-graph/).
- **Dual of activity selection.** $\nu$ is the optimum of activity selection, and $\tau = \nu$ by the min-max theorem.
- **From element distinctness.** As in the Bounds section.
- **To set cover.** Exchanging the roles of points and intervals turns piercing into covering a set of points by sets; for intervals both directions stay easy.

## Applications

- **Fewest checks.** The fewest moments at which to poll, so that every job that runs during a known interval is seen running at least once.
- **Sensors and guards.** The fewest guard positions on a corridor, each guard seeing every room whose span contains the position.
- **Scheduling meetings.** The fewest broadcast times so that each person, available in one interval, hears one.
- **Snapshots.** The fewest snapshot times of a database such that the lifetime of each record contains a snapshot.

## References
