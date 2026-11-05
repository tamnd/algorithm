---
tag: 28Z5VA
kind: definition
slug: neighborhood
name: Neighborhood
aliases:
- adjacency set
- neighbourhood
area: graphs/graph-representation
level: intro
summary: Set of vertices adjacent to a given vertex.
prereqs: [graph, vertex, edge]
see_also: [degree, neighborhood-enumeration, adjacency-query, in-degree-and-out-degree, graph-square, induced-subgraph, bfs-layers, regular-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs), neighbours and the neighbourhood N(v) and N(U); Section 1.2 (The degree of a vertex)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, neighbours and the neighbourhood N(v); Section 1.4, the out-neighbourhood and in-neighbourhood of a vertex in a digraph
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), adjacency; Section 20.1 (Representations of graphs), the list Adj[u] of the vertices adjacent to u
---

The neighborhood $N(v)$ of a [vertex](/vertex/) $v$ in a [graph](/graph/) is the set of vertices joined to $v$ by an [edge](/edge/). It is the most used set in graph algorithms: [breadth-first search](/breadth-first-search/), [depth-first search](/depth-first-search/) and almost every local rule read the graph one neighborhood at a time, and the [adjacency list](/adjacency-list/) is a stored copy of all the neighborhoods. Its size is the [degree](/degree/) in a simple graph. In a [directed graph](/directed-graph/) each vertex has an out-neighborhood and an in-neighborhood.

## Definition

**Undirected graphs.** Let $G = (V, E)$ be an undirected graph and $v \in V$. The (open) **neighborhood** of $v$ is

$$N(v) = N_G(v) = \{u \in V : \{u, v\} \in E\}.$$

Its elements are the *neighbours* of $v$, and $u \in N(v)$ if and only if $v \in N(u)$. The **closed neighborhood** is $N[v] = N(v) \cup \{v\}$. For a set $S \subseteq V$, $N(S) = \bigcup_{v \in S} N(v) \setminus S$ is the set of vertices outside $S$ with a neighbour in $S$; some authors leave out the "$\setminus S$" and must say so.

**Directed graphs.** For $G = (V, E)$ with $E \subseteq V \times V$,

$$N^+(v) = \{u : (v, u) \in E\}, \qquad N^-(v) = \{u : (u, v) \in E\}$$

are the *out-neighborhood* (the successors of $v$) and the *in-neighborhood* (the predecessors of $v$). Here $u \in N^+(v) \iff v \in N^-(u)$, but $N^+(v)$ and $N^-(v)$ can be different. Their sizes are the [out-degree and in-degree](/in-degree-and-out-degree/).

**Self-loops and multigraphs.** A [self-loop](/self-loop/) at $v$ puts $v$ into $N(v)$ under this definition. In a [multigraph](/multigraph/), $N(v)$ is a set, so a neighbour joined by three parallel edges appears once. That is why $|N(v)| = d(v)$ holds only in a [simple graph](/simple-graph/): in general, $|N(v)| \le d(v)$.

**Distance neighborhoods.** For an integer $r \ge 0$, the $r$-th neighborhood is $N_r(v) = \{u : \text{dist}(v, u) \le r\}$, the ball of radius $r$, so $N_1(v) = N[v]$. The sets $\{u : \text{dist}(v, u) = r\}$ are the [layers of breadth-first search](/bfs-layers/) from $v$. In the [square](/graph-square/) $G^2$, the neighborhood of $v$ is $N_2(v) \setminus \{v\}$.

**The neighbourhood graph.** $G[N(v)]$, the [induced subgraph](/induced-subgraph/) on the neighbours of $v$, is the *link* or *ego network* of $v$. The number of its edges is the number of triangles through $v$.

**Cost.** The cost of listing or testing a neighborhood depends on the representation, for $n$ vertices and $m$ edges:

| representation | list $N(v)$ | test $u \in N(v)$ | space |
|---|---|---|---|
| [adjacency list](/adjacency-list/) | $\Theta(1 + d(v))$ | $O(1 + d(v))$ | $\Theta(n + m)$ |
| adjacency list, sorted | $\Theta(1 + d(v))$ | $O(\log(2 + d(v)))$ | $\Theta(n + m)$ |
| [hash-based adjacency](/hash-based-adjacency/) | $\Theta(1 + d(v))$ | $O(1)$ expected | $\Theta(n + m)$ |
| [adjacency matrix](/adjacency-matrix/) | $\Theta(n)$ | $O(1)$ | $\Theta(n^2)$ |
| [edge list](/edge-list/) | $\Theta(m)$ | $\Theta(m)$ | $\Theta(m)$ |

Listing is the problem of [neighborhood enumeration](/neighborhood-enumeration/), and testing is the [adjacency query](/adjacency-query/). For a directed graph stored as out-lists, $N^-(v)$ is not stored; it costs $\Theta(n + m)$ to find, or $\Theta(1 + d^-(v))$ after building the lists of the [transpose graph](/transpose-graph/).

## Examples and non-examples

Let $G$ have $V = \{1, \ldots, 6\}$ and $E = \{12, 13, 23, 24, 45\}$, where $12$ means $\{1, 2\}$. The vertex 6 is isolated.

| $v$ | $N(v)$ | $N[v]$ | $\lvert N(v) \rvert$ |
|---|---|---|---|
| 1 | $\{2, 3\}$ | $\{1, 2, 3\}$ | 2 |
| 2 | $\{1, 3, 4\}$ | $\{1, 2, 3, 4\}$ | 3 |
| 3 | $\{1, 2\}$ | $\{1, 2, 3\}$ | 2 |
| 4 | $\{2, 5\}$ | $\{2, 4, 5\}$ | 2 |
| 5 | $\{4\}$ | $\{4, 5\}$ | 1 |
| 6 | $\emptyset$ | $\{6\}$ | 0 |

The sizes sum to $10 = 2 \cdot 5$. For $S = \{1, 2\}$, $N(S) = \{3, 4\}$. The ball $N_2(1) = \{1, 2, 3, 4\}$. The link $G[N(2)] = G[\{1, 3, 4\}]$ has the one edge $13$, so 2 lies on one triangle, $\{1, 2, 3\}$. The vertices 1 and 3 are *twins*: $N[1] = N[3]$.

**Directed.** In the graph with the edges $(1, 2), (2, 3), (3, 1), (1, 3)$, $N^+(1) = \{2, 3\}$ and $N^-(1) = \{3\}$, while $N^+(3) = \{1\}$ and $N^-(3) = \{1, 2\}$.

**Non-examples.**

- $N(v)$ is not the set of vertices reachable from $v$; it holds only those at distance 1. In the path $1\text{-}2\text{-}3$, the vertex 3 is reachable from 1 but $3 \notin N(1)$.
- $N(v)$ is not the set of edges at $v$; those are the incident edges, which an [incidence list](/incidence-list/) stores. In a multigraph they can be more numerous than the neighbours.

## Related definitions

- **Degree.** $d(v) = |N(v)|$ in a simple graph. See [degree](/degree/).
- **Adjacency.** $u$ and $v$ are adjacent when $u \in N(v)$. The query is the [adjacency query](/adjacency-query/).
- **Regular graph.** All neighborhoods have the same size. See [regular graph](/regular-graph/).
- **Dominating set.** A set $D$ with $N[D] = V$, that is, each vertex is in $D$ or has a neighbour in $D$.
- **Hall's condition.** In a bipartite graph with sides $X$ and $Y$, a matching that covers $X$ exists if and only if $|N(S)| \ge |S|$ for each $S \subseteq X$.

## References
