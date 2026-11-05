---
tag: 7TA0S6
kind: algorithm
slug: rnc-perfect-matching
name: Randomized parallel perfect matching
aliases:
- Mulmuley-Vazirani-Vazirani algorithm
- RNC matching
area: graphs/matching
level: research
summary: Decides and finds perfect matchings in randomized NC using the Tutte matrix determinant.
solves: [perfect-matching]
model: crew-pram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: "O(n^(7/2) m log^2 n)"}
  space: {extra: "O(n^3 (m + log n))"}
  depth: {expected: O(log^2 n)}
properties: {deterministic: false, recursive: false}
history:
  year: 1987
  people: [Ketan Mulmuley, Umesh Vazirani, Vijay Vazirani]
  note: Mulmuley, Vazirani and Vazirani isolated one minimum-weight perfect matching with random weights and read it off one matrix inversion, a simpler route than the first randomized NC algorithm of Karp, Upfal and Wigderson.
prereqs: [perfect-matching, tutte-matrix, determinant]
see_also: [tutte-matrix, schwartz-zippel-lemma, matrix-inversion, berkowitz-algorithm, maximum-matching, minimum-weight-perfect-matching, monte-carlo-algorithm, counting-perfect-matchings]
sources:
  - paper: doi:10.1007/BF02579206
    title: Ketan Mulmuley, Umesh V. Vazirani and Vijay V. Vazirani, Matching is as easy as matrix inversion, Combinatorica 7(1), 105 to 113 (1987)
    locator: the whole paper (the isolating lemma, the two lemmas on the 2-adic value of the determinant and of the cofactors, and the parallel algorithm)
  - paper: doi:10.1007/BF02579407
    title: Richard M. Karp, Eli Upfal and Avi Wigderson, Constructing a perfect matching is in random NC, Combinatorica 6(1), 35 to 48 (1986)
    locator: the whole paper (the first randomized NC algorithm for constructing a perfect matching)
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press
    locator: Chapter 12, Parallel and Distributed Algorithms (the isolating lemma and the parallel algorithm for perfect matchings)
  - paper: "László Lovász, On determinants, matchings, and random algorithms, Fundamentals of Computation Theory (FCT 1979), Akademie-Verlag Berlin, 565 to 574 (1979)"
    locator: the whole paper (the randomized decision test by the Tutte matrix)
---

The randomized parallel perfect matching algorithm of Mulmuley, Vazirani and Vazirani (MVV) finds a [perfect matching](/perfect-matching/) of a general graph without weights in $O(\log^2 n)$ parallel time with a polynomial number of processors. It puts random weights on the edges, so that with probability at least $1/2$ exactly one perfect matching has the least weight. Then one [determinant](/determinant/) and one [matrix inversion](/matrix-inversion/) of a weighted [Tutte matrix](/tutte-matrix/) tell, for every edge at once, whether it is in that matching. Both steps are in NC, so the whole algorithm is in randomized NC. It is the standard example of the *isolation lemma*.

## In plain words

A graph has many perfect matchings, and a parallel algorithm cannot easily agree on one of them. Many processors working at once would pick edges from different matchings.

The trick is to make one matching special. Give each edge a random whole number as its weight. With good chance, exactly one perfect matching has the smallest total weight. Now build a matrix from the graph in which each edge appears as two to the power of its weight. Its determinant is a sum with one term per pair of perfect matchings, and the special matching gives the term with the fewest factors of two. So the number of factors of two in the determinant reveals the smallest weight. A second matrix computation then checks each edge separately: it is in the special matching exactly when a certain number is odd. All edges are checked at the same time.

## The problem

The input is a finite undirected graph $G = (V, E)$, general (odd cycles allowed) and without weights, with vertices $1, \ldots, n$ and $m$ edges. The output is a perfect matching of $G$, or "none". The empty graph has the empty perfect matching. A graph with an odd number of vertices, or with no perfect matching for another reason, gives "none".

The algorithm is a [Monte Carlo algorithm](/monte-carlo-algorithm/) with one-sided error: a matching it returns is checked and always correct, and "none" is always correct if $G$ has no perfect matching. If $G$ has one, each trial finds a perfect matching with probability at least $1/2$, so after $k$ independent trials the chance of a wrong "none" is at most $2^{-k}$. Run until success, it is a [Las Vegas algorithm](/las-vegas-algorithm/) for graphs known to have a perfect matching, with at most 2 trials expected.

## The algorithm

For a weight $w(ij) \ge 1$ on each edge, let $B$ be the $n \times n$ matrix with $B_{ij} = 2^{w(ij)}$ and $B_{ji} = -2^{w(ij)}$ for each edge $ij$ with $i < j$, and 0 elsewhere. It is the [Tutte matrix](/tutte-matrix/) with $2^{w(ij)}$ in place of the variable $x_{ij}$. Write $\nu_2(D)$ for the largest $t$ such that $2^t$ divides the integer $D \ne 0$.

