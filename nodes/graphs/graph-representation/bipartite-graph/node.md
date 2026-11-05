---
tag: APQ4NP
kind: definition
slug: bipartite-graph
name: Bipartite graph
area: graphs/graph-representation
level: intro
summary: A graph whose vertices split into two sets so that every edge joins a vertex of one set to a vertex of the other.
prereqs: [graph, acyclic-graph]
see_also: [bipartite-odd-cycle-theorem, bipartiteness-testing, bipartite-matching, konig-theorem, hall-theorem, complete-graph, graph-coloring, hypergraph]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.6 (Bipartite graphs), the proposition that a graph is bipartite if and only if it contains no odd cycle
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 3, Section 3.4 (Testing bipartiteness, an application of breadth-first search)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 1.2 (König's theorem that a graph is bipartite if and only if it has no odd cycle)
---

A bipartite graph is an undirected [graph](/graph/) whose vertex set splits into two disjoint parts such that each [edge](/edge/) has one end in each part. Equivalently, its vertices can be colored with two colors so that no edge joins two vertices of the same color. A graph is bipartite exactly when it has no cycle of odd length, and [breadth-first search](/breadth-first-search/) decides this in $O(n + m)$ time. Bipartite graphs model two kinds of objects and the relation between them, such as workers and jobs, and they are the setting of [bipartite matching](/bipartite-matching/).

## Definition

A simple undirected graph $G = (V, E)$ is **bipartite** when there are sets $A, B$ with

$$V = A \cup B, \qquad A \cap B = \emptyset, \qquad \text{each } \{u, v\} \in E \text{ has } |\{u, v\} \cap A| = 1.$$

The pair $(A, B)$ is a *bipartition*, and $A$ and $B$ are the *parts* or *sides*. One part may be empty, so a graph with no edges is bipartite. We often write $G = (A, B, E)$ when the bipartition is part of the input.

**As a coloring.** $G$ is bipartite if and only if it has a proper 2-coloring $c : V \to \{0, 1\}$, one with $c(u) \ne c(v)$ for each edge $\{u, v\}$: take $A = c^{-1}(0)$ and $B = c^{-1}(1)$. So $G$ is bipartite exactly when its [chromatic number](/chromatic-number/) is at most 2.

**Uniqueness.** If $G$ is connected and bipartite, the bipartition is unique up to swapping $A$ and $B$. Fix a vertex $s$ in $A$; then each vertex $v$ must be in $A$ when its distance from $s$ is even and in $B$ when it is odd, because the parts alternate along each path. A graph with $c$ components that is bipartite has exactly $2^{c-1}$ bipartitions as unordered pairs $\{A, B\}$.

**Theorem (König).** A graph is bipartite if and only if it contains no cycle of odd length.

*Proof.* If $(A, B)$ is a bipartition, the vertices of each cycle alternate between $A$ and $B$, so a closed walk returns to its start only after an even number of steps. So each cycle has even length.

Conversely, let $G$ have no odd cycle. It is enough to treat each component, so let $G$ be connected, pick a vertex $s$, and let $A$ be the vertices at even distance from $s$ and $B$ the vertices at odd distance. Suppose an edge $\{u, v\}$ had both ends in the same part, so $\operatorname{dist}(s, u) \equiv \operatorname{dist}(s, v) \pmod 2$. Take shortest paths $P$ from $s$ to $u$ and $Q$ from $s$ to $v$, and let $x$ be the last vertex of $P$ that is also on $Q$. Since $P$ and $Q$ are shortest paths, $x$ has the same distance $k$ from $s$ along both. The part of $P$ from $x$ to $u$, the edge $\{u, v\}$ and the part of $Q$ from $v$ back to $x$ form a cycle of length

$$(\operatorname{dist}(s, u) - k) + 1 + (\operatorname{dist}(s, v) - k),$$

which is odd because the two distances have the same parity. This is a contradiction. $\blacksquare$

The page [bipartite odd cycle theorem](/bipartite-odd-cycle-theorem/) has the theorem in more detail. The proof is also the algorithm: a [BFS](/breadth-first-search/) from each unvisited vertex colors the vertices by the parity of their level, and the graph is bipartite exactly when no edge joins two vertices of the same level parity. See [bipartiteness testing](/bipartiteness-testing/).

**The most edges.** A bipartite graph with parts of sizes $p$ and $q$ has at most $pq$ edges, and $pq \le \lfloor n^2/4 \rfloor$ for $p + q = n$. The complete bipartite graph $K_{\lfloor n/2 \rfloor, \lceil n/2 \rceil}$ meets this bound.

**Directed and multigraph forms.** A directed graph or a multigraph is bipartite when its underlying undirected graph is, so each edge goes between the parts in either direction. A loop is never allowed, since its two ends are the same vertex.

**Biadjacency matrix.** For $G = (A, B, E)$ with $A = \{a_1, \ldots, a_p\}$ and $B = \{b_1, \ldots, b_q\}$, the *biadjacency matrix* is the $p \times q$ matrix $M$ with $M_{ij} = 1$ when $\{a_i, b_j\} \in E$. The [adjacency matrix](/adjacency-matrix/) of $G$ in the order $a_1, \ldots, a_p, b_1, \ldots, b_q$ is

$$\begin{pmatrix} 0 & M \\ M^{\mathsf{T}} & 0 \end{pmatrix},$$

so $M$ stores the same graph in $pq$ cells instead of $(p+q)^2$.

## Examples and non-examples

**A worked example.** Workers $A = \{x, y, z\}$ and jobs $B = \{1, 2, 3, 4\}$, with the edges $x1, x2, y2, y3, z3, z4$. Each edge joins a worker to a job, so the graph is bipartite, with $m = 6 \le 3 \cdot 4 = 12$. Its biadjacency matrix is

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| $x$ | 1 | 1 | 0 | 0 |
| $y$ | 0 | 1 | 1 | 0 |
| $z$ | 0 | 0 | 1 | 1 |

The matching $x1, y2, z3$ assigns a job to each worker.

**A BFS trace.** Take the cycle $C_6$ on $0, \ldots, 5$ with the edges $\{i, i+1 \bmod 6\}$. A BFS from 0 gives the levels $0: \{0\}$, $1: \{1, 5\}$, $2: \{2, 4\}$, $3: \{3\}$. The parts are $A = \{0, 2, 4\}$ and $B = \{1, 3, 5\}$, and each edge joins an even level to an odd one. So $C_6$ is bipartite. On $C_5$ the BFS from 0 gives the levels $\{0\}$, $\{1, 4\}$, $\{2, 3\}$, and the edge $\{2, 3\}$ joins two vertices of level 2. So $C_5$ is not bipartite, and $0, 1, 2, 3, 4$ is its odd cycle.

**More examples.**

- Each [tree](/tree/) and each forest, since they have no cycles at all.
- Each even cycle $C_{2k}$.
- Grid graphs: color the cell $(i, j)$ by the parity of $i + j$.
- The hypercube $Q_d$ on the bit strings of length $d$, with edges between strings that differ in one bit: color a string by the parity of its number of 1 bits.
- The graph of a [hypergraph](/hypergraph/) $H = (V, F)$, with the vertices $V \cup F$ and an edge $\{v, f\}$ when $v \in f$. This is the *incidence graph*, and it is bipartite by its construction.

**Non-examples.**

- Each odd cycle $C_{2k+1}$, in particular the triangle $K_3$.
- $K_n$ for $n \ge 3$, since it contains a triangle.
- The Petersen graph, which contains a cycle of length 5.

**The cost of the test.** With $n$ vertices and $m$ edges, a BFS 2-coloring takes $\Theta(n + m)$ time on an [adjacency list](/adjacency-list/) and $\Theta(n^2)$ on an [adjacency matrix](/adjacency-matrix/). When the graph is not bipartite, the same search returns an odd cycle in the same time bound.

## Related definitions

- [Bipartite odd cycle theorem](/bipartite-odd-cycle-theorem/): the theorem of this page.
- [Bipartiteness testing](/bipartiteness-testing/) and [bipartite graph test](/bipartite-graph-test/): the algorithms.
- [Bipartite matching](/bipartite-matching/), [Hall's theorem](/hall-theorem/), [König's theorem](/konig-theorem/) on matchings and covers, and [Hopcroft-Karp](/hopcroft-karp/).
- [Graph coloring](/graph-coloring/) and [chromatic number](/chromatic-number/): bipartite means 2-colorable.
- [Complete graph](/complete-graph/) and the complete bipartite graph $K_{p,q}$.

## References
