---
tag: EM0041
kind: concept
slug: triangle-inequality
name: Triangle inequality
aliases:
- triangle inequality pruning
area: searching/similarity-search
level: intro
summary: The distance axiom d(x,z) ≤ d(x,y)+d(y,z) that lets metric indexes prune candidates.
prereqs: [metric-space]
see_also: [metric-space-indexing, pivot-based-indexing, vantage-point-tree, m-tree, ball-tree, similarity-range-query, nearest-neighbor-search, bk-tree]
sources:
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (the lower bound |d(p,q) − d(p,x)| ≤ d(q,x) used to discard elements, the pivot-based and clustering-based families, and AESA)
  - book: isbn:9780387291468
    title: Pavel Zezula, Giuseppe Amato, Vlastislav Dohnal and Michal Batko, Similarity Search, The Metric Space Approach, Springer, 2006
    locator: Chapter 1, Foundations of Metric Space Searching (the object-pivot, range-pivot, pivot-pivot and double-pivot distance constraints, ball and generalized hyperplane partitioning)
  - book: isbn:9780123694461
    title: Hanan Samet, Foundations of Multidimensional and Metric Data Structures, Morgan Kaufmann, 2006
    locator: Chapter 4, Section 4.5, Distance-Based Indexing Methods (the pruning rules for ball partitioning and for generalized hyperplane partitioning)
  - paper: Charles Elkan, Using the triangle inequality to accelerate k-means, Proceedings of the 20th International Conference on Machine Learning (ICML), 2003
    locator: pages 147 to 153 (the lemmas that skip distance computations in Lloyd's algorithm)
---

The triangle inequality says that in a [metric space](/metric-space/) a detour is never shorter than the direct way: $d(x, z) \le d(x, y) + d(y, z)$ for all points $x$, $y$ and $z$. Rearranged, it gives a lower bound on an unknown distance from two known ones, $d(q, x) \ge |d(q, p) - d(p, x)|$. Every exact [metric space index](/metric-space-indexing/) uses such bounds to skip objects without computing their distance to the query. When the distance function breaks the inequality, these indexes return wrong answers.

## In plain words

Three towns are joined by straight roads. The road from the first town to the third is never longer than the trip through the second town. This simple rule is the triangle inequality.

It is useful in search because it works in reverse. Say you know that a town is 100 kilometers from a landmark, and a shop is 3 kilometers from the same landmark. Then the shop is at least 97 kilometers from the town, and you know this without measuring. If you look for shops within 5 kilometers of the town, you can skip this shop.

A search index stores the distances from each object to a few landmarks when it is built. At query time it measures the distance from the query to the landmarks only. Then it removes every object that is too far by this rule, and measures only the objects that remain.

## The idea

Let $(M, d)$ be a metric space. The triangle inequality is the axiom

$$d(x, z) \le d(x, y) + d(y, z) \qquad \text{for all } x, y, z \in M.$$

**Lemma 1 (the two-sided bound).** For all $q, p, x \in M$,

$$|d(q, p) - d(p, x)| \le d(q, x) \le d(q, p) + d(p, x).$$

*Proof.* The right inequality is the axiom with the path $q, p, x$. For the left one, the axiom with the path $q, x, p$ gives $d(q, p) \le d(q, x) + d(x, p)$, so $d(q, p) - d(p, x) \le d(q, x)$ by symmetry. The axiom with the path $p, q, x$ gives $d(p, x) \le d(p, q) + d(q, x)$, so $d(p, x) - d(q, p) \le d(q, x)$. The larger of the two left sides is $|d(q, p) - d(p, x)|$. $\square$

In search, $p$ is a **pivot** (also called a vantage point or a landmark), $q$ is the query and $x$ is a stored object. The index stores $d(p, x)$ at build time. At query time it computes $d(q, p)$ once. Then Lemma 1 gives an interval for $d(q, x)$ with no more distance evaluations.

**Rule 1 (exclude).** In a [range query](/similarity-range-query/) of radius $r$, if $|d(q, p) - d(p, x)| > r$, then $x$ is not an answer. With $k$ pivots $p_1, \ldots, p_k$ the best bound is $\max_i |d(q, p_i) - d(p_i, x)|$. This is the $\ell_\infty$ distance between the vectors $(d(q, p_i))_i$ and $(d(x, p_i))_i$, which is the base of [pivot-based indexing](/pivot-based-indexing/).

**Rule 2 (include).** If $d(q, p) + d(p, x) \le r$, then $x$ is an answer, and its distance need not be computed.

**Lemma 2 (balls).** Let every object of a set $S$ lie in the ball $B(c, R)$, that is $d(c, x) \le R$ for each $x \in S$. Then $d(q, x) \ge d(q, c) - R$ for each $x \in S$.

*Proof.* By Lemma 1, $d(q, x) \ge d(q, c) - d(c, x) \ge d(q, c) - R$. $\square$

So a range query of radius $r$ skips the whole set when $d(q, c) > R + r$, and a nearest neighbor search skips it when $d(q, c) - R$ is at least the best distance found so far. The [ball tree](/ball-tree/) and the [M-tree](/m-tree/) store such covering balls. A [vantage-point tree](/vantage-point-tree/) uses the same rule on a ring: if every $x$ of a subtree has $a \le d(p, x) \le b$, then $d(q, x) \ge \max(a - d(q, p),\ d(q, p) - b,\ 0)$.

**Lemma 3 (generalized hyperplanes).** Let $p_1, p_2 \in M$, and let $x$ be at least as close to $p_1$ as to $p_2$, that is $d(x, p_1) \le d(x, p_2)$. Then $d(q, x) \ge (d(q, p_1) - d(q, p_2)) / 2$.

*Proof.* By the axiom, $d(q, p_1) \le d(q, x) + d(x, p_1) \le d(q, x) + d(x, p_2) \le d(q, x) + d(x, q) + d(q, p_2)$. So $d(q, p_1) - d(q, p_2) \le 2\, d(q, x)$. $\square$

So a range query skips the side of $p_1$ when $d(q, p_1) - d(q, p_2) > 2r$. The [GNAT](/gnat/) and the generalized hyperplane tree split the data this way.

**When the axiom fails.** If $d$ only satisfies a *relaxed* triangle inequality $d(x, z) \le \rho\,(d(x, y) + d(y, z))$ with $\rho \ge 1$, the same steps give $d(q, x) \ge d(q, p)/\rho - d(p, x)$, a weaker bound. The squared Euclidean distance satisfies it with $\rho = 2$, since $(a + b)^2 \le 2a^2 + 2b^2$ by $(a - b)^2 \ge 0$, and the Euclidean distance satisfies the axiom with $a = d_2(x, y)$ and $b = d_2(y, z)$. An index that uses Rule 1 with a distance that breaks the axiom can skip a true answer: it gives fast answers that are wrong.

## Examples

**Exclusion with one pivot.** In the plane with the Euclidean distance, take the pivot $p = (0, 0)$, the query $q = (6, 8)$ and the radius $r = 2$. Then $d(q, p) = 10$. The index has stored $d(p, x)$ for six objects.

| object | $x$ | $d(p, x)$ | lower bound $\lvert 10 - d(p, x) \rvert$ | decision | true $d(q, x)$ |
|---|---|---|---|---|---|
| a | (3, 0) | 3 | 7 | skip | 8.5440 |
| b | (0, 7) | 7 | 3 | skip | 6.0828 |
| c | (5, 6) | 7.8102 | 2.1898 | skip | 2.2361 |
| d | (9, 0) | 9 | 1 | compute | 8.5440 |
| e | (6, 10) | 11.6619 | 1.6619 | compute | 2 |
| f | (12, 9) | 15 | 5 | skip | 6.0828 |

The query costs 3 distance evaluations (the pivot, d and e) instead of 6, and it reports e. Object d is a false candidate: its lower bound is small, but it is far from $q$. Object c is close to the radius, and the bound still excludes it correctly.

**A second pivot.** Add the pivot $p_2 = (10, 0)$, with $d(q, p_2) = \sqrt{80} \approx 8.9443$ and the stored $d(p_2, d) = 1$. Now d has the lower bound $7.9443 > 2$ and is skipped. The bound for e from $p_2$ is $|8.9443 - 10.7703| = 1.8261$, so e is still computed. With both pivots, the query costs 3 evaluations (two pivots and e), and only true answers are computed.

**A hyperplane.** Let $p_1 = (0, 0)$ and $p_2 = (8, 8)$. For $q = (6, 8)$, $d(q, p_1) = 10$ and $d(q, p_2) = 2$. By Lemma 3, each object at least as close to $p_1$ as to $p_2$ has $d(q, x) \ge (10 - 2)/2 = 4$. A range query with $r = 2$ skips that whole side.

**A failure.** On the line, let the "distance" be $s(x, y) = (x - y)^2$, with the pivot $p = 0$, the query $q = 2$ and the radius $r = 1$. The object $x = 1$ is an answer, since $s(q, x) = 1$. But Rule 1 computes $|s(q, p) - s(p, x)| = |4 - 1| = 3 > 1$ and skips it. The index misses a true answer, because $s$ is not a metric.

## Where it is used

- **[Pivot-based indexing](/pivot-based-indexing/)**: AESA, LAESA and their relatives store distances to pivots and apply Rule 1 with many pivots.
- **Ball partitioning**: the [vantage-point tree](/vantage-point-tree/), the [multi-vantage-point tree](/mvp-tree/) and the [BK-tree](/bk-tree/) prune by rings around a vantage point.
- **Covering balls**: the [ball tree](/ball-tree/), the [M-tree](/m-tree/) and the [cover tree](/cover-tree/) apply Lemma 2.
- **Hyperplane partitioning**: the [GNAT](/gnat/) applies Lemma 3.
- **Queries**: [similarity range queries](/similarity-range-query/) and exact [nearest neighbor search](/nearest-neighbor-search/) in any metric space.
- **Clustering**: Elkan's version of [Lloyd's algorithm](/lloyds-algorithm/) for [k-means](/k-means/) skips most point to center distances by the same lemmas.
- **Approximation**: the [metric TSP](/metric-tsp/) has approximation algorithms, such as the [Christofides algorithm](/christofides-algorithm/), because shortcuts in a tour do not make it longer.

## References
