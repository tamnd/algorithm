---
tag: CNCPA1
kind: problem
slug: hamiltonian-cycle-problem
name: Hamiltonian cycle problem
aliases:
- Hamiltonian circuit
- Hamiltonian circuit problem
- HAM-CYCLE
area: graphs/paths-and-cycles
level: intro
summary: Decide whether a graph has a Hamiltonian cycle; NP-complete for directed and undirected graphs.
prereqs: [hamiltonian-cycle, np-complete, polynomial-time-reduction]
see_also: [hamiltonian-path-problem, hamiltonian-cycle-np-completeness, held-karp-algorithm, traveling-salesman-problem, karps-21-np-complete-problems, ore-theorem, dirac-theorem, exact-exponential-algorithms]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.2 (the language HAM-CYCLE and its verifier) and Section 34.5.3 (The hamiltonian-cycle problem, the reduction from vertex cover)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the problems DIRECTED HAMILTON CIRCUIT and UNDIRECTED HAMILTON CIRCUIT
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.4 (the proof for Hamiltonian circuit) and Appendix A1.3, problems GT37 (Hamiltonian circuit) and GT38 (directed Hamiltonian circuit), with the special cases that stay NP-complete
  - paper: doi:10.1137/0205049
    title: M. R. Garey, D. S. Johnson and R. Endre Tarjan, The planar Hamiltonian circuit problem is NP-complete, SIAM Journal on Computing 5(4), 704 to 714 (1976)
    locator: the main theorem (planar, cubic, 3-connected graphs)
  - paper: doi:10.1137/0110015
    title: Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the Society for Industrial and Applied Mathematics 10(1), 196 to 210 (1962)
    locator: the dynamic program over subsets for the traveling salesman problem
  - paper: Andreas Björklund, Determinant sums for undirected Hamiltonicity, SIAM Journal on Computing 43(1), 2014 (conference version FOCS 2010)
    title: Andreas Björklund, Determinant sums for undirected Hamiltonicity, SIAM Journal on Computing 43(1), 280 to 299 (2014)
    locator: the main theorem (a Monte Carlo algorithm in O*(1.657^n) time for undirected graphs)
  - paper: Richard M. Karp, Dynamic programming meets the principle of inclusion and exclusion, Operations Research Letters 1(2), 1982
    title: Karp, counting Hamiltonian cycles by inclusion and exclusion in polynomial space
    locator: the whole paper
  - paper: Paul Camion, Chemins et circuits hamiltoniens des graphes complets, Comptes Rendus de l'Académie des Sciences de Paris 249, 1959
    title: Camion, every strongly connected tournament with at least 3 vertices has a Hamiltonian cycle
    locator: the main theorem
  - paper: Alon Itai, Christos H. Papadimitriou and Jayme Luiz Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 1982
    title: Itai, Papadimitriou and Szwarcfiter, NP-completeness for grid graphs
    locator: the main theorem
  - paper: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 1979
    title: Valiant, #P-completeness of counting problems, including Hamiltonian cycles
    locator: the list of #P-complete problems
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 14 (Lower bounds based on the Exponential-Time Hypothesis), the lower bounds for Hamiltonian cycle and path
---

The Hamiltonian cycle problem asks whether a given graph has a [Hamiltonian cycle](/hamiltonian-cycle/), a cycle that passes through every vertex exactly once. It is [NP-complete](/np-complete/) for directed and for undirected graphs, and it was one of Karp's 21 problems of 1972. No polynomial-time algorithm is known, and the best exact algorithms take time exponential in the number of vertices: $O(2^n n^2)$ by dynamic programming over subsets, and less for undirected graphs by algebraic methods. It is the unweighted core of the [traveling salesman problem](/traveling-salesman-problem/).

## In plain words

A graph is a set of towns and roads. You want a round trip that visits each town exactly once and comes back home. Some maps have such a trip and some do not. The question is how to tell.

For the similar question about roads (use each road once), a quick test on the number of roads at each town answers it. For towns, no quick test is known. A program can try all orders of the towns, but the number of orders grows faster than any power of the number of towns. Better programs remember, for each group of visited towns, where a partial trip can end. They still take time that doubles with each extra town. Most experts believe that no fast method exists, because a fast method would also solve thousands of other hard problems.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n = |V|$ vertices and $m = |E|$ edges. In the undirected version $G$ is undirected; in the directed version $G$ is a [directed graph](/directed-graph/). Parallel edges and self-loops may appear; for $n \ge 3$ they do not change the answer (see [Hamiltonian cycle](/hamiltonian-cycle/)), so an algorithm can first replace $G$ by its underlying simple graph.

**Decision question.** Is there an ordering $(v_1, \ldots, v_n)$ of $V$ such that $v_i v_{i+1} \in E$ for $1 \le i < n$ and $v_n v_1 \in E$ (arcs $(v_i, v_{i+1})$ and $(v_n, v_1)$ in the directed version)? As a language,

