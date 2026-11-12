---
tag: SWEZG3
kind: problem
slug: permanent-computation
name: Computing the permanent
aliases:
- permanent of a matrix
- matrix permanent
area: combinatorics/counting-algorithms
level: advanced
summary: 'Sums products of matrix entries over permutations; #P-hard in general.'
prereqs: [determinant, symmetric-group, perfect-matching, inclusion-exclusion-principle]
see_also: [ryser-formula, glynn-formula, counting-perfect-matchings, kasteleyn-method, determinant-computation, fpras, toda-theorem, derangement]
sources:
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8(2), 189 to 201, 1979
    locator: "the main theorem (the permanent of a 0-1 matrix is #P-complete) and the result on the permanent modulo powers of 2"
  - book: isbn:9780521006019
    title: J. H. van Lint and R. M. Wilson, A Course in Combinatorics, second edition, Cambridge University Press, 2001
    locator: Chapter 11, Permanents (Bregman's theorem); Chapter 12, The Van der Waerden conjecture
  - paper: doi:10.1145/1008731.1008738
    title: Mark Jerrum, Alistair Sinclair and Eric Vigoda, A polynomial-time approximation algorithm for the permanent of a matrix with nonnegative entries, Journal of the ACM 51(4), 671 to 697, 2004
    locator: the main theorem (an FPRAS for the permanent of a nonnegative matrix)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: the chapter on the permanent of a matrix (Ryser's formula evaluated in Gray code order)
---

Computing the permanent asks for $\operatorname{per}(A) = \sum_{\pi \in S_n} \prod_{i=1}^{n} a_{i \pi(i)}$ for an $n \times n$ matrix $A$. The formula is the [determinant](/determinant/) without the signs, but the two behave very differently. The determinant takes $O(n^3)$ operations by [Gaussian elimination](/gaussian-elimination/). The permanent has no such method: Valiant proved in 1979 that it is #P-complete, even for 0-1 matrices, where it counts the [perfect matchings](/counting-perfect-matchings/) of a bipartite graph. The best exact algorithms, [Ryser's formula](/ryser-formula/) and [Glynn's formula](/glynn-formula/), take $O(2^n n)$ operations. For nonnegative matrices there is an [FPRAS](/fpras/), by Jerrum, Sinclair and Vigoda.

## In plain words

Take a square table of numbers. Pick one number from each row so that no two picks share a column, and multiply the picks. Do this for every possible way of picking, and add up all the results. That sum is the permanent.

When the table holds only zeros and ones, the permanent counts the ways to pair the rows with the columns using only the ones. A close cousin, the determinant, uses the same sum with some terms subtracted, and it is fast to compute. The permanent has no known fast method, and there is strong evidence that none exists. The best exact methods take time that doubles with each extra row. For tables with no negative numbers, a random method gives a close estimate quickly.

## Definition

Notation: $A = (a_{ij})$ is an $n \times n$ matrix over a commutative ring (usually the integers, the rationals or the reals), $S_n$ is the [symmetric group](/symmetric-group/) on $[n] = \{1, \ldots, n\}$, $J$ is the all-ones matrix and $I$ the identity.

**Problem.** Input: an $n \times n$ matrix $A$. Output:

$$\operatorname{per}(A) = \sum_{\pi \in S_n} \prod_{i=1}^{n} a_{i \pi(i)}.$$

The permanent of the $0 \times 0$ matrix is 1.

**Basic properties.** For all $A$:

- $\operatorname{per}(A)$ does not change when rows or columns are permuted, or when $A$ is transposed.
- It is linear in each row and in each column.
- *Expansion.* $\operatorname{per}(A) = \sum_{j=1}^{n} a_{1j} \operatorname{per}(A_{1j})$, where $A_{1j}$ is $A$ without row 1 and column $j$. This is the Laplace expansion without signs.
- It is *not* multiplicative: $\operatorname{per}(AB) \ne \operatorname{per}(A) \operatorname{per}(B)$ in general, and adding a multiple of one row to another changes it. This is why elimination does not work.

*Proof of the expansion.* Group the permutations by $j = \pi(1)$. The rest of $\pi$ is a bijection from rows $2, \ldots, n$ to the columns other than $j$, which is a term of $\operatorname{per}(A_{1j})$. $\square$

**Combinatorial meaning.** If $A$ is a 0-1 matrix, $\operatorname{per}(A)$ is the number of permutations $\pi$ with $a_{i \pi(i)} = 1$ for all $i$. These are the perfect matchings of the bipartite graph with biadjacency matrix $A$, and also the placements of $n$ non-attacking rooks on the allowed cells.

## Variants

- **0-1 matrices.** The counting case. It is #P-complete (Valiant).
- **Nonnegative matrices.** Approximation within a factor $1 \pm \varepsilon$ has an FPRAS (Jerrum, Sinclair and Vigoda, 2004).
- **Modulo 2.** $\operatorname{per}(A) \equiv \det(A) \pmod 2$, since $-1 \equiv 1$, so it takes $O(n^3)$ operations. Valiant showed that the permanent modulo any fixed power of 2 also takes polynomial time.
- **Rectangular matrices.** For $m \times n$ with $m \le n$, sum over the injections from rows to columns.
- **Hafnian.** The hafnian of a symmetric matrix sums over perfect matchings of $K_{2m}$ instead of permutations; it counts the perfect matchings of general graphs, and $\operatorname{per}(B) = \operatorname{haf} \begin{pmatrix} 0 & B \\ B^T & 0 \end{pmatrix}$.
- **Algebraic complexity.** As a polynomial in $n^2$ variables, the permanent is complete for Valiant's class VNP, and the determinant is complete for VP (under a suitable notion of reduction). Whether VP $\ne$ VNP is the algebraic analog of P versus NP.

## Examples

**A $3 \times 3$ matrix.** For $A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$, the expansion along the first row gives

$$\operatorname{per}(A) = 1 \cdot (5 \cdot 9 + 6 \cdot 8) + 2 \cdot (4 \cdot 9 + 6 \cdot 7) + 3 \cdot (4 \cdot 8 + 5 \cdot 7) = 93 + 156 + 201 = 450,$$

while $\det(A) = 0$.

**All ones.** $\operatorname{per}(J_n) = n!$.

**Derangements.** $\operatorname{per}(J_n - I_n)$ counts the permutations with no fixed point, the [derangements](/derangement/). For $n = 0, \ldots, 10$: 1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496, 1334961 (OEIS A000166).

**Ménage numbers.** Let $P_n$ be the cyclic shift, with ones at $(i, i+1 \bmod n)$. Then $\operatorname{per}(J_n - I_n - P_n)$ counts the permutations with $\pi(i) \ne i$ and $\pi(i) \ne i + 1 \pmod n$. For $n = 3, \ldots, 11$: 1, 2, 13, 80, 579, 4738, 43387, 439792, 4890741 (OEIS A000179).

## Known algorithms

- **Definition.** Sum over all $n!$ permutations, $O(n! \, n)$ operations.
- **Expansion with memoization.** Let $f(S)$ be the permanent of the submatrix with rows $1, \ldots, |S|$ and columns $S$. Then $f(S) = \sum_{j \in S} a_{|S|, j} f(S \setminus \{j\})$, which gives $O(2^n n)$ operations and $O(2^n)$ space.
- **Ryser's formula.** $\operatorname{per}(A) = (-1)^n \sum_{S \subseteq [n]} (-1)^{|S|} \prod_{i=1}^{n} \sum_{j \in S} a_{ij}$, by inclusion-exclusion. With a Gray code over $S$ it takes $O(2^n n)$ operations and $O(n)$ space. See [Ryser's formula](/ryser-formula/).
- **Glynn's formula.** $\operatorname{per}(A) = 2^{-(n-1)} \sum_{\delta} \left(\prod_k \delta_k\right) \prod_{j=1}^{n} \sum_{i=1}^{n} \delta_i a_{ij}$, over $\delta \in \{\pm 1\}^n$ with $\delta_1 = 1$. Also $O(2^n n)$ with a Gray code, with half the terms of Ryser. See [Glynn's formula](/glynn-formula/).
- **Sparse and structured matrices.** For 0-1 matrices with few ones per row, branching on the rows or a dynamic program over a tree decomposition of the bipartite graph is faster. For planar bipartite graphs, [Kasteleyn's method](/kasteleyn-method/) gives a determinant.
- **Approximation for nonnegative matrices.** The JSV algorithm is an FPRAS: it runs a Markov chain on perfect and near-perfect matchings, with weights tuned by simulated annealing. Deterministic approximation within a factor of $e^n$ follows from matrix scaling and the Van der Waerden bound (Linial, Samorodnitsky and Wigderson).

## Bounds

**Hardness.** The permanent of 0-1 matrices is #P-complete (Valiant, 1979). By [Toda's theorem](/toda-theorem/), a polynomial-time algorithm for it would put the whole polynomial hierarchy in P. The fastest known exact algorithms take $2^{n - o(n)}$ time.

**Value bounds.**

- $|\operatorname{per}(A)| \le \prod_{i=1}^{n} \sum_{j=1}^{n} |a_{ij}|$, since expanding the right side gives every term of the permanent, in absolute value, and more.
- *Bregman.* For a 0-1 matrix with row sums $r_1, \ldots, r_n$, $\operatorname{per}(A) \le \prod_i (r_i!)^{1/r_i}$.
- *Van der Waerden (Egorychev, Falikman).* For a doubly stochastic matrix $D$, $\operatorname{per}(D) \ge n! / n^n$, with equality only for $D = J_n / n$.

## Reductions

- **To perfect matchings.** A 0-1 permanent is the number of perfect matchings of a bipartite graph, and back.
- **From #SAT.** Valiant's proof builds, from a 3-CNF formula, an integer matrix whose permanent is a fixed multiple of the number of satisfying assignments, then removes the negative and large entries.
- **To the determinant, in special cases.** If the 0-1 matrix is the biadjacency matrix of a planar bipartite graph, a sign pattern makes every term of the determinant positive, so $\operatorname{per}$ is $|\det|$ of the signed matrix.

## Applications

- Counting perfect matchings, permutations with restricted positions (derangements, ménage problem) and [Latin squares](/counting-latin-squares/).
- Physics: the amplitudes of non-interacting bosons are permanents of submatrices of a unitary matrix, the basis of boson sampling.
- Complexity theory: the central #P-complete problem, used to show other counting problems hard.

## References
