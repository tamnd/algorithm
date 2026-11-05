---
tag: CST612
kind: data-structure
slug: k-nearest-neighbor-graph
name: k-nearest neighbor graph
aliases:
- kNN graph
- KNNG
area: searching/similarity-search
level: advanced
summary: A graph with an edge from each point to its k nearest neighbors, used as an index and in clustering.
implements: [similarity-index]
model: real-ram
complexity:
  vars: {n: the number of points, k: the out-degree, E: the time of one distance evaluation, ef: the beam width of a search}
  time: {build: O(n^2 (E + log k)), neighbors: O(1), search: O(n k (E + log(n k)))}
  space: {total: O(n k)}
history:
  year: 1989
  people: [Pravin M. Vaidya, Paul B. Callahan, S. Rao Kosaraju, Wei Dong, Moses Charikar, Kai Li]
  note: Vaidya gave an O(n log n) algorithm for all nearest neighbors in fixed dimension in 1989; Callahan and Kosaraju built the k-nearest neighbor graph in O(n log n + kn) time in 1995 with the well-separated pair decomposition; Dong, Charikar and Li made approximate construction for general distances practical with NN-descent in 2011.
prereqs: [k-nearest-neighbor-search, directed-graph]
see_also: [k-nearest-neighbor-graph-construction, nn-descent, all-nearest-neighbors, navigable-small-world, hnsw, diskann, reverse-nearest-neighbor, hubness]
sources:
  - paper: doi:10.1007/BF02187718
    title: Pravin M. Vaidya, An O(n log n) algorithm for the all-nearest-neighbors problem, Discrete and Computational Geometry 4, 1989
    locator: pages 101 to 115 (all nearest neighbors of n points in fixed dimension in O(n log n) time)
  - paper: doi:10.1145/200836.200853
    title: Paul B. Callahan and S. Rao Kosaraju, A decomposition of multidimensional point sets with applications to k-nearest-neighbors and n-body potential fields, Journal of the ACM 42(1), 1995
    locator: pages 67 to 90 (the k-nearest neighbor graph of n points in fixed dimension in O(n log n + kn) time)
  - paper: doi:10.1145/1963405.1963487
    title: Wei Dong, Moses Charikar and Kai Li, Efficient k-nearest neighbor graph construction for generic similarity measures, Proceedings of the 20th International World Wide Web Conference (WWW), 2011
    locator: pages 577 to 586 (NN-descent, and the use of the k-nearest neighbor graph for search and in learning)
  - paper: doi:10.1145/502807.502808
    title: Edgar Chávez, Gonzalo Navarro, Ricardo Baeza-Yates and José Luis Marroquín, Searching in metric spaces, ACM Computing Surveys 33(3), 2001
    locator: pages 273 to 321 (graph-based indexes for metric spaces and the use of stored distances for pruning)
---

The $k$-nearest neighbor graph of a finite point set $P$ is the [directed graph](/directed-graph/) with an edge from each point $p$ to each of its $k$ nearest other points in $P$. It stores $nk$ edges, answers "the $k$ neighbors of $p$" in constant time, and gives a natural index for [nearest neighbor search](/k-nearest-neighbor-search/): start at some points and walk along edges toward the query, as the [navigable small world](/navigable-small-world/) graphs, [HNSW](/hnsw/) and [DiskANN](/diskann/) do with better-connected graphs. Building it by brute force costs $n(n-1)$ distance evaluations; faster exact and approximate methods are the subject of [k-nearest neighbor graph construction](/k-nearest-neighbor-graph-construction/).

## In plain words

Each point makes a list of its $k$ closest other points and draws an arrow to each. The arrows form the graph.

The graph answers questions about the data itself at once: which points are close to this one, which points are in a dense area, which points nobody picks as a neighbor. Clustering, manifold learning and outlier detection all start from it.

The graph can also guide a search for a new point. Start somewhere, look at the arrows, move to the neighbor that is closest to the new point, and repeat until no neighbor is closer. This is fast, but it can stop at the wrong place, because the arrows of one cluster may never lead into another cluster.

## The abstract type

A similarity index over a set $P = \{p_0, \dots, p_{n-1}\}$ with a distance $\delta$, built once for a fixed $k$, with these operations:

