---
tag: 0TJM1C
kind: problem
slug: articulation-point-finding
name: Articulation point finding
aliases:
- Cut vertex finding
area: graphs/connectivity
level: intro
summary: Find all vertices whose removal increases the number of connected components.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m)}
prereqs: [articulation-point, connected-components]
see_also: [hopcroft-tarjan-biconnectivity, bridge-finding, biconnected-components, block-cut-tree, low-link, depth-first-search, vertex-connectivity]
sources:
  - paper: doi:10.1137/0201010
    title: Robert E. Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146 to 160 (1972)
    locator: Section 4, the biconnectivity algorithm (low points and the test for articulation points)
  - paper: doi:10.1145/362248.362272
    title: John Hopcroft and Robert Tarjan, Algorithm 447, Efficient algorithms for graph manipulation, Communications of the ACM 16(6), 372 to 378 (1973)
    locator: the biconnected components algorithm and its analysis
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-2, Articulation points, bridges, and biconnected components (Problem 22-2 in the third edition)
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition, edited by Guy Even, Cambridge University Press (2012)
    locator: Chapter 3, Depth-first search (the section on nonseparable components)
---

Articulation point finding is the problem of listing every [articulation point](/articulation-point/) of an [undirected graph](/undirected-graph/): every vertex whose removal increases the number of [connected components](/connected-components/). The obvious method removes each vertex in turn and counts the components, in $\Theta(n(n + m))$ time. One [depth-first search](/depth-first-search/) with [low-link](/low-link/) values does it in $\Theta(n + m)$ time, which is optimal. The problem is the first step of the decomposition of a graph into [biconnected components](/biconnected-components/), and it finds the single points of failure of a network.

## In plain words

A network of towns and roads may have a town that is the only way between two parts of the network. If that town is closed, the network falls apart. The task is to find all such towns.

You could close each town in turn and check whether the rest still hangs together, but that repeats almost the same work once for every town. A better way walks the network once, deep first, and notes for each town how high back toward the start its part of the walk can climb by a short cut. A town is a weak point when some part below it has no short cut that climbs above it. One walk finds every weak point.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $V = \{0, 1, \ldots, n-1\}$ and $m = |E|$, in [adjacency lists](/adjacency-list/). Parallel edges and [self-loops](/self-loop/) are allowed. The graph need not be connected.

**Output.** The set

$$A(G) = \{\, v \in V : c(G - v) > c(G) \,\},$$

where $G - v$ is $G$ without $v$ and its edges, and $c(H)$ is the number of components of $H$. Loops and parallel edges do not change $A(G)$, because it depends only on which pairs of vertices are adjacent.

The set $A(G)$ is unique, so each correct algorithm gives the same answer, in any order.

## Variants

- **Decision.** Is $A(G)$ empty? For a connected graph with at least three vertices, this asks whether $G$ is [biconnected](/biconnected-graph/).
- **Count of pieces.** For each $v$, output $c(G - v)$. The same search gives it: in a [depth-first forest](/dfs-forest/), a root $v$ with $t$ children has $c(G - v) = c(G) - 1 + t$, and a vertex $v$ that is not a root has $c(G - v) = c(G) + k$, where $k$ is the number of children $s$ of $v$ with $\mathrm{low}[s] \ge d[v]$.
- **Blocks as well.** List the [biconnected components](/biconnected-components/) too, or build the [block-cut tree](/block-cut-tree/). The articulation points are exactly the vertices that lie in two or more blocks.
- **Edges instead of vertices.** [Bridge finding](/bridge-finding/) lists the edges whose removal disconnects the graph.
- **Sets of vertices.** The smallest set of vertices whose removal disconnects the graph is the [vertex connectivity](/vertex-connectivity/) problem. Articulation points are the case of size 1.
- **Dynamic graphs.** Keep the answer while edges are added and deleted. See [dynamic biconnectivity](/dynamic-biconnectivity/).
- **Directed graphs.** A *strong articulation point* is a vertex whose removal increases the number of [strongly connected components](/strongly-connected-components/). It is a different problem.

## Examples

The graph has $n = 7$ vertices and 10 edges: a triangle $0, 1, 2$ with a second copy of $\{0, 1\}$, the edge $\{2, 3\}$, a triangle $3, 4, 5$, the edge $\{5, 6\}$, and a loop at 6. A depth-first search from 0, with the lists in increasing order, visits $0, 1, 2, 3, 4, 5, 6$ in this order along one path, so $d[v] = v + 1$.

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d[v]$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
| $\mathrm{low}[v]$ | 1 | 1 | 1 | 4 | 4 | 4 | 7 |
| $c(G - v)$ | 1 | 1 | 2 | 2 | 1 | 2 | 1 |

