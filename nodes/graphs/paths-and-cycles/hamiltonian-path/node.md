---
tag: VYEN0Y
kind: definition
slug: hamiltonian-path
name: Hamiltonian path
aliases:
- Hamilton path
- traceable graph
area: graphs/paths-and-cycles
level: intro
summary: A simple path that visits every vertex exactly once.
prereqs: [simple-path, graph]
see_also: [hamiltonian-cycle, hamiltonian-path-problem, eulerian-path, longest-path-problem, held-karp-algorithm, knights-tour-problem, gray-code, minimum-path-cover-problem]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 18 (Hamilton Cycles), Hamilton paths and cycles, and the necessary condition on the number of components after deleting a set of vertices
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 7.2 (Hamiltonian cycles), spanning paths and cycles and their necessary conditions
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 10 (Hamilton cycles)
  - paper: László Rédei, Ein kombinatorischer Satz, Acta Litterarum ac Scientiarum Szeged 7, 39 to 43 (1934)
    title: Rédei, every tournament has a Hamiltonian path
    locator: the main theorem
---

A Hamiltonian path is a [simple path](/simple-path/) that visits every vertex of a graph exactly once. A graph that has one is called *traceable*. It is the vertex analogue of an [Eulerian path](/eulerian-path/), which uses every edge once, but the two behave very differently: an Eulerian path is decided by degrees in linear time, while deciding whether a Hamiltonian path exists is the NP-complete [Hamiltonian path problem](/hamiltonian-path-problem/). A Hamiltonian path that can be closed by one more edge gives a [Hamiltonian cycle](/hamiltonian-cycle/).

## Definition

Let $G = (V, E)$ be a graph with $n = |V| \ge 1$ vertices, directed or undirected, possibly a [multigraph](/multigraph/).

**Hamiltonian path.** A *Hamiltonian path* of $G$ is a simple path $P = (v_1, v_2, \ldots, v_n)$ that contains every vertex of $V$, each exactly once. Equivalently, $(v_1, \ldots, v_n)$ is an ordering of $V$ such that $v_i$ and $v_{i+1}$ are adjacent for each $i$ with $1 \le i \le n - 1$; in a directed graph, the arc must go from $v_i$ to $v_{i+1}$. Its length is $n - 1$. $G$ is *traceable* if it has a Hamiltonian path. A *Hamiltonian $u$-$v$ path* is one with $v_1 = u$ and $v_n = v$.

**Multigraphs.** A simple path uses no [self-loop](/self-loop/), and it uses at most one of the parallel edges between two vertices. So a multigraph is traceable exactly when its underlying simple graph is. Loops and parallel edges never matter here, except when the paths are counted with their edges.

**Small cases.** The graph with one vertex is traceable, by the path $(v_1)$ of length 0. For the graph with no vertex, the convention varies; this site does not use it.

**Necessary conditions.** Let $G$ be undirected with $n \ge 2$ and traceable by $P$.

1. $G$ is [connected](/connected-graph/), because $P$ connects every pair of vertices.
2. $G$ has no vertex of degree 0, and at most two vertices of degree 1. A vertex of degree 1 in $G$ has degree at most 1 on $P$, so it is an end of $P$, and $P$ has two ends.
3. For every set $S \subseteq V$, the graph $G - S$ has at most $|S| + 1$ connected components. Deleting the $|S|$ vertices of $S$ from the path $P$ cuts it into at most $|S| + 1$ pieces, each piece is connected, and every vertex of $G - S$ is in one of them.

None of these conditions is sufficient. For a directed graph, condition 1 becomes: some vertex reaches every other vertex (the first vertex of the path), and the [condensation](/condensation-graph/) of $G$ must itself have a Hamiltonian path, since $P$ visits the strongly connected components one after another; for an acyclic graph this means that the topological ordering is unique.

**Path and cycle.** $G$ has a Hamiltonian path if and only if the graph $G^+$, made from $G$ by adding a new vertex $z$ joined to every vertex (in both directions, if directed), has a [Hamiltonian cycle](/hamiltonian-cycle/). A Hamiltonian path $(v_1, \ldots, v_n)$ gives the cycle $(z, v_1, \ldots, v_n, z)$, and deleting $z$ from a Hamiltonian cycle of $G^+$ leaves a Hamiltonian path of $G$.

