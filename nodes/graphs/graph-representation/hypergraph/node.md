---
tag: WE18V0
kind: definition
slug: hypergraph
name: Hypergraph
aliases:
- set system
area: graphs/graph-representation
level: core
summary: Generalisation of a graph in which an edge may join any number of vertices.
prereqs: [graph, edge, bipartite-graph]
see_also: [incidence-matrix, bipartite-graph, hitting-set, set-cover, exact-cover, vertex-cover, hyperclique, sat]
sources:
  - book: isbn:9780444874894
    title: Claude Berge, Hypergraphs, Combinatorics of Finite Sets, North-Holland Mathematical Library 45, 1989
    locator: Chapter 1 (General concepts), the definitions of a hypergraph, its rank, its dual, its incidence matrix, its representative graph, transversals and matchings
  - book: isbn:9783319000794
    title: Alain Bretto, Hypergraph Theory, An Introduction, Springer, 2013
    locator: Chapter 1 (Hypergraphs, basic concepts), the definitions of uniform hypergraphs, the dual, the 2-section and the incidence graph
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: the exercises of Appendix B.4 (Graphs), the definition of a hypergraph and of its bipartite incidence graph
---

A hypergraph is a pair $H = (V, E)$ of a finite set $V$ of vertices and a family $E$ of nonempty subsets of $V$, called hyperedges, so an [edge](/edge/) may join any number of vertices instead of exactly two. A [graph](/graph/) is the case where each hyperedge has exactly two vertices. Hypergraphs model relations of many objects at once: the clauses of a formula, the nets of a circuit, the tables of a database and the sets of a [set cover](/set-cover/) instance. They are stored as incidence lists, as an [incidence matrix](/incidence-matrix/), or as a [bipartite](/bipartite-graph/) incidence graph, and many graph algorithms run on that bipartite graph.

## Definition

A **hypergraph** is a pair $H = (V, E)$ where $V$ is a finite set and $E = (e_1, \ldots, e_m)$ is a finite family of nonempty subsets of $V$. The elements of $V$ are the *vertices*, the sets $e_j$ are the *hyperedges* or simply *edges*, and we write $n = |V|$ and $m = |E|$. The definition has these conventions:

- **Family, not set.** $E$ may list the same subset twice. If it does not, $H$ is *simple* in the sense of having no repeated edges. Some authors also call $H$ simple only when no edge contains another; such a hypergraph is a *Sperner family* or *clutter*.
- **Nonempty edges.** Most authors forbid the empty edge, and Berge also asks that each vertex be in some edge. We allow isolated vertices.
- **Undirected and unweighted.** An edge is an unordered set, and it has no weight. A *weighted* hypergraph adds a function $w : E \to \mathbb{R}$. A *directed* hypergraph, used for Horn formulas and some network models, gives each edge a tail set and a head set; it is a different object.

**Measures.**

- The **size** of the hypergraph is $p = \sum_{e \in E} |e|$, the number of pairs $(v, e)$ with $v \in e$. This is the input length of most algorithms on $H$.
- The **degree** $d(v)$ is the number of edges that contain $v$. Counting the incidence pairs $(v, e)$ in two ways gives the hypergraph form of the [handshake lemma](/handshake-lemma/): $\sum_{v \in V} d(v) = \sum_{e \in E} |e| = p$.
- The **rank** is $\max_e |e|$. $H$ is **$k$-uniform** when $|e| = k$ for each edge. A simple graph without loops is a 2-uniform hypergraph without repeated edges, and a graph with loops allows edges of size 1 too.

**Derived objects.**

- The **incidence matrix** is the $n \times m$ 0-1 matrix $M$ with $M_{v j} = 1$ when $v \in e_j$. It has exactly $p$ ones.
- The **incidence graph** (or *Levi graph*) is the bipartite graph $B(H)$ with the parts $V$ and $E$ and an edge $\{v, e\}$ for each $v \in e$. It has $n + m$ vertices and $p$ edges, and $M$ is its biadjacency matrix. The map $H \mapsto B(H)$ is a bijection between hypergraphs on $V$ and bipartite graphs with one part $V$ and no isolated vertex in the other part, so each hypergraph is a bipartite graph with a chosen side.
- The **dual** $H^*$ has a vertex for each edge of $H$ and an edge $\{e : v \in e\}$ for each vertex $v$ of $H$ with $d(v) \ge 1$. Its incidence matrix is $M^{\mathsf{T}}$, so $(H^*)^* = H$ when $H$ has no isolated vertex.
- The **2-section** (also *primal graph*, or *clique expansion*) is the simple graph on $V$ with an edge $\{u, v\}$ when $u \ne v$ lie in a common edge of $H$. It replaces each edge by a clique and loses information: the triangle $\{1,2\},\{2,3\},\{1,3\}$ and the single edge $\{1, 2, 3\}$ have the same 2-section.
- A **transversal** or *hitting set* is a set $T \subseteq V$ that meets each edge; the least size is $\tau(H)$. A **matching** is a set of pairwise disjoint edges; the largest size is $\nu(H)$. Each edge of a matching needs its own vertex of $T$, so $\nu(H) \le \tau(H)$.

**Representations and their costs.** With $n$ vertices, $m$ edges and size $p$:

