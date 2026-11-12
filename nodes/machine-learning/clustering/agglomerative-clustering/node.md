---
tag: G398XN
kind: algorithm
slug: agglomerative-clustering
name: Agglomerative clustering
aliases:
- bottom-up clustering
- hierarchical agglomerative clustering
- HAC
area: machine-learning/clustering
level: core
summary: "Start with each point as a cluster and repeatedly merge the two closest clusters under a linkage criterion. Naive time O(n^3), memory O(n^2)."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: "Θ(n^3)"}
  space: {extra: "Θ(n^2)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1957
  people: [Peter H. A. Sneath, Robert R. Sokal, Charles D. Michener, G. N. Lance, W. T. Williams]
  note: Sneath (1957) used single linkage and Sokal and Michener (1958) used average linkage to classify organisms. Lance and Williams (1967) gave one update formula for all common linkages.
prereqs: [hierarchical-clustering-problem, linkage-criterion, priority-queue]
see_also: [lance-williams-formula, nearest-neighbor-chain, single-linkage-clustering, complete-linkage-clustering, ward-method, divisive-clustering, dendrogram, upgma]
sources:
  - paper: doi:10.1093/comjnl/9.4.373
    title: "G. N. Lance and W. T. Williams, A general theory of classificatory sorting strategies 1. Hierarchical systems, The Computer Journal 9(4) (1967), 373-380"
    locator: the general agglomerative scheme and the recurrence that updates the dissimilarity matrix after each fusion
  - book: isbn:9780471878766
    title: Leonard Kaufman and Peter J. Rousseeuw, Finding Groups in Data, An Introduction to Cluster Analysis
    locator: Chapter 5 (agglomerative nesting, program AGNES)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval
    locator: Chapter 17 (the naive algorithm in Θ(N^3) and the priority-queue algorithm in Θ(N^2 log N))
  - paper: doi:10.1007/BF01890115
    title: "William H. E. Day and Herbert Edelsbrunner, Efficient algorithms for agglomerative hierarchical clustering methods, Journal of Classification 1(1) (1984), 7-24"
    locator: the O(n^2 log n) algorithms for the linkages of the Lance-Williams family
  - url: https://arxiv.org/abs/1109.2378
    title: "Daniel Müllner, Modern hierarchical, agglomerative clustering algorithms, arXiv:1109.2378 (2011)"
    locator: Section 3 (the primitive algorithm, the generic algorithm with a priority queue, and the nearest-neighbor chain)
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (agglomerative algorithms and the Lance-Williams recurrence)
---

Agglomerative clustering builds a [hierarchical clustering](/hierarchical-clustering-problem/) from the bottom up. Each point starts as a cluster of its own. At each step, the two clusters with the smallest dissimilarity under a [linkage criterion](/linkage-criterion/) merge into one. After $n - 1$ merges, one cluster holds all points, and the list of merges with their heights is a [dendrogram](/dendrogram/). With the [Lance-Williams formula](/lance-williams-formula/), each update of the dissimilarity matrix takes $O(n)$ time, so the naive algorithm runs in $\Theta(n^3)$ time and $\Theta(n^2)$ memory. A [priority queue](/priority-queue/) of pairs brings the time to $O(n^2 \log n)$, and the [nearest-neighbor chain](/nearest-neighbor-chain/) to $O(n^2)$ for the reducible linkages.

## In plain words

At the start, each item is a group of one. Look at all pairs of groups and find the two that are closest. Join them into one group. Now the new group needs a distance to each other group. A simple rule gives each of these distances from the old ones, so you do not need to look at the items again.

Do this again and again. Each time, there is one group fewer. Stop when one group is left. Keep a note of each join and of the distance at which it happened. These notes are the tree.

## The problem

The input is an $n \times n$ dissimilarity matrix $D$, symmetric with zeros on the diagonal, and a linkage criterion. For centroid, median and Ward linkage, $D$ holds the squared Euclidean distances of points. The output is the list of $n - 1$ merges, each one a pair of clusters and a height, made by the greedy rule: at each step, merge the pair of current clusters with the smallest linkage value. This tree is the solution of the [hierarchical clustering problem](/hierarchical-clustering-problem/) that the linkage defines.

## The algorithm

Slot $i$ of the matrix holds one current cluster. After a merge of the clusters in slots $i$ and $j$, slot $i$ holds the union and slot $j$ is dropped. LW is the Lance-Williams update of the chosen linkage: it returns the dissimilarity of cluster $k$ to the union of $i$ and $j$ from $D[k, i]$, $D[k, j]$, $D[i, j]$ and the three sizes.

```pseudo id=main
AGGLOMERATIVE(D, linkage)             ▷ D is an n × n dissimilarity matrix
L1  active ← {1, …, n}, size[i] ← 1 for each i
L2  merges ← empty list
L3  while |active| > 1 do
L4      (i, j) ← the pair of active slots with the smallest D[i, j]
L5      h ← D[i, j]
L6      for each k in active − {i, j} do
L7          D[i, k] ← D[k, i] ← LW(D[k, i], D[k, j], D[i, j], size[i], size[j], size[k])
L8      append (i, j, h) to merges
L9      size[i] ← size[i] + size[j], remove j from active
L10 return merges
```

When two pairs tie at line L4, the code takes the first pair in the order of the slots. A different rule can give a different tree, but each tree it gives is a correct greedy tree.

**The priority queue version.** Keep all pairs $(D[i, j], i, j)$ in a binary heap. Line L4 pops the smallest pair, and skips it if slot $i$ or $j$ was dropped or changed after the pair was pushed. After lines L6 and L7, push the $O(n)$ new pairs of slot $i$. Each version of a slot carries a number, so a stale pair is easy to see.

## Example

Average linkage on the points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line, with $D[x, y] = |x - y|$. For average linkage, LW is $\frac{n_i}{n_i + n_j} D[k, i] + \frac{n_j}{n_i + n_j} D[k, j]$.

| step | merge | height | new values in slot $i$ |
|---|---|---|---|
| 1 | $b$, $c$ | 1 | $D(a, bc) = 5/2$, $D(d, bc) = 9/2$, $D(e, bc) = 21/2$, $D(f, bc) = 37/2$ |
| 2 | $a$, $bc$ | $5/2$ | $D(d, abc) = (7 + 2 \cdot 9/2)/3 = 16/3$, $D(e, abc) = 34/3$, $D(f, abc) = 58/3$ |
| 3 | $d$, $abc$ | $16/3$ | $D(e, abcd) = (6 + 3 \cdot 34/3)/4 = 10$, $D(f, abcd) = 18$ |
| 4 | $e$, $f$ | 8 | $D(abcd, ef) = (10 + 18)/2 = 14$ |
| 5 | $abcd$, $ef$ | 14 | |

At step 3, the pair $d, abc$ at $16/3$ wins over the pair $d, e$ at $6$. At step 4, the pair $e, f$ at $8$ wins over the pair $e, abcd$ at $10$. Each value is the mean of the distances between the two clusters. For example $D(e, abcd) = (13 + 11 + 10 + 6)/4 = 10$. The heights $1, 5/2, 16/3, 8, 14$ increase, as they must for a reducible linkage. Single and complete linkage give other trees on these points; the three trees are on the page [hierarchical clustering problem](/hierarchical-clustering-problem/).

## Correctness

The invariant of the loop of line L3 is this: for each two active slots $i$ and $k$, $D[i, k]$ is the linkage value of the clusters that the slots hold, and size$[i]$ is the size of the cluster in slot $i$. It is true at the start, because the linkage value of two single points is their dissimilarity for each of the seven linkages. Line L4 then picks the pair of clusters with the smallest linkage value, which is the greedy rule. Line L7 keeps the invariant because the Lance-Williams formula gives the exact linkage value of the union, which the proof checks row by row. The loop ends after $n - 1$ merges, because each one drops one slot. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Naive version.** Line L4 scans $O(n^2)$ pairs in each of the $n - 1$ rounds, and lines L6 and L7 take $O(n)$ time. So the time is $\Theta(n^3)$ in each case: the round with $m$ active slots scans $m(m - 1)/2$ pairs, and the sum over $m$ is $\Theta(n^3)$.
- **Priority queue version.** The heap starts with $n(n - 1)/2$ pairs, built in $O(n^2)$ time. Each round pushes at most $n$ pairs, so at most $O(n^2)$ pairs are pushed in total, and each push or pop costs $O(\log n)$. The time is $O(n^2 \log n)$.
- **Memory.** Both versions keep the matrix, $\Theta(n^2)$ numbers. The heap has $O(n^2)$ pairs.
- **Lower bound.** For a general matrix, an exact algorithm must read all $n(n - 1)/2$ entries in the worst case (see the problem page), so $\Omega(n^2)$ time is necessary.

## Properties

- **Deterministic** for a fixed rule for ties.
- **Monotone heights** for the reducible linkages: single, complete, average, weighted and Ward. Centroid and median linkage can give inversions: on the points $(0, 0)$, $(8, 0)$ and $(4, 7)$, centroid linkage merges at heights $64$ and then $49$.
- **Greedy, not optimal.** Each merge is the best single step. The tree does not optimize a global objective. For example, the cut of Ward's tree at $k$ clusters is not always the best [k-means](/k-means-problem/) partition, and the cut of the complete linkage tree does not always have the smallest largest diameter.
- **Ties.** With equal dissimilarities, the greedy tree is not unique. For single linkage, all greedy trees have the same cophenetic distance, but for the other linkages they can differ.

## Variants and improvements

- **[Nearest-neighbor chain](/nearest-neighbor-chain/).** For reducible linkages, merge reciprocal nearest neighbors as they appear. It gives the same tree in $O(n^2)$ time.
- **[SLINK](/slink/).** Single linkage in $O(n^2)$ time and $O(n)$ memory, with no matrix.
- **[Single linkage](/single-linkage-clustering/) by a [minimum spanning tree](/minimum-spanning-tree/).** In the plane, the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) gives single linkage in $O(n \log n)$ time.
- **Generic algorithm of Müllner.** A priority queue of nearest neighbors, one per slot, which is fast in practice for all seven linkages.
- **Stored data instead of a matrix.** For centroid, median and Ward linkage, keep the centroids and sizes, and compute each value from them. This takes $O(n d)$ memory and $O(n^3 d)$ time for points in $\mathbb{R}^d$.
- **Connectivity constraints.** Allow only merges of clusters that are neighbors in a graph. This is region merging in image segmentation.

