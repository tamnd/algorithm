---
tag: 93790T
kind: definition
slug: eulerian-path
name: Eulerian path
aliases:
- Euler trail
area: graphs/paths-and-cycles
level: intro
summary: A trail that uses every edge of the graph exactly once.
prereqs: [trail, walk, graph]
see_also: [eulerian-circuit, eulerian-graph, eulers-theorem-eulerian-graphs, eulerian-path-problem, hierholzer-algorithm, fleury-algorithm, hamiltonian-path, chinese-postman-problem]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.8, Euler tours (the definition of an Euler tour and Theorem 1.8.1)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3, Connected graphs, Section 3.3, Euler tours (Euler trails and Euler tours in graphs with loops and parallel edges)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-3, Euler tour (the directed case)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer, 2020
    locator: Section 18.7, Eulerian Cycle/Chinese Postman
---

An Eulerian path, or Euler trail, is a [trail](/trail/) that uses every edge of a [graph](/graph/) exactly once. It may end where it starts, and then it is an [Eulerian circuit](/eulerian-circuit/), or it may end at another vertex. The definition works the same way for [directed and undirected graphs](/directed-and-undirected-graphs/), and it allows [multigraphs](/multigraph/) with parallel edges and [self-loops](/self-loop/), because a trail is a sequence of edges, not of vertices. [Euler's theorem](/eulers-theorem-eulerian-graphs/) tells exactly which graphs have one, and [Hierholzer's algorithm](/hierholzer-algorithm/) finds one in linear time.

## Definition

Let $G = (V, E)$ be a finite graph. It may be directed or undirected, and it may have parallel edges and self-loops. A [walk](/walk/) of length $k$ is an alternating sequence

$$W = (v_0, e_1, v_1, e_2, v_2, \ldots, e_k, v_k)$$

of vertices and edges in which each edge $e_i$ joins $v_{i-1}$ and $v_i$. In a directed graph, $e_i$ must go from $v_{i-1}$ to $v_i$. A self-loop $e_i$ at $v$ has $v_{i-1} = v_i = v$. The walk is a *trail* if the edges $e_1, \ldots, e_k$ are pairwise distinct.

**Eulerian path.** A trail $W$ is an *Eulerian path* of $G$ if each edge of $E$ occurs in $W$ exactly once, that is, $k = |E|$ and $\{e_1, \ldots, e_k\} = E$.

- $W$ is *closed* if $v_0 = v_k$. A closed Eulerian path is an [Eulerian circuit](/eulerian-circuit/).
- $W$ is *open* if $v_0 \ne v_k$. Some books reserve the words "Euler trail" or "Eulerian path" for this open case. On this site an Eulerian path may be open or closed, and the page says "open" when it means only the open case.
- The edges are listed with their names. In a multigraph, two parallel edges are two different entries of the trail. For this reason a vertex sequence alone does not describe an Eulerian path of a multigraph.

**Vertices.** An Eulerian path does not have to visit every vertex. A vertex with no edges, an *isolated vertex*, is never on an Eulerian path unless it is the only vertex that the path touches (the graph has no edges at all). A graph with $E = \emptyset$ has the Eulerian paths of length 0, each of them one vertex $(v_0)$. Some authors exclude this trivial case.

