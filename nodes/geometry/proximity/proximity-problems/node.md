---
tag: DY9YC7
kind: concept
slug: proximity-problems
name: Proximity problems
aliases:
- proximity queries
- geometric proximity
- closest-point problems
area: geometry/proximity
level: intro
summary: Problems asking which points are close to each other, or how close they are, under a geometric distance.
prereqs: [euclidean-distance, real-ram]
see_also: [closest-pair-of-points, all-nearest-neighbors, euclidean-minimum-spanning-tree, farthest-pair, nearest-neighbor-search, voronoi-diagram, closest-pair-lower-bound, proximity-graphs]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: the list of closest-point problems, their solution with the Voronoi diagram in O(n log n) time, and the lower bounds
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms, and Chapter 6, Proximity, variants and generalizations
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 7 (Voronoi diagrams) and Chapter 9 (Delaunay triangulations)
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the main theorem and its applications to element distinctness and geometric problems
---

Proximity problems ask which points of a set are close to each other, or how close they are: the [closest pair](/closest-pair-of-points/), the nearest neighbor of every point, the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), the [farthest pair](/farthest-pair/), and the [nearest neighbor](/nearest-neighbor-search/) of a query point. Shamos and Hoey showed in 1975 that one structure, the [Voronoi diagram](/voronoi-diagram/) and its dual the [Delaunay triangulation](/delaunay-triangulation/), solves most of them in the plane in $O(n \log n)$ time. A reduction from element uniqueness shows that this is optimal in the [algebraic decision tree](/algebraic-decision-tree/) model.

## In plain words

You have a map with many dots, such as shops or stars. Many questions about the dots are about closeness. Which two dots are the closest? Which dot is the nearest one for each dot? How can you join all dots with roads of the least total length? Which two dots are the farthest apart? Given a new dot, which old dot is nearest?

Checking every pair of dots answers all these questions, but the number of pairs grows very fast. The clever methods look at only a few pairs. The main tool divides the map into regions, one for each dot, holding the places that are nearer to that dot than to any other. Neighbouring regions tell you which pairs can matter. Building this map takes about as long as sorting the dots, and no method of a standard kind can do better.

## The idea

**Notation.** $P \subset \mathbb{R}^d$ is the input point set, $n = |P|$, $d$ is the dimension, and $p = (x, y)$ is a point of the plane. The distance is the [Euclidean distance](/euclidean-distance/) $\|p - q\|$ unless a page says otherwise. Algorithms run on the [real RAM](/real-ram/), and lower bounds use the [algebraic decision tree](/algebraic-decision-tree/) or the [algebraic computation tree](/algebraic-computation-tree/), named on each page.

**The main problems.** The table gives the planar case with $d = 2$. Each row links to its page.

| problem | output | best bound in the plane | lower bound |
| --- | --- | --- | --- |
| [closest pair](/closest-pair-of-points/) | $\min_{p \ne q} \lVert p - q \rVert$ | $\Theta(n \log n)$ worst case; $O(n)$ expected with the floor function | $\Omega(n \log n)$ algebraic decision tree |
| [all nearest neighbors](/all-nearest-neighbors/) | the nearest other point of every point | $\Theta(n \log n)$ | $\Omega(n \log n)$, by the same reduction |
| [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) | a spanning tree of least total length | $\Theta(n \log n)$ | $\Omega(n \log n)$ |
| [farthest pair](/farthest-pair/) | $\max_{p, q} \lVert p - q \rVert$ | $\Theta(n \log n)$ by the hull and [rotating calipers](/rotating-calipers/) | $\Omega(n \log n)$ algebraic decision tree |
| [nearest neighbor search](/nearest-neighbor-search/) | the nearest point of $P$ to a query $q$ | $O(\log n)$ query after $O(n \log n)$ preprocessing | $\Omega(\log n)$ per query in a decision tree of constant branching, since there are $n$ possible answers |
| [bichromatic closest pair](/bichromatic-closest-pair/) | the closest pair with one point from each of two sets | $\Theta(n \log n)$ | $\Omega(n \log n)$ |
| [collinear points](/collinear-points/) | three or more points on one line | $O(n^2)$ | the problem is [3SUM](/3sum/)-hard |

