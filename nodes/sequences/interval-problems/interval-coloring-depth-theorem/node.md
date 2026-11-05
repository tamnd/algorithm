---
tag: MRFSCX
kind: theorem
slug: interval-coloring-depth-theorem
name: Interval coloring depth theorem
aliases:
- Chromatic number of an interval graph equals its depth
- Interval graphs are perfect
area: sequences/interval-problems
level: core
summary: The fewest colors needed for intervals so that overlapping intervals differ equals the largest number of intervals through one point.
prereqs: [interval-partitioning, maximum-overlap, graph-coloring, induction]
see_also: [interval-partitioning-greedy, helly-property-intervals, perfect-graph, chordal-graph, greedy-coloring, chromatic-number, clique-number, circular-arc-coloring]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling, the subsection on interval partitioning (the depth bound and the greedy that meets it)
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 8, Interval Graphs (interval graphs are chordal and perfect)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.1, the exercise on scheduling all activities in the fewest lecture halls
---

The interval coloring depth theorem says that a finite family of intervals can be colored with $d$ colors, so that intervals that meet get different colors, where $d$ is the depth, the largest number of intervals that contain one point, and that fewer colors never suffice. In graph terms, the [chromatic number](/chromatic-number/) of an interval graph equals its [clique number](/clique-number/). It is the reason why [interval partitioning](/interval-partitioning/) has a simple greedy solution, and it shows that interval graphs are [perfect](/perfect-graph/). The theorem holds for closed, half-open and open intervals alike, but the depth itself depends on the type, because touching intervals meet only when both contain the common end point.

## Statement

Let $\mathcal{F} = \{I_1, \ldots, I_n\}$ be a finite family of nonempty intervals of $\mathbb{R}$, all closed, all half-open, or all open. Let

$$ d(\mathcal{F}) = \max_{x \in \mathbb{R}} \bigl|\{\, j : x \in I_j \,\}\bigr| $$

be its depth, and let $G$ be its interval graph, with a vertex for each $I_j$ and an edge between $I_i$ and $I_j$, $i \ne j$, when $I_i \cap I_j \ne \emptyset$. Then

$$ \chi(G) = \omega(G) = d(\mathcal{F}). $$

That is, there is a map $c : \{1, \ldots, n\} \to \{1, \ldots, d\}$ with $c(i) \ne c(j)$ whenever $I_i \cap I_j \ne \emptyset$, and every such map with fewer than $d$ colors fails.

## In plain words

Picture each interval as a bar on a line, and color the bars so that bars that overlap get different colors. Find the place on the line where the most bars pile up. All those bars overlap each other, so each needs its own color. The theorem says that this is the only reason you ever need many colors: as many colors as the highest pile always suffice.

The type of the bar ends matters only in deciding which bars overlap. Two bars that touch at one end overlap only if both include that end.

## Proof

There are three steps: $\omega \ge d$, $\chi \ge \omega$, and $\chi \le d$.

**Step 1: $\omega(G) \ge d$.** Let $x$ be a point in $d$ intervals. These $d$ intervals pairwise meet, at $x$, so they form a clique of $G$.

**Step 2: $\chi(G) \ge \omega(G)$.** The vertices of a clique pairwise share an edge, so they need different colors. This holds in every graph.

**Step 3: $\chi(G) \le d$.** Order the intervals by left end, $l_1 \le l_2 \le \cdots \le l_n$ after renaming, and color them in this order by [greedy coloring](/greedy-coloring/): $I_j$ gets the smallest color not used by an earlier interval that meets $I_j$. Fix $j$, and let $E_j$ be the set of earlier intervals $I_i$, $i < j$, that meet $I_j$. We show that the intervals of $E_j$ and $I_j$ all contain one common point $z$:

- *Closed and half-open intervals.* Take $z = l_j$, which lies in $I_j$. For $I_i \in E_j$ we have $l_i \le l_j$. If $I_i$ did not contain $l_j$, every point of $I_i$ would be less than $l_j$, since $I_i$ starts at or before $l_j$ and is an interval, and $I_i$ would miss $I_j$, whose points are all at least $l_j$. So $l_j \in I_i$.
- *Open intervals.* $I_j = (l_j, r_j)$ contains no point at or left of $l_j$. Each $I_i \in E_j$ has $l_i \le l_j$ and meets $I_j$, so it contains a point greater than $l_j$, and since $l_i \le l_j$ it contains the whole open interval $(l_j, \min(r_i, r_j))$. Take $z$ with $l_j < z < \min_{I_i \in E_j \cup \{I_j\}} r_i$; the minimum is over finitely many values, all greater than $l_j$.

So $|E_j| + 1 \le d$, and $E_j$ uses at most $d - 1$ colors. The smallest free color of $I_j$ is at most $d$. Hence the greedy uses at most $d$ colors, and the coloring is proper by construction.

Together, $d \le \omega(G) \le \chi(G) \le d$. $\blacksquare$

**The step with the heap.** The [interval partitioning greedy](/interval-partitioning-greedy/) is a fast way to carry out Step 3: instead of the smallest free color it takes any free color, the one whose last interval ends first, and the same argument bounds the number of colors it opens.

## Consequences

- **Interval partitioning.** The fewest resources for a set of intervals with fixed times is the depth, and the greedy of Step 3 finds an optimal assignment in $O(n \log n)$ time.
- **Interval graphs are perfect.** An induced subgraph of an interval graph is the interval graph of a subfamily, so the theorem applies to it too: $\chi(H) = \omega(H)$ for every induced subgraph $H$ of $G$. This is the definition of a [perfect graph](/perfect-graph/).
- **Maximum clique in polynomial time.** $\omega(G)$ is the depth, so a [maximum clique](/maximum-clique/) of an interval graph is found by the [sweep for maximum overlap](/sweep-maximum-overlap/) in $O(n \log n)$ time, though the problem is NP-hard in general graphs.
- **Interval graphs are chordal.** In the order by left end, the earlier neighbors of each interval form a clique, as Step 3 shows. So the reverse of this order is a [perfect elimination ordering](/perfect-elimination-ordering/), in which the later neighbors of each vertex form a clique, and interval graphs are [chordal](/chordal-graph/).
- **Register pressure.** For straight-line code, the live ranges of variables are intervals, and the fewest registers without spills is the largest number of variables live at one point.

## Tightness

- **The bound is reached.** The $d$ intervals through the deepest point need $d$ colors, so the number $d$ cannot be lowered.
- **Order matters for first fit.** Greedy coloring in an arbitrary order can use more than $d$ colors. For the half-open intervals $[0, 2), [4, 6), [1, 4), [3, 5)$ in this order, the first two get color 1, $[1, 4)$ gets color 2, and $[3, 5)$ meets $[4, 6)$ and $[1, 4)$, so it gets color 3, while $d = 2$.
- **Circular arcs.** For arcs of a circle the theorem fails in both of its equalities. Five arcs, each meeting only its two neighbors, form a cycle of length 5, which has $\omega = 2$ and $\chi = 3$. Three arcs that pairwise meet with no common point have $\omega = 3$ but depth 2; see [circular-arc coloring](/circular-arc-coloring/).
- **Rectangles.** For axis-parallel rectangles in the plane, five thin rectangles arranged in a ring also form a cycle of length 5, so $\chi > \omega$ again. The theorem is special to one dimension.
- **Touching end points.** $[1, 3]$ and $[3, 5]$ need 2 colors, while $[1, 3)$ and $[3, 5)$ need 1. The theorem holds in both cases, but with different depths.

## History

Kleinberg and Tardos give the depth bound and the greedy that meets it as the solution of the interval partitioning problem, and CLRS pose the same question as an exercise on scheduling lectures in the fewest halls. Golumbic's book treats interval graphs as a class of perfect graphs, in which the equality of chromatic number and clique number holds for every induced subgraph.

## References
