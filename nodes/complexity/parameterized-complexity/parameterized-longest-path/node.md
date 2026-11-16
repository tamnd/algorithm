---
tag: SW1MP3
kind: problem
slug: parameterized-longest-path
name: Parameterized longest path
aliases:
- k-path
- longest path parameterized by length
area: complexity/parameterized-complexity
level: advanced
summary: "Decide whether a graph has a simple path with k vertices, with k as the parameter. FPT in randomized time O*(2^k), but with no polynomial kernel unless NP is a subset of coNP/poly."
prereqs: [longest-path-problem, fixed-parameter-tractable]
see_also: [k-path-color-coding, color-coding, divide-and-color, representative-families, hamiltonian-cycle-problem, kernel-lower-bounds, parameterized-counting-complexity, graph-motif]
sources:
  - paper: doi:10.1145/210332.210337
    title: "Noga Alon, Raphael Yuster and Uri Zwick, Color-coding, Journal of the ACM 42(4), 844-856 (1995)"
    locator: simple paths of length k in 2^O(k) m expected time
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 5 (Section 5.2.1, color coding for Longest Path; Section 5.4, divide and color for Longest Path), Chapter 10 (Section 10.4.1, Longest Path in time 2^k n^O(1)), Chapter 12 (representative sets and Longest Path) and Chapter 15 (kernel lower bounds)
  - paper: doi:10.1016/j.jcss.2009.04.001
    title: "Hans L. Bodlaender, Rodney G. Downey, Michael R. Fellows and Danny Hermelin, On problems without polynomial kernels, Journal of Computer and System Sciences 75(8), 423-434 (2009)"
    locator: composition and the lower bound for Longest Path
  - paper: doi:10.1137/080716475
    title: "Jianer Chen, Joachim Kneis, Songjian Lu, Daniel Mölle, Stefan Richter, Peter Rossmanith, Sing-Hoi Sze and Fenghui Zhang, Randomized divide-and-conquer: improved path, matching, and packing algorithms, SIAM Journal on Computing 38(6), 2526-2547 (2009)"
    locator: k-path in randomized time O(4^k k^2.7 m) with polynomial space
  - paper: doi:10.1016/j.ipl.2008.11.004
    title: "Ryan Williams, Finding paths of length k in O*(2^k) time, Information Processing Letters 109(6), 315-318 (2009)"
    locator: the main result, randomized O*(2^k) time
  - paper: doi:10.1016/j.jcss.2017.03.003
    title: "Andreas Björklund, Thore Husfeldt, Petteri Kaski and Mikko Koivisto, Narrow sieves for parameterized paths and packings, Journal of Computer and System Sciences 87, 119-139 (2017)"
    locator: k-path in undirected graphs in randomized time O*(1.66^k)
  - paper: doi:10.1145/2886094
    title: "Fedor V. Fomin, Daniel Lokshtanov, Fahad Panolan and Saket Saurabh, Efficient computation of representative families with applications in parameterized and exact algorithms, Journal of the ACM 63(4), article 29 (2016)"
    locator: deterministic k-path in time O(2.619^k n log n)
---

Parameterized longest path, or p-Longest-Path, asks whether a graph has a simple path with $k$ vertices, with $k$ as the [parameter](/parameter/). The classical [longest path problem](/longest-path-problem/) is NP-hard, because $k = n$ asks for a Hamiltonian path. With the parameter $k$, the problem is [fixed-parameter tractable](/fixed-parameter-tractable/): [color coding](/k-path-color-coding/) solves it in randomized time $O((2e)^k (n + m))$, and algebraic methods in randomized time $O^*(2^k)$, where $O^*$ hides factors polynomial in $n$. It is a standard example of a problem that is FPT but has no polynomial kernel unless $\mathsf{NP} \subseteq \mathsf{coNP/poly}$. This page gives only the parameterized view. The [longest path problem](/longest-path-problem/) page has the optimization problem, the weighted form and the polynomial cases such as DAGs and trees.

## In plain words

You have a map of towns and roads. The question is whether there is a trip through a given number of towns that never visits a town twice. When the number is as large as the whole map, this is the famous hard question of a trip through every town.

When the number of towns on the trip is small, there are fast methods. Their cost grows very fast with the length of the trip, but only slowly with the size of the map. So a short trip can be found in a huge map.

There is a limit, though. No fast method is known that first shrinks the map to a small piece whose size depends only on the length of the trip, and such a method would contradict a widely believed assumption.