**When one exists.** By [Euler's theorem](/eulers-theorem-eulerian-graphs/), an undirected graph has an Eulerian path if and only if all its edges lie in one [connected component](/connected-components/) and it has zero or two vertices of odd [degree](/degree/), where a self-loop adds 2 to the degree of its vertex. With two odd vertices, every Eulerian path is open and goes from one odd vertex to the other. A directed graph has one if and only if all its edges lie in one component of the underlying undirected graph and either every vertex has equal in-degree and out-degree, or exactly one vertex has $d^+ - d^- = 1$ (the start), exactly one has $d^- - d^+ = 1$ (the end), and all others are balanced. The proof is on the theorem page.

## Examples and non-examples

**The house of Nicholas.** Draw a square with vertices $0$ (bottom left), $1$ (bottom right), $2$ (top right), $3$ (top left), add both diagonals $\{0, 2\}$ and $\{1, 3\}$, and add a roof vertex $4$ with the edges $\{2, 4\}$ and $\{3, 4\}$. The 8 edges give the degrees $d(0) = d(1) = 3$, $d(2) = d(3) = 4$ and $d(4) = 2$. Vertices 0 and 1 are odd, so each Eulerian path is open and joins 0 and 1. One of them is

$$0 \to 1 \to 2 \to 0 \to 3 \to 2 \to 4 \to 3 \to 1.$$

There are 44 Eulerian paths that start at 0, and by reversal 44 that start at 1, so 88 in total. None is closed. This is the child's puzzle of drawing the house without lifting the pen.

**A directed graph.** The edges $0 \to 1$, $1 \to 2$, $2 \to 0$ and $0 \to 3$ have $d^+(0) - d^-(0) = 1$ and $d^-(3) - d^+(3) = 1$, and vertices 1 and 2 are balanced. The only Eulerian path is $0 \to 1 \to 2 \to 0 \to 3$. It passes through vertex 0 twice.

**Self-loops.** On the vertices 0 and 1 with a self-loop at 0 and the edge $\{0, 1\}$, the degrees are $d(0) = 3$ and $d(1) = 1$. The two Eulerian paths are $0 \to 0 \to 1$ (the loop first) and its reverse $1 \to 0 \to 0$.

**Parallel edges.** The multigraph on $\{0, 1\}$ with three parallel edges $a, b, c$ has two odd vertices. An Eulerian path from 0 is $(0, a, 1, b, 0, c, 1)$, and there are $3! = 6$ of them from 0, one for each order of the edges.

**Non-example: Königsberg.** The four land areas of Königsberg, joined by seven bridges, form a multigraph with degrees 5, 3, 3 and 3. It has four odd vertices, so it has no Eulerian path. This was Euler's problem of 1736.

**Non-example: two components.** The graph with the edges $\{0, 1\}$ and $\{2, 3\}$ has all degrees odd, but the main reason it fails is that its edges lie in two components: a trail stays inside one component.

**Non-example: a star.** The star $K_{1,3}$ has three leaves of degree 1 and a centre of degree 3. It has four odd vertices and no Eulerian path. A trail that enters a leaf cannot leave it again, so at most two leaves can be the ends of a trail.

**Non-example: a walk that repeats an edge.** In the path graph $0 - 1 - 2$, the walk $0, 1, 2, 1$ covers all edges but uses $\{1, 2\}$ twice, so it is not a trail. The trail $0, 1, 2$ is an Eulerian path.

**Isolated vertices do not matter.** Adding any number of isolated vertices to a graph does not change its Eulerian paths. A graph is not "disconnected" in the sense that matters here because of an isolated vertex.

## Related definitions

- [Walk](/walk/), [trail](/trail/) and [simple path](/simple-path/): an Eulerian path is a trail. It is usually not a simple path, because it may revisit vertices.
- [Eulerian circuit](/eulerian-circuit/): the closed case.
- [Eulerian graph](/eulerian-graph/): a graph with an Eulerian circuit. A graph with an open Eulerian path but no Eulerian circuit is often called *semi-Eulerian* or *traversable*.
- [Hamiltonian path](/hamiltonian-path/): the dual notion for vertices. It visits each vertex exactly once. Deciding whether an Eulerian path exists takes linear time; deciding whether a Hamiltonian path exists is NP-complete.
- [Eulerian path problem](/eulerian-path-problem/): the task of finding one, solved by [Hierholzer's algorithm](/hierholzer-algorithm/) and by [Fleury's algorithm](/fleury-algorithm/).
- [Chinese postman problem](/chinese-postman-problem/): the shortest closed walk that uses every edge at least once. It equals the total edge weight exactly when the graph has an Eulerian circuit.
- [De Bruijn sequence](/de-bruijn-sequence/): an Eulerian circuit of a [de Bruijn graph](/de-bruijn-graph/).

## References
