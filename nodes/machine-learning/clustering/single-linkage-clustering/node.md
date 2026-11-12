---
tag: NRPC50
kind: algorithm
slug: single-linkage-clustering
name: Single-linkage clustering
aliases:
area: machine-learning/clustering
level: core
summary: "Agglomerative clustering that merges the two clusters with the closest pair of points. Its tree is Kruskal's algorithm on a minimum spanning tree."
solves: [hierarchical-clustering-problem]
model: real-ram
complexity:
  vars: {n: the number of points}
  time: {worst: "Θ(n^2)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1951
  people: [Kazimierz Florek, Peter H. A. Sneath, John C. Gower, Gavin J. S. Ross]
  note: Florek and others (1951) and Sneath (1957) used the method in taxonomy. Gower and Ross (1969) showed that it is the same as a minimum spanning tree.
prereqs: [agglomerative-clustering, minimum-spanning-tree, kruskal]
see_also: [slink, prim, maximum-spacing-k-clustering, ultrametric, hdbscan, euclidean-minimum-spanning-tree, minimum-bottleneck-spanning-tree, complete-linkage-clustering]
sources:
  - paper: doi:10.2307/2346439
    title: "J. C. Gower and G. J. S. Ross, Minimum spanning trees and single linkage cluster analysis, Journal of the Royal Statistical Society, Series C (Applied Statistics) 18(1) (1969), 54-64"
    locator: the equivalence of the single linkage hierarchy and the minimum spanning tree, and the algorithm that derives one from the other
  - paper: doi:10.1093/comjnl/16.1.30
    title: "R. Sibson, SLINK: an optimally efficient algorithm for the single-link cluster method, The Computer Journal 16(1) (1973), 30-34"
    locator: the O(n^2) time and O(n) memory bound for the single link method
  - paper: "P. H. A. Sneath, The application of computers to taxonomy, Journal of General Microbiology 17(1) (1957), 201-226"
    locator: the single linkage method for the classification of bacteria
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 4.7 (clustering of maximum spacing by Kruskal's algorithm)
  - paper: "Gunnar Carlsson and Facundo Mémoli, Characterization, stability and convergence of hierarchical clustering methods, Journal of Machine Learning Research 11 (2010), 1425-1470"
    locator: single linkage as the unique method under their axioms, and its output as the subdominant ultrametric
  - book: isbn:9780130222787
    title: Anil K. Jain and Richard C. Dubes, Algorithms for Clustering Data
    locator: Chapter 3, Section 3.2 (the single-link method and its graph form)
---

Single-linkage clustering is [agglomerative clustering](/agglomerative-clustering/) with the single [linkage](/linkage-criterion/): the dissimilarity of two clusters is the smallest dissimilarity between a point of one and a point of the other. Gower and Ross (1969) showed that its merges are exactly the edges that [Kruskal's algorithm](/kruskal/) adds on the complete graph of the points, in the same order. So the tree comes from a [minimum spanning tree](/minimum-spanning-tree/): build the tree with [Prim's algorithm](/prim/) in $\Theta(n^2)$ time, sort its $n - 1$ edges, and replay them. The cophenetic distance of the tree is the largest edge on the tree path, which is the subdominant [ultrametric](/ultrametric/). The method finds clusters of any shape, but a chain of close points can join two clusters that should stay apart. This effect is called chaining.

## In plain words

Two groups are as close as their two closest members, one from each group. At each step, join the two closest groups.

This is the same as a simple rule on a map. Draw a line between the two closest points. Then draw the next shortest line, but skip any line that joins two points already connected. Each line joins two groups. The lines form a tree that connects all points with the least total length.

To get some number of groups, remove the longest lines of that tree. The groups that remain are the clusters. A thin trail of points can hold two large groups together, because only one short step is needed to cross.

## The problem

The input is an $n \times n$ symmetric dissimilarity matrix $D$ with a zero diagonal, or a function that returns $D(u, v)$. The output is the single linkage hierarchy: the $n - 1$ merges of the greedy rule that always merges the two clusters $A, B$ with the smallest $\min_{a \in A, b \in B} D(a, b)$, with that value as the height. It solves the [hierarchical clustering problem](/hierarchical-clustering-problem/) for the single linkage.

## The algorithm

Lines L1 to L6 are Prim's algorithm on the complete graph, in the form for a dense graph: $\text{best}[v]$ is the smallest dissimilarity from $v$ to the tree so far. Lines L7 to L9 replay the tree edges in increasing order with a [disjoint-set](/disjoint-set/) structure. Each edge joins two clusters and becomes one merge.

```pseudo id=main
SINGLE-LINKAGE(D)                     ▷ D is n × n, the points are 1..n
L1  put point 1 in the tree, best[v] ← D[1, v] for each v
L2  edges ← empty list
L3  repeat n − 1 times
L4      k ← the point outside the tree with the smallest best[k]
L5      add k to the tree, append (best[k], the tree point that gave best[k], k) to edges
L6      for each v outside the tree, best[v] ← min(best[v], D[k, v])
L7  sort edges by weight
L8  for each edge (w, u, v) in this order do
L9      UNION(FIND(u), FIND(v)) and record the merge of the two clusters at height w
L10 return the merges
```

The cut into $k$ clusters undoes the last $k - 1$ merges, which is the same as a deletion of the $k - 1$ longest tree edges. That cut is the [maximum spacing k-clustering](/maximum-spacing-k-clustering/).

## Example

Take the six points $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$ on a line, with $D(x, y) = |x - y|$. Prim's algorithm from $a$ adds $b$ with the edge $ab$ of weight 2, then $c$ by $bc$ of weight 1, then $d$ by $cd$ of weight 4, then $e$ by $de$ of weight 6, then $f$ by $ef$ of weight 8. Sorted, the edges give these merges.

| merge | edge | height | new cluster |
|---|---|---|---|
| 1 | $bc$ | 1 | $\{b, c\}$ |
| 2 | $ab$ | 2 | $\{a, b, c\}$ |
| 3 | $cd$ | 4 | $\{a, b, c, d\}$ |
| 4 | $de$ | 6 | $\{a, b, c, d, e\}$ |
| 5 | $ef$ | 8 | all six |

After the first merge, each merge adds one single point to the big cluster: this is chaining in its purest form. The cut into three clusters drops the edges $ef$ and $de$, and gives $\{a, b, c, d\}$, $\{e\}$, $\{f\}$. The closest two points in different clusters are $d$ and $e$, at distance 6, and no partition into three clusters has a larger spacing. [Complete linkage](/complete-linkage-clustering/) instead gives $\{a, b, c\}$, $\{d, e\}$, $\{f\}$ on the same points. The cophenetic distance of $a$ and $f$ is 8, the largest edge on the path from $a$ to $f$, though the two points are 21 apart.

## Correctness

Before each merge, the clusters are the components of the forest of the tree edges replayed so far. For two points $x$ and $y$ in different components, the path between them in the minimum spanning tree has an edge that is not yet replayed, so its weight is at least the next weight $w$. By the [cycle property](/cycle-property/), the largest edge on that path is at most $D(x, y)$. So no two clusters are closer than $w$, and the next edge joins two clusters at exactly $w$, which is a greedy single linkage step. The same argument shows that the height at which two points first share a cluster is the minimax path value, the subdominant ultrametric. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Time.** Prim's algorithm on the dense matrix takes $\Theta(n^2)$ time: each of the $n - 1$ rounds scans and updates $O(n)$ values. The sort takes $O(n \log n)$ time and the replay $O(n\,\alpha(n))$. The total is $\Theta(n^2)$.
- **Memory.** Besides the input, the method keeps $O(n)$ values: best, the origin of each best value, the edges and the disjoint sets. If the dissimilarity is a function of the points, no matrix is needed at all.
- **Optimality.** A general dissimilarity matrix needs $\Omega(n^2)$ reads for an exact single linkage tree (see the [problem page](/hierarchical-clustering-problem/)), so the time is optimal. [SLINK](/slink/) reaches the same bounds without a spanning tree.
- **Geometric input.** For points in the plane, the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) takes $O(n \log n)$ time, and so does single linkage.

## Properties

- **Unique cophenetic distance.** With ties, the binary tree can differ, but the cophenetic distance is always the minimax path value. So the non-binary tree is unique, even with ties.
- **Monotone.** The heights are the sorted edge weights.
- **Invariant under monotone maps.** If $f$ is increasing, the tree of $f(D)$ is the tree of $D$ with the heights mapped by $f$. Only the order of the dissimilarities matters for the shape.
- **Maximum spacing.** Each cut maximizes the smallest distance between two clusters, by the [maximum spacing theorem](/maximum-spacing-optimality/).
- **Axiomatic.** Carlsson and Mémoli (2010) proved that single linkage is the only hierarchical method that satisfies their axioms of stability and consistency.
- **Chaining.** It is space-contracting: a cluster grows toward the nearest point, wherever it is. Noise points between two clusters can join them.

## Variants and improvements

- **[SLINK](/slink/).** Sibson (1973) builds the pointer form of the tree one point at a time, in $\Theta(n^2)$ time and $\Theta(n)$ memory.
- **Other spanning tree algorithms.** [Kruskal](/kruskal/) or [Borůvka](/boruvka/) on a sparse graph of candidate edges, such as a $k$-nearest-neighbor graph, gives an approximate tree for very large data.
- **Robust single linkage and [HDBSCAN](/hdbscan/).** Replace $D$ with the mutual reachability distance, which uses the distance to the $k$-th nearest neighbor, and then run single linkage. This reduces chaining through sparse noise.
- **[DBSCAN](/dbscan/).** The clusters of DBSCAN at a radius are related to a single linkage cut on the core points.
- **Distributed versions.** Borůvka's rounds merge many components at once, which suits parallel computers.

## When to use it

Use single linkage when clusters may have long or curved shapes and are separated by gaps, for example clusters along roads or rivers. Use it when you need the maximum spacing clustering, or the subdominant ultrametric. Its $O(n)$ memory makes it the hierarchical method for the largest $n$. Do not use it on noisy data without a fix such as HDBSCAN, because one bridge of noise points joins two clusters.

## Pitfalls

- **Chaining.** The cut at $k$ often gives one giant cluster and $k - 1$ outliers, as in the example. Look at the sizes of the clusters before you trust a cut.
- **A matrix that is not needed.** Prim's algorithm on a function of the points needs no $n \times n$ matrix. Building one wastes $\Theta(n^2)$ memory.
- **A heap in the dense case.** Prim's algorithm with a binary heap takes $O(n^2 \log n)$ time on a complete graph. The array version above is faster.
- **Ties.** Different spanning trees give different binary trees. Compare cophenetic distances or cuts, not merge lists.

## Implementations

## History

The Wrocław school of Florek, Łukaszewicz, Perkal, Steinhaus and Zubrzycki described the method in 1951 as a way to link points of a finite set. Sneath (1957) used it to classify bacteria, and it became the first method of numerical taxonomy. Gower and Ross (1969) showed that the single linkage tree and the minimum spanning tree hold the same information, which gave fast algorithms. Sibson (1973) gave SLINK, with optimal time and memory. Kleinberg and Tardos (2005) teach the method as the clustering of maximum spacing.

## References
