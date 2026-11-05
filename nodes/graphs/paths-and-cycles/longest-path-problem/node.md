---
tag: 27BGH7
kind: problem
slug: longest-path-problem
name: Longest path problem
aliases:
- longest simple path problem
area: graphs/paths-and-cycles
level: intro
summary: Find a simple path of maximum length or weight; NP-hard in general, but linear-time on DAGs and trees.
prereqs: [simple-path, hamiltonian-path-problem, np-hard]
see_also: [dag-longest-path, tree-diameter, k-path-color-coding, longest-to-shortest-paths-reduction, critical-path, hamiltonian-path, held-karp-algorithm, shortest-path-optimal-substructure]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A2 (network design), the problem Longest path, NP-complete by a reduction from Hamiltonian path, and solvable in polynomial time for acyclic digraphs
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.3, Elements of dynamic programming (the unweighted longest simple path problem as an example without optimal substructure), and Section 22.2 (single-source shortest paths in directed acyclic graphs, and critical paths)
  - paper: David Karger, Rajeev Motwani and G. D. S. Ramkumar, On approximating the longest path in a graph, Algorithmica 18(1), 1997
    title: Karger, Motwani and Ramkumar, hardness of approximating the longest path
    locator: the main hardness theorems (no constant-factor approximation unless P = NP)
  - paper: doi:10.1145/210332.210337
    title: Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844 to 856 (1995)
    locator: the algorithms for simple paths of length k
  - paper: Kyriaki Ioannidou, George B. Mertzios and Stavros D. Nikolopoulos, The longest path problem has a polynomial solution on interval graphs, Algorithmica 61(2), 2011
    title: Ioannidou, Mertzios and Nikolopoulos, longest paths in interval graphs
    locator: the main theorem
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 5 (Randomized methods in parameterized algorithms), color coding for Longest Path
---

The longest path problem asks for a [simple path](/simple-path/) with the most edges, or with the largest total weight, in a graph. It looks like the shortest path problem with max in place of min, but it is much harder: a simple path with $n - 1$ edges is a [Hamiltonian path](/hamiltonian-path/), so the problem is [NP-hard](/np-hard/). The path must be simple, because a walk can go around a cycle forever. On a [directed acyclic graph](/directed-acyclic-graph/) every walk is simple, and a [dynamic program over a topological order](/dag-longest-path/) solves it in linear time; on a tree it is the [diameter](/tree-diameter/).

## In plain words

You walk through a park along its paths, and you may never pass the same crossing twice. How long a walk can you make?

For the shortest way between two places there are fast methods, because a shortest way is made of shortest pieces. A longest way is not made of longest pieces: the best route to a middle point may use crossings that the rest of the route needs. No fast method is known for a general park, and the question "can you visit every crossing once?" is a special case of it.

If all paths are one-way and you can never come back to a crossing, the problem becomes easy: work through the crossings in their one-way order and keep the longest way to each of them.

## Definition

**Input.** A finite graph $G = (V, E)$ with $n = |V| \ge 1$, directed or undirected, and optionally edge weights $w : E \to \mathbb{R}$. Without weights, every edge has weight 1. The graph may be a [multigraph](/multigraph/) with [self-loops](/self-loop/): a simple path uses no loop, and of parallel edges it uses at most one, so only the heaviest edge between two vertices matters. Isolated vertices are allowed; each is a path of length 0.

**Output.** A simple path $P = (v_0, e_1, v_1, \ldots, e_k, v_k)$, with $v_0, \ldots, v_k$ distinct, that maximizes $w(P) = \sum_{i=1}^{k} w(e_i)$. In the unweighted case this is the number of edges $k$, at most $n - 1$.

**Decision version.** Given $G$ and an integer $K$, is there a simple path with at least $K$ edges? It is [NP-complete](/np-complete/): a path with at least $K$ edges is a certificate checked in $O(n + m)$ time.

**With ends.** The $s$-$t$ version fixes the first and last vertices; the single-source version fixes only the first.