## Definition

The input is a graph $G = (V, E)$ given by adjacency lists, with $n = |V|$ and $m = |E|$, and an integer $k \ge 1$. A *k-path* is a sequence of $k$ distinct vertices $v_1, \ldots, v_k$ in which consecutive vertices are adjacent. Its length in edges is $k - 1$.

**p-LONGEST-PATH**

- Instance: a graph $G = (V, E)$ and an integer $k \ge 1$.
- Parameter: $k$.
- Question: does $G$ have a simple path with $k$ vertices?

A yes-instance has a certificate of $k$ vertex names, checked in $O(k + m)$ time. A graph with a path of at least $k$ vertices also has one of exactly $k$ vertices (take a part of it), so "exactly $k$" and "at least $k$" give the same problem. If $k > n$, the answer is no. Some texts take the length $k$ in edges; then the path has $k + 1$ vertices, and the bounds below change only by a constant factor.

## Variants

- *Directed graphs.* Ask for a directed path with $k$ vertices. Color coding and the $O^*(2^k)$ algebraic method work unchanged. The $O^*(1.66^k)$ bound below is for undirected graphs only.
- *Exact cycle.* Is there a cycle with exactly $k$ vertices? This is FPT by the same methods: [color coding](/color-coding/) finds a colorful path that closes into a cycle.
- *Long cycle.* Is there a cycle with *at least* $k$ vertices? This is not the same as the exact form, because the shortest such cycle may have many more than $k$ vertices. It is still FPT; Cygan et al. treat the directed form with [representative families](/representative-families/).
- *Structural parameters.* With the [treewidth](/treewidth/) $t$ as the parameter, the problem is FPT in time $2^{O(t \log t)} n$ by dynamic programming over a tree decomposition, and in randomized time $2^{O(t)} n^{O(1)}$ by [cut and count](/cut-and-count/).
- *Planar graphs.* On [planar graphs](/planar-graph/), the problem is solvable in time $2^{O(\sqrt{k})} n^{O(1)}$ by [bidimensionality](/bidimensionality-theory/).
- *Counting.* Counting the $k$-paths is #W[1]-hard (Flum and Grohe, 2004), although finding one is FPT. See [parameterized counting complexity](/parameterized-counting-complexity/).
- *Patterns other than paths.* [Graph motif](/graph-motif/) asks for a connected set of vertices with given colors; the colorful $k$-path is close to it.

## Examples

The counts below come from a brute-force search over all simple paths, counting each path once (not once per direction).

- *A star.* Let $G$ be the star with one center and 5 leaves. It has 5 paths with 2 vertices, 10 paths with 3 vertices (leaf, center, leaf) and none with 4. So $(G, 3)$ is a yes-instance and $(G, 4)$ is a no-instance.
- *The 3 by 3 grid.* It has 9 vertices and 12 edges, and 20 paths with 9 vertices. So $(G, 9)$ is a yes-instance, and every $k \le 9$ gives a yes-instance.
- *The Petersen graph.* It has 10 vertices and 15 edges. The numbers of $k$-paths for $k = 1, \ldots, 10$ are 10, 15, 30, 60, 120, 180, 240, 300, 300 and 120. So $(G, 10)$ is a yes-instance: the Petersen graph has a Hamiltonian path, although it has no Hamiltonian cycle (see [Hamiltonian cycle problem](/hamiltonian-cycle-problem/)).

The parameter matters in the size of the search. Brute force over all sequences of $k$ distinct vertices of the Petersen graph tries up to $10 \cdot 9 \cdots (11 - k)$ sequences, while color coding works with $2^k$ color sets per vertex.

## Known algorithms

Time bounds are for the word RAM with words of $O(\log n)$ bits; $O^*$ hides factors polynomial in $n$.

