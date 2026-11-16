---
tag: MFG7PM
kind: problem
slug: parameterized-steiner-tree
name: Parameterized Steiner tree
aliases:
- k-Steiner tree
area: complexity/parameterized-complexity
level: advanced
summary: "Connect k terminals by a tree of least weight. FPT in k: O*(3^k) by Dreyfus and Wagner, O*(2^k M) for integer weights at most M by fast subset convolution; W[2]-hard in the number of Steiner vertices."
prereqs: [steiner-tree-problem, fixed-parameter-tractable]
see_also: [steiner-tree-problem, cut-and-count, set-cover, kernel-lower-bounds, w-hardness, dijkstra, walsh-hadamard-transform, karps-21-np-complete-problems]
sources:
  - paper: doi:10.1002/net.3230010302
    title: "Stuart E. Dreyfus and Robert A. Wagner, The Steiner problem in graphs, Networks 1(3), 195-207 (1971)"
    locator: the dynamic program over subsets of terminals, O*(3^k)
  - paper: doi:10.1145/1250790.1250801
    title: "Andreas Björklund, Thore Husfeldt, Petteri Kaski and Mikko Koivisto, Fourier meets Möbius: fast subset convolution, STOC 2007, 67-74"
    locator: fast subset convolution in O(2^n n^2) ring operations, and Steiner tree in O*(2^k M) for integer weights at most M
  - paper: doi:10.1145/2650261
    title: "Michael Dom, Daniel Lokshtanov and Saket Saurabh, Kernelization lower bounds through colors and IDs, ACM Transactions on Algorithms 11(2), article 13 (2014)"
    locator: no polynomial kernel for Steiner tree parameterized by the number of terminals and the solution size unless NP is a subset of coNP/poly (conference version ICALP 2009)
  - paper: doi:10.1145/2925416
    title: "Marek Cygan, Holger Dell, Daniel Lokshtanov, Daniel Marx, Jesper Nederlof, Yoshio Okamoto, Ramamohan Paturi, Saket Saurabh and Magnus Wahlström, On problems as hard as CNF-SAT, ACM Transactions on Algorithms 12(3), article 41 (2016)"
    locator: no (2 - ε)^t n^O(1) algorithm for Steiner tree with t terminals unless the set cover conjecture fails (conference version CCC 2012)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 85-103 (1972)"
    locator: Steiner tree is NP-complete
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 6, Miscellaneous (dynamic programming over subsets, Steiner tree); Chapter 10, Algebraic techniques (subset convolution)
---

Parameterized Steiner tree is the [Steiner tree problem](/steiner-tree-problem/) in graphs with the number $k$ of terminals as the [parameter](/parameter/). It is [fixed-parameter tractable](/fixed-parameter-tractable/): Dreyfus and Wagner gave a dynamic program over subsets of terminals in $O^\ast(3^k)$ time in 1971, where $O^\ast$ hides factors polynomial in the input size. Björklund, Husfeldt, Kaski and Koivisto lowered this to $O^\ast(2^k M)$ for integer edge weights at most $M$, with fast subset convolution. No $(2 - \varepsilon)^k n^{O(1)}$ algorithm is expected, and there is no polynomial kernel even when the solution size is added to the parameter. With the number of non-terminal vertices in the tree as the parameter, the problem is W[2]-hard. This page gives the parameterized view; the Steiner tree page has the approximation algorithms.

## In plain words

You have a road map and a few towns that must be joined. You may build roads along the map, and you may pass through other places on the way. You want the cheapest set of roads that joins all the towns.

If there are only $k$ towns, you can build the answer from smaller answers: the best way to join a group of towns and one meeting point. A group of towns splits into two smaller groups at some meeting point. There are about $3^k$ ways to choose a group and split it, and for each one the work is polynomial in the size of the map. So the time grows fast with the number of towns but only slowly with the size of the map.

## Definition

- Instance: an undirected graph $G$ with $n$ vertices and $m$ edges, positive integer edge weights $w$, a set $T \subseteq V(G)$ of terminals with $|T| = k$, and an integer $\ell$.
- Parameter: $k$.
- Question: is there a subtree of $G$ that contains every vertex of $T$ and has total weight at most $\ell$?

The vertices of the tree that are not terminals are *Steiner vertices*. In the unweighted version all weights are 1, and the tree has at most $\ell$ edges.

## Variants

- **Parameter: the size $\ell$ of the solution.** In the unweighted version $k \le \ell + 1$, so this parameter is larger, and the problem is again FPT. The kernel lower bound below holds for $k + \ell$ together.
- **Parameter: the number $p$ of Steiner vertices.** W[2]-hard (see Reductions). So a solution with few extra vertices does not help.
- **Node-weighted Steiner tree.** Weights on vertices instead of edges. Dynamic programming over subsets of terminals works here as well.
- **Directed Steiner tree.** Find an arborescence from a root to all terminals. The Dreyfus and Wagner recurrence works for directed graphs with the same $3^k$ bound.
- **Treewidth as the parameter.** With a tree decomposition of width $t$, [cut and count](/cut-and-count/) solves the node version in $3^t n^{O(1)}$ time with a Monte Carlo algorithm.

## Examples

A scratch script built the $3 \times 4$ grid with vertices $(i, j)$, $0 \le i \le 2$, $0 \le j \le 3$, and 17 edges with random weights in $\{1, 2, 3\}$ (seed 7). The terminals are the four corners $(0, 0)$, $(0, 3)$, $(2, 0)$, $(2, 3)$.

