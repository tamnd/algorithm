---
tag: MFMXQM
kind: algorithm
slug: dbscan
name: DBSCAN
aliases:
- density-based spatial clustering of applications with noise
area: machine-learning/clustering
level: core
summary: "Find clusters as connected groups of core points, which have at least MinPts points within distance eps; mark points far from all core points as noise."
solves: [density-based-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features}
  time: {worst: "Θ(n^2 d)", best: "Θ(n^2 d)"}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 1996
  people: [Martin Ester, Hans-Peter Kriegel, Jörg Sander, Xiaowei Xu]
  note: Ester, Kriegel, Sander and Xu presented DBSCAN at KDD 1996. It received the KDD test of time award in 2014.
prereqs: [density-based-clustering-problem, fixed-radius-near-neighbors, connected-components]
see_also: [optics, hdbscan, single-linkage-clustering, denclue, mean-shift, k-means, kd-tree, r-star-tree]
sources:
  - paper: "Martin Ester, Hans-Peter Kriegel, Jörg Sander and Xiaowei Xu, A density-based algorithm for discovering clusters in large spatial databases with noise, Proceedings of the Second International Conference on Knowledge Discovery and Data Mining (KDD-96), AAAI Press, 1996"
    locator: "pp. 226 to 231; Section 3 (Definitions 1 to 6, Lemmas 1 and 2) and Section 4 (the algorithm, the run time claim and the sorted k-dist graph)"
  - paper: doi:10.1145/3068335
    title: "Erich Schubert, Jörg Sander, Martin Ester, Hans-Peter Kriegel and Xiaowei Xu, DBSCAN revisited, revisited: why and how you should (still) use DBSCAN, ACM Transactions on Database Systems 42(3), 2017"
    locator: Article 19 (the abstract form of the algorithm, the worst case of Θ(n^2) region query work, and the advice on the parameters)
  - paper: doi:10.1145/2723372.2737792
    title: "Junhao Gan and Yufei Tao, DBSCAN revisited: mis-claim, un-fixability, and approximation, Proceedings of ACM SIGMOD 2015"
    locator: the reduction from unit-spherical emptiness checking (the Ω(n^(4/3)) barrier for d at least 3), the O(n log n) algorithm in the plane, and ρ-approximate DBSCAN
  - paper: doi:10.1002/widm.30
    title: "Hans-Peter Kriegel, Peer Kröger, Jörg Sander and Arthur Zimek, Density-based clustering, WIREs Data Mining and Knowledge Discovery 1(3), 2011"
    locator: pp. 231 to 240 (a survey of DBSCAN and its descendants)
---

DBSCAN is a [density-based clustering](/density-based-clustering-problem/) algorithm with two parameters, a radius $\varepsilon$ and a count $\mathit{MinPts}$. A point with at least $\mathit{MinPts}$ points within distance $\varepsilon$ is a *core point*. Clusters are the [connected components](/connected-components/) of the core points under the relation "within $\varepsilon$", together with the non-core points near them, and the remaining points are *noise*. With brute force [range queries](/fixed-radius-near-neighbors/) it makes $n$ queries and costs $\Theta(n^2 d)$ time in the [real RAM](/real-ram/) model; the number of clusters is an output, not an input.

## In plain words

Look at each point and count how many points lie in a small circle around it. If the count is large enough, the point sits in a crowded area. Call it a core point.

Two core points that are close to each other belong to the same group. Follow these links from core point to core point, and you get one group. A group can have any shape: a ring, a long curve, a blob.

A point that is not crowded itself, but is close to a core point, joins that group at its edge. A point that is far from every core point is noise and joins no group.

You choose the size of the circle and the count. You do not choose the number of groups.

## The problem

The data model is clustering of points: the input is a set $D = \{x_1, \ldots, x_n\}$ of points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), or in any [metric space](/metric-space/), a radius $\varepsilon > 0$ and an integer $\mathit{MinPts} \ge 1$. The number of clusters $k$ is not given. Ester et al. (1996, Section 3) define:

