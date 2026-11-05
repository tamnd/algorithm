---
tag: YDMNX2
kind: definition
slug: directed-graph
name: Directed graph
aliases:
- digraph
area: graphs/graph-representation
level: intro
summary: Graph whose edges are ordered pairs with a direction.
prereqs: [graph, edge]
see_also: [directed-and-undirected-graphs, undirected-graph, in-degree-and-out-degree, directed-acyclic-graph, transpose-graph, strongly-connected-components, reachability, adjacency-list]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the definition of a directed graph, paths, cycles and strong connectivity
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2 (Directed graphs), the Digraph API and the glossary
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.10 (Other notions of graphs), directed graphs and orientations
---

A directed graph, or digraph, is a [graph](/graph/) $G = (V, E)$ in which each [edge](/edge/) is an ordered pair $(u, v)$ that goes from the vertex $u$ to the vertex $v$. The direction matters: $(u, v)$ is an edge does not imply that $(v, u)$ is one. Directed graphs model one-way relations, such as web links, calls between functions, the order of tasks and the moves of a state machine. On them, [reachability](/reachability/), [strongly connected components](/strongly-connected-components/) and [topological order](/topological-sort/) are the basic questions.

## Definition

A **directed graph** is a pair $G = (V, E)$ of a finite set $V$ and a set $E \subseteq V \times V$. The elements of $V$ are vertices and the elements of $E$ are directed edges, or arcs. We write $n = |V|$ and $m = |E|$.

This is the convention of CLRS, Appendix B.4. It allows a [self-loop](/self-loop/) $(v, v)$, and it allows no two edges with the same tail and the same head. So $0 \le m \le n^2$. Many authors also forbid self-loops; then $m \le n(n-1)$. A directed graph with parallel edges is a directed [multigraph](/multigraph/).

For an edge $(u, v)$: $u$ is the *tail*, $v$ is the *head*, the edge *leaves* $u$ and *enters* $v$, and $v$ is an *out-neighbour* of $u$. We write

$$N^+(u) = \{v : (u, v) \in E\}, \qquad N^-(v) = \{u : (u, v) \in E\},$$

and the [out-degree and in-degree](/in-degree-and-out-degree/) are $d^+(u) = |N^+(u)|$ and $d^-(v) = |N^-(v)|$. Each edge has exactly one tail and one head, so

$$\sum_{v \in V} d^+(v) = \sum_{v \in V} d^-(v) = m.$$

**Paths and reachability.** A *directed walk* of length $k \ge 0$ is a sequence $v_0, v_1, \ldots, v_k$ of vertices with $(v_{i-1}, v_i) \in E$ for each $1 \le i \le k$. It is a *directed path* when the $v_i$ are distinct. A vertex $v$ is *reachable* from $u$ when a directed walk from $u$ to $v$ exists; then a directed path exists too, by cutting out each part of the walk between two visits of the same vertex. A *directed cycle* is a directed walk with $k \ge 1$ and $v_0 = v_k$ in which $v_1, \ldots, v_k$ are distinct. A self-loop is a cycle of length 1, and $(u, v), (v, u)$ is a cycle of length 2.

**Strong connectivity.** $G$ is *strongly connected* when each vertex is reachable from each other vertex. The *underlying undirected graph* of $G$ has the edge $\{u, v\}$ for each $(u, v) \in E$ with $u \ne v$; $G$ is *weakly connected* when that graph is connected.

**Transpose.** The [transpose graph](/transpose-graph/) is $G^T = (V, \{(v, u) : (u, v) \in E\})$. It has the same vertices and the reverse of each edge.

## Examples and non-examples

**A worked example.** Let $V = \{0, 1, 2, 3, 4\}$ and

$$E = \{(0, 1), (0, 2), (1, 2), (2, 3), (3, 1), (3, 4)\}.$$

| vertex | $N^+$ | $N^-$ | $d^+$ | $d^-$ |
|---|---|---|---|---|
| 0 | 1, 2 | none | 2 | 0 |
| 1 | 2 | 0, 3 | 1 | 2 |
| 2 | 3 | 0, 1 | 1 | 2 |
| 3 | 1, 4 | 2 | 2 | 1 |
| 4 | none | 3 | 0 | 1 |

Both columns of degrees sum to $6 = m$. The walk $1, 2, 3, 1$ is a directed cycle of length 3. The vertex 4 is reachable from 0 by the path $0, 2, 3, 4$, but 0 is not reachable from any other vertex, because $d^-(0) = 0$. So $G$ is weakly connected but not strongly connected. Its strongly connected components are $\{0\}$, $\{1, 2, 3\}$ and $\{4\}$.

**More examples.**

- The web graph: pages are vertices, and a link from page $p$ to page $q$ is the edge $(p, q)$.
- A call graph: functions are vertices, and $(f, g)$ is an edge when $f$ calls $g$. A recursive function has a self-loop.
- A [directed acyclic graph](/directed-acyclic-graph/), such as the graph of the tasks of a build, where $(a, b)$ means that $a$ must finish before $b$ starts.
- The graph of a function $f : V \to V$, with the edges $(v, f(v))$. This is a [functional graph](/functional-graph/), and each vertex has out-degree 1.
- A tournament: for each two distinct vertices $u, v$, exactly one of $(u, v)$ and $(v, u)$ is an edge. It has $\binom{n}{2}$ edges.

**Non-examples.**

- An undirected graph is not a directed graph: its edges are sets $\{u, v\}$, not pairs. It corresponds to the *symmetric* directed graph with both $(u, v)$ and $(v, u)$ for each edge, which is how an [adjacency list](/adjacency-list/) stores it. This correspondence is a bijection between simple undirected graphs and loopless directed graphs with a symmetric edge relation.
- Two flights from $A$ to $B$ at different times are two parallel edges. They do not fit in $E \subseteq V \times V$, so they need a directed multigraph.
- A relation on an infinite set, such as $<$ on the integers, is not a directed graph in the sense of this page, because $V$ must be finite.

## Related definitions

- [Undirected graph](/undirected-graph/), and the comparison on [directed and undirected graphs](/directed-and-undirected-graphs/).
- [In-degree and out-degree](/in-degree-and-out-degree/).
- [Directed acyclic graph](/directed-acyclic-graph/): a directed graph with no directed cycle.
- [Transpose graph](/transpose-graph/): all edges reversed.
- [Reachability](/reachability/), [transitive closure](/transitive-closure/) and [strongly connected components](/strongly-connected-components/).
- [Functional graph](/functional-graph/): each out-degree is 1.
- [Adjacency list](/adjacency-list/) and [adjacency matrix](/adjacency-matrix/): the two standard ways to store it.

## References