```pseudo id=main
MVV(G = (V, E), k)
L1  repeat k times
L2      choose w(e) ∈ {1, …, 2m} uniformly and independently for each edge e
L3      build B: B[i][j] ← 2^w(ij), B[j][i] ← −2^w(ij) for each edge ij with i < j, 0 elsewhere
L4      D ← det(B);  if D = 0 then next trial
L5      W2 ← ν₂(D);  if W2 is odd then next trial          ▷ W2 = 2W when the minimum is unique
L6      A ← adj(B), the adjugate, so that A[j][i] = ±det(B with row i and column j removed)
L7      M ← {ij ∈ E : |A[j][i]| · 2^w(ij) / 2^W2 is an odd integer}
L8      if M is a perfect matching of G then return M
L9  return "none"
```

Lines L2 to L7 are the parallel part: each entry, the determinant and the adjugate are computed in $O(\log^2 n)$ depth, and line L7 tests all edges at once. Line L8 is a check that also runs in $O(\log n)$ depth.

**Why it works.** The Pfaffian of $B$ is $\operatorname{Pf}(B) = \sum_M \pm 2^{w(M)}$, one term for each perfect matching $M$, where $w(M)$ is its total weight, and $\det B = \operatorname{Pf}(B)^2$. If exactly one perfect matching $M_0$ has the least weight $W$, then $\operatorname{Pf}(B) = 2^W \cdot (\text{odd})$, because every other term is divisible by $2^{W+1}$. So $\nu_2(\det B) = 2W$. For an edge $ij$, the cofactor satisfies $|A_{ji}| \, 2^{w(ij)} = |\operatorname{Pf}(B)| \cdot |\sum_{M \ni ij} \pm 2^{w(M)}|$, a sum over the perfect matchings that contain $ij$. That sum is $2^W$ times an odd number if $ij \in M_0$, and divisible by $2^{W+1}$ otherwise. So line L7 selects exactly the edges of $M_0$.

**The isolation lemma.** Let $\mathcal F$ be any family of subsets of a set of $m$ elements, and give each element a weight chosen uniformly from $\{1, \ldots, N\}$. Then the probability that exactly one set of $\mathcal F$ has the least total weight is at least $1 - m/N$. With $N = 2m$ and $\mathcal F$ the perfect matchings of $G$, this is at least $1/2$.

## Example

Take the 4-cycle $1 - 2 - 3 - 4 - 1$ with the chord $13$. Its perfect matchings are $\{12, 34\}$ and $\{14, 23\}$; the chord is in none. Suppose the weights are $w(12) = 1$, $w(23) = 2$, $w(34) = 3$, $w(14) = 4$ and $w(13) = 5$. The matchings weigh $1 + 3 = 4$ and $2 + 4 = 6$, so the least weight $W = 4$ is reached once.

$$B = \begin{pmatrix} 0 & 2 & 32 & 16 \\ -2 & 0 & 4 & 0 \\ -32 & -4 & 0 & 8 \\ -16 & 0 & -8 & 0 \end{pmatrix}, \qquad \operatorname{Pf}(B) = B_{12}B_{34} - B_{13}B_{24} + B_{14}B_{23} = 16 - 0 + 64 = 80.$$

So $\det B = 6400 = 2^8 \cdot 25$, and $\nu_2 = 8 = 2W$. The test of line L7 gives:

| edge | $\lvert A_{ji} \rvert$ | $\lvert A_{ji} \rvert \cdot 2^{w} / 2^8$ | odd? |
|---|---|---|---|
| 12 | 640 | $1280 / 256 = 5$ | yes |
| 34 | 160 | $1280 / 256 = 5$ | yes |
| 23 | 1280 | $5120 / 256 = 20$ | no |
| 14 | 320 | $5120 / 256 = 20$ | no |
| 13 | 0 | 0 | no |

The output is $\{12, 34\}$, the matching of least weight.

**No perfect matching.** For a triangle, or the 5-cycle, or a center joined by one edge to each of three triangles, the Pfaffian is a sum with no terms, so $\det B = 0$ for every choice of weights, every trial stops at line L4, and the answer is "none". These graphs have odd cycles; odd cycles are no problem for the method, which does not search for paths.

## Correctness

The full proof is below. It has three parts.

1. **The isolation lemma.** For an element $e$, let $a_e$ be the least weight of a set of $\mathcal F$ that avoids $e$, and $b_e$ the least weight, without $w(e)$, of a set that contains $e$. Both do not depend on $w(e)$. If two sets of $\mathcal F$ have the least weight, then some element $e$ is in one and not in the other, and then $w(e) = a_e - b_e$. For fixed other weights this has probability at most $1/N$, so the union over $m$ elements gives at most $m/N$.
2. **The 2-adic lemmas.** As above, when $M_0$ is unique, $\nu_2(\det B) = 2W$, and line L7 selects exactly $M_0$.
3. **One-sided error.** Line L8 returns only a checked perfect matching. If $G$ has no perfect matching, line L8 never succeeds and the answer is "none", which is correct. If $G$ has one, each trial succeeds when $M_0$ is unique, which happens with probability at least $1/2$, independently across trials.

## Complexity