- The $\varepsilon$-neighborhood $N_\varepsilon(p) = \{q \in D : \mathrm{dist}(p, q) \le \varepsilon\}$. It holds $p$ itself.
- $p$ is a **core point** if $|N_\varepsilon(p)| \ge \mathit{MinPts}$.
- $q$ is **directly density-reachable** from $p$ if $p$ is a core point and $q \in N_\varepsilon(p)$.
- $q$ is **density-reachable** from $p$ if there is a chain $p = p_1, p_2, \ldots, p_m = q$ in which each $p_{t+1}$ is directly density-reachable from $p_t$. This relation is not symmetric: a non-core point $q$ near a core point $p$ is reachable from $p$, but $p$ is not reachable from $q$, because no chain starts at a non-core point.
- $p$ and $q$ are **density-connected** if some point $o$ has both $p$ and $q$ density-reachable from it. This relation is symmetric.
- A **cluster** is a non-empty set $C \subseteq D$ that is maximal (if $p \in C$ and $q$ is density-reachable from $p$, then $q \in C$) and connected (each two points of $C$ are density-connected). **Noise** is the set of points in no cluster.

Lemmas 1 and 2 of the paper show that a cluster is the set of points density-reachable from any one of its core points. So, in graph words: let $G$ be the graph on the core points with an edge between two core points at distance at most $\varepsilon$. Each component $K$ of $G$ gives one cluster, $K$ together with the *border points*, the non-core points within $\varepsilon$ of a point of $K$. Noise is the non-core points with no core point within $\varepsilon$. A border point can be within $\varepsilon$ of two components, so the clusters of the definition can overlap at border points. The algorithm gives such a point to one of them.

## The algorithm

```pseudo id=main
DBSCAN(D, ε, MinPts)
L1  label[p] ← UNDEFINED for each point p; C ← 0
L2  for each point i of D, in input order do
L3      if label[i] ≠ UNDEFINED then continue
L4      N ← RANGE-QUERY(i, ε)                 ▷ N_ε(i), with i in it
L5      if |N| < MinPts then label[i] ← NOISE; continue
L6      C ← C + 1; label[i] ← C; Q ← an empty queue
L7      for each j in N do CLAIM(j, C, Q)
L8      while Q is not empty do
L9          q ← DEQUEUE(Q)
L10         N' ← RANGE-QUERY(q, ε)
L11         if |N'| ≥ MinPts then             ▷ q is a core point
L12             for each j in N' do CLAIM(j, C, Q)
L13 return label

CLAIM(j, C, Q)
L14 if label[j] = NOISE then label[j] ← C            ▷ a border point found late
L15 else if label[j] = UNDEFINED then label[j] ← C; ENQUEUE(Q, j)
```

Each run of lines L6 to L12 grows one cluster from an unlabeled core point by a [breadth-first search](/breadth-first-search/) of the density-reachable points. Line L5 marks a non-core point as NOISE for now. If a later cluster reaches it, line L14 turns it into a border point of that cluster, without a new query, because it is already known to be non-core. Line L15 puts a point in the queue only when it was UNDEFINED, so each point is queried exactly once.

**Tie rule and order.** A border point within $\varepsilon$ of core points of two clusters goes to the cluster that reaches it first. This depends on the order of the input. The core points, the partition of the core points into clusters, and the noise do not depend on the order.

## Example

Take $\varepsilon = 1.5$ and $\mathit{MinPts} = 4$, with the Euclidean distance, on these 11 points:

| point | coordinates | $N_\varepsilon$ | size | type | label |
|---|---|---|---|---|---|
| a | (0, 0) | a, b, c, d | 4 | core | 1 |
| b | (1, 0) | a, b, c, d, e | 5 | core | 1 |
| c | (0, 1) | a, b, c, d | 4 | core | 1 |
| d | (1, 1) | a, b, c, d, e | 5 | core | 1 |
| e | (2, 1) | b, d, e | 3 | border | 1 |
| f | (6, 6) | f, g, h, i | 4 | core | 2 |
| g | (7, 6) | f, g, h, i | 4 | core | 2 |
| h | (6, 7) | f, g, h, i | 4 | core | 2 |
| i | (7, 7) | f, g, h, i | 4 | core | 2 |
| j | (4, 4) | j | 1 | noise | NOISE |
| k | (9, 0) | k | 1 | noise | NOISE |

The diagonal of a unit square is $\sqrt 2 \approx 1.414 \le 1.5$, so a and d are neighbors, and so are b and e. The point e is at distance 2 from c and $\sqrt 5 \approx 2.24$ from a, so its neighborhood has only 3 points.

