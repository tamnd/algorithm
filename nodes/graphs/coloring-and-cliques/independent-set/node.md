---
tag: 6MYPVF
kind: definition
slug: independent-set
name: Independent set
aliases:
- stable set
area: graphs/coloring-and-cliques
level: intro
summary: A set of vertices with no edges between any two of them.
prereqs: [graph, undirected-graph]
see_also: [independence-number, maximum-independent-set, maximal-independent-set, clique, vertex-cover, graph-coloring, complement-graph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.1, Graphs (independent sets of vertices and edges); Section 5.5, Perfect graphs (the notation α(G))
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.1 (cliques and independent sets), and Section 3.1 (independent sets and covers, Gallai's identity α(G) + β(G) = n(G))
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.2, problem GT20, Independent set
---

An independent set of a [graph](/graph/) is a set of vertices in which no two vertices are joined by an edge. It is the opposite of a [clique](/clique/), where every two vertices are joined, and the two ideas swap when you pass to the [complement graph](/complement-graph/). The color classes of a proper [coloring](/graph-coloring/) are independent sets, and the complement of an independent set is a [vertex cover](/vertex-cover/). Another name is *stable set*.

## Definition

Let $G = (V, E)$ be a finite simple [undirected graph](/undirected-graph/). A set $S \subseteq V$ is **independent** if

$$\forall u, v \in S: \quad \{u, v\} \notin E.$$

So the [induced subgraph](/induced-subgraph/) $G[S]$ has no edges. The empty set and each single vertex are independent.

- $S$ is a **maximal** independent set if it is independent and no vertex of $V \setminus S$ can be added: each $v \notin S$ has a neighbor in $S$.
- $S$ is a **maximum** independent set if no independent set of $G$ has more vertices. Its size is the [independence number](/independence-number/) $\alpha(G)$.

Each maximum independent set is maximal. The converse is false (see the examples).

With a weight $w : V \to \mathbb{R}_{\ge 0}$, the weight of $S$ is $w(S) = \sum_{v \in S} w(v)$, and a maximum-weight independent set is an independent set of largest weight.

The same word is used for edges: a set of edges is independent if no two of them share an end. An independent set of edges is a [matching](/maximum-matching/). On this page, "independent set" means a set of vertices.

## Examples and non-examples

The Petersen graph below has the outer 5-cycle $0, 1, 2, 3, 4$, the inner pentagram $5\!-\!7\!-\!9\!-\!6\!-\!8\!-\!5$ (vertex $i$ is joined to $i \pm 2$ inside $\{5, \ldots, 9\}$), and the spokes $\{i, i + 5\}$.

- **Independent.** $\{0, 2, 8, 9\}$. The vertex 0 is adjacent only to 1, 4 and 5; the vertex 2 only to 1, 3 and 7; and 8 and 9 are not adjacent because $9 - 8 = 1$, not $\pm 2$ modulo 5. This set has 4 vertices, and the Petersen graph has no independent set of 5 vertices, so $\alpha = 4$. There are exactly 5 independent sets of size 4.
- **Maximal but not maximum.** $\{0, 2, 6\}$ is independent, and each of the other 7 vertices has a neighbor in it. So no vertex can be added, but the set has only 3 vertices. The Petersen graph has 15 maximal independent sets: 5 of size 4 and 10 of size 3.
- **Not independent.** $\{0, 2, 7\}$, because $\{2, 7\}$ is a spoke.
- **Paths and cycles.** The path $P_n$ with $n$ vertices has $\alpha = \lceil n/2 \rceil$ (take every second vertex). The cycle $C_n$ has $\alpha = \lfloor n/2 \rfloor$. The number of independent sets, the empty set included, is the [Fibonacci number](/fibonacci-numbers/) $F_{n+2}$ for $P_n$ (2, 3, 5, 8, 13 for $n = 1$ to $5$) and the Lucas number $L_n$ for $C_n$ (4, 7, 11, 18 for $n = 3$ to $6$).
- **Extremes.** In the [complete graph](/complete-graph/) $K_n$, the independent sets are the empty set and the single vertices, so $\alpha(K_n) = 1$. In the graph with $n$ vertices and no edges, every set is independent.
- **Bipartite graphs.** Each side of a [bipartite graph](/bipartite-graph/) is independent. In $K_{m,n}$ the maximal independent sets are exactly the two sides, so $\alpha(K_{m,n}) = \max(m, n)$.

## Related definitions

- **Clique.** $S$ is independent in $G$ if and only if $S$ is a [clique](/clique/) in the [complement](/complement-graph/) $\overline{G}$. So $\alpha(G) = \omega(\overline{G})$, where $\omega$ is the [clique number](/clique-number/), and each statement about cliques becomes one about independent sets.
- **Vertex cover.** $S$ is independent if and only if $V \setminus S$ touches every edge, that is, $V \setminus S$ is a [vertex cover](/vertex-cover/). An edge with both ends in $S$ is exactly an edge that $V \setminus S$ misses. So $\alpha(G) + \beta(G) = |V|$, where $\beta$ is the size of a smallest vertex cover (Gallai).
- **Coloring.** A proper $k$-coloring is a partition of $V$ into $k$ independent sets. So $\chi(G) \ge |V| / \alpha(G)$, where $\chi$ is the [chromatic number](/chromatic-number/).
- **Hereditary.** Each subset of an independent set is independent. So the independent sets form a downward-closed family, and a maximal one can be found by a [greedy](/greedy-independent-set/) pass that adds any vertex with no neighbor in the set.
- **Problems.** Finding a largest independent set is the [maximum independent set problem](/maximum-independent-set/), which is NP-hard (Garey and Johnson, problem GT20). Finding one maximal independent set takes linear time; see [maximal independent set](/maximal-independent-set/). Listing all of them is [maximal independent set enumeration](/maximal-independent-set-enumeration/).

## References
