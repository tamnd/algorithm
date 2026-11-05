---
tag: 26EJCW
kind: problem
slug: counting-graph-colorings
name: Counting graph colorings
aliases:
- counting proper k-colorings
area: graphs/coloring-and-cliques
level: advanced
summary: 'Count the proper k-colorings of a graph; #P-hard in general.'
prereqs: [chromatic-polynomial, graph-coloring, k-coloring]
see_also: [chromatic-polynomial, deletion-contraction, k-coloring, bjorklund-chromatic-number, chordal-graph-coloring, inclusion-exclusion-principle, treewidth, bitmask-dp]
sources:
  - paper: doi:10.1017/S0305004100068936
    title: F. Jaeger, D. L. Vertigan and D. J. A. Welsh, On the computational complexity of the Jones and Tutte polynomials, Mathematical Proceedings of the Cambridge Philosophical Society 108(1), 35 to 53 (1990)
    locator: the main theorem (the Tutte polynomial is #P-hard to evaluate except on one hyperbola and at 8 special points; for the chromatic polynomial, every integer k at least 3 is hard)
  - paper: doi:10.1137/070683933
    title: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 546 to 563 (2009)
    locator: the O*(2^n) algorithm for counting k-colorings and computing the chromatic polynomial
  - paper: doi:10.1002/rsa.3240070205
    title: Mark Jerrum, A very simple algorithm for estimating the number of k-colorings of a low-degree graph, Random Structures and Algorithms 7(2), 157 to 165 (1995)
    locator: the main theorem (an FPRAS for k > 2 Delta by Glauber dynamics)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Appendix A1.1, problem GT4, Graph K-colorability (the decision version for fixed K at least 3 is NP-complete)
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Łukasz Kowalik, Daniel Lokshtanov, Dániel Marx, Marcin Pilipczuk, Michał Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 7, Treewidth (dynamic programming over tree decompositions) and Chapter 10, Algebraic techniques (inclusion-exclusion and subset convolution)
---

Counting graph colorings asks for the number $P(G, k)$ of proper colorings of the vertices of a graph $G$ with colors from $\{1, \ldots, k\}$. As a function of $k$ this is the [chromatic polynomial](/chromatic-polynomial/). The count is easy for $k \le 2$, but for every fixed $k \ge 3$ it is #P-complete (Jaeger, Vertigan and Welsh 1990), since even deciding $P(G, k) > 0$ is NP-complete. The best known exact algorithm runs in $O^*(2^n)$ time, and for $k > 2\Delta$ there is a fast randomized approximation.

## In plain words

You have a network and $k$ colors. Each point gets a color, and joined points must differ. How many ways are there to do this?

With one or two colors the answer is quick: with two colors, each connected piece of the network either has exactly two colorings or none. With three or more colors, nobody knows a fast way, and it is believed that none exists, because even telling whether the count is zero is already hard.

The exact methods are slow but much better than trying all colorings. When there are many more colors than the number of neighbors of any point, a random walk over colorings gives a close estimate quickly.

## Definition

Let $G = (V, E)$ be a finite graph without loops, with $n$ vertices and $m$ edges.

**#$k$-COLORING.** Input: $G$ and an integer $k \ge 0$. Output:

$$P(G, k) = \big|\{ c : V \to \{1, \ldots, k\} : c(u) \ne c(v) \text{ for each } uv \in E \}\big|.$$

Colorings are maps, so two colorings that differ by a permutation of the colors are counted separately. The number of partitions of $V$ into exactly $j$ non-empty [independent sets](/independent-set/), $a_j(G)$, counts colorings up to the names of the colors, and

$$P(G, k) = \sum_{j=0}^{n} a_j(G)\, k(k-1)\cdots(k-j+1).$$

## Variants

- **Fixed $k$.** For each fixed $k$, the input is $G$ only.
- **The whole polynomial.** Output all $n + 1$ coefficients of $P(G, k)$. Evaluating at $k = 0, 1, \ldots, n$ and interpolating gives them, so this costs $n + 1$ evaluations.
- **List colorings.** Each vertex has its own list of allowed colors.
- **Weighted counting.** The Potts model partition function gives each coloring a weight depending on the number of edges with equal colors; proper colorings are the zero-temperature antiferromagnetic case.
- **Approximate counting.** Output a number within a factor $1 \pm \varepsilon$ of $P(G, k)$, with high probability.
- **Uniform sampling.** Output a uniformly random proper $k$-coloring. Jerrum's approximate counter is built from an approximate sampler; see Reductions.

## Examples

| graph | $P(G, k)$ | $P(G, 3)$ | $a_j$ for $j = 1, \ldots, n$ |
|---|---|---|---|
| $C_5$ | $(k-1)^5 - (k-1)$ | 30 | 0, 0, 5, 5, 1 |
| $K_4$ | $k(k-1)(k-2)(k-3)$ | 0 | 0, 0, 0, 1 |
| triangle strip $S$ | $k(k-1)(k-2)^4$ | 6 | |
| Petersen graph | degree 10 | 120 | 0, 0, 20, 520, 2244, 2865, 1435, 315, 30, 1 |

$S$ is the graph on $0, \ldots, 5$ with edges $01, 02, 12, 13, 23, 24, 34, 35, 45$.

**Check for $C_5$.** The formula above gives $P(C_5, 3) = a_3 \cdot 3 \cdot 2 \cdot 1 = 5 \cdot 6 = 30$, since the falling factorial vanishes for $j \ge 4$. The 5 partitions into 3 independent sets are, for each vertex $i$, $\{i\}$, $\{i+1, i+3\}$, $\{i+2, i+4\}$ modulo 5.

**Check for the Petersen graph.** $a_3 = 20$ gives $P(3) = 20 \cdot 6 = 120$, the value found by trying all $3^{10}$ maps.

## Known algorithms

- **Brute force.** Try all $k^n$ maps: $O(k^n m)$ time.
- **$k \le 2$.** $P(G, 0) = 0$ for $n \ge 1$; $P(G, 1) = 1$ if $E = \emptyset$ and 0 otherwise; $P(G, 2) = 2^c$ if $G$ is [bipartite](/bipartiteness-testing/) with $c$ components, and 0 otherwise. All in $O(n + m)$ time.
- **[Deletion-contraction](/deletion-contraction/).** $P(G) = P(G - e) - P(G / e)$ gives the whole polynomial in $O^*(\varphi^{n + m})$ time with $\varphi \approx 1.618$. Good in practice on sparse graphs with caching of isomorphic minors.
- **Subset dynamic programming.** Compute $a_j(S)$, the number of partitions of $S \subseteq V$ into $j$ independent sets, by choosing the block of the smallest vertex of $S$: $a_j(S) = \sum a_{j-1}(S \setminus B)$ over independent $B \subseteq S$ that contain it. This takes $O(3^n n)$ time and gives all $a_j(G)$, so the whole polynomial. See [bitmask DP](/bitmask-dp/).
- **Inclusion-exclusion (Björklund, Husfeldt and Koivisto 2009).** For one value of $k$, count the $k$-tuples of disjoint independent sets that cover $V$ with the ranked zeta transform over subsets, in $O^*(2^n)$ time and space. This is the best known bound for general graphs. See [Björklund's algorithm](/bjorklund-chromatic-number/).
- **Bounded treewidth.** Dynamic programming over a tree decomposition of width $w$ stores, for each bag, the number of partial colorings for each coloring of the bag, in $O(k^{w+1} \cdot \mathrm{poly}(n))$ time. See [treewidth](/treewidth/).
- **Chordal graphs.** If $v_1, \ldots, v_n$ is the reverse of a [perfect elimination ordering](/perfect-elimination-ordering/), so that the earlier neighbors $E(v_i)$ of each $v_i$ form a clique, then $P(G, k) = \prod_i (k - |E(v_i)|)$, because $v_i$ sees $|E(v_i)|$ different colors whatever the coloring before it. For $S$ the earlier neighbor counts in the order $0, 1, \ldots, 5$ are $0, 1, 2, 2, 2, 2$, which gives $k(k-1)(k-2)^4$. See [coloring chordal graphs](/chordal-graph-coloring/).
- **Approximate counting (Jerrum 1995).** For $k > 2\Delta$, where $\Delta$ is the maximum degree, the Glauber dynamics, which recolors a random vertex with a random allowed color, mixes in $O(n \log n)$ steps, and it gives a fully polynomial randomized approximation scheme.

## Bounds

- **#P-completeness.** For each fixed integer $k \ge 3$, computing $P(G, k)$ is #P-complete. Jaeger, Vertigan and Welsh (1990) showed that the Tutte polynomial is #P-hard to evaluate at every point outside the hyperbola $(x - 1)(y - 1) = 1$ and eight special points; $P(G, k)$ is the point $(1 - k, 0)$, which is easy only for $k \in \{0, 1, 2\}$.
- **NP-hardness of the support.** Deciding $P(G, k) > 0$ is [$k$-coloring](/k-coloring/), NP-complete for $k \ge 3$ (Garey and Johnson, GT4). So even an approximation within any factor is NP-hard for $k \ge 3$ without a restriction such as $k > 2\Delta$.
- **Exact.** $O^*(2^n)$ time and space for a single $k$ (Björklund, Husfeldt and Koivisto 2009).
- **Approximate.** An FPRAS exists for $k > 2\Delta$ (Jerrum 1995).

## Reductions

- **From $k$-coloring.** Any algorithm that counts $k$-colorings decides $k$-colorability, so #$k$-COLORING is NP-hard for $k \ge 3$.
- **To Tutte polynomial evaluation.** $P(G, k) = (-1)^{n - c} k^c\, T(G; 1 - k, 0)$, where $c$ is the number of components.
- **Interpolation.** Counting $k$-colorings for $n + 1$ values of $k$ gives the whole chromatic polynomial by Lagrange interpolation, and conversely. Hardness proofs for single points use such interpolation on graphs built from $G$.
- **Counting from sampling.** For $k > 2\Delta$, Jerrum removes the edges of $G$ one at a time. Each ratio $P(G_{i}, k) / P(G_{i+1}, k)$ between consecutive graphs is bounded away from 0 and is estimated from random colorings of $G_{i+1}$, and the product of the ratios times $k^n$ estimates $P(G, k)$.

## Applications

- **Statistical physics.** $P(G, k)$ is the ground state degeneracy of the antiferromagnetic $k$-state Potts model on $G$; its growth rate on lattices is the residual entropy.
- **Exact chromatic number.** $\chi(G)$ is the least $k$ with $P(G, k) > 0$, and the counting algorithms of Björklund, Husfeldt and Koivisto are the fastest known way to compute it.
- **Probabilistic analysis.** Counting colorings of random graphs underlies thresholds for $k$-colorability.
- **Constraint satisfaction.** Counting solutions of a CSP whose constraints are all "not equal" is counting colorings, a test case for model counters.

## References
