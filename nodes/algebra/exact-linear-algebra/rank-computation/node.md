---
tag: 0PTXD7
kind: problem
slug: rank-computation
name: Rank computation
aliases: [matrix rank, computing the rank, rank of a matrix computation]
area: algebra/exact-linear-algebra
level: core
summary: Compute the rank of a matrix over a field or over the integers.
model: algebraic-computation-tree
complexity:
  vars: {m: the number of rows, n: the number of columns, r: the rank of A}
  time: {worst: "O(m n r^(ω-2))"}
prereqs: [rank, gaussian-elimination]
see_also: [nullspace-computation, reduced-row-echelon-form, gaussian-elimination-modular, wiedemann-algorithm, black-box-matrix, schwartz-zippel-lemma, tutte-matrix, tensor-rank]
sources:
  - paper: doi:10.1016/0196-6774(82)90007-4
    title: Oscar H. Ibarra, Shlomo Moran and Roger Hui, A generalization of the fast LUP matrix decomposition algorithm and applications, Journal of Algorithms 3(1), 1982
    locator: pp. 45 to 56 (the LSP decomposition of a matrix of any shape and rank, and the rank in O(m n r^(ω-2)) operations)
  - paper: "Arne Storjohann, Algorithms for Matrix Canonical Forms, PhD thesis, ETH Zurich, 2000"
    locator: Chapter 2, echelon forms over fields (rank, rank profile and reduced echelon form in O(n m r^(ω-2)) field operations)
  - paper: doi:10.1007/3-540-54522-0_93
    title: Erich Kaltofen and B. David Saunders, On Wiedemann's method of solving sparse linear systems, AAECC-9, Lecture Notes in Computer Science 539, 1991
    locator: pp. 29 to 38 (the rank of a black box matrix from the minimal polynomial of a preconditioned matrix, Monte Carlo)
  - paper: "Ho Yee Cheung, Tsz Chiu Kwok and Lap Chi Lau, Fast matrix rank algorithms and applications, Journal of the ACM 60(5), 2013"
    locator: the rank of an m by n matrix in about the number of nonzero entries plus r^ω field operations, randomized
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 5.5, Modular determinant computation (primes for which reduction is faithful, bounded with the Hadamard bound), and Section 12.4, Wiedemann's algorithm and black box linear algebra
---

Rank computation asks for the [rank](/rank/) $r$ of an $m \times n$ matrix $A$ over a field $K$: the largest number of linearly independent rows or columns. Elimination finds it in $O(m n r)$ field operations, and fast matrix multiplication gives $O(m n r^{\omega - 2})$. For an integer matrix, the rank over $\mathbb{Q}$ equals the rank modulo $p$ for all but a few primes $p$, so one elimination modulo a random prime gives a fast Monte Carlo algorithm whose only possible error is an answer that is too small.

## In plain words

The rank of a table of numbers counts how many of its rows are really new, in the sense that they cannot be built from the others by scaling and adding. Elimination finds it: clear the table into a staircase, and the number of steps is the rank.

With whole numbers you can avoid large fractions by doing the arithmetic with remainders modulo a prime. That can only lose rank, never gain it, and it loses rank only for the few primes that divide a certain determinant, so a random large prime almost always gives the right answer.

## Definition

**Notation.** $K$ is a field, $R$ an integral domain with field of fractions $K$ (usually $\mathbb{Z}$ and $\mathbb{Q}$), and $A$ an $m \times n$ matrix. $\omega$ is the exponent of matrix multiplication, and $b$ the maximum binary length of an entry of an integer matrix.

**Input.** An $m \times n$ matrix $A$ over $K$, or over $R$.

**Output.** The rank $r = \operatorname{rank}(A)$: the dimension of the column space, which equals the dimension of the row space and the largest order of a nonzero minor.

**Over an integral domain.** The rank of a matrix over $R$ is its rank over $K$. For $R = \mathbb{Z}$ it is also the rank of the lattice spanned by the columns.

**Modulo a prime.** For an integer matrix $A$ and a prime $p$, $\operatorname{rank}_p(A)$ is the rank of $A \bmod p$ over $\mathbb{F}_p$. Every minor of $A \bmod p$ is the reduction of a minor of $A$, so $\operatorname{rank}_p(A) \le \operatorname{rank}(A)$, with equality if and only if $p$ does not divide every $r \times r$ minor of $A$.

## Variants

- **Full rank decision.** Is $r = \min(m, n)$? For square $A$ this is $\det A \ne 0$; see [determinant computation](/determinant-computation/).
- **Rank profile.** The list of pivot columns of the [reduced row echelon form](/reduced-row-echelon-form/) (the column rank profile), or the lexicographically first set of independent rows (the row rank profile). Both come with elimination at the same cost.
- **Black box rank.** $A$ is given only by $v \mapsto A v$; see [black box matrix](/black-box-matrix/) and the [Wiedemann algorithm](/wiedemann-algorithm/).
- **Symbolic rank.** The entries are polynomials or indeterminates, and the rank is over the field of rational functions. Substituting random values gives it with high probability by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), and no deterministic polynomial-time algorithm is known in general (Edmonds' problem).
- **Rank over $\mathbb{Z}/N\mathbb{Z}$ or of a module.** Over a ring that is not a domain, several notions differ; the [Smith normal form](/smith-normal-form/) gives the complete answer.
- **Tensor rank.** For tensors of order $3$ and more, [tensor rank](/tensor-rank/) is NP-hard over $\mathbb{Q}$ (Hastad, 1990), which contrasts with matrices.
- **Numerical rank.** With floating point input, the rank is replaced by the number of singular values above a tolerance. That is a different, approximate problem.

## Examples

**A rank-deficient matrix.** $\begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}$ has rank $2$: row $3$ is $2 \cdot$ row $2 -$ row $1$, and the minor $\det \begin{pmatrix} 1 & 2 \\ 4 & 5 \end{pmatrix} = -3$ is not zero.

