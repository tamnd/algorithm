---
tag: 5K0BMD
kind: problem
slug: all-nearest-neighbors
name: All nearest neighbors
aliases:
- all-pairs nearest neighbor
- all nearest neighbours
area: geometry/proximity
level: advanced
summary: For every input point, find its nearest other input point.
prereqs: [closest-pair-of-points, nearest-neighbor-search, euclidean-distance]
see_also: [nearest-neighbor-graph, k-nearest-neighbor-graph, delaunay-triangulation, well-separated-pair-decomposition, kd-tree-nearest-neighbor-search, reverse-nearest-neighbor, bichromatic-closest-pair, closest-pair-of-points]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: all nearest neighbours in the plane in O(n log n) time from the Voronoi diagram
  - paper: "Pravin M. Vaidya, An O(n log n) algorithm for the all-nearest-neighbors problem, Discrete and Computational Geometry 4, 1989, 101-115"
    locator: the deterministic O(n log n) algorithm in every fixed dimension
  - paper: "Kenneth L. Clarkson, Fast algorithms for the all nearest neighbors problem, Proceedings of the 24th Annual Symposium on Foundations of Computer Science, 1983, 226-232"
    locator: the randomized O(n log n) algorithm in fixed dimension
  - paper: doi:10.1145/200836.200853
    title: Paul B. Callahan and S. Rao Kosaraju, A decomposition of multidimensional point sets with applications to k-nearest-neighbors and n-body potential fields, Journal of the ACM 42(1), 1995, 67-90
    locator: all k nearest neighbours from the well-separated pair decomposition
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (the all nearest neighbours problem and its relation to the Voronoi diagram)
---

The all nearest neighbors problem asks, for each of $n$ points, for another input point at the smallest distance from it. Running a brute-force scan for each point takes $\Theta(n^2)$ time. In the plane, every nearest neighbour pair is an edge of the [Delaunay triangulation](/delaunay-triangulation/), so Shamos and Hoey (1975) solved the problem in $O(n \log n)$ time; Clarkson (1983, randomized) and Vaidya (1989, deterministic) reached $O(n \log n)$ in every fixed dimension. Since the [closest pair](/closest-pair-of-points/) is the smallest of the $n$ answers, the $\Omega(n \log n)$ lower bound of that problem carries over. The output, read as a directed graph, is the [nearest neighbor graph](/nearest-neighbor-graph/).

## In plain words

Picture a crowd on a square, and ask every person who is standing closest to them. Answering it one person at a time, by measuring the distance to everyone else, takes a long time when the crowd is large.

The faster methods notice that your closest person is always one of your immediate neighbours in a natural map of who borders whom. Draw that map once, and each person only has to compare a handful of candidates. In the plane, a person can be the closest for at most six others, so the answers are spread out.

## Definition

**Input.** A list $P = (p_1, \ldots, p_n)$ of $n \ge 2$ points in $\mathbb{R}^d$. Points may repeat; for exact algorithms the coordinates are integers or rationals.

**Output.** For each $i$, an index $\text{nn}(i) \ne i$ with
$$\|p_i - p_{\text{nn}(i)}\| = \min_{j \ne i} \|p_i - p_j\|.$$
If a point is repeated, its nearest neighbour is a copy at distance $0$. With ties, any nearest point is correct; implementations often take the smallest index so that the answer is unique and testable.

**Exactness.** All comparisons are between squared distances; for integer input they are exact, and the float tie of $10^{16}$ and $10^{16} + 1$ cannot occur.

## Variants

- **k nearest neighbours.** For each point, its $k$ closest other points: the [k-nearest neighbor graph](/k-nearest-neighbor-graph/). Callahan and Kosaraju solve it in $O(n \log n + kn)$ time in fixed dimension.
- **Bichromatic version.** For each red point, its nearest blue point; the smallest answer is the [bichromatic closest pair](/bichromatic-closest-pair/).
- **Approximate version.** Each answer within a factor $1 + \varepsilon$ of the true nearest distance, as with [approximate nearest neighbor](/approximate-nearest-neighbor/) structures; in high dimension this is the only practical version.
- **All farthest neighbours.** For each point, the farthest other point. It is solved in the plane with the farthest-point Voronoi diagram, and the largest answer is the [farthest pair](/farthest-pair/).
- **Reverse question.** For a point $q$, which points have $q$ as nearest neighbour: [reverse nearest neighbor](/reverse-nearest-neighbor/) search.

## Examples

For $P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$:

| point | nearest neighbour | squared distance | second nearest, squared distance |
| --- | --- | --- | --- |
| $(1,3)$ | $(5,1)$ | 20 | $(2,8)$, 26 |
| $(1,11)$ | $(2,8)$ | 10 | $(1,3)$, 64 |
| $(2,8)$ | $(1,11)$ | 10 | $(1,3)$, 26 |
| $(5,1)$ | $(1,3)$ | 20 | $(11,1)$, 36 |
| $(9,6)$ | $(11,4)$ | 8 | $(11,1)$, 29 |
| $(11,1)$ | $(11,4)$ | 9 | $(9,6)$, 29 |
| $(11,4)$ | $(9,6)$ | 8 | $(11,1)$, 9 |

