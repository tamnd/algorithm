---
tag: QHN19M
kind: concept
slug: directed-and-undirected-graphs
name: Directed and undirected graphs
aliases:
- Undirected vs directed graphs
area: graphs/graph-representation
level: intro
summary: Describes graphs whose edges either have a direction, going from one vertex to another, or have none and connect vertices symmetrically.
prereqs: [graph, directed-graph]
see_also: [undirected-graph, directed-graph, edge, in-degree-and-out-degree, degree, strongly-connected-components, connected-components, adjacency-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), directed and undirected graphs and the conversions between them; Section 20.1 (Representations of graphs)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.1 (Undirected graphs) and Section 4.2 (Directed graphs)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 3, Section 3.1 (Basic definitions and applications) and Section 3.5 (Connectivity in directed graphs)
---

A graph is *directed* when each [edge](/edge/) is an ordered pair $(u, v)$ that goes from $u$ to $v$, and *undirected* when each edge is an unordered pair $\{u, v\}$ that joins $u$ and $v$ with no direction. The two kinds share most words and most data structures, but they differ in how degrees are counted, in what "connected" means, and in which algorithms apply. Each undirected graph can be seen as a directed graph with each edge in both directions, and this is how programs usually store it.

## In plain words

A friendship goes both ways: if Ann is a friend of Bob, then Bob is a friend of Ann. A graph of friendships has lines with no arrows. This is an undirected graph.

A follow on a social site goes one way: Ann can follow Bob while Bob does not follow Ann. A graph of follows has arrows. This is a directed graph.

The difference changes the questions you can ask. In a friendship graph you ask whether two people are in the same group. In a follow graph you ask whether you can get from one person to another along the arrows, and the answer can be yes one way and no the other way. A program often stores a friendship as two arrows, one in each direction.

## The idea

**The two definitions.** On a finite vertex set $V$ with $n = |V|$:

- An [undirected graph](/undirected-graph/) has $E \subseteq \{\{u, v\} : u, v \in V,\ u \ne v\}$. It is *simple*: there is no loop and no parallel edge, so $m = |E| \le \binom{n}{2}$.
- A [directed graph](/directed-graph/) has $E \subseteq V \times V$. Self-loops are allowed in the convention of CLRS, so $m \le n^2$.

Both can carry weights $w : E \to \mathbb{R}$, and both have a [multigraph](/multigraph/) form with parallel edges.

**From undirected to directed.** Map an undirected graph $G = (V, E)$ to the directed graph

$$\vec{G} = (V, \{(u, v), (v, u) : \{u, v\} \in E\}).$$

The relation of $\vec G$ is symmetric and has no loops, and it has exactly $2m$ edges. The map is a bijection from undirected simple graphs on $V$ to symmetric loopless directed graphs on $V$: the inverse keeps $\{u, v\}$ for each pair $(u, v)$, and two different edge sets give two different relations. An [adjacency list](/adjacency-list/) of $G$ is the adjacency list of $\vec G$, so it has $2m$ entries; an [adjacency matrix](/adjacency-matrix/) of $G$ is a symmetric matrix with a zero diagonal.

**From directed to undirected.** The *underlying undirected graph* of a directed graph $D$ keeps $\{u, v\}$ for each $(u, v) \in E$ with $u \ne v$. It forgets the direction, merges $(u, v)$ and $(v, u)$ into one edge and drops the loops. So it can have fewer edges than $D$. The opposite step, which picks one direction for each undirected edge, is an *orientation*.

**What changes.** The table compares the basic notions.

| notion | undirected | directed |
|---|---|---|
| edge | $\{u, v\}$, $u \ne v$ | $(u, v)$, tail $u$, head $v$ |
| most edges | $\binom{n}{2}$ | $n^2$ (with loops) |
| degree | [degree](/degree/) $d(v)$, $\sum_v d(v) = 2m$ | [out-degree and in-degree](/in-degree-and-out-degree/), $\sum_v d^+(v) = \sum_v d^-(v) = m$ |
| adjacency | symmetric: $u \sim v \iff v \sim u$ | not symmetric |
| connectivity | [connected components](/connected-components/), an equivalence relation | [strongly connected components](/strongly-connected-components/); reachability is not symmetric |
| shortest cycle | length 3 at least | length 1 (a loop) or 2 at least |
| no cycle at all | a forest, at most $n - 1$ edges | a [DAG](/directed-acyclic-graph/), up to $\binom{n}{2}$ edges |
| adjacency list entries | $2m$ | $m$ |

**Why a cycle has length at least 3.** In a simple undirected graph, the walk $u, v, u$ uses the edge $\{u, v\}$ twice. It is not a cycle, because a cycle may not repeat an edge. The directed walk $u, v, u$ uses two different edges $(u, v)$ and $(v, u)$, so it is a cycle of length 2. This is why [cycle detection](/cycle-detection-in-graph/) by [depth-first search](/depth-first-search/) must skip the edge back to the parent in an undirected graph, and must not skip it in a directed graph.

**Why a DAG can be dense and a forest cannot.** A forest on $n$ vertices with $c$ components has exactly $n - c$ edges. The directed graph on $\{1, \ldots, n\}$ with the edges $(i, j)$ for each $i < j$ has no directed cycle, because each edge goes to a larger number, and it has $\binom{n}{2}$ edges.

## Examples

**One graph, two readings.** Take $V = \{0, 1, 2, 3\}$ and the four pairs $01$, $12$, $23$, $30$.

- As an undirected graph, these are 4 edges that form a cycle of length 4. Each vertex has degree 2. The graph is connected, and each vertex reaches each other one.
- As the directed graph with the edges $(0, 1), (1, 2), (2, 3), (3, 0)$, it is a directed cycle, and it is strongly connected. Each vertex has $d^+ = d^- = 1$.
- As the directed graph with $(0, 1), (1, 2), (2, 3), (0, 3)$, it has no directed cycle. Its underlying undirected graph is still the 4-cycle. The vertex 3 reaches no vertex, and 0 is reached by none, so the strongly connected components are the four single vertices.

**Storage.** For the undirected 4-cycle, an adjacency list holds 8 entries: $0: 1, 3$; $1: 0, 2$; $2: 1, 3$; $3: 2, 0$. For the directed 4-cycle it holds 4 entries: $0: 1$; $1: 2$; $2: 3$; $3: 0$.

**A one-way street.** In a city map with one-way streets, the edge $(a, b)$ is a street that you may drive from $a$ to $b$. A two-way street is the pair of edges $(a, b)$ and $(b, a)$, often with the same weight. The shortest route from $a$ to $b$ can then be longer than the route from $b$ to $a$.

## Where it is used

- Undirected graphs: [connected components](/connected-components/), [minimum spanning trees](/minimum-spanning-tree/), [bipartite graphs](/bipartite-graph/), [graph coloring](/graph-coloring/), [maximum matching](/maximum-matching/) and the [handshake lemma](/handshake-lemma/).
- Directed graphs: [reachability](/reachability/), [strongly connected components](/strongly-connected-components/), [topological sort](/topological-sort/) of a [directed acyclic graph](/directed-acyclic-graph/), [shortest paths](/shortest-path/) with one-way edges, flow networks and [PageRank](/pagerank/).
- Algorithms that work on both: [breadth-first search](/breadth-first-search/) and [depth-first search](/depth-first-search/), with the changes above. A shortest-path algorithm for directed graphs runs on an undirected graph after the map $G \mapsto \vec G$, when the weights are not negative. With a negative weight, the undirected edge becomes a negative cycle of length 2.

## References
