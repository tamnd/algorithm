---
tag: G9NW7V
kind: algorithm
slug: bfr-algorithm
name: BFR algorithm
aliases:
- Bradley-Fayyad-Reina algorithm
- scalable k-means of Bradley, Fayyad and Reina
area: machine-learning/clustering
level: advanced
summary: Scalable k-means for data that does not fit in memory, using discard, compression and retained sets.
solves: [k-means-problem]
model: external-memory-model
complexity:
  vars: {n: the number of points, k: the number of clusters, d: the dimension, b: the chunk size, t: "the number of chunks (about n / b)", r: the most summaries in CS and RS together, I: the number of k-means iterations on the first chunk}
  time: {worst: "O(n (k + r) d + t r^3 d + I b k d)"}
  space: {extra: "O(b d + (k + r) d)"}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1998
  people: [Paul S. Bradley, Usama M. Fayyad, Cory Reina]
  note: Bradley, Fayyad and Reina of Microsoft Research presented the method at KDD 1998 as a k-means that reads a large database once with a fixed memory buffer.
prereqs: [k-means, k-means-problem, external-memory-model]
see_also: [k-means, birch, clustering-feature-tree, streaming-k-median, mini-batch-k-means, gaussian-mixture-model, canopy-clustering, cure]
sources:
  - paper: "P. S. Bradley, U. M. Fayyad and C. Reina, Scaling clustering algorithms to large databases, Proceedings of KDD 1998, pp. 9-15"
    title: Bradley, Fayyad and Reina 1998
    locator: the buffer, primary compression (discard set), secondary compression (sub-clusters) and the retained set
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition
    locator: "Section 7.3, The algorithm of Bradley, Fayyad and Reina (7.3.4 to 7.3.6)"
  - paper: "T. Zhang, R. Ramakrishnan and M. Livny, BIRCH: an efficient data clustering method for very large databases, Proceedings of SIGMOD 1996, pp. 103-114"
    title: Zhang, Ramakrishnan and Livny 1996
    locator: the clustering feature (N, LS, SS), which BFR keeps per dimension
---

The BFR algorithm of Bradley, Fayyad and Reina is a version of [k-means](/k-means/) for data that is too large for memory. It reads the data in chunks and keeps no points after a chunk, only summaries. Each summary holds three statistics per dimension: the count $N$, the sum $\mathrm{SUM}$ and the sum of squares $\mathrm{SUMSQ}$. From these it knows the centroid and the variance in each dimension. A point that is close to a cluster in the sense of the Mahalanobis distance is added to that cluster's summary and then discarded. Points that fit no cluster are kept as small mini-clusters or as single points. BFR assumes that each cluster is close to a Gaussian whose axes are parallel to the coordinate axes. It is a heuristic: it has no bound on the cost.

## In plain words

You must sort a very long list of points into $k$ groups, but you can look at only one part of the list at a time. Sort the first part with k-means. For each group, write down only how many points it has, their sum and the sum of their squares in each coordinate. This is enough to know the center and the spread of the group.

Then read the next part. A point that is well inside a group, compared with that group's spread, is added to the group's three numbers and forgotten. The other points are kept for now. Points that are kept and lie close together are joined into small groups of their own, again stored only as three numbers. Single points that fit nowhere stay as they are.

At the end, each small group and each single point goes to the nearest of the $k$ groups.

## The problem

The input is a set of $n$ points in $\mathbb{R}^d$, read in chunks of size $b$, and the number $k$ of clusters. The goal is the same as in the [k-means problem](/k-means-problem/): $k$ clusters with a small sum of squared distances to their centroids. The memory holds one chunk and $O((k + r)d)$ numbers of summaries, where $r$ is the number of mini-clusters and retained points. Each point is read once, as in the [external memory model](/external-memory-model/) with one scan.

BFR keeps three sets:

- the **discard set** (DS): $k$ summaries, one for each cluster. Their points are discarded.
- the **compressed set** (CS): summaries of mini-clusters, groups of at least two points that are close to each other but not to a DS cluster.
- the **retained set** (RS): single points that fit nowhere yet.