Three pairs are mutual nearest neighbours: $(1,11), (2,8)$, then $(1,3), (5,1)$, then $(9,6), (11,4)$. The point $(11,4)$ is the nearest neighbour of two points. The smallest answer, 8, gives the closest pair. The seven answers form four distinct edges, all among the 12 Delaunay edges of $P$.

**Duplicates.** For $P = \{(0,0), (3,4), (0,0)\}$ the two copies of $(0,0)$ are each other's nearest neighbours at distance $0$, and $(3,4)$ has either copy at distance $5$. An implementation that removes duplicates first answers the wrong question.

## Known algorithms

| algorithm | time | setting | idea |
| --- | --- | --- | --- |
| brute force | $\Theta(n^2)$ | any dimension | scan all others for each point |
| [Delaunay triangulation](/delaunay-triangulation/) or [Voronoi diagram](/voronoi-diagram/) (Shamos and Hoey, 1975) | $O(n \log n)$ | plane | the nearest neighbour is a Delaunay neighbour; scan the $O(n)$ edges |
| randomized (Clarkson, 1983) | $O(n \log n)$ expected | fixed $d$ | randomized subdivision of space |
| Vaidya (1989) | $O(n \log n)$ | fixed $d$ | hierarchical subdivision into boxes, constant $2^{O(d)}$ |
| [WSPD](/well-separated-pair-decomposition/) (Callahan and Kosaraju, 1995) | $O(n \log n + kn)$ for $k$ neighbours | fixed $d$ | the pair that separates $p$ from its nearest neighbour has $\{p\}$ on one side |
| [k-d tree](/kd-tree-nearest-neighbor-search/) queries | $O(n \log n)$ expected for well-spread data (Friedman, Bentley and Finkel, 1977) | low $d$, practical | build one tree, query each point while skipping itself |

**Why Delaunay neighbours suffice.** Let $q$ be a nearest neighbour of $p$. Any point $x \ne p, q$ in the closed disk with diameter $pq$ sees $pq$ at an angle of at least $90°$, so $\|p - x\| < \|p - q\|$, which is impossible. So the disk is empty, $pq$ is an edge of the [Gabriel graph](/gabriel-graph/), and hence of every Delaunay triangulation. This needs no general position.

## Bounds

- **Lower bound.** $\Omega(n \log n)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, since the [closest pair](/closest-pair-of-points/) is the minimum of the answers, and that problem has this bound by [element distinctness](/element-distinctness/).
- **Upper bound.** $O(n \log n)$ in every fixed dimension, so the problem is solved optimally in that model; the constant grows exponentially with $d$.
- **Output size.** In the plane, with distinct points, a point is the nearest neighbour of at most 6 others: two points $a, b$ that both have $q$ as nearest neighbour satisfy $\|a - b\| \ge \max(\|a - q\|, \|b - q\|)$, so the angle $aqb$ is at least $60°$.
- **High dimension.** When $d$ is part of the input, no algorithm is known that is much faster than $n^2$ for exact answers in the worst case, which is why approximate methods dominate there.

## Reductions

- **Closest pair reduces to it.** Take the smallest of the $n$ answers.
- **It reduces to the Delaunay triangulation.** In the plane, compute the triangulation and, for each point, its closest Delaunay neighbour, in $O(n)$ extra time.
- **It reduces to $n$ nearest neighbour queries.** Build a [nearest neighbor search](/nearest-neighbor-search/) structure once and query every point, excluding the point itself.
- **It is the bichromatic version with one colour.** All nearest neighbours of $P$ are the per-point answers of the bichromatic problem with $R = B = P$ and the pair $i = i$ excluded.

## Applications

- **Nearest neighbour graphs and clustering.** The answers form the [nearest neighbor graph](/nearest-neighbor-graph/); its components are a first clustering, and density-based methods such as [DBSCAN](/dbscan/) use neighbour distances to set their radius.
- **Manifold learning.** Methods such as [Isomap](/isomap/) start from the $k$ nearest neighbours of every sample; see [manifold learning](/manifold-learning/).
- **Outliers and density.** The distance to the nearest or $k$-th nearest neighbour estimates the local density; points with a large distance are outlier candidates.
- **Spatial statistics.** The mean nearest neighbour distance tests whether a pattern of points is clustered, random or regular, as in the Clark and Evans test.
- **Mesh generation and simulation.** Particle methods and [mesh generation](/mesh-generation/) need, for every point, its closest neighbours to set local sizes or interaction lists.

## References
