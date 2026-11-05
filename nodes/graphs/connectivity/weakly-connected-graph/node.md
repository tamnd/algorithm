---
tag: 24M951
kind: definition
slug: weakly-connected-graph
name: Weakly connected graph
area: graphs/connectivity
level: intro
summary: A directed graph whose underlying undirected graph is connected.
prereqs: [directed-graph, connected-graph]
see_also: [strongly-connected-graph, connected-components, strongly-connected-components, condensation-graph, union-find-connectivity, undirected-graph]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.4, Directed graphs (underlying graph, weakly connected and strongly connected digraphs)
  - book: isbn:9781848009974
    title: Jørgen Bang-Jensen and Gregory Gutin, Digraphs, Theory, Algorithms and Applications, second edition, Springer (2009)
    locator: Chapter 1, Basic terminology, notation and results (underlying graph, connected and strong digraphs)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4, Graphs (the undirected version of a directed graph, connected and strongly connected graphs)
---

A weakly connected graph is a [directed graph](/directed-graph/) that becomes a [connected graph](/connected-graph/) when the directions of its arcs are ignored. It is the weakest of the usual notions of connection for directed graphs: a [strongly connected graph](/strongly-connected-graph/) is always weakly connected, but a weakly connected graph can have pairs of vertices that reach each other in neither direction. The maximal weakly connected parts of a directed graph are its *weak components*, and they are found in linear time by any search on the graph with both directions of each arc.

## Definition

Let $G = (V, E)$ be a directed graph. [Parallel arcs](/multigraph/) and [self-loops](/self-loop/) are allowed. The *underlying graph* $U(G)$ is the [undirected graph](/undirected-graph/) on $V$ with one edge $\{x, y\}$ for each arc $(x, y) \in E$. Two opposite arcs $(x, y)$ and $(y, x)$ give two parallel edges in $U(G)$, and a loop stays a loop. None of this changes connectivity.

$$G \text{ is weakly connected} \iff U(G) \text{ is connected.}$$

So $V \neq \emptyset$, and for each two vertices $u, v$ there is a sequence $u = x_0, x_1, \ldots, x_k = v$ in which each consecutive pair is joined by an arc in at least one direction. Such a sequence is a *semipath*. The graph with one vertex is weakly connected, and the graph with no vertex is not, by the convention of the [connected graph](/connected-graph/) page.

**Cut form.** For $S \subseteq V$, let $E(S)$ be the set of arcs with exactly one end in $S$, in either direction. A directed graph with $V \neq \emptyset$ is weakly connected if and only if $E(S) \neq \emptyset$ for each $S$ with $\emptyset \neq S \subsetneq V$. This is the cut form of connectivity applied to $U(G)$, because an edge of $U(G)$ leaves $S$ exactly when its arc has one end in $S$. Compare the [strongly connected](/strongly-connected-graph/) case, where the arc must point out of $S$.

**Three levels.** Call $G$ *unilaterally connected* if $V \neq \emptyset$ and for each pair $u, v$ there is a directed path from $u$ to $v$ or from $v$ to $u$. Then

$$\text{strongly connected} \implies \text{unilaterally connected} \implies \text{weakly connected},$$

and both converses fail (examples below). The first implication is clear. For the second, a directed path in either direction is a semipath.

**Unilateral connection through the condensation.** Let $C$ be the [condensation](/condensation-graph/) of $G$, the acyclic graph with one vertex for each [strongly connected component](/strongly-connected-components/). Then $G$ is unilaterally connected if and only if $C$ has a directed path through all of its vertices.

*Proof.* Two vertices of one component reach each other, so $G$ is unilaterally connected exactly when, for each two components $A \ne B$, one reaches the other in $C$. If $C$ has a path $c_1 \to c_2 \to \cdots \to c_k$ through all its vertices, then $c_i$ reaches $c_j$ for $i < j$, so this holds. Conversely, assume it holds. List the components in a [topological order](/topological-ordering/) $c_1, \ldots, c_k$ of $C$. For each $i < k$, the vertex $c_{i+1}$ cannot reach $c_i$, because each arc goes forward in the order. So $c_i$ reaches $c_{i+1}$. Every vertex on such a path lies between $c_i$ and $c_{i+1}$ in the order, and there is no index strictly between $i$ and $i + 1$, so the path is the single arc $(c_i, c_{i+1})$. These arcs form the path through all vertices. $\square$

**Fewest arcs.** A weakly connected graph on $n$ vertices has at least $n - 1$ arcs, because $U(G)$ is a connected graph with the same number of edges. Each orientation of a [spanning tree](/spanning-tree/) has exactly $n - 1$ arcs and is weakly connected.

**Testing.** Build $U(G)$ by adding each arc to the lists of both of its ends, then run one [graph search](/graph-reachability/) from any vertex, or join the two ends of each arc with [union-find](/union-find-connectivity/). Both take $O(n + m)$ time, the union-find route up to an inverse Ackermann factor. A search that follows only the outgoing arcs is wrong here: from a vertex with no outgoing arc it marks only that vertex.

## Examples and non-examples

| graph | weakly | unilaterally | strongly |
|---|---|---|---|
| the directed cycle $0 \to 1 \to 2 \to 0$ | yes | yes | yes |
| the directed path $0 \to 1 \to 2$ | yes | yes | no |
| the "V" with arcs $0 \to 1$ and $2 \to 1$ | yes | no | no |
| the star with arcs $0 \to 1$, $0 \to 2$, $0 \to 3$ | yes | no | no |
| the arcs $0 \to 1$, $1 \to 0$, $1 \to 2$, $2 \to 3$, $3 \to 2$ | yes | yes | no |
| two directed triangles with no common vertex | no | no | no |
| one vertex with a loop | yes | yes | yes |

In the "V", the vertices 0 and 2 do not reach each other in either direction, but they are joined by the semipath $0, 1, 2$. In the fifth row, the condensation is the path $\{0, 1\} \to \{2, 3\}$, so the graph is unilaterally connected.

The table counts the weakly connected graphs on the vertex set $\{1, \ldots, n\}$ without loops and parallel arcs, among all $2^{n(n-1)}$ such graphs.

| $n$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| all directed graphs | 1 | 4 | 64 | 4096 |
| weakly connected | 1 | 3 | 54 | 3834 |
| strongly connected | 1 | 1 | 18 | 1606 |

For $n = 2$ the three weakly connected graphs are $0 \to 1$, $1 \to 0$ and the pair of opposite arcs.

## Related definitions

- [Connected graph](/connected-graph/) and [connected components](/connected-components/): the undirected notions. The weak components of $G$ are the connected components of $U(G)$.
- [Strongly connected graph](/strongly-connected-graph/) and [strongly connected components](/strongly-connected-components/): mutual reachability. Each strong component lies inside one weak component.
- [Condensation graph](/condensation-graph/): the acyclic graph of the strong components. Each weak component of $G$ gives one weak component of the condensation.
- [Directed acyclic graph](/directed-acyclic-graph/): a weakly connected directed acyclic graph with $n \ge 2$ vertices is never strongly connected.
- [Connectivity by union-find](/union-find-connectivity/): finds the weak components by processing the arcs in any order and with any direction.

## References
