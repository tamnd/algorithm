---
tag: 5FSZA2
kind: problem
slug: hamiltonian-path-problem
name: Hamiltonian path problem
aliases:
- Hamiltonian path
- HAM-PATH
area: graphs/paths-and-cycles
level: intro
summary: Decide whether a graph has a Hamiltonian path; NP-complete in general, linear-time on DAGs and trivial on tournaments.
prereqs: [hamiltonian-path, np-complete, hamiltonian-cycle-problem]
see_also: [hamiltonian-cycle-problem, longest-path-problem, held-karp-algorithm, k-path-color-coding, topological-sort, minimum-path-cover-problem, bitmask-dp, traveling-salesman-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.3, problem GT39 (Hamiltonian path), with the variants with given ends and the directed version
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 34.5.3 (The hamiltonian-cycle problem), and Section 34.2 (the verifier for HAM-CYCLE)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 14 (Lower bounds based on the Exponential-Time Hypothesis), and Chapter 5 (Randomized methods in parameterized algorithms), color coding for longest path
  - paper: doi:10.1145/210332.210337
    title: Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844 to 856 (1995)
    locator: the algorithm for simple paths of length k
  - paper: László Rédei, Ein kombinatorischer Satz, Acta Litterarum ac Scientiarum Szeged 7, 1934
    title: Rédei, every tournament has a Hamiltonian path
    locator: the main theorem
---

The Hamiltonian path problem asks whether a graph has a [Hamiltonian path](/hamiltonian-path/), a simple path that visits every vertex exactly once. It is [NP-complete](/np-complete/) for directed and undirected graphs, with or without fixed end vertices, and it is polynomially equivalent to the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/). Two special cases are easy: on a [directed acyclic graph](/directed-acyclic-graph/) one [topological sort](/topological-sort/) decides it in linear time, and every tournament has a Hamiltonian path. The general exact algorithms take $O^*(2^n)$ time.

## In plain words

You must visit every room of a building exactly once, walking only through doors between rooms. You may start and stop in any room. Is it possible?

The rooms and doors form a graph. For a few kinds of buildings the answer is quick. If all doors are one-way and you can never come back to a room, there is only one possible order to check. If every pair of rooms has a one-way door between them, the answer is always yes. For a general building, no quick method is known. The best known methods keep, for each group of visited rooms, the rooms where a tour of that group can end, and their work doubles with each extra room.

## Definition

**Input.** A finite graph $G = (V, E)$, directed or undirected, with $n = |V| \ge 1$ and $m = |E|$. Parallel edges and self-loops may appear; a simple path never uses a loop or two parallel edges, so the answer depends only on the underlying simple graph. Isolated vertices are allowed and make the answer "no" when $n \ge 2$.

**Question.** Is there an ordering $(v_1, \ldots, v_n)$ of $V$ such that $v_i$ and $v_{i+1}$ are adjacent (in the directed version, $(v_i, v_{i+1}) \in E$) for each $1 \le i < n$?

**Versions with ends.** The *$s$-$t$ version* fixes $v_1 = s$ and $v_n = t$. The *one-end version* fixes only $v_1 = s$. All three versions are NP-complete, and each reduces to the others.

**Certificate.** The ordering. Checking it takes $O(n + m)$ time, so the problem is in NP.

## Variants

- **Hamiltonian cycle.** The closed version; see the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/).
- **Longest path.** Find a simple path with the most edges. The answer is $n - 1$ exactly when a Hamiltonian path exists; see the [longest path problem](/longest-path-problem/).
- **$k$-path.** Is there a simple path with $k$ vertices? For $k = n$ this is the Hamiltonian path problem; for fixed $k$ it is solved by [color coding](/k-path-color-coding/).
- **Path cover.** Cover $V$ with the fewest vertex-disjoint paths. One path suffices exactly when a Hamiltonian path exists; see the [minimum path cover problem](/minimum-path-cover-problem/).
- **Shortest Hamiltonian path.** With edge weights, find the cheapest Hamiltonian path: the path version of the [traveling salesman problem](/traveling-salesman-problem/).

## Examples

**A directed acyclic graph.** Arcs $0 \to 1$, $0 \to 2$, $1 \to 2$, $1 \to 3$, $2 \to 3$. A topological order is $0, 1, 2, 3$, and the arcs $0 \to 1$, $1 \to 2$, $2 \to 3$ all exist, so $(0, 1, 2, 3)$ is a Hamiltonian path. Delete the arc $1 \to 2$. Now $0, 1, 2, 3$ is still a topological order, but $1 \to 2$ is missing, so the graph has no Hamiltonian path: the other order $0, 2, 1, 3$ also fails, at $2 \to 1$.

**The Petersen graph.** It has 120 Hamiltonian paths (without direction) and no Hamiltonian cycle.

**The star $K_{1,3}$.** Three vertices have degree 1, but a path has only two ends, so the answer is no.

**An isolated vertex.** $K_3$ plus an isolated vertex has no Hamiltonian path, although $K_3$ alone has 3.

**A self-loop.** Adding a loop at every vertex of the star $K_{1,3}$ does not help: loops are never used.

**A tournament on 4 vertices.** Arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $3 \to 0$, $1 \to 3$, $3 \to 2$. Insert the vertices in the order $0, 1, 2, 3$ as in Rédei's proof on the [Hamiltonian path](/hamiltonian-path/) page. Start with $(0)$. Since $0 \to 1$, vertex 1 goes last: $(0, 1)$. Since $2 \to 0$, vertex 2 goes first: $(2, 0, 1)$. Since $3 \to 2$, vertex 3 goes first: $(3, 2, 0, 1)$, a Hamiltonian path.

