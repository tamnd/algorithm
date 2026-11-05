---
tag: BM6DJD
kind: definition
slug: simple-path
name: Simple path
aliases:
- path
- elementary path
area: graphs/paths-and-cycles
level: intro
summary: A walk that visits no vertex more than once.
prereqs: [walk, graph]
see_also: [walk, trail, simple-cycle, hamiltonian-path, longest-path-problem, shortest-path, enumerating-simple-paths, read-tarjan-path-enumeration]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.4 (Graphs), the definitions of path, simple path, reachability and subpath
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 1, Section 1.3 (Paths and cycles), the path as a graph, its length and its ends
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3 (Connected Graphs), Section 3.1, walks, paths and connection
---

A simple path is a [walk](/walk/) that visits no vertex twice. Graph theory books usually call it just a *path*; algorithm books such as CLRS say *simple path*, because they use "path" for a walk. Simple paths are what [shortest-path](/shortest-path/) algorithms return, what a [Hamiltonian path](/hamiltonian-path/) and the [longest path problem](/longest-path-problem/) ask for, and what the enumeration algorithms of this area list. Finding a shortest one is easy, but finding a longest one is NP-hard.

## Definition

Let $G = (V, E)$ be a graph, directed or undirected, possibly a [multigraph](/multigraph/).

**Simple path.** A walk $P = (v_0, e_1, v_1, \ldots, e_k, v_k)$ is a *simple path* of length $k \ge 0$ if its vertices are pairwise distinct: $v_i \ne v_j$ for $0 \le i < j \le k$. It is a $v_0$-$v_k$ path, and $v_1, \ldots, v_{k-1}$ are its *inner* vertices. In a directed graph, each $e_i$ is an arc from $v_{i-1}$ to $v_i$.

**Consequences of the definition.**

- The edges of a simple path are distinct, so a simple path is a [trail](/trail/). For $i < j$, the edge $e_j$ has the end $v_j$, and $v_j$ is neither $v_{i-1}$ nor $v_i$, the ends of $e_i$.
- A simple path contains no [self-loop](/self-loop/), since a loop would repeat its vertex.
- It has $k + 1$ distinct vertices, so $0 \le k \le n - 1$ when $n = |V|$.
- In a multigraph, two paths with the same vertices that use different parallel edges are different. When only the vertices matter, as in most algorithms, a path is the vertex sequence $(v_0, \ldots, v_k)$.

**The path as a graph.** Diestel and Bondy and Murty also call the subgraph with vertices $\{v_0, \ldots, v_k\}$ and edges $\{e_1, \ldots, e_k\}$ a path. In an undirected graph, this subgraph does not record the direction, so $(v_0, \ldots, v_k)$ and its reverse are the same path in that sense. On this site a path is the sequence, unless a page says otherwise.

**Subpaths.** For $0 \le i \le j \le k$, $(v_i, e_{i+1}, \ldots, e_j, v_j)$ is again a simple path. This is what makes the [optimal substructure of shortest paths](/shortest-path-optimal-substructure/) work.

**Walks contain paths.** Each $u$-$v$ walk contains a $u$-$v$ simple path, made of a subsequence of its steps (proof on the [walk](/walk/) page). So "there is a walk" and "there is a path" mean the same, and [reachability](/reachability/) can be defined with either.

**Counting.** The number of simple paths can be exponential in $n$. In the complete graph $K_n$, the number of simple paths with $k$ edges, counted as sequences, is $n(n-1)\cdots(n-k)$ for $0 \le k \le n - 1$, since each new vertex is any vertex not yet used. So listing them needs output-sensitive algorithms, such as [Read-Tarjan path enumeration](/read-tarjan-path-enumeration/).

## Examples and non-examples

Take the undirected graph with vertices $0, 1, 2, 3, 4$ and edges $01, 02, 12, 13, 23, 34$.

- $(0, 1, 3, 4)$ is a simple path of length 3.
- $(0, 1, 2, 3, 4)$ is a simple path of length 4 that visits every vertex: a [Hamiltonian path](/hamiltonian-path/).
- $(0, 1, 2, 0)$ is not a simple path: it repeats 0. It is a [simple cycle](/simple-cycle/).
- $(0, 1, 3, 2, 1)$ is a walk and a trail, but not a simple path: it repeats 1.
- $(3)$ is a simple path of length 0.

The simple paths from 0 to 4 are $(0, 1, 3, 4)$, $(0, 2, 3, 4)$, $(0, 1, 2, 3, 4)$ and $(0, 2, 1, 3, 4)$: four in all, two of length 3 and two of length 4. A shortest one has length 3, a longest one length 4.

**Directed.** In the directed graph with arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, the only simple path from 0 to 2 is $(0, 1, 2)$. There is no simple path from 1 to 1 except the trivial one $(1)$.

**Complete graph.** $K_4$ has $4$ simple paths of length 0, $12$ of length 1, $24$ of length 2 and $24$ of length 3, as sequences. Counted without direction, the paths of length at least 1 are $6 + 12 + 12 = 30$.

**Multigraph.** If $u$ and $v$ are joined by two parallel edges $a$ and $b$, then $(u, a, v)$ and $(u, b, v)$ are two different simple paths, with the same vertex sequence.

## Related definitions

- **Walk and trail.** A simple path is a walk with no repeated vertex, and so a trail. See [walk](/walk/) and [trail](/trail/).
- **Simple cycle.** A closed walk in which only the first and last vertices are equal. See [simple cycle](/simple-cycle/). Adding an edge from $v_k$ back to $v_0$ to a simple path of length at least 2 in a simple graph makes a simple cycle.
- **Hamiltonian path.** A simple path that contains every vertex. See [Hamiltonian path](/hamiltonian-path/).
- **Shortest and longest paths.** See [shortest path](/shortest-path/) and the [longest path problem](/longest-path-problem/).
- **Disjoint paths.** Paths with no common inner vertex, or no common edge, appear in [Menger's theorem](/menger-theorem/) and in [vertex-disjoint paths](/vertex-disjoint-paths/).

## References
