---
tag: TWFCT6
kind: concept
slug: proximity-graphs
name: Proximity graphs
aliases:
- proximity graph family
- empty-region graphs
area: geometry/proximity
level: advanced
summary: Family of graphs whose edges join point pairs that satisfy a geometric closeness criterion.
prereqs: [delaunay-triangulation, minimum-spanning-tree, euclidean-distance]
see_also: [gabriel-graph, relative-neighborhood-graph, urquhart-graph, beta-skeleton, nearest-neighbor-graph, yao-graph, geometric-spanner, euclidean-minimum-spanning-tree]
sources:
  - paper: doi:10.1109/5.163414
    title: Jerzy W. Jaromczyk and Godfried T. Toussaint, Relative neighborhood graphs and their relatives, Proceedings of the IEEE 80(9), 1992, 1502-1517
    locator: the survey of proximity graphs defined by empty regions, the inclusion hierarchy, and algorithms
  - paper: doi:10.1016/0031-3203(80)90066-7
    title: Godfried T. Toussaint, The relative neighbourhood graph of a finite planar set, Pattern Recognition 12(4), 1980, 261-268
    locator: the inclusions MST in RNG in DT
  - paper: doi:10.1111/j.1538-4632.1980.tb00031.x
    title: David W. Matula and Robert R. Sokal, Properties of Gabriel graphs relevant to geographic variation research and the clustering of points in the plane, Geographical Analysis 12(3), 1980, 205-222
    locator: the inclusions between the minimum spanning tree, the relative neighborhood graph, the Gabriel graph and the Delaunay triangulation
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 9, Delaunay Triangulations (the empty-circle characterization of Delaunay edges, and the exercises on the Gabriel graph, the relative neighborhood graph and the Euclidean minimum spanning tree)
---

A proximity graph on a set $P$ of points joins two points when they are close in some geometric sense. Most of the classical ones are empty-region graphs: $p$ and $q$ are joined when a region attached to the segment $pq$ contains no other point of $P$. The size of the region decides the density. A small region, such as a circle through $p$ and $q$ with nothing inside, gives the [Delaunay triangulation](/delaunay-triangulation/). The circle with diameter $pq$ gives the [Gabriel graph](/gabriel-graph/). The lune of two disks of radius $\|pq\|$ gives the [relative neighborhood graph](/relative-neighborhood-graph/). The [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) and the [nearest neighbor graph](/nearest-neighbor-graph/) close the chain. For every point set in the plane,
$$\text{NNG} \subseteq \text{MST} \subseteq \text{RNG} \subseteq \text{GG} \subseteq \text{DT},$$
where the first inclusion needs distinct distances and the others hold for every minimum spanning tree and every Delaunay triangulation.

## In plain words

Given a cloud of points, which ones should count as neighbours? There is no single answer, so geometry offers a ladder of answers, from strict to generous.

The strictest links each point only to its closest point. One step up is the cheapest network that connects everything. Then come networks where a link survives as long as no other point stands "between" the two ends, with "between" measured by a shape around the link: a fat almond shape, a circle, or any empty circle through both points. The smaller the shape, the easier it is to keep it empty, and the more links survive.

Each rung contains the one below it. All of them are networks without crossing links, so each has fewer than three links per point.

## The idea

**Empty-region graphs.** Fix for each pair $p, q$ a region $R(p, q)$. The graph has the edge $pq$ when $R(p, q) \cap P \subseteq \{p, q\}$. The main examples, from the largest region to the smallest:

| graph | region $R(p, q)$ | exact test for a third point $r$ |
| --- | --- | --- |
| relative neighborhood graph | open lune: both open disks of radius $\|pq\|$ around $p$ and $q$ | $\max(\|pr\|^2, \|qr\|^2) < \|pq\|^2$ |
| Gabriel graph | closed disk with diameter $pq$ | $(p - r) \cdot (q - r) \le 0$ |
| Delaunay graph | some closed disk with $p$, $q$ on its boundary | no such disk is empty |

For the Delaunay graph the region is not fixed: the edge exists when at least one closed disk through $p$ and $q$ avoids all other points. A larger region is harder to keep empty, so containment of regions gives containment of graphs in the opposite direction. The [beta-skeletons](/beta-skeleton/) make this a continuous family with a parameter $\beta$: $\beta = 1$ is the Gabriel graph, $\beta = 2$ the relative neighborhood graph, and the graphs shrink as $\beta$ grows.

**Why each inclusion holds.**

