---
tag: VDMAD0
kind: problem
slug: bichromatic-closest-pair
name: Bichromatic closest pair
aliases:
- two-set closest pair
- bipartite closest pair
- red-blue closest pair
- BCP
area: geometry/proximity
level: advanced
summary: Given two point sets, find the closest pair with one point from each set.
prereqs: [closest-pair-of-points, euclidean-distance, voronoi-diagram]
see_also: [euclidean-minimum-spanning-tree, well-separated-pair-decomposition, nearest-neighbor-search, delaunay-triangulation, hausdorff-distance, approximate-nearest-neighbor, orthogonal-vectors-hypothesis, single-linkage-clustering]
sources:
  - paper: "Pankaj K. Agarwal, Herbert Edelsbrunner, Otfried Schwarzkopf and Emo Welzl, Euclidean minimum spanning trees and bichromatic closest pairs, Discrete and Computational Geometry 6, 1991, 407-422"
    locator: algorithms for the bichromatic closest pair in dimension 3 and higher, and the equivalence with the Euclidean minimum spanning tree
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (nearest neighbour queries by Voronoi diagram and point location)
  - paper: "Michiel Smid, Closest-point problems in computational geometry, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 877-935"
    locator: the survey of closest-pair problems and their variants
  - paper: "David Eppstein, Spanning trees and spanners, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 425-461"
    locator: the relation between bichromatic closest pairs and geometric minimum spanning trees
---

The bichromatic closest pair problem gives two finite point sets, red points $R$ and blue points $B$, and asks for a red point and a blue point at the smallest distance. Checking all $|R| \cdot |B|$ pairs is the obvious method. In the plane the answer is an edge of the [Delaunay triangulation](/delaunay-triangulation/) of $R \cup B$, which gives $O(N \log N)$ time for $N = |R| + |B|$ points; in one dimension sorting suffices. Unlike the [closest pair](/closest-pair-of-points/) problem, there is no packing argument: two red points may be arbitrarily close, and only the red-blue distances count. In dimension $d \ge 3$ the best algorithms are subquadratic but far from linear, and the problem has nearly the same complexity as the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), which motivated its study.

## In plain words

You have two kinds of places on a map, for example fire stations and houses, and you want the fire station and the house that are nearest to each other. Distances between two stations or between two houses do not matter.

The obvious method measures every station against every house. The faster methods prepare one of the two sets, for example by dividing the map into the regions that are nearest to each station, so that each house can find its nearest station quickly. The best pair is the best of these answers.

## Definition

**Input.** Two lists $R = (r_1, \ldots, r_m)$ and $B = (b_1, \ldots, b_n)$ of points in $\mathbb{R}^d$, both nonempty. A point may appear in both lists and points may repeat. For exact algorithms the coordinates are integers or rationals.

**Output.** Indices $i, j$ with
$$\|r_i - b_j\| = \delta(R, B) = \min_{a, c} \|r_a - b_c\|,$$
and usually the value $\delta(R, B)$ or its square. If a point is both red and blue, the answer is $0$. If several pairs reach the minimum, any of them is correct.

**Exactness.** As for the closest pair, the comparisons are between squared distances, which are exact integers for integer input; floating-point square roots can merge two different distances, for example $10^{16}$ and $10^{16} + 1$.

**Relation to the sets' distance.** $\delta(R, B)$ is the distance between the two sets in the sense of the infimum over pairs. The [Hausdorff distance](/hausdorff-distance/) uses the maximum over one set of the distance to the other instead, and is a different quantity.

## Variants

- **Monochromatic closest pair.** If $R = B$, with the pair $i = j$ excluded, the problem is the [closest pair](/closest-pair-of-points/) problem.
- **Decision version.** Is there a red-blue pair at distance at most $\varepsilon$? Unlike the monochromatic case, a grid of side $\varepsilon$ does not make it easy, because a cell may hold many red points and the cell next to it many blue points, all slightly more than $\varepsilon$ apart.
- **All red nearest neighbours.** For each red point, its nearest blue point; the bichromatic closest pair is the smallest of these.
- **Bichromatic farthest pair.** The red-blue pair at the largest distance, a relative of the [farthest pair](/farthest-pair/) problem.
- **Approximate version.** Find a red-blue pair within a factor $1 + \varepsilon$ of $\delta(R, B)$, with [approximate nearest neighbor](/approximate-nearest-neighbor/) structures or the [well-separated pair decomposition](/well-separated-pair-decomposition/) in fixed dimension, and with locality-sensitive hashing in high dimension.
- **Other metrics and inner products.** The same question for $L_1$, $L_\infty$ or Hamming distance, or the maximum inner product between the sets.

## Examples

Color the seven points of the [proximity graphs](/proximity-graphs/) page as $R = \{(9,6), (11,1), (11,4)\}$ and $B = \{(1,3), (1,11), (2,8), (5,1)\}$. The closest pair of all seven points, $(9,6)$ and $(11,4)$ at squared distance $8$, is red-red and does not count. The red-blue squared distances closest to the minimum are

