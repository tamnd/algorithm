---
tag: 2C6X4V
kind: problem
slug: k-nearest-neighbor-graph-construction
name: k-nearest neighbor graph construction
aliases:
- kNN graph construction
area: searching/similarity-search
level: advanced
summary: Build a directed graph in which each point has edges to its k nearest neighbors.
prereqs: [k-nearest-neighbor-graph, k-nearest-neighbor-search]
see_also: [all-nearest-neighbors, nn-descent, well-separated-pair-decomposition, closest-pair-of-points, all-pairs-similarity-search, fixed-radius-near-neighbors, locality-sensitive-hashing, hnsw]
sources:
  - paper: doi:10.1007/BF02187718
    title: Pravin M. Vaidya, An O(n log n) algorithm for the all-nearest-neighbors problem, Discrete and Computational Geometry 4, 1989
    locator: pages 101 to 115 (all nearest neighbors of n points in fixed dimension in O(n log n) time)
  - paper: doi:10.1145/200836.200853
    title: Paul B. Callahan and S. Rao Kosaraju, A decomposition of multidimensional point sets with applications to k-nearest-neighbors and n-body potential fields, Journal of the ACM 42(1), 1995
    locator: pages 67 to 90 (the well-separated pair decomposition, and the k-nearest neighbor graph of n points in fixed dimension in O(n log n + kn) time)
  - paper: doi:10.1145/1963405.1963487
    title: Wei Dong, Moses Charikar and Kai Li, Efficient k-nearest neighbor graph construction for generic similarity measures, Proceedings of the 20th International World Wide Web Conference (WWW), 2011
    locator: pages 577 to 586 (NN-descent, the local join, sampling, and the measured cost of about n^1.14 distance evaluations on their data sets)
  - paper: doi:10.1145/800061.808735
    title: Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC), 1983
    locator: pages 80 to 86 (depth Ω(log N − n) for deciding membership in a set with N connected components, which gives Ω(n log n) for element distinctness)
---

The $k$-nearest neighbor graph construction problem asks, for $n$ points and a distance, for the [k-nearest neighbor graph](/k-nearest-neighbor-graph/): for every point, the list of its $k$ nearest other points. The case $k = 1$ is the [all nearest neighbors](/all-nearest-neighbors/) problem. A scan of all pairs solves it with $n(n-1)$ distance evaluations for any distance; in fixed dimension, Callahan and Kosaraju solve it in $O(n \log n + kn)$ time, which is optimal in the algebraic decision tree model. In high dimension the exact problem has no known truly subquadratic algorithm, and practice uses approximate methods such as [NN-descent](/nn-descent/).

## In plain words

Every point wants to know its $k$ closest other points. The plain method measures every pair, which is fine for thousands of points but not for millions.

When the points have few coordinates, trees and the geometry of the plane or space let you skip most pairs, and the work becomes close to sorting. When the points have many coordinates, no exact method is known that is much faster than measuring every pair. Then one builds an almost correct graph: start with random lists, and keep improving them by asking each point's neighbors for their neighbors.

## Definition

**Input.** Points $p_0, \dots, p_{n-1}$ in a space with a distance $\delta$, and an integer $k \ge 1$.

**Output.** For each $i$, the list $N(i)$ of the $\min(k, n-1)$ indices $j \ne i$ with the least pairs $(\delta(p_i, p_j), j)$, in increasing order. Ties in distance go to the smaller index, so the output is unique.

**Approximate output.** A list $N'(i)$ of $k$ indices for each $i$. Its quality is the **recall** $\frac{1}{nk} \sum_i |N'(i) \cap N(i)|$, the fraction of true edges found. Some methods give a guarantee per edge instead: each $j \in N'(i)$ is within $c$ times the distance from $p_i$ to its true $k$-th neighbor, with a stated probability.

## Variants

