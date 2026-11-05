---
tag: SJK56N
kind: definition
slug: clique
name: Clique
aliases:
- complete subgraph
area: graphs/coloring-and-cliques
level: intro
summary: A set of vertices that are pairwise adjacent.
prereqs: [undirected-graph, complete-graph, induced-subgraph]
see_also: [clique-number, maximal-clique, maximum-clique, independent-set, clique-decision, bron-kerbosch, clique-cover, complement-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1, Graphs (complete graphs and the terms clique and independent set) and Section 5.5, Perfect graphs (the clique number ω(G))
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1, What is a graph? (the definition of clique and independent set)
  - paper: doi:10.1007/BF02760024
    title: J. W. Moon and L. Moser, On cliques in graphs, Israel Journal of Mathematics 3(1), 23 to 28 (1965)
    locator: the whole paper (the largest number of maximal cliques of a graph on n vertices)
---

A clique of an undirected [graph](/graph/) is a set of vertices in which each two are adjacent, so that the [induced subgraph](/induced-subgraph/) on it is a [complete graph](/complete-graph/). A clique is *maximal* when no vertex can be added to it, and *maximum* when no clique of the graph is larger; the size of a maximum clique is the [clique number](/clique-number/) $\omega(G)$. Cliques are the opposite of [independent sets](/independent-set/): a set is a clique of $G$ exactly when it is independent in the [complement graph](/complement-graph/). Finding a maximum clique is NP-hard, and listing all maximal cliques is the classic task of the [Bron-Kerbosch algorithm](/bron-kerbosch/).

## Definition

Let $G = (V, E)$ be a simple undirected graph.

- A set $K \subseteq V$ is a **clique** of $G$ if $\{u, v\} \in E$ for all distinct $u, v \in K$. A clique with $k$ vertices is a **$k$-clique**. The empty set and each single vertex are cliques.
- A clique $K$ is **maximal** if no $v \in V \setminus K$ makes $K \cup \{v\}$ a clique, that is, if no vertex outside $K$ is adjacent to all of $K$.
- A clique $K$ is **maximum** if $|K| \ge |K'|$ for each clique $K'$ of $G$. Its size is the clique number $\omega(G)$.

Each maximum clique is maximal. The converse is false. Some authors use "clique" for the complete subgraph $G[K]$ and not for the set $K$; some use it only for maximal cliques. On this site a clique is a set of vertices, and the word maximal is always written out.

**Complement.** $K$ is a clique of $G$ if and only if $K$ is an independent set of the complement $\overline G$, which has an edge $\{u, v\}$ exactly when $G$ has none. So $\omega(G) = \alpha(\overline G)$, where $\alpha$ is the [independence number](/independence-number/).

**Directed graphs.** In a directed graph, a clique usually means a set in which each two vertices are joined by arcs in both directions, that is, a clique of the undirected graph of the 2-cycles.

## Examples and non-examples

Take the graph $G$ on the vertices $0, \ldots, 6$ with the 11 edges

$$01,\ 02,\ 12,\ 13,\ 23,\ 24,\ 34,\ 35,\ 45,\ 06,\ 56.$$

- $\{1, 2, 3\}$ is a clique: $12$, $13$ and $23$ are edges. It is maximal: vertex 0 is not adjacent to 3, vertex 4 is not adjacent to 1, and vertices 5 and 6 are not adjacent to 1.
- $\{0, 6\}$ is a maximal clique of size 2. It is maximal because no other vertex is adjacent to both 0 and 6. It is not maximum.
- $G$ has exactly 6 maximal cliques: $\{0,1,2\}$, $\{1,2,3\}$, $\{2,3,4\}$, $\{3,4,5\}$, $\{0,6\}$ and $\{5,6\}$. So $\omega(G) = 3$.
- $G$ has 23 cliques in total: the empty set, 7 single vertices, 11 edges and 4 triangles.
- **Non-example.** $\{1, 2, 3, 4\}$ is not a clique, because $14$ is not an edge.
- **Non-example.** $\{0, 1\}$ is a clique but not a maximal one, because vertex 2 is adjacent to both.

Other examples:

- In the complete graph $K_n$, each set of vertices is a clique, and $V$ is the only maximal clique.
- In a graph with no edges, the maximal cliques are the single vertices.
- In a [bipartite graph](/bipartite-graph/) with at least one edge, the maximal cliques are the edges and the isolated vertices, and $\omega = 2$.
- In a cycle $C_n$ with $n \ge 4$, the maximal cliques are the $n$ edges.

**How many maximal cliques.** A graph on $n$ vertices can have exponentially many maximal cliques. The complete 3-partite graph $K_{3,3,3}$ (9 vertices, two vertices adjacent when they are in different parts) has $3^3 = 27$ maximal cliques: choose one vertex from each part. Moon and Moser (1965) proved that the largest number of maximal cliques of a graph on $n \ge 2$ vertices is $3^{n/3}$ when $3 \mid n$, $4 \cdot 3^{(n-4)/3}$ when $n \equiv 1 \pmod 3$, and $2 \cdot 3^{(n-2)/3}$ when $n \equiv 2 \pmod 3$. The complete multipartite graphs reach these numbers: all parts of size 3 when $3 \mid n$; parts of size 3 and one part of size 4, or two parts of size 2, when $n \equiv 1$; parts of size 3 and one part of size 2 when $n \equiv 2$.

## Related definitions

- [Clique number](/clique-number/): $\omega(G)$, the size of a maximum clique.
- [Maximal clique](/maximal-clique/) and [maximum clique](/maximum-clique/): the two optimality notions above, with their own algorithms.
- [Independent set](/independent-set/): a set with no edge inside; a clique of the complement.
- [Clique cover](/clique-cover/): a partition of the vertices into cliques.
- [Clique decision problem](/clique-decision/): does $G$ have a clique of size $k$? It is NP-complete.
- [Chromatic number](/chromatic-number/): $\chi(G) \ge \omega(G)$, because a clique needs one color for each vertex.
- [Perfect graph](/perfect-graph/): $\chi(H) = \omega(H)$ for each induced subgraph $H$.
- [Hyperclique](/hyperclique/): the analogue in a hypergraph.
- [Turán's theorem](/turan-theorem/) and [Ramsey's theorem](/ramsey-theorem/): how many edges, or how many vertices, force a clique of a given size.

## References