**Tournaments.** A *tournament* is a directed graph with exactly one arc between each pair of distinct vertices. Every tournament has a Hamiltonian path (Rédei, 1934). *Proof* by induction on $n$. For $n = 1$ the path is $(v_1)$. For $n \ge 2$, take any vertex $x$, and a Hamiltonian path $(v_1, \ldots, v_{n-1})$ of the tournament without $x$. If $x \to v_1$, put $x$ first. Otherwise $v_1 \to x$. If $v_{n-1} \to x$, put $x$ last. Otherwise $x \to v_{n-1}$, and then there is a first index $j$ with $x \to v_j$, where $2 \le j \le n - 1$. Then $v_{j-1} \to x$, and $(v_1, \ldots, v_{j-1}, x, v_j, \ldots, v_{n-1})$ is a Hamiltonian path. $\square$ With binary search for the index $j$ (keep two positions $lo < hi$ with $v_{lo} \to x$ and $x \to v_{hi}$, and halve the gap), each insertion asks $O(\log n)$ arc queries, so a Hamiltonian path of a tournament is found with $O(n \log n)$ queries. This is binary insertion sort with a comparison that need not be transitive.

## Examples and non-examples

**Complete graphs.** In $K_n$ every ordering of the vertices is a Hamiltonian path, so there are $n!$ of them as sequences and $n!/2$ as undirected paths, for $n \ge 2$. For $n = 4$ that is 12, for $n = 6$ it is 360.

**The Petersen graph.** It has 120 Hamiltonian paths (each counted once, without direction) and no Hamiltonian cycle. So traceable does not imply Hamiltonian.

**The cube.** The 3-dimensional cube $Q_3$ has 72 Hamiltonian paths and 6 Hamiltonian cycles. A [Gray code](/gray-code/) is a Hamiltonian path of the cube $Q_d$: it lists all $d$-bit strings so that neighbours differ in one bit.

**A path graph.** The path $1 - 2 - 3 - 4$ is its own Hamiltonian path, and it has no Hamiltonian cycle.

**Non-examples.**

- The star $K_{1,3}$ with centre 0 and leaves 1, 2, 3 has three vertices of degree 1, so it has no Hamiltonian path (condition 2).
- Two disjoint edges $\{1, 2\}$ and $\{3, 4\}$: the graph is not connected.
- The complete bipartite graph $K_{2,4}$: deleting the 2 vertices of the small side leaves 4 isolated vertices, more than $2 + 1$, so condition 3 fails.
- A graph with an isolated vertex and $n \ge 2$ has no Hamiltonian path, even if the other vertices form a complete graph.
- The directed graph with arcs $1 \to 2$ and $3 \to 2$ has no Hamiltonian path: both 1 and 3 have no incoming arc, and only the first vertex of the path can lack one.

**Knight's tour.** An open [knight's tour](/knights-tour-problem/) of a chessboard is a Hamiltonian path of the knight's graph, whose vertices are the squares and whose edges are the knight's moves.

## Related definitions

- **Hamiltonian cycle.** A cycle through every vertex; see [Hamiltonian cycle](/hamiltonian-cycle/). Every Hamiltonian graph with $n \ge 2$ is traceable: delete one edge of the cycle.
- **Eulerian path.** A trail through every edge; see [Eulerian path](/eulerian-path/).
- **Path cover.** A set of vertex-disjoint paths that covers all vertices. A Hamiltonian path is a path cover with one path; see the [minimum path cover problem](/minimum-path-cover-problem/).
- **Longest path.** A Hamiltonian path is a simple path of the largest possible length $n - 1$; see the [longest path problem](/longest-path-problem/).
- **Deciding and finding.** See the [Hamiltonian path problem](/hamiltonian-path-problem/) and the dynamic program of [Held and Karp](/held-karp-algorithm/).

## References
