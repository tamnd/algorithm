---
tag: QB1ZZX
kind: problem
slug: bitonic-tsp
name: Bitonic euclidean traveling salesman problem
aliases:
- bitonic tour
area: techniques/dynamic-programming
level: intro
summary: Find the shortest closed tour through points that goes left to right and then back, with no other turns.
prereqs: [traveling-salesman-problem, euclidean-tsp, optimal-substructure]
see_also: [euclidean-tsp, traveling-salesman-problem, held-karp-algorithm, mst-tsp-heuristic, interval-dp, monge-property]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 14, end-of-chapter problems, Bitonic euclidean traveling-salesman problem
  - paper: doi:10.1145/3414845
    title: Mark de Berg, Kevin Buchin, Bart M. P. Jansen and Gerhard Woeginger, Fine-grained complexity analysis of two classic TSP variants, ACM Transactions on Algorithms 17(1), 2021
    locator: the part on bitonic TSP (the O(n log^2 n) algorithm, and its extension to pyramidal tours in the plane)
  - paper: doi:10.1016/0166-218X(95)00103-X
    title: Rainer E. Burkard, Bettina Klinz and Rüdiger Rudolf, Perspectives of Monge properties in optimization, Discrete Applied Mathematics 70(2), 95-161, 1996
    locator: the section on the traveling salesman problem and pyramidal tours
---

The bitonic traveling salesman problem asks for the shortest closed tour through $n$ points in the plane that starts at the leftmost point, goes strictly from left to right to the rightmost point, and comes back strictly from right to left to the start. Such a tour is called bitonic. The general [Euclidean TSP](/euclidean-tsp/) is NP-hard, but the bitonic restriction has a simple dynamic program that runs in $O(n^2)$ time, which is a classic exercise in CLRS. De Berg, Buchin, Jansen and Woeginger showed in 2021 that it can be solved in $O(n \log^2 n)$ time.

## In plain words

You must visit some towns and come back home, and you want the shortest trip. In general this is a very hard problem. So add a rule: first drive only to the east until you reach the town furthest east, then drive only to the west until you are home. Each town is visited on the way out or on the way back.

With this rule, the trip is two chains that both go from the west end to the east end. When you add the towns one by one from west to east, the next town must join the end of one of the two chains. So you only need to remember where the two chains end, and that gives a small table.

## Definition

**Input.** Points $p_1, \ldots, p_n$ in the plane, $n \ge 2$, with distinct $x$-coordinates, numbered so that $x(p_1) < x(p_2) < \cdots < x(p_n)$. The distance $d(p_i, p_j)$ is the Euclidean distance.

**Bitonic tour.** A closed tour that visits every point once and is the union of two paths from $p_1$ to $p_n$, each with strictly increasing $x$-coordinates, which share only their end points. Equivalently, as a cyclic sequence starting at $p_1$, the $x$-coordinates go up to $p_n$ and then down.

**Output.** A bitonic tour of least total length. For $n = 2$ the tour is $p_1 p_2 p_1$.

## Variants

- **Pyramidal TSP.** For any distance matrix on the labels $1, \ldots, n$, a pyramidal tour goes $1 \to \cdots \to n$ through increasing labels and back through decreasing labels. The bitonic problem is the case where the labels are the order by $x$. The dynamic program below works for any distance matrix.
- **Bitonic paths.** Find the shortest path from $p_1$ to $p_n$ through all points that first goes right and then left, or other fixed shapes; the same table applies with a different end condition.
- **Bottleneck version.** Minimize the longest edge instead of the sum. De Berg, Buchin, Jansen and Woeginger solve it in $O(n \log^3 n)$ time.
- **Equal $x$-coordinates.** Break ties by $y$, or treat the problem as pyramidal TSP on a fixed order.

## Examples

Take the seven points, sorted by $x$,

$$p_1 = (0, 6),\; p_2 = (1, 0),\; p_3 = (2, 3),\; p_4 = (5, 4),\; p_5 = (6, 1),\; p_6 = (7, 5),\; p_7 = (8, 2).$$

The shortest bitonic tour is $p_1 \to p_2 \to p_5 \to p_7 \to p_6 \to p_4 \to p_3 \to p_1$, of length about 25.584. The lower chain $p_1, p_2, p_5, p_7$ goes right, and the upper chain $p_7, p_6, p_4, p_3, p_1$ comes back. The shortest tour without the bitonic rule has length about 24.886, so the restriction costs about 2.8 percent here. A check of all $2^5$ ways to put $p_2, \ldots, p_6$ on the two chains, and of all $6!$ tours, confirms both values.

The table $b[i, j]$ of the algorithm below, rounded to two decimals:

