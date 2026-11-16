---
tag: 3BMX12
kind: problem
slug: parameterized-feedback-vertex-set
name: Parameterized feedback vertex set
aliases:
- k-feedback vertex set
- FVS
area: complexity/parameterized-complexity
level: advanced
summary: "Delete at most k vertices so that the rest of an undirected graph has no cycle. FPT in k: deterministic 3.460^k n^O(1), randomized 2.7^k n^O(1), and a kernel with 4k^2 vertices."
prereqs: [feedback-vertex-set-problem, fixed-parameter-tractable]
see_also: [feedback-vertex-set-problem, iterative-compression, odd-cycle-transversal, directed-feedback-vertex-set, cut-and-count, kernelization, treewidth, bidimensionality-theory]
sources:
  - paper: doi:10.1145/1721837.1721848
    title: "Stéphan Thomassé, A 4k^2 kernel for feedback vertex set, ACM Transactions on Algorithms 6(2) (2010)"
    locator: the kernel with at most 4k^2 vertices
  - paper: doi:10.1016/j.ipl.2014.05.001
    title: "Tomasz Kociumaka and Marcin Pilipczuk, Faster deterministic feedback vertex set, Information Processing Letters 114(10), 556-560 (2014)"
    locator: deterministic time 3.619^k n^O(1) by iterative compression
  - paper: doi:10.1007/s00453-021-00815-w
    title: "Yoichi Iwata and Yusuke Kobayashi, Improved analysis of highest-degree branching for feedback vertex set, Algorithmica 83(8), 2503-2520 (2021)"
    locator: deterministic time 3.460^k n^O(1)
  - paper: doi:10.1145/3504027
    title: "Jason Li and Jesper Nederlof, Detecting feedback vertex sets of size k in O*(2.7^k) time, ACM Transactions on Algorithms 18(4), article 34 (2022)"
    locator: the randomized algorithm in time O*(2.7^k)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: feedback vertex set as a running example, in Chapter 4 (Iterative compression) and Chapter 5 (Randomized methods in parameterized algorithms)
---

Parameterized feedback vertex set asks whether at most $k$ vertices can be deleted from an undirected graph so that no cycle is left, that is, so that the rest is a forest. The parameter is the solution size $k$. The problem is NP-hard, and the general problem, its approximation and its directed form are on the page [feedback vertex set](/feedback-vertex-set-problem/). This page gives the parameterized view. The problem is [fixed-parameter tractable](/fixed-parameter-tractable/), and it has been a test bed for most techniques in the field: [bounded search trees](/bounded-search-tree/), [iterative compression](/iterative-compression/), random sampling, [cut and count](/cut-and-count/) and kernelization. The best known bounds are deterministic time $3.460^k n^{O(1)}$ (Iwata and Kobayashi, 2021), randomized time $2.7^k n^{O(1)}$ (Li and Nederlof), and a kernel with $4k^2$ vertices (Thomassé, 2010).

## In plain words

You have a network with some loops in it, and you want to break all the loops by removing at most $k$ points. A network with no loops is a forest: a set of trees.

Removing one point can break many loops at once, so the choice matters. Points that touch only one or two links never need to be removed, which already makes the network simpler.

The problem is hard in general. But when $k$ is small, there are methods whose cost grows fast with $k$ and only slowly with the size of the network. You can also shrink any input to an equivalent one whose size depends only on $k$.

## Definition

A *feedback vertex set* of an undirected graph $G = (V, E)$ is a set $X \subseteq V$ such that $G - X$ is a forest.

**FEEDBACK-VERTEX-SET**

- Instance: an undirected graph $G = (V, E)$, which may have loops and parallel edges, and an integer $k$.
- Parameter: $k$.
- Question: is there a feedback vertex set $X$ with $|X| \le k$?

A certificate is the set $X$, checked in $O(n + m)$ time with a union-find pass or a graph search over $G - X$. Loops and parallel edges are allowed because the reduction rules create them: a vertex with a loop must be in every solution, and two parallel edges form a cycle of length 2. The smallest size of a feedback vertex set of $G$ is written $\mathrm{fvs}(G)$.

## Variants

- *Directed graphs.* [Directed feedback vertex set](/directed-feedback-vertex-set/) asks for a set that meets every directed cycle. It is also FPT in $k$, but much harder, and has its own page.
- *Weighted.* Each vertex has a weight, and the set must have weight at most $w$ and at most $k$ vertices.
- *Subset feedback vertex set.* Only cycles through a given set of terminals must be broken. This is FPT in $k$ too.
- *Other parameters.* Since $\mathrm{tw}(G) \le \mathrm{fvs}(G) + 1$, the feedback vertex set number bounds the [treewidth](/treewidth/), and problems that are FPT in treewidth are FPT in it as well. On planar graphs the problem is solvable in time $2^{O(\sqrt{k})} n^{O(1)}$ by [bidimensionality](/bidimensionality-theory/).