**Why simple.** Without the condition, a walk that reaches a cycle of positive weight has no maximum. In a directed acyclic graph every walk is a simple path, so the condition costs nothing there.

## Variants

- **Weighted or unweighted.** Unit weights count edges. With weights of any sign, the problem contains the unweighted one, and on a DAG both are linear.
- **Longest path in a DAG.** Linear time by [dynamic programming over a topological order](/dag-longest-path/); see also the [critical path](/critical-path/) of a project.
- **Longest path in a tree.** The diameter; two breadth-first searches find it in $O(n)$ time, see [tree diameter](/tree-diameter/).
- **$k$-path.** Is there a simple path with $k$ vertices? This is the parameterized form; see [color coding for $k$-path](/k-path-color-coding/) and [parameterized longest path](/parameterized-longest-path/).
- **Longest cycle.** Find a simple cycle of maximum length, the *circumference* of the graph. The answer is $n$ exactly when the graph has a [Hamiltonian cycle](/hamiltonian-cycle/).
- **Longest induced path.** The path must also have no edge between non-consecutive vertices. It is also NP-hard.
- **Longest trail.** Repeated vertices are allowed but repeated edges are not; with all edges used this is an [Eulerian path](/eulerian-path/). In general it is also NP-hard.

## Examples

**A square with two tails.** Take the undirected graph with edges $01, 12, 23, 30, 04, 25$: a square $0, 1, 2, 3$ with a pendant vertex 4 at 0 and a pendant vertex 5 at 2. A longest simple path has 4 edges, for example $(4, 0, 1, 2, 5)$ or $(1, 0, 3, 2, 5)$. No simple path has 5 edges: it would be a Hamiltonian path, whose ends must be the two pendant vertices 4 and 5, and then it would read $4, 0, x, 2, 5$ with only one of 1 and 3 between 0 and 2.

**No optimal substructure.** In the triangle with vertices $a, b, c$, the longest $a$-$c$ path is $(a, b, c)$ with 2 edges. Its part from $a$ to $b$ has 1 edge, but the longest $a$-$b$ path is $(a, c, b)$ with 2 edges. So a longest path need not be made of longest paths, unlike a shortest path (see [optimal substructure of shortest paths](/shortest-path-optimal-substructure/)). The longest $a$-$b$ path uses $c$, which the $b$-$c$ part also needs, and this is why the shortest path methods do not carry over.

**A weighted DAG.** Arcs $0 \to 1$ (weight 3), $0 \to 2$ (2), $2 \to 1$ (4), $1 \to 3$ (2), $2 \to 3$ (1), $3 \to 4$ (5). A topological order is $0, 2, 1, 3, 4$. The longest path weights $L$ from vertex 0 are $L(0) = 0$, $L(2) = 2$, $L(1) = \max(0 + 3, 2 + 4) = 6$, $L(3) = \max(6 + 2, 2 + 1) = 8$ and $L(4) = 8 + 5 = 13$, along $0, 2, 1, 3, 4$. The shortest path from 0 to 4 is $0, 1, 3, 4$ with weight 10.

**Self-loops and isolated vertices.** A loop at every vertex of a path graph changes nothing: loops are never used. The graph with one edge $01$ and an isolated vertex 2 has longest path length 1.

**A directed cycle.** In the directed cycle $0 \to 1 \to \cdots \to n - 1 \to 0$, the longest simple path has $n - 1$ edges, but the walks have no longest one.

## Known algorithms

