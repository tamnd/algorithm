---
tag: F6NG6T
kind: problem
slug: odd-cycle-transversal
name: Odd cycle transversal
aliases:
- OCT
- bipartization
area: complexity/parameterized-complexity
level: advanced
summary: "Delete at most k vertices so that the rest of the graph is bipartite. NP-hard, but FPT in k: 3^k n^O(1) by iterative compression, 2.3146^k n^O(1) by linear programming."
prereqs: [bipartite-graph, fixed-parameter-tractable, iterative-compression]
see_also: [iterative-compression, parameterized-vertex-cover, parameterized-feedback-vertex-set, bipartite-testing, max-flow-min-cut-theorem, kernelization, bounded-degree-deletion, strong-exponential-time-hypothesis]
sources:
  - paper: doi:10.1016/j.orl.2003.10.009
    title: "Bruce Reed, Kaleigh Smith and Adrian Vetta, Finding odd cycle transversals, Operations Research Letters 32(4), 299-301 (2004)"
    locator: the first FPT algorithm, by iterative compression and minimum cuts
  - paper: doi:10.1145/2566616
    title: "Daniel Lokshtanov, N. S. Narayanaswamy, Venkatesh Raman, M. S. Ramanujan and Saket Saurabh, Faster parameterized algorithms using linear programming, ACM Transactions on Algorithms 11(2) (2014)"
    locator: odd cycle transversal in time O*(2.3146^k), through vertex cover above a matching
  - paper: doi:10.1145/2635810
    title: "Stefan Kratsch and Magnus Wahlström, Compression via matroids: a randomized polynomial kernel for odd cycle transversal, ACM Transactions on Algorithms 10(4) (2014)"
    locator: the randomized polynomial kernel
  - paper: doi:10.1016/0022-0000(80)90060-4
    title: "John M. Lewis and Mihalis Yannakakis, The node-deletion problem for hereditary properties is NP-complete, Journal of Computer and System Sciences 20(2), 219-230 (1980)"
    locator: NP-completeness of vertex deletion to any nontrivial hereditary property, which includes bipartite graphs
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 4, Iterative compression, Section 4.4, Odd Cycle Transversal, p. 91
---

Odd cycle transversal asks whether at most $k$ vertices can be deleted from a graph so that the rest is [bipartite](/bipartite-graph/). A graph is bipartite exactly when it has no cycle of odd length, so the deleted set must meet every odd cycle, which gives the name. The problem is NP-hard, because bipartite graphs form a hereditary class (Lewis and Yannakakis, 1980). With the solution size $k$ as the [parameter](/parameter/) it is [fixed-parameter tractable](/fixed-parameter-tractable/): Reed, Smith and Vetta (2004) solved it in time $3^k n^{O(1)}$ with a new technique, [iterative compression](/iterative-compression/), and Lokshtanov, Narayanaswamy, Raman, Ramanujan and Saurabh (2014) lowered the base to $2.3146$. Kratsch and Wahlström (2014) gave a randomized polynomial kernel. This page treats the parameterized problem; the test for whether a graph is already bipartite is on [bipartite testing](/bipartite-testing/).

## In plain words

You have a network and you want to split its points into two teams so that every link joins two different teams. Some networks cannot be split like this, because they contain a loop with an odd number of points.

So you may remove a few points first. The question is whether removing at most $k$ points is enough to make the split possible.

This is hard in general. But when $k$ is small, there are methods whose cost grows fast with $k$ and only slowly with the size of the network. The best known one guesses how the removed points and their neighbors should be split, and then uses a flow computation to finish the job.

## Definition

A graph $G = (V, E)$ is bipartite if $V$ splits into two independent sets. A set $X \subseteq V$ is an *odd cycle transversal* if $G - X$ is bipartite.

**ODD-CYCLE-TRANSVERSAL**

- Instance: a graph $G = (V, E)$ and an integer $k$.
- Parameter: $k$.
- Question: is there a set $X \subseteq V$ with $|X| \le k$ such that $G - X$ is bipartite?

A certificate is the set $X$. It is checked in $O(n + m)$ time by a 2-coloring of $G - X$ with a graph search. The smallest size of an odd cycle transversal of $G$ is written $\mathrm{oct}(G)$.

## Variants

- *Edge bipartization.* Delete at most $k$ edges instead of vertices. This is also FPT in $k$, by iterative compression.
- *Weighted.* Each vertex has a weight, and the deleted set must have total weight at most $w$ and at most $k$ vertices.
- *Above a guarantee.* In the reduction to vertex cover below, the vertex cover number of an auxiliary graph is at least $n$, and the parameter is the excess over $n$. Parameters above such lower bounds are the basis of the $2.3146^k$ algorithm.

