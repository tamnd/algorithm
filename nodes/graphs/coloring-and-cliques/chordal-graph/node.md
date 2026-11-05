---
tag: WE2K34
kind: definition
slug: chordal-graph
name: Chordal graph
aliases:
- triangulated graph
area: graphs/coloring-and-cliques
level: core
summary: A graph in which every cycle of length four or more has a chord.
prereqs: [undirected-graph, induced-subgraph, clique]
see_also: [perfect-elimination-ordering, chordal-graph-coloring, lexicographic-bfs, maximum-cardinality-search, perfect-graph, tree-decomposition, treewidth, interval-partitioning]
sources:
  - book: isbn:9780444515308
    title: Martin Charles Golumbic, Algorithmic Graph Theory and Perfect Graphs, second edition, Annals of Discrete Mathematics 57, Elsevier, 2004
    locator: Chapter 4, Triangulated graphs (simplicial vertices, perfect elimination orderings, minimal separators, and the subtree characterization)
  - paper: doi:10.1007/BF02992776
    title: G. A. Dirac, On rigid circuit graphs, Abhandlungen aus dem Mathematischen Seminar der Universität Hamburg 25, 71 to 76 (1961)
    locator: the whole paper (minimal separators are cliques, and every chordal graph that is not complete has two non-adjacent simplicial vertices)
  - paper: doi:10.2140/pjm.1965.15.835
    title: D. R. Fulkerson and O. A. Gross, Incidence matrices and interval graphs, Pacific Journal of Mathematics 15(3), 835 to 855 (1965)
    locator: the characterization of chordal graphs by perfect elimination orderings
  - paper: doi:10.1016/0095-8956(74)90094-X
    title: Fănică Gavril, The intersection graphs of subtrees in trees are exactly the chordal graphs, Journal of Combinatorial Theory, Series B 16(1), 47 to 56 (1974)
    locator: the main theorem
  - paper: doi:10.1137/0205021
    title: Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 266 to 283 (1976)
    locator: lexicographic breadth-first search and the linear-time recognition of chordal graphs
---

A chordal graph is an undirected [graph](/graph/) in which every cycle of length at least 4 has a *chord*, an edge between two vertices of the cycle that are not consecutive on it. Equivalently, it has no [induced](/induced-subgraph/) cycle of length 4 or more. Chordal graphs are exactly the graphs with a [perfect elimination ordering](/perfect-elimination-ordering/), and exactly the intersection graphs of subtrees of a tree. They are [perfect](/perfect-graph/), they can be recognized in linear time, and problems that are NP-hard in general, such as [coloring](/chordal-graph-coloring/) and maximum clique, are solved on them in linear time.

## Definition

Let $G = (V, E)$ be a finite simple undirected graph. A *chord* of a cycle $C = u_1 u_2 \cdots u_k u_1$ in $G$ is an edge $u_i u_j \in E$ with $u_i, u_j$ on $C$ and not consecutive on $C$.

**Definition.** $G$ is **chordal** if every cycle of $G$ of length at least 4 has a chord. Equivalently, for no $k \ge 4$ does $G$ contain the cycle $C_k$ as an induced subgraph. The older names are *triangulated* graph and *rigid circuit* graph.

The two forms agree: a cycle without a chord is exactly an induced cycle, because the subgraph induced by its vertices then has no edges besides those of the cycle.

A vertex $v$ is **simplicial** if its neighbors form a [clique](/clique/). An order $v_1, \ldots, v_n$ of $V$ is a **perfect elimination ordering** if each $v_i$ is simplicial in $G[\{v_i, \ldots, v_n\}]$, that is, its later neighbors form a clique.

**Characterizations.** For a graph $G$, the following are equivalent:

1. $G$ is chordal.
2. Every minimal vertex separator of $G$ (a minimal set $S$ whose removal puts two given vertices $a, b$ in different components) is a clique (Dirac 1961).
3. Every induced subgraph of $G$ has a simplicial vertex; if it is not complete, it has two non-adjacent ones (Dirac 1961).
4. $G$ has a perfect elimination ordering (Fulkerson and Gross 1965).
5. $G$ is the intersection graph of a family of subtrees of a tree: there is a tree $T$ and subtrees $T_v$ with $uv \in E$ exactly when $T_u$ and $T_v$ share a node (Gavril 1974; also Buneman and Walter). The tree can be chosen with the maximal cliques of $G$ as its nodes, a *clique tree*.

Chordality is *hereditary*: every induced subgraph of a chordal graph is chordal, since an induced cycle of the subgraph is an induced cycle of $G$.

## Examples and non-examples

Take the graph $G$ on the vertices $0, \ldots, 5$ with the 9 edges $01, 02, 12, 13, 23, 24, 34, 35, 45$, a strip of 4 triangles $\{0,1,2\}$, $\{1,2,3\}$, $\{2,3,4\}$, $\{3,4,5\}$.

- $G$ is chordal. The order $0, 1, 2, 3, 4, 5$ is a perfect elimination ordering: the later neighbors of $0, 1, 2, 3, 4$ are $\{1, 2\}$, $\{2, 3\}$, $\{3, 4\}$, $\{4, 5\}$ and $\{5\}$, and each is a clique. Vertices 0 and 5 are its two non-adjacent simplicial vertices.
- The 4-cycle $1, 3, 4, 2$ of $G$ has the chord $23$. Its minimal separator between 0 and 5, $\{2, 3\}$, is a clique.
- **Non-example.** Add a vertex 6 and the edges $06$ and $56$. The cycle $0, 2, 4, 5, 6$ has length 5, and none of the pairs $04$, $05$, $25$, $26$, $46$ is an edge, so it is an induced $C_5$. The new graph is not chordal.
- **Non-example.** $C_4$ is the smallest graph that is not chordal. Each cycle $C_k$ with $k \ge 4$ fails, while $C_3 = K_3$ is chordal.
- **Non-example.** A bipartite graph is chordal exactly when it is a forest: a shortest cycle of a graph is always induced, and in a bipartite graph it has length at least 4.

Other chordal graphs:

- Every forest: it has no cycles at all.
- Every complete graph $K_n$.
- Interval graphs, the intersection graphs of intervals on a line: intervals are subtrees of a path. See [interval partitioning](/interval-partitioning/).
- $k$-trees, built from $K_{k+1}$ by adding vertices adjacent to a $k$-clique; the strip $G$ above is a 2-tree.
- Split graphs, whose vertices split into a clique and an independent set.

## Related definitions

- [Perfect elimination ordering](/perfect-elimination-ordering/): the order of characterization 4. [Lexicographic BFS](/lexicographic-bfs/) and [maximum cardinality search](/maximum-cardinality-search/) find one in $O(n + m)$ time if $G$ is chordal, and a linear-time check of the order then decides chordality (Rose, Tarjan and Lueker 1976; Tarjan and Yannakakis 1984).
- [Perfect graph](/perfect-graph/): chordal graphs are perfect, so $\chi(H) = \omega(H)$ for every induced subgraph $H$. Greedy coloring in reverse perfect elimination order is optimal; see [coloring chordal graphs](/chordal-graph-coloring/).
- **Maximal cliques.** A chordal graph has at most $n$ maximal cliques, each of the form $\{v_i\} \cup$ (later neighbors of $v_i$) in a perfect elimination ordering. So maximum clique, and by perfectness maximum independent set and minimum [clique cover](/clique-cover/), are polynomial.
- [Tree decomposition](/tree-decomposition/) and [treewidth](/treewidth/): a clique tree of a chordal graph is a tree decomposition whose bags are the maximal cliques, so the treewidth is $\omega(G) - 1$. The treewidth of any graph is the least $\omega(H) - 1$ over chordal supergraphs $H$ (*triangulations*) of it.
- **Chordal bipartite and strongly chordal graphs** are related classes with stronger or weaker conditions on cycles.

## References
