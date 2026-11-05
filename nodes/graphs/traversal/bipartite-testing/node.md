---
tag: QG8NFP
kind: problem
slug: bipartite-testing
name: Two-coloring graphs (bipartite testing)
aliases:
- Two-coloring graphs
area: graphs/traversal
level: intro
summary: Decides whether a graph's vertices can be colored with two colors so no edge joins same colored vertices, using a graph traversal.
prereqs: [bipartite-graph, graph-coloring]
see_also: [bipartiteness-check, bipartite-graph-recognition, bipartite-graph-test, k-coloring, greedy-coloring, dsu-with-parity, bipartite-odd-cycle-theorem, connected-components]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 3.4, Testing bipartiteness (coloring the BFS layers red and blue)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Appendix A1.1, problem GT4, Graph K-colorability (polynomial for K = 2, NP-complete for K = 3), and Appendix A3.1, problem SP4, Set splitting (hypergraph 2-colorability)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1, Undirected graphs (two-colorability with depth-first search)
---

Two-colouring asks for a colouring of the vertices of a [graph](/graph/) with two colours such that the two ends of each edge get different colours, or a proof that none exists. A graph has such a colouring exactly when it is [bipartite](/bipartite-graph/). This is the case $k = 2$ of the [$k$-colouring problem](/k-coloring/), and it is the one easy case: it takes linear time by a graph traversal, while 3-colouring is NP-complete. The reason is that two colours leave no choice. Once one vertex of a [connected component](/connected-components/) has a colour, every other vertex of the component has a forced colour, the parity of its distance. This page is about the colouring: finding it, counting the colourings, extending a partial colouring, and the limits of the method. The decision by search is on [bipartiteness checking](/bipartiteness-check/).

## In plain words

You want to paint every dot in a drawing black or white, so that every line joins a black dot and a white dot.

Paint one dot black. Every dot joined to it must be white. Every dot joined to those must be black. Nothing is up to you. Keep going until all the dots of this part of the drawing are painted, and then check every line.

If a line joins two dots of one colour, no painting works, not even a different one, because every step was forced. If all lines are fine, you are done. A part of the drawing that is not joined to the rest can start with either colour, so each such part doubles the number of paintings.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges.

**Output.** A *proper 2-colouring* $c : V \to \{0, 1\}$, with $c(u) \ne c(v)$ for every edge $\{u, v\}$, or the report that none exists.

In other words, $c$ solves the system of equations $c(u) + c(v) = 1$ over the two-element field, one equation for each edge. The *chromatic number* $\chi(G)$ is at most 2 exactly when a proper 2-colouring exists, and $\chi(G) = 1$ exactly when $G$ has no edges.

**Forcing.** Let $C$ be a connected component and $s \in C$. In each proper 2-colouring, $c(v) = c(s)$ if $\delta(s, v)$ is even and $c(v) \ne c(s)$ if it is odd, because the colours alternate along a shortest path from $s$ to $v$. So a component has either no proper 2-colouring or exactly two, and the two differ by swapping the colours.

## Variants

- **Counting.** If $G$ is bipartite with $k$ connected components, it has exactly $2^k$ proper 2-colourings, by forcing. Otherwise it has none. More generally, the number of proper $q$-colourings is the chromatic polynomial evaluated at $q$, which is #P-hard to compute for $q \ge 3$.
- **Extension of a partial colouring.** Some vertices have fixed colours. A colouring that extends them exists exactly when the graph is bipartite and, in each component, the fixed vertices agree with the forced parities: two fixed vertices at even distance have the same fixed colour, and two at odd distance have different ones. One search per component checks this.
- **Parity constraints.** Each edge says either "same colour" or "different colours". This is the system $c(u) + c(v) = b_{uv}$ over the two-element field, and the same search solves it, with the colour of $v$ set to $c(u) + b_{uv}$. A [disjoint-set structure with parity](/dsu-with-parity/) solves it online.
- **Three or more colours.** Deciding whether $\chi(G) \le 3$ is NP-complete, so no forcing argument works for $k \ge 3$: with three colours, a neighbour of a coloured vertex still has two choices.
- **Hypergraphs.** Colour the vertices with two colours so that no hyperedge is all one colour. This is *set splitting*, and it is NP-complete already when every hyperedge has three vertices. With hyperedges of two vertices it is the graph problem.