- Brute force over all sequences of $k$ vertices: $O(n^k)$ time, which is [XP](/xp/) but not FPT.
- Monien (1985): deterministic $O(k! \cdot nm)$ time, the first FPT algorithm.
- [Color coding](/k-path-color-coding/) (Alon, Yuster and Zwick, 1995): randomized $O((2e)^k (n + m))$ time with one-sided error, and deterministic $2^{O(k)} m \log n$ time with perfect hash families.
- [Divide and color](/divide-and-color/) (Chen et al., 2009): randomized $O(4^k k^{2.7} m)$ time with polynomial space, and deterministic $4^{k + o(k)} m$ time.
- Algebraic methods: randomized $O^*(2^k)$ time and polynomial space (Koutis, 2008, gave $O^*(2^{3k/2})$; Williams, 2009, gave $O^*(2^k)$), for directed and undirected graphs.
- Narrow sieves (Björklund, Husfeldt, Kaski and Koivisto, 2017): randomized $O^*(1.66^k)$ time on undirected graphs.
- [Representative families](/representative-families/) (Fomin, Lokshtanov, Panolan and Saurabh, 2016): deterministic $O(2.619^k n \log n)$ time; the conference version had $O(2.851^k m \log^2 n)$. Zehavi (2015) and Tsur (2019) lowered the deterministic base to about $2.597$ and $2.554$.

All randomized algorithms above have [one-sided error](/one-sided-error/): a path they return is a real path, and the answer "no" is wrong with a small probability.

## Bounds

- *NP-hardness.* With $k = n$ the problem is the [Hamiltonian path problem](/hamiltonian-path-problem/), which is NP-complete under polynomial-time many-one reductions. So no algorithm runs in time polynomial in $n$ and $k$ unless P = NP.
- *ETH.* Under the Exponential Time Hypothesis (stated on the page [strong exponential time hypothesis](/strong-exponential-time-hypothesis/)), Hamiltonian path has no $2^{o(n)}$ algorithm, because the standard reduction from 3-SAT makes a graph with $O(N + M)$ vertices from a formula with $N$ variables and $M$ clauses, and the sparsification lemma lets us take $M = O(N)$. With $k = n$, a $2^{o(k)} n^{O(1)}$ algorithm for p-Longest-Path would give a $2^{o(n)}$ algorithm for Hamiltonian path. So there is no $2^{o(k)} n^{O(1)}$ algorithm unless ETH fails. This is a lower bound on the base form, separate from W-hardness, which does not apply because the problem is FPT.
- *No polynomial kernel.* p-Longest-Path has no kernel of size $k^{O(1)}$, in vertices, edges or bits, unless $\mathsf{NP} \subseteq \mathsf{coNP/poly}$ (Bodlaender, Downey, Fellows and Hermelin, 2009). The reason is that the disjoint union of $t$ instances with the same $k$ has a $k$-path if and only if one of them has one: this is an OR-composition. See [kernel lower bounds](/kernel-lower-bounds/) and [cross-composition](/cross-composition/). Since the problem is FPT, it has a kernel whose size is some function of $k$, but that function is not a polynomial unless the assumption fails.
- *Algebraic barrier.* The $O^*(2^k)$ algorithms rely on detecting a multilinear monomial. No deterministic $O^*(2^k)$ algorithm is known; the best deterministic base is about $2.554$.

## Reductions

- *From Hamiltonian path.* The map $G \mapsto (G, n)$ is a polynomial-time many-one reduction. It proves NP-hardness but is not a [parameterized reduction](/parameterized-reduction/) from a problem with a small parameter.
- *OR-composition.* The map $(G_1, k), \ldots, (G_t, k) \mapsto (G_1 \cup \cdots \cup G_t, k)$, with the graphs made disjoint, runs in linear time and keeps the parameter. It is the composition behind the kernel lower bound above.
- *To a cycle through a given vertex.* Add a new vertex $s$ adjacent to every vertex of $G$. For $k \ge 2$, $G$ has a $k$-path if and only if the new graph has a cycle with $k + 1$ vertices through $s$: the two ends of the path close the cycle at $s$, and removing $s$ from such a cycle leaves a $k$-path of $G$. The map takes linear time and maps $k$ to $k + 1$.
- *Contrast with clique.* p-Longest-Path is FPT, while [p-Clique](/parameterized-clique/) is W[1]-complete. Both ask for a fixed pattern on $k$ vertices; the difference is that a path has treewidth 1 and a clique has treewidth $k - 1$, which is what color coding needs.

## Applications

- *Pathways in biological networks.* In protein interaction networks, short simple paths model signal pathways. Color coding finds paths with up to about 10 to 12 proteins in networks with thousands of proteins, and the counting form estimates how many there are.
- *Tests for new methods.* Many techniques of parameterized algorithms were first shown on $k$-path: color coding, divide and color, the algebraic methods and representative families. It is the standard benchmark for single-exponential randomized and deterministic bounds.
- *Kernel lower bounds.* It is the first example of an FPT problem without a polynomial kernel, and the textbook example for compositions.

## References