A summary of a point set $P$ is $(N, \mathrm{SUM}, \mathrm{SUMSQ})$ with $\mathrm{SUM}_i = \sum_{x \in P} x_i$ and $\mathrm{SUMSQ}_i = \sum_{x \in P} x_i^2$. The centroid is $\mu_i = \mathrm{SUM}_i / N$ and the variance is $\sigma_i^2 = \mathrm{SUMSQ}_i / N - \mu_i^2$. A point $x$ is close to a summary if its Mahalanobis distance $\sqrt{\sum_i (x_i - \mu_i)^2 / \sigma_i^2}$ is below $\alpha\sqrt{d}$ for a chosen $\alpha$, for example 2 or 3.

## The algorithm

```pseudo id=main
BFR(chunks, k, α, v)         ▷ α: distance threshold; v: largest variance of a mini-cluster
L1  run k-means on the first chunk; DS ← the summaries of its k clusters; CS, RS ← empty
    for each later chunk do
L2      for each point x of the chunk do
L3          s ← the DS summary with the least Mahalanobis distance to x
L4          if that distance is below α√d then add x to s; continue with the next point
L5          if some CS summary has Mahalanobis distance below α√d then add x to the nearest one
L6          else make x a new RS summary with N = 1
L7      while two summaries of CS ∪ RS have the nearest centroids among the pairs whose
            merge has variance at most v in each dimension do merge them;
        CS ← the merged summaries with N ≥ 2;  RS ← the summaries with N = 1
L8  merge each CS and RS summary into the DS summary with the nearest centroid; return DS
```

Adding a point to a summary adds $1$, $x_i$ and $x_i^2$ to the three statistics, and merging two summaries adds them. This additivity is what lets BFR forget the points. Line L7 is the secondary compression: it finds tight groups among the points that are left, and also joins mini-clusters that have come close.

This page follows the description in Mining of Massive Datasets. The original paper also runs k-means again on the buffer together with the summaries, and it decides which points to discard with a confidence interval around each centroid. The three sets and the summaries are the same.

## Example

Take $d = 2$, $k = 2$, $\alpha = 2$ (so the test is: squared Mahalanobis distance below $\alpha^2 d = 8$) and $v = 1$. The first chunk is $(0,0), (2,0), (0,2), (2,2), (10,10), (12,10), (10,12), (12,12)$, and k-means finds the two squares.

| set | $N$ | $\mathrm{SUM}$ | $\mathrm{SUMSQ}$ | centroid | variances |
|---|---|---|---|---|---|
| DS 1 | 4 | $(4, 4)$ | $(8, 8)$ | $(1, 1)$ | $(1, 1)$ |
| DS 2 | 4 | $(44, 44)$ | $(488, 488)$ | $(11, 11)$ | $(1, 1)$ |

The second chunk is $(1, 2), (5, 5), (6, 5), (11, 13)$.

| point | squared distance to DS 1 | to DS 2 | action |
|---|---|---|---|
| $(1, 2)$ | $0 + 1 = 1$ | $100 + 81$ | add to DS 1 |
| $(5, 5)$ | $16/0.8 + 3.8^2/0.96 \approx 35.0$ | $36 + 36 = 72$ | RS |
| $(6, 5)$ | $25/0.8 + 3.8^2/0.96 \approx 46.3$ | $25 + 36 = 61$ | RS |
| $(11, 13)$ | about 270 | $0 + 4 = 4$ | add to DS 2 |

After $(1, 2)$ is added, DS 1 has centroid $(1, 1.2)$ and variances $(0.8, 0.96)$, and the later points are tested against these new values. DS 1 is now $N = 5$, $\mathrm{SUM} = (5, 6)$, $\mathrm{SUMSQ} = (9, 12)$, and DS 2 is $N = 5$, $\mathrm{SUM} = (55, 57)$, $\mathrm{SUMSQ} = (609, 657)$. In line L7 the two RS points would merge into $N = 2$, $\mathrm{SUM} = (11, 10)$, $\mathrm{SUMSQ} = (61, 50)$, with variances $61/2 - 5.5^2 = 0.25$ and $0$, both at most 1. So they form one CS mini-cluster. At the end, line L8 merges this mini-cluster into DS 1, whose centroid $(1, 1.2)$ is nearer to $(5.5, 5)$ than $(11, 11.4)$. The final DS 1 has $N = 7$, $\mathrm{SUM} = (16, 16)$ and $\mathrm{SUMSQ} = (70, 62)$, which are exactly the statistics of its seven points.

