---
tag: B483NH
kind: problem
slug: euclidean-minimum-spanning-tree
name: Euclidean minimum spanning tree
aliases:
- Euclidean MST
- geometric MST
- EMST
area: geometry/proximity
level: advanced
summary: Find a minimum-weight spanning tree on a point set where edge weights are Euclidean distances.
prereqs: [minimum-spanning-tree, euclidean-distance, delaunay-triangulation]
see_also: [proximity-graphs, relative-neighborhood-graph, bichromatic-closest-pair, well-separated-pair-decomposition, yao-graph, single-linkage-clustering, steiner-tree-problem, closest-pair-of-points]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: the Euclidean minimum spanning tree in the plane in O(n log n) time from the Voronoi diagram
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (the Euclidean minimum spanning tree, its relation to the Voronoi diagram, and its lower bound)
  - paper: doi:10.1137/0211059
    title: Andrew Chi-Chih Yao, On constructing minimum spanning trees in k-dimensional spaces and related problems, SIAM Journal on Computing 11(4), 1982, 721-736
    locator: the first subquadratic algorithms in fixed dimension, using nearest neighbours in cones
  - paper: "Pankaj K. Agarwal, Herbert Edelsbrunner, Otfried Schwarzkopf and Emo Welzl, Euclidean minimum spanning trees and bichromatic closest pairs, Discrete and Computational Geometry 6, 1991, 407-422"
    locator: the reduction of the Euclidean minimum spanning tree to bichromatic closest pair problems, and the resulting algorithms in dimension 3 and higher
  - paper: "Paul B. Callahan and S. Rao Kosaraju, Faster algorithms for some geometric graph problems in higher dimensions, Proceedings of the 4th Annual ACM-SIAM Symposium on Discrete Algorithms, 1993, 291-300"
    locator: the minimum spanning tree from bichromatic closest pairs of a well-separated pair decomposition
  - paper: "David Eppstein, Spanning trees and spanners, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 425-461"
    locator: the survey of geometric minimum spanning tree algorithms and their relation to bichromatic closest pairs
---