- **neighbors**$(i)$: the $k$ points nearest to $p_i$ among $P \setminus \{p_i\}$, in order of distance (fewer if $n - 1 < k$).
- **reverse**$(i)$: the points that have $p_i$ in their list, the [reverse nearest neighbors](/reverse-nearest-neighbor/) of $p_i$ within $P$.
- **search**$(q, k', ef, S)$: up to $k'$ points near a query $q$, found by a walk along the edges from the start set $S$. The answer is approximate; the walk is exact only under the conditions of the theorem below.

When two points are at the same distance, the smaller index is taken first, so the graph is well defined.

## Representation

An [adjacency list](/adjacency-list/): an array of $n$ lists, list $i$ holding the indices of the $k$ out-neighbors of $p_i$ in order of distance. Many systems also store the distances, which saves work in construction methods such as [NN-descent](/nn-descent/). The reverse lists are computed on demand in $O(nk)$ time.

Two other graphs come from it. The **symmetric** (or undirected) $k$-NN graph keeps an edge $\{p, x\}$ if either point lists the other. The **mutual** $k$-NN graph keeps it only if both do. The directed graph and these two are used in different places below.

## Operations

```pseudo id=main
BUILD(P, k)
L1  for i ← 0 to n − 1
L2    for each j ≠ i, with d ← δ(p_i, p_j)
L3      offer (d, j) to a max-heap H_i that keeps the k least pairs
L4    N(i) ← the indices in H_i, in increasing order of (d, j)
```

Line L3 is [top-$k$ selection](/top-k-selection/) with a [binary heap](/binary-heap/) of size $k$: the new pair replaces the root when it is less than the root. Line L4 sorts the $k$ survivors.

**Search** is a best-first beam search with a candidate min-heap $C$, a result max-heap $W$ of at most $ef$ pairs, and a visited set $V$:

```pseudo id=search
SEARCH(q, k', ef, S)
L5  V ← S; C ← S, keyed by δ(q, ·); W ← the ef nearest points of S
L6  while C is not empty
L7    c ← extract the nearest point of C; if δ(q, c) > δ(q, farthest of W) then stop
L8    for each e ∈ N(c) with e ∉ V: add e to V; if |W| < ef or δ(q, e) < δ(q, farthest of W) then add e to C and W, and remove the farthest of W if |W| > ef
L9  return the k' nearest points of W
```

With $ef = 1$ this is plain greedy search: move to a better neighbor until there is none. A larger $ef$ keeps more paths open, as in [beam search](/beam-search/). It is the same procedure as SEARCH-LAYER in [HNSW](/hnsw/), run on one graph.

## Example

Six points on a line, at $0, 1, 3, 6, 10, 11$ (indices 0 to 5), with $k = 2$ and $\delta(x, y) = |x - y|$:

| point | position | out-neighbors | in-neighbors |
|---|---|---|---|
| 0 | 0 | 1, 2 | 1, 2 |
| 1 | 1 | 0, 2 | 0, 2 |
| 2 | 3 | 1, 0 | 0, 1, 3 |
| 3 | 6 | 2, 4 | 4, 5 |
| 4 | 10 | 5, 3 | 3, 5 |
| 5 | 11 | 4, 3 | 4 |

Point 2 has two candidates at distance 3, points 0 and 3; the tie goes to index 0. So no arrow leaves the set $\{0, 1, 2\}$: point 3 lists 2, but none of 0, 1, 2 lists 3.

Search for $q = 9$ with $k' = 1$, $ef = 2$, start $S = \{0\}$. The walk expands 0 (distance 9), adds 1 (distance 8) and 2 (distance 6), and drops 0 from $W$. It expands 2 and 1; their neighbors are all visited, and $C$ becomes empty. The answer is point 2 at distance 6, but the true nearest point is 4 at distance 1. The walk never left $\{0, 1, 2\}$.

From $S = \{5\}$ the walk expands 5 (distance 2), adds 4 (distance 1) and 3 (distance 3), keeps $W = \{4, 5\}$, expands 4, and returns point 4 at distance 1, the correct answer.

## Correctness

The full proofs are in the proof file. The main facts:

**Build.** List $N(i)$ is the sequence of the $k$ least pairs $(\delta(p_i, p_j), j)$ over $j \ne i$, in increasing order. This is the invariant of top-$k$ selection with a bounded heap: after each offer, $H_i$ holds the $\min(k, \text{offers})$ least pairs offered so far.

**Search ends.** Each point enters $V$ at most once, and enters $C$ only when it enters $V$, so line L7 runs at most $n$ times.

**The first answer is a local minimum.** Let $w$ be the nearest point returned. Then no out-neighbor of $w$ is strictly nearer to $q$ than $w$. So greedy search with $ef = 1$ stops at a point that is a local minimum of $\delta(q, \cdot)$ in the graph, which may not be the global one, as the example shows.

**Theorem (exact search on the reachable set).** If $ef \ge n$, SEARCH returns the $k'$ nearest points to $q$ among the points reachable from $S$ along directed edges, with ties broken by index. In particular, if every point is reachable from $S$, the search is exact.

There is no general guarantee for $ef < n$, and the $k$-NN graph itself may have no path from $S$ to the answer: in the example, the set $\{0, 1, 2\}$ has no outgoing edge.

## Complexity

| operation | time | space |
|---|---|---|
| build (brute force) | $n(n-1)$ distance evaluations, $O(n^2 (E + \log k))$ | $O(nk)$ |
| neighbors$(i)$ | $O(1)$ to get the list, $O(k)$ to read it | none |
| reverse, all points | $O(nk)$ | $O(nk)$ |
| search | at most $n$ expansions, $O(nk)$ distance evaluations, $O(nk (E + \log(nk)))$ | $O(n)$ |

All bounds are worst-case on the real RAM, where $E$ is the time of one distance evaluation. Each expansion at line L8 reads $k$ edges and pushes at most $k$ pairs on $C$, so the heaps hold $O(nk)$ pairs. In practice a search with small $ef$ expands a small number of points, but no bound below $\Theta(n)$ holds in the worst case: on the line example with points added to the far left, a greedy walk from the far left moves one point per step.

The out-degree is exactly $\min(k, n - 1)$. The in-degree is not bounded by $k$: in the plane, a point can be the nearest neighbor of at most 6 others when ties are broken consistently, and in $\mathbb{R}^D$ the bound grows exponentially in $D$. In high dimension the in-degrees become very uneven; see [hubness](/hubness/).

## Variants

- **Symmetric and mutual graphs.** Adding reverse edges makes the walk reach more points and is the usual fix for the trap in the example. Mutual $k$-NN graphs are sparser and are used to find dense groups and outliers.
- **Approximate graphs.** [NN-descent](/nn-descent/) improves a random graph by the rule "a neighbor of a neighbor is likely a neighbor" and finds most true edges with far fewer than $n^2$ distance evaluations on many data sets, with no worst-case guarantee.
- **Navigable graphs.** [Navigable small world](/navigable-small-world/) graphs, [HNSW](/hnsw/) and [DiskANN](/diskann/) start from near neighbors but prune edges to keep them in different directions and add long edges, so that greedy walks reach the answer in few steps.
- **$\varepsilon$-graphs.** Connect all pairs at distance at most $\varepsilon$, as in [fixed-radius near neighbors](/fixed-radius-near-neighbors/). The degree adapts to the density instead of being fixed at $k$.

## When to use it

- When the task needs the neighbors of every data point: [spectral clustering](/spectral-clustering/), [DBSCAN](/dbscan/), [UMAP](/umap/), [t-SNE](/t-sne/), [Isomap](/isomap/), outlier scores based on the $k$-th distance.
- As the base layer of a graph index for approximate search, once it is made symmetric or pruned for navigation.
- For answering new queries directly, prefer [HNSW](/hnsw/) or a tree such as the [k-d tree](/kd-tree/) for low dimension: a plain $k$-NN graph gives no guarantee.

## Pitfalls

- **Disconnection.** The directed graph, and even the symmetric one, can have several components when the data form separate clusters. A walk from one cluster never finds an answer in another. Start from several points or add long edges.
- **Self and duplicates.** A point must not list itself. With duplicate points, several neighbors are at distance 0, and the tie rule decides which are kept.
- **Asymmetry.** $x \in N(p)$ does not imply $p \in N(x)$. Code that assumes symmetry, for example in clustering, must build the symmetric graph explicitly.
- **Cost of the brute-force build.** $n(n-1)$ distance evaluations are too many for $n$ in the millions; use the methods of [k-nearest neighbor graph construction](/k-nearest-neighbor-graph-construction/).

## Implementations

## History

The all-nearest-neighbors problem, the case $k = 1$, was solved in $O(n \log n)$ time in fixed dimension by Vaidya in 1989. Callahan and Kosaraju built the $k$-nearest neighbor graph in $O(n \log n + kn)$ time in 1995 with the [well-separated pair decomposition](/well-separated-pair-decomposition/). Dong, Charikar and Li made approximate construction for general distances practical with NN-descent in 2011, and listed the uses of the graph for search and in learning.

## References
