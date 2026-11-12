---
tag: XAAHPM
kind: problem
slug: maximum-spacing-k-clustering
name: Maximum-spacing k-clustering
aliases:
- max-spacing clustering
- maximum split clustering
area: machine-learning/clustering
level: core
summary: "Partition n points into k nonempty clusters so that the least distance between two points in different clusters is as large as possible."
prereqs: [clustering-problem, minimum-spanning-tree, kruskal]
see_also: [maximum-spacing-optimality, single-linkage-clustering, prim, spanning-forest, euclidean-minimum-spanning-tree, minimum-bottleneck-spanning-tree, k-center-problem, disjoint-set]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 4.7 (Clustering), the k-clustering of maximum spacing by Kruskal's algorithm
  - paper: doi:10.1093/comjnl/16.1.30
    title: "R. Sibson, SLINK: an optimally efficient algorithm for the single-link cluster method, The Computer Journal 16(1) (1973), 30-34"
    locator: the single link hierarchy, whose cuts give the clusterings of maximum spacing
  - paper: doi:10.2307/2346439
    title: "J. C. Gower and G. J. S. Ross, Minimum spanning trees and single linkage cluster analysis, Journal of the Royal Statistical Society Series C 18(1) (1969), 54-64"
    locator: the single linkage clusters as the parts of a minimum spanning tree after the deletion of its longest edges
  - paper: doi:10.1007/BF02614317
    title: "Pierre Hansen and Brigitte Jaumard, Cluster analysis and mathematical programming, Mathematical Programming 79 (1997), 191-215"
    locator: the split of a partition, which is its spacing, and the maximum split problem solved by a minimum spanning tree
---

The maximum-spacing k-clustering problem asks for a partition of $n$ points into $k$ nonempty clusters that makes the *spacing*, the least distance between two points in different clusters, as large as possible. So the clusters are as far apart as they can be. Unlike most clustering objectives, this one is easy: run [Kruskal's algorithm](/kruskal/) on all pairs and stop when $k$ components are left, or build a [minimum spanning tree](/minimum-spanning-tree/) and delete its $k - 1$ longest edges. The result is the cut of the [single-linkage](/single-linkage-clustering/) tree into $k$ clusters, and its spacing is the $(k - 1)$-th largest edge weight of the minimum spanning tree. The [maximum spacing theorem](/maximum-spacing-optimality/) proves that this is optimal.

## In plain words

You have a set of items, a distance for each pair, and a number $k$. Put the items into $k$ groups. Look at all pairs of items that are in different groups, and find the closest such pair. That distance is the gap between the groups. Make the gap as large as you can.

The way to do it: join the closest pair of items, then the next closest, and so on, but skip a pair that is already in one group. Stop when there are $k$ groups. The next pair that you would join is the gap.

## Definition

**Input.** A set $U$ of $n$ points, a distance $d(p, q) = d(q, p) \ge 0$ for each pair, and an integer $k$ with $2 \le k \le n$.

**Output.** A $k$-clustering, which is a partition $\mathcal{C} = \{C_1, \ldots, C_k\}$ of $U$ into $k$ nonempty sets, that maximizes the spacing

$$\text{spacing}(\mathcal{C}) = \min\{d(p, q) : p \in C_a,\ q \in C_b,\ a \ne b\}.$$

The distance need not be a metric. Only the order of the distances matters for which clustering is optimal. The optimal spacing is unique, but the optimal clustering need not be when distances are equal.

## Variants

- **On a graph.** The distances are given only for the $m$ edges of a graph, and two points with no edge are infinitely far apart. Kruskal's algorithm on the edges gives a minimum [spanning forest](/spanning-forest/), and the same rule works when the graph has at most $k$ connected components.
- **The decision form.** For a threshold $t$, is there a $k$-clustering with spacing at least $t$? This holds exactly when the graph of the pairs with $d < t$ has at least $k$ connected components.
- **Similarities.** With similarities in place of distances, minimize the largest similarity between clusters. Use a maximum spanning tree and delete its $k - 1$ lightest edges.
- **Spacing against diameter.** The problem of the least largest diameter for $k$ clusters, close to the [k-center problem](/k-center-problem/), is NP-hard. The two goals can conflict, and bicriterion versions trade the spacing against the diameter.
- **Euclidean points.** For points in the plane, the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) has only $O(n)$ edges, which makes the problem faster.

## Examples

**Points on a line.** Take $a, b, c, d, e, f$ at $0, 2, 3, 7, 13, 21$, with $d(x, y) = |x - y|$. The minimum spanning tree has the edges $bc$ 1, $ab$ 2, $cd$ 4, $de$ 6 and $ef$ 8.

