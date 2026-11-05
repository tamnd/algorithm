---
tag: YAC0K8
kind: definition
slug: subgraph
name: Subgraph
area: graphs/graph-representation
level: intro
summary: Graph formed from a subset of the vertices and edges of another graph.
prereqs: [graph, vertex, edge]
see_also: [induced-subgraph, spanning-tree, spanning-forest, subgraph-isomorphism, clique, graph-minor, k-core, maximum-common-subgraph]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the definitions of a subgraph and of the subgraph induced by a vertex set
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (Graphs), subgraph, induced subgraph, spanning subgraph, and the operations G − U, G − F and G + F
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, the definition of a subgraph; Section 1.2, spanning subgraphs and induced subgraphs
---

A subgraph of a [graph](/graph/) $G$ is a graph whose [vertices](/vertex/) are some of the vertices of $G$ and whose [edges](/edge/) are some of the edges of $G$ between those vertices. Most graph problems ask for a subgraph with a property: a path, a cycle, a [spanning tree](/spanning-tree/), a [clique](/clique/), a matching. Two kinds are special: an [induced subgraph](/induced-subgraph/) keeps every edge between its vertices, and a spanning subgraph keeps every vertex. The relation "is a subgraph of" is a partial order on graphs.

## Definition

Let $G = (V, E)$ be a graph, [directed](/directed-graph/) with $E \subseteq V \times V$ or [undirected](/undirected-graph/) with $E$ a set of 2-element subsets of $V$. A graph $H = (V', E')$ of the same kind is a **subgraph** of $G$, written $H \subseteq G$, if

$$V' \subseteq V, \qquad E' \subseteq E, \qquad \text{and each edge of } E' \text{ has both ends in } V'.$$

The third condition makes $H$ a graph: an edge cannot have an end that is not a vertex of $H$. If also $H \ne G$, then $H$ is a *proper* subgraph. $G$ is a *supergraph* of $H$.

For a [multigraph](/multigraph/) $G = (V, E, \psi)$, with an incidence function $\psi$ that gives the ends of each edge, a subgraph is $(V', E', \psi|_{E'})$ with $V' \subseteq V$, $E' \subseteq E$ and the ends $\psi(e) \subseteq V'$ for each $e \in E'$. For a [weighted graph](/weighted-graph/), the subgraph keeps the weights of its edges.

**Special kinds.**

- **Spanning subgraph**: $V' = V$. It is fixed by its edge set $E' \subseteq E$, so a graph with $m$ edges has exactly $2^m$ spanning subgraphs.
- **Induced subgraph** $G[S]$, for $S \subseteq V$: the vertex set $S$ and all the edges of $G$ with both ends in $S$. It is the largest subgraph with the vertex set $S$. See [induced subgraph](/induced-subgraph/).
- **Edge-induced subgraph** $G[F]$, for $F \subseteq E$: the edge set $F$ and the vertex set of all ends of edges in $F$. It is the smallest subgraph with the edge set $F$.
- **Deletions.** $G - v = G[V \setminus \{v\}]$ removes a vertex with its edges, and $G - e = (V, E \setminus \{e\})$ removes one edge. Each subgraph is reached from $G$ by a sequence of edge deletions and then vertex deletions.

**Partial order.** $\subseteq$ is reflexive, antisymmetric and transitive on graphs over a fixed ground set, because it is the pair of the set inclusions $V' \subseteq V$ and $E' \subseteq E$.

**"Contains a copy of."** In algorithms, "$G$ contains $H$" often means that some subgraph of $G$ is *isomorphic* to $H$: there is an injective map $f : V(H) \to V(G)$ with $(f(x), f(y)) \in E(G)$ for each edge $(x, y) \in E(H)$. Deciding this is the [subgraph isomorphism](/subgraph-isomorphism/) problem. It is NP-complete in general, since it contains the [clique](/clique-problem/) problem ($H = K_k$) and the Hamiltonian cycle problem ($H = C_n$). For a fixed $H$ with $k$ vertices, trying all maps takes $O(n^k)$ time.

**Building a subgraph.** From an [adjacency list](/adjacency-list/), the subgraph with a given vertex set $V'$ and a given edge set $E'$ takes $\Theta(|V'| + |E'|)$ time to store as a new adjacency list, with a table that renames the vertices of $V'$ to $0, \ldots, |V'| - 1$. A view that filters the edges of $G$ on the fly needs no copy, but each `neighbors` call then costs the degree in $G$.

## Examples and non-examples

Let $G$ have $V = \{1, 2, 3, 4, 5\}$ and $E = \{12, 13, 23, 24, 34, 45\}$, where $12$ means $\{1, 2\}$.

- $H_1 = (\{1, 2, 3, 4\}, \{12, 23, 34\})$ is a subgraph. It is a path. It is not induced, because $13$ and $24$ join vertices of $H_1$ and are missing.
- $H_2 = G[\{1, 2, 3, 4\}] = (\{1, 2, 3, 4\}, \{12, 13, 23, 24, 34\})$ is the induced subgraph on these four vertices.
- $H_3 = (V, \{12, 13, 24, 45\})$ is a spanning subgraph, and it is a [spanning tree](/spanning-tree/): it has 5 vertices, 4 edges and no cycle.
- $H_4 = G[\{23, 45\}] = (\{2, 3, 4, 5\}, \{23, 45\})$ is an edge-induced subgraph with two components.
- $(\{1, 2, 3, 4, 5\}, \emptyset)$ is a spanning subgraph, and $(\emptyset, \emptyset)$ is a subgraph of each graph if the empty graph is allowed.

**Non-examples.**

- $(\{1, 2\}, \{13\})$ is not a subgraph, because the edge $13$ has the end 3, which is not in the vertex set. It is not even a graph.
- $(\{1, 4\}, \{14\})$ is not a subgraph, because $14 \notin E$.
- In the directed graph with $E = \{(1, 2)\}$, the graph $(\{1, 2\}, \{(2, 1)\})$ is not a subgraph: $(2, 1) \ne (1, 2)$.

**Counts.** The number of subgraphs of $G$ is $\sum_{S \subseteq V} 2^{|E(G[S])|}$, since a subgraph with vertex set $S$ is any subset of the edges inside $S$. For the triangle $K_3$ this is $1 + 3 \cdot 1 + 3 \cdot 2 + 8 = 18$, counting the empty graph, and for $K_4$ it is 113.

## Related definitions

- **Induced subgraph.** The subgraph that keeps all edges inside a vertex set. Many graph classes are defined by forbidden induced subgraphs. See [induced subgraph](/induced-subgraph/).
- **Spanning tree and spanning forest.** A spanning subgraph that is a tree, or a forest with the same components as $G$. See [spanning tree](/spanning-tree/) and [spanning forest](/spanning-forest/).
- **Minor.** A [graph minor](/graph-minor/) allows edge contractions as well as deletions, so each subgraph is a minor but not each minor is a subgraph.
- **Complement.** The [complement graph](/complement-graph/) has the same vertices and the missing edges. A [clique](/clique/) of $G$ is an [independent set](/independent-set/) of the complement.
- **Cores.** The [k-core](/k-core/) is the largest induced subgraph in which each vertex has degree at least $k$.
- **Common subgraphs.** The [maximum common subgraph](/maximum-common-subgraph/) of two graphs is a largest graph that is isomorphic to a subgraph of each.

## References
