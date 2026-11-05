---
tag: H5WFSA
kind: problem
slug: feedback-vertex-set-problem
name: Feedback vertex set problem
aliases:
- cycle transversal problem
area: graphs/paths-and-cycles
level: advanced
summary: Find a smallest set of vertices whose removal leaves a forest, or a DAG for directed graphs. NP-hard; 2-approximable and FPT on undirected graphs.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(2^n (n + m))}
prereqs: [tree, induced-subgraph, vertex-cover, np-hard]
see_also: [feedback-arc-set-problem, directed-feedback-vertex-set, parameterized-feedback-vertex-set, iterative-compression, odd-cycle-transversal, cycle-detection, girth, vertex-cover]
sources:
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 85 to 103 (1972)
    locator: the list of 21 problems (feedback node set, for directed graphs, reduced from vertex cover)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman (1979)
    locator: Appendix A1.1, problem GT7 (feedback vertex set) and its comments
  - paper: "Vineet Bafna, Piotr Berman and Toshihiro Fujito, A 2-approximation algorithm for the undirected feedback vertex set problem, SIAM Journal on Discrete Mathematics 12(3), 289 to 297 (1999)"
    locator: the whole paper (a 2-approximation for weighted undirected feedback vertex set)
  - paper: "Ann Becker and Dan Geiger, Optimization of Pearl's method of conditioning and greedy-like approximation algorithms for the vertex feedback set problem, Artificial Intelligence 83(1), 167 to 188 (1996)"
    locator: the whole paper (a 2-approximation, found independently)
  - paper: "Guy Even, Joseph Naor, Baruch Schieber and Madhu Sudan, Approximating minimum feedback sets and multicuts in directed graphs, Algorithmica 20(2), 151 to 174 (1998)"
    locator: the whole paper (an O(log n log log n) approximation for directed graphs)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer (2015)
    locator: Chapters 3 to 5 and 9, the feedback vertex set examples (branching, iterative compression, randomized methods, kernels)
  - paper: "Paul Erdős and Lajos Pósa, On independent circuits contained in a graph, Canadian Journal of Mathematics 17, 347 to 352 (1965)"
    locator: the main theorem (k disjoint cycles or a feedback vertex set of size O(k log k))
  - paper: "Jianer Chen, Yang Liu, Songjian Lu, Barry O'Sullivan and Igor Razgon, A fixed-parameter algorithm for the directed feedback vertex set problem, Journal of the ACM 55(5), article 21 (2008)"
    locator: the whole paper (directed feedback vertex set is fixed-parameter tractable)
---