- *NNG in MST.* If $q$ is the nearest neighbour of $p$ and all distances are distinct, $pq$ is the unique lightest edge leaving the set $\{p\}$, so by the [cut property](/cut-property/) it lies in the minimum spanning tree.
- *MST in RNG.* If a third point $r$ is in the lune of an MST edge $pq$, then $\|pr\| < \|pq\|$ and $\|qr\| < \|pq\|$. Deleting $pq$ splits the tree into the side of $p$ and the side of $q$; one of $pr$ and $rq$ crosses between them and is shorter, so the tree was not minimum. This uses no general position.
- *RNG in GG.* If $r$ is in the closed disk with diameter $pq$, then $(p - r) \cdot (q - r) \le 0$, and expanding $\|pq\|^2 = \|(p - r) - (q - r)\|^2$ gives $\|pq\|^2 \ge \|pr\|^2 + \|qr\|^2$. Both terms are positive, so $r$ is strictly closer to $p$ and to $q$ than $\|pq\|$: it is in the lune.
- *GG in DT.* The disk with diameter $pq$ is a closed disk with $p$ and $q$ on its boundary. If it is empty, $pq$ is an edge of the Delaunay graph by the [empty-circle characterization](/empty-circle-property/), and every Delaunay triangulation contains the Delaunay graph.

**General position and the cocircular case.** When no four points are on a circle, the Delaunay graph is a triangulation and the chain ends in a unique graph. When four or more points are cocircular, the Delaunay graph has faces with more than three sides, and a Delaunay triangulation must add diagonals by an arbitrary choice. The Gabriel graph is still inside every such triangulation, because it is inside the Delaunay graph itself. For the corners of a unit square, the Gabriel graph, the RNG and the Delaunay graph are all the four sides, and each of the two Delaunay triangulations adds one diagonal. Ties in distances affect the bottom of the chain: for three points at equal distance, every pair is a nearest neighbour pair, the NNG is a triangle, and no spanning tree contains it.

**Planarity and size.** All graphs in the chain are subgraphs of a Delaunay triangulation, so they are planar straight-line graphs with at most $3n - 6$ edges for $n \ge 3$, and all except the NNG are connected, since they contain a spanning tree. The [Yao graph](/yao-graph/), the [Urquhart graph](/urquhart-graph/) and the [k-nearest neighbor graph](/k-nearest-neighbor-graph/) are proximity graphs outside this exact chain: the Urquhart graph lies between the RNG and the DT, while the Yao graph contains the MST but need not be planar.

## Examples

For $P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, a set in general position, an exact brute-force computation gives:

| graph | edges | what is added at this rung |
| --- | --- | --- |
| NNG | 4 | $(1,3)(5,1)$, $(1,11)(2,8)$, $(9,6)(11,4)$, $(11,1)(11,4)$; three components |
| MST | 6 | $(1,3)(2,8)$ of squared length 26 and $(5,1)(11,1)$ of squared length 36 join the components |
| RNG | 7 | $(2,8)(9,6)$, squared length 53, closes a cycle |
| GG | 8 | $(5,1)(9,6)$: $(11,1)$ is in its lune but outside its diametral disk |
| DT | 12 | $(1,3)(1,11)$, $(1,11)(9,6)$, $(2,8)(5,1)$, $(5,1)(11,4)$; each has a point in its diametral disk, for the last one $(11,1)$ exactly on the circle |

The Urquhart graph of this set equals the Gabriel graph, and the 8-cone Yao graph has 15 edges, including two that cross. The pages of the individual graphs give the computations.

## Where it is used

- **Clustering and shape.** [Single-linkage clustering](/single-linkage-clustering/) cuts the longest edges of the minimum spanning tree; RNG and Gabriel graphs give slightly richer skeletons that describe the shape of a dot pattern, which was Toussaint's motivation.
- **Spatial statistics and geography.** Gabriel and Sokal introduced their graph to decide which sampling sites are neighbours; spatial autocorrelation tests still use Gabriel and Delaunay neighbours.
- **Wireless networks.** Geographic routing protocols planarize the network by keeping only Gabriel or RNG edges, which each node can decide from the positions of its neighbours.
- **Computing the minimum spanning tree.** Since the MST lies in the RNG, the GG and the DT, it can be computed from $O(n)$ candidate edges in $O(n \log n)$ total time, see the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/).
- **Spanners.** When short paths matter, [geometric spanners](/geometric-spanner/) such as Delaunay triangulations, Yao graphs, and graphs from the [well-separated pair decomposition](/well-separated-pair-decomposition/) are used instead; the Gabriel graph and the RNG can have paths far longer than the straight-line distance.

## References
