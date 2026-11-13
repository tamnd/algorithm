---
tag: E8A1SK
kind: concept
slug: geometric-spanner
name: Geometric spanner
aliases:
- t-spanner
- Euclidean spanner
- stretch factor
area: geometry/proximity
level: research
summary: Sparse graph on points whose shortest-path distances approximate Euclidean distances within a factor t.
prereqs: [euclidean-distance, shortest-path, dijkstra]
see_also: [yao-graph, well-separated-pair-decomposition, delaunay-triangulation, proximity-graphs, euclidean-minimum-spanning-tree, planar-graph, all-pairs-shortest-paths, motion-planning]
sources:
  - book: isbn:9780521815130
    title: Giri Narasimhan and Michiel Smid, Geometric Spanner Networks, Cambridge University Press, 2007
    locator: the definitions of t-spanners and their quality measures, the Theta-graph, the well-separated pair spanner, the greedy spanner, and the lower bounds
  - paper: "Ingo Althöfer, Gautam Das, David Dobkin, Deborah Joseph and José Soares, On sparse spanners of weighted graphs, Discrete and Computational Geometry 9(1), 1993, 81-100"
    locator: the greedy spanner algorithm
  - paper: "L. Paul Chew, There are planar graphs almost as good as the complete graph, Journal of Computer and System Sciences 39(2), 1989, 205-219"
    locator: planar spanners from Delaunay triangulations under other distance functions
  - paper: "J. Mark Keil and Carl A. Gutwin, Classes of graphs which approximate the complete Euclidean graph, Discrete and Computational Geometry 7(1), 1992, 13-28"
    locator: the stretch bound 2 pi / (3 cos(pi/6)), about 2.42, for the Delaunay triangulation
  - paper: "Ge Xia, The stretch factor of the Delaunay triangulation is less than 1.998, SIAM Journal on Computing 42(4), 2013, 1620-1659"
    locator: the upper bound 1.998 on the stretch of the Delaunay triangulation
  - paper: "Prosenjit Bose, Luc Devroye, William Evans and David Kirkpatrick, On the spanning ratio of Gabriel graphs and beta-skeletons, SIAM Journal on Discrete Mathematics 20(2), 2006, 412-427"
    locator: the worst-case spanning ratio of the Gabriel graph, of order the square root of n
---

A geometric spanner is a graph $G$ on a set $P$ of points whose edges are weighted by their Euclidean length and in which every pair of points is joined by a short path. It is a $t$-spanner, for a real $t \ge 1$, when
$$d_G(p, q) \le t \, \|p - q\| \quad \text{for all } p, q \in P,$$
where $d_G$ is the [shortest-path](/shortest-path/) distance in $G$. The smallest such $t$ is the stretch factor, also called dilation or spanning ratio. The complete graph is a 1-spanner with $\binom{n}{2}$ edges; the point of spanners is to get stretch close to 1 with $O(n)$ edges, and often with extra properties such as bounded degree, small total weight, or planarity. The main constructions are the [Yao and Theta graphs](/yao-graph/), the [well-separated pair decomposition](/well-separated-pair-decomposition/), the greedy spanner, and the [Delaunay triangulation](/delaunay-triangulation/).

## In plain words

Think of towns and a road network. The best network for travel would be a straight road between every two towns, but that is far too many roads. A spanner is a network with few roads in which every trip, going along the roads, is at most a fixed factor longer than the straight line, for example at most twice as long.

The factor is the price paid for building fewer roads. Some networks keep it very low with only a handful of roads per town. Others, like the cheapest network that connects all towns, can force huge detours between two towns that are close but sit at opposite ends of a long chain.

## The idea

