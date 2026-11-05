---
tag: F9V5EX
kind: problem
slug: shortest-cycle-problem
name: Shortest cycle problem
aliases:
- girth computation
area: graphs/paths-and-cycles
level: advanced
summary: Find the girth of a graph and a cycle achieving it.
prereqs: [girth, simple-cycle, breadth-first-search]
see_also: [itai-rodeh-girth-algorithm, dijkstra, floyd-warshall, negative-triangle, cycle-detection, minimum-mean-cycle-problem, hamiltonian-cycle-problem, longest-path-problem]
sources:
  - paper: doi:10.1137/0207033
    title: Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 413 to 423 (1978)
    locator: the O(nm) breadth-first search algorithm, the approximation that errs by at most one, triangle finding, and the matrix multiplication method
  - paper: Liam Roditty and Virginia Vassilevska Williams, Minimum weight cycles and triangles, equivalences and algorithms, FOCS 2011 (arXiv 1104.2882)
    title: Roditty and Vassilevska Williams, minimum weight cycles and triangles
    locator: the reductions from the minimum weight cycle problem, directed and undirected, to the minimum weight triangle problem
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2 (breadth-first search), Section 22.3 (Dijkstra's algorithm), Section 23.2 (the Floyd-Warshall algorithm)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1 (graph theory), Hamiltonian circuit, used for the hardness with negative weights
---

The shortest cycle problem asks for a cycle of least length in a graph: the fewest edges in an unweighted graph, which is the [girth](/girth/), or the least total weight in a weighted one. With nonnegative weights it is solvable in polynomial time, by one search from every vertex: $O(nm)$ for unweighted graphs with the [Itai-Rodeh algorithm](/itai-rodeh-girth-algorithm/) or its directed form, and $O(n(m + n \log n))$ with [Dijkstra's algorithm](/dijkstra/) for weights. For dense weighted graphs no algorithm is known that is much faster than $n^3$, and the problem is tied to the minimum weight triangle by fine-grained reductions. With negative weights allowed in cycles that must be simple, it contains the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) and is NP-hard.

## In plain words

You want the shortest round trip in a road network: start somewhere, drive along roads, and come back, without passing the same crossing twice on the way.

If every road has the same length, count the roads. Otherwise add up the lengths. If roads are one-way, the trip must follow them.

A simple way to solve it is to start from each crossing in turn, find the shortest ways out from it, and look for a road that brings you back. The shortest such return over all start points is the answer.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n$ vertices and $m$ edges, directed or undirected, and optionally a weight $w(e) \ge 0$ for each edge; without weights every edge has length 1. The graph may be a [multigraph](/multigraph/) with [self-loops](/self-loop/), and may have isolated vertices.

**Output.** A [simple cycle](/simple-cycle/) $C$ of least weight $w(C)$, and its weight, or the answer that $G$ has no cycle. In the unweighted case $w(C) = |C|$ is the girth.

**Cycles in multigraphs.** A self-loop is a cycle of length 1. In an undirected graph, two parallel edges between $u$ and $v$ form a cycle of length 2, but one edge used twice is not a cycle. In a directed graph, the arcs $u \to v$ and $v \to u$ form a cycle of length 2, and parallel arcs in the same direction form no cycle.

**Directed and undirected differ.** An undirected graph whose edges are all oriented has the same cycles only if the cycles follow the orientation. A directed graph with arcs $u \to v$ and $v \to u$ has a 2-cycle, while the undirected graph with one edge $\{u, v\}$ has none. So the two versions are separate problems, and each needs its own algorithm.

## Variants

- **Undirected, unweighted (girth).** [Itai-Rodeh](/itai-rodeh-girth-algorithm/): a breadth-first search from each vertex, and every non-tree edge $\{u, v\}$ gives the candidate $d(u) + d(v) + 1$. $O(nm)$ time.
- **Directed, unweighted.** The shortest cycle through $r$ has length $1 + \min d(r, u)$ over arcs $u \to r$. One breadth-first search per vertex, $O(nm)$ time.
- **Nonnegative weights.** The same two rules with Dijkstra's algorithm in place of breadth-first search: candidates $d(r, u) + w(e) + d(r, v)$ for non-tree edges $e = \{u, v\}$ if undirected, and $d(r, u) + w(u, r)$ if directed.
- **Directed, with negative weights but no negative cycle.** Reweight with potentials as in Johnson's all-pairs method. The weight of every cycle does not change under reweighting, so the shortest cycle is the same, and the nonnegative case applies.
- **Shortest cycle through a given vertex or edge.** One search instead of $n$: for an edge $e = \{u, v\}$, the answer is $w(e)$ plus the distance from $u$ to $v$ in $G - e$.
- **Triangle detection.** Deciding whether the girth is 3; see [triangle counting](/triangle-counting/).
- **Arbitrary weights, simple cycles.** NP-hard, see Bounds.

## Examples

**Girth and weight disagree.** An undirected graph with a triangle $0, 1, 2$ whose edges have weight 5 each, and a square $2, 3, 4, 5$ whose edges have weight 1 each, joined at vertex 2. The girth is 3, from the triangle, but the minimum weight cycle is the square, of weight 4 against 15.

**Multigraph.** Undirected edges $\{0, 1\}, \{1, 2\}, \{2, 0\}$ and a second edge $\{0, 1\}$. The two parallel edges form a cycle of length 2, so the girth is 2. Add a loop at 2 and the girth is 1.

**Directed.** Arcs $0 \to 1$, $1 \to 2$, $2 \to 0$ and $1 \to 0$. The directed cycles are $0, 1, 2$ and $0, 1$, so the directed girth is 2. With only the first three arcs, the directed girth is 3. Read as an undirected graph without the arc $1 \to 0$, the girth is also 3.

**Trees and forests.** A tree, or a forest with isolated vertices, has no cycle; the girth is $\infty$ by convention, and the answer is "no cycle".

**One root is not enough.** In the Itai-Rodeh example, a 5-cycle and a 4-cycle that share an edge, a search from a vertex of the 5-cycle that is not on the 4-cycle sees candidates 5 and 6 but not 4. The minimum must be taken over all roots, or at least over a root on a shortest cycle.

## Known algorithms

- **Search from every vertex.** $O(nm)$ unweighted, $O(n(m + n \log n))$ with nonnegative weights and Fibonacci heaps, both directed and undirected; see [Itai-Rodeh](/itai-rodeh-girth-algorithm/) and [Dijkstra](/dijkstra/).
- **Floyd-Warshall, directed.** Set $d(v, v) = \infty$ at the start instead of 0, so that $d(v, v)$ becomes the least weight of a cycle through $v$; the minimum over $v$ is the answer. $O(n^3)$ time; see [Floyd-Warshall](/floyd-warshall/). For undirected graphs this rule finds an edge used twice, so it is wrong there.
- **One edge removed at a time, undirected.** For each edge $e = \{u, v\}$, compute the distance from $u$ to $v$ in $G - e$. Simple but $m$ searches.
- **Approximation in $O(n^2)$, undirected unweighted.** Itai and Rodeh stop each search at its first non-tree edge, and return a cycle of length at most $g + 1$.
- **Matrix multiplication.** Itai and Rodeh find a triangle in $O(n^\omega)$ time and the girth of an undirected unweighted graph within the same bound.
- **Triangles in sparse graphs.** $O(m^{3/2})$ time by Itai and Rodeh, and by the degree-ordering method; see [triangle counting](/triangle-counting/).
- **Exact, arbitrary weights.** Enumerate simple cycles, for example with [Johnson's algorithm](/johnson-elementary-cycles-algorithm/), or use a subset dynamic program as for the Hamiltonian cycle.

## Bounds

- **Polynomial with nonnegative weights.** The algorithms above.
- **NP-hard with negative weights.** Give every edge weight $-1$. A simple cycle of weight $-n$ exists if and only if $G$ has a Hamiltonian cycle, which is NP-complete for directed and for undirected graphs (Garey and Johnson, Appendix A1). So the minimum weight simple cycle is NP-hard when negative weights may form negative cycles. If there is no negative cycle in a directed graph, the reweighting above makes it polynomial.
- **Fine-grained.** Roditty and Vassilevska Williams (2011) reduce the minimum weight cycle problem, in undirected graphs with weights in $\{1, \ldots, M\}$ and in directed graphs with weights in $\{-M, \ldots, M\}$ and no negative cycles, to the minimum weight triangle problem on $\Theta(n)$ vertices; the minimum weight triangle problem is in turn tied to [all-pairs shortest paths](/all-pairs-shortest-paths/), see [negative triangle](/negative-triangle/). So a truly subcubic algorithm for dense weighted graphs is not expected.
- **Lower bound.** $\Omega(n + m)$, since every edge may be on the only cycle.

## Reductions

- **To shortest paths.** For an edge $e = \{u, v\}$ in an undirected graph, the shortest cycle through $e$ has weight $w(e) + d_{G - e}(u, v)$. For an arc $u \to v$ in a directed graph, it is $w(u, v) + d(v, u)$. The answer is the minimum over all edges or arcs.
- **From Hamiltonian cycle.** With all weights $-1$, as in Bounds.
- **From triangle detection.** A graph with no loop and no parallel edges has girth 3 if and only if it has a triangle, so a girth algorithm decides triangle detection.
- **To cycle detection.** Whether the answer is finite is [cycle detection](/cycle-detection/), solvable in $O(n + m)$ time without the minimum.

## Applications

- **Codes on graphs.** Low-density parity-check codes are decoded on their Tanner graphs, and short cycles hurt the decoder, so code design asks for large girth.
- **Network design.** A shortest cycle through a link gives the shortest backup route for it.
- **Graph theory.** The girth bounds other parameters: a graph with girth $g$ and minimum degree $d$ has many vertices (the Moore bound), and graphs of large girth and large chromatic number exist by the probabilistic method.
- **Chemistry and biology.** Ring perception in molecules starts from smallest cycles.

## References