## Examples

Brute force over all vertex sets gives:

| graph | $n$ | $m$ | $\mathrm{oct}$ | number of minimum solutions |
|---|---|---|---|---|
| cycle $C_5$ | 5 | 5 | 1 | 5 |
| complete graph $K_4$ | 4 | 6 | 2 | 6 |
| complete graph $K_5$ | 5 | 10 | 3 | 10 |
| wheel $W_5$ (hub and 5-cycle) | 6 | 10 | 2 | 5 |
| triangular prism | 6 | 9 | 2 | 9 |
| Petersen graph | 10 | 15 | 3 | 30 |

For $K_n$, the rest must have at most 2 vertices, so $\mathrm{oct}(K_n) = n - 2$. In the wheel $W_5$, the hub lies on five triangles, and without the hub three rim vertices are needed to break them. So every minimum solution is the hub plus one rim vertex, which breaks the outer 5-cycle.

## Known algorithms

All bounds are on a word RAM; $O^*$ hides factors polynomial in $n$.

- Brute force over all sets of at most $k$ vertices takes $n^{k} \cdot O(n + m)$ time, which is an [XP](/xp/) algorithm and not FPT.
- Reed, Smith and Vetta (2004) solve it in time $3^k n^{O(1)}$ by [iterative compression](/iterative-compression/): with a solution of size $k + 1$, guess for each of its vertices whether it is deleted or on which side it goes, and finish with a minimum vertex cut by [max flow](/max-flow-min-cut-theorem/).
- Lokshtanov, Narayanaswamy, Raman, Ramanujan and Saurabh (2014) solve it in time $O^*(2.3146^k)$, through vertex cover above a matching and a branching guided by linear programming.
- Kratsch and Wahlström (2014) give a randomized polynomial kernel: an equivalent instance of size polynomial in $k$, computed in polynomial time with a small chance of error, built from a matroid that encodes the cut structure.

## Bounds

- *NP-hardness.* Vertex deletion to bipartite graphs is NP-complete (Lewis and Yannakakis, 1980), so no polynomial algorithm exists unless P = NP.
- *Exponential time.* The reduction from vertex cover below keeps $k$ unchanged and adds only $m$ vertices. So, under the exponential time hypothesis, there is no algorithm in time $2^{o(k)} n^{O(1)}$. The exponential time hypothesis is the weaker cousin of the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/).
- *Kernels.* A randomized polynomial kernel exists. No deterministic polynomial kernel is known.

## Reductions

- *From vertex cover.* Given $G$, replace every edge $uv$ by a triangle $u, v, w_{uv}$ with a new vertex $w_{uv}$. A vertex cover $C$ of $G$ is an odd cycle transversal of the new graph: what remains is an independent set of $G$ and the new vertices, each of which keeps at most one neighbor, so the rest is a forest. Conversely, an odd cycle transversal must meet each triangle, and replacing each $w_{uv}$ in it by $u$ gives a vertex cover of $G$ of the same size or smaller. So [vertex cover](/parameterized-vertex-cover/) with parameter $k$ reduces to odd cycle transversal with parameter $k$.
- *To vertex cover above a matching.* Take two copies $v_1, v_2$ of each vertex $v$, the edges $u_1 v_1$ and $u_2 v_2$ for every edge $uv$ of $G$, and the matching edges $v_1 v_2$. Every vertex cover of this graph has at least $n$ vertices because of the matching, and the smallest one has exactly $n + \mathrm{oct}(G)$ vertices. From a minimum cover, the vertices $v$ with both copies in the cover form an odd cycle transversal. On all six graphs of the table, a brute-force check gives the vertex cover number $n + \mathrm{oct}(G)$, for example $10 + 3 = 13$ for the Petersen graph.
- *To almost 2-SAT.* Vertex cover above a matching is equivalent to deleting at most $k$ clauses from a 2-CNF formula to make it satisfiable, which is how the linear programming algorithms are applied.

## Applications

- *Constraint graphs.* When variables are linked by constraints of the form "these two take different values of two", the constraint graph must be bipartite. An odd cycle transversal is a smallest set of variables to drop so that the rest can be satisfied.
- *Conflict graphs from data.* When two groups of items must be separated and a graph records which items conflict, the graph should be bipartite. A small transversal points to the items whose data is most likely wrong.
- *A model problem.* The problem was the first use of iterative compression, and its randomized kernel started the use of matroids in kernelization. Both tools now apply to many other deletion problems.

## References
