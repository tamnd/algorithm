---
tag: 3BD165
kind: algorithm
slug: birch
name: BIRCH
aliases:
- balanced iterative reducing and clustering using hierarchies
- BIRCH clustering
area: machine-learning/clustering
level: advanced
summary: Single-pass clustering that summarises points in a clustering-feature tree.
solves: [k-means-problem]
model: external-memory-model
complexity:
  vars: {n: the number of points, d: the dimension, M: the largest number of leaf entries, h: the height of the CF tree, B: the branching factor, L: the leaf size, r: the number of rebuilds, k: the number of clusters}
  time: {worst: "O(n h (B + L) d + r M h (B + L) d + M^3 d + n k d)"}
  space: {extra: "O(M d + M^2)"}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1996
  people: [Tian Zhang, Raghu Ramakrishnan, Miron Livny]
  note: Zhang, Ramakrishnan and Livny presented BIRCH at SIGMOD 1996 as one of the first clustering methods designed for databases larger than memory; it received the SIGMOD test of time award in 2006.
prereqs: [clustering-feature-tree, k-means-problem, agglomerative-clustering]
see_also: [clustering-feature-tree, bfr-algorithm, cure, ward-method, k-means, streaming-k-median, dbscan, canopy-clustering]
sources:
  - paper: "T. Zhang, R. Ramakrishnan and M. Livny, BIRCH: an efficient data clustering method for very large databases, Proceedings of SIGMOD 1996, pp. 103-114"
    title: Zhang, Ramakrishnan and Livny 1996
    locator: "Section 5 (the overview of phases 1 to 4 and the rebuilding with a larger threshold) and Section 6 (experiments)"
  - paper: "T. Zhang, R. Ramakrishnan and M. Livny, BIRCH: a new data clustering algorithm and its applications, Data Mining and Knowledge Discovery 1(2), 1997, pp. 141-182"
    title: Zhang, Ramakrishnan and Livny 1997
    locator: the journal version, with the threshold heuristics, outlier handling and applications
  - book: isbn:9780123814791
    title: Jiawei Han, Micheline Kamber and Jian Pei, Data Mining, Concepts and Techniques, third edition
    locator: Section 10.3.3 (BIRCH, multiphase hierarchical clustering using clustering feature trees)
---

BIRCH (balanced iterative reducing and clustering using hierarchies) is a clustering method for large data sets of Euclidean points, by Zhang, Ramakrishnan and Livny (1996). It reads the data once and builds a [clustering feature tree](/clustering-feature-tree/), which keeps a few thousand small clusters, each as a summary $(N, \mathrm{LS}, \mathrm{SS})$. If the tree grows too large for the memory, BIRCH raises the threshold $T$ that bounds the size of a small cluster and rebuilds a smaller tree from the old summaries. Then it clusters the small clusters with a global method, such as agglomerative clustering, into $k$ clusters, and an optional second scan assigns each point to the nearest final centroid. BIRCH is a heuristic for the [k-means problem](/k-means-problem/); its strength is that it needs one scan and a fixed memory.

## In plain words

You have far too many points to cluster them directly. BIRCH works in four steps.

First it reads the points one by one and puts each into a small group of nearby points. It keeps only a short summary of each small group: the number of points, their sum and the sum of their squares. If there are too many small groups for the memory, it allows each small group to be a little wider and joins the groups again, so there are fewer of them.

Second, if it wants, it makes the groups fewer once more.

Third, it treats each small group as one heavy point and clusters these few heavy points into $k$ clusters with a slower but better method.

Fourth, if it can read the data again, it gives each point to the nearest final center, which repairs points that were put in a bad small group.

## The problem

The input is a set of $n$ points in $\mathbb{R}^d$, too large for memory but readable in one or more scans, a number $k$ of clusters, and a memory budget, here written as the largest number $M$ of leaf entries. The output is $k$ clusters, ideally with a small sum of squared distances to their centroids as in the [k-means problem](/k-means-problem/). BIRCH does not promise any factor; it promises one scan for phases 1 to 3, and a memory that does not depend on $n$.