- **All nearest neighbors**, $k = 1$: the [all nearest neighbors](/all-nearest-neighbors/) problem.
- **Symmetric or mutual graph:** keep an edge if either or both endpoints list the other. Both come from the directed graph in $O(nk)$ time.
- **Bichromatic:** for every point of a set $A$, its $k$ nearest points of a set $B$. This is a batch of $|A|$ [k-nearest neighbor](/k-nearest-neighbor-search/) queries.
- **Threshold graph:** all pairs within distance $r$, the all-pairs form of [fixed-radius near neighbors](/fixed-radius-near-neighbors/); for similarities, [all-pairs similarity search](/all-pairs-similarity-search/).
- **Dynamic:** keep the graph correct under insertions and deletions of points.

## Examples

Take the points $0, 1, 3, 6, 10, 11$ on a line, indices 0 to 5, with $k = 2$. The scan computes $\binom{6}{2} = 15$ distinct distances (30 evaluations if each point computes its own) and gives

$$N(0) = (1, 2),\ N(1) = (0, 2),\ N(2) = (1, 0),\ N(3) = (2, 4),\ N(4) = (5, 3),\ N(5) = (4, 3).$$

For point 2, both 0 and 3 are at distance 3, and the tie goes to 0.

On a line, the problem is easy after sorting: the $k$ nearest neighbors of a point are among the $k$ points to its left and the $k$ points to its right in sorted order, and a merge of the two sides in order of distance picks them. So $O(n \log n + nk)$ time suffices for $d = 1$. For $k = 1$ in the example, the sorted order gives $N(0) = 1$, $N(1) = 0$, $N(2) = 1$, $N(3) = 2$, $N(4) = 5$, $N(5) = 4$.

## Known algorithms

| method | setting | time | output |
|---|---|---|---|
| scan of all pairs | any distance, $E$ per evaluation | $O(n^2 (E + \log k))$ | exact |
| sort, then merge two sides | the real line | $O(n \log n + nk)$ | exact |
| Vaidya | $\mathbb{R}^d$, $d$ fixed, $k = 1$ | $O(n \log n)$ | exact |
| Callahan and Kosaraju | $\mathbb{R}^d$, $d$ fixed | $O(n \log n + kn)$ | exact |
| a tree, then $n$ queries | low dimension or low intrinsic dimension | no worst-case gain over the scan | exact |
| LSH, then $n$ queries | $\ell_2$ or Hamming | $n^{1 + \rho + o(1)}$ for a $(c, r)$ guarantee per point | approximate |
| NN-descent | any distance | no worst-case bound; about $n^{1.14}$ evaluations measured | approximate |

**Scan.** For each $i$, offer the $n - 1$ pairs $(\delta(p_i, p_j), j)$ to a heap of size $k$, as in the build of the [k-nearest neighbor graph](/k-nearest-neighbor-graph/), where it is proved correct. Computing each distance once and offering it to both endpoints halves the evaluations.

**Fixed dimension.** Both exact algorithms use a hierarchical split of space by boxes. Callahan and Kosaraju build the [well-separated pair decomposition](/well-separated-pair-decomposition/) in $O(n \log n)$ time; it lists $O(n)$ pairs of point sets $(A, B)$ such that every pair of points is covered by exactly one listed pair and the sets of each pair are far apart compared to their sizes. The $k$ nearest neighbors of a point $p$ are then found among few listed pairs, which leads to $O(n \log n + kn)$ total time. The constants grow exponentially with $d$.

**Index, then queries.** Build an index such as a [k-d tree](/kd-tree/), [ball tree](/ball-tree/) or [cover tree](/cover-tree/), and query each point for its $k + 1$ nearest points, dropping the point itself. This is the common practical method in low dimension; with a cover tree the time is bounded in terms of the expansion constant of the data, see [intrinsic dimensionality](/intrinsic-dimensionality/).

