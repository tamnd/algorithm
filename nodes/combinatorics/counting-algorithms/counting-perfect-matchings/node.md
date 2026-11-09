---
tag: DM37AB
kind: problem
slug: counting-perfect-matchings
name: Counting perfect matchings
aliases:
- number of perfect matchings
- '#PerfectMatching'
- dimer counting
area: combinatorics/counting-algorithms
level: advanced
summary: Counts perfect matchings; equivalent to the permanent for bipartite graphs.
prereqs: [perfect-matching, bipartite-graph, permanent-computation, determinant]
see_also: [kasteleyn-method, ryser-formula, glynn-formula, domino-tiling-problem, tutte-matrix, fpras, counting-latin-squares, treewidth]
sources:
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 189 to 201, 1979
    locator: the main theorem (the permanent of a 0-1 matrix, hence the number of perfect matchings of a bipartite graph, is #P-complete)
  - paper: doi:10.1016/0031-8914(61)90063-5
    title: P. W. Kasteleyn, The statistics of dimers on a lattice, Physica 27(12), 1209 to 1225, 1961
    locator: the Pfaffian method and the product formula for the dimer coverings of a rectangle
  - paper: doi:10.1145/1008731.1008738
    title: Mark Jerrum, Alistair Sinclair and Eric Vigoda, A polynomial-time approximation algorithm for the permanent of a matrix with nonnegative entries, Journal of the ACM 51(4), 671 to 697, 2004
    locator: the FPRAS for the number of perfect matchings of a bipartite graph
  - paper: doi:10.1137/1.9781611973099.73
    title: Andreas Björklund, Counting perfect matchings as fast as Ryser, Proceedings of the 23rd ACM-SIAM Symposium on Discrete Algorithms (SODA), 914 to 921, 2012
    locator: the O*(2^(n/2)) algorithm for the number of perfect matchings of a general graph on n vertices
  - book: isbn:9780821847596
    title: László Lovász and Michael D. Plummer, Matching Theory, AMS Chelsea Publishing, 2009
    locator: Chapter 8, Determinants and matchings (Pfaffians, planar graphs and the number of perfect matchings)
---

Counting perfect matchings asks for the number $\Phi(G)$ of [perfect matchings](/perfect-matching/) of a graph $G$, that is, the sets of edges that cover each vertex exactly once. For a [bipartite graph](/bipartite-graph/) with biadjacency matrix $B$, $\Phi(G)$ is the [permanent](/permanent-computation/) $\operatorname{per}(B)$, and Valiant proved in 1979 that this is #P-complete, although deciding whether a perfect matching exists takes polynomial time. Three facts shape the algorithms: for [planar graphs](/planar-graph/) the count is a determinant, by [Kasteleyn's method](/kasteleyn-method/); for bipartite graphs it has an [FPRAS](/fpras/), by Jerrum, Sinclair and Vigoda; and for general graphs exact counting takes $O^*(2^{n/2})$ time on $n$ vertices.

## In plain words

You have a group of people and a list of which pairs are willing to work together. A perfect pairing puts every person in exactly one pair, using only willing pairs. How many perfect pairings are there?

Finding one perfect pairing is easy with known methods. Counting all of them is much harder: no fast exact method is known for general lists, and there is strong evidence that none exists. There are two good exceptions. When the willing pairs can be drawn on paper without crossing lines, a clever choice of signs turns the count into a determinant, which is fast to compute. When the people form two sides and each pair has one person from each side, a random walk gives a count that is close to the true one with high probability.

## Definition

Notation: $G = (V, E)$ is a simple graph with $|V| = n$. A *perfect matching* is a set $M \subseteq E$ such that each vertex is in exactly one edge of $M$; it needs $n$ to be even. $\Phi(G)$ is the number of perfect matchings. For a bipartite graph with sides $\{u_1, \ldots, u_m\}$ and $\{w_1, \ldots, w_m\}$, the biadjacency matrix $B$ has $B_{ij} = 1$ when $u_i w_j \in E$.

**Problem.** Input: a graph $G$. Output: $\Phi(G)$. The weighted version takes edge weights $x_e$ and asks for $\sum_M \prod_{e \in M} x_e$.

**Fact 1 (bipartite graphs).** $\Phi(G) = \operatorname{per}(B) = \sum_{\pi \in S_m} \prod_{i=1}^{m} B_{i \pi(i)}$.

*Proof.* A perfect matching of a bipartite graph matches each $u_i$ to some $w_{\pi(i)}$ with $\pi$ a bijection, and all edges $u_i w_{\pi(i)}$ must exist. So perfect matchings correspond to permutations $\pi$ with $\prod_i B_{i \pi(i)} = 1$. $\square$

**Fact 2 (general graphs).** $\Phi(G)$ is the hafnian of the adjacency matrix $A$: $\operatorname{haf}(A) = \frac{1}{2^{n/2} (n/2)!} \sum_{\sigma \in S_n} \prod_{i=1}^{n/2} A_{\sigma(2i-1) \sigma(2i)}$. Each perfect matching appears $2^{n/2} (n/2)!$ times in the sum, once for each order of its edges and each order of the two ends of each edge.

## Variants

- **Weighted matchings.** With weights, $\sum_M \prod_{e \in M} x_e$ is the dimer partition function of statistical physics; with $x_e \ge 0$ the approximation results below still hold for bipartite graphs.
- **All matchings.** Counting all matchings, not only perfect ones (the monomer-dimer problem), is also #P-complete, and it has an FPRAS for all graphs, by the Markov chain of Jerrum and Sinclair.
- **Planar graphs.** The count is $\sqrt{\det K}$ for a Kasteleyn orientation $K$, computable in polynomial time; see [Kasteleyn's method](/kasteleyn-method/). [Domino tilings](/domino-tiling-problem/) of a region are the perfect matchings of a planar grid graph.
- **Regular bipartite graphs.** These have the bounds below, and counting [Latin squares](/counting-latin-squares/) row by row uses them.
- **Modulo 2.** $\operatorname{per}(B) \equiv \det(B) \pmod 2$, so the parity of $\Phi$ for bipartite graphs takes polynomial time. Valiant showed that the permanent modulo any fixed power of 2 also takes polynomial time.

## Examples

| graph | $\Phi$ | reason |
|---|---|---|
| complete bipartite $K_{m,m}$ | $m!$ | every permutation |
| complete graph $K_{2k}$, $k = 0, \ldots, 7$ | 1, 1, 3, 15, 105, 945, 10395, 135135 | $(2k-1)!!$, OEIS A001147 |
| ladder, the $2 \times n$ grid, $n = 1, \ldots, 14$ | 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610 | Fibonacci numbers, OEIS A000045 |
| $2k \times 2k$ grid, $k = 0, \ldots, 7$ | 1, 2, 36, 6728, 12988816, 258584046368, 53060477521960000, 112202208776036178000000 | OEIS A004003 |
| hypercube $Q_d$, $d = 1, \ldots, 4$ | 1, 2, 9, 272 | OEIS A005271 |
| Petersen graph | 6 | |

**The $8 \times 8$ chessboard.** Its domino tilings number $12988816$. Kasteleyn's product formula gives the count of the $m \times n$ grid as

$$\prod_{j=1}^{m} \prod_{k=1}^{n} \left( 4 \cos^2 \frac{\pi j}{m+1} + 4 \cos^2 \frac{\pi k}{n+1} \right)^{1/4},$$

which for $m = n = 8$ evaluates to $12988816$.

**$K_4$.** On vertices $1, 2, 3, 4$, the perfect matchings are $\{12, 34\}$, $\{13, 24\}$ and $\{14, 23\}$, so $\Phi(K_4) = 3$.

## Known algorithms

- **Bit mask recursion.** Match the lowest unmatched vertex $v$ with each free neighbor and recurse on the rest: $\Phi(G) = \sum_{u \in N(v)} \Phi(G - u - v)$. With memoization over vertex subsets this takes $O(2^n n)$ time; without it, at most $(n-1)!!$ leaves.
- **Bipartite: Ryser and Glynn.** $\operatorname{per}(B)$ for $m \times m$ by [Ryser's formula](/ryser-formula/) or [Glynn's formula](/glynn-formula/) in $O(2^m m)$ operations with a Gray code, which is $O(2^{n/2} n)$ for $n = 2m$ vertices.
- **General graphs: Björklund.** Fix a pairing of the vertices. An inclusion-exclusion over the subsets of these pairs, with a polynomial-time algebraic computation for each subset, gives $\Phi(G)$ in $O(2^{n/2} n^3)$ time and polynomial space, the same exponent as Ryser.
- **Planar graphs: Kasteleyn (FKT).** Orient the edges so that each inner face has an odd number of clockwise edges. Then $\Phi(G)^2 = \det K$ for the signed skew-symmetric adjacency matrix $K$, which is $O(n^3)$ operations, or $O(n^{\omega/2})$ with nested dissection. See [Kasteleyn's method](/kasteleyn-method/).
- **Bounded treewidth.** A dynamic program over a tree decomposition of width $k$ stores, for each bag, which bag vertices are already matched, so $2^{k+1}$ states per bag and $O(2^k n)$ states in all, as on [treewidth](/treewidth/). Grids of fixed height are counted this way, by a transfer matrix over columns.
- **Approximate: JSV.** For bipartite graphs, the Markov chain on perfect and near-perfect matchings, with weights learned by simulated annealing, gives an FPRAS (Jerrum, Sinclair and Vigoda, 2004). For general graphs no FPRAS is known.
- **Randomized algebra.** The Tutte matrix (see [Tutte matrix](/tutte-matrix/)) with random values tests whether $\Phi(G) > 0$, but its Pfaffian has terms with signs that cancel, so it does not give the count unless the graph has a Pfaffian orientation, as planar graphs do.

## Bounds

**Hardness.** Counting perfect matchings of bipartite graphs is #P-complete (Valiant, 1979), even though deciding $\Phi(G) > 0$ is in P by [bipartite matching](/bipartite-matching/). So the counting problem can be hard while its decision version is easy.

**Regular bipartite graphs.** Let $G$ be $k$-regular bipartite with $m$ vertices on each side. Then

$$m! \left( \frac{k}{m} \right)^m \;\le\; \Phi(G) \;\le\; (k!)^{m/k}.$$

The lower bound is the Van der Waerden bound $\operatorname{per}(D) \ge m! / m^m$ for the doubly stochastic matrix $D = B / k$, proved by Egorychev and Falikman. The upper bound is Bregman's theorem $\operatorname{per}(B) \le \prod_i (r_i!)^{1/r_i}$ for a 0-1 matrix with row sums $r_i$; it is tight for a disjoint union of copies of $K_{k,k}$. By Stirling's formula, $m! (k/m)^m \ge (k/e)^m$, so a $k$-regular bipartite graph has at least $(k/e)^m$ perfect matchings.

## Reductions

- **To the permanent.** For bipartite graphs, by Fact 1. Conversely, the permanent of a 0-1 matrix is the count of perfect matchings of its bipartite graph, so the two problems are the same.
- **To the hafnian.** For general graphs, by Fact 2.
- **To determinants, for planar graphs.** By Kasteleyn's method. The method extends to graphs of bounded genus with $4^g$ determinants.
- **Hardness from #3SAT.** Valiant's proof reduces #3SAT to the permanent of an integer matrix with gadgets, then to the 0-1 permanent by replacing weights with small subgraphs and using arithmetic modulo many primes.

## Applications

- Statistical physics: the dimer model on lattices, where the count of domino tilings gives the entropy per dimer.
- Chemistry: the Kekulé structures of a benzenoid hydrocarbon are the perfect matchings of its planar carbon graph.
- Combinatorics: counting Latin squares, tilings of regions, and permutations with forbidden positions, such as derangements, which are the permanents of $J - I$.
- Complexity theory: the main example of a counting problem that is #P-complete while its decision problem is in P.

## References