- **Directed acyclic graphs: $O(n + m)$.** Process the vertices in topological order and set $L(v) = \max(0, \max_{(u, v) \in E} L(u) + w(u, v))$, the best weight of a path that ends at $v$. Equivalently, negate the weights and compute shortest paths, the [longest-to-shortest reduction](/longest-to-shortest-paths-reduction/), which is correct exactly because a DAG has no cycle. See [DAG longest path](/dag-longest-path/).
- **Trees: $O(n)$.** Two breadth-first searches for unit weights, two depth-first passes for nonnegative weights; see [tree diameter](/tree-diameter/).
- **Subset dynamic programming: $O(2^n n^2)$.** Let $B(S, v)$ be the largest weight of a simple path with vertex set exactly $S$ that ends at $v$. Then $B(\{v\}, v) = 0$ and $B(S, v) = \max_{u} B(S \setminus \{v\}, u) + w(u, v)$ over $u \in S \setminus \{v\}$ with $(u, v) \in E$. The answer is the largest finite $B(S, v)$. This is the [Held-Karp](/held-karp-algorithm/) table with max in place of min, using $O(2^n n)$ space.
- **Color coding: $2^{O(k)} m$ expected time** for a simple path with $k$ vertices (Alon, Yuster and Zwick, 1995), so the problem is [fixed-parameter tractable](/fixed-parameter-tractable/) in the length; see [color coding for $k$-path](/k-path-color-coding/).
- **Backtracking.** Extend paths by depth-first search and keep the best one. $O(n!)$ in the worst case, but practical on small or sparse graphs.
- **Special classes.** Polynomial algorithms are known for some graph classes, such as interval graphs (Ioannidou, Mertzios and Nikolopoulos, 2011), and graphs of bounded [treewidth](/treewidth/).

## Bounds

- **NP-hardness.** The decision version is NP-complete for directed and undirected graphs, also without weights (Garey and Johnson). It holds already for $K = n - 1$, which is the [Hamiltonian path problem](/hamiltonian-path-problem/).
- **Approximation.** Karger, Motwani and Ramkumar (1997) show that no polynomial algorithm finds, on every graph, a path whose length is within a constant factor of the longest, unless P = NP; under stronger assumptions the factor cannot even be $2^{\log^{1 - \varepsilon} n}$. This holds even for Hamiltonian graphs, where the longest path has $n - 1$ edges.
- **Exact time.** $O^*(2^n)$ by the subset dynamic program, or by the faster Hamiltonian path methods applied to all subsets. Under the Exponential Time Hypothesis, no $2^{o(n)}$ algorithm exists, since the reduction from Hamiltonian path keeps $n$.
- **Parameterized.** $2^{O(k)} \mathrm{poly}(n)$ for a path with $k$ vertices; see [parameterized longest path](/parameterized-longest-path/).
- **Easy cases.** $O(n + m)$ on DAGs, $O(n)$ on trees.

## Reductions

- **From Hamiltonian path.** $G$ has a Hamiltonian path if and only if its longest simple path has $n - 1$ edges. This reduction is the identity map with $K = n - 1$, and it proves NP-hardness.
- **To Hamiltonian path.** Conversely, a $K$-edge path exists if and only if some set of $K + 1$ vertices induces a subgraph with a Hamiltonian path; this gives the subset method, not a polynomial reduction.
- **From and to shortest paths.** Negating the weights turns a longest simple path into a shortest simple path. On a DAG the negated graph has no cycle, so ordinary shortest path algorithms apply. In a general graph, every cycle of positive weight becomes a [negative cycle](/negative-cycle/), and shortest *simple* paths in graphs with negative cycles are NP-hard by the same argument.
- **Weighted to unweighted.** For DAGs no reduction is needed. In general, the unweighted problem is the special case with all weights 1, so the weighted problem is at least as hard.

## Applications

- **Project scheduling.** In a DAG of tasks with durations, the longest path is the [critical path](/critical-path/): its length is the shortest time in which the project can end, and its tasks cannot be delayed without delaying the project.
- **Dynamic programming.** Many dynamic programs, such as longest increasing subsequence and edit distance with scores, are longest or shortest paths in a DAG of states.
- **Circuit timing.** The delay of a combinational circuit is the longest path in its DAG of gates.
- **Hardness proofs and benchmarks.** The longest path and $k$-path problems are standard sources of NP-hardness and standard test cases for parameterized algorithms.

## References