The feedback vertex set problem asks for a smallest set $X$ of vertices such that $G - X$ has no cycle: a forest if $G$ is undirected, a [directed acyclic graph](/directed-acyclic-graph/) if $G$ is directed. It is [NP-hard](/np-hard/) in both forms; the directed form is one of [Karp's 21 problems](/karps-21-np-complete-problems/). On undirected graphs it has a polynomial 2-approximation and is [fixed-parameter tractable](/fixed-parameter-tractable/) in the size of the answer. Trying all $2^n$ vertex sets with a [cycle test](/cycle-detection/) solves it exactly in $O(2^n (n + m))$ time.

## In plain words

A network has loops, and loops cause trouble: a signal can go round for ever, or a set of programs can wait for each other for ever. The aim is to remove as few points of the network as possible so that no loop is left.

Every loop must lose at least one of its points. A single point can be on many loops, so a good choice removes points that many loops share. No fast method is known that always finds the smallest choice. A simple fast method finds a choice at most twice as large as the smallest one when the links have no direction.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n$ vertices and $m$ edges, undirected or directed. Parallel edges and [self-loops](/self-loop/) are allowed, so $G$ may be a [multigraph](/multigraph/). In the weighted form each vertex has a weight $w(v) \ge 0$.

**Output.** A set $X \subseteq V$ of smallest size (or weight) such that the [induced subgraph](/induced-subgraph/) $G - X$ has no cycle. The minimum is written $\tau(G)$ here; for undirected graphs it is also called the decycling number.

**Decision form.** Given $G$ and $k$, is there a feedback vertex set with at most $k$ vertices? This is NP-complete for both forms.

**Conventions.** A self-loop at $v$ is a cycle of length 1, so $v$ is in every feedback vertex set. In an undirected multigraph, two parallel edges between $u$ and $v$ form a cycle of length 2, so $u$ or $v$ must be removed; in a directed graph, the opposite arcs $u \to v$ and $v \to u$ do the same, while two parallel arcs in the same direction do not form a cycle. Isolated vertices are never needed.

## Variants

- **Weighted.** Minimise $w(X)$.
- **Directed.** Make the graph acyclic; see [directed feedback vertex set](/directed-feedback-vertex-set/) for the parameterized version.
- **Arc version.** Remove arcs instead of vertices: the [feedback arc set problem](/feedback-arc-set-problem/). For undirected graphs the edge version is easy, with answer $m - n + c$.
- **Odd cycles.** Remove vertices to destroy only the odd cycles, that is, to make the graph bipartite: [odd cycle transversal](/odd-cycle-transversal/).
- **Parameterized.** Decide whether $\tau(G) \le k$ in time $f(k) \cdot n^{O(1)}$: [parameterized feedback vertex set](/parameterized-feedback-vertex-set/).
- **Disjoint cycles.** The dual packing problem asks for the largest number of vertex-disjoint cycles $\nu(G)$; always $\nu(G) \le \tau(G)$.

## Examples

**Complete graphs.** $\tau(K_n) = n - 2$ for $n \ge 2$: any three remaining vertices form a triangle, and two remaining vertices form an edge.

**Petersen graph.** $\tau = 3$. Removing $k$ vertices of a 3-regular graph deletes at most $3k$ edges, and a forest on $n - k$ vertices has at most $n - k - 1$ edges, so $15 - 3k \le 9 - k$ and $k \ge 3$; a search finds a set of 3 that works.

**Directed example.** Take arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 1$, $3 \to 4$, $4 \to 2$. All three directed cycles pass through vertex $2$, so $\tau = 1$, while the arc version needs 2 arcs.

**Forests and DAGs.** $\tau = 0$ exactly when the graph is a forest (undirected) or a DAG (directed), which a [depth-first search](/dfs-cycle-detection/) checks in $O(n + m)$ time.

**Self-loops and parallel edges.** The undirected multigraph with a loop at $0$, two parallel edges $1 2$ and an isolated vertex $3$ has $\tau = 2$: vertex $0$, and one of $1, 2$.

## Known algorithms

| algorithm | input | guarantee | time |
|---|---|---|---|
| all subsets with a cycle test | both | exact | $O(2^n (n + m))$ |
| subset DP for directed graphs | directed | exact | $O(2^n n)$ |
| Bafna, Berman and Fujito (1999); Becker and Geiger (1996) | undirected, weighted | ratio 2 | polynomial |
| Even, Naor, Schieber and Sudan (1998) | directed, weighted | ratio $O(\log n \log \log n)$ | polynomial |
| [iterative compression](/iterative-compression/), branching, randomized methods | undirected | exact, FPT in $k$ | $c^k \cdot n^{O(1)}$ |
| Chen, Liu, Lu, O'Sullivan and Razgon (2008) | directed | exact, FPT in $k$ | $f(k) \cdot n^{O(1)}$ |

**Subset DP for directed graphs.** A vertex set $S$ induces a DAG if and only if $S$ is empty or some $v \in S$ has no in-arc from $S$ and $S \setminus \{v\}$ induces a DAG, because every nonempty DAG has a source (see the [DAG source lemma](/dag-source-lemma/)). With the in-neighbours of each vertex stored as a bit mask, the test for $v$ costs $O(1)$ word operations, so all $2^n$ sets are classified in $O(2^n n)$ time, and $\tau(G) = n - \max \{ |S| : S \text{ induces a DAG} \}$. Self-loops are handled because $v$ is then an in-neighbour of itself. Tested against brute force over all vertex subsets on 600 random directed multigraphs with up to 5 vertices, it gave the same value every time.

**Reduction rules.** In an undirected graph, a vertex of degree at most 1 lies on no cycle and can be deleted; a vertex of degree 2 can be bypassed by an edge between its neighbours, which may create a parallel edge or a loop. After these rules a graph has minimum degree 3, and such a graph has a cycle of length at most $2 \log_2 n + 1$, which bounds the branching. Kernels with $O(k^2)$ vertices follow from these rules and further ones; see the textbook by Cygan and others.

**Fixed-parameter algorithms.** For undirected graphs the textbook by Cygan and others gives deterministic algorithms by branching and by iterative compression, and a simple randomized algorithm with running time $4^k \cdot n^{O(1)}$. For directed graphs, fixed-parameter tractability was open for many years and was settled by Chen and others in 2008.

## Bounds

**NP-hardness.** Karp (1972) proved the directed form NP-complete. The undirected form is also NP-complete (Garey and Johnson, GT7), by the reduction from [vertex cover](/vertex-cover/) below.

**Approximation hardness.** Both reductions below keep the size of the answer, so the known lower bounds for vertex cover apply: no ratio better than 1.36 unless P = NP, and no ratio $2 - \varepsilon$ under the [Unique Games Conjecture](/unique-games-conjecture/). Hence the ratio 2 is optimal for undirected graphs under that conjecture. For directed graphs, no constant ratio is known.

**Counting lower bound.** If $G$ is undirected and connected with maximum degree $\Delta \ge 2$, then $\tau(G) \ge (m - n + 1)/(\Delta - 1)$: removing $k$ vertices deletes at most $k\Delta$ edges, and the remaining forest on $n - k$ vertices has at most $n - k - 1$ edges. The Petersen graph meets this bound.

**Erdős-Pósa property.** Erdős and Pósa (1965) proved that every graph either has $k$ vertex-disjoint cycles or a feedback vertex set of size $O(k \log k)$, and the $k \log k$ order is tight.

## Reductions

**Vertex cover to directed feedback vertex set.** Replace each edge $uv$ of $H$ by the two arcs $u \to v$ and $v \to u$. The directed cycles of length 2 are exactly the edges, so a feedback vertex set covers all edges. Conversely, a vertex cover meets every directed cycle, because every arc of a cycle comes from an edge of $H$ and the cycle contains both ends of that arc.

**Vertex cover to undirected feedback vertex set on simple graphs.** For each edge $uv$ of $H$ add a new vertex $x_{uv}$ adjacent to $u$ and $v$. If $C$ covers $H$, then in $G - C$ the old vertices form an independent set and each $x_{uv}$ keeps at most one neighbour, so $G - C$ is a forest. Conversely, a feedback vertex set must meet each triangle $u, v, x_{uv}$, and if it contains $x_{uv}$ it can use $u$ instead, so the smallest one is a vertex cover of $H$. With multigraphs, doubling each edge gives the same result more directly.

Both reductions were checked by brute force on 500 random graphs with up to 5 vertices.

**Arc and vertex versions.** The [feedback arc set problem](/feedback-arc-set-problem/) and directed feedback vertex set reduce to each other by subdividing arcs and splitting vertices.

## Applications

- **Deadlock recovery.** Choose the fewest processes to abort so that the [wait-for graph](/wait-for-graph/) has no cycle.
- **Probabilistic inference.** In Pearl's method of conditioning on a [Bayesian network](/bayesian-network/), fixing the variables of a feedback vertex set leaves a tree-like network on which inference is easy; this motivated the Becker and Geiger algorithm.
- **Circuit testing and verification.** Scan registers placed at a feedback vertex set break all loops of a sequential circuit.
- **Combinatorial structure.** Graphs with a small feedback vertex set have small [treewidth](/treewidth/), so many hard problems become tractable on them.

## References