## When to use it

Use agglomerative clustering when you want the clusters at all scales, or do not know the number of clusters, and $n$ is at most some tens of thousands, so that the $n^2$ matrix fits in memory. Use it when only a dissimilarity matrix is known and not the points. Pick the linkage for the shape of the clusters that you expect: single for long, thin clusters, complete for compact clusters, average for a balance, and Ward for clusters of similar size and spread. For very large $n$, use [BIRCH](/birch/), [HDBSCAN](/hdbscan/) or [k-means](/k-means/) first.

## Pitfalls

- **Squared distances.** The Lance-Williams rows for centroid, median and Ward are exact only on squared Euclidean distances. With plain distances, the update gives wrong values.
- **Memory.** The matrix of $10^5$ points has $5 \cdot 10^9$ entries. Check the memory before a run.
- **Ties and the input order.** With ties, a permutation of the input can change the tree. With integer data, ties are common.
- **Inversions.** With centroid or median linkage, a cut at a height can be wrong. Cut at a number of clusters, or use a reducible linkage.
- **Stale heap entries.** In the heap version, a pair that was pushed before a merge has a wrong value. Without a check of versions, the code merges with old values.

## Implementations

## History

Sneath (1957) used single linkage to classify bacteria, and Sokal and Michener (1958) introduced average linkage, now called UPGMA. Ward (1963) proposed the minimum variance criterion. Lance and Williams (1967) showed that one recurrence updates the matrix for all of these linkages, which made one program enough for all of them. Day and Edelsbrunner (1984) gave $O(n^2 \log n)$ algorithms for the whole family. Murtagh (1983) surveyed the $O(n^2)$ methods based on reciprocal nearest neighbors.

## References