## Correctness

The summary of a union of disjoint sets is the sum of their summaries, so each add and merge keeps the summaries exact. The centroid and the variance in each dimension follow from $(N, \mathrm{SUM}, \mathrm{SUMSQ})$, because $\frac{1}{N}\sum (x_i - \mu_i)^2 = \mathrm{SUMSQ}_i / N - \mu_i^2$. Each point goes to exactly one summary, so at all times the summaries partition the points read so far, and at the end the $k$ DS summaries partition all $n$ points. The proof is on the correctness page.

The quality of the clusters is not proved. BFR never moves a point that it has discarded, so the result depends on the first chunk and on the order of the data.

## Complexity

- **Time.** Each point is compared with $k$ DS summaries and up to $r$ CS summaries, in $O(d)$ time each: $O(n(k + r)d)$ in total. Line L7 with the simple pair search here takes $O(r^3 d)$ per chunk. The k-means on the first chunk takes $O(Ibkd)$ for $I$ iterations.
- **Space.** One chunk of $bd$ numbers, and $(2d + 1)$ numbers per summary, so $O(bd + (k + r)d)$. This is independent of $n$ as long as $r$ stays small.
- **Passes.** One pass over the data.

## Properties

- **One pass, fixed memory.** The memory does not grow with $n$ unless many points stay in RS.
- **Axis-aligned Gaussian clusters.** The Mahalanobis test uses only the variance in each dimension, so it fits clusters whose shape is an ellipse with axes along the coordinates. A cluster that is long along a diagonal is tested badly.
- **No bound.** BFR is a heuristic. It finds no k-means local optimum in general.
- **Order dependent.** The first chunk fixes the $k$ clusters, and a point once discarded stays in its cluster.
- **Randomized start.** The k-means on the first chunk uses random seeds; with a fixed seed the whole run is deterministic.

## Variants and improvements

- **The original paper** keeps a buffer, runs k-means on the buffer together with the DS and CS summaries, and discards points whose cluster would not change if the centroids moved within a confidence interval.
- **[BIRCH](/birch/)** uses the same additive statistics, but with one scalar sum of squares, and stores the summaries in a [clustering feature tree](/clustering-feature-tree/).
- **[CURE](/cure/)** keeps several representative points per cluster and can find clusters that are not ellipses.
- **[Mini-batch k-means](/mini-batch-k-means/)** reads small batches and moves the centers by small steps; it does not keep summaries of mini-clusters.
- **[Streaming k-median](/streaming-k-median/)** has a proven constant factor in any metric, for the k-median objective.
- **Full covariance.** Keeping the sums $\sum x_i x_j$ for all pairs allows clusters of any orientation, at a cost of $O(d^2)$ numbers per summary.

## When to use it

Use BFR when the data is too large for memory, $k$ is known, and the clusters are roughly Gaussian with axes along the coordinates, for example after a principal component rotation. If clusters have other shapes, use a method like [CURE](/cure/). If the data fits in memory, plain [k-means](/k-means/) is simpler and can move points between clusters.

## Pitfalls

- **Zero variance.** A cluster with all points equal in some dimension has $\sigma_i = 0$. Use a small floor for the variance.
- **The threshold.** A small $\alpha$ sends many points to RS, so the memory grows. A large $\alpha$ discards points into the wrong cluster.
- **Bad first chunk.** If the first chunk misses a cluster or splits one, BFR cannot repair it later. Shuffle the data or use a large first chunk.
- **Precision.** $\mathrm{SUMSQ}_i / N - \mu_i^2$ subtracts two large numbers and can lose precision or even become negative in floating point. Center the data first or use a stable update.
- **Leftovers.** The last step forces every CS and RS point into a DS cluster. Some programs report them as outliers instead.

## Implementations

## History

Bradley, Fayyad and Reina presented the method at KDD 1998, as part of work at Microsoft Research on clustering large databases with one scan and a fixed buffer. It builds on the clustering features of [BIRCH](/birch/) (1996). Leskovec, Rajaraman and Ullman made a simpler version with the names DS, CS and RS widely known in their book Mining of Massive Datasets.

## References
