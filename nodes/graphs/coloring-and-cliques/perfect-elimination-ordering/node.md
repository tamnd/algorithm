---
tag: W1EBF1
kind: concept
slug: perfect-elimination-ordering
name: Perfect elimination ordering
aliases:
- PEO
area: graphs/coloring-and-cliques
level: advanced
summary: A vertex ordering in which each vertex's later neighbors form a clique; such an ordering exists exactly for chordal graphs.
prereqs: [chordal-graph, clique]
see_also: [lexicographic-bfs, maximum-cardinality-search, chordal-graph-coloring, elimination-ordering, treewidth, cholesky-decomposition, perfect-graph, maximal-clique-enumeration]
sources:
  - paper: doi:10.2140/pjm.1965.15.835
    title: D. R. Fulkerson and O. A. Gross, Incidence matrices and interval graphs, Pacific Journal of Mathematics 15(3), 835 to 855 (1965)
    locator: the characterization of chordal graphs by perfect elimination orderings
  - paper: "G. A. Dirac, On rigid circuit graphs, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 25, 71 to 76 (1961)"
    locator: every chordal graph that is not complete has two non-adjacent simplicial vertices
  - paper: "D. J. Rose, Triangulated graphs and the elimination process, Journal of Mathematical Analysis and Applications 32, 597 to 609 (1970)"
    locator: elimination without fill-in and perfect elimination orderings
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 266 to 283 (1976)
    locator: lexicographic breadth-first search and the linear-time test of an ordering
  - paper: doi:10.1137/0213035
    title: Robert E. Tarjan and Mihalis Yannakakis, Simple linear-time algorithms to test chordality of graphs, test acyclicity of hypergraphs, and selectively reduce acyclic hypergraphs, SIAM Journal on Computing 13(3), 566 to 579 (1984)
    locator: maximum cardinality search
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Elsevier, 2004
    locator: Chapter 4, Triangulated graphs
---

A perfect elimination ordering of a graph is an order $v_1, \ldots, v_n$ of its vertices in which, for each $i$, the neighbors of $v_i$ that come after it form a [clique](/clique/). Fulkerson and Gross proved in 1965 that a graph has such an ordering if and only if it is [chordal](/chordal-graph/), that is, every cycle of length at least 4 has a chord. [Lexicographic BFS](/lexicographic-bfs/) and [maximum cardinality search](/maximum-cardinality-search/) find one in $O(n + m)$ time, and with it coloring, maximum clique and maximum independent set become easy on chordal graphs.

## In plain words

Remove the points of a network one at a time. Call a point safe to remove when the points it is still linked to are all linked to each other. An ordering is perfect when every point is safe at the moment it is removed.

Some networks have such an ordering and some do not. A ring of four points has none: each point has two remaining partners that are not linked. The networks that have one are exactly those with no long ring without a shortcut. For them, many hard questions, such as how many colors are needed, become easy, because the ordering tells you how to answer them one point at a time.

## The idea

A vertex $v$ is **simplicial** in $G$ when $N(v)$ is a clique. An order $\sigma = (v_1, \ldots, v_n)$ is a **perfect elimination ordering** (PEO) when each $v_i$ is simplicial in $G[\{v_i, \ldots, v_n\}]$. Write $L(v)$ for the set of later neighbors of $v$.

**Theorem (Fulkerson and Gross 1965).** $G$ has a PEO if and only if $G$ is chordal.

*If $G$ has a PEO, it is chordal.* Let $C$ be a cycle of length at least 4, and let $v$ be its earliest vertex in $\sigma$. Its two neighbors on $C$ are later, so they are adjacent, and that edge is a chord of $C$.

*If $G$ is chordal, it has a PEO.* Dirac proved that every chordal graph has a simplicial vertex; in fact, every chordal graph that is not complete has two non-adjacent ones. Induced subgraphs of chordal graphs are chordal. So remove a simplicial vertex, recurse on the rest, and list the vertices in the order of removal. $\square$

**Finding one.** Lexicographic BFS (Rose, Tarjan and Lueker 1976) and maximum cardinality search (Tarjan and Yannakakis 1984) each produce an order whose reverse is a PEO whenever $G$ is chordal, in $O(n + m)$ time.

**Testing one.** For each $v$, let $p(v)$ be the earliest vertex of $L(v)$. The order is a PEO if and only if, for every $v$, the set $L(v) \setminus \{p(v)\}$ lies in $N(p(v))$. Collecting these requests and checking them all with one pass over the adjacency lists takes $O(n + m)$ time. Together with a search above, this decides whether a graph is chordal in linear time.

## Examples

Take the graph with vertices $0, \ldots, 5$ and edges $01, 02, 12, 13, 23, 34, 35, 45$: the triangles $\{0, 1, 2\}$, $\{1, 2, 3\}$ and $\{3, 4, 5\}$, glued along the edge $12$ and the vertex $3$.

| order | later neighbors | PEO? |
|---|---|---|
| $0, 4, 1, 2, 3, 5$ | $L(0) = \{1, 2\}$, $L(4) = \{3, 5\}$, $L(1) = \{2, 3\}$, $L(2) = \{3\}$, $L(3) = \{5\}$ | yes |
| $1, 0, 2, 3, 4, 5$ | $L(1) = \{0, 2, 3\}$, and $0$, $3$ are not adjacent | no |

Of the $720$ orders of this graph, $108$ are perfect elimination orderings.

- **Coloring.** Color greedily in the reverse order $5, 3, 2, 1, 4, 0$: the colors are $c(5) = 1$, $c(3) = 2$, $c(2) = 1$, $c(1) = 3$, $c(4) = 3$, $c(0) = 2$. This uses 3 colors, the size of the largest clique.
- **Cliques.** The sets $\{v\} \cup L(v)$ are $\{0, 1, 2\}$, $\{4, 3, 5\}$, $\{1, 2, 3\}$, $\{2, 3\}$, $\{3, 5\}$ and $\{5\}$. The maximal ones are the three triangles, and they are all the [maximal cliques](/maximal-clique/) of the graph.

**Non-examples.** The cycle $C_n$ for $n \ge 4$ has no PEO: no vertex is simplicial. Trees, [complete graphs](/complete-graph/), interval graphs and split graphs all have one; for a tree, removing leaves one at a time gives a PEO.

## Where it is used

- **Coloring and cliques on chordal graphs.** Greedy coloring in the reverse of a PEO uses exactly $\omega(G)$ colors, because each vertex sees only its earlier-colored later neighbors, which form a clique of size at most $\omega - 1$. The maximal cliques of a chordal graph are among the $n$ sets $\{v\} \cup L(v)$, so there are at most $n$ of them, and a maximum clique and a maximum independent set take $O(n + m)$ time. See [chordal graph coloring](/chordal-graph-coloring/). This is also why chordal graphs are [perfect](/perfect-graph/).
- **Sparse Gaussian elimination.** Eliminating the rows and columns of a sparse symmetric matrix in the order of a PEO of its nonzero pattern creates no fill-in (Rose 1970). In general, the fill-in of an [elimination ordering](/elimination-ordering/) is the set of edges that make the graph chordal, which is the basis of sparse [Cholesky decomposition](/cholesky-decomposition/).
- **Treewidth.** The [treewidth](/treewidth/) of a graph is the least, over all chordal supergraphs $H$, of $\omega(H) - 1$, and a PEO of $H$ gives a [tree decomposition](/tree-decomposition/) whose bags are the sets $\{v\} \cup L(v)$.
- **Probabilistic inference.** Variable elimination and the junction tree algorithm in graphical models triangulate the graph and eliminate along a PEO.

## References