$$\textsf{HAM-CYCLE} = \{\langle G \rangle : G \text{ has a Hamiltonian cycle}\}.$$

**Search version.** Output such an ordering, or report that none exists.

**Certificate.** The ordering itself. A verifier checks in $O(n + m)$ time, with an adjacency matrix in $O(n)$ time after $O(n^2)$ setup, that it is a permutation of $V$ and that the $n$ required edges exist. So the problem is in NP.

## Variants

- **Hamiltonian path.** Ask for a path through all vertices, possibly with fixed ends. See the [Hamiltonian path problem](/hamiltonian-path-problem/). The two problems reduce to each other in polynomial time.
- **Search from decision.** With an oracle for the decision question, delete each edge in turn and keep the deletion when the graph stays Hamiltonian. After $m$ calls, the remaining edges form a Hamiltonian cycle. This is a [search-to-decision reduction](/search-to-decision-reduction/).
- **Counting.** Count the Hamiltonian cycles. The inclusion-exclusion method below counts them; the counting problem is #P-complete.
- **Weighted version.** With edge weights, find a Hamiltonian cycle of minimum weight: the [traveling salesman problem](/traveling-salesman-problem/).
- **Restricted classes.** Planar graphs, cubic graphs, bipartite graphs, grid graphs, tournaments and graphs of bounded treewidth. Some stay NP-complete, some become easy; see Bounds.

## Examples

**The house.** Take the square $0, 1, 2, 3$ with edges $01, 12, 23, 30$, and a roof vertex 4 joined to 0 and 1. The cycle $(0, 4, 1, 2, 3, 0)$ is Hamiltonian, and it is the only one. The graph has 7 Hamiltonian paths (counted without direction).

The subset dynamic program below, started at vertex 0, finds these possible end vertices $R(S)$ for the sets $S$ that contain 0 and have a path:

| $\lvert S \rvert$ | sets $S$ and their end sets $R(S)$ |
|---|---|
| 1 | $\{0\}$: 0 |
| 2 | $\{0,1\}$: 1; $\{0,3\}$: 3; $\{0,4\}$: 4 |
| 3 | $\{0,1,2\}$: 2; $\{0,2,3\}$: 2; $\{0,1,4\}$: 1, 4 |
| 4 | $\{0,1,2,3\}$: 1, 3; $\{0,1,2,4\}$: 2 |
| 5 | $\{0,1,2,3,4\}$: 3, 4 |

Both 3 and 4 are adjacent to 0, so a Hamiltonian cycle exists. The two ends give the same cycle in its two directions.

**The Petersen graph.** It has 10 vertices, each of degree 3, and it is 3-connected, but it has no Hamiltonian cycle. It has 120 Hamiltonian paths.

**The dodecahedron.** It has 20 vertices and 30 Hamiltonian cycles.

**Trivial no-instances.** A graph with a vertex of degree at most 1 (for $n \ge 3$), a disconnected graph, a graph with an [articulation point](/articulation-point/), and a bipartite graph with unequal sides have no Hamiltonian cycle. Such quick tests reject many inputs, but not all: the Petersen graph passes all of them.

**Directed.** The directed graph with arcs $0 \to 1$, $1 \to 2$, $2 \to 0$ has the Hamiltonian cycle $(0, 1, 2, 0)$. If the arc $2 \to 0$ is replaced by $0 \to 2$, vertex 0 has no incoming arc, and no Hamiltonian cycle exists, although the underlying undirected graph is a triangle.

## Known algorithms

- **Brute force.** Fix $v_1$ and try the $(n-1)!$ orders of the other vertices: $O(n!)$ time. Backtracking with pruning (stop when the partial path cannot be extended, or when the rest of the graph is disconnected) is much faster on many inputs but has the same worst case.
- **Dynamic programming over subsets (Held and Karp 1962).** Fix a start $s$. For each set $S \ni s$ let $R(S)$ be the set of $v \in S$ such that some simple path from $s$ to $v$ has vertex set exactly $S$. Then $R(\{s\}) = \{s\}$, and
  $$R(S) = \{v \in S \setminus \{s\} : \exists u \in R(S \setminus \{v\}) \text{ with } (u, v) \in E\}.$$
  $G$ is Hamiltonian if and only if some $v \in R(V)$ has $(v, s) \in E$ (for $n \ge 2$; for $n = 2$ in the undirected version, two parallel edges are needed). This takes $O(2^n n^2)$ time and $O(2^n n)$ bits of space, or $O(2^n n)$ word operations when $R(S)$ is a bit mask and the neighbourhoods are bit masks. It is the decision form of the [Held-Karp algorithm](/held-karp-algorithm/).