## Known algorithms

- **Dynamic programming over subsets.** Let $R(S)$, for nonempty $S \subseteq V$, be the set of vertices $v \in S$ such that some simple path with vertex set exactly $S$ ends at $v$. Then $R(\{v\}) = \{v\}$ and
  $$R(S) = \{ v \in S : \exists u \in R(S \setminus \{v\}),\ (u, v) \in E \} \quad (|S| \ge 2).$$
  The answer is "yes" if and only if $R(V) \ne \emptyset$. With bit masks this takes $O(2^n n)$ word operations and $2^n$ words of space. It is the decision form of the [Held-Karp algorithm](/held-karp-algorithm/) with every vertex allowed as a start; replacing the sets by counts gives the number of Hamiltonian paths.
- **Inclusion-exclusion.** The number of Hamiltonian paths, as sequences, is $\sum_{T \subseteq V} (-1)^{|T|} w_{G - T}(n - 1)$, where $w_H(k)$ is the number of walks with $k$ edges in $H$. This takes $O(2^n n m)$ time and polynomial space. The proof is the one for cycles on the [Hamiltonian cycle problem](/hamiltonian-cycle-problem/) page.
- **Directed acyclic graphs: $O(n + m)$.** Compute one topological order $(v_1, \ldots, v_n)$ and check that each $(v_i, v_{i+1})$ is an arc. *Correctness.* If the check passes, the order is a Hamiltonian path. Conversely, let $P$ be a Hamiltonian path of a DAG. Every arc $(x, y)$ goes forward along $P$, since a backward arc would close a cycle with the part of $P$ from $y$ to $x$. So $P$ is a topological order, and it is the only one, because each consecutive pair is ordered by an arc. Hence the computed order is $P$ and the check passes.
- **Tournaments: $O(n \log n)$ queries.** The answer is always "yes", and binary insertion builds the path (see [Hamiltonian path](/hamiltonian-path/)).
- **Color coding for short paths.** A simple path with $k$ vertices can be found in $2^{O(k)} m$ expected time (Alon, Yuster and Zwick, 1995); see [color coding for $k$-path](/k-path-color-coding/). For $k = n$ this is no better than the dynamic program.
- **Backtracking with pruning.** Extend a path one vertex at a time and stop a branch when the unvisited vertices cannot all be reached. Fast on many inputs, $O(n!)$ in the worst case.

## Bounds

- **NP-completeness.** All versions are NP-complete, directed and undirected (Garey and Johnson, problem GT39). The reductions below transfer the hardness from the Hamiltonian cycle problem, which Karp proved NP-complete in 1972.
- **Hard special cases.** The cycle problem stays NP-complete on planar cubic 3-connected graphs and on grid graphs, and the reductions below keep planarity, so the path problem stays hard on planar graphs too.
- **Exact time.** $O^*(2^n)$ by either method above. Under the Exponential Time Hypothesis, no $2^{o(n)}$ algorithm exists.
- **Easy cases.** DAGs in $O(n + m)$, tournaments always, graphs that meet [Dirac's](/dirac-theorem/) or [Ore's](/ore-theorem/) condition (they are even Hamiltonian), and graphs of bounded treewidth.

## Reductions

- **Path to cycle.** $G$ has a Hamiltonian path if and only if $G$ plus a new vertex joined to every vertex (both directions, if directed) has a Hamiltonian cycle.
- **Cycle to path.** Pick a vertex $v$, add a twin $v'$ with the same neighbours as $v$, and add new vertices $s$ joined to $v$ and $t$ joined to $v'$. For $n \ge 3$, the new graph has a Hamiltonian path if and only if $G$ has a Hamiltonian cycle. *Proof.* A cycle $(v, a, \ldots, b, v)$ gives the path $(s, v, a, \ldots, b, v', t)$. Conversely $s$ and $t$ have degree 1, so they are the two ends of any Hamiltonian path, which then reads $(s, v, \ldots, x, v', t)$, and $x$ is a neighbour of $v'$, hence of $v$; the part from $v$ to $x$ closes to a Hamiltonian cycle of $G$.
- **$s$-$t$ version to the free version.** Add a vertex $s'$ joined only to $s$ and $t'$ joined only to $t$. A Hamiltonian path of the new graph must end at $s'$ and $t'$, so it gives a Hamiltonian $s$-$t$ path.
- **To longest path and path cover.** The answer is yes if and only if the longest simple path has $n - 1$ edges, and if and only if the minimum path cover has one path. So both problems are NP-hard on general graphs.

## Applications

- **Sequencing.** Ordering items so that consecutive items are compatible, such as fragments with overlaps in early genome assembly (a Hamiltonian path in the overlap graph, in contrast to the Eulerian path in a [de Bruijn graph](/de-bruijn-graph/)), or jobs with compatible setups.
- **Ranking a tournament.** A Hamiltonian path of a tournament orders the players so that each one beat the next.
- **Gray codes and listings.** A [Gray code](/gray-code/) is a Hamiltonian path of the hypercube.
- **Hardness proofs.** Many NP-hardness proofs for path and scheduling problems start from the Hamiltonian path problem.

## References
