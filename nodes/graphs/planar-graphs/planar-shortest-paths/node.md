---
tag: WDGSD3
kind: problem
slug: planar-shortest-paths
name: Shortest paths in planar graphs
aliases:
- planar single-source shortest paths
area: graphs/planar-graphs
level: advanced
summary: Single-source shortest paths restricted to planar graphs, admitting faster algorithms than general graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: O(n)}
  space: {extra: O(n)}
prereqs: [single-source-shortest-paths, planar-graph, planar-separator-theorem]
see_also: [r-division, dijkstra, planar-dual-graph, planar-separator-finding, max-flow-problem, near-linear-negative-sssp, distance-oracle, monge-property]
sources:
  - paper: doi:10.1137/0216064
    title: Greg N. Frederickson, Fast algorithms for shortest paths in planar graphs, with applications, SIAM Journal on Computing 16(6), 1004 to 1022 (1987)
    locator: the r-division (there called a suitable division) and the O(n (log n)^(1/2)) single-source algorithm for nonnegative lengths
  - paper: doi:10.1006/jcss.1997.1493
    title: Monika R. Henzinger, Philip Klein, Satish Rao and Sairam Subramanian, Faster shortest-path algorithms for planar graphs, Journal of Computer and System Sciences 55(1), 3 to 23 (1997)
    locator: the linear-time single-source algorithm for nonnegative lengths using a recursive division and a scheduled Dijkstra
  - paper: doi:10.1016/j.jcss.2005.05.007
    title: Jittat Fakcharoenphol and Satish Rao, Planar graphs, negative weight edges, shortest paths, and near linear time, Journal of Computer and System Sciences 72(5), 868 to 889 (2006)
    locator: the dense distance graph, the Monge-based Dijkstra on it, and the O(n log^3 n) algorithm for negative lengths
  - paper: doi:10.1145/2488608.2488672
    title: Philip N. Klein, Shay Mozes and Christian Sommer, Structured recursive separator decompositions for planar graphs in linear time, STOC 2013, 505 to 514
    locator: the linear-time construction of recursive r-divisions with few holes, and its use in linear-time shortest paths
  - paper: "Richard J. Lipton, Donald J. Rose and Robert Endre Tarjan, Generalized nested dissection, SIAM Journal on Numerical Analysis 16(2), 346 to 358 (1979)"
    locator: the O(n^(3/2)) algorithm for planar shortest paths with negative lengths by nested dissection
---

The planar shortest path problem is [single-source shortest paths](/single-source-shortest-paths/) on a directed or undirected [planar graph](/planar-graph/) with edge lengths. Because a planar graph has at most $3n - 6$ edges and small [separators](/planar-separator-theorem/), it can be solved faster than on general graphs: in $O(n)$ time for nonnegative lengths (Henzinger, Klein, Rao and Subramanian, 1997), against $O(n \log n)$ for [Dijkstra](/dijkstra/) with a heap, and in $O(n \log^2 n / \log \log n)$ time for lengths that may be negative, against near-linear in $m$ with large polylogarithmic factors for general graphs. The tools behind these results, [r-divisions](/r-division/), dense distance graphs and the [Monge property](/monge-property/) of distances on a face, are the core of planar graph algorithms.

## In plain words

You want the shortest route from one place to every other place on a road map, where roads only meet at junctions, so the map can be drawn flat with no bridges.

On such a map, a short ring of junctions can always cut the map into two parts of similar size. The fast methods cut the map into many small pieces this way, solve each piece, and then only need to know the distances between the few junctions on the borders of the pieces. That saves the logarithmic factor of a priority queue for positive lengths, and much more when some lengths are negative.

## Definition

**Input.** A planar graph $G = (V, E)$ with $n$ vertices, directed or undirected, a length $\ell(e) \in \mathbb{R}$ for each edge, and a source $s$. Fast algorithms need a planar embedding, given as a [rotation system](/rotation-system/) $\rho$ ($\rho(v)$ lists the neighbours of $v$ counterclockwise); if only the graph is given, a [planarity test](/planarity-testing/) finds one in $O(n)$ time. The embedding is used to find cycle separators and the [faces](/planar-face/) of pieces.

**Output.** For every vertex $v$, the distance $d(s, v)$, the minimum length of a path from $s$ to $v$ ($+\infty$ if none exists), and a [shortest path tree](/shortest-path-tree/) given by parent pointers; or a negative cycle reachable from $s$, when lengths may be negative.

Planarity bounds the size: $m \le 3n - 6$ for simple graphs by the [edge bound](/planar-edge-bound/), so all running times are written in $n$ alone.

## Variants

- **Nonnegative lengths.** The main case, solved in $O(n)$ time.
- **Negative lengths.** Lengths may be negative, and the algorithm must find a negative cycle or the distances. This is the case with the largest gap to general graphs.
- **Unit lengths.** [Breadth-first search](/breadth-first-search/) already takes $O(n)$ time on any sparse graph; planarity gives nothing new here.
- **Multiple-source shortest paths.** All sources on one face, with distances available implicitly; Klein's algorithm takes $O(n \log n)$ time.
- **All pairs and distance oracles.** $n$ runs of the linear-time algorithm give all pairs in $O(n^2)$, which is optimal for explicit output; planar [distance oracles](/distance-oracle/) answer queries in polylogarithmic time from near-linear space.
- **Bounded genus and minor-free graphs.** Many of the techniques extend to graphs embedded on fixed surfaces and to graphs excluding a fixed minor.

## Examples