**Rank modulo primes.** For

$$A = \begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 10 \end{pmatrix}, \qquad \det A = -3,$$

$\operatorname{rank}(A) = 3$. Modulo $3$ the determinant vanishes and $\operatorname{rank}_3(A) = 2$, while $\operatorname{rank}_2(A) = 3$. The only prime that gives a wrong rank is $3$, the only prime factor of the $3 \times 3$ minor. For $\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}$, $\det = -2$ and the rank modulo $2$ is $1$.

**Edge cases.** The zero matrix and every $m \times 0$ or $0 \times n$ matrix have rank $0$; a $1 \times 1$ matrix $(a)$ has rank $1$ if $a \ne 0$.

## Known algorithms

- **Gaussian elimination.** Count the pivots of an [echelon form](/echelon-form/): $r$ pivot steps of $O(m n)$ field operations each, so $O(m n r + m n)$. Over $\mathbb{F}_2$, packing rows into machine words divides the cost by the word size; see [bitset Gaussian elimination](/bitset-gaussian-elimination/).
- **Fast elimination.** The LSP decomposition of Ibarra, Moran and Hui (1982) and the echelon form algorithms of Storjohann's thesis (Chapter 2) give the rank in $O(m n r^{\omega - 2})$ field operations.
- **Black box rank** (Kaltofen and Saunders, 1991). Precondition $A$ with random Toeplitz and diagonal matrices so that the minimal polynomial of the result reveals the rank, then run the [Wiedemann algorithm](/wiedemann-algorithm/): $O(n)$ products by $A$ and $O(n^2)$ further operations, Monte Carlo, over a field with enough elements.
- **Sparse and randomized rank** (Cheung, Kwok and Lau, 2013): about $\operatorname{nnz}(A) + r^\omega$ field operations, up to logarithmic factors, by random compression of the rows and columns.
- **Over $\mathbb{Z}$, deterministic.** Fraction-free elimination in the style of the [Bareiss algorithm](/bareiss-algorithm/), or elimination modulo enough primes that their product exceeds the Hadamard bound of the $r \times r$ minors.
- **Over $\mathbb{Z}$, Monte Carlo.** Elimination modulo one random prime, as in [modular Gaussian elimination](/gaussian-elimination-modular/). The answer is at most the true rank, and it is correct with the probability given below.

## Bounds

**Algebraic model.** $O(m n r^{\omega - 2})$ field operations suffice, which is $O(n^\omega)$ for square $n \times n$ input. The only general lower bound is the trivial $\Omega(m n)$ for reading a dense input. These are proved.

**Bit complexity over $\mathbb{Z}$.** Fraction-free elimination keeps every intermediate entry equal to a minor of order at most $r$, and by the [Hadamard bound](/hadamard-bound/) such a minor has absolute value at most $H = r^{r/2} 2^{r b}$, so at most $r (b + \tfrac12 \log_2 r)$ binary digits. The cost is $O(m n r)$ operations on integers of that length, that is $O(m n r^3 (b + \log r)^2)$ bit operations with schoolbook arithmetic. This bound is proved, and it is the reason for preferring fraction-free elimination to elimination with unreduced fractions, whose entries can double in length at each step.

**How many primes are bad.** Fix a nonzero $r \times r$ minor $\Delta$ of $A$. A prime $p$ with $\operatorname{rank}_p(A) < r$ divides $\Delta$, and $|\Delta| \le H$, so at most $\log_2 H$ primes are bad, and at most $\log_2 H / \log_2 P$ primes larger than $P$ are bad. Choosing $p$ uniformly among $2 \log_2 H$ primes gives the right rank with probability at least $1/2$, and choosing among $k \log_2 H$ primes with probability at least $1 - 1/k$. By the [prime number theorem](/prime-number-theorem/) such primes have $O(\log (r b))$ binary digits, so one elimination costs $O(m n r)$ operations on small numbers. These are proved bounds, and in practice a single random prime near $2^{31}$ or $2^{63}$ is almost never bad for moderate matrices, an observation that follows from the bound when $H$ is not huge.

## Reductions

- **Rank and nullspace.** $\operatorname{rank}(A) = n - \dim \ker A$, so [nullspace computation](/nullspace-computation/) gives the rank, and an echelon form gives both.
- **Rank to determinant.** For a square $A$, full rank is $\det A \ne 0$. In general, $\operatorname{rank}(A) \ge k$ if and only if some $k \times k$ minor is nonzero, and after multiplying by random matrices the leading $k \times k$ minor serves with high probability.
- **Matching to rank.** The size of a maximum matching in a graph is half the rank of its [Tutte matrix](/tutte-matrix/) with indeterminate entries (Lovasz, 1979), so random substitution and rank computation give a randomized matching algorithm in $O(n^\omega)$; see [maximum matching](/maximum-matching/).

## Applications

- **Solvability of linear systems.** $A x = c$ is solvable if and only if $\operatorname{rank}(A) = \operatorname{rank}(A \mid c)$.
- **Graph algorithms.** Matchings, vertex connectivity and linkage problems reduce to the rank of random substitutions of symbolic matrices.
- **Coding theory.** The dimension of a linear code is the rank of its generator matrix over $\mathbb{F}_q$, and the minimum distance is tied to the ranks of its column subsets.
- **Algebraic geometry and combinatorics.** Dimensions of spaces of polynomials, of homology groups (with the [Smith normal form](/smith-normal-form/) over $\mathbb{Z}$) and of matroids are ranks of large exact matrices.

## References
