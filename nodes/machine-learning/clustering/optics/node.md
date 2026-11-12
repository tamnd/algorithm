---
tag: P3H623
kind: algorithm
slug: optics
name: OPTICS
aliases:
- ordering points to identify the clustering structure
area: machine-learning/clustering
level: advanced
summary: "Order the points greedily by reachability distance. The DBSCAN clusters for every radius up to eps can then be read from this one ordering and its reachability plot."
solves: [density-based-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of features}
  time: {worst: "O(n^2 d + n^2 log n)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, online: false, exact: true, recursive: false}
history:
  year: 1999
  people: [Mihael Ankerst, Markus M. Breunig, Hans-Peter Kriegel, Jörg Sander]
  note: Ankerst, Breunig, Kriegel and Sander presented OPTICS at ACM SIGMOD 1999 as an extension of DBSCAN to all radii up to a generating distance.
prereqs: [dbscan, priority-queue]
see_also: [hdbscan, single-linkage-clustering, dendrogram, prim, binary-heap, density-peak-clustering]
sources:
  - paper: doi:10.1145/304181.304187
    title: "Mihael Ankerst, Markus M. Breunig, Hans-Peter Kriegel and Jörg Sander, OPTICS: ordering points to identify the clustering structure, Proceedings of ACM SIGMOD 1999 (SIGMOD Record 28(2))"
    locator: "Section 3.2.1 (Definitions 5 and 6, Figures 5 to 7 for the algorithm and the seed list, the run time), Figure 8 (ExtractDBSCAN-Clustering and the remark on border objects), Section 4.1 (reachability plots and the choice of the parameters)"
  - paper: "Martin Ester, Hans-Peter Kriegel, Jörg Sander and Xiaowei Xu, A density-based algorithm for discovering clusters in large spatial databases with noise, Proceedings of KDD-96, AAAI Press, 1996"
    locator: "pp. 226 to 231, Section 3 (the definitions that OPTICS extends)"
  - paper: "Jörg Sander, Xuejie Qin, Zhiyong Lu, Nan Niu and Alex Kovarsky, Automatic extraction of clusters from hierarchical clustering representations, PAKDD 2003, LNCS 2637, Springer"
    locator: the relation of reachability plots to dendrograms and the extraction of a cluster tree from a reachability plot
  - paper: doi:10.1145/342009.335388
    title: "Markus M. Breunig, Hans-Peter Kriegel, Raymond T. Ng and Jörg Sander, LOF: identifying density-based local outliers, Proceedings of ACM SIGMOD 2000"
    locator: the local outlier factor, built on the reachability distance
  - paper: doi:10.1002/widm.30
    title: "Hans-Peter Kriegel, Peer Kröger, Jörg Sander and Arthur Zimek, Density-based clustering, WIREs Data Mining and Knowledge Discovery 1(3), 2011"
    locator: the sections on OPTICS and on hierarchical density-based clustering
---

OPTICS is a [density-based clustering](/density-based-clustering-problem/) method that does not return one clustering. It returns an ordering of the points with two numbers for each point, a *core distance* and a *reachability distance*. From this ordering, one linear scan recovers the [DBSCAN](/dbscan/) clustering for any radius $\varepsilon' \le \varepsilon$, with the same core points and the same partition of the core points; only some border points may become noise. The plot of the reachability distances in the order, the *reachability plot*, shows the clusters at all density levels as valleys. With brute force range queries it costs $O(n^2 d + n^2 \log n)$ time.

## In plain words

DBSCAN needs one radius, and one radius cannot fit clusters of different densities. OPTICS avoids the choice. It walks through the data, always stepping next to the point that is easiest to reach from the points it has already visited. For each point it writes down how far that step was.

Inside a dense group the steps are short. To leave a group and enter the next one, the walk must make a long step. So if you draw the step lengths as bars, in the order of the walk, each group is a valley and each gap between groups is a high bar.

A horizontal line through this bar chart at some height cuts it into valleys. Each valley below the line is a DBSCAN cluster for that radius. Lower lines give smaller, denser clusters.

## The problem

The data model is clustering of points: a set $D$ of $n$ points in $\mathbb{R}^d$ with the [Euclidean distance](/euclidean-distance/), or in any [metric space](/metric-space/). The parameters are a *generating distance* $\varepsilon$ (it may be $\infty$) and an integer $\mathit{MinPts} \ge 1$. The number of clusters $k$ is not given. The output is an order $o_1, \ldots, o_n$ of $D$ and, for each point, a core distance and a reachability distance. The definitions of the paper (Section 3.2.1), with $N_\varepsilon(p)$ the points within $\varepsilon$ of $p$, $p$ included:

- **Core distance** (Definition 5). $\mathrm{core}(p)$ is the distance from $p$ to its $\mathit{MinPts}$-th nearest point, counting $p$ itself, if $|N_\varepsilon(p)| \ge \mathit{MinPts}$, and UNDEFINED ($\infty$) otherwise. It is the smallest radius $\varepsilon' \le \varepsilon$ at which $p$ is a DBSCAN core point.
- **Reachability distance** (Definition 6). $r(o, p) = \max(\mathrm{core}(o), \mathrm{dist}(o, p))$ if $o$ has a core distance and $p \in N_\varepsilon(o)$, and $\infty$ otherwise. It is the smallest radius at which $p$ is directly density-reachable from $o$. It is not symmetric.

The reachability of a point in the output, $\mathrm{reach}(o_i)$, is $\min_{j < i} r(o_j, o_i)$.

## The algorithm

```pseudo id=main
OPTICS(D, ε, MinPts)
L1  for each point i of D, in input order do
L2      if i is processed then continue
L3      N ← RANGE-QUERY(i, ε)                      ▷ reach[i] is ∞ here
L4      mark i processed; core[i] ← CORE-DISTANCE(N, MinPts)
L5      append i to the order
L6      if core[i] < ∞ then
L7          UPDATE(N, i, Seeds)
L8          while Seeds is not empty do
L9              q ← remove the seed with the smallest reach (ties: smaller index)
L10             N' ← RANGE-QUERY(q, ε); mark q processed; core[q] ← CORE-DISTANCE(N', MinPts)
L11             append q to the order
L12             if core[q] < ∞ then UPDATE(N', q, Seeds)

UPDATE(N, c, Seeds)                              ▷ OrderSeeds::update of the paper
L13 for each unprocessed o in N do r ← max(core[c], dist(c, o))
L14     if r < reach[o] then reach[o] ← r; insert o into Seeds or decrease its key

EXTRACT-DBSCAN(order, ε')                        ▷ for ε' ≤ ε
L15 C ← NOISE
L16 for each p in the order do
L17     if reach[p] > ε' then
L18         if core[p] ≤ ε' then
L19             C ← the next cluster id; label[p] ← C
L20         else label[p] ← NOISE
L21     else label[p] ← C
```

All reach values start at $\infty$. The seed list is a [priority queue](/priority-queue/) keyed by the reachability. The implementation uses a [binary heap](/binary-heap/) with lazy deletion: a decrease of a key pushes a new entry, and an entry whose key is no longer current is skipped when it comes out.

## Example

Take the points $1, 2, 3, 4, 10, 12, 14, 16, 30$ on the line, with $\varepsilon = 10$ and $\mathit{MinPts} = 3$. The output, in the order of the walk:

| order | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| point | 1 | 2 | 3 | 4 | 10 | 12 | 14 | 16 | 30 |
| core distance | 2 | 1 | 1 | 2 | 4 | 2 | 2 | 4 | ∞ |
| reachability | ∞ | 2 | 1 | 1 | 6 | 4 | 2 | 2 | ∞ |

The core distance of 1 is 2, because its three nearest points (itself counted) are 1, 2 and 3. The walk starts at 1 and gives the points 2 and 3 the reachabilities $\max(2, 1) = 2$ and $\max(2, 2) = 2$, the point 4 the value $\max(2, 3) = 3$, and the point 10 the value $\max(2, 9) = 9$. It processes 2 next, which lowers the reachability of 3 to $\max(1, 1) = 1$. Then 3, then 4, which lowers the reachability of 10 to $\max(2, 6) = 6$. The dense group ends, so the walk must step to 10 at cost 6. In the sparse group the steps cost 4, 2 and 2. The point 30 is more than 10 from every point, so its reachability is $\infty$.

The reachability plot is $\infty, 2, 1, 1, 6, 4, 2, 2, \infty$: a deep valley for the dense group, a shallower valley for the sparse group, and a peak of 6 between them. EXTRACT-DBSCAN gives:

| $\varepsilon'$ | labels in the order |
|---|---|
| 1 | NOISE, A, A, A, NOISE, NOISE, NOISE, NOISE, NOISE |
| 2 | A, A, A, A, NOISE, B, B, B, NOISE |
| 6 | A, A, A, A, A, A, A, A, NOISE |

At $\varepsilon' = 1$, DBSCAN makes 1 a border point of the cluster $\{2, 3, 4\}$, because 1 is within 1 of the core point 2. OPTICS processed 1 first, before any core point of that cluster at radius 1, so the extraction reports it as noise. The same happens to 10 at $\varepsilon' = 2$. This is the case that the paper describes in its discussion of Figure 8.

## Correctness

The proof has two parts. First, an invariant of the seed list shows that $\mathrm{reach}(o_i) = \min_{j < i} r(o_j, o_i)$, and that each chosen point has the smallest current reachability of all unprocessed points: the order is greedy, in the way of [Prim's algorithm](/prim/). Second, fix $\varepsilon' \le \varepsilon$. A point is a DBSCAN core point at $\varepsilon'$ if and only if its core distance is at most $\varepsilon'$, and $r(o, p) \le \varepsilon'$ if and only if $p$ is directly density-reachable from $o$ at $\varepsilon'$. A point with reachability above $\varepsilon'$ is a *break*. By the greedy property, after a break, each point with a small reachability is reachable from a point at or after the break, and no break can fall between two adjacent core points. So each run between breaks holds exactly the core points of one component of the DBSCAN core graph. The theorem that follows:

- the core points of EXTRACT-DBSCAN and of DBSCAN at $(\varepsilon', \mathit{MinPts})$ are the same, and so is the partition of the core points into clusters;
- each DBSCAN noise point is NOISE in the extraction;
- a border point is NOISE in the extraction exactly when all core points within $\varepsilon'$ of it come after it in the order.

So the noise of the extraction can be larger than the noise of DBSCAN, by such border points. Give each of them the label of a core point within $\varepsilon'$, and the noise sets are equal. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/). Here $n$ is the number of points and $d$ the number of features.

- **Range queries.** OPTICS makes exactly $n$ range queries, like DBSCAN. With brute force each costs $\Theta(n d)$, so they cost $\Theta(n^2 d)$ in total.
- **Seed list.** UPDATE runs over $\sum_p |N_\varepsilon(p)| \le n^2$ neighbors in total. With a binary heap each change costs $O(\log n)$, so the seed list costs $O(n^2 \log n)$ in the worst case. With $\varepsilon = \infty$, a plain array of the reach values and a linear scan for the minimum cost $O(n)$ per step and $O(1)$ per update, which gives $\Theta(n^2 d)$ in total, as in the dense form of Prim's algorithm.
- **Memory.** The lazy heap can hold $O(n^2)$ entries. A heap with decrease-key, or the array, needs $\Theta(n)$ extra space.
- **With an index.** The paper notes that the run time is dominated by the range queries and is $O(n \log n)$ when a tree index answers each query in $O(\log n)$ time. As for DBSCAN, this is not a worst case bound: a large $\varepsilon$ makes the neighborhoods large, and the paper itself recommends an $\varepsilon$ large enough that most points are reachable. In its experiments OPTICS took about 1.6 times the time of DBSCAN.
- **Extraction.** EXTRACT-DBSCAN takes $\Theta(n)$ time for each $\varepsilon'$.

## Properties

- **One run, many radii.** The ordering contains the DBSCAN core clusterings for all $\varepsilon' \le \varepsilon$ at the fixed $\mathit{MinPts}$. The clusters at smaller $\varepsilon'$ are nested inside the clusters at larger $\varepsilon'$, so the reachability plot shows a hierarchy.
- **Link to single linkage.** With $\mathit{MinPts} \le 2$, the core distance of a point is 0 or its nearest neighbor distance, and $r(o, p) = \mathrm{dist}(o, p)$ for $p \ne o$. With $\varepsilon = \infty$, OPTICS is then Prim's algorithm on the complete graph, the reachabilities are the edges of a [minimum spanning tree](/minimum-spanning-tree/), and the plot represents the [single linkage](/single-linkage-clustering/) [dendrogram](/dendrogram/). A larger $\mathit{MinPts}$ smooths the plot and weakens the chaining effect of single linkage.
- **Not unique.** The order depends on the start point and on ties. The set of plateaus and valleys does not.
- **Insensitive to $\varepsilon$.** The generating distance only cuts off the plot: a larger $\varepsilon$ shows more levels and costs more time. The paper reports that the shape of the plot changes little with $\mathit{MinPts}$, and used values from 10 to 20.

## Variants and improvements

- **ξ-clusters.** The paper also extracts a hierarchy of clusters automatically from steep down and steep up areas of the plot, controlled by a steepness parameter $\xi$ (Section 4.3 of the paper).
- **Cluster trees from the plot.** Sander et al. (2003) extract a tree of significant clusters from a reachability plot and show how plots and dendrograms convert into each other.
- **Outlier scores.** Breunig, Kriegel, Ng and Sander (2000) use a form of the reachability distance for the local outlier factor (LOF), which compares the density around a point with the density around its neighbors.
- **HDBSCAN.** [HDBSCAN](/hdbscan/) replaces the asymmetric reachability by the symmetric mutual reachability distance, builds the full hierarchy from a minimum spanning tree, and selects the flat clusters by a stability measure instead of a horizontal cut.

## When to use it

Use OPTICS when the clusters have different densities, when you want to look at the cluster structure at all density levels before you choose a radius, or when you need the DBSCAN clusterings for many radii. Use plain [DBSCAN](/dbscan/) when one radius is known to be right. Use [HDBSCAN](/hdbscan/) when you want an automatic flat clustering with clusters at different density levels.

## Pitfalls

- **Expecting the exact DBSCAN result.** EXTRACT-DBSCAN can report some border points as noise, as in the example. Reassign them if you need DBSCAN's result.
- **A too small $\varepsilon$.** Points with an undefined core distance cut the plot into pieces with $\infty$ bars, and the sparse clusters are lost. Use a large $\varepsilon$ when the range queries allow it.
- **Reading the order as a clustering.** The order alone is not a clustering. The clusters come from the valleys of the plot, by a cut or by the ξ method.
- **Comparing reachabilities across runs.** The order and the first reach value depend on the start point. Compare the extracted clusters, not the raw sequence.
- **Lazy heap without a check.** A heap with lazy deletion must skip the entries whose key is no longer the current reach, or a point is processed twice.

## Implementations

## History

Mihael Ankerst, Markus Breunig, Hans-Peter Kriegel and Jörg Sander, at the University of Munich, presented OPTICS at ACM SIGMOD in 1999. They observed that DBSCAN clusters for a smaller radius lie inside the clusters for a larger radius, and stored only the order and two distances per point instead of the clusters themselves. Breunig, Kriegel, Ng and Sander used the reachability distance for the local outlier factor in 2000. Sander, Qin, Lu, Niu and Kovarsky related reachability plots to dendrograms in 2003, and Campello, Moulavi and Sander built HDBSCAN on these ideas in 2013.

## References