**Three common ingredients.**

1. *The locus approach.* The Voronoi cell of $p$ is the set of places nearer to $p$ than to any other point of $P$. The nearest neighbor of each point is a Voronoi neighbour, and the closest pair, the minimum spanning tree and the [relative neighborhood graph](/relative-neighborhood-graph/) are subgraphs of the Delaunay triangulation, which has at most $3n - 6$ edges. So after an $O(n \log n)$ construction, each of these problems needs only $O(n)$ or $O(n \log n)$ more work. Shamos and Hoey called this the locus approach.
2. *The lower bound.* Element uniqueness, "are $n$ real numbers distinct", needs $\Omega(n \log n)$ operations in the algebraic decision tree model by [Ben-Or's theorem](/ben-or-theorem/). Put the numbers on a line: they are distinct if and only if the closest pair distance is positive. So the closest pair, all nearest neighbors and the minimum spanning tree inherit the bound; see [closest pair lower bound](/closest-pair-lower-bound/).
3. *Exact comparisons.* Each algorithm compares distances. Comparing squared distances is exact with integer coordinates, and a float root can tie or reverse two different distances, as on the page on [Euclidean distance](/euclidean-distance/).

**The model matters.** The lower bound holds for algebraic decision trees, which have no floor function and no hashing. With the floor function and random choices, the closest pair takes $O(n)$ expected time by the [randomized grid method](/randomized-closest-pair/) of Rabin, and with a word RAM other bounds change too. In high dimension the exact problems suffer from the curse of dimensionality, and [approximate nearest neighbor](/approximate-nearest-neighbor/) methods trade a factor $1 + \varepsilon$ for speed.

## Examples

Take the six points $P = \{(1,1), (2,6), (3,4), (3,5), (4,8), (9,5)\}$. All 15 squared distances are different.

- **Closest pair.** $(3,4)$ and $(3,5)$, at squared distance $1$.
- **Farthest pair.** $(1,1)$ and $(9,5)$, at squared distance $64 + 16 = 80$.
- **All nearest neighbors.** With squared distances: $(1,1) \to (3,4)$ at $13$; $(2,6) \to (3,5)$ at $2$; $(3,4) \leftrightarrow (3,5)$ at $1$; $(4,8) \to (2,6)$ at $8$; $(9,5) \to (4,8)$ at $34$.
- **Euclidean minimum spanning tree.** [Kruskal's algorithm](/kruskal/) on the 15 pairs takes the edges of squared length $1, 2, 8, 13, 34$, in that order. These are exactly the nearest neighbor edges, because here the nearest neighbor graph is already connected. The total length is $1 + \sqrt{2} + \sqrt{8} + \sqrt{13} + \sqrt{34} \approx 14.679$.
- **Nearest neighbor query.** For the query $q = (6, 6)$, the squared distances are $50, 16, 13, 10, 8, 10$, so the nearest point is $(4, 8)$. Two points, $(3, 5)$ and $(9, 5)$, tie for the second place.

## Where it is used

- **Clustering.** Single-linkage clustering is the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) with its longest edges removed, and density-based methods use [nearest neighbor graphs](/nearest-neighbor-graph/).
- **Classification and search.** The $k$-nearest neighbor rule of machine learning, recommendation and similarity search are [nearest neighbor searches](/nearest-neighbor-search/), often [approximate](/approximate-nearest-neighbor/) and in high dimension, with [kd-trees](/kd-tree-nearest-neighbor-search/) or [locality-sensitive hashing](/locality-sensitive-hashing/).
- **Networks.** [Geometric spanners](/geometric-spanner/) and [proximity graphs](/proximity-graphs/) such as the [Gabriel graph](/gabriel-graph/) and the [relative neighborhood graph](/relative-neighborhood-graph/) are topologies for wireless and road networks.
- **Collision and traffic control.** The closest pair among moving objects, which was a motivation of Shamos and Hoey.
- **Shape comparison.** The [Hausdorff distance](/hausdorff-distance/) and the [Fréchet distance](/frechet-distance/) compare point sets and curves.

## References
