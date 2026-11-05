---
tag: 83C4SY
kind: definition
slug: line-graph
name: Line graph
aliases:
- edge graph
- interchange graph
area: graphs/graph-representation
level: core
summary: Graph whose vertices are the edges of a graph, adjacent when the edges share an endpoint.
prereqs: [undirected-graph, simple-graph, edge, degree]
see_also: [edge-coloring, chromatic-index, independent-set, de-bruijn-graph, eulerian-circuit, hamiltonian-cycle, graph-isomorphism-problem, complement-graph]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 7.1 (Line graphs and edge-coloring), the definition of the line graph, the count of its edges, and the characterizations of line graphs
  - paper: doi:10.2307/2371086
    title: Hassler Whitney, Congruent graphs and the connectivity of graphs, American Journal of Mathematics 54(1), 1932
    locator: pages 150 to 168, the theorem that connected graphs with isomorphic line graphs are isomorphic, except for the triangle and the claw
  - paper: P. G. H. Lehot, An optimal algorithm to detect a line graph and output its root graph, Journal of the ACM 21(4), 1974
    locator: pages 569 to 575, recognition of a line graph and recovery of its root graph in linear time
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.1 (the line graph L(G) of G)
---

The line graph $L(G)$ of an [undirected](/undirected-graph/) [simple graph](/simple-graph/) $G$ has one [vertex](/vertex/) for each [edge](/edge/) of $G$, and two of these vertices are adjacent when the two edges share an end. It turns questions about edges into questions about vertices: a matching of $G$ is an [independent set](/independent-set/) of $L(G)$, and an [edge coloring](/edge-coloring/) of $G$ is a vertex coloring of $L(G)$. The line graph has $\sum_v \binom{d(v)}{2}$ edges, so it can be much larger than $G$. Whitney proved in 1932 that a connected graph, with one exception, is fixed up to isomorphism by its line graph.

## Definition

Let $G = (V, E)$ be an undirected simple graph, so $E$ is a set of 2-element subsets of $V$. The **line graph** of $G$ is the undirected simple graph

$$L(G) = \big(E,\ \{\{e, f\} : e, f \in E,\ e \ne f,\ e \cap f \ne \emptyset\}\big).$$

Two distinct edges of a simple graph share at most one end, so $e \cap f \ne \emptyset$ means $|e \cap f| = 1$. The graph $G$ is called a **root graph** of $L(G)$. A graph $H$ is a **line graph** if $H \cong L(G)$ for some simple graph $G$.

**Size.** The edges of $G$ at a vertex $v$ are pairwise adjacent in $L(G)$, so they form a clique of $d(v)$ vertices in $L(G)$. Each edge $\{e, f\}$ of $L(G)$ comes from exactly one vertex of $G$, the unique common end of $e$ and $f$. So, with $n = |V|$ and $m = |E|$,

$$|V(L(G))| = m, \qquad |E(L(G))| = \sum_{v \in V} \binom{d(v)}{2}, \qquad d_{L(G)}(\{u, v\}) = d(u) + d(v) - 2.$$

The last equation counts the edges at $u$ other than $\{u, v\}$, and the edges at $v$ other than $\{u, v\}$; no edge is counted twice, because an edge with both ends $u$ and $v$ is $\{u, v\}$ itself.

**Building it.** From an [adjacency list](/adjacency-list/) or an [incidence list](/incidence-list/) of $G$, give the edges the names $0$ to $m - 1$, and for each vertex $v$ output each pair of the edges at $v$. This takes $\Theta(n + m + \sum_v \binom{d(v)}{2})$ time, which is linear in the size of the input and the output. The output can be large: the star $K_{1, n-1}$ has $n - 1$ edges, and its line graph is the complete graph $K_{n-1}$ with $\binom{n-1}{2}$ edges.

**Line digraph.** For a [directed graph](/directed-graph/) $D = (V, A)$, the line digraph $L(D)$ has the vertex set $A$ and an arc from $(u, v)$ to $(v, w)$ for each pair of arcs where the head of the first is the tail of the second. A walk of length $k + 1$ in $D$ is a walk of length $k$ in $L(D)$. The [de Bruijn graph](/de-bruijn-graph/) $B(q, k+1)$ is the line digraph of $B(q, k)$.

## Examples and non-examples

