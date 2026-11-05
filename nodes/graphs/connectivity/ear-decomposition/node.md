---
tag: W71K6K
kind: concept
slug: ear-decomposition
name: Ear decomposition
aliases:
- Whitney ear decomposition
- open ear decomposition
area: graphs/connectivity
level: advanced
summary: A decomposition of a 2-edge-connected graph into an initial cycle plus open paths called ears.
prereqs: [biconnected-graph, two-edge-connected-graph, depth-first-search]
see_also: [strong-orientation, st-numbering, hopcroft-tarjan-biconnectivity, bridge-finding, menger-theorem, biconnected-components, k-edge-connected-graph, edge-classification]
sources:
  - paper: doi:10.1090/S0002-9947-1932-1501641-2
    title: Hassler Whitney, Non-separable and planar graphs, Transactions of the American Mathematical Society 34(2), 339 to 362 (1932)
    locator: the construction of every non-separable graph from a cycle by adding arcs (open ears)
  - paper: doi:10.2307/2303897
    title: Herbert E. Robbins, A theorem on graphs, with an application to a problem of traffic control, American Mathematical Monthly 46(5), 281 to 283 (1939)
    locator: the ear decomposition of a graph without bridges and the strong orientation built from it
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 3.1, 2-connected graphs and subgraphs (Proposition 3.1.1, a graph is 2-connected if and only if it can be built from a cycle by adding H-paths)
  - paper: doi:10.1016/j.ipl.2013.01.016
    title: Jens M. Schmidt, A simple test on 2-vertex- and 2-edge-connectivity, Information Processing Letters 113(7), 241 to 244 (2013)
    locator: the chain decomposition and the tests for 2-edge-connectivity and 2-vertex-connectivity
---

An ear decomposition of an [undirected graph](/undirected-graph/) splits its edges into a cycle $P_0$ and a sequence of *ears* $P_1, \ldots, P_k$, where each ear is a path or a cycle whose ends lie on the earlier pieces and whose inner vertices are new. A graph has an ear decomposition if and only if it is [2-edge-connected](/two-edge-connected-graph/) (Robbins, 1939), and an *open* one, where every ear is a path with two distinct ends, if and only if it is [biconnected](/biconnected-graph/) (Whitney, 1932). So the decomposition is a way to build exactly the graphs of these two classes, one piece at a time, and a proof that a graph is in the class. One [depth-first search](/depth-first-search/) finds an ear decomposition in $\Theta(n + m)$ time, and many algorithms for biconnected graphs, such as [st-numbering](/st-numbering/), start from one.

## In plain words

Start with one closed ring of roads. Now add a new road, maybe through some new towns, that starts and ends at towns you already have. This new piece is an ear. Keep adding ears until the whole network is built.

If you may let an ear start and end at the same town, you can build exactly the networks in which no single road is the only link between two parts. If each ear must end at a different town than it starts, you can build exactly the networks in which no single town is such a link.

The rule is useful because each step keeps the property. A road network that is built this way stays whole when any one road, or any one town, is closed.

## The idea

**Definitions.** Let $G = (V, E)$ be an undirected graph with no isolated vertex. Parallel edges are allowed. A loop is a cycle with one edge, and it can only be a closed ear. An *ear decomposition* of $G$ is a partition $E = P_0 \cup P_1 \cup \cdots \cup P_k$ where

1. $P_0$ is a cycle, and
2. for $i \ge 1$, $P_i$ is a path whose two ends lie in $V(P_0 \cup \cdots \cup P_{i-1})$ and whose inner vertices do not; or $P_i$ is a cycle with exactly one vertex in $V(P_0 \cup \cdots \cup P_{i-1})$.

An ear of the first kind with distinct ends is *open*; an ear of the second kind is *closed*. The decomposition is *open* if every $P_i$ with $i \ge 1$ is open. A single edge whose ends are old vertices is an open ear with no inner vertex.

**Counting.** An ear with $j$ inner vertices has $j + 1$ edges, so it raises $m - n$ by 1. A closed ear with $j$ new vertices has $j + 1$ edges too. The cycle $P_0$ has $m - n = 0$. So every ear decomposition of $G$ has exactly $k = m - n + 1$ ears after $P_0$, the cyclomatic number of $G$, whatever the choice of ears.

**Theorem (Whitney, 1932).** A graph with at least three vertices and no loop is biconnected if and only if it has an open ear decomposition. Loops do not change biconnectivity, so for a graph with loops, apply the theorem to the graph without them. The graph with two vertices and two parallel edges has an open ear decomposition, its 2-cycle, but it has fewer than three vertices.

*Why.* Adding an open ear $P$ with ends $a \neq b$ to a biconnected graph $H$ keeps it biconnected: removing a vertex of $H$ leaves $H$ connected, and the rest of $P$ stays attached through $a$ or $b$; removing an inner vertex of $P$ leaves the two parts of $P$ attached at $a$ and $b$. A cycle is biconnected, so every graph with an open ear decomposition is. Conversely, let $G$ be biconnected and let $H \subseteq G$ be a largest subgraph with an open ear decomposition; it exists, since $G$ has a cycle. If $H \neq G$, there is an edge $uv \notin H$ with $u \in V(H)$, since $G$ is connected. If $v \in V(H)$, the edge $uv$ is an open ear. If not, $G - u$ is connected, so it has a path from $v$ to $V(H) \setminus \{u\}$, and with $uv$ it gives an open ear. Both contradict the choice of $H$. This is Proposition 3.1.1 of Diestel.