The Euclidean minimum spanning tree (EMST) of $n$ points is a [minimum spanning tree](/minimum-spanning-tree/) of the complete graph on the points, with each edge weighted by its Euclidean length. Running [Prim's algorithm](/prim/) on the complete graph solves it in $\Theta(n^2)$ time in any dimension. In the plane, the tree is contained in the [Delaunay triangulation](/delaunay-triangulation/), so Shamos and Hoey (1975) found it in $O(n \log n)$ time from $O(n)$ candidate edges, which is optimal in the algebraic decision tree model. In fixed dimension $d \ge 3$ the best algorithms are subquadratic but far from linear, and the problem is tied to the [bichromatic closest pair](/bichromatic-closest-pair/) problem. It is a member of the chain of [proximity graphs](/proximity-graphs/) and the backbone of [single-linkage clustering](/single-linkage-clustering/).

## In plain words

You have a set of towns and want to connect them all with cables, so that every town can reach every other one, using as little cable as possible. Cables run in straight lines and may only branch at towns.

The cheapest network never has a loop, so it is a tree. You could build it by repeatedly adding the shortest cable that does not close a loop, but there are a huge number of possible cables. The geometric shortcut is that a cable in the cheapest network always joins two towns that are "natural neighbours", with no other town between them, and in the plane each town has only a few such neighbours. Checking only those candidates is enough.

## Definition

**Input.** A list $P = (p_1, \ldots, p_n)$ of $n \ge 1$ points in $\mathbb{R}^d$, usually the plane. Points may repeat; for exact algorithms the coordinates are integers or rationals.

**Output.** A set $T$ of $n - 1$ pairs $\{i, j\}$ forming a spanning tree of $\{1, \ldots, n\}$ that minimizes the total length
$$w(T) = \sum_{\{i, j\} \in T} \|p_i - p_j\|.$$
For $n = 1$ the tree is empty. Equal points are joined by edges of length $0$.

**Exactness.** Which spanning tree is minimum depends only on the order of the edge lengths: [Kruskal's algorithm](/kruskal/) looks at nothing else. So an exact algorithm compares squared distances, which are integers for integer input, and never takes a square root. The total weight $w(T)$ is a sum of square roots; computing it is fine, but comparing such sums exactly is a different and much harder problem.

**Uniqueness.** If all $\binom{n}{2}$ distances are distinct, the tree is unique. With ties there can be several: for the four corners of a square, any three of the four sides form a minimum spanning tree.

## Variants

- **Other metrics.** The same question for the $L_1$ or $L_\infty$ distance; in the plane it is solved the same way, with the Delaunay triangulation for that metric.
- **Bottleneck tree.** Minimize the longest edge instead of the sum. Every minimum spanning tree is also a [minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/), so the same algorithms apply.
- **Steiner tree.** Allow extra branch points anywhere in the plane. The tree can be shorter, by up to a constant factor (three points at the corners of an equilateral triangle are joined more cheaply through the center), and the problem becomes NP-hard; see the [Steiner tree problem](/steiner-tree-problem/).
- **Approximate tree.** Find a spanning tree within a factor $1 + \varepsilon$ of the minimum. The minimum spanning tree of a $(1 + \varepsilon)$-[spanner](/geometric-spanner/) does this, in $O(n \log n)$ time in fixed dimension.
- **Maximum spanning tree.** The tree of largest total length, the opposite question.
- **Dynamic and kinetic versions.** Maintain the tree as points are inserted, deleted or move.

## Examples

For the seven points $P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, Kruskal's algorithm on the edges in order of squared length accepts or rejects:

| edge | squared length | decision |
| --- | --- | --- |
| $(9,6)$, $(11,4)$ | 8 | accept |
| $(11,1)$, $(11,4)$ | 9 | accept |
| $(1,11)$, $(2,8)$ | 10 | accept |
| $(1,3)$, $(5,1)$ | 20 | accept |
| $(1,3)$, $(2,8)$ | 26 | accept |
| $(9,6)$, $(11,1)$ | 29 | reject: closes a cycle with the two accepted edges at $(11,4)$ |
| $(5,1)$, $(11,1)$ | 36 | accept, the tree is complete |

The total length is $2\sqrt{2} + 3 + \sqrt{10} + 2\sqrt{5} + \sqrt{26} + 6 \approx 24.56$. All six edges are among the 12 edges of the Delaunay triangulation of $P$, and the [relative neighborhood graph](/relative-neighborhood-graph/) has just one more edge, $(2,8)$, $(9,6)$.

**Points on a line.** For points on the $x$-axis, the tree joins each point to its neighbour in sorted order. So the tree gives the sorted order, which is the basis of the lower bound below.

**Degree.** Around a point, two tree edges always make an angle of at least $60°$: if $pq$ and $pr$ made a smaller angle, $qr$ would be strictly shorter than the longer of the two, and exchanging would give a lighter tree. So every vertex of a planar EMST has degree at most 6; the six neighbours of the center of a regular hexagon show that 6 happens.

## Known algorithms

| algorithm | time | setting | idea |
| --- | --- | --- | --- |
| [Prim](/prim/) on the complete graph | $\Theta(n^2)$ | any dimension | array-based Prim, no geometry; the best choice when $d$ is large |
| [Delaunay triangulation](/delaunay-triangulation/) and [Kruskal](/kruskal/) (Shamos and Hoey, 1975) | $O(n \log n)$ | plane | the tree lies in the triangulation, which has $O(n)$ edges |
| [Yao graph](/yao-graph/) (Yao, 1982) | $o(n^2)$ | fixed $d$ | nearest neighbour in each of a few cones per point gives $O(n)$ candidate edges |
| bichromatic closest pairs (Agarwal, Edelsbrunner, Schwarzkopf and Welzl, 1991) | about $n^{4/3}$ up to logarithmic factors for $d = 3$ | fixed $d \ge 3$ | grow the tree by repeated bichromatic closest pair queries |
| [WSPD](/well-separated-pair-decomposition/) (Callahan and Kosaraju, 1993) | $O(T_{BCP}(n) \log n)$ | fixed $d$ | one bichromatic closest pair per well-separated pair gives the candidate edges |
| [Boruvka](/boruvka/) with nearest neighbour queries | $O(\log n)$ rounds of nearest neighbour searches | any dimension, practical | each component finds its nearest outside point with a [k-d tree](/kd-tree/) |
| $(1 + \varepsilon)$-spanner, then Kruskal | $O(n \log n)$ | fixed $d$, approximate | MST of a sparse spanner |

Here $T_{BCP}(n)$ is the time to find a bichromatic closest pair between two sets with $n$ points in total.

**Why the candidate graphs work.** Every edge of a minimum spanning tree is the lightest edge across some cut, by the [cut property](/cut-property/), and an edge $pq$ that is strictly the longest edge of some cycle is in no minimum spanning tree, by the [cycle property](/cycle-property/). If a point $r$ lies strictly inside the lune of $pq$, then $pq$ is the longest edge of the triangle $p, q, r$, so the tree lies in the relative neighborhood graph; the chain $\text{RNG} \subseteq \text{GG} \subseteq \text{DT}$ on the [proximity graphs](/proximity-graphs/) page then puts it in every Delaunay triangulation. This holds even with ties and cocircular points.

## Bounds

- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, already in one dimension. The shortest tree edge is a [closest pair](/closest-pair-of-points/), so the [element distinctness](/element-distinctness/) bound applies: the numbers $x_i$ are distinct exactly when the tree of the points $(x_i, 0)$ has no edge of length $0$.
- **Plane.** $O(n \log n)$, matching the lower bound.
- **Fixed dimension $d \ge 3$.** Subquadratic algorithms exist, with exponents that tend to 2 as $d$ grows; no $O(n \log n)$ algorithm is known for $d \ge 3$.
- **High dimension.** When $d$ is part of the input, the $\Theta(n^2 d)$ Prim algorithm is the reference; no exact algorithm that is subquadratic in $n$ for every $d$ is known.

## Reductions

- **Closest pair reduces to EMST.** The shortest tree edge is a closest pair.
- **Sorting reduces to EMST in one dimension.** The tree of points on a line is the path in sorted order, read off in $O(n)$ time.
- **EMST reduces to the Delaunay triangulation in the plane.** Compute the triangulation, then run Kruskal on its at most $3n - 6$ edges; the [Voronoi diagram](/voronoi-diagram/) gives the same edges.
- **EMST and bichromatic closest pair.** Bichromatic closest pair reduces to EMST: the tree of the union of the red and blue points contains a shortest red-blue edge, by the cut property for the cut between red and blue. Conversely, Agarwal, Edelsbrunner, Schwarzkopf and Welzl, and Callahan and Kosaraju, reduce EMST to bichromatic closest pair computations with a logarithmic overhead, so in fixed dimension the two problems have nearly the same complexity.

## Applications

- **Clustering.** Removing the $k - 1$ longest tree edges gives the $k$ clusters of [single-linkage clustering](/single-linkage-clustering/); astronomers use the same idea, called friends-of-friends, to find groups of galaxies.
- **Approximating harder problems.** Doubling the tree and shortcutting gives a tour at most twice the optimal for the [Euclidean TSP](/euclidean-tsp/), and the tree is within a constant factor of the shortest [Steiner tree](/steiner-tree-problem/).
- **Network design.** Cheapest wiring for pipelines, cables or circuit nets when branching happens only at the sites.
- **Image and shape analysis.** Minimum spanning trees of pixels or feature points give segmentations and skeletons; see [image segmentation](/image-segmentation/).
- **Candidate graphs for other problems.** The tree is the bottom of the chain of [proximity graphs](/proximity-graphs/) and is contained in every [Yao graph](/yao-graph/) with at least six cones.

## References