**A small graph.** Let $G$ have the vertices $1, \ldots, 5$ and the edges $a = 12$, $b = 23$, $c = 34$, $d = 13$ and $e = 35$. The degrees are $2, 2, 4, 1, 1$. The four edges $b, c, d, e$ at vertex 3 form a clique $K_4$ in $L(G)$; the edges $a, d$ at vertex 1 give the edge $ad$, and the edges $a, b$ at vertex 2 give the edge $ab$. So $L(G)$ has 5 vertices and the 8 edges $ab, ad, bc, bd, be, cd, ce, de$, and $\binom22 + \binom22 + \binom42 = 1 + 1 + 6 = 8$.

**Standard families.**

| $G$ | $L(G)$ |
|---|---|
| the path $P_n$ with $n \ge 2$ vertices | the path $P_{n-1}$ |
| the cycle $C_n$, $n \ge 3$ | the cycle $C_n$ |
| the star $K_{1, k}$ | the complete graph $K_k$ |
| the triangle $K_3$ | $K_3$ |
| the complete graph $K_4$ | the octahedron $K_{2,2,2}$: 6 vertices, 12 edges, each of degree 4 |
| the complete graph $K_n$ | the triangular graph, $\binom{n}{2}$ vertices, each of degree $2(n-2)$ |
| the complete bipartite graph $K_{p,q}$ | the $p \times q$ rook's graph: cells of a grid, adjacent in the same row or column |
| the Petersen graph, 10 vertices, 3-regular | a 4-regular graph with 15 vertices and 30 edges |

**Two graphs, one line graph.** $L(K_3) = K_3$ and $L(K_{1,3}) = K_3$, but the triangle and the claw $K_{1,3}$ are not isomorphic. Whitney's theorem says that this is the only exception: if $G$ and $G'$ are connected and $L(G) \cong L(G')$, then $G \cong G'$ unless $\{G, G'\} = \{K_3, K_{1,3}\}$.

**A non-example: the claw.** The claw $K_{1,3}$ is not a line graph. *Proof.* Suppose $L(H) \cong K_{1,3}$. The center is an edge $e = \{x, y\}$ of $H$ that shares an end with three edges $f_1, f_2, f_3$, and no two of the $f_i$ share an end. Each $f_i$ contains $x$ or $y$. By the pigeonhole principle, two of the three contain the same one of these two vertices, so these two share an end, and they are adjacent in $L(H)$. This is a contradiction. $\square$ So no line graph has the claw as an [induced subgraph](/induced-subgraph/): in a line graph, the neighbours of each vertex $\{x, y\}$ are covered by two cliques, the edges at $x$ and the edges at $y$. Beineke showed that line graphs are exactly the graphs with none of nine graphs as an induced subgraph, and the claw is one of the nine (West, Section 7.1).

**A non-example: a multigraph.** For a [multigraph](/multigraph/), the definition above does not apply as written: two parallel edges share two ends, and a [self-loop](/self-loop/) is not a 2-element set. Some authors then join two vertices of $L(G)$ by as many edges as the edges of $G$ have common ends. This page uses only simple graphs.

## Related definitions

- **Edge problems become vertex problems.** A matching of $G$ is an [independent set](/independent-set/) of $L(G)$, and a maximum matching of $G$ is a maximum independent set of $L(G)$. A proper edge coloring of $G$ is a proper vertex coloring of $L(G)$, so the [chromatic index](/chromatic-index/) of $G$ is the [chromatic number](/chromatic-number/) of $L(G)$. Matchings can be found in polynomial time while maximum independent set is NP-hard in general, so the line graphs form a class on which independent set is easy.
- **Euler and Hamilton.** If $G$ has an [Eulerian circuit](/eulerian-circuit/), then $L(G)$ has a [Hamiltonian cycle](/hamiltonian-cycle/): consecutive edges of the circuit share an end, so the circuit visits each vertex of $L(G)$ once. The converse is false: $L(K_{1,3}) = K_3$ is Hamiltonian, but the claw has three vertices of odd degree.
- **Recognition.** Lehot gave an algorithm that decides whether a graph $H$ with $n'$ vertices and $m'$ edges is a line graph, and outputs a root graph, in $O(n' + m')$ time. By Whitney's theorem the root graph of a connected line graph other than $K_3$ is unique up to isomorphism.
- **Iterated line graphs.** $L^2(G) = L(L(G))$, and so on. The [de Bruijn graph](/de-bruijn-graph/) is the directed case of this construction.
- **Total graph and intersection graph.** The total graph has both the vertices and the edges of $G$ as its vertices. The line graph is the intersection graph of the edges of $G$, each edge viewed as the set of its two ends.

## References