The root 0 has one child, so it is not an articulation point. The vertex 2 has the child 3 with $\mathrm{low}[3] = 4 \ge d[2] = 3$, the vertex 3 has the child 4 with $\mathrm{low}[4] = 4 \ge d[3] = 4$, and the vertex 5 has the child 6 with $\mathrm{low}[6] = 7 \ge d[5] = 6$. So $A(G) = \{2, 3, 5\}$. The vertex 1 has the child 2 with $\mathrm{low}[2] = 1 < d[1] = 2$, because of the edge from 2 back to 0, so 1 is not an articulation point.

More small cases:

| graph | $A(G)$ |
|---|---|
| the path $0 - 1 - 2 - 3$ | $\{1, 2\}$ |
| a star with centre 0 and 4 leaves | $\{0\}$, with $c(G - 0) = 4$ |
| a cycle, or a [complete graph](/complete-graph/) | empty |
| two triangles sharing the vertex 0 | $\{0\}$ |
| a single edge, or a single vertex | empty |
| no edges at all | empty |

## Known algorithms

| algorithm | time | remark |
|---|---|---|
| Remove each vertex and count the components | $\Theta(n(n + m))$ | $n$ runs of a [component search](/connected-components/) |
| [Hopcroft-Tarjan biconnectivity](/hopcroft-tarjan-biconnectivity/) | $\Theta(n + m)$ | one depth-first search with [low-link](/low-link/) values; gives blocks and bridges too |
| [Gabow's path-based method](/gabow-path-based-scc/), biconnected version | $\Theta(n + m)$ | one search with stacks of the current path instead of low values |

The test of the Hopcroft-Tarjan algorithm is: a root of the depth-first forest is an articulation point if and only if it has at least two children, and a vertex $v$ that is not a root is one if and only if it has a child $s$ with $\mathrm{low}[s] \ge d[v]$. Here $\mathrm{low}[s]$ is the smallest discovery time that the subtree of $s$ reaches by at most one back edge. The proof is on the algorithm page.

## Bounds

**Upper bound.** $O(n + m)$ time in the [word RAM](/word-ram/) model with adjacency lists, by one depth-first search.

**Lower bound.** Each deterministic algorithm reads $\Omega(n + m)$ list entries in the worst case.

*Proof.* For the term $m$: let $A$ and $B$ be two disjoint copies of the [complete graph](/complete-graph/) $K_t$ with $t \ge 3$, and let a new vertex $x$ have one edge to a vertex of $A$ and one edge to a vertex of $B$. Then $x$ is an articulation point. Suppose the algorithm reads neither list entry of an edge $\{a_1, a_2\}$ of $A$ and neither entry of an edge $\{b_1, b_2\}$ of $B$. Rewrite these four unread entries so that the two edges become $\{a_1, b_2\}$ and $\{b_1, a_2\}$. In the new graph, $A$ and $B$ are joined without $x$, because $K_t$ minus one edge is still connected. So $x$ is no longer an articulation point, but the algorithm sees the same input and gives the same output. Hence it reads an entry of every edge of $A$ or of every edge of $B$, which is at least $t(t-1)/2$ entries, a constant fraction of $m$. For the term $n$: if three isolated vertices $x, y, z$ have unread lists, adding the edges $\{x, y\}$ and $\{y, z\}$ makes $y$ an articulation point without changing what the algorithm reads. So all but two of the isolated vertices are read. $\square$

**Space.** The depth-first search uses $\Theta(n)$ words for the times, the low values and the stack. The stack of the search can be $n$ deep, so programs use an explicit stack instead of recursion.

## Reductions

- **To biconnected components.** Given the blocks, the articulation points are the vertices that lie in at least two blocks. Counting takes $O(n + m)$ time.
- **To connectivity, $n$ times.** $v \in A(G)$ if and only if $G - v$ has more components than $G$. This is the brute-force method.
- **From the 2-connectivity test.** A graph with at least three vertices is [biconnected](/biconnected-graph/) if and only if it is connected and $A(G)$ is empty. So the test for [2-vertex-connectivity](/k-vertex-connected-graph/) costs $O(n + m)$, much less than a general [vertex connectivity](/vertex-connectivity/) computation.
- **Bridges from articulation points.** Subdivide each edge $\{u, v\}$ by a new vertex $w_e$. An edge $e$ that is not a loop is a [bridge](/bridge/) of $G$ if and only if $w_e$ is an articulation point of the new graph. The new graph has $n + m$ vertices and $2m$ edges.

## Applications

- Find the single points of failure of a computer, power or road network: a router, a substation or a crossing whose loss cuts some users off.
- Split a graph into blocks before an algorithm that works block by block, such as [planarity testing](/planarity-testing/), the count of [spanning trees](/counting-spanning-trees/), or the search for [Hamiltonian cycles](/hamiltonian-cycle/), which cannot cross an articulation point.
- Find people who are the only link between groups of a social network, a measure related to [structural holes](/structural-holes/).

## References