| representation | space | list the vertices of $e$ | list the edges at $v$ | test $v \in e$ |
|---|---|---|---|---|
| edge lists (each $e$ as an array of vertices) | $\Theta(m + p)$ | $\Theta(\lvert e \rvert)$ | $\Theta(p)$ | $O(\lvert e \rvert)$, or $O(\log \lvert e \rvert)$ if sorted |
| edge lists plus vertex lists (both sides of $B(H)$) | $\Theta(n + m + p)$ | $\Theta(\lvert e \rvert)$ | $\Theta(d(v))$ | $O(\min(\lvert e \rvert, d(v)))$ |
| incidence matrix, one bit per cell | $\Theta(nm)$ bits | $\Theta(n)$ | $\Theta(m)$ | $O(1)$ |
| 2-section as an adjacency list | $O(n + \sum_e \lvert e \rvert^2)$ | lost | lost | lost |

The second row is the [adjacency list](/adjacency-list/) of the incidence graph, and it is the usual choice: [breadth-first search](/breadth-first-search/) on $B(H)$ visits all of $H$ in $\Theta(n + m + p)$ time, and two vertices of $H$ are in the same connected component of $H$ exactly when they are in the same component of $B(H)$. A [compressed sparse row](/compressed-sparse-row/) array for each side gives the same bounds in $n + m + 2p + 2$ words.

## Examples and non-examples

**A worked example.** Let $V = \{0, \ldots, 5\}$ and

$$e_1 = \{0, 1, 2\}, \quad e_2 = \{1, 3\}, \quad e_3 = \{2, 3, 4, 5\}, \quad e_4 = \{5\}.$$

Then $n = 6$, $m = 4$, the rank is 4 and $H$ is not uniform. The size is $p = 3 + 2 + 4 + 1 = 10$, and the degrees $d(0), \ldots, d(5)$ are $1, 2, 2, 2, 1, 2$, which also sum to 10. The incidence matrix is

| | $e_1$ | $e_2$ | $e_3$ | $e_4$ |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 1 | 0 | 0 |
| 2 | 1 | 0 | 1 | 0 |
| 3 | 0 | 1 | 1 | 0 |
| 4 | 0 | 0 | 1 | 0 |
| 5 | 0 | 0 | 1 | 1 |

- The incidence graph has $6 + 4 = 10$ vertices and 10 edges.
- The dual has the vertices $e_1, \ldots, e_4$ and the edges $\{e_1\}$, $\{e_1, e_2\}$, $\{e_1, e_3\}$, $\{e_2, e_3\}$, $\{e_3\}$, $\{e_3, e_4\}$, one for each of the vertices $0, \ldots, 5$.
- The 2-section has the edges $01, 02, 12$ from $e_1$, $13$ from $e_2$, and $23, 24, 25, 34, 35, 45$ from $e_3$, so 10 edges; the edge $e_4$ gives none.
- The set $\{1, 5\}$ is a transversal: 1 meets $e_1$ and $e_2$, and 5 meets $e_3$ and $e_4$. No single vertex meets both $e_1$ and $e_4$, so $\tau(H) = 2$.
- $\{e_1, e_4\}$ is a matching. Each two of $e_1, e_2, e_3$ share a vertex, so no matching has three edges, and $\nu(H) = 2$.

**More examples.**

- **Graphs.** Each simple graph is a 2-uniform hypergraph, and each [multigraph](/multigraph/) is a hypergraph with edges of size 2 that may repeat.
- **The Fano plane.** The 7 points $\{0, \ldots, 6\}$ and the 7 lines $\{i, i+1, i+3\} \bmod 7$, that is $013, 124, 235, 346, 450, 561, 602$. It is 3-uniform, each vertex has degree 3, and each two points lie on exactly one line. It cannot be 2-colored so that no edge is all one color, and no 3-uniform hypergraph with fewer edges has this property.
- **Formulas.** A CNF formula of [SAT](/sat/) gives a hypergraph on its variables with one edge per clause. A $k$-[SAT](/k-sat/) formula with $k$ distinct variables per clause gives a $k$-uniform one.
- **Covering problems.** An instance of [set cover](/set-cover/), [hitting set](/hitting-set/) or [exact cover](/exact-cover/) is a hypergraph. Hitting set asks for $\tau(H)$, and [vertex cover](/vertex-cover/) is hitting set on a 2-uniform hypergraph.
- **Circuits and databases.** A net of a circuit joins all the pins on one wire, and a database schema joins the attributes of each table.
- **Complete $k$-uniform hypergraph.** $K_n^{(k)}$ has all $\binom{n}{k}$ subsets of size $k$ as edges; its size is $p = k \binom{n}{k}$.

**Non-examples.**

- A directed graph is not a hypergraph in this sense, since its edges are ordered pairs. Its underlying undirected graph is.
- A relation of ordered tuples, such as the rows $(a, b, c)$ of a table, is not a hypergraph, since $\{a, b, c\}$ forgets the order and the positions.
- The 2-section of $H$ is not a representation of $H$: different hypergraphs have the same 2-section.

## Related definitions

- [Graph](/graph/) and [edge](/edge/): the 2-uniform case.
- [Bipartite graph](/bipartite-graph/) and [incidence matrix](/incidence-matrix/): the incidence graph and its matrix store $H$.
- [Hitting set](/hitting-set/), [set cover](/set-cover/) and [exact cover](/exact-cover/): the transversal, the cover and the perfect matching of the dual.
- [Hyperclique](/hyperclique/): a clique in a uniform hypergraph.
- [Matroid](/matroid/): a hypergraph of independent sets with the exchange property.

## References