The model is the CREW [PRAM](/crew-pram/).

- **Numbers.** Entries of $B$ have $O(m)$ bits. A cofactor is a sum of at most $n!$ products of $n - 1$ entries, so it has $O(n(m + \log n))$ bits. The $n^2$ entries of the adjugate take $O(n^3(m + \log n))$ bits in total, which is the space bound in the front matter, counted in bits.
- **Depth.** The determinant and the adjugate of an $n \times n$ integer matrix can be computed in $O(\log^2 n)$ depth, for example by Csanky's method or by [Berkowitz's algorithm](/berkowitz-algorithm/), on numbers of polynomial size. MVV state $O(\log^2 n)$ time with $O(n^{3.5} m)$ processors.
- **Trials.** At most 2 trials are expected when a perfect matching exists, and $k$ trials give error at most $2^{-k}$.
- **Sequential simulation.** The Python version uses exact integer and rational elimination, $O(n^3)$ arithmetic operations on numbers of $O(n(m + \log n))$ bits per trial. It is meant to show the method on small graphs, not to compete with [maximum matching](/maximum-matching/) algorithms.

## Properties

- **General graphs, unweighted.** Odd cycles need no special handling. The random weights are internal to the algorithm.
- **One-sided error, checkable output.** A returned matching is verified. A "none" is certain only if the graph has no perfect matching.
- **Not deterministic.** Whether perfect matching is in deterministic NC is open. Fenner, Gurjar and Thierauf showed in 2016 that bipartite perfect matching is in quasi-NC by derandomizing the isolation, and Svensson and Tarnawski extended this to general graphs in 2017.
- **Weighted extension.** If the edges have integer costs of polynomial size, multiply the costs by a large enough factor and add the random weights. The isolated matching then has the least cost, so a [minimum-weight perfect matching](/minimum-weight-perfect-matching/) is also found in randomized NC.

## Variants and improvements

- **Deciding only.** Lovász's test substitutes random values from a large field into the Tutte matrix and checks whether the determinant is nonzero. It decides existence but does not find a matching. See the [Tutte matrix](/tutte-matrix/) and the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/).
- **Karp-Upfal-Wigderson.** The first randomized NC algorithm for constructing a perfect matching, from 1985, was more involved.
- **Maximum matching.** Adding vertices joined to all others reduces maximum matching to perfect matching, so maximum matching is also in randomized NC.
- **Sequential algebraic matching.** Mucha and Sankowski find a maximum matching in $O(n^{\omega})$ randomized sequential time with Gaussian elimination on a random Tutte matrix; see [matrix multiplication exponent](/matrix-multiplication-exponent/).
- **Modular arithmetic.** Working modulo a random prime keeps the numbers short, at the price of a small extra error probability.

## When to use it

Use it to reason about parallel complexity: it shows that perfect matching is in randomized NC and is the model for other uses of the isolation lemma. For a sequential program, [Edmonds' blossom algorithm](/edmonds-blossom/) or the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) is faster and deterministic. For a quick randomized existence test, Lovász's test with a modular determinant is simpler.

## Pitfalls

- **Weights too small.** With weights from $\{1, \ldots, N\}$ and $N < m$, the bound $1 - m/N$ says nothing, and ties become likely. Use $N \ge 2m$.
- **Floating point.** The numbers $2^{w}$ are huge and the test is about divisibility by powers of 2, so floating point gives garbage. Use exact integers or work modulo a large prime with care.
- **Reading $\nu_2$ wrongly.** If the minimum is not unique, $\nu_2(\det B)$ can be odd or larger than $2W$, and line L7 can select a set of edges that is not a matching. Line L8 must check the result before returning it.
- **Index order in the adjugate.** $A_{ji}$, not $A_{ij}$, is the cofactor of the entry $(i, j)$. For a skew-symmetric matrix the two differ only in sign, so the absolute value hides the mistake here, but not in other uses.
- **Treating "none" as proof.** With a perfect matching present, $\det B$ can vanish by cancellation when the minimum is not unique, so one failed trial proves nothing. Only the bound $2^{-k}$ holds.

## Implementations

The Python version takes the number of vertices, a list of edges and an optional seeded random generator, and returns the partner of each vertex or None. It computes the determinant by Bareiss elimination over the integers and the adjugate by exact Gauss-Jordan elimination over the rationals. The tests check the determinant and adjugate against the permutation formula, and the whole method against a brute force on random graphs with up to 10 vertices.

## History

Tutte introduced the skew-symmetric matrix of a graph in 1947. Lovász observed in 1979 that random substitution gives a fast randomized test for perfect matchings, which also puts the decision problem in randomized NC. Constructing a matching in parallel was harder: Karp, Upfal and Wigderson gave the first randomized NC algorithm in 1985. In 1987 Mulmuley, Vazirani and Vazirani gave the simpler algorithm here, with the isolation lemma as its key tool; the title of their paper, "Matching is as easy as matrix inversion", states its main idea. The lemma later found many uses in complexity theory, and the question of a deterministic NC algorithm led to the quasi-NC results of 2016 and 2017.

## References