- The Dreyfus and Wagner dynamic program gives weight 10, and brute force over all sets of Steiner vertices also gives 10.
- The optimal tree is unique. Its Steiner vertices are $(0, 2)$, $(1, 0)$, $(1, 1)$, $(1, 2)$, $(1, 3)$, and its 8 edges are $(0,0)(1,0)$ of weight 2, $(1,0)(1,1)$ of weight 2, and $(1,0)(2,0)$, $(1,1)(1,2)$, $(1,2)(0,2)$, $(0,2)(0,3)$, $(1,2)(1,3)$, $(1,3)(2,3)$ of weight 1 each.
- The shortest path distances between terminals are 3, 4, 5, 5, 6 and 6. A minimum spanning tree on these distances has weight $3 + 4 + 5 = 12$, the classical 2-approximation.
- The merge step of the recurrence ran 600 times. That is 12 vertices times 50 ordered splits, and $50 = 3^4 - 2 \cdot 2^4 + 1$ is the number of pairs $(S', S \setminus S')$ with $S \subseteq T$ and $\emptyset \ne S' \subsetneq S$.

The same script checked fast subset convolution against the direct sum for $n = 3, 5, 8$. The direct method uses $27$, $243$ and $6561$ pairs, which is $3^n$, and the fast method gave the same results.

## Known algorithms

- **Dreyfus and Wagner (1971).** Let $D(S, v)$ be the least weight of a tree that contains $S \subseteq T$ and the vertex $v$. Then $D(\{t\}, v)$ is the shortest path distance $d(t, v)$, computed with [Dijkstra's algorithm](/dijkstra/), and for $|S| \ge 2$
  $$D(S, v) = \min_{u \in V} \Big( d(v, u) + \min_{\emptyset \ne S' \subsetneq S} \big( D(S', u) + D(S \setminus S', u) \big) \Big).$$
  In an optimal tree, $u$ is the vertex where the path from $v$ meets the rest of the tree and the tree branches. The inner minimum runs over all ordered splits, $3^k$ in total over all $S$, and the outer minimum costs $O(n^2)$ per set, so the time is $O(3^k n + 2^k n^2)$ after the all-pairs distances. The answer is $D(T, t)$ for any terminal $t$.
- **Björklund, Husfeldt, Kaski and Koivisto (2007).** The inner minimum is a *subset convolution* in the min-plus sense: $(f \ast g)(S) = \min_{S' \subseteq S} f(S') + g(S \setminus S')$. With integer values at most $M'$, replace a value $x$ by $\beta^x$ for a large base $\beta$. Then the sum-product convolution $\sum_{S' \subseteq S} \beta^{f(S')} \beta^{g(S \setminus S')}$ has its lowest power of $\beta$ at the min-plus value. The sum-product convolution takes $O(2^k k^2)$ ring operations with the ranked zeta and Möbius transforms. This gives $O^\ast(2^k M)$ for weights at most $M$, and $O^\ast(2^k)$ for unweighted graphs. The scratch script checked the embedding on 3 elements with values at most 4.
- **Cut and count.** For graphs of treewidth $t$, a Monte Carlo algorithm in $3^t n^{O(1)}$ time (see [cut and count](/cut-and-count/)).

## Bounds

- **Classical complexity.** NP-complete under polynomial-time many-one reductions; Steiner tree is one of Karp's 21 problems (1972).
- **Lower bound in time.** No $(2 - \varepsilon)^k n^{O(1)}$ algorithm exists for any $\varepsilon > 0$ unless the set cover conjecture fails (Cygan, Dell, Lokshtanov, Marx, Nederlof, Okamoto, Paturi, Saurabh and Wahlström). So the base 2 of the algorithm of Björklund et al. is probably optimal.
- **Kernels.** Steiner tree parameterized by $k + \ell$ in the unweighted version has no polynomial kernel unless NP is a subset of coNP/poly (Dom, Lokshtanov and Saurabh). See [kernel lower bounds](/kernel-lower-bounds/).
- **W-hardness.** With the number of Steiner vertices as the parameter, the problem is W[2]-hard (see Reductions and [W-hardness](/w-hardness/)).

## Reductions

- **From set cover, for the number of Steiner vertices.** Given a universe $U$, sets $S_1, \ldots, S_m$ and a budget $p$, build a graph with one terminal per element of $U$, one more terminal $r$, and one vertex $s_j$ per set. Join $r$ to every $s_j$, and join $s_j$ to the elements of $S_j$. All weights are 1. The terminals form an independent set, so every Steiner tree uses set vertices, and each element needs a neighbor $s_j$ in the tree. A set cover $C$ gives a tree with Steiner vertices $\{s_j : j \in C\}$, and a tree with $p$ Steiner vertices gives a cover with $p$ sets. The parameter $p$ is kept, so W[2]-hardness of [set cover](/set-cover/) by solution size carries over.
- **To the metric closure.** Replace $G$ by the complete graph on $V(G)$ in which each edge $uv$ has weight $d(u, v)$. The least weight of a Steiner tree does not change, because each edge of the closure can be replaced by a shortest path. This is the first step of the dynamic program and of the 2-approximation.

## Applications

Steiner trees model the cheapest wiring that connects given pins in VLSI routing, the cheapest network that connects given sites, and the connection of given nodes in a phylogenetic or biological network. In many such inputs the number of terminals is small and the graph is large, which is the case the FPT algorithms handle well. The Dreyfus and Wagner recurrence is also a standard subroutine: other algorithms use it to connect a few chosen vertices inside a larger dynamic program.

## References
