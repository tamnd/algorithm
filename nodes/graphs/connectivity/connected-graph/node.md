---
tag: XXWVNN
kind: definition
slug: connected-graph
name: Connected graph
aliases:
- Connected undirected graph
area: graphs/connectivity
level: intro
summary: An undirected graph in which every pair of vertices is joined by a path.
prereqs: [undirected-graph, simple-path]
see_also: [connected-components, weakly-connected-graph, strongly-connected-graph, spanning-tree, articulation-point, bridge, k-vertex-connected-graph, k-edge-connected-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Section 1.4, Connectivity (connected graphs and components), and Section 1.5, Trees and forests (a connected graph on n vertices has at least n - 1 edges)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2, Paths, cycles, and trails (connection, components, and the count of components when edges are added)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4, Graphs (connected graphs and connected components)
---

A connected graph is an [undirected graph](/undirected-graph/) with at least one vertex in which each two vertices are joined by a [path](/simple-path/). It is the base notion of graph connectivity: a graph that is not connected falls apart into [connected components](/connected-components/), and stronger notions such as [biconnected graphs](/biconnected-graph/) and [k-vertex-connected graphs](/k-vertex-connected-graph/) ask that the graph stays connected after some vertices or edges are removed. A connected graph on $n$ vertices has at least $n - 1$ edges, and it has exactly $n - 1$ edges if and only if it is a [tree](/tree/).

## Definition

Let $G = (V, E)$ be an undirected graph. Parallel edges and [self-loops](/self-loop/) are allowed, as in a [multigraph](/multigraph/). They do not change any statement of this section except the edge bound for simple graphs, because a path never needs a loop or a second copy of an edge.

A *$u$-$v$ path* is a sequence of distinct vertices $u = x_0, x_1, \ldots, x_k = v$ with an edge between $x_{i-1}$ and $x_i$ for each $i$. Its length is $k$. For each vertex $u$, the sequence $u$ alone is a $u$-$u$ path of length 0.

$$G \text{ is connected} \iff V \neq \emptyset \ \text{ and } \ \forall u, v \in V \ \exists \text{ a } u\text{-}v \text{ path in } G.$$

We follow Diestel and require $V \neq \emptyset$, so the graph with no vertex is not connected. Some authors call it connected; the difference matters only for statements such as "a graph has exactly one component".

**Walks are enough.** If there is a [walk](/walk/) from $u$ to $v$ (vertices may repeat), there is a path: take a shortest walk; if it visited some vertex twice, cutting out the part between the two visits gives a shorter walk. So "joined by a walk" and "joined by a path" define the same relation. This relation is reflexive (length 0), symmetric (reverse the path) and transitive (join two walks). It is an [equivalence relation](/equivalence-relation/), and its classes are the vertex sets of the connected components. So $G$ is connected exactly when it has one component.

**The cut form.** For a set $S \subseteq V$, write $E(S, V \setminus S)$ for the set of edges with one end in $S$ and the other end outside $S$. Then a graph with $V \neq \emptyset$ is connected if and only if

$$\forall S \text{ with } \emptyset \neq S \subsetneq V : \ E(S, V \setminus S) \neq \emptyset.$$

*Proof.* Suppose $G$ is connected and $\emptyset \neq S \subsetneq V$. Pick $u \in S$ and $v \notin S$, and a $u$-$v$ path $x_0, \ldots, x_k$. Let $i$ be the least index with $x_i \notin S$. Then $i \ge 1$, $x_{i-1} \in S$, and the edge between $x_{i-1}$ and $x_i$ is in $E(S, V \setminus S)$. Conversely, suppose $G$ is not connected, and let $S$ be the set of vertices joined to some vertex $u$ by a path. Some $v$ is not joined to $u$, so $u \in S$ and $v \notin S$. An edge from $x \in S$ to $y \notin S$ would extend the $u$-$x$ walk to a $u$-$y$ walk, which is impossible. So $E(S, V \setminus S) = \emptyset$. $\square$

This form is the one that algorithms use: [graph search](/generic-component-growing/) grows a set $S$ from one vertex and stops when no edge leaves $S$.

**Fewest edges.** A connected graph on $n$ vertices has at least $n - 1$ edges.

*Proof.* Start from the graph $(V, \emptyset)$, which has $n$ components, and add the edges of $E$ one by one. An edge with both ends in one component leaves the components as they are. An edge with ends in two components merges these two into one and leaves the others. So each edge lowers the number of components by at most 1. To go from $n$ components to 1, at least $n - 1$ edges are needed. $\square$

A connected graph with exactly $n - 1$ edges has no cycle: in the proof each edge must merge two components, and an edge that closes a cycle joins two vertices of the same component. So it is a tree. Each connected graph contains a tree on all its vertices, a [spanning tree](/spanning-tree/).

**Two sufficient conditions for simple graphs.** Let $G$ be [simple](/simple-graph/) with $n \ge 2$ vertices.

- If $|E| > \binom{n-1}{2}$, then $G$ is connected. *Proof.* If $G$ is not connected, take a component with $k$ vertices, $1 \le k \le n - 1$. No edge joins it to the other $n - k$ vertices, so $|E| \le \binom{k}{2} + \binom{n-k}{2}$. This sum is a convex function of $k$, so on $1 \le k \le n-1$ it is largest at $k = 1$ or $k = n - 1$, where it equals $\binom{n-1}{2}$. $\square$ The bound is tight: the [complete graph](/complete-graph/) $K_{n-1}$ plus one isolated vertex has $\binom{n-1}{2}$ edges and is not connected.
- If each vertex has [degree](/degree/) at least $(n-1)/2$, then $G$ is connected. *Proof.* Take two vertices $u \neq v$ that are not adjacent. Their neighbour sets lie in $V \setminus \{u, v\}$, which has $n - 2$ vertices, and their sizes add up to at least $n - 1$. So they share a vertex $w$, and $u, w, v$ is a path. $\square$

Neither condition holds for multigraphs: two vertices with a hundred parallel edges, plus one isolated vertex, are not connected.

**Directed graphs.** For a [directed graph](/directed-graph/), "connected" splits in two. The graph is [weakly connected](/weakly-connected-graph/) when the undirected graph that forgets the directions is connected. It is [strongly connected](/strongly-connected-graph/) when for each ordered pair $(u, v)$ there is a directed path from $u$ to $v$. Strongly connected implies weakly connected, and the directed path $0 \to 1$ shows that the converse fails.

## Examples and non-examples

| graph | vertices | edges | connected? | why |
|---|---|---|---|---|
| one vertex, no edge ($K_1$) | 1 | 0 | yes | the only pair is $(u, u)$, joined by the path of length 0 |
| the path $0 - 1 - 2 - 3$ | 4 | 3 | yes | a tree, so the fewest edges possible |
| the cycle $0 - 1 - 2 - 3 - 0$ | 4 | 4 | yes | one edge more than a tree |
| two vertices with 3 parallel edges and a loop | 2 | 4 | yes | parallel edges and loops do not matter |
| two triangles with no common vertex | 6 | 6 | no | the cut between the triangles is empty |
| $K_4$ plus an isolated vertex | 5 | 6 | no | $6 = \binom{4}{2}$, the largest disconnected simple graph on 5 vertices |
| any simple graph on 5 vertices with 7 edges | 5 | 7 | yes | $7 > \binom{4}{2}$ |
| the graph with no vertex | 0 | 0 | no | by the convention $V \neq \emptyset$ |

The table counts the connected simple graphs on the vertex set $\{1, \ldots, n\}$ among all $2^{\binom{n}{2}}$ simple graphs on it.

| $n$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| all graphs | 1 | 2 | 8 | 64 | 1024 |
| connected | 1 | 1 | 4 | 38 | 728 |

**A directed non-example.** The directed graph with the edges $0 \to 1$ and $1 \to 2$ is weakly connected but not strongly connected, because no directed path goes from 2 to 0.

## Related definitions

- [Connected components](/connected-components/): the maximal connected subgraphs, one for each class of the relation "joined by a path". The page gives the linear-time algorithms that find them.
- [Articulation point](/articulation-point/) and [bridge](/bridge/): a vertex or an edge whose removal splits a component.
- [Biconnected graph](/biconnected-graph/), [k-vertex-connected graph](/k-vertex-connected-graph/) and [k-edge-connected graph](/k-edge-connected-graph/): graphs that stay connected after the removal of a few vertices or edges.
- [Tree](/tree/) and [spanning tree](/spanning-tree/): the connected graphs with the fewest edges, and the trees inside a connected graph.
- [Weakly connected graph](/weakly-connected-graph/) and [strongly connected graph](/strongly-connected-graph/): the two notions for directed graphs.
- [Graph reachability](/graph-reachability/): the question whether one given vertex is joined to another.

## References