The scan starts at a: $|N_\varepsilon(a)| = 4$, so a is core and starts cluster 1. Line L7 puts b, c and d in the queue. The query of b finds 5 points, so b is core, and e enters the queue. The queries of c and d find core points again and add nothing new. The query of e finds 3 points, so e is not core: it stays in cluster 1 as a border point, and its neighbors are not added. The scan then skips b to e, starts cluster 2 at f, and labels f, g, h and i. The queries of j and k find only the point itself, so they are noise. In total the algorithm made 11 range queries, one for each point.

**Order dependence.** On the line, take the points 0, 3, 6, 9, 15, 21, 24, 27, 30 with $\varepsilon = 6$ and $\mathit{MinPts} = 4$. The points 3, 6, 9, 21, 24 and 27 are core. The point 15 has the neighbors 9 and 21 only, so it is a border point of both groups. In this order 15 joins the cluster of 9. With the input reversed, it joins the cluster of 21. The core points and the noise (none here) are the same in both runs.

## Correctness

The claim has four parts. Each point gets one label. Two core points share a label if and only if they are in the same component of the core graph $G$. A point is NOISE if and only if it is not core and no core point lies within $\varepsilon$ of it. A border point gets the label of a core point within $\varepsilon$ of it. The proof first shows that a cluster label never changes and that each point is queried exactly once, so each core point calls CLAIM on its whole neighborhood. Then the core points with one label are joined in $G$, by induction on the order of labeling. Conversely, a first core point on a path in $G$ that misses the label would contradict the CLAIM calls of its predecessor. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with one unit for each arithmetic operation and comparison on reals. Here $n$ is the number of points and $d$ the number of features.

- **Range queries.** The algorithm makes exactly $n$ range queries. CLAIM runs $\sum_{p \text{ core}} |N_\varepsilon(p)| \le n^2$ times. The queue holds each point at most once, so the extra space is $\Theta(n)$ besides the input.
- **Brute force.** A query compares the point with all $n$ points, in $\Theta(d)$ time each, so the time is $\Theta(n^2 d)$ in every case.
- **With an index.** A [k-d tree](/kd-tree/), an [R\*-tree](/r-star-tree/) or a grid answers a [circular range query](/circular-range-searching/) faster when the neighborhoods are small. The original paper says that a region query on an R\*-tree takes $O(\log n)$ time on average, and concludes an average run time of $O(n \log n)$. This is not a worst case bound. The output of the $n$ queries alone has size $\sum_p |N_\varepsilon(p)|$, which is $\Theta(n^2)$ when $\varepsilon$ is large enough that each point has a constant fraction of the data in its neighborhood. Schubert et al. (2017) state the worst case of the algorithm as $O(n^2)$ even with an index, and the index queries degrade in high dimensions.
- **Lower bound for exact DBSCAN.** Gan and Tao (2015) reduce unit-spherical emptiness checking, a problem of the Hopcroft type, to DBSCAN in $\mathbb{R}^3$. So any algorithm, not only this one, that computes the exact DBSCAN clusters in $\mathbb{R}^d$ for $d \ge 3$ in $o(n^{4/3})$ time would solve that problem in $o(n^{4/3})$ time, which is believed to be impossible. This is a conditional lower bound of $\Omega(n^{4/3})$, not an unconditional one. In the plane, exact DBSCAN takes $O(n \log n)$ time, with a grid of cells of side $\varepsilon / \sqrt 2$ and nearest neighbor structures between cells (Gan and Tao 2015, after a thesis of Gunawan, 2013).
- **Approximation.** Gan and Tao define $\rho$-approximate DBSCAN, which may also join two core points at distance up to $(1 + \rho)\varepsilon$, and compute it in $O(n)$ expected time for a fixed dimension $d$ and a fixed $\rho > 0$.

## Properties

