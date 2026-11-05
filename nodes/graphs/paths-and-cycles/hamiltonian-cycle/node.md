---
tag: NHWW8D
kind: definition
slug: hamiltonian-cycle
name: Hamiltonian cycle
aliases:
- Hamiltonian circuit
- Hamilton cycle
- Hamiltonian graph
area: graphs/paths-and-cycles
level: intro
summary: A simple cycle that visits every vertex exactly once.
prereqs: [simple-cycle, hamiltonian-path]
see_also: [hamiltonian-cycle-problem, dirac-theorem, ore-theorem, traveling-salesman-problem, eulerian-circuit, held-karp-algorithm, hypercube-hamiltonian-cycle, knights-tour-problem]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer, 2008
    locator: Chapter 18 (Hamilton Cycles), Hamiltonian and non-Hamiltonian graphs, the condition on components after deleting a set of vertices, and the Petersen graph
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Chapter 10 (Hamilton cycles), Section 10.1 (sufficient conditions)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 7.2 (Hamiltonian cycles), necessary conditions, the Petersen graph, and the theorems of Dirac, Ore and Chvátal
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.2 (Polynomial-time verification), the Hamiltonian cycle and the language HAM-CYCLE
  - paper: J. A. Bondy and V. Chvátal, A method in graph theory, Discrete Mathematics 15(2), 1976
    title: Bondy and Chvátal, the closure of a graph and its use for Hamiltonian cycles
    locator: the closure lemma and theorem for Hamiltonian cycles
---

A Hamiltonian cycle is a [simple cycle](/simple-cycle/) that passes through every vertex of a graph. A graph that has one is called *Hamiltonian*. The notion is named after William Rowan Hamilton, who studied such tours on the dodecahedron. It looks like the [Eulerian circuit](/eulerian-circuit/), with vertices in place of edges, but no simple test for it is known: deciding whether a graph is Hamiltonian is the NP-complete [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). In a complete graph with edge weights, a cheapest Hamiltonian cycle is a solution of the [traveling salesman problem](/traveling-salesman-problem/).

## Definition

Let $G = (V, E)$ be a graph with $n = |V| \ge 1$ vertices, directed or undirected, possibly a [multigraph](/multigraph/) with [self-loops](/self-loop/). Cycles are as defined on the [simple cycle](/simple-cycle/) page.

**Hamiltonian cycle.** A *Hamiltonian cycle* of $G$ is a simple cycle $C = (v_1, v_2, \ldots, v_n, v_1)$ that contains every vertex of $V$. Equivalently, $(v_1, \ldots, v_n)$ is an ordering of $V$ such that $v_i$ is adjacent to $v_{i+1}$ for $1 \le i \le n - 1$ and $v_n$ is adjacent to $v_1$, with distinct edges for these $n$ steps. In a directed graph, the arcs go from $v_i$ to $v_{i+1}$ and from $v_n$ to $v_1$. The length of $C$ is $n$. $G$ is *Hamiltonian* if it has a Hamiltonian cycle.

**Small cases and multigraphs.** With the definition of a simple cycle used on this site:

| $n$ | undirected | directed |
|---|---|---|
| 1 | Hamiltonian if and only if there is a loop | Hamiltonian if and only if there is a loop |
| 2 | Hamiltonian if and only if there are two parallel edges | Hamiltonian if and only if both arcs $u \to v$ and $v \to u$ exist |
| $\ge 3$ | depends only on the underlying simple graph | depends only on the underlying simple directed graph |

For $n \ge 3$ a Hamiltonian cycle uses no loop and at most one of each group of parallel edges, so loops and parallel edges change nothing. Many books state results only for simple graphs with $n \ge 3$, and some call $K_1$ Hamiltonian by convention; this page avoids the cases $n \le 2$ in its statements unless it says otherwise.

**Counting the same cycle once.** A Hamiltonian cycle of an undirected graph with $n \ge 3$ is written as a sequence in $2n$ ways (choose the start and the direction). Counts on this page count the cycles as edge sets.

**Necessary conditions.** Let $G$ be undirected and Hamiltonian with $n \ge 3$.

1. **Toughness.** For every nonempty $S \subseteq V$, the graph $G - S$ has at most $|S|$ connected components. *Proof.* Deleting $|S| \ge 1$ vertices from the cycle $C$ cuts it into at most $|S|$ pieces, each piece is connected, and every vertex of $G - S$ is in one piece. $\square$
2. **2-connected.** The case $|S| = 1$ of condition 1: no single vertex disconnects $G$, so $G$ has no [articulation point](/articulation-point/) and is [biconnected](/biconnected-graph/). In particular every vertex has degree at least 2.
3. **Balanced bipartite.** If $G$ is [bipartite](/bipartite-graph/) with sides $X$ and $Y$, then $|X| = |Y|$, because $C$ alternates between the sides. So a Hamiltonian bipartite graph has an even number of vertices.