| $k$ | delete | clustering | spacing |
|---|---|---|---|
| 2 | $ef$ | $\{a, b, c, d, e\}$, $\{f\}$ | 8 |
| 3 | $ef$, $de$ | $\{a, b, c, d\}$, $\{e\}$, $\{f\}$ | 6 |
| 4 | $ef$, $de$, $cd$ | $\{a, b, c\}$, $\{d\}$, $\{e\}$, $\{f\}$ | 4 |

For $k = 3$, the cut of [complete linkage](/complete-linkage-clustering/) is $\{a, b, c\}$, $\{d, e\}$, $\{f\}$, with spacing $d(c, d) = 4 < 6$. Its clusters are tighter, but closer to each other.

**Chaining.** Take $1, 2, \ldots, 10$ on a line and a far point at $100$. For $k = 2$, the best clustering is $\{1, \ldots, 10\}$, $\{100\}$ with spacing 90. A long chain of points with small gaps stays in one cluster however long it is. This is the reason the objective suits clusters of any shape, but also why one far outlier can be a cluster of its own.

**Ties.** For the points $0, 1, 2$ and $k = 2$, both $\{0\}, \{1, 2\}$ and $\{0, 1\}, \{2\}$ have the best spacing 1.

## Known algorithms

| algorithm | time | memory | note |
|---|---|---|---|
| [Kruskal](/kruskal/) on all pairs, stopped at $k$ components | $O(n^2 \log n)$ | $\Theta(n^2)$ | sort the pairs, union with a [disjoint-set](/disjoint-set/) structure |
| [Prim](/prim/) on the dense graph, then delete the $k - 1$ longest edges | $\Theta(n^2)$ | $\Theta(n)$ | optimal for a general distance |
| [SLINK](/slink/), then cut the tree at $k$ clusters | $\Theta(n^2)$ | $\Theta(n)$ | gives all $k$ at once |
| Kruskal on a graph with $m$ edges | $O(m \log n)$ | $O(m)$ | the graph form |
| Euclidean minimum spanning tree in the plane | $O(n \log n)$ | $O(n)$ | by the Delaunay triangulation |

After one minimum spanning tree, the clustering for every $k$ follows in $O(n \log n)$ time: sort the tree edges once. All these algorithms give the cut of the single linkage tree.

## Bounds

- **General distances.** $\Theta(n^2)$ time. Prim's algorithm on the dense graph gives the upper bound. For the lower bound, an algorithm that does not read the distance of some pair $p, q$ cannot tell whether $d(p, q)$ is much smaller than all other values, which changes the answer. Values in $[1, 2]$ keep every such matrix a metric.
- **Points in the plane.** $O(n \log n)$ time, by the Euclidean minimum spanning tree. For $k = n - 1$ with distinct distances, the answer is the [closest pair](/closest-pair-of-points/) as one cluster, so the problem is at least as hard as the closest pair problem.
- **The optimal value.** If the tree edges in increasing order have weights $w_1 \le \cdots \le w_{n-1}$, the best spacing is $w_{n-k+1}$, the $(k - 1)$-th largest.

## Reductions

- **To a minimum spanning tree.** The problem reduces to one minimum spanning tree and a selection of the $k - 1$ largest tree edges, in $O(n)$ extra time.
- **The decision form to connected components.** Spacing at least $t$ is possible exactly when the graph of the pairs with $d < t$ has at least $k$ components. If it has, group its components into $k$ clusters: a pair in different clusters is in different components, so its distance is at least $t$. If a $k$-clustering has spacing at least $t$, each pair with $d < t$ is inside one cluster, so each component lies in one cluster, and there are at least $k$ components.
- **From the cut of a dendrogram.** The single linkage [dendrogram](/dendrogram/) holds the optimal clustering for each $k$: undo its last $k - 1$ merges.
- **Bottleneck paths.** The spacing of the optimal $k$-clustering, for $k = 2$, is the largest bottleneck distance between two points, which is the largest edge of a [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/).

## Applications

- **Taxonomy and biology.** Single linkage clusters, which are the maximum-spacing clusterings, were among the first methods in numerical taxonomy.
- **Image segmentation.** Graph-based segmentation joins pixels in the order of Kruskal's algorithm, with a stop rule in place of a fixed $k$.
- **Detection of gaps and outliers.** A large spacing means that the clusters are well separated. A point that forms a cluster of its own at a small $k$ is far from all others.
- **Density-based clustering.** [HDBSCAN](/hdbscan/) runs the same minimum spanning tree method on a distance that is corrected for density.

## References