**Measuring the stretch.** For a given graph, the stretch is the largest ratio $d_G(p, q) / \|p - q\|$ over all pairs. Running [Dijkstra's algorithm](/dijkstra/) from every vertex computes it in $O(n (m + n \log n))$ time for $m$ edges; this is how the stretches on this page were checked. The ratio involves sums of square roots, so it is compared with a tolerance; the graph constructions themselves can be exact.

**Quality measures.** Besides the stretch $t$, a spanner is judged by its number of edges, its maximum degree, its weight compared with the [minimum spanning tree](/euclidean-minimum-spanning-tree/), its hop diameter (the number of edges needed on $t$-paths), whether it is plane, and its fault tolerance.

**Easy bounds.**

- A $t$-spanner is connected, so it has at least $n - 1$ edges.
- If no three points are collinear, the only 1-spanner is the complete graph: a path of length exactly $\|p - q\|$ must run along the segment $pq$, and no other point lies on it.
- A plane spanner cannot have stretch below $\sqrt{2}$ in general: for the four corners of a square, a plane graph misses at least one of the two crossing diagonals, and the path between its ends has length at least two sides, $\sqrt{2}$ times the diagonal.
- The [minimum spanning tree](/euclidean-minimum-spanning-tree/) has no constant stretch: for $n$ points evenly spaced on a circle it is a path around the circle, and its two ends, which are neighbours on the circle, have stretch $n - 1$.

**Constructions.**

| construction | edges | stretch | remarks |
| --- | --- | --- | --- |
| [Yao graph](/yao-graph/) or Theta-graph, cone angle $\theta < \pi/3$ | $O(n/\theta)$ | $1/(1 - 2\sin(\theta/2))$ | local: each point picks its own edges |
| [WSPD](/well-separated-pair-decomposition/) with separation $s > 4$ | $O(s^d n)$ | $(s+4)/(s-4)$ | any $1 + \varepsilon$ with $s = 4 + 8/\varepsilon$, $O(n \log n)$ time |
| greedy spanner | $O(n)$ in fixed dimension | any chosen $t > 1$ | bounded degree and weight $O(\text{MST})$; the sparsest in practice |
| [Delaunay triangulation](/delaunay-triangulation/) | at most $3n - 6$ | below $1.998$ | plane; no parameter |
| [Gabriel graph](/gabriel-graph/), [RNG](/relative-neighborhood-graph/), MST | $O(n)$ | grows with $n$ | not spanners: Gabriel graph $\Theta(\sqrt{n})$ in the worst case |

The greedy spanner takes the pairs in order of increasing distance and adds the edge $pq$ when the graph built so far has no path of length at most $t \|p - q\|$. Every pair that is skipped already has a $t$-path, and the edges added later only shorten paths, so the result is a $t$-spanner for exactly the chosen $t$. Run directly, it makes one shortest-path query per pair, which costs about $n^3 \log n$ time; faster versions exist. Althöfer, Das, Dobkin, Joseph and Soares (1993) introduced it, and its size, degree and weight bounds are in Narasimhan and Smid.

For the Delaunay triangulation, the stretch bound improved from a first constant by Dobkin, Friedman and Supowit to about $2.42$ by Keil and Gutwin (1992) and to $1.998$ by Xia (2013); some point sets need stretch above $1.59$, so the exact worst case is still open. Chew (1989) showed that Delaunay triangulations for other distance functions are spanners with stretch $\sqrt{10}$ and $2$.

## Examples

The seven points $P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$ of the [proximity graphs](/proximity-graphs/) page, with stretches computed by all-pairs Dijkstra:

| graph | edges | stretch | worst pair |
| --- | --- | --- | --- |
| Delaunay triangulation | 12 | $1.273$ | $(1,3)$, $(9,6)$ |
| Gabriel graph | 8 | $1.342$ | $(5,1)$, $(11,4)$ |
| relative neighborhood graph | 7 | $1.847$ | $(5,1)$, $(9,6)$ |
| minimum spanning tree | 6 | $2.939$ | $(2,8)$, $(9,6)$ |
| greedy spanner, $t = 1.1$ | 14 | $1.082$ | $(9,6)$, $(11,1)$ |
| Yao graph, 8 cones | 15 | $1.11$ | $(1,3)$, $(11,4)$ |

In the minimum spanning tree, $(2,8)$ and $(9,6)$ are about $7.3$ apart, but the tree path goes down through $(1,3)$, $(5,1)$, $(11,1)$ and $(11,4)$, almost three times as long. Adding that one edge gives the relative neighborhood graph and cuts the stretch to $1.85$.

On larger inputs the gap widens. For 100 random points with integer coordinates in $[0, 10^4]$ (seed 1), the Delaunay triangulation has 285 edges and stretch $1.37$; the Gabriel graph $1.57$; the RNG $2.76$; the minimum spanning tree $17.6$. The greedy spanner with $t = 1.5$ has only 172 edges, fewer than the triangulation, with stretch $1.498$.

## Where it is used

- **Network design.** Road, rail and communication networks trade the number or length of links against detours; wireless topology control keeps a sparse spanner of the radio graph, often a Yao graph built locally.
- **Approximation algorithms.** Running an exact graph algorithm on a $(1 + \varepsilon)$-spanner instead of the complete graph approximates many geometric problems. The minimum spanning tree of a $t$-spanner weighs at most $t$ times the [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), and spanners are a step of approximation schemes for the [Euclidean TSP](/euclidean-tsp/).
- **Motion planning.** Clarkson used cone graphs to approximate shortest paths among obstacles, as a sparse substitute for the [visibility graph](/visibility-graph/) in [motion planning](/motion-planning/).
- **Distance oracles.** A sparse spanner, preprocessed for shortest-path queries, answers approximate distance queries; see [distance oracles](/distance-oracle/).
- **Metric spaces.** The same definitions apply to points in any metric, and spanners of graphs, where the stretch is measured against the graph distance, are used in distributed computing and routing.

## References