None of them is sufficient: the Petersen graph meets all three and is not Hamiltonian.

**Sufficient conditions.** For a simple undirected graph with $n \ge 3$:

- [Dirac's theorem](/dirac-theorem/): if every vertex has degree at least $n/2$, then $G$ is Hamiltonian.
- [Ore's theorem](/ore-theorem/): if $\deg u + \deg v \ge n$ for every pair of distinct non-adjacent vertices, then $G$ is Hamiltonian.
- The Bondy-Chvátal closure: $G$ is Hamiltonian if and only if the graph obtained by repeatedly joining non-adjacent pairs with degree sum at least $n$ is Hamiltonian. If that closure is complete, $G$ is Hamiltonian.

These conditions force many edges. Sparse Hamiltonian graphs, such as the cycle $C_n$ itself, meet none of them.

**Cycle and path.** Deleting one edge of a Hamiltonian cycle leaves a [Hamiltonian path](/hamiltonian-path/). Conversely, a Hamiltonian path $(v_1, \ldots, v_n)$ with $v_n$ adjacent to $v_1$ closes to a Hamiltonian cycle when $n \ge 3$.

## Examples and non-examples

**Complete graphs.** $K_n$ with $n \ge 3$ has $(n-1)!/2$ Hamiltonian cycles: fix $v_1$, order the other $n - 1$ vertices, and identify each order with its reverse. For $n = 3, 4, 5, 6$ the counts are $1, 3, 12, 60$.

**Complete bipartite graphs.** $K_{k,k}$ with $k \ge 2$ has $k!\,(k-1)!/2$ Hamiltonian cycles: $1$ for $k = 2$ (the square) and $6$ for $k = 3$. $K_{k,k+1}$ has none, by condition 3.

**The dodecahedron.** The graph of the dodecahedron (20 vertices, 30 edges, all degrees 3) has 30 Hamiltonian cycles. This is the graph of Hamilton's icosian game.

**The cube.** The cube $Q_d$ is Hamiltonian for $d \ge 2$; a cyclic [Gray code](/gray-code/) is such a cycle (see [Hamiltonian cycle of the hypercube](/hypercube-hamiltonian-cycle/)). $Q_3$ has 6 Hamiltonian cycles.

**The Petersen graph.** It is 3-regular, 3-connected, and has no Hamiltonian cycle, although it has 120 Hamiltonian paths. It is the standard example that degree and connectivity conditions alone do not decide Hamiltonicity.

**Grid graphs.** The $p \times q$ grid with $p, q \ge 2$ is bipartite with sides of sizes $\lceil pq/2 \rceil$ and $\lfloor pq/2 \rfloor$. If $pq$ is odd, the sides differ, so it is not Hamiltonian by condition 3. If $pq$ is even, it is Hamiltonian: the $3 \times 4$ grid has 2 Hamiltonian cycles and the $4 \times 4$ grid has 6, while the $3 \times 3$ grid has none.

**Non-examples.**

- A tree with $n \ge 3$ has no cycle at all.
- Two triangles that share one vertex (the bowtie): deleting the shared vertex leaves 2 components, more than $|S| = 1$.
- A graph with an isolated vertex and $n \ge 2$.
- A directed graph with a vertex of in-degree 0 or out-degree 0.

**Knight's tour.** A closed [knight's tour](/knights-tour-problem/) is a Hamiltonian cycle of the knight's graph; the $8 \times 8$ board has one.

## Related definitions

- **Hamiltonian path.** See [Hamiltonian path](/hamiltonian-path/).
- **Eulerian circuit.** A closed trail through every edge, decided by degree parity and connectivity; see [Eulerian circuit](/eulerian-circuit/).
- **Traveling salesman.** A minimum-weight Hamiltonian cycle of a weighted complete graph; see [traveling salesman problem](/traveling-salesman-problem/) and the [Held-Karp algorithm](/held-karp-algorithm/).
- **Pancyclic and Hamilton-connected graphs.** A graph is *pancyclic* if it has cycles of every length from 3 to $n$, and *Hamilton-connected* if every pair of distinct vertices is joined by a Hamiltonian path.
- **Decision problem.** See the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) and its [NP-completeness proof](/hamiltonian-cycle-np-completeness/).

## References
