---
tag: MEYRRB
kind: theorem
slug: k-center-hardness
name: Hardness of k-center approximation
aliases:
- 2-epsilon hardness of k-center
- 2-epsilon hardness of max-diameter clustering
area: machine-learning/clustering
level: advanced
summary: "No (2 - epsilon)-approximation exists for the largest cluster radius or diameter in a metric unless P = NP; farthest-first reaches 2."
prereqs: [k-center-problem, metric-space, dominating-set]
see_also: [k-center-inapproximability, gonzalez-k-center, k-median-problem, clustering-problem, complete-linkage-clustering, graph-coloring, k-means-plus-plus]
sources:
  - paper: doi:10.1016/0166-218X(79)90044-1
    title: "W.-L. Hsu and G. L. Nemhauser, Easy and hard bottleneck location problems, Discrete Applied Mathematics 1(3), 1979"
    locator: the NP-hardness of approximating the k-center radius within a factor below 2
  - paper: doi:10.1016/0304-3975(85)90224-5
    title: "T. F. Gonzalez, Clustering to minimize the maximum intercluster distance, Theoretical Computer Science 38, 1985"
    locator: the farthest-first algorithm, its ratio 2 for the largest cluster diameter, and the NP-hardness of the ratio 2 - ε for that objective
  - paper: doi:10.1287/moor.10.2.180
    title: "D. S. Hochbaum and D. B. Shmoys, A best possible heuristic for the k-center problem, Mathematics of Operations Research 10(2), 1985"
    locator: the threshold 2-approximation for the radius and the remark that 2 is best possible unless P = NP
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.2 (the greedy algorithm for k-center and the hardness from dominating set)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A1.1, problems GT2 (dominating set) and GT15 (partition into cliques)
  - paper: "T. Feder and D. H. Greene, Optimal algorithms for approximate clustering, Proceedings of the 20th ACM Symposium on Theory of Computing (STOC), 1988"
    title: Feder and Greene 1988
    locator: the smaller hardness thresholds for points in the plane
---

The hardness of k-center approximation says that, for each $\varepsilon > 0$, no polynomial algorithm clusters points of a [metric space](/metric-space/) into $k$ groups with a largest cluster radius within $2 - \varepsilon$ of the optimum, unless P = NP; the same holds for the largest cluster diameter. The radius result is from Hsu and Nemhauser (1979), the diameter result from Gonzalez (1985), and both follow from gap reductions in which every distance is 1 or 2. The farthest-first traversal reaches the factor 2 for both objectives, so 2 is the exact threshold. The approximation area states the radius result with its non-metric extension on [k-center inapproximability](/k-center-inapproximability/); this page is the clustering view, with both objectives side by side and their 2-approximation.

## Statement

The data model is a finite set $X$ of $n$ points with a metric $d$ (symmetric, zero exactly on the diagonal, with the triangle inequality), and an integer $k$ with $1 \le k < n$. The number of clusters $k$ is given. Two clustering objectives measure the worst cluster:

- **Largest radius ([k-center](/k-center-problem/)).** Choose centers $C \subseteq X$ with $|C| \le k$ and minimize $r(C) = \max_{x \in X} \min_{c \in C} d(x, c)$. Its optimum is $\mathrm{OPT}_r$.
- **Largest diameter.** Partition $X$ into at most $k$ clusters $X_1, \ldots, X_k$ and minimize $\max_j \max_{x, y \in X_j} d(x, y)$. Its optimum is $\mathrm{OPT}_D$.

A ratio $\rho$ means that the algorithm returns a solution of value at most $\rho$ times the optimum, on every input.

**Theorem.** Let $0 < \varepsilon \le 1$.

1. (Hsu and Nemhauser 1979.) If a polynomial algorithm has ratio $2 - \varepsilon$ for the largest radius, then P = NP.
2. (Gonzalez 1985.) If a polynomial algorithm has ratio $2 - \varepsilon$ for the largest diameter, then P = NP.
3. (Gonzalez 1985; Hochbaum and Shmoys 1985 for the radius by another method.) The farthest-first traversal returns centers $C$ with $r(C) \le 2\,\mathrm{OPT}_r$, and its clusters, each point with its nearest center, have largest diameter at most $2\,\mathrm{OPT}_D$. It takes $O(nk)$ distance evaluations.

Parts 1 and 2 hold already for metrics with all distances between distinct points in $\{1, 2\}$.

## In plain words

You want to split a set of points into a few groups so that the worst group is small. "Small" can mean that every point is near the middle of its group, or that every two points in a group are near each other. For both meanings, a cheap greedy method finds groups at most twice as wide as the best ones: start anywhere, and again and again take the point farthest from those taken so far.

The theorem says that nothing fast can promise less than twice, unless a large family of hard puzzles all have fast solutions. The reason is a set of inputs in which every distance is one or two. On those inputs, the best width is one or two, and to tell which is the same as to solve a known hard graph puzzle.

## Proof

Both reductions start from a graph $H = (V, E)$ with $n$ vertices and an integer $k$ with $1 \le k < n$, and build the metric

$$d(u, v) = \begin{cases} 0 & u = v, \\ 1 & \{u, v\} \in E, \\ 2 & \text{otherwise}, \end{cases}$$

on $X = V$, in $O(n^2)$ time. It is a metric: for distinct $u, v, w$, $d(u, w) \le 2 \le d(u, v) + d(v, w)$, because each distance between distinct points is at least 1; if two of the three points are equal, the inequality is an equality or reads $d(u, w) \le d(u, w)$.

