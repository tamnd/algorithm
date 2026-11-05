---
tag: J5B09G
kind: theorem
slug: helly-property-intervals
name: Helly property for intervals
aliases:
- One-dimensional Helly theorem
- Pairwise intersecting intervals share a point
area: sequences/interval-problems
level: core
summary: If every two intervals of a finite family meet, then all of them share a common point.
prereqs: [maximum-overlap]
see_also: [helly-theorem, interval-coloring-depth-theorem, interval-piercing, maximal-clique, maximum-clique, consecutive-ones-property, chordal-graph, circular-arc-coloring]
sources:
  - paper: "Eduard Helly, Ueber Mengen konvexer Koerper mit gemeinschaftlichen Punkten, Jahresbericht der Deutschen Mathematiker-Vereinigung 32 (1923), pages 175 to 176"
    locator: the theorem for convex sets in d dimensions, of which this page is the case d = 1
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition
    locator: Chapter 8, Interval Graphs (the maximal cliques of an interval graph and their linear order)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.1, Interval Scheduling (the depth as a set of intervals through one point)
---

The Helly property for intervals says that if every two intervals of a finite family meet, then one point lies in all of them. It is the one-dimensional case of [Helly's theorem](/helly-theorem/) on convex sets, and its proof is one line: the largest left end is at most the smallest right end. In the language of interval graphs it says that every clique is a set of intervals through one point, which is why the clique number equals the depth and the maximal cliques correspond to points of the line. The property needs the family to be finite, or the intervals to be closed and bounded, and the precise inequality depends on whether the end points belong to the intervals.

## Statement

Let $I_1, \ldots, I_n$ be finitely many nonempty intervals of $\mathbb{R}$, of any types, with $n \ge 1$. If $I_i \cap I_j \ne \emptyset$ for all $i, j$, then

$$ \bigcap_{j=1}^{n} I_j \ne \emptyset. $$

For intervals of one type with end points $l_j \le r_j$, a common point is given explicitly. Let $L = \max_j l_j$ and $R = \min_j r_j$.

| type | pairwise meeting means | then $L$ and $R$ satisfy | a common point |
|---|---|---|---|
| closed $[l_j, r_j]$ | $l_i \le r_j$ for all $i, j$ | $L \le R$ | $L$ |
| half-open $[l_j, r_j)$ | $l_i < r_j$ for all $i, j$ | $L < R$ | $L$ |
| open $(l_j, r_j)$ | $l_i < r_j$ for all $i, j$ | $L < R$ | $(L + R)/2$, in $\mathbb{R}$ |

## In plain words

Lay some sticks along a line. Suppose that every two sticks overlap somewhere. Then there is one spot that all sticks cover at the same time.

To find it, take the stick that starts last. Every other stick must reach that start, because it overlaps this stick and starts no later. So the spot where the last stick starts is covered by all of them.

If sticks may leave out their end spots, the same idea works, but you may have to move a tiny bit to the right of that start.

## Proof

**One type.** First take closed intervals. Let $i$ be an index with $l_i = L$ and $j$ any index. Since $I_i \cap I_j \ne \emptyset$, some $x$ has $l_i \le x \le r_j$, so $L = l_i \le r_j$. This holds for every $j$, so $L \le R$. Then $l_j \le L \le R \le r_j$ for every $j$, so $L \in I_j$ for all $j$.

For half-open intervals, $I_i \cap I_j \ne \emptyset$ gives some $x$ with $l_i \le x < r_j$, so $l_i < r_j$, and $L < R$ as before. Then $l_j \le L < R \le r_j$, so $L \in [l_j, r_j)$ for all $j$.

For open intervals, $I_i \cap I_j \ne \emptyset$ gives some $x$ with $l_i < x < r_j$, so again $L < R$. The point $m = (L + R)/2$ has $l_j \le L < m < R \le r_j$, so $m \in (l_j, r_j)$ for all $j$.

**Mixed types.** An interval is a nonempty convex set: if it contains $x < y$, it contains every point between them. For each $j$ let $a_j = \inf I_j$ and $b_j = \sup I_j$, which may be infinite. Let $a^* = \max_j a_j$, attained by $I_p$, and $b^* = \min_j b_j$, attained by $I_q$. A point $x \in I_p \cap I_q$ has $a^* \le x \le b^*$, so $a^* \le b^*$.

*Case $a^* < b^*$.* Take any $z$ with $a^* < z < b^*$. For each $j$, $a_j \le a^* < z$, so $I_j$ has a point less than $z$, and $z < b^* \le b_j$, so it has a point greater than $z$. By convexity $z \in I_j$.

*Case $a^* = b^* = c$.* $I_p$ has no point less than $c$ and $I_q$ has no point greater than $c$, so their common point is $c$, and $c$ lies in both. Take any $j$. If $a_j < c < b_j$, then $c \in I_j$ by convexity as before. If $a_j = c$, then $I_j$ has no point less than $c$, and it meets $I_q$, whose points are at most $c$, so $c \in I_j$. If $b_j = c$, the same argument with $I_p$ gives $c \in I_j$. So $c$ lies in every $I_j$. $\blacksquare$

## Consequences

- **Cliques are points.** In an interval graph, a set of intervals is a clique if and only if it has a common point. So the clique number is the depth, as used by the [interval coloring depth theorem](/interval-coloring-depth-theorem/), and a [maximum clique](/maximum-clique/) is found by a sweep.
- **At most $n$ maximal cliques.** Let $C$ be a [maximal clique](/maximal-clique/) of the interval graph of closed intervals. Its intervals share the point $L_C$, the largest left end in $C$. The set of all intervals that contain $L_C$ is a clique that contains $C$, so by maximality it equals $C$. So each maximal clique is the set of intervals through some left end, and there are at most $n$ of them. Sorting these sets by their point gives a linear order of the maximal cliques in which each interval lies in a consecutive run, the [consecutive ones property](/consecutive-ones-property/) of the clique matrix.
- **One point pierces all.** A family has [piercing number](/interval-piercing/) 1 if and only if every two of its intervals meet. Checking this needs only $L$ and $R$, in $O(n)$ time.
- **Intersection of a family.** For one type, $\bigcap_j I_j$ is the interval from $L$ to $R$, with the types of the ends that attain them, and it is nonempty exactly when the pairwise condition holds.
- **Helly number 2.** In the language of convex geometry, intervals have Helly number 2: the condition on all pairs is enough. In $\mathbb{R}^d$, [Helly's theorem](/helly-theorem/) needs every $d + 1$ sets to meet.

## Tightness

- **Infinite families of open or half-open intervals.** The open intervals $(0, 1/k)$, $k = 1, 2, \ldots$, pairwise meet, since $(0, 1/k) \cap (0, 1/m) = (0, 1/\max(k, m))$, but no point lies in all of them. The half-open intervals $[0, 1/k)$ have the common point 0, but $(0, 1/k]$ have none.
- **Infinite families of closed unbounded intervals.** The rays $[k, \infty)$ pairwise meet and have no common point.
- **Infinite families of closed bounded intervals do have it.** If every two of the intervals $[l_j, r_j]$ meet, then $\sup_j l_j \le \inf_j r_j$, and $\sup_j l_j$ lies in all of them. So the finiteness condition can be dropped for closed bounded intervals.
- **Circular arcs.** Three arcs of a circle, each covering a little more than a third of it and placed at equal spacing, pairwise meet without a common point. The theorem is special to the line, which is why [circular-arc coloring](/circular-arc-coloring/) is harder.
- **Pairs are needed.** Some two intervals not meeting is enough to have no common point, so the pairwise condition cannot be weakened.

## History

Helly proved the theorem for convex sets in $d$ dimensions, published in 1923, and the case $d = 1$ is the statement for intervals. Golumbic's book uses it for interval graphs: it makes each clique a set of intervals through one point and gives the linear order of the maximal cliques.

## References