## The algorithm

```pseudo id=main
BIRCH(points, k, B, L, M)
    ▷ phase 1: load the data into a CF tree
L1  T ← 0; tree ← an empty CF tree with branching factor B, leaf size L, threshold T
L2  for each point x do insert the CF (1, x, ‖x‖²) into the tree
L3      while the tree has more than M leaf entries do
L4          T ← a larger threshold; tree ← a new tree built by inserting the old leaf entries
    ▷ phase 2 (optional): rebuild with a larger T to get fewer, larger leaf entries
    ▷ phase 3: global clustering of the leaf entries
L5  clusters ← the leaf entries, each a weighted cluster given by its CF
L6  while there are more than k clusters do join the two whose union raises the sum of squares least
    ▷ phase 4 (optional, one more scan): refine
L7  label each point with the nearest centroid of the k clusters
L8  recompute each centroid from the points with its label; return the labels and centroids
```

In line L4 the new threshold here is the smallest radius of a merge of two entries of the same leaf, and at least twice the old one; the paper uses a similar heuristic from the growth of the data. In line L6 the increase of the sum of squares is $\frac{ab}{a + b}\|\mu_A - \mu_B\|^2$ for clusters of sizes $a$, $b$ and centroids $\mu_A$, $\mu_B$, which is [Ward's method](/ward-method/) and needs only the two CFs. The paper allows other global methods in phase 3, for example k-means on the weighted centroids.

## Example

Take points on a line, $B = L = 2$, $M = 4$ and $k = 2$, and read $0, 1, 10, 11, 20, 5, 21, 12$. The threshold is on $R^2$, the squared radius. An entry is $(N, \mathrm{LS}, \mathrm{SS})$.

| step | what happens | leaf entries after the step |
|---|---|---|
| read $0, 1, 10, 11$ | with $T = 0$ only equal points could join | $0$; $1$; $10$; $11$ |
| read $20$ | 5 entries $> M$: the least merge in a leaf, $\{0, 1\}$, has $R^2 = 1/4$; rebuild with $T^2 = 1/4$ | $(2, 1, 1)$, $(2, 21, 221)$, $(1, 20, 400)$ |
| read $5, 21$ | $5$ is a new entry; $21$ joins $20$ with $R^2 = 1/4$ | $(2,1,1)$, $(1,5,25)$, $(2,21,221)$, $(2,41,841)$ |
| read $12$ | 5 entries: rebuild with $T^2 = \max(2/3, 2 \cdot 1/4) = 2/3$, where $2/3$ is $R^2$ of $\{10, 11, 12\}$ | $(2,1,1)$, $(1,5,25)$, $(3,33,365)$, $(2,41,841)$ |

Phase 3 compares the increases of the sum of squares. The least is $\frac{2 \cdot 1}{3}(0.5 - 5)^2 = 13.5$ for $\{0, 1\}$ and $\{5\}$. After that join, $\{10, 11, 12\}$ and $\{20, 21\}$ cost $\frac{3 \cdot 2}{5}(11 - 20.5)^2 = 108.3$, less than $\frac{3 \cdot 3}{6}(2 - 11)^2 = 121.5$ for $\{0, 1, 5\}$ and $\{10, 11, 12\}$. So the two clusters are $\{0, 1, 5\}$ with centroid 2 and $\{10, 11, 12, 20, 21\}$ with centroid $74/5$. Phase 4 assigns $10$ to the second centroid, because $|10 - 14.8| < |10 - 2|$, and keeps the same clusters.

## Correctness

The leaf entries are exact CFs of a partition of the points, because a CF of a union is the sum of the CFs. The rebuild loop stops: the threshold at least doubles, and once $T$ is at least the largest distance between two points, every merge passes the test and there is one entry. So after each point the tree has at most $M$ leaf entries. Phase 3 joins clusters by the exact increase of the sum of squares, computed from the CFs. In phase 4, giving each point to the nearest centroid and then moving each centroid to the mean of its points can only lower the sum of squares, so phase 4 is never worse than the partition of phase 3. The proofs are on the correctness page. The quality of the partition itself is not proved.

## Complexity

- **Phase 1.** One insertion costs $O(h(B + L)d)$ for a tree of height $h$, so $O(nh(B + L)d)$ for $n$ points. Each rebuild inserts at most $M + 1$ entries. The paper keeps the I/O to one scan of the data plus the pages of the tree.
- **Phase 3.** Agglomerative clustering of $M$ entries by the simple pair search takes $O(M^3 d)$; with a priority queue it takes $O(M^2 \log M \cdot d)$. This does not depend on $n$.
- **Phase 4.** One more scan with $O(kd)$ work per point, so $O(nkd)$.
- **Space.** $O(Md)$ for the tree and $O(M^2)$ for phase 3. In the paper, $M$ follows from the memory size and the page size.

## Properties

- **One scan.** Phases 1 to 3 read each point once. Phase 4 needs a second scan.
- **Fixed memory.** The tree never has more than $M$ leaf entries.
- **Order dependent.** The small clusters depend on the order of the points.
- **Round clusters.** The summaries measure radius and diameter, so BIRCH prefers round, similar-size clusters, like k-means.
- **Euclidean.** The CF needs vector sums, so the data must be vectors.
- **Deterministic.** For a fixed order and fixed parameters the result is fixed.

## Variants and improvements

- **Outliers.** The paper can write sparse leaf entries to disk during a rebuild and test them again at the end, to remove noise.
- **Other global methods.** Phase 3 can use k-means on the weighted centroids, CLARANS, or any method that accepts weighted points.
- **[BFR](/bfr-algorithm/).** Uses the same kind of summaries with a sum of squares per dimension and Mahalanobis tests, for k-means on large data.
- **[CURE](/cure/).** Keeps several representative points per cluster to find clusters that are not round.
- **BIRCH\* and BUBBLE.** Ganti et al. (1999) extended the idea to general metric spaces with other summaries.
- **Stream micro-clusters.** CluStream and later stream methods keep CF-like micro-clusters with time stamps.

## When to use it

Use BIRCH when the data is much larger than memory, the points are vectors, and the clusters are round. It is fast and needs little memory, and its phase 1 is a good way to reduce a large set to a few thousand weighted points for a slower method. For clusters of any shape use [DBSCAN](/dbscan/) or [CURE](/cure/). For a proven factor in a metric space use [streaming k-median](/streaming-k-median/). If the data fits in memory, [k-means](/k-means/) on all of it is simpler.

## Pitfalls

- **The threshold.** If the first $T$ is far too small, the tree is rebuilt many times; if it grows too fast, different clusters are merged in a leaf entry and no later step can split them.
- **Sizes of $B$ and $L$.** Node splits are forced by capacity, so a natural cluster can be spread over several leaves; phase 3 must join them again.
- **Order of input.** Sorted input can give long thin small clusters. Shuffle the data if possible.
- **Precision.** The radius from $\mathrm{SS}/N - \|\mathrm{LS}/N\|^2$ loses precision in floating point when the points are far from the origin. Center the data first.
- **Skipping phase 4.** Without phase 4 a point stays in the cluster of its leaf entry, even if another centroid is closer.

## Implementations

## History

Zhang, Ramakrishnan and Livny presented BIRCH at SIGMOD 1996 and a longer version in Data Mining and Knowledge Discovery in 1997. It was one of the first clustering methods from the database community that handled data larger than memory with one scan, and it introduced the clustering feature. The paper received the SIGMOD test of time award in 2006. Its summaries were taken up by the [BFR algorithm](/bfr-algorithm/) in 1998 and later by many stream clustering methods.

## References