## Examples

Brute force over all vertex sets gives:

| graph | $n$ | $m$ | $\mathrm{fvs}$ | minimum solutions | $\mathrm{oct}$ |
|---|---|---|---|---|---|
| cycle $C_5$ | 5 | 5 | 1 | 5 | 1 |
| complete graph $K_4$ | 4 | 6 | 2 | 6 | 2 |
| complete graph $K_5$ | 5 | 10 | 3 | 10 | 3 |
| wheel $W_5$ (hub and 5-cycle) | 6 | 10 | 2 | 5 | 2 |
| triangular prism | 6 | 9 | 2 | 6 | 2 |
| $3 \times 3$ grid | 9 | 12 | 2 | 10 | 0 |
| $K_{3,3}$ | 6 | 9 | 2 | 6 | 0 |
| Petersen graph | 10 | 15 | 3 | 20 | 3 |

The last column is the [odd cycle transversal](/odd-cycle-transversal/) number. A feedback vertex set is always an odd cycle transversal, so $\mathrm{oct}(G) \le \mathrm{fvs}(G)$, and the grid and $K_{3,3}$ show that the gap can be large: they are bipartite but have many cycles. In $K_{3,3}$ the 6 minimum solutions are the pairs of vertices on the same side; deleting one vertex from each side leaves a $K_{2,2}$, which is a 4-cycle.

## Known algorithms

All bounds are on a word RAM; $O^*$ hides factors polynomial in $n$.

- *Branching.* After the reduction rules, every vertex has degree at least 3, and a minimum solution contains one of the $3k$ vertices of largest degree. Branching on them gives $(3k)^k n^{O(1)}$. See [bounded search tree](/bounded-search-tree/).
- *Random sampling.* After the reduction rules, a random edge has an end in a fixed solution with probability at least $1/2$. Picking a random end of a random edge, $k$ times, finds a solution with probability at least $4^{-k}$, which gives a one-sided error algorithm in time $4^k n^{O(1)}$.
- *Iterative compression.* [Iterative compression](/iterative-compression/) with a branching for the disjoint step gives $5^k n^{O(1)}$, and a finer analysis by Kociumaka and Pilipczuk (2014) gives $3.619^k n^{O(1)}$, deterministic.
- *Branching on a vertex of highest degree.* Iwata and Kobayashi (2021) show that a simple branching on a vertex of highest degree, analyzed with a careful measure, runs in deterministic time $3.460^k n^{O(1)}$.
- *Cut and count.* [Cut and count](/cut-and-count/) gives randomized time $3^k n^{O(1)}$ with one-sided error.
- *Randomized, best known.* Li and Nederlof give randomized time $O^*(2.7^k)$ with one-sided error.
- *Kernel.* Thomassé (2010) gives a kernel with at most $4k^2$ vertices, computed in polynomial time.

## Bounds

- *NP-hardness.* The problem is NP-complete, since forests form a hereditary class. So no polynomial algorithm exists unless P = NP.
- *Exponential time.* Replace each edge $uv$ of a graph by a triangle $u, v, w_{uv}$. A vertex cover of the old graph is a feedback vertex set of the new one, and a feedback vertex set of the new one gives a vertex cover of the same size. So vertex cover reduces to the problem with the same $k$, and under the exponential time hypothesis no algorithm in time $2^{o(k)} n^{O(1)}$ exists. That hypothesis is the weaker cousin of the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/).
- *Kernel size.* The kernel with $O(k^2)$ vertices is likely close to the best possible: Dell and van Melkebeek showed that no kernel with $O(k^{2 - \varepsilon})$ bits exists for any $\varepsilon > 0$ unless $\mathsf{NP} \subseteq \mathsf{coNP/poly}$. See [kernel lower bounds](/kernel-lower-bounds/).

## Reductions

- *From vertex cover.* The triangle construction above keeps the parameter, so [vertex cover](/parameterized-vertex-cover/) reduces to feedback vertex set.
- *Reduction rules.* Delete a vertex of degree at most 1. Bypass a vertex of degree 2 by an edge between its two neighbors. Put a vertex with a loop into the solution and decrease $k$. Keep at most two parallel edges between two vertices. These rules keep the answer and are the start of every algorithm above.

## Applications

- *Probabilistic inference.* In Bayesian networks, the loop cutset problem asks for a set of variables whose fixing turns the network into a forest, so that inference by tree methods is possible for each fixed value. A small feedback vertex set gives a small number of cases.
- *Structural parameter.* Many problems are solved in time $f(\mathrm{fvs}) \cdot n^{O(1)}$ when the feedback vertex set number is small, since the rest of the graph is a forest.

## References