## Examples

**Forcing in action.** Take the vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$. Starting with $c(0) = 0$, the colours are forced in BFS order:

| vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| forced from | start | 0 | 0 | 1 | 2 | 3 | 5 | new start |
| $c$ | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 |

All 8 edges join two colours. The graph has two components, $\{0, \ldots, 6\}$ and $\{7\}$, so it has exactly $2^2 = 4$ proper 2-colourings.

**A partial colouring that does not extend.** Fix $c(0) = 0$ and $c(6) = 1$ in the same graph. The distance from 0 to 6 is 4, which is even, so the forced colour of 6 is 0, and no proper colouring extends the fixed colours.

**Odd cycles.** On a cycle of length 5, forcing from one vertex around the cycle gives colours $0, 1, 0, 1, 0$, and the last edge joins two vertices of colour 0. Every odd cycle fails in this way, which is one direction of the [odd cycle theorem](/bipartite-odd-cycle-theorem/).

## Known algorithms

| method | time | notes |
|---|---|---|
| BFS or DFS forcing, then a check of all edges | $\Theta(n + m)$ | colour each new vertex opposite to its parent; see [bipartiteness checking](/bipartiteness-check/) and [bipartiteness testing](/bipartiteness-testing/) |
| [greedy colouring](/greedy-coloring/) in BFS order | $\Theta(n + m)$ | on a connected bipartite graph it uses 2 colours, because each vertex's earlier neighbours are in the previous layer |
| [union-find with parity](/dsu-with-parity/) | $O(n + m\,\alpha(n))$ | edges in any order, online; also parity constraints |
| Gaussian elimination over the two-element field | $O(n^2 m)$ | treats the problem as a linear system; much slower, but it shows that the problem is linear algebra |

The forcing algorithm is optimal: it reads each edge at most twice, and every correct algorithm must read every edge on some inputs (see the bounds on [bipartiteness checking](/bipartiteness-check/)).

Greedy colouring in an arbitrary order can need many colours even on bipartite graphs. On the "crown" graph, $K_{t,t}$ minus a perfect matching, the order $a_1, b_1, a_2, b_2, \ldots$ makes greedy use $t$ colours.

## Bounds

- **Time.** $\Theta(n + m)$ is necessary and enough.
- **Number of colourings.** Exactly $0$ or $2^k$, where $k$ is the number of components.
- **The gap to three colours.** $k$-colouring is in linear time for $k \le 2$ and NP-complete for each fixed $k \ge 3$. The reason for the gap is the forcing property, which holds only with two colours.

## Reductions

- **To 2-SAT.** One variable $x_v$ per vertex and two clauses $(x_u \lor x_v)$ and $(\lnot x_u \lor \lnot x_v)$ per edge. A satisfying assignment is a proper 2-colouring.
- **To linear equations.** The system $x_u + x_v = 1$ over the two-element field, one equation per edge.
- **To connectivity.** Through the [bipartite double cover](/bipartite-double-cover/): $G$ is 2-colourable exactly when no vertex $v$ has $(v, 0)$ and $(v, 1)$ in one component of the cover.
- **From interval splitting.** Can a set of intervals be split into two groups with no overlap inside a group? Build the graph with an edge between every two overlapping intervals and 2-colour it. (A sweep over the endpoints answers this faster, but the colouring view is the general one.)

## Applications

- **Two resources under conflicts.** Assign each task one of two machines, rooms or time slots, when some pairs of tasks conflict.
- **Bipartite algorithms.** Algorithms for [bipartite matching](/bipartite-matching/) and for vertex covers on bipartite graphs take the two sides as input. Two-colouring produces them.
- **Parity arguments.** The chessboard colouring of a grid is the 2-colouring of the grid graph, and it proves that some tilings and some paths cannot exist.
- **Sub-step of harder colourings.** Algorithms for 3-colouring often fix the colour of some vertices and then solve the rest as a 2-colouring or a 2-SAT problem.

## References
