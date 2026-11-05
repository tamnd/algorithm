---
tag: J78N2E
kind: problem
slug: rural-postman-problem
name: Rural postman problem
area: graphs/paths-and-cycles
level: advanced
summary: Find a shortest closed walk covering a required subset of edges; NP-hard in general.
prereqs: [walk, eulerian-circuit, minimum-weight-perfect-matching, np-hard]
see_also: [chinese-postman-problem, edmonds-johnson-algorithm, traveling-salesman-problem, christofides-algorithm, steiner-tree-problem, minimum-spanning-tree, all-pairs-shortest-paths, hamiltonian-cycle-problem]
sources:
  - paper: J. K. Lenstra and A. H. G. Rinnooy Kan, On general routing problems, Networks 6(3), 1976
    title: Lenstra and Rinnooy Kan, the NP-hardness of the rural postman problem
    locator: the reduction from the Hamiltonian cycle problem and the classification of routing problems
  - paper: C. S. Orloff, A fundamental problem in vehicle routing, Networks 4(1), 1974
    title: Orloff, the general routing problem and the rural postman problem
    locator: the definition of the general routing problem, with required vertices and edges
  - paper: Greg N. Frederickson, Approximation algorithms for some postman problems, Journal of the ACM 26(3), 538 to 554 (1979)
    title: Frederickson, approximation algorithms for postman problems
    locator: the heuristic for the rural postman problem by a spanning tree on the components and a matching, with worst-case ratio 3/2
  - paper: Jack Edmonds and Ellis L. Johnson, Matching, Euler tours and the Chinese postman, Mathematical Programming 5, 88 to 124 (1973)
    title: Edmonds and Johnson, the Chinese postman problem by matching
    locator: the reduction of the Chinese postman problem to a minimum weight perfect matching on the odd vertices
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A2 (network design), the problem Rural postman, NP-complete, with a reference to Lenstra and Rinnooy Kan
---

The rural postman problem asks for a shortest closed walk in a weighted graph that passes through every edge of a given required set at least once. The other edges may be used or not. If every edge is required, it is the [Chinese postman problem](/chinese-postman-problem/), which is solvable in polynomial time by matching. In general it is [NP-hard](/np-hard/) (Lenstra and Rinnooy Kan, 1976), because the walk must also decide how to travel between the separate groups of required edges, which contains the [traveling salesman problem](/traveling-salesman-problem/). When the required edges form one connected piece, the matching method works again, and when there are several pieces, Frederickson's heuristic finds a walk at most 3/2 times the optimum.

## In plain words

A postman in the country must walk along certain roads, the ones with houses on them, and return to the post office. Other roads have no houses, but he may use them as shortcuts. What is the shortest round trip?

If every road had houses, he would walk each road once and repeat as few roads as possible to come back; that is a solved problem. Here, some roads are only for getting from one group of houses to the next. Choosing which groups to visit in which order is like the traveling salesman's choice of the order of cities, and no fast method is known for that.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with a weight $w(e) \ge 0$ for each edge, and a set $R \subseteq E$ of *required* edges. The graph may be a [multigraph](/multigraph/): parallel edges are different edges, and each required one must be traversed. A required [self-loop](/self-loop/) at $v$ must be traversed once, at cost $w$, from $v$ back to $v$; a loop that is not required is never useful. Vertices that are on no edge of $R$ need not be visited; isolated vertices are never visited.

**Output.** A closed [walk](/walk/) $W$ in $G$ that traverses every edge of $R$ at least once, of least total weight $w(W)$, where an edge traversed $k$ times counts $k$ times. If $R$ is empty, the empty walk with weight 0 is optimal.

**Edge multiset form.** A closed walk corresponds to an Eulerian multigraph: the multiset of traversed edges has all degrees even and is connected. So the problem is to choose a multiset $A$ of extra copies of edges of $G$ such that $R \cup A$ is connected on the vertices it touches and has even degrees, with $w(A)$ least; then $w(R) + w(A)$ is the answer, and an [Eulerian circuit](/eulerian-circuit/) of $R \cup A$ is the walk. In an optimal walk no edge is traversed more than twice, since removing two copies of an edge keeps the degrees even and the multigraph connected.

**Directed and mixed versions.** In the directed rural postman problem, arcs must be traversed in their direction; in the mixed version, some links are undirected and some are arcs. Both contain the undirected version's difficulty and are also NP-hard.

## Variants

- **Chinese postman problem.** $R = E$. Polynomial by the reduction of Edmonds and Johnson (1973) to a [minimum weight perfect matching](/minimum-weight-perfect-matching/) on the odd vertices; see the [Chinese postman problem](/chinese-postman-problem/) and the [Edmonds-Johnson algorithm](/edmonds-johnson-algorithm/).
- **Connected required edges.** If the edges of $R$ form one connected subgraph, the problem is polynomial: add a minimum weight perfect matching of the odd-degree vertices of $(V, R)$ with shortest path distances in $G$.
- **General routing problem.** Some vertices are also required (Orloff, 1974). A required vertex is a required loop of weight 0, so this is the same problem.
- **Directed, mixed and windy versions.** The directed version with connected required arcs is solvable by minimum cost flow, as the directed Chinese postman; the mixed Chinese postman problem is already NP-hard (Papadimitriou, 1976).
- **Capacitated arc routing.** Several vehicles with a capacity each serve the required edges; a common model for refuse collection.
- **Open walk.** A walk that need not return to its start.