| $b[i, j]$ | $j = 2$ | $j = 3$ | $j = 4$ | $j = 5$ | $j = 6$ | $j = 7$ |
|---|---|---|---|---|---|---|
| $i = 1$ | 6.08 | 9.25 | 12.41 | 15.57 | 19.69 | 22.85 |
| $i = 2$ | | 9.69 | 12.85 | 16.01 | 20.14 | 23.30 |
| $i = 3$ | | | 14.63 | 17.79 | 21.92 | 25.08 |
| $i = 4$ | | | | 17.95 | 22.07 | 25.23 |
| $i = 5$ | | | | | 20.19 | 23.35 |
| $i = 6$ | | | | | | 22.42 |

The answer is $b[6, 7] + d(p_6, p_7) = 22.42 + 3.16 = 25.58$.

## Known algorithms

**The $O(n^2)$ dynamic program.** For $1 \le i < j \le n$, let $b[i, j]$ be the length of the shortest bitonic path: two disjoint paths, both with increasing $x$, one from $p_1$ to $p_i$ and one from $p_1$ to $p_j$, which together visit exactly $p_1, \ldots, p_j$. Equivalently, a single path from $p_i$ to $p_j$ that goes left to $p_1$ and then right to $p_j$.

1. $b[1, 2] = d(p_1, p_2)$.
2. For $i < j - 1$: $b[i, j] = b[i, j-1] + d(p_{j-1}, p_j)$.
3. For $j \ge 3$: $b[j-1, j] = \min_{1 \le k < j-1} \bigl( b[k, j-1] + d(p_k, p_j) \bigr)$.
4. The answer is $b[n-1, n] + d(p_{n-1}, p_n)$.

*Why rule 2 holds.* In a bitonic path for $(i, j)$ with $i < j - 1$, the point $p_{j-1}$ is not an end, so it lies on the chain that ends at $p_j$. That chain has increasing $x$ and visits nothing between $p_{j-1}$ and $p_j$, so its last edge is $p_{j-1} p_j$. Removing it leaves a bitonic path for $(i, j-1)$, and by the usual cut-and-paste argument that path must be shortest.

*Why rule 3 holds.* In a bitonic path for $(j-1, j)$, one chain ends at $p_{j-1}$ and the other at $p_j$. The last edge into $p_j$ comes from some $p_k$ with $k < j - 1$ (the point $p_{j-1}$ is on the other chain). Removing it leaves a bitonic path for $(k, j-1)$. Each $k$ gives a valid path, so the minimum is right.

*Why rule 4 holds.* In a bitonic tour, $p_n$ is joined to two points, one on each chain, and one of them is $p_{n-1}$, because $p_{n-1}$ is the last point of its chain before $p_n$. Removing the edge $p_{n-1} p_n$ leaves a bitonic path for $(n-1, n)$.

There are $O(n^2)$ entries. Rule 2 costs $O(1)$ each, and rule 3 is used $n - 2$ times at $O(n)$ each, so the time is $O(n^2)$ after sorting, and the space is $O(n^2)$, or $O(n)$ if only the length is needed. A table of the chosen $k$ in rule 3 gives the tour.

**Subquadratic time.** De Berg, Buchin, Jansen and Woeginger gave an $O(n \log^2 n)$ algorithm for points in the plane, which also works for pyramidal tours in the plane.

**Pyramidal tours for any distance matrix.** The same dynamic program with an arbitrary matrix $d$ finds the best pyramidal tour in $O(n^2)$ time.

## Bounds

- **Upper bounds.** $O(n^2)$ by the dynamic program, and $O(n \log^2 n)$ by the method of de Berg, Buchin, Jansen and Woeginger.
- **Lower bound.** $\Omega(n)$ to read the input. For a general distance matrix (the pyramidal problem), every edge $\{i, j\}$ occurs in some pyramidal tour, so an algorithm that does not read some distance can be fooled by making that distance very small. So $\Omega(n^2)$ reads are needed, and the dynamic program is optimal there.
- **Relation to the optimum.** A bitonic tour can be much longer than the optimal tour, for example for points on a zigzag. It is an exact answer only to the restricted problem.

## Reductions

- **To pyramidal TSP.** Sorting by $x$ turns the bitonic problem into the pyramidal problem with the Euclidean distance matrix in that order.
- **From the general TSP for special matrices.** For some classes of distance matrices, there is always an optimal tour that is pyramidal, so the general [TSP](/traveling-salesman-problem/) on such matrices is solved by the $O(n^2)$ dynamic program. Burkard, Klinz and Rudolf survey such classes, several of which are defined by [Monge](/monge-property/)-type conditions.

## Applications

- **Teaching.** The problem is a standard example of how a restriction on the shape of a solution makes the state of a dynamic program small, in contrast with the $O(n^2 2^n)$ of the [Held-Karp algorithm](/held-karp-algorithm/) for the general problem.
- **A step in the study of special cases of TSP.** Pyramidal tours, the general form of bitonic tours, are the main tool for the cases of the TSP that are solvable in polynomial time for special distance matrices.
- **Starting tours for heuristics.** A bitonic tour is a valid tour that local search can then improve.

## References
