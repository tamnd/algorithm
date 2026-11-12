---
tag: 158EAF
kind: problem
slug: perfect-matching
name: Perfect matching
aliases:
- 1-factor
- perfect matching problem
area: graphs/matching
level: core
summary: Decide whether a graph has a matching that covers every vertex, or find one.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m n^(1/2))}
prereqs: [maximum-matching, hall-theorem]
see_also: [tutte-theorem, petersens-theorem, tutte-matrix, rnc-perfect-matching, minimum-weight-perfect-matching, counting-perfect-matchings, edmonds-blossom, hopcroft-karp]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.1, Matchings and covers (Hall's theorem and regular bipartite graphs), and Section 3.3, Matchings in general graphs (Tutte's 1-factor theorem and Petersen's theorem)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer
    locator: Chapter 2, Matching, Covering and Packing (Sections 2.1 and 2.2)
  - paper: doi:10.1112/jlms/s1-22.2.107
    title: William T. Tutte, The factorization of linear graphs, Journal of the London Mathematical Society 22(2), 107 to 111 (1947)
    locator: the whole paper
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 189 to 201 (1979)
    locator: "the whole paper (counting perfect matchings of bipartite graphs is #P-complete)"
  - paper: "László Lovász, On determinants, matchings, and random algorithms, Fundamentals of Computation Theory (FCT 1979), Akademie-Verlag Berlin, 565 to 574 (1979)"
    locator: the whole paper (the randomized test by the Tutte matrix)
  - paper: doi:10.1145/1008731.1008738
    title: Mark Jerrum, Alistair Sinclair and Eric Vigoda, A polynomial-time approximation algorithm for the permanent of a matrix with nonnegative entries, Journal of the ACM 51(4), 671 to 697 (2004)
    locator: the whole paper
---

The perfect matching problem asks whether a graph has a matching that covers every vertex, and asks for one if it does. Such a matching is also called a 1-factor. It is the case $k = n/2$ of [maximum matching](/maximum-matching/), so it is solved in $O(m \sqrt n)$ time. Its existence is characterized by [Hall's theorem](/hall-theorem/) for bipartite graphs and by [Tutte's theorem](/tutte-theorem/) for general graphs, and it has a short randomized algebraic test by the [Tutte matrix](/tutte-matrix/).

## In plain words

An even number of people want to split into pairs, and each person can pair only with some of the others. Can everyone be paired at the same time, with nobody left alone? If yes, find such a pairing.

An odd number of people can never be paired. Less obvious reasons also block a pairing: if a few people are the only links of many small odd groups, each odd group needs one of those few people, and there are not enough of them. Tutte's theorem says that such a group of key people is the only obstacle. The usual way to find the pairing is to build the largest set of pairs and check whether it covers everyone.

## Definition

Let $G = (V, E)$ be a finite undirected graph, without weights, bipartite or general, with $n = |V|$ and $m = |E|$. A matching $M$ is *perfect* if every vertex of $V$ is an end of an edge of $M$; then $|M| = n/2$.

- **Decision input:** $G$. **Output:** yes if $G$ has a perfect matching, otherwise no.
- **Search input:** $G$. **Output:** a perfect matching, or a certificate that none exists.

The graph with no vertices has the empty perfect matching. A graph with an isolated vertex or with an odd number of vertices has none.

**Certificates of "no".**

- *General graphs* ([Tutte's theorem](/tutte-theorem/)): $G$ has no perfect matching if and only if there is a set $U \subseteq V$ such that $G - U$ has more than $|U|$ connected components with an odd number of vertices. Each odd component needs a matching edge to $U$, and different components need different vertices of $U$.
- *Bipartite graphs with sides $L$ and $R$, $|L| = |R|$* ([Hall's theorem](/hall-theorem/)): $G$ has no perfect matching if and only if some $X \subseteq L$ has fewer than $|X|$ neighbours.

Both certificates can be checked in $O(n + m)$ time, and both are produced by the matching algorithms. So the problem is in $\mathsf{NP} \cap \mathsf{coNP}$ by these theorems alone, and in $\mathsf{P}$ by the algorithms.

## Variants

- **Bipartite or general.** In a bipartite graph with sides $L$ and $R$, a perfect matching needs $|L| = |R|$. A matching that covers only $L$ is an *$L$-perfect* matching, the question of Hall's theorem.
- **Weighted.** Find a perfect matching of least total weight: [minimum-weight perfect matching](/minimum-weight-perfect-matching/), and in the bipartite case the [assignment problem](/assignment-problem/).
- **Counting.** Count the perfect matchings. This is [#P-complete](/counting-perfect-matchings/), by Valiant, already for bipartite graphs, where it equals the permanent of the 0-1 biadjacency matrix.
- **Factors.** A *$k$-factor* is a spanning subgraph in which each vertex has degree $k$; a perfect matching is a 1-factor. See the [f-factor problem](/f-factor-problem/).
- **Parallel.** The [randomized parallel algorithm](/rnc-perfect-matching/) decides and finds a perfect matching in randomized NC. Whether a deterministic NC algorithm exists is open.
- **Exact matching.** With red and blue edges, is there a perfect matching with exactly $k$ red edges? It has a randomized polynomial algorithm, and no deterministic one is known.

## Examples

| graph | has a perfect matching? | number of perfect matchings | reason |
|---|---|---|---|
| no vertices | yes | 1 | the empty matching |
| [complete graph](/complete-graph/) $K_n$, $n$ even | yes | $(n-1)(n-3) \cdots 3 \cdot 1$, for example 15 for $K_6$ | pair the first vertex, then recurse |
| $K_n$, $n$ odd | no | 0 | odd number of vertices |
| complete bipartite $K_{k,k}$ | yes | $k!$ | each permutation |
| even cycle $C_{2k}$ | yes | 2 | every other edge, two ways |
| odd cycle $C_{2k+1}$ | no | 0 | odd number of vertices |
| star $K_{1,3}$ | no | 0 | $U$ = the center leaves 3 odd components |
| cube $Q_3$ | yes | 9 | 3-regular bipartite |
| Petersen graph | yes | 6 | [Petersen's theorem](/petersens-theorem/) |

**A graph with an even number of vertices and no perfect matching.** Take a center $c$ joined to three triangles, one edge to one vertex of each triangle. It has $1 + 9 = 10$ vertices. Deleting $c$ leaves three triangles, which are 3 odd components, and $3 > |\{c\}| = 1$. So by Tutte's theorem there is no perfect matching, though the vertex count is even and the graph is connected.

**A bipartite example.** Let $L = \{1, 2, 3\}$, $R = \{a, b, c\}$, and $E = \{1a, 2a, 3a, 3b, 3c\}$. The set $X = \{1, 2\}$ has the single neighbour $a$, so no perfect matching exists.

**Regular bipartite graphs.** Each $k$-regular bipartite graph with $k \ge 1$ has a perfect matching. Proof: for $X \subseteq L$, the $k|X|$ edges at $X$ end in $N(X)$, which has at most $k|N(X)|$ edge ends, so $|N(X)| \ge |X|$, and Hall's theorem applies. Counting edges gives $k|L| = k|R|$, so $|L| = |R|$.

## Known algorithms

| algorithm | graphs | time | output |
|---|---|---|---|
| [Hopcroft-Karp](/hopcroft-karp/) | bipartite | $O(m \sqrt n)$ | a perfect matching or a Hall set |
| [Kuhn's algorithm](/kuhn-algorithm/) | bipartite | $O(nm)$ | a perfect matching or a Hall set |
| [Micali-Vazirani](/micali-vazirani-algorithm/) | general | $O(m \sqrt n)$ | a maximum matching |
| [Edmonds' blossom algorithm](/edmonds-blossom/) | general | $O(n^3)$ with Gabow's implementation | a maximum matching and a Tutte set |
| Lovász's test with the [Tutte matrix](/tutte-matrix/) | general | one determinant, $O(n^{\omega})$ | yes or no, one-sided error |
| [Randomized parallel perfect matching](/rnc-perfect-matching/) | general | polylogarithmic depth | a perfect matching |

The Tutte matrix test is Monte Carlo with one-sided error. Replace each variable of the Tutte matrix by a random element of a field with at least $2n$ elements. If $G$ has no perfect matching, the determinant is always 0. If it has one, the determinant is not 0 with probability at least $1/2$, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), since the determinant of the Tutte matrix is a nonzero polynomial of degree $n$.

## Bounds

- **Upper bounds.** $O(m \sqrt n)$ deterministic on the [word RAM](/word-ram/), from maximum matching; $O(n^{\omega})$ randomized, where $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/).
- **Lower bound.** $\Omega(n + m)$, the size of the input, in the worst case. No better general bound is known.
- **Counting.** #P-complete. For bipartite graphs, there is a fully polynomial randomized approximation scheme for the number of perfect matchings, by Jerrum, Sinclair and Vigoda, since that number is a permanent of a nonnegative matrix; see [counting perfect matchings](/counting-perfect-matchings/).

## Reductions

- **To maximum matching.** $G$ has a perfect matching if and only if $\nu(G) = n/2$. The reverse direction, from maximum matching to perfect matching, adds new vertices; see [maximum matching](/maximum-matching/).
- **Bipartite case to max flow.** With unit capacities on $s \to L \to R \to t$, a perfect matching exists if and only if the [maximum flow](/max-flow-problem/) is $|L| = |R|$.
- **To a determinant.** $G$ has a perfect matching if and only if the determinant of its [Tutte matrix](/tutte-matrix/) is not the zero polynomial; for bipartite graphs the Edmonds matrix plays the same part.

## Applications

- **Assignment.** $n$ workers and $n$ jobs: can each worker get a job they can do? With costs, this is the [assignment problem](/assignment-problem/).
- **Chemistry and physics.** The perfect matchings of the graph of a molecule are its Kekulé structures, and in statistical physics they are the dimer coverings of a lattice.
- **Edge coloring.** A $k$-regular bipartite graph splits into $k$ perfect matchings, by repeated use of the regular case above, so its edges can be colored with $k$ colors.
- **Routing and tours.** [Christofides' algorithm](/christofides-algorithm/) and the [Chinese postman problem](/chinese-postman-problem/) need a [minimum-weight perfect matching](/minimum-weight-perfect-matching/) on the odd-degree vertices.

## References