- **Inclusion-exclusion (Karp 1982).** The number of directed Hamiltonian cycles through $s$, as sequences, is
  $$\sum_{T \subseteq V \setminus \{s\}} (-1)^{|T|}\, W_{G - T}(s, n),$$
  where $W_H(s, n)$ is the number of closed walks of length $n$ from $s$ in $H$. A closed walk of length $n$ from $s$ that visits every vertex is a Hamiltonian cycle, and the sum removes, by the [inclusion-exclusion principle](/inclusion-exclusion-principle/), each walk that misses a vertex. Each $W$ costs $O(n m)$ by $n$ steps of vector-matrix products, so the total is $O(2^n n m)$ time and only polynomial space.
- **Björklund's algorithm (2010, journal 2014).** For undirected graphs, a Monte Carlo algorithm decides Hamiltonicity in $O^*(1.657^n)$ time, and in $O^*(2^{n/2})$ time for bipartite graphs, by sums of determinants over a field of characteristic 2. No algorithm with a base below 2 is known for the general directed case.
- **Sufficient conditions.** When [Dirac's](/dirac-theorem/) or [Ore's](/ore-theorem/) condition holds, the cycle exists, and the proofs turn into $O(n^2)$ algorithms that build it.
- **Tournaments.** A tournament with $n \ge 3$ is Hamiltonian if and only if it is [strongly connected](/strongly-connected-graph/) (Camion 1959), so the decision takes $O(n^2)$ time.
- **Practice.** Backtracking with pruning, SAT and integer programming encodings, and TSP solvers run on the weights of the reduction below decide many large instances, with no guarantee on the time.

## Bounds

- **NP-completeness.** The directed and undirected versions are NP-complete (Karp 1972). CLRS prove it by a reduction from [vertex cover](/vertex-cover/) with widgets of 12 vertices; see [Hamiltonian cycle NP-completeness](/hamiltonian-cycle-np-completeness/).
- **Restricted classes that stay NP-complete.** Planar, cubic, 3-connected graphs (Garey, Johnson and Tarjan, 1976). Grid graphs, that is induced subgraphs of the square grid (Itai, Papadimitriou and Szwarcfiter, 1982). Bipartite graphs (listed in Garey and Johnson). So degree bounds and planarity do not make the problem easy.
- **Lower bounds under hypotheses.** Under the Exponential Time Hypothesis, no algorithm decides the problem in $2^{o(n)}$ time, because the standard reductions from 3-SAT produce graphs whose size is linear in the size of the formula.
- **Exact upper bounds.** $O^*(2^n)$ time for directed graphs, by either method above, and $O^*(1.657^n)$ for undirected graphs (Björklund). The dynamic program needs exponential space; inclusion-exclusion needs only polynomial space.
- **Counting.** Counting Hamiltonian cycles is #P-complete (Valiant, 1979).

## Reductions

- **Directed to undirected.** Replace each vertex $v$ by a path $v_{\text{in}} - v_{\text{mid}} - v_{\text{out}}$ and each arc $(u, v)$ by the edge $u_{\text{out}} v_{\text{in}}$. The new graph has $3n$ vertices. A Hamiltonian cycle of it must pass through each $v_{\text{mid}}$ between $v_{\text{in}}$ and $v_{\text{out}}$, since $v_{\text{mid}}$ has degree 2, so it reads as a directed Hamiltonian cycle of the original. The undirected case is a special case of the directed one (two arcs for each edge).
- **Hamiltonian path to cycle.** Add a vertex joined to all others; see [Hamiltonian path](/hamiltonian-path/).
- **Cycle to path.** Pick a vertex $v$, add a copy $v'$ with the same neighbours, and add two new vertices $s$ and $t$ of degree 1, joined to $v$ and to $v'$. For $n \ge 3$, the new graph has a Hamiltonian path (necessarily from $s$ to $t$) if and only if $G$ has a Hamiltonian cycle.
- **To the traveling salesman problem.** On the complete graph over $V$, give each edge of $G$ weight 1 and each non-edge weight 2. $G$ is Hamiltonian if and only if the shortest tour has weight $n$. With weight $\rho n + 1$ instead of 2, the same construction shows that the general TSP has no polynomial-time $\rho$-approximation unless P = NP; see [general TSP inapproximability](/general-tsp-inapproximability/).
- **To SAT.** Encode "position $i$ holds vertex $v$" with $n^2$ Boolean variables; the constraints say each position holds one vertex, each vertex has one position, and consecutive positions hold adjacent vertices.

## Applications

- **Tours and routing.** Each TSP instance contains a Hamiltonian cycle problem; a vehicle route that must visit every stop once is a Hamiltonian cycle in the road graph.
- **Combinatorial generation.** A cyclic [Gray code](/gray-code/) is a Hamiltonian cycle of the hypercube, and many listing problems (permutations by adjacent swaps, combinations by one exchange) ask for a Hamiltonian cycle or path of a graph of objects.
- **Puzzles.** Closed [knight's tours](/knights-tour-problem/) and Hamilton's icosian game.
- **Lower bounds by reduction.** Proofs that a new problem is NP-hard often start from the Hamiltonian cycle or path problem, as for the [longest path problem](/longest-path-problem/).

## References