- **Determinism.** Core points, the partition of the core points and the noise are determined by $\varepsilon$ and $\mathit{MinPts}$. Only the border points within $\varepsilon$ of two clusters and the numbering of the clusters depend on the order.
- **Arbitrary shapes.** A cluster follows any chain of dense points, so it can be a ring or a curve. [k-means](/k-means/) cannot find such clusters, because its clusters are cells of a Voronoi diagram.
- **Noise.** Points in sparse regions get no cluster, so a few outliers do not pull a cluster toward them, as they pull a mean in k-means.
- **Link to single linkage.** With $\mathit{MinPts} \le 2$, every point that has another point within $\varepsilon$ is core, so the clusters are the components of the graph "distance at most $\varepsilon$" with at least 2 points (with $\mathit{MinPts} = 1$, also the single points). This is the [single linkage](/single-linkage-clustering/) clustering cut at height $\varepsilon$.
- **One density level.** One pair $(\varepsilon, \mathit{MinPts})$ fixes one density threshold. Clusters of very different densities cannot all be found with one setting: [OPTICS](/optics/) and [HDBSCAN](/hdbscan/) handle all thresholds at once.
- **Monotone in $\varepsilon$.** For a fixed $\mathit{MinPts}$, each core point at $\varepsilon$ is core at each larger $\varepsilon'$, and each cluster at $\varepsilon$ lies inside a cluster at $\varepsilon'$, up to border points. This nesting is what OPTICS uses.

## Variants and improvements

- **GDBSCAN.** Sander, Ester, Kriegel and Xu (1998) replace the neighborhood by any reflexive and symmetric predicate and the count by any weight, for polygons and other spatial objects.
- **DBSCAN\*.** Campello, Moulavi and Sander (2013) drop the border points: a non-core point is always noise. The clusters are then exactly the components of $G$, and the result does not depend on the order. This is the flat clustering behind [HDBSCAN](/hdbscan/).
- **OPTICS.** [OPTICS](/optics/) computes one ordering from which the DBSCAN clusters for every $\varepsilon' \le \varepsilon$ can be read.
- **Grid and index acceleration.** A grid with cells of side $\varepsilon / \sqrt d$ makes all points of a cell neighbors of each other, so a dense cell needs no distance computations inside it.
- **Parallel and distributed DBSCAN.** The core graph can be built with [union-find](/disjoint-set/) on partitions of the data, then merged, since components are what matters.

## When to use it

Use DBSCAN when the clusters are dense regions of any shape, when the data has noise or outliers, when you do not know the number of clusters, and when the dimension is low enough for a distance to be meaningful and for a spatial index to work. Avoid it when the clusters have very different densities, when the dimension is high, or when every point must get a cluster.

## Pitfalls

- **Does MinPts count the point itself?** In the original paper and in scikit-learn (`min_samples`) it does. Some implementations count only the other points. The two conventions differ by one, so state which one you use.
- **$\le$ against $<$.** The paper uses $\mathrm{dist}(p, q) \le \varepsilon$. With $<$, points at exactly $\varepsilon$ change from neighbors to non-neighbors, which matters on integer or grid data.
- **Choosing $\varepsilon$.** The paper suggests the sorted $k$-dist graph: sort the distances of each point to its $k$-th nearest neighbor and pick $\varepsilon$ at the "knee", with $\mathit{MinPts} = k + 1$ counting the point itself (the paper used 4-dist and $\mathit{MinPts} = 4$ for 2D data). Schubert et al. (2017) suggest $\mathit{MinPts} = 2d$ as a start. A too small $\varepsilon$ makes most points noise. A too large one merges all clusters and makes the run quadratic.
- **Unscaled features.** The radius is the same in every direction. Standardize the features first.
- **High dimension.** Distances concentrate in high dimension, so the neighborhoods are either almost empty or almost everything (see [curse of dimensionality](/curse-of-dimensionality/)).
- **Treating border labels as stable.** Do not compare two runs by the label of border points. Compare the core points, or use DBSCAN\*.
- **Quadratic memory.** An implementation that first stores all neighborhoods uses $\Theta(n^2)$ memory when $\varepsilon$ is large. Query the neighborhoods one at a time, as in the pseudocode.

## Implementations

## History

Martin Ester, Hans-Peter Kriegel, Jörg Sander and Xiaowei Xu, at the University of Munich, presented DBSCAN at the KDD conference in 1996, for clusters of any shape in spatial databases with noise. They gave the definitions of density-reachability and density-connectivity and an algorithm built on R\*-tree region queries. Sander, Ester, Kriegel and Xu generalized it as GDBSCAN in 1998, and Ankerst, Breunig, Kriegel and Sander built OPTICS on it in 1999. Gan and Tao showed in 2015 that the claimed $O(n \log n)$ time does not hold in the worst case and gave the $n^{4/3}$ barrier for $d \ge 3$. Schubert, Sander, Ester, Kriegel and Xu replied in 2017 with a discussion of the run time in practice and advice on the parameters.

## References
