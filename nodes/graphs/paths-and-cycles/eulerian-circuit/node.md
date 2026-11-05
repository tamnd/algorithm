---
tag: G5EZFV
kind: definition
slug: eulerian-circuit
name: Eulerian circuit
aliases:
- Euler tour
- Eulerian cycle
area: graphs/paths-and-cycles
level: intro
summary: A closed trail that uses every edge of the graph exactly once.
prereqs: [eulerian-path, trail]
see_also: [eulerian-graph, eulers-theorem-eulerian-graphs, eulerian-path-problem, hierholzer-algorithm, fleury-algorithm, chinese-postman-problem, de-bruijn-sequence, hamiltonian-cycle]
sources:
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.8, Euler tours (Euler tours and Theorem 1.8.1)
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 3, Connected graphs, Section 3.3, Euler tours
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-3, Euler tour (a directed graph has an Euler tour if and only if in-degree equals out-degree at each vertex, for a strongly connected graph, and an O(E) algorithm)
---

An Eulerian circuit, or Euler tour, is a closed [trail](/trail/) that uses every edge of a [graph](/graph/) exactly once: it starts and ends at the same vertex and never uses an edge twice. It is the closed case of an [Eulerian path](/eulerian-path/). A graph with an Eulerian circuit is an [Eulerian graph](/eulerian-graph/). By [Euler's theorem](/eulers-theorem-eulerian-graphs/), an undirected graph whose edges lie in one component has one exactly when every vertex has even [degree](/degree/), and [Hierholzer's algorithm](/hierholzer-algorithm/) builds one in linear time.

## Definition

Let $G = (V, E)$ be a finite graph, directed or undirected, which may have parallel edges and [self-loops](/self-loop/). An *Eulerian circuit* of $G$ is a closed [walk](/walk/)

$$C = (v_0, e_1, v_1, \ldots, e_m, v_m), \qquad v_m = v_0, \quad m = |E|,$$

in which $e_1, \ldots, e_m$ are pairwise distinct and $\{e_1, \ldots, e_m\} = E$. Each edge $e_i$ joins $v_{i-1}$ and $v_i$; in a directed graph it goes from $v_{i-1}$ to $v_i$.

**Rotation and reversal.** A closed trail has no natural first edge. The rotations $(v_j, e_{j+1}, \ldots, e_m, v_0, e_1, \ldots, e_j, v_j)$ describe the same circuit with another start, and in an undirected graph the reversed sequence describes the same circuit in the other direction. When circuits are counted, the count must say which of these it identifies. In a directed graph the reversal is not a circuit, unless each edge has a partner in the other direction.

**The word "cycle".** Many texts say "Eulerian cycle". An Eulerian circuit is a [cycle](/simple-cycle/) in the strict sense, with no repeated vertex, only when the graph itself is one cycle. In general it passes through a vertex $v$ exactly $d(v)/2$ times in an undirected graph and $d^+(v) = d^-(v)$ times in a directed graph, where a pass through the start vertex counts the end and the start together as one.

**Empty graph.** A graph with no edges has the trivial circuit $(v_0)$ at each vertex. Books that define Eulerian graphs only for connected graphs with at least one edge exclude it.

**Existence.** For an undirected graph, an Eulerian circuit exists if and only if all edges lie in one [connected component](/connected-components/) and each vertex has even degree, where a self-loop adds 2. For a directed graph, it exists if and only if all edges lie in one component of the underlying undirected graph and $d^+(v) = d^-(v)$ for each $v$. Under the balance condition, "one weak component" and "one [strong component](/strongly-connected-components/) holding all edges" are the same. The proofs are on the page of [Euler's theorem](/eulers-theorem-eulerian-graphs/).

## Examples and non-examples

**Cycles.** The cycle $C_n$ with $n \ge 3$ has exactly one Eulerian circuit up to rotation and reversal: the cycle itself.

**The complete graph $K_5$.** Each vertex has degree 4, so $K_5$ has an Eulerian circuit, for example

$$0 \to 1 \to 2 \to 3 \to 4 \to 0 \to 2 \to 4 \to 1 \to 3 \to 0.$$

It uses the 5 edges of the outer pentagon and then the 5 diagonals. As sequences of edges with a fixed start vertex 0, there are 528 Eulerian circuits. Each one passes through vertex 0 twice, so it has two rotations that start at 0. This gives 264 circuits counted up to rotation, and 132 when the direction is also ignored.

**Complete graphs in general.** $K_n$ has degree $n - 1$ at each vertex, so it has an Eulerian circuit exactly when $n$ is odd (and $n \ge 3$, or $n = 1$ with the trivial circuit).

**A self-loop.** A single vertex with one self-loop has degree 2 and the Eulerian circuit $(v, e, v)$ of length 1. Two vertices joined by two parallel edges $a$ and $b$ have the circuit $(0, a, 1, b, 0)$ of length 2.

**A directed example.** The directed multigraph with the edges $0 \to 1$, $1 \to 2$, $2 \to 0$, $0 \to 2$ and a second edge $2 \to 0$ has $d^+ = d^- = 2$ at vertices 0 and 2 and $d^+ = d^- = 1$ at vertex 1. So it is balanced, and $0 \to 1 \to 2 \to 0 \to 2 \to 0$ is an Eulerian circuit that uses both parallel edges $2 \to 0$.

**Non-example: odd degrees.** $K_4$ and the Petersen graph are connected, but all their degrees are 3, so they have no Eulerian circuit.

**Non-example: two components.** Two disjoint triangles have all degrees equal to 2, but no closed trail can use edges of both triangles. So the even-degree condition alone is not enough: the edges must lie in one component.

**Non-example: a directed graph whose underlying graph is Eulerian.** The directed edges $0 \to 1$, $1 \to 2$ and $0 \to 2$ form a triangle, and each vertex has total degree 2. But $d^+(0) = 2$ and $d^-(0) = 0$, so there is no directed Eulerian circuit: a closed trail leaves each vertex as often as it enters it.

**Non-example: an open Eulerian path.** The path graph $0 - 1 - 2$ has the Eulerian path $0, 1, 2$, but no Eulerian circuit, because vertices 0 and 2 have degree 1.

## Related definitions

- [Eulerian path](/eulerian-path/): a trail through every edge exactly once, open or closed.
- [Eulerian graph](/eulerian-graph/): a graph that has an Eulerian circuit.
- [Hamiltonian cycle](/hamiltonian-cycle/): a cycle through every vertex exactly once. The two notions are unrelated in general: $K_4$ has a Hamiltonian cycle and no Eulerian circuit, and two triangles that share one vertex have an Eulerian circuit and no Hamiltonian cycle.
- [Chinese postman problem](/chinese-postman-problem/): a shortest closed walk through every edge at least once. Its optimum equals the total weight exactly when an Eulerian circuit exists.
- [De Bruijn sequence](/de-bruijn-sequence/): the label sequence of an Eulerian circuit in a [de Bruijn graph](/de-bruijn-graph/).
- [Euler tour technique](/euler-tour-technique/): a tree method that walks an Eulerian circuit of the tree with each edge doubled.

## References