**How the embedding is given.** In these examples the graph is small enough that only the graph matters; the embedding would be the rotation system of the drawing.

| graph | source and lengths | result |
|---|---|---|
| a single vertex | itself | distance 0, the tree is the vertex |
| a tree | any lengths, any source | the unique path to each vertex is shortest, found by one [depth-first search](/depth-first-search/) in $O(n)$ time; a negative undirected edge is a negative cycle by itself when walked back and forth, so undirected trees need $\ell \ge 0$ |
| $K_4$ on $0, 1, 2, 3$ | $\ell(01) = 4$, $\ell(02) = 1$, $\ell(03) = 5$, $\ell(12) = 2$, $\ell(13) = 1$, $\ell(23) = 6$, source 0 | $d = (0, 3, 1, 4)$; the path to 3 is $0, 2, 1, 3$, shorter than the direct edge of length 5 |
| $K_5$, $K_{3,3}$ | any | not planar, so the planar algorithms do not apply; general algorithms are used. With unit lengths, $K_5$ has all distances 1, and $K_{3,3}$ has distance 1 to the other side and 2 to the own side |

The $K_4$ example shows why a shortest path tree need not use the cheapest edge at each vertex: the tree has edges $02$, $21$, $13$.

## Known algorithms

| algorithm | lengths | time | idea |
|---|---|---|---|
| [Dijkstra](/dijkstra/) with a binary heap | $\ge 0$ | $O(n \log n)$ | general algorithm, $m = O(n)$ |
| [Bellman-Ford](/bellman-ford/) | any | $O(n^2)$ | general algorithm, $m = O(n)$ |
| Lipton, Rose and Tarjan (1979) | any | $O(n^{3/2})$ | nested dissection with [separators](/planar-separator-theorem/) |
| Frederickson (1987) | $\ge 0$ | $O(n \sqrt{\log n})$ | an [r-division](/r-division/), Dijkstra on the boundary vertices with distances inside pieces precomputed |
| Henzinger, Klein, Rao and Subramanian (1997) | $\ge 0$ | $O(n)$ | a recursive division with a few levels; Dijkstra runs on each piece only for a limited number of steps before moving to another piece, so the heaps stay small |
| Fakcharoenphol and Rao (2006) | any | $O(n \log^3 n)$ | recursive cycle separators; the dense distance graph between boundary vertices is searched in nearly linear time in its number of vertices by the Monge property |
| Klein, Mozes and Weimann (2010) | any | $O(n \log^2 n)$ | one cycle separator per level, multiple-source shortest paths on the separator, and a Bellman-Ford over the separator using Monge search |
| Mozes and Wulff-Nilsen (2010) | any | $O(n \log^2 n / \log \log n)$ | the same framework with an unbalanced recursion |

Klein, Mozes and Sommer (2013) showed how to build the recursive r-divisions with few holes needed by the linear-time algorithm in $O(n)$ time; before, constructing them took $O(n \log n)$ time and the linear bound of Henzinger et al. needed a separately computed decomposition.

## Bounds

- **Nonnegative lengths.** $\Theta(n)$: the algorithm of Henzinger et al. is linear, and every algorithm must read the input and output $n$ distances.
- **Negative lengths.** $O(n \log^2 n / \log \log n)$ is the best known bound; whether linear time is possible is open. The general [near-linear algorithm](/near-linear-negative-sssp/) of Bernstein, Nanongkai and Wulff-Nilsen gives $O(n \log^8 n \log W)$ on planar inputs with integer lengths of absolute value at most $W$, slower than the planar algorithms.
- **Why a heap is not needed.** A Dijkstra over all $n$ vertices pays $\Theta(\log n)$ per vertex in a comparison-based heap. Henzinger et al. avoid this by keeping each heap within a small piece of a recursive division, so that heap operations cost much less than $\log n$, and by charging the extra work of running pieces out of order to the boundary vertices, of which a division into pieces of size $r$ has only $O(n / \sqrt{r})$.

## Reductions

- **Maximum flow and minimum cut.** For an undirected planar graph, a minimum $s$-$t$ cut is a shortest cycle in the [dual graph](/planar-dual-graph/) that separates the faces next to $s$ and $t$; for $s$ and $t$ on the same face, the max flow comes from one shortest path computation in the dual (Hassin, 1981). So planar [max flow](/max-flow-problem/) in that case reduces to this problem.
- **Global minimum cut.** A minimum cut of a planar graph is a shortest cycle of its dual, which is a [shortest cycle problem](/shortest-cycle-problem/) on a planar graph.
- **Feasible flow and bipartite matching.** Feasible circulation with demands in a planar graph, and with it perfect matching in planar bipartite graphs, reduces to shortest paths with negative lengths in the dual (Miller and Naor).
- **From general to bounded degree.** Each vertex can be replaced by a cycle of zero-length edges, keeping planarity; several algorithms assume degree at most 3 this way.

## Applications

- **Road networks.** Road maps are nearly planar, and separator-based preprocessing is the basis of route planners such as customizable route planning.
- **Flows and cuts in planar graphs.** Shortest paths in the dual give planar max flow, min cut and image segmentation by graph cuts on grid graphs.
- **Approximation schemes.** Shortest path trees and their fundamental cycles give the separators and layers used by [Baker's technique](/baker-planar-ptas/) and other planar approximation schemes.
- **Distance oracles.** The dense distance graphs and r-divisions of the planar algorithms are reused by [distance oracles](/distance-oracle/) for planar graphs.

## References
