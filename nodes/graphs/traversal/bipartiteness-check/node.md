---
tag: XC2A7V
kind: problem
slug: bipartiteness-check
name: Bipartiteness checking
aliases:
- Checking a graph for bipartiteness
area: graphs/traversal
level: intro
summary: Problem of deciding whether a graph can be two-colored so no edge joins same-colored vertices, solved with a breadth-first or depth-first search.
prereqs: [bipartite-graph, breadth-first-search]
see_also: [bipartite-testing, bipartite-graph-recognition, bipartiteness-testing, bipartite-odd-cycle-theorem, bfs-layers, dsu-with-parity, dynamic-bipartiteness, bipartite-double-cover]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness, an application of breadth-first search (the BFS coloring, and the proof that an edge inside a layer gives an odd cycle)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (the two-colorability question solved with depth-first search)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5, Basic graph algorithms (the exercises on bipartite graphs and odd cycles)
---

Bipartiteness checking asks whether the vertices of an undirected [graph](/graph/) can be split into two sets so that every edge has one end in each set, that is, whether the graph is [bipartite](/bipartite-graph/). A graph is bipartite exactly when it has no cycle of odd length, by the [odd cycle theorem](/bipartite-odd-cycle-theorem/). One [breadth-first search](/breadth-first-search/) or [depth-first search](/depth-first-search/) decides it in $\Theta(n + m)$ time: give each new vertex the colour opposite to its parent's, and look for an edge whose two ends got the same colour. This page treats the search-based check. The pages on [two-colouring](/bipartite-testing/) and on [recognition with certificates](/bipartite-graph-recognition/) treat the colouring and the certificates in more depth.

## In plain words

You want to put every person at one of two tables, so that no two people who dislike each other sit at the same table.

Start with anyone at table A. Everyone who dislikes them must go to table B. Everyone who dislikes one of those must go to table A, and so on. There is never a choice: once the first person is placed, the whole group is forced.

So just do it. If you ever find two people who dislike each other at the same table, no seating works. If you never do, you have a seating. A group that is not connected to the first one gets a new start.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, in [adjacency lists](/adjacency-list/).

**Output.** YES if there is a map $c : V \to \{0, 1\}$ with $c(u) \ne c(v)$ for each edge $\{u, v\}$, and NO otherwise.

Such a map is a proper 2-colouring, and the sets $c^{-1}(0)$ and $c^{-1}(1)$ are the two sides. A self-loop $\{u, u\}$ makes the answer NO. Parallel edges do not change the answer. A graph is bipartite exactly when each of its [connected components](/connected-components/) is, so the check runs on each component.

## Variants

- **With a witness.** Return the colouring for YES and an odd cycle for NO. See [bipartite graph recognition](/bipartite-graph-recognition/).
- **Two-colouring.** Find the colouring itself, count all colourings, or fix the colours of some vertices in advance. See [two-colouring](/bipartite-testing/).
- **Edges arrive one at a time.** Report the first edge that makes the graph non-bipartite. A [disjoint-set structure with parity](/dsu-with-parity/) does this in near-linear total time.
- **Fully dynamic.** Edges are inserted and deleted between queries. See [dynamic bipartiteness](/dynamic-bipartiteness/).
- **Close to bipartite.** Delete at most $k$ vertices to make the graph bipartite: the NP-hard [odd cycle transversal](/odd-cycle-transversal/) problem. The check is the case $k = 0$.

## Examples

| graph | bipartite | reason |
|---|---|---|
| a tree, a forest | yes | no cycles at all; colour by the parity of the depth |
| the cycle $C_n$ | exactly when $n$ is even | the cycle itself is the only cycle |
| a grid of pixels | yes | colour $(i, j)$ by the parity of $i + j$, like a chessboard |
| the cube graph $Q_d$ | yes | colour a bit string by the parity of its number of ones |
| the complete graph $K_n$, $n \ge 3$ | no | it contains a triangle |
| the Petersen graph | no | its outer ring is a 5-cycle |

**A worked case.** Take the vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$. BFS from 0 gives the [layers](/bfs-layers/) $\{0\}$, $\{1, 2\}$, $\{3, 4\}$, $\{5\}$, $\{6\}$, and the colours are the parities of the layers: 0 on $\{0, 3, 4, 6\}$ and 1 on $\{1, 2, 5\}$. Every edge joins two colours, so the answer is YES. Vertex 7 is a component of its own and gets colour 0. If the edge $\{1, 2\}$ is added, the scan of 1 finds 2 with the same colour 1, and the answer is NO: $0, 1, 2$ is a triangle.

## Known algorithms

**BFS check.** Run BFS from an uncoloured vertex $s$ with $c(s) = 0$. When the scan of $u$ finds an uncoloured neighbour $v$, set $c(v) = 1 - c(u)$ and enqueue $v$. When it finds a coloured neighbour $v$ with $c(v) = c(u)$, answer NO. Repeat from every uncoloured vertex, and answer YES if no conflict appears.