## Examples

**Several groups of required edges.** Vertices $0, \ldots, 5$ and the edges $\{0,1\}$ (weight 2), $\{1,2\}$ (3), $\{2,3\}$ (2), $\{3,0\}$ (4), $\{1,3\}$ (1), $\{3,4\}$ (5), $\{4,5\}$ (1), $\{2,5\}$ (2). The required edges are $\{0,1\}$, $\{2,3\}$ and $\{4,5\}$, of total weight 5, in three separate groups. An optimal walk is $0, 1, 3, 2, 5, 4, 5, 2, 1, 0$, of weight $2 + 1 + 2 + 2 + 1 + 1 + 2 + 3 + 2 = 16$; it traverses $\{4, 5\}$ twice and uses the shortcuts $\{1, 3\}$, $\{2, 5\}$ and $\{1, 2\}$. Requiring all eight edges, the Chinese postman tour, costs 23.

**Matching alone is wrong when $R$ is not connected.** In the same graph, require only $\{0,1\}$ and $\{2,3\}$. All four ends have odd degree in $R$, and the cheapest matching pairs 0 with 1 and 2 with 3, at cost $2 + 2$, which gives 8: each required edge walked back and forth, as two separate closed walks. The optimum is the walk $0, 1, 3, 2, 1, 0$ of weight 10, which needs the connecting edges.

**Connected required edges.** Require $\{0,1\}$ and $\{1,3\}$, which share vertex 1. The odd vertices of $R$ are 0 and 3, at distance 3 (through 1). The answer is $w(R) + 3 = 3 + 3 = 6$, the walk $0, 1, 3, 1, 0$.

**NP-hardness on a small scale.** Take any graph $H$ on $n \ge 3$ vertices with unit weights and attach a new pendant vertex $v'$ to every vertex $v$ by a required edge of weight 0. A closed walk must visit every vertex of $H$, and its weight is its number of edges in $H$; a walk of weight $n$ exists if and only if $H$ has a [Hamiltonian cycle](/hamiltonian-cycle-problem/).

The values above were computed by an exact search over the states (vertex, set of required edges already traversed) and checked against an enumeration of all closed walks.

## Known algorithms

- **Connected required edges: polynomial.** Compute all shortest path distances, take the odd-degree vertices $T$ of $(V, R)$, and add a minimum weight perfect matching of $T$; $O(n^3)$ time with standard matching algorithms.
- **Frederickson's heuristic: ratio 3/2.** Contract each component of $R$, connect the components by a [minimum spanning tree](/minimum-spanning-tree/) with shortest path distances between components, add a minimum weight perfect matching on the odd vertices, and take an Eulerian circuit. Frederickson (1979) proved a worst-case ratio of 3/2, by the same argument as [Christofides' algorithm](/christofides-algorithm/) for the traveling salesman problem.
- **Exact search over states.** A shortest path search over pairs (vertex, set of required edges traversed) gives an exact answer in $O(2^{|R|}(n + m)\log(2^{|R|} n))$ time; useful only for small $R$.
- **Integer programming.** Branch-and-cut methods on formulations with parity and connectivity constraints solve instances with hundreds of required edges in practice.
- **Local search and metaheuristics.** For large instances, as in street sweeping and snow plowing.

## Bounds

- **NP-hardness.** Lenstra and Rinnooy Kan (1976) proved that the rural postman problem is NP-hard, and it is listed as NP-complete in Garey and Johnson, Appendix A2. The pendant-edge construction above is a reduction from the Hamiltonian cycle problem.
- **Polynomial cases.** $R = E$ (Chinese postman), and $R$ connected, both by matching.
- **Approximation.** Ratio 3/2 by Frederickson's heuristic. The problem contains the metric traveling salesman problem, so it inherits its hardness of approximation.

## Reductions

- **From the Hamiltonian cycle problem.** The pendant-edge construction in the examples, with unit weights.
- **From the traveling salesman problem.** For a graph metric, make each city a required loop of weight 0 (or a pendant required edge of weight 0). A closed walk that visits all cities is a traveling salesman tour in the shortest path metric, with the same weight.
- **To the Chinese postman problem.** When $R$ is connected, on the graph $(V, R)$ with shortest path edges added between odd vertices.
- **To an Eulerian multigraph.** Every solution is an Eulerian circuit of $R$ plus extra edge copies, as in the definition, so any method that chooses the extra copies solves the problem.

## Applications

- **Mail delivery in rural areas.** The origin of the name: only roads with houses must be served.
- **Street sweeping and snow plowing.** Only some streets need service, and others are used to move between them.
- **Meter reading and inspection.** Inspecting power lines, pipelines or railway tracks where only some segments are due.
- **Routing in manufacturing.** Laser cutting and pen plotting: the cuts are required edges and the moves between them are free travel, so the shortest plan is a rural postman tour, often an open one.

## References
