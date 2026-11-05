---
tag: 5TZN3A
kind: definition
slug: in-degree-and-out-degree
name: In-degree and out-degree
aliases:
- indegree
- outdegree
area: graphs/graph-representation
level: intro
summary: Numbers of edges entering and leaving a vertex in a directed graph.
prereqs: [directed-graph, degree]
see_also: [degree, handshake-lemma, kahns-algorithm, topological-sort, universal-sink, eulerian-circuit, transpose-graph, functional-graph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), out-degree and in-degree; Section 20.1 (Representations of graphs), Exercise 20.1-1 on computing the out-degrees and in-degrees from adjacency lists
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.10 (Other notions of graphs), directed graphs
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.4 (Directed graphs), out-degree, in-degree and the degree-sum formula for digraphs
---

The out-degree $d^+(v)$ of a vertex $v$ of a [directed graph](/directed-graph/) is the number of edges that leave $v$, and the in-degree $d^-(v)$ is the number of edges that enter $v$. They split the [degree](/degree/) of an undirected graph into two numbers, one for each direction. In each directed graph the out-degrees and the in-degrees both sum to the number of edges. Vertices of in-degree 0 (sources) and of out-degree 0 (sinks) drive [topological sorting](/topological-sort/), and equal in-degree and out-degree at each vertex is the condition for a directed [Eulerian circuit](/eulerian-circuit/).

## Definition

Let $G = (V, E)$ be a directed graph, with $E \subseteq V \times V$, as in CLRS. For $v \in V$,

$$d^+(v) = |\{u \in V : (v, u) \in E\}|, \qquad d^-(v) = |\{u \in V : (u, v) \in E\}|.$$

Other notations are $\deg^+(v)$, $\text{outdeg}(v)$ and $\deg^-(v)$, $\text{indeg}(v)$. The sets in the two formulas are the out-neighbourhood $N^+(v)$ and the in-neighbourhood $N^-(v)$ of $v$ (see [neighborhood](/neighborhood/)), so $d^+(v) = |N^+(v)|$ and $d^-(v) = |N^-(v)|$.

**Self-loops.** A [self-loop](/self-loop/) $(v, v)$ leaves $v$ and enters $v$, so it adds 1 to $d^+(v)$ and 1 to $d^-(v)$.

**Multigraphs.** In a directed [multigraph](/multigraph/), where each edge $e$ has a tail $t(e)$ and a head $h(e)$ and two edges may have the same ends, the definitions count edges, not neighbours: $d^+(v) = |\{e : t(e) = v\}|$ and $d^-(v) = |\{e : h(e) = v\}|$. Then $d^+(v)$ can be larger than $|N^+(v)|$.

**Degree sum.** For each directed graph or directed multigraph with $m$ edges,

$$\sum_{v \in V} d^+(v) = \sum_{v \in V} d^-(v) = m.$$

*Proof.* Each edge has exactly one tail, so it is counted exactly once in the first sum, at its tail. In the same way, it is counted exactly once in the second sum, at its head. $\square$ This is the directed form of the [handshake lemma](/handshake-lemma/). The total degree $d^+(v) + d^-(v)$, which some authors call the degree of $v$, sums to $2m$.

**Words.** A vertex is a *source* if $d^-(v) = 0$ and a *sink* if $d^+(v) = 0$. Some authors also ask that a source have $d^+(v) > 0$. A vertex is *balanced* if $d^+(v) = d^-(v)$, and $G$ is balanced if each vertex is. The minimum and maximum out-degree are $\delta^+(G)$ and $\Delta^+(G)$, and in the same way $\delta^-(G)$ and $\Delta^-(G)$. In the [transpose graph](/transpose-graph/) $G^T$, the two numbers swap: $d^+_{G^T}(v) = d^-_G(v)$.

**Computing them.** The cost depends on the representation, for $n$ vertices and $m$ edges:

| representation | $d^+(v)$ | $d^-(v)$ | all $d^-$ at once |
|---|---|---|---|
| [adjacency list](/adjacency-list/) with list lengths | $O(1)$ | $\Theta(n + m)$, a scan of all lists | $\Theta(n + m)$ |
| [adjacency matrix](/adjacency-matrix/) | $\Theta(n)$, a row sum | $\Theta(n)$, a column sum | $\Theta(n^2)$ |
| [edge list](/edge-list/) | $\Theta(m)$ | $\Theta(m)$ | $\Theta(n + m)$ |
| [incidence list](/incidence-list/) with in-lists | $O(1)$ | $O(1)$ | $\Theta(n)$ |

To get all in-degrees from adjacency lists, set $c[v] = 0$ for each $v$, then for each $u$ and each $v$ in the list of $u$, add 1 to $c[v]$. Each list entry is read once, so the time is $\Theta(n + m)$. This is the first step of [Kahn's algorithm](/kahns-algorithm/).

## Examples and non-examples

**A worked example.** Let $V = \{0, 1, 2, 3, 4, 5\}$ and $E = \{(0,1), (0,2), (1,2), (2,0), (2,3), (3,3), (4,3)\}$.

| vertex | $N^+$ | $N^-$ | $d^+$ | $d^-$ |
|---|---|---|---|---|
| 0 | $\{1, 2\}$ | $\{2\}$ | 2 | 1 |
| 1 | $\{2\}$ | $\{0\}$ | 1 | 1 |
| 2 | $\{0, 3\}$ | $\{0, 1\}$ | 2 | 2 |
| 3 | $\{3\}$ | $\{2, 3, 4\}$ | 1 | 3 |
| 4 | $\{3\}$ | $\emptyset$ | 1 | 0 |
| 5 | $\emptyset$ | $\emptyset$ | 0 | 0 |

Both columns sum to $7 = |E|$. The vertex 4 is a source. The vertex 3 is not a sink, because its self-loop leaves it: it has $d^+(3) = 1$. The vertex 5 is isolated, so it is both a source and a sink. The vertices 1 and 2 are balanced.

**Special graphs.**

- In a [functional graph](/functional-graph/), which has one edge $(v, f(v))$ for each $v$, each vertex has $d^+(v) = 1$, and $d^-(v)$ is the number of preimages of $v$.
- In a tournament, which has exactly one of $(u, v)$ and $(v, u)$ for each pair $u \ne v$, $d^+(v) + d^-(v) = n - 1$ for each $v$. The out-degrees are the scores of the players.
- In a [directed acyclic graph](/directed-acyclic-graph/) with at least one vertex, there is at least one source and at least one sink: follow edges forward from any vertex; with no cycle, no vertex repeats, so the walk ends at a sink after at most $n - 1$ steps. Reverse the edges for a source.
- A directed graph in which each vertex has $d^+(v) \ge 1$ has a directed cycle, by the same walk argument.

**Non-examples.**

- In an [undirected graph](/undirected-graph/) the edges have no direction, so there is no in-degree or out-degree, only the [degree](/degree/). Treating each undirected edge as the two arcs $(u, v)$ and $(v, u)$ gives $d^+(v) = d^-(v) = d(v)$.
- The number of vertices reachable from $v$ is not $d^+(v)$: $d^+(v)$ counts only the edges out of $v$, not longer paths.

## Related definitions

- **Directed Euler circuits.** A directed multigraph whose edges all lie in one weakly connected component has a directed Eulerian circuit if and only if each vertex is balanced. See [Eulerian circuit](/eulerian-circuit/).
- **Universal sink.** A vertex with $d^-(v) = n - 1$ and $d^+(v) = 0$ in a graph with no self-loops. The [universal sink](/universal-sink/) problem finds it in $O(n)$ time from an adjacency matrix.
- **Kahn's algorithm.** [Kahn's algorithm](/kahns-algorithm/) for topological order removes sources one by one and updates the in-degrees.
- **Degree centrality.** In-degree measures how many others point to a vertex, as in counting the links into a web page. [PageRank](/pagerank/) refines this by weighting each link by its source.
- **Regular digraphs.** A directed graph is $k$-regular when $d^+(v) = d^-(v) = k$ for each $v$; see [regular graph](/regular-graph/).

## References