| pair | squared distance |
| --- | --- |
| $(5,1)$, $(11,1)$ | 36 |
| $(5,1)$, $(9,6)$ | 41 |
| $(5,1)$, $(11,4)$ | 45 |
| $(2,8)$, $(9,6)$ | 53 |

so $\delta^2(R, B) = 36$ and the pair is $(5,1)$, $(11,1)$. This edge is also the edge of the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) that joins the red and the blue parts, as the cut property predicts.

**One dimension.** For red numbers $3, 10, 11$ and blue numbers $6, 14$, the merged sorted order is $3^R, 6^B, 10^R, 11^R, 14^B$. The closest red-blue pair is one of the adjacent pairs with different colours, here $14 - 11 = 3$, tied with $6 - 3 = 3$. The red pair $10, 11$ is closer but does not count.

## Known algorithms

| algorithm | time | setting | idea |
| --- | --- | --- | --- |
| brute force | $\Theta(mn)$ | any dimension | check every red-blue pair |
| sort and merge | $O(N \log N)$ | one dimension | the answer is adjacent in the merged order |
| [Delaunay triangulation](/delaunay-triangulation/) of $R \cup B$ | $O(N \log N)$ | plane | scan the red-blue Delaunay edges |
| [Voronoi diagram](/voronoi-diagram/) of $B$ and point location | $O(N \log N)$ | plane | find the nearest blue point of each red point |
| Agarwal, Edelsbrunner, Schwarzkopf and Welzl (1991) | about $N^{4/3}$ up to logarithmic factors for $d = 3$, randomized | fixed $d \ge 3$ | divide and conquer with nearest neighbour structures for subsets |
| [k-d tree](/kd-tree/) queries | no good worst-case bound | practical, low $d$ | query each red point against a tree on $B$ |
| [WSPD](/well-separated-pair-decomposition/) or approximate nearest neighbours | $O(N \log N)$ for fixed $d$ and $\varepsilon$ | approximate | $(1 + \varepsilon)$-approximate answer |

**Why the Delaunay edge.** Let $r, b$ be a bichromatic closest pair. A point $x \ne r, b$ inside the closed disk with diameter $rb$ satisfies $\|x - r\| < \|r - b\|$ and $\|x - b\| < \|r - b\|$, because the angle at $x$ is at least $90°$. If $x$ is red, $x, b$ is a closer red-blue pair; if blue, $r, x$ is. So the disk is empty, $rb$ is an edge of the [Gabriel graph](/gabriel-graph/) of $R \cup B$, and therefore of every Delaunay triangulation. When $r$ and $b$ coincide the distance is $0$ and the pair is found by sorting.

## Bounds

- **Lower bound.** $\Omega(N \log N)$ in the [algebraic decision tree](/algebraic-decision-tree/) model, already in one dimension: two sets of numbers are disjoint exactly when $\delta(R, B) > 0$, and set disjointness has this lower bound by [Ben-Or's theorem](/ben-or-theorem/), like [element distinctness](/element-distinctness/).
- **Plane.** $O(N \log N)$, matching the lower bound.
- **Fixed dimension $d \ge 3$.** Subquadratic, with exponents tending to 2 as $d$ grows; no near-linear exact algorithm is known.
- **High dimension.** For 0/1 vectors, squared Euclidean distance equals Hamming distance. When $d$ grows faster than $\log N$, exact bichromatic closest pair has no algorithm running in $O(N^{2 - \delta})$ time for a constant $\delta > 0$ under the [orthogonal vectors hypothesis](/orthogonal-vectors-hypothesis/), a [conditional lower bound](/conditional-lower-bound/) that explains why practical systems settle for approximate answers.

## Reductions

- **Set disjointness reduces to it.** Map the numbers of the two sets to red and blue points on a line; the sets intersect exactly when the answer is $0$.
- **It reduces to nearest neighbour queries.** Build a [nearest neighbour](/nearest-neighbor-search/) structure on $B$ and query it with every red point.
- **It reduces to the Euclidean minimum spanning tree.** Every minimum spanning tree of $R \cup B$ contains a shortest edge across the cut between red and blue, by the [cut property](/cut-property/), so scanning the $N - 1$ tree edges finds the answer.
- **The minimum spanning tree reduces to it.** In fixed dimension the tree can be computed with bichromatic closest pair queries at a logarithmic overhead (Agarwal and coauthors; Callahan and Kosaraju through the [WSPD](/well-separated-pair-decomposition/)), so the two problems have nearly the same complexity.

## Applications

- **Minimum spanning trees.** The reduction above is how subquadratic Euclidean minimum spanning tree algorithms in dimension 3 and higher work.
- **Clustering.** In [single-linkage clustering](/single-linkage-clustering/), the distance between two clusters is the bichromatic closest pair distance of their points.
- **Spatial joins.** Databases pair objects of two tables by proximity, such as each customer with the nearest store, and the closest pair is the first answer of a distance join.
- **Separation of two sets.** The bichromatic closest pair distance tells how far apart two shapes sampled by points are, for example in collision checks between two point clouds.

## References