*Values of the optima.* Every value of either objective lies in $\{0, 1, 2\}$. It is not 0: since $k < n$, some cluster holds two distinct points, and some point is not a center. So $\mathrm{OPT}_r, \mathrm{OPT}_D \in \{1, 2\}$.

*Part 1.* A center set $C$ with $|C| \le k$ has $r(C) = 1$ exactly when each point outside $C$ is at distance 1 from a center, that is, when $C$ is a [dominating set](/dominating-set/) of $H$. So $\mathrm{OPT}_r = 1$ if $H$ has a dominating set of size at most $k$, and $\mathrm{OPT}_r = 2$ otherwise. Run the assumed algorithm. In the first case it returns a radius at most $2 - \varepsilon < 2$, so the radius 1. In the second case every radius is 2. So the algorithm decides dominating set, which is NP-complete (Garey and Johnson, GT2), in polynomial time.

*Part 2.* A cluster has diameter at most 1 exactly when each two of its points are adjacent in $H$, that is, when it is a clique. So $\mathrm{OPT}_D = 1$ if the vertices of $H$ split into at most $k$ cliques, and $\mathrm{OPT}_D = 2$ otherwise. A partition into $k$ cliques of $H$ is the same as a proper coloring of the complement graph with $k$ colors, so the question is NP-complete for each fixed $k \ge 3$ ([graph coloring](/graph-coloring/); Garey and Johnson, GT15). An algorithm with ratio $2 - \varepsilon$ returns diameter 1 in the first case and 2 in the second, and so decides it.

*Part 3.* Let the traversal choose $c_1, \ldots, c_t$ with $t \le k$, each $c_{i+1}$ a point farthest from $\{c_1, \ldots, c_i\}$, stopping early when that distance is 0. Let $C$ be the chosen set and $r = r(C)$. If $r = 0$ both claims hold. Otherwise $t = k$. Let $f$ be a point with $d(f, C) = r$. When $c_j$ was chosen, it was farthest from $\{c_1, \ldots, c_{j-1}\}$, and distances to a growing set never increase, so $d(c_i, c_j) \ge r$ for $i < j$. With $f$, the $k + 1$ points $c_1, \ldots, c_k, f$ are pairwise at distance at least $r$.

- *Radius.* Some optimal center serves two of the $k + 1$ points, $u$ and $v$, by the pigeonhole principle. Then $r \le d(u, v) \le 2\,\mathrm{OPT}_r$.
- *Diameter.* Some optimal cluster holds two of the $k + 1$ points, so $r \le \mathrm{OPT}_D$. In the traversal's clusters, two points $x, y$ with the same center $c$ have $d(x, y) \le d(x, c) + d(c, y) \le 2r \le 2\,\mathrm{OPT}_D$.

Each of the $k$ rounds updates $n$ nearest distances, so the traversal makes $O(nk)$ distance evaluations. $\blacksquare$

### Example

Let $H$ be the 5-cycle $0 - 1 - 2 - 3 - 4 - 0$. Its domination number is 2 (for example $\{0, 2\}$), and it needs 3 cliques to cover its vertices, because its cliques are single edges and single vertices. So the metric of the proof has

| $k$ | $\mathrm{OPT}_r$ | $\mathrm{OPT}_D$ |
|---|---|---|
| 1 | 2 | 2 |
| 2 | 1 | 2 |
| 3 | 1 | 1 |

For $k = 2$ the two objectives disagree: two centers reach every point at distance 1, but any split into two groups puts two non-adjacent vertices together. The implementation checks the table and both reductions against brute force on random graphs, and checks part 3 on random shortest-path metrics with rational weights.

## Consequences

- **The threshold is exactly 2 for both objectives.** In clustering, these are the objectives of the worst cluster. The [farthest-first traversal](/gonzalez-k-center/) is optimal among polynomial algorithms for them in the worst case, unless P = NP.
- **No approximation scheme.** The gap is a full factor of 2, so neither objective has a [PTAS](/ptas/) in general metrics.
- **Greedy merging has no such guarantee by this argument.** [Complete linkage clustering](/complete-linkage-clustering/) also aims at small diameters, but it merges greedily from the bottom and the factor 2 proof above does not apply to it.
- **Seeding.** The farthest-first order is the deterministic relative of the seeding of [k-means++](/k-means-plus-plus/), which picks the next center with probability proportional to the squared distance instead of taking the farthest point. Farthest-first itself is fragile with outliers, because the farthest point is often an outlier.
- **Other objectives.** For the sum objectives the gap is smaller: [k-median](/k-median-problem/) is hard to approximate below $1 + 2/e$, not 2.

## Tightness

The constant 2 in parts 1 and 2 cannot be raised, because part 3 reaches it. The factor 2 of the traversal is also tight for the traversal itself: on the line points $0, 1, 2$ with $k = 1$ and the first center 0, the radius is 2 while the center 1 gives 1.

The theorem needs a general metric. For points in the plane, Feder and Greene (1988) showed smaller thresholds (about 1.822 for the radius under the Euclidean distance), and the factor 2 remains the best known ratio. The condition $k < n$ excludes only the trivial case $k = n$ with value 0.

## History

Hsu and Nemhauser (1979) proved the hardness for bottleneck location problems, which includes the radius objective. Gonzalez (1985) introduced the farthest-first traversal for the largest diameter objective, proved its ratio 2, and showed that $2 - \varepsilon$ is NP-hard for that objective. In the same year Hochbaum and Shmoys gave the threshold algorithm for the radius, with ratio 2, under a title that calls it best possible. Williamson and Shmoys (Section 2.2) give the radius reduction as a textbook result.

## References