**Hashing.** With [locality-sensitive hashing](/locality-sensitive-hashing/) for $\ell_2$ or Hamming distance and a radius $r$, querying every point gives, for each point whose nearest neighbor is within $r$, a point within $cr$ with constant probability, in $n^{1 + \rho + o(1)}$ total time, where $\rho < 1$ depends on $c$ and on the hash family. Repeating $O(\log n)$ times makes all points succeed with high probability.

**NN-descent.** Start from random lists. In each round, for each point, compare pairs of its neighbors and reverse neighbors, and update both lists of each compared pair when the new distance is better than their current $k$-th one. Stop when few lists change. Dong, Charikar and Li measured high recall at a cost of about $n^{1.14}$ distance evaluations on their data sets; no worst-case bound is known.

**Graph indexes.** [HNSW](/hnsw/) and similar indexes are built by inserting points one by one with a search of the current graph; the candidate lists they find during insertion give an approximate $k$-NN graph as a side product.

## Bounds

- **Output and input.** $\Omega(nk)$ time to write the lists and $\Omega(n)$ to read the points, in every model.
- **Algebraic decision trees.** In the [algebraic decision tree](/algebraic-decision-tree/) model, even $k = 1$ on the real line needs $\Omega(n \log n)$ time. *Proof.* Given the 1-NN graph of reals $x_0, \dots, x_{n-1}$, the numbers are distinct if and only if $|x_i - x_{N(i)}| > 0$ for every $i$, which $n$ more tests decide. So the 1-NN graph decides [element distinctness](/element-distinctness/). The set of inputs with distinct entries has $n!$ connected components, one per order of the entries, so by Ben-Or's theorem element distinctness needs depth $\Omega(\log n!) = \Omega(n \log n)$. $\square$ Together with the output bound, the $O(n \log n + kn)$ algorithm of Callahan and Kosaraju is optimal in this model for fixed $d$.
- **High dimension.** The 1-NN graph also gives the closest pair distance by $n$ more comparisons, so it decides whether some pair is within distance $r$. For Hamming distance in dimension $c \log n$ this decision is as hard as [orthogonal vectors](/orthogonal-vectors/), by the reduction given for [fixed-radius near neighbors](/fixed-radius-near-neighbors/). So under the [Strong Exponential Time Hypothesis](/strong-exponential-time-hypothesis/), for each $\varepsilon > 0$ there is a $c$ such that exact construction in Hamming space of dimension $c \log n$ has no $O(n^{2 - \varepsilon})$ algorithm.

## Reductions

- **From closest pair.** The [closest pair of points](/closest-pair-of-points/) is the pair $\{i, N(i)\}$ with the least distance in the 1-NN graph, found in $O(n)$ extra time. This gives the lower bounds above.
- **To $k$-nearest neighbor queries.** $n$ queries for the $k + 1$ nearest points, on an index of the points themselves, give the graph. Any query structure thus gives a construction algorithm, with $n$ times its query time plus its build time.
- **To all-pairs threshold joins.** If every point has at least $k$ other points within $r$, the $k$ nearest are among the pairs within $r$, so a [fixed-radius](/fixed-radius-near-neighbors/) all-pairs join followed by selection gives the graph. This helps only when the join output is small.
- **Symmetric and mutual graphs** come from the directed graph in $O(nk)$ time, by computing the reverse lists.

## Applications

- **Clustering and embedding.** [Spectral clustering](/spectral-clustering/), [DBSCAN](/dbscan/), [UMAP](/umap/), [t-SNE](/t-sne/) and [Isomap](/isomap/) start from a $k$-NN graph of the data.
- **Graph indexes for search.** Many approximate nearest neighbor indexes, such as [DiskANN](/diskann/), are built from an approximate $k$-NN graph that is then pruned and given long edges.
- **Outliers and density.** The distance to the $k$-th neighbor, and the number of points that list a point, are simple density and outlier scores.
- **Recommendation and deduplication.** Item-to-item similar lists are a $k$-NN graph over item vectors.

## References