**Theorem (Robbins, 1939).** A connected graph with at least one edge is 2-edge-connected if and only if it has an ear decomposition (closed ears allowed).

*Why.* An ear never becomes a [bridge](/bridge/): each of its edges lies on a cycle through the ear and a path between its ends in the old part. Conversely, if $G$ has no bridge, grow $H$ as before. An edge $uv$ leaving $H$ is not a bridge, so $G - uv$ has a path from $v$ back to $V(H)$; the first return gives a path or a cycle through $u$, which is an ear.

**Strong orientations.** Orient $P_0$ as a directed cycle and each ear as a directed path or cycle. Each step keeps the oriented graph strongly connected, since a new vertex can reach the end of its ear and be reached from the start. So a graph has a [strong orientation](/strong-orientation/) if and only if it has no bridge. This was the purpose of Robbins's paper.

**Finding one with depth-first search: chains.** Run a depth-first search of a connected graph. Every edge that is not a tree edge joins a vertex to one of its ancestors ([edge classification](/edge-classification/)). Mark all vertices unvisited. For each vertex $v$ in the order of discovery, and for each back edge from a descendant $w$ up to $v$, form a *chain*: mark $v$, take the back edge from $v$ to $w$, then follow tree edges upward from $w$ and mark each vertex, until a vertex that was already marked. The chains $C_1, C_2, \ldots$ in this order form Schmidt's *chain decomposition*. Schmidt (2013) proved:

- $G$ is 2-edge-connected if and only if the chains cover all edges; in general, the bridges are exactly the edges in no chain.
- A 2-edge-connected $G$ is biconnected if and only if $C_1$ is the only chain that is a cycle.
- When the chains cover $G$ and only $C_1$ is a cycle, $C_1, C_2, \ldots$ is an open ear decomposition.

Each edge is in at most one chain, and each vertex is marked once, so the whole method takes $\Theta(n + m)$ time. The [Hopcroft-Tarjan](/hopcroft-tarjan-biconnectivity/) low points give an ear decomposition in linear time too.

## Examples

**A biconnected graph.** The vertices are $0, \ldots, 4$, and the 7 edges are $\{0,1\}$, $\{1,2\}$, $\{2,3\}$, $\{3,0\}$, $\{1,3\}$, $\{0,4\}$, $\{4,2\}$. A depth-first search from 0, with the lists in the order of the edges, has the tree edges $\{0,1\}$, $\{1,2\}$, $\{2,3\}$, $\{2,4\}$ and the back edges $\{3,0\}$, $\{4,0\}$, $\{3,1\}$.

| chain | vertices | kind |
|---|---|---|
| $C_1$ | $0 \to 3 \to 2 \to 1 \to 0$ | the cycle $P_0$ |
| $C_2$ | $0 \to 4 \to 2$ | open ear, inner vertex 4 |
| $C_3$ | $1 \to 3$ | open ear, one edge |

The chains cover the $4 + 2 + 1 = 7$ edges, and only $C_1$ is a cycle, so the graph is biconnected, and $k = 2 = m - n + 1 = 7 - 5 + 1$ ears follow $P_0$.

**Two triangles sharing a vertex.** The edges are $\{0,1\}$, $\{1,2\}$, $\{2,0\}$, $\{0,3\}$, $\{3,4\}$, $\{4,0\}$. The chains are $0 \to 2 \to 1 \to 0$ and $0 \to 4 \to 3 \to 0$. They cover all edges, so the graph is 2-edge-connected, but the second chain is a cycle, a closed ear at 0. So the graph is not biconnected: 0 is an [articulation point](/articulation-point/).

**Parallel edges.** A triangle $0, 1, 2$ with a second copy of $\{0, 1\}$: the search uses one copy of $\{0, 1\}$ as a tree edge, and the other copy is a back edge. The chains are the 2-cycle $0 \to 1 \to 0$ and the open ear $0 \to 2 \to 1$. The graph is biconnected.

**A bridge.** In two triangles joined by one edge, no chain contains the joining edge, which is the bridge. The graph has no ear decomposition.

**Not unique.** The cycle $C_4$ with one chord has the decompositions "the 4-cycle, then the chord" and "one triangle, then the other two edges as one ear". Both have $m - n + 1 = 2$ pieces, $P_0$ and one ear.

## Where it is used

- **Testing and certificates.** A chain decomposition tests 2-edge-connectivity and biconnectivity in linear time, and the decomposition itself is a certificate that a checker can verify easily.
- **[st-numbering](/st-numbering/).** For a biconnected graph and an edge $st$, an order of the vertices from $s$ to $t$ in which every other vertex has a neighbour before it and one after it. It is built ear by ear, and it is a first step of planarity testing and of graph drawing.
- **[Strong orientation](/strong-orientation/).** Orient each ear in one direction, as above.
- **Higher connectivity.** Tests for 3-edge-connectivity and 3-vertex-connectivity, and the certifying algorithms for them, are built on chain or ear decompositions.
- **Matching theory.** A graph is factor-critical (removing any vertex leaves a perfect matching) if and only if it has an ear decomposition in which every ear has an odd number of edges (Lovász, 1972).
- **Parallel algorithms.** Ear decompositions can be found in parallel in polylogarithmic time, and they are a standard way to run connectivity algorithms on many processors, where depth-first search is hard to use.

## References