*Why it is correct.* Within a component, $c(v)$ is the parity of the BFS distance $\delta(s, v)$. If the run ends without a conflict, every edge was checked from at least one end at a time when both ends had colours, so $c$ is a proper colouring. If the check finds an edge $\{u, v\}$ with $c(u) = c(v)$, then $\delta(s, u)$ and $\delta(s, v)$ have the same parity, and since they differ by at most one, they are equal: the edge lies inside one layer $L_i$. Let $z \in L_j$ be the lowest common ancestor of $u$ and $v$ in the [BFS tree](/bfs-tree/). The tree paths from $z$ to $u$ and to $v$ have $i - j$ edges each and meet only at $z$, so with the edge $\{u, v\}$ they form a cycle of length $2(i - j) + 1$, which is odd. No odd cycle can be properly 2-coloured, because the colours must alternate around it. So the answer NO is correct.

**DFS check.** Colour each vertex by the parity of its depth in the [DFS forest](/dfs-forest/). In an undirected DFS every non-tree edge is a back edge from a vertex to an ancestor (see [edge classification](/edge-classification/)). A back edge $\{u, v\}$ with $v$ an ancestor of $u$ and both depths of the same parity closes the cycle of the tree path from $v$ to $u$, of even length, plus the edge, which is odd. If no back edge has this form, the colouring is proper.

| method | time | extra space | output |
|---|---|---|---|
| BFS check | $\Theta(n + m)$ | $\Theta(n)$ | colouring or an odd cycle through the BFS tree |
| DFS check | $\Theta(n + m)$ | $\Theta(n)$ | colouring or an odd cycle of the tree path and one back edge |
| [union-find with parity](/dsu-with-parity/) | $O(n + m\,\alpha(n))$ | $\Theta(n)$ | online, edge by edge |
| with an [adjacency matrix](/adjacency-matrix/) | $\Theta(n^2)$ | $\Theta(n)$ | the same, each row is read in full |

The [bipartiteness testing](/bipartiteness-testing/) page gives the BFS check as an algorithm with pseudocode and code.

## Bounds

**Linear time is optimal.** Every correct algorithm must read all of a worst-case input. Take a connected bipartite graph in which every edge lies on a cycle and each side has at least two vertices, for example an even cycle or the complete bipartite graph $K_{a,b}$ with $a, b \ge 2$, which has $m = ab$ edges. Assume that an algorithm answers YES without reading the edge $e = \{x, y\}$. Replace $e$ by an edge $\{x, z\}$, where $z \ne x$ is on the same side as $x$; this is a new edge, because no two vertices of one side are adjacent. The graph $G - e$ is still connected, because $e$ lies on a cycle, and its 2-colouring is forced, so $x$ and $z$ still have the same colour, and the new graph has an odd cycle. The algorithm sees the same input values as before and answers YES again, which is wrong. So it must read all $m$ edges, and it must also look at all $n$ vertices, which gives $\Omega(n + m)$.

**Space.** The check needs $\Theta(n)$ bits in the plain search. On a read-only input, bipartiteness is in deterministic logspace: it reduces to undirected connectivity, as in the [reductions](#reductions) below, and undirected connectivity is in logspace by Reingold's theorem.

## Reductions

- **To connectivity.** In the [bipartite double cover](/bipartite-double-cover/) of $G$, with the vertices $(v, 0)$ and $(v, 1)$ and an edge between $(u, i)$ and $(v, 1 - i)$ for each edge $\{u, v\}$, the vertices $(v, 0)$ and $(v, 1)$ are connected exactly when $v$ lies on a closed walk of odd length. So $G$ is bipartite exactly when no $v$ has both copies in one component.
- **To 2-SAT.** Take one Boolean variable $x_v$ per vertex and, for each edge, the two clauses $(x_u \lor x_v)$ and $(\lnot x_u \lor \lnot x_v)$, which say $x_u \ne x_v$. The formula is satisfiable exactly when $G$ is bipartite.
- **From the odd cycle theorem.** The check is the algorithmic form of the [bipartite odd cycle theorem](/bipartite-odd-cycle-theorem/): the BFS proof above shows both directions of the theorem.
- **Directed graphs.** For a directed graph, bipartiteness is the property of its underlying undirected graph. Edge directions do not matter.

## Applications

- **Matching.** Bipartite [matching](/bipartite-matching/) algorithms such as Hopcroft-Karp need the two sides. The check finds them.
- **Two-way splits under conflicts.** Seating rivals at two tables, putting conflicting jobs on two machines, splitting a set of intervals into two groups without overlaps inside a group: each is a check on a conflict graph.
- **Grids and images.** The chessboard colouring of a grid is a bipartition, which parity arguments use, for example to show that a board with two opposite corners removed cannot be tiled by dominoes.
- **Special structure.** Many algorithms first check whether the input is bipartite, because bipartite graphs have special structure: [maximum independent sets](/bipartite-maximum-independent-set/) and minimum vertex covers are polynomial on them, by König's theorem.

## References
